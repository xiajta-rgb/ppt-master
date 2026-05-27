// State
let collections = collectionsData;
let currentCollection = null;
let currentSlide = 0;
let deleteHistory = [];
let lastDeletedToast = null;
let isFullscreen = false;
let dropdownOpen = false;
let viewMode = 'normal';
let lastCheckTime = 0;
let hotReloadEnabled = true;
let slideUpdateTimeout = null;
let saveSvgTimeout = null;
let isSlideUpdating = false;
let pendingSlideIndex = null;
let isEditMode = false;
let editingElement = null;
let currentEditingSlidePath = null;
let undoStack = [];
let redoStack = [];
const MAX_UNDO = 50;
const svgCache = new Map();

let selectedImage = null;
let selectedImages = [];
let selectedPlaceholderRect = null;
let selectionBoxes = [];
let resizeHandles = [];
let isDragging = false;
let isResizing = false;
let dragStartX = 0;
let dragStartY = 0;
let imageStartX = 0;
let imageStartY = 0;
let imageStartPositions = [];
let resizeHandle = null;
let resizeStartX = 0;
let resizeStartY = 0;
let imageStartWidth = 0;
let imageStartHeight = 0;
let alignmentGuides = [];
let snapThreshold = 5;
let propertiesPanel = null;
let pasteImageMode = false;

// Hot reload check
let hotReloadInFlight = false;
let hotReloadSeq = 0;
async function checkForChanges() {
    if (!hotReloadEnabled || hotReloadInFlight) return;
    hotReloadInFlight = true;
    const seq = ++hotReloadSeq;
    try {
        const response = await fetch('/api/check-changes', { cache: 'no-store' });
        if (seq !== hotReloadSeq) { hotReloadInFlight = false; return; }
        if (!response.ok) {
            hotReloadEnabled = false;
            hotReloadInFlight = false;
            return;
        }
        const data = await response.json();
        if (seq !== hotReloadSeq) { hotReloadInFlight = false; return; }
        if (data.changed && data.timestamp > lastCheckTime) {
            lastCheckTime = data.timestamp;
            showHotReloadNotification(data.files);
        }
    } catch (e) {
        if (seq !== hotReloadSeq) { hotReloadInFlight = false; return; }
        hotReloadEnabled = false;
    } finally {
        if (seq === hotReloadSeq) hotReloadInFlight = false;
    }
}

function showHotReloadNotification(changedFiles) {
    let notification = document.getElementById('hot-reload-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'hot-reload-notification';
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 cursor-pointer';
        notification.onclick = () => location.reload();
        document.body.appendChild(notification);
    }
    notification.innerHTML = `🔄 ${changedFiles.length} 个文件已更新，点击刷新`;
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 10000);
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadDynamicCollections();
    renderCollections();

    hotReloadEnabled = true;
    setInterval(checkForChanges, 3000);

    // Setup image upload handler
    const fileInput = document.getElementById('imageUploadInput');
    if (fileInput) {
        fileInput.addEventListener('change', onImageFileSelected);
    }

    // Setup clipboard paste handler for images
    document.addEventListener('paste', handleClipboardPaste);

    const urlParams = new URLSearchParams(window.location.search);
    const collectionId = urlParams.get('project');
    if (collectionId) {
        let collection = collections.find(c => c.id === collectionId);
        if (!collection) collection = collections.find(c => c.alias === collectionId);
        if (!collection) collection = collections.find(c => c.id.includes(collectionId) || (c.alias && c.alias.includes(collectionId)));
        if (collection) openCollection(collection);
    }
});

async function loadDynamicCollections() {
    try {
        const res = await fetch('/api/scan-projects');
        if (!res.ok) return;

        const data = await res.json();
        const staticMap = new Map(collections.map(c => [c.id, c]));
        const staticAliasMap = new Map(collections.map(c => [c.alias, c]).filter(([k]) => k));

        collections = data.projects.map(p => {
            const staticData = staticMap.get(p.id) || staticAliasMap.get(p.alias?.[0]) || staticMap.get(p.alias?.[0]);
            let slides;
            if (staticData?.slides?.length) {
                slides = p.slides.map(s => {
                    const staticSlide = staticData.slides.find(ss => ss.file === s.file);
                    return staticSlide || { file: s.file, title: s.file.replace('.svg', ''), desc: '' };
                });
            } else {
                slides = p.slides.map(s => ({
                    file: s.file,
                    title: s.file.replace('.svg', ''),
                    desc: ''
                }));
            }
            return {
                id: p.id,
                seqId: staticData?.seqId || '',
                alias: p.alias?.[0] || '',
                title: staticData?.title || parseProjectTitle(p.id),
                description: staticData?.description || `Project: ${p.id}`,
                icon: staticData?.icon || '📊',
                color: staticData?.color || '#6366f1',
                folder: staticData?.folder || p.folder,
                slides: slides
            };
        });

        const apiIds = new Set(data.projects.map(p => p.id));
        for (const c of staticMap.values()) {
            if (!apiIds.has(c.id) && !apiIds.has(c.alias)) {
                collections.push(c);
            }
        }
    } catch (e) {
    }
}

function parseProjectTitle(dirName) {
    const parts = dirName.split('_');
    if (parts.length >= 3) return parts.slice(2).join('_');
    return dirName;
}

const categoryKeywords = {
    'consulting': ['咨询', '报告', '分析', '区域', '市场'],
    'tech': ['AI', '技术', '科技', 'Claude', 'Anthropic', 'Gemini', '代理', 'Agent'],
    'market': ['市场', '营销', '服装', '策略', '战术'],
    'academic': ['学术', '研究', '论文', '科学', '理论']
};

function getCategoryFromTitle(title) {
    const lowerTitle = title.toLowerCase();
    for (const [category, keywords] of Object.entries(categoryKeywords)) {
        if (keywords.some(kw => lowerTitle.includes(kw.toLowerCase()))) return category;
    }
    return 'consulting';
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return '';
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

let currentCategory = 'all';
let searchQuery = '';
let filteredCollections = [];

function filterCollections() {
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearSearch');
    searchQuery = searchInput.value.trim().toLowerCase();
    clearBtn.classList.toggle('hidden', !searchQuery);
    applyFilters();
}

function clearSearch() {
    document.getElementById('searchInput').value = '';
    document.getElementById('clearSearch').classList.add('hidden');
    searchQuery = '';
    applyFilters();
}

function setCategory(category) {
    currentCategory = category;
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('bg-brand-500', 'text-white');
        btn.classList.add('bg-white/10', 'text-white/70');
    });
    document.getElementById(`cat-${category}`).classList.remove('bg-white/10', 'text-white/70');
    document.getElementById(`cat-${category}`).classList.add('bg-brand-500', 'text-white');
    applyFilters();
}

function applyFilters() {
    filteredCollections = collections.filter(c => {
        const matchSearch = !searchQuery ||
            c.title.toLowerCase().includes(searchQuery) ||
            c.description.toLowerCase().includes(searchQuery) ||
            (c.alias && c.alias.toLowerCase().includes(searchQuery));
        const matchCategory = currentCategory === 'all' || getCategoryFromTitle(c.title) === currentCategory;
        return matchSearch && matchCategory;
    });
    renderFilteredCollections();
    updateResultsCount();
}

function updateResultsCount() {
    const countEl = document.getElementById('resultsCount');
    const infoEl = document.getElementById('resultsInfo');
    if (countEl) countEl.textContent = filteredCollections.length;
    if (infoEl) {
        if (searchQuery || currentCategory !== 'all') {
            infoEl.classList.remove('hidden');
        } else {
            infoEl.classList.add('hidden');
        }
    }
}

function renderCollections() {
    filteredCollections = [...collections];
    renderFilteredCollections();
    updateResultsCount();
}

function renderFilteredCollections() {
    const grid = document.getElementById('collectionsGrid');
    const emptyState = document.getElementById('emptyState');

    if (filteredCollections.length === 0) {
        grid.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');
    grid.innerHTML = filteredCollections.map(collection => {
        const firstSlide = collection.slides && collection.slides[0];
        const coverPath = firstSlide ? '/' + encodePath(`${collection.folder}/${firstSlide.file}`) : '';
        const slideCount = collection.slides ? collection.slides.length : 0;
        const category = getCategoryFromTitle(collection.title);
        const categoryLabels = {
            'consulting': '咨询',
            'tech': '科技',
            'market': '市场',
            'academic': '学术'
        };
        const categoryColors = {
            'consulting': 'bg-purple-500/20 text-purple-300 border border-purple-500/30',
            'tech': 'bg-blue-500/20 text-blue-300 border border-blue-500/30',
            'market': 'bg-green-500/20 text-green-300 border border-green-500/30',
            'academic': 'bg-orange-500/20 text-orange-300 border border-orange-500/30'
        };

        return `
        <div class="collection-card cursor-pointer group" onclick='openCollection(${JSON.stringify(collection).replace(/'/g, "&#39;")})'>
            <div class="relative h-48 bg-dark-900 overflow-hidden">
                ${firstSlide ? `
                    <img src="${coverPath}" class="w-full h-full object-contain p-4 transition-transform duration-300 group-hover:scale-105" loading="lazy" alt="${collection.title}"
                        onerror="this.parentElement.innerHTML='<div class=\\'flex items-center justify-center h-full text-gray-600\\'><i class=\\'fas fa-image text-4xl\\'></i></div>'">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                ` : `<div class="flex items-center justify-center h-full text-gray-600"><i class="fas fa-image text-4xl"></i></div>`}
                <div class="absolute top-3 left-3">
                    <span class="seq-id-badge">${extractSeqNumber(collection.seqId) || '--'}</span>
                </div>
                <div class="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
                    <span class="px-2 py-1 bg-white/10 backdrop-blur-sm rounded text-xs text-gray-200 border border-white/10">
                        <i class="fas fa-eye mr-1"></i>View
                    </span>
                </div>
            </div>
            <div class="p-5">
                <div class="flex items-start justify-between mb-2">
                    <h3 class="font-bold text-gray-100 text-lg leading-tight pr-2">${collection.title}</h3>
                </div>
                <p class="text-gray-400 text-sm mb-3 line-clamp-2">${collection.description}</p>
                <div class="flex items-center justify-between text-xs text-gray-500">
                    <div class="flex items-center gap-3">
                        <span class="flex items-center gap-1">
                            <i class="fas fa-file-alt"></i>
                            ${slideCount} slides
                        </span>
                        <span class="flex items-center gap-1">
                            <i class="fas fa-layer-group"></i>
                            ${categoryLabels[category]}
                        </span>
                    </div>
                </div>
                <div class="mt-3 flex flex-wrap gap-1">
                    <span class="px-2 py-0.5 ${categoryColors[category]} rounded text-xs">${categoryLabels[category]}</span>
                </div>
            </div>
        </div>
    `}).join('');

    renderDropdown();
}

function extractSeqNumber(seqId) {
    if (!seqId) return '';
    const match = seqId.match(/(\d+)$/);
    return match ? match[1] : seqId;
}

function renderDropdown() {
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.innerHTML = collections.map(collection => `
        <div class="flex items-center px-4 py-3 hover:bg-white/5 cursor-pointer transition-colors ${currentCollection?.id === collection.id ? 'bg-white/5' : ''}"
             onclick='switchCollection(${JSON.stringify(collection).replace(/'/g, "&#39;")})'>
            <span class="seq-id-badge mr-3">${extractSeqNumber(collection.seqId)}</span>
            <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-100 truncate">${collection.title}</p>
                <p class="text-xs text-gray-500">${collection.slides.length} slides</p>
            </div>
            ${currentCollection?.id === collection.id ? '<i class="fas fa-check text-brand-400"></i>' : ''}
        </div>
    `).join('');
}

function toggleDropdown() {
    dropdownOpen = !dropdownOpen;
    document.getElementById('dropdownMenu').classList.toggle('hidden', !dropdownOpen);
}

document.addEventListener('click', (e) => {
    if (!e.target.closest('#collectionSelector')) {
        dropdownOpen = false;
        document.getElementById('dropdownMenu').classList.add('hidden');
    }
});

function openCollection(collection) {
    currentCollection = collection;
    currentSlide = 0;

    const projectId = collection.alias || collection.id;
    const url = new URL(window.location);
    url.searchParams.set('project', projectId);
    window.history.pushState({}, '', url);

    document.getElementById('libraryView').classList.add('hidden');
    document.getElementById('viewerView').classList.remove('hidden');
    document.getElementById('collectionSelector').classList.remove('hidden');
    document.getElementById('keyboardHints').classList.add('hidden');
    document.getElementById('keyboardHints').classList.remove('flex');
    document.getElementById('keyboardHintsHeader').classList.remove('hidden');
    document.getElementById('keyboardHintsHeader').classList.add('flex');
    document.getElementById('mainContent').classList.add('viewer-expanded');

    setViewMode('normal');

    document.getElementById('currentCollectionIcon').textContent = extractSeqNumber(collection.seqId) || '--';
    document.getElementById('currentCollectionName').textContent = collection.title;

    document.getElementById('viewerTitle').innerHTML = `<span class="seq-id-badge" style="vertical-align: middle;">${extractSeqNumber(collection.seqId) || '--'}</span> ${collection.title}`;
    document.getElementById('viewerDescription').textContent = collection.description;
    document.getElementById('totalPages').textContent = collection.slides.length;
    document.getElementById('fullscreenTotal').textContent = collection.slides.length;

    document.getElementById('progressBar').style.background = '#4a4a5a';

    generateThumbnails();
    generateOverview();
    updateSlide();
    renderDropdown();

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function switchCollection(collection) {
    toggleDropdown();
    openCollection(collection);
}

function backToLibrary() {
    currentCollection = null;

    const url = new URL(window.location);
    url.searchParams.delete('project');
    window.history.pushState({}, '', url);

    document.getElementById('libraryView').classList.remove('hidden');
    document.getElementById('viewerView').classList.add('hidden');
    document.getElementById('collectionSelector').classList.add('hidden');
    document.getElementById('keyboardHints').classList.add('hidden');
    document.getElementById('keyboardHints').classList.remove('flex');
    document.getElementById('keyboardHintsHeader').classList.add('hidden');
    document.getElementById('keyboardHintsHeader').classList.remove('flex');
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('mainContent').classList.remove('viewer-expanded');
    document.getElementById('slideViewerContainer').classList.remove('theater-mode');

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setViewMode(mode) {
    viewMode = mode;
    const container = document.getElementById('slideViewerContainer');
    const normalBtn = document.getElementById('normalModeBtn');
    const theaterBtn = document.getElementById('theaterModeBtn');

    if (mode === 'theater') {
        container.classList.add('theater-mode');
        normalBtn.classList.remove('active');
        theaterBtn.classList.add('active');
    } else {
        container.classList.remove('theater-mode');
        normalBtn.classList.add('active');
        theaterBtn.classList.remove('active');
    }
}

function toggleViewMode() {
    setViewMode(viewMode === 'normal' ? 'theater' : 'normal');
}

function toggleEditMode() {
    if (!localStorage.getItem('authToken')) {
        showToast('请先登录', 'error');
        const loginModal = document.getElementById('loginModal');
        if (loginModal) loginModal.style.display = 'flex';
        return;
    }
    isEditMode = !isEditMode;
    const toolbar = document.getElementById('editToolbar');
    const editHint = document.getElementById('editHint');
    const slideContainer = document.getElementById('slideContainer');

    if (isEditMode) {
        toolbar.classList.remove('hidden');
        editHint.classList.remove('hidden');
        slideContainer.classList.add('edit-mode');
        const svgEl = document.querySelector('#slideWrapper svg');
        if (svgEl) {
            setupTextEditListeners(svgEl);
            setupImageEditListeners();
        }
    } else {
        toolbar.classList.add('hidden');
        editHint.classList.add('hidden');
        slideContainer.classList.remove('edit-mode');
        removeEditOverlay();
        clearImageSelection();
        saveCurrentSvg(true);
    }
}

function setupTextEditListeners(svgEl) {
    if (!svgEl) return;

    const textElements = svgEl.querySelectorAll('text, tspan');
    textElements.forEach((el, index) => {
        if (el.dataset.editListener) return;

        const textContent = el.textContent.trim();
        const isImagePlaceholder = /^\[.*\]/.test(textContent) && /图|image|photo|示意图|图片/i.test(textContent);

        if (isImagePlaceholder) {
            el.style.cursor = 'pointer';
            el.dataset.imagePlaceholder = 'true';
            el.addEventListener('click', (e) => {
                if (!isEditMode) return;
                e.stopPropagation();
                removeEditOverlay();
                showImageUploadDialog(el);
            });
        } else {
            el.style.cursor = 'text';
            el.addEventListener('dblclick', (e) => {
                if (!isEditMode) return;
                e.stopPropagation();
                showTextEditOverlay(el, index);
            });
        }

        el.dataset.editListener = 'true';
    });
}

function showTextEditOverlay(textElement, elementIndex) {
    const existing = document.getElementById('textEditOverlay');
    if (existing) existing.remove();

    const rect = textElement.getBoundingClientRect();
    const slideWrapper = document.getElementById('slideWrapper');
    const wrapperRect = slideWrapper.getBoundingClientRect();

    const overlay = document.createElement('div');
    overlay.id = 'textEditOverlay';
    overlay.className = 'absolute bg-dark-900/95 backdrop-blur rounded-lg shadow-2xl z-50 p-4 w-80 border border-white/10';
    overlay.style.cssText = `
        left: ${rect.left - wrapperRect.left + slideWrapper.scrollLeft}px;
        top: ${rect.top - wrapperRect.top + slideWrapper.scrollTop}px;
        min-width: 200px;
    `;

    const originalText = textElement.getAttribute('data-original-text') || textElement.textContent;
    textElement.setAttribute('data-original-text', originalText);
    editingElement = textElement;

    overlay.innerHTML = `
        <div class="flex justify-between items-center mb-3">
            <h4 class="font-semibold text-gray-100 text-sm">Edit Text</h4>
            <button onclick="removeEditOverlay()" class="text-gray-400 hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <textarea id="textEditInput" class="w-full p-3 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 resize-none focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
            rows="3" placeholder="Enter text...">${originalText}</textarea>
        <div class="flex justify-end gap-2 mt-3">
            <button onclick="removeEditOverlay()" class="px-3 py-1.5 text-sm text-gray-400 hover:bg-white/5 rounded-lg">Cancel</button>
            <button onclick="saveTextEdit(editingElement, document.getElementById('textEditInput').value, ${elementIndex})"
                class="px-3 py-1.5 text-sm bg-brand-500 text-white rounded-lg hover:bg-brand-600">Save</button>
        </div>
    `;

    slideWrapper.style.position = 'relative';
    slideWrapper.appendChild(overlay);

    const textarea = document.getElementById('textEditInput');
    textarea.focus();
    textarea.select();

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.max(60, this.scrollHeight) + 'px';
        updatePreview();
    });

    updatePreview();
}

function updatePreview() {
    if (!editingElement || !currentEditingSlidePath) return;
}

function removeEditOverlay() {
    const existing = document.getElementById('textEditOverlay');
    if (existing) existing.remove();
    editingElement = null;
}

function showImageUploadDialog(placeholderEl) {
    const existing = document.getElementById('imageUploadDialog');
    if (existing) existing.remove();

    const rect = placeholderEl.getBoundingClientRect();
    const slideWrapper = document.getElementById('slideWrapper');
    const wrapperRect = slideWrapper.getBoundingClientRect();

    const dialog = document.createElement('div');
    dialog.id = 'imageUploadDialog';
    dialog.className = 'absolute bg-dark-900/95 backdrop-blur rounded-lg shadow-2xl z-[60] p-4 w-96 border border-blue-500/30';
    dialog.style.cssText = `
        left: ${Math.max(0, rect.left - wrapperRect.left + slideWrapper.scrollLeft - 80)}px;
        top: ${Math.max(0, rect.top - wrapperRect.top + slideWrapper.scrollTop - 50)}px;
    `;

    const placeholderText = placeholderEl.textContent.trim();
    const x = parseFloat(placeholderEl.getAttribute('x') || 0);
    const y = parseFloat(placeholderEl.getAttribute('y') || 0);
    const fontSize = parseFloat(placeholderEl.getAttribute('font-size') || 14);
    const estimatedWidth = placeholderText.length * fontSize * 0.6;
    const estimatedHeight = fontSize * 1.5;

    dialog.innerHTML = `
        <div class="flex justify-between items-center mb-3">
            <h4 class="font-semibold text-gray-100 text-sm">Upload Image</h4>
            <button id="closeUploadDialog" class="text-gray-400 hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="mb-3 p-3 bg-white/5 rounded-lg text-xs text-gray-400">
            <div>Placeholder: ${placeholderText.substring(0, 50)}...</div>
            <div class="mt-1">Position: (${Math.round(x)}, ${Math.round(y)})</div>
        </div>
        <div class="space-y-3">
            <div>
                <label class="block text-xs text-gray-400 mb-1">Upload Mode</label>
                <div class="flex gap-2">
                    <button id="singleUploadBtn" class="flex-1 px-3 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                        <i class="fas fa-image mr-1"></i> Single
                    </button>
                    <button id="batchUploadBtn" class="flex-1 px-3 py-2 text-sm bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                        <i class="fas fa-images mr-1"></i> Batch
                    </button>
                </div>
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1">Image Width (px)</label>
                <input id="imageWidthInput" type="number" value="${Math.round(estimatedWidth)}" min="50" max="1920"
                    class="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100" />
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1">Image Height (px)</label>
                <input id="imageHeightInput" type="number" value="${Math.round(estimatedHeight * 3)}" min="50" max="1080"
                    class="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100" />
            </div>
            <input type="file" id="imageFileInput" accept="image/*" multiple class="hidden" />
        </div>
    `;

    slideWrapper.style.position = 'relative';
    slideWrapper.appendChild(dialog);

    const fileInput = dialog.querySelector('#imageFileInput');
    const singleBtn = dialog.querySelector('#singleUploadBtn');
    const batchBtn = dialog.querySelector('#batchUploadBtn');
    const closeBtn = dialog.querySelector('#closeUploadDialog');

    const openFilePicker = (multiple) => {
        fileInput.multiple = multiple;
        fileInput.click();
    };

    singleBtn.addEventListener('click', () => openFilePicker(false));
    batchBtn.addEventListener('click', () => openFilePicker(true));
    closeBtn.addEventListener('click', () => dialog.remove());

    fileInput.addEventListener('change', async (e) => {
        const files = Array.from(e.target.files);
        if (files.length === 0) return;

        const imgWidth = parseInt(dialog.querySelector('#imageWidthInput').value) || 400;
        const imgHeight = parseInt(dialog.querySelector('#imageHeightInput').value) || 300;

        dialog.remove();
        showToast(`Processing ${files.length} image(s)...`, 'info');

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            try {
                const base64 = await readFileAsBase64(file);
                const offsetX = i * 20;
                const offsetY = i * 20;
                replacePlaceholderWithImage(placeholderEl, base64, x + offsetX, y + offsetY, imgWidth, imgHeight);
            } catch (err) {
                showToast(`Failed to process ${file.name}: ${err.message}`, 'error');
            }
        }

        await saveCurrentSvg();
        showToast(`${files.length} image(s) added`, 'success');
    });
}

function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function replacePlaceholderWithImage(placeholderEl, base64Data, x, y, width, height) {
    const svgEl = placeholderEl.closest('svg');
    if (!svgEl) return;

    const containerRect = findImageContainer(placeholderEl);
    let clipId = null;
    if (containerRect) {
        clipId = `clip_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        addClipPathToContainer(svgEl, containerRect, clipId);
    }

    const imageEl = document.createElementNS('http://www.w3.org/2000/svg', 'image');
    imageEl.setAttribute('x', x);
    imageEl.setAttribute('y', y);
    imageEl.setAttribute('width', width);
    imageEl.setAttribute('height', height);
    imageEl.setAttribute('href', base64Data);
    imageEl.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    imageEl.style.cursor = 'move';

    if (clipId) {
        imageEl.setAttribute('clip-path', `url(#${clipId})`);
        imageEl.dataset.containerClipId = clipId;
    }

    if (containerRect) {
        imageEl.dataset.containerX = containerRect.getAttribute('x') || 0;
        imageEl.dataset.containerY = containerRect.getAttribute('y') || 0;
        imageEl.dataset.containerWidth = containerRect.getAttribute('width') || 0;
        imageEl.dataset.containerHeight = containerRect.getAttribute('height') || 0;
    }

    placeholderEl.parentNode.insertBefore(imageEl, placeholderEl.nextSibling);

    placeholderEl.style.opacity = '0.3';
    placeholderEl.textContent = '[ Image Added ]';

    if (isEditMode) {
        imageEl.dataset.imageEditListener = 'true';
        imageEl.setAttribute('pointer-events', 'all');
        imageEl.addEventListener('mousedown', onImageMouseDown);
    }

    checkImageOutOfBounds(imageEl);
}

function findImageContainer(element) {
    let sibling = element.previousElementSibling;
    while (sibling) {
        if (sibling.tagName === 'rect' && sibling.getAttribute('stroke-dasharray')) {
            return sibling;
        }
        sibling = sibling.previousElementSibling;
    }
    return null;
}

function addClipPathToContainer(svgEl, containerRect, clipId) {
    let defs = svgEl.querySelector('defs');
    if (!defs) {
        defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        svgEl.insertBefore(defs, svgEl.firstChild);
    }

    const clipPath = document.createElementNS('http://www.w3.org/2000/svg', 'clipPath');
    clipPath.setAttribute('id', clipId);

    const clipRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    clipRect.setAttribute('x', containerRect.getAttribute('x') || 0);
    clipRect.setAttribute('y', containerRect.getAttribute('y') || 0);
    clipRect.setAttribute('width', containerRect.getAttribute('width') || 0);
    clipRect.setAttribute('height', containerRect.getAttribute('height') || 0);

    clipPath.appendChild(clipRect);
    defs.appendChild(clipPath);
}

function checkImageOutOfBounds(imageEl) {
    const containerX = parseFloat(imageEl.dataset.containerX || 0);
    const containerY = parseFloat(imageEl.dataset.containerY || 0);
    const containerW = parseFloat(imageEl.dataset.containerWidth || 0);
    const containerH = parseFloat(imageEl.dataset.containerHeight || 0);

    if (!containerW || !containerH) return;

    const imgX = parseFloat(imageEl.getAttribute('x') || 0);
    const imgY = parseFloat(imageEl.getAttribute('y') || 0);
    const imgW = parseFloat(imageEl.getAttribute('width') || 0);
    const imgH = parseFloat(imageEl.getAttribute('height') || 0);

    const hasAnyPartInside = !(
        imgX + imgW < containerX ||
        imgX > containerX + containerW ||
        imgY + imgH < containerY ||
        imgY > containerY + containerH
    );

    if (hasAnyPartInside) {
        imageEl.style.opacity = '1';
        delete imageEl.dataset.outOfBounds;
        const clipId = imageEl.dataset.containerClipId;
        if (clipId) {
            imageEl.setAttribute('clip-path', `url(#${clipId})`);
        }
    } else {
        imageEl.style.opacity = '0';
        imageEl.dataset.outOfBounds = 'complete';
        imageEl.removeAttribute('clip-path');
    }
}

function showOutOfBoundsIndicator(imageEl) {
    removeOutOfBoundsIndicator();

    if (!imageEl || imageEl.dataset.outOfBounds !== 'complete') return;

    const svgEl = imageEl.closest('svg');
    const slideWrapper = document.getElementById('slideWrapper');
    if (!svgEl || !slideWrapper) return;

    const svgRect = svgEl.getBoundingClientRect();
    const wrapperRect = slideWrapper.getBoundingClientRect();

    const imgScreenRect = imageEl.getBoundingClientRect();

    const indicator = document.createElement('div');
    indicator.id = 'outOfBoundsIndicator';
    indicator.className = 'absolute border-2 border-red-500 z-30 cursor-pointer';
    indicator.style.cssText = `
        left: ${imgScreenRect.left - wrapperRect.left}px;
        top: ${imgScreenRect.top - wrapperRect.top}px;
        width: ${imgScreenRect.width}px;
        height: ${imgScreenRect.height}px;
        border-style: dashed;
        pointer-events: auto;
        animation: pulse-red 1.5s ease-in-out infinite;
    `;

    indicator.addEventListener('mousedown', (e) => {
        e.stopPropagation();
    });

    indicator.addEventListener('click', (e) => {
        e.stopPropagation();
        selectImage(imageEl);
        removeOutOfBoundsIndicator();
        if (imageEl.style.opacity === '0') {
            imageEl.style.opacity = '0.5';
        }
    });

    slideWrapper.style.position = 'relative';
    slideWrapper.appendChild(indicator);
}

function removeOutOfBoundsIndicator() {
    const indicator = document.getElementById('outOfBoundsIndicator');
    if (indicator) indicator.remove();
}

async function doSaveCurrentSvg() {
    if (!currentEditingSlidePath) return;
    const token = localStorage.getItem('authToken');
    if (!token) {
        showToast('请先登录', 'error');
        return;
    }

    try {
        const svgEl = document.querySelector('#slideWrapper svg');
        if (!svgEl) return;

        const clone = svgEl.cloneNode(true);

        clone.removeAttribute('class');
        clone.removeAttribute('data-slide-path');
        clone.removeAttribute('style');

        clone.querySelectorAll('[data-edit-listener]').forEach(el => {
            el.removeAttribute('data-edit-listener');
            el.removeAttribute('data-image-placeholder');
            el.removeAttribute('data-img-placeholder');
            el.removeAttribute('data-original-text');
            el.style.cursor = '';
            el.style.opacity = '';
            if (el.style.cssText === '') el.removeAttribute('style');
        });

        clone.querySelectorAll('[data-image-edit-listener]').forEach(el => {
            el.removeAttribute('data-image-edit-listener');
            el.removeAttribute('data-overlay-listener');
            el.removeAttribute('pointer-events');
            el.removeAttribute('data-container-x');
            el.removeAttribute('data-container-y');
            el.removeAttribute('data-container-width');
            el.removeAttribute('data-container-height');
            el.removeAttribute('data-container-clip-id');
            el.removeAttribute('data-out-of-bounds');
            el.removeAttribute('data-img-placeholder');
            el.removeAttribute('data-img-placeholder-checked');
            el.style.opacity = '';
            el.style.cursor = '';
            if (el.style.cssText === '') el.removeAttribute('style');
        });

        clone.querySelectorAll('[data-img-placeholder]').forEach(el => {
            el.removeAttribute('data-img-placeholder');
            el.removeAttribute('data-img-placeholder-checked');
            el.removeAttribute('pointer-events');
            el.style.cursor = '';
            if (el.style.cssText === '') el.removeAttribute('style');
        });

        // Clean up placeholder groups
        clone.querySelectorAll('g.image-placeholder-group').forEach(el => {
            el.removeAttribute('data-overlay-listener');
            el.removeAttribute('data-image-edit-listener');
        });

        clone.querySelectorAll('[data-resize-handle]').forEach(el => el.remove());

        const svgContent = new XMLSerializer().serializeToString(clone);

        const response = await fetch('/api/save-svg', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                file: decodeURIComponent(currentEditingSlidePath.replace(/.*\//, '')),
                folder: decodeURIComponent(currentEditingSlidePath.replace(/\/[^/]+$/, '')).replace(/.*examples/, 'examples'),
                content: svgContent
            })
        });

        const data = await response.json();
        if (!response.ok || !data.success) {
            console.error('Save failed:', data.error);
        } else {
            svgCache.delete(currentEditingSlidePath);
        }
    } catch (err) {
        console.error('Save error:', err);
    }
}

async function saveCurrentSvg(immediate) {
    if (!currentEditingSlidePath) return;

    if (saveSvgTimeout) {
        clearTimeout(saveSvgTimeout);
        saveSvgTimeout = null;
    }

    if (immediate) {
        await doSaveCurrentSvg();
    } else {
        saveSvgTimeout = setTimeout(() => doSaveCurrentSvg(), 300);
    }
}

function showToast(message, type = 'success') {
    const existing = document.getElementById('toastNotification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'toastNotification';
    toast.className = `fixed bottom-6 right-6 px-6 py-3 rounded-lg shadow-xl z-50 flex items-center space-x-3 transform transition-all duration-300 translate-y-0 opacity-0`;

    const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500';
    const icon = type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';

    toast.innerHTML = `
        <i class="fas ${icon} text-white text-lg"></i>
        <span class="text-white font-medium">${message}</span>
    `;
    toast.classList.add(bgColor);

    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-0', 'opacity-0');
    });

    setTimeout(() => {
        toast.classList.add('translate-y-0', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function saveTextEdit(textElement, newText, elementIndex) {
    if (!editingElement) return;
    if (!localStorage.getItem('authToken')) {
        showToast('请先登录', 'error');
        return;
    }

    const slidePath = currentEditingSlidePath;
    const originalText = textElement.getAttribute('data-original-text') || textElement.textContent;

    if (!newText || newText === originalText) {
        removeEditOverlay();
        return;
    }

    textElement.textContent = newText;
    removeEditOverlay();

    undoStack.push({
        type: 'text',
        slidePath: slidePath,
        elementIndex: elementIndex,
        data: {
            oldText: originalText,
            newText: newText,
            elementIndex: elementIndex
        },
        timestamp: Date.now()
    });
    if (undoStack.length > MAX_UNDO) undoStack.shift();
    redoStack = [];

    try {
        const response = await fetch('/api/edit-svg', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                file: decodeURIComponent(slidePath.replace(/.*\//, '')),
                folder: decodeURIComponent(slidePath.replace(/\/[^/]+$/, '')).replace(/.*examples/, 'examples'),
                oldText: originalText,
                newText: newText,
                elementIndex: elementIndex
            })
        });

        const text = await response.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch {
            showToast('Server error: ' + (text.substring(0, 100) || 'Invalid response'), 'error');
            return;
        }

        if (response.ok && data.success) {
            showToast('Text updated successfully', 'success');
            if (slidePath) svgCache.delete(slidePath);
        } else {
            showToast(data.error || 'Failed to save changes', 'error');
        }
    } catch (err) {
        console.error('Save error:', err);
        showToast('Network error: ' + err.message, 'error');
    }
}

function setupImageEditListeners() {
    const slideWrapper = document.getElementById('slideWrapper');
    if (!slideWrapper) return;

    const svgEl = slideWrapper.querySelector('svg');
    if (!svgEl) return;

    document.querySelectorAll('.image-placeholder-overlay').forEach(el => el.remove());

    const viewBox = svgEl.viewBox.baseVal;
    const svgW = viewBox.width || 1280;
    const svgH = viewBox.height || 720;

    const allRects = svgEl.querySelectorAll('rect');
    const imagePlaceholders = [];

    allRects.forEach(rect => {
        if (rect.dataset.imgPlaceholder === 'true') return;
        if (rect.style.display === 'none') return;

        const w = parseFloat(rect.getAttribute('width') || 0);
        const h = parseFloat(rect.getAttribute('height') || 0);
        const fill = rect.getAttribute('fill') || '';
        const stroke = rect.getAttribute('stroke') || '';
        const rx = rect.getAttribute('rx') || rect.getAttribute('ry') || '';

        if (w < 80 || h < 80) return;
        if (w >= svgW * 0.95 && h >= svgH * 0.95) return;
        if (!stroke) return;

        const isDarkFill = /^#[0-3]/i.test(fill) || fill === 'none';
        if (!isDarkFill && !rx) return;

        const parent = rect.parentElement;
        const hasImageSibling = parent && parent.querySelector('image');
        if (hasImageSibling) return;

        const nextEl = rect.nextElementSibling;
        if (nextEl && nextEl.tagName && nextEl.tagName.toLowerCase() === 'image') return;

        imagePlaceholders.push(rect);
    });

    console.log(`[Edit] Found ${imagePlaceholders.length} image placeholder rects`);

    imagePlaceholders.forEach((rect, idx) => {
        rect.setAttribute('pointer-events', 'all');
        rect.style.cursor = 'pointer';
        rect.dataset.imgPlaceholder = 'true';

        let el = rect.parentElement;
        while (el && el !== svgEl) {
            if (el.setAttribute) {
                el.setAttribute('pointer-events', 'all');
            }
            el = el.parentElement;
        }

        rect.addEventListener('click', function(e) {
            if (!isEditMode) return;
            e.stopPropagation();
            e.preventDefault();
            console.log('[Edit] Placeholder rect clicked:', rect);
            selectPlaceholderRect(rect);
        });

        rect.addEventListener('mousedown', function(e) {
            if (!isEditMode) return;
            e.stopPropagation();
            e.preventDefault();
            console.log('[Edit] Placeholder rect mousedown:', rect);
            selectPlaceholderRect(rect);
        });

        const overlay = document.createElement('div');
        overlay.className = 'image-placeholder-overlay';
        overlay.innerHTML = '<span class="upload-text">📷 点击上传 / Ctrl+V 粘贴</span>';
        overlay.style.cssText = `
            position: absolute;
            pointer-events: none;
            font-size: 14px;
            color: #8C8C8C;
            text-align: center;
            white-space: nowrap;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            background: rgba(0,0,0,0.3);
            border-radius: 4px;
            border: 1px dashed rgba(140,140,140,0.4);
        `;
        slideWrapper.appendChild(overlay);

        const textSpan = overlay.querySelector('.upload-text');
        textSpan.style.pointerEvents = 'auto';
        textSpan.style.cursor = 'pointer';
        textSpan.style.padding = '6px 12px';
        textSpan.style.borderRadius = '4px';
        textSpan.style.fontSize = '13px';
        textSpan.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            if (!isEditMode) return;
            selectPlaceholderRect(rect);
            window._uploadTargetRect = rect;
            document.getElementById('imageUploadInput').click();
        });

        rect._overlayEl = overlay;
        rect._slideWrapper = slideWrapper;
        rect._svgEl = svgEl;
        updateOverlayPosition(rect);
    });

    const images = svgEl.querySelectorAll('image');
    console.log(`[Edit] Found ${images.length} image elements`);
    
    images.forEach((img, idx) => {
        if (img.dataset.imageEditListener) return;
        img.dataset.imageEditListener = 'true';
        img.style.cursor = 'move';
        img.setAttribute('pointer-events', 'all');
        img.addEventListener('mousedown', onImageMouseDown);

        if (!img.dataset.containerX) {
            detectImageContainerBounds(img);
        }
        checkImageOutOfBounds(img);
    });

    const placeholderGroups = svgEl.querySelectorAll('g.image-placeholder-group');
    placeholderGroups.forEach((group, idx) => {
        group.removeAttribute('data-overlay-listener');
        group.removeAttribute('data-image-edit-listener');
        group.dataset.imageEditListener = 'true';
        group.style.cursor = 'move';
        group.setAttribute('pointer-events', 'all');
        
        const rect = group.querySelector('rect');
        if (rect) {
            rect.setAttribute('pointer-events', 'all');
            rect.addEventListener('mousedown', onImageMouseDown);

            const overlay = document.createElement('div');
            overlay.className = 'image-placeholder-overlay';
            overlay.innerHTML = '<span class="upload-text">📷 点击上传 / Ctrl+V 粘贴</span>';
            overlay.style.cssText = `
                position: absolute;
                pointer-events: none;
                font-size: 14px;
                color: #8C8C8C;
                text-align: center;
                white-space: nowrap;
                user-select: none;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 100;
                background: rgba(0,0,0,0.3);
                border-radius: 4px;
                border: 1px dashed rgba(140,140,140,0.4);
            `;
            slideWrapper.appendChild(overlay);

            const textSpan = overlay.querySelector('.upload-text');
            textSpan.style.pointerEvents = 'auto';
            textSpan.style.cursor = 'pointer';
            textSpan.style.padding = '6px 12px';
            textSpan.style.borderRadius = '4px';
            textSpan.style.fontSize = '13px';
            textSpan.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                if (!isEditMode) return;
                selectPlaceholderRect(rect);
                window._uploadTargetRect = rect;
                window._uploadTargetGroup = group;
                document.getElementById('imageUploadInput').click();
            });

            rect._overlayEl = overlay;
            rect._slideWrapper = slideWrapper;
            rect._svgEl = svgEl;
            updateOverlayPosition(rect);
        }
    });

    if (!slideWrapper.dataset.slideWrapperEditListener) {
        slideWrapper.dataset.slideWrapperEditListener = 'true';
        slideWrapper.addEventListener('mousedown', onSlideWrapperMouseDown);
    }

    if (!window._overlayResizeListener) {
        window._overlayResizeListener = true;
        window.addEventListener('resize', () => {
            const svg = document.querySelector('#slideWrapper svg');
            if (svg) {
                svg.querySelectorAll('rect[data-img-placeholder]').forEach(r => {
                    if (r._overlayEl) updateOverlayPosition(r);
                });
                svg.querySelectorAll('g.image-placeholder-group rect').forEach(r => {
                    if (r._overlayEl) updateOverlayPosition(r);
                });
            }
        });
    }
}

function selectPlaceholderRect(rect) {
    clearImageSelection();
    removeOutOfBoundsIndicator();
    
    selectedPlaceholderRect = rect;
    pasteImageMode = true;

    const boundingRect = rect.getBoundingClientRect();
    const slideWrapper = document.getElementById('slideWrapper');
    const wrapperRect = slideWrapper.getBoundingClientRect();
    slideWrapper.style.position = 'relative';

    const box = document.createElement('div');
    box.id = 'imageSelectionBox';
    box.className = 'absolute border-2 border-green-500 z-40 paste-ready';
    box.style.cssText = `
        left: ${boundingRect.left - wrapperRect.left}px;
        top: ${boundingRect.top - wrapperRect.top}px;
        width: ${boundingRect.width}px;
        height: ${boundingRect.height}px;
        pointer-events: none;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.5);
    `;
    slideWrapper.appendChild(box);
    selectionBoxes.push(box);

    rect.style.fill = '#1a3a1a';
    rect.style.stroke = '#22c55e';
    rect.style.strokeWidth = '2';

    showPasteHint();
    updatePropertiesPanel();
}

function updateOverlayPosition(rect) {
    if (!rect._overlayEl || !rect._slideWrapper || !rect._svgEl) return;

    const boundingRect = rect.getBoundingClientRect();
    const slideRect = rect._slideWrapper.getBoundingClientRect();

    const overlayLeft = boundingRect.left - slideRect.left;
    const overlayTop = boundingRect.top - slideRect.top;
    const overlayWidth = boundingRect.width;
    const overlayHeight = boundingRect.height;

    rect._overlayEl.style.left = overlayLeft + 'px';
    rect._overlayEl.style.top = overlayTop + 'px';
    rect._overlayEl.style.width = overlayWidth + 'px';
    rect._overlayEl.style.height = overlayHeight + 'px';
}

function setupImagePlaceholderOverlays() {
    const slideWrapper = document.getElementById('slideWrapper');
    if (!slideWrapper) return;

    const svgEl = slideWrapper.querySelector('svg');
    if (!svgEl) return;

    document.querySelectorAll('.image-placeholder-overlay').forEach(el => el.remove());

    const viewBox = svgEl.viewBox.baseVal;
    const svgW = viewBox.width || 1280;
    const svgH = viewBox.height || 720;

    const allRects = svgEl.querySelectorAll('rect');
    const imagePlaceholders = [];

    allRects.forEach(rect => {
        if (rect.dataset.imgPlaceholder === 'true') return;
        if (rect.style.display === 'none') return;

        const w = parseFloat(rect.getAttribute('width') || 0);
        const h = parseFloat(rect.getAttribute('height') || 0);
        const fill = rect.getAttribute('fill') || '';
        const stroke = rect.getAttribute('stroke') || '';
        const rx = rect.getAttribute('rx') || rect.getAttribute('ry') || '';

        if (w < 80 || h < 80) return;
        if (w >= svgW * 0.95 && h >= svgH * 0.95) return;
        if (!stroke) return;

        const isDarkFill = /^#[0-3]/i.test(fill) || fill === 'none';
        if (!isDarkFill && !rx) return;

        const parent = rect.parentElement;
        const hasImageSibling = parent && parent.querySelector('image');
        if (hasImageSibling) return;

        const nextEl = rect.nextElementSibling;
        if (nextEl && nextEl.tagName && nextEl.tagName.toLowerCase() === 'image') return;

        imagePlaceholders.push(rect);
    });

    imagePlaceholders.forEach((rect, idx) => {
        rect.dataset.imgPlaceholder = 'true';
        rect.setAttribute('pointer-events', 'all');

        const overlay = document.createElement('div');
        overlay.className = 'image-placeholder-overlay';
        overlay.innerHTML = '<span class="upload-text">📷 上传图片</span>';
        overlay.style.cssText = `
            position: absolute;
            pointer-events: none;
            font-size: 18px;
            color: #8C8C8C;
            text-align: center;
            white-space: nowrap;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            background: rgba(255,255,255,0.05);
            border-radius: 4px;
        `;
        slideWrapper.appendChild(overlay);

        const textSpan = overlay.querySelector('.upload-text');
        textSpan.style.pointerEvents = 'auto';
        textSpan.style.cursor = 'pointer';
        textSpan.style.padding = '8px 16px';
        textSpan.style.borderRadius = '4px';
        textSpan.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            window._uploadTargetRect = rect;
            document.getElementById('imageUploadInput').click();
        });

        rect._overlayEl = overlay;
        rect._slideWrapper = slideWrapper;
        rect._svgEl = svgEl;
        updateOverlayPosition(rect);
    });

    const placeholderGroups = svgEl.querySelectorAll('g.image-placeholder-group');
    console.log(`[Overlay] Found ${placeholderGroups.length} placeholder groups, ${imagePlaceholders.length} auto-detected placeholders`);
    
    placeholderGroups.forEach((group, idx) => {
        group.removeAttribute('data-overlay-listener');
        group.dataset.overlayListener = 'true';
        
        const rect = group.querySelector('rect');
        if (rect) {
            rect.setAttribute('pointer-events', 'all');

            const overlay = document.createElement('div');
            overlay.className = 'image-placeholder-overlay';
            overlay.innerHTML = '<span class="upload-text">📷 上传图片</span>';
            overlay.style.cssText = `
                position: absolute;
                pointer-events: none;
                font-size: 18px;
                color: #8C8C8C;
                text-align: center;
                white-space: nowrap;
                user-select: none;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 100;
                background: rgba(255,255,255,0.05);
                border-radius: 4px;
            `;
            slideWrapper.appendChild(overlay);

            const textSpan = overlay.querySelector('.upload-text');
            textSpan.style.pointerEvents = 'auto';
            textSpan.style.cursor = 'pointer';
            textSpan.style.padding = '8px 16px';
            textSpan.style.borderRadius = '4px';
            textSpan.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                window._uploadTargetRect = rect;
                window._uploadTargetGroup = group;
                document.getElementById('imageUploadInput').click();
            });

            rect._overlayEl = overlay;
            rect._slideWrapper = slideWrapper;
            rect._svgEl = svgEl;
            updateOverlayPosition(rect);
        }
    });

    if (!window._overlayResizeListener) {
        window._overlayResizeListener = true;
        window.addEventListener('resize', () => {
            const svgEl = document.querySelector('#slideWrapper svg');
            if (svgEl) {
                svgEl.querySelectorAll('rect[data-img-placeholder]').forEach(rect => {
                    if (rect._overlayEl) updateOverlayPosition(rect);
                });
                svgEl.querySelectorAll('g.image-placeholder-group rect').forEach(rect => {
                    if (rect._overlayEl) updateOverlayPosition(rect);
                });
            }
        });
    }
}

function onUploadTriggerClick(e) {
    e.stopPropagation();
    e.preventDefault();
    
    const group = e.target.closest('g.image-placeholder-group');
    if (!group) return;
    
    const rect = group.querySelector('rect');
    if (!rect) return;
    
    // Store the target rect for upload
    window._uploadTargetRect = rect;
    window._uploadTargetGroup = group;
    
    // Trigger file input
    const fileInput = document.getElementById('imageUploadInput');
    if (fileInput) {
        fileInput.value = ''; // Reset to allow re-upload
        fileInput.click();
    }
}

async function onImageFileSelected(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const rect = window._uploadTargetRect;
    const group = window._uploadTargetGroup;
    
    try {
        const base64Data = await readFileAsBase64(file);
        
        if (pasteImageMode && selectedPlaceholderRect && !rect) {
            await insertImageToPlaceholder(selectedPlaceholderRect, base64Data);
            return;
        }
        
        if (pasteImageMode && selectedImage && !rect) {
            await replaceSelectedImage(base64Data);
            return;
        }
        
        if (rect && rect.dataset.imgPlaceholder) {
            await insertImageToPlaceholder(rect, base64Data);
            window._uploadTargetRect = null;
            window._uploadTargetGroup = null;
            return;
        }
        
        if (!rect || !group) return;
        
        const x = parseFloat(rect.getAttribute('x') || 0);
        const y = parseFloat(rect.getAttribute('y') || 0);
        const width = parseFloat(rect.getAttribute('width') || 400);
        const height = parseFloat(rect.getAttribute('height') || 300);
        
        const svgEl = rect.closest('svg');
        const ns = 'http://www.w3.org/2000/svg';
        const img = document.createElementNS(ns, 'image');
        img.setAttribute('x', x);
        img.setAttribute('y', y);
        img.setAttribute('width', width);
        img.setAttribute('height', height);
        img.setAttribute('href', base64Data);
        img.setAttribute('preserveAspectRatio', 'xMidYMid slice');
        img.setAttribute('pointer-events', 'all');
        img.style.cursor = 'move';
        
        rect.parentNode.insertBefore(img, rect);
        
        rect.style.display = 'none';
        
        const trigger = group.querySelector('text.upload-trigger');
        if (trigger) {
            trigger.style.display = 'none';
        }
        
        img.addEventListener('mousedown', onImageMouseDown);
        
        saveCurrentSvg(true);
        
        window._uploadTargetRect = null;
        window._uploadTargetGroup = null;
    } catch (err) {
        console.error('Image upload failed:', err);
    }
}

function detectImageContainerBounds(img) {
    if (img.dataset.containerX) return;

    let sibling = img.previousElementSibling;
    while (sibling) {
        if (sibling.tagName === 'rect' && sibling.getAttribute('stroke-dasharray')) {
            img.dataset.containerX = sibling.getAttribute('x') || 0;
            img.dataset.containerY = sibling.getAttribute('y') || 0;
            img.dataset.containerWidth = sibling.getAttribute('width') || 0;
            img.dataset.containerHeight = sibling.getAttribute('height') || 0;

            if (!img.dataset.containerClipId) {
                let clipId = `clip_existing_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
                addClipPathToContainer(img.closest('svg'), sibling, clipId);
                img.setAttribute('clip-path', `url(#${clipId})`);
                img.dataset.containerClipId = clipId;
            }
            break;
        }
        sibling = sibling.previousElementSibling;
    }
}

function onImageMouseDown(e) {
    if (!isEditMode) return;
    
    if (e.target.classList.contains('upload-trigger')) {
        return;
    }
    
    e.stopPropagation();
    e.preventDefault();

    let target = null;
    let el = e.target;
    while (el) {
        if (el.tagName && (el.tagName.toLowerCase() === 'image' || el.tagName === 'image')) {
            target = el;
            break;
        }
        if (el.classList && el.classList.contains('image-placeholder-group')) {
            target = el;
            break;
        }
        el = el.parentElement;
    }
    
    if (!target) {
        if (e.target.tagName && e.target.tagName.toLowerCase() === 'rect') {
            const parent = e.target.parentElement;
            if (parent && parent.classList && parent.classList.contains('image-placeholder-group')) {
                target = parent;
            }
        }
    }
    
    if (!target) return;

    const img = (target.tagName && target.tagName.toLowerCase() === 'g') ? target.querySelector('rect') || target : target;

    if (e.shiftKey) {
        toggleImageSelection(img);
    } else {
        if (selectedImages.length > 1 && selectedImages.includes(img)) {
            selectImages(selectedImages);
        } else {
            selectImage(img);
        }
    }

    isDragging = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    imageStartX = parseFloat(selectedImage.getAttribute('x') || 0);
    imageStartY = parseFloat(selectedImage.getAttribute('y') || 0);
    imageStartPositions = selectedImages.map(el => ({
        el,
        x: parseFloat(el.getAttribute('x') || 0),
        y: parseFloat(el.getAttribute('y') || 0)
    }));

    const svgEl = e.target.closest('svg');
    const svgRect = svgEl.getBoundingClientRect();
    const svgViewBox = svgEl.viewBox.baseVal;
    window._svgScaleX = svgViewBox.width / svgRect.width;
    window._svgScaleY = svgViewBox.height / svgRect.height;

    document.addEventListener('mousemove', onImageMouseMove);
    document.addEventListener('mouseup', onImageMouseUp);
}

function onSlideWrapperMouseDown(e) {
    if (!isEditMode) return;
    
    let isImageOrPlaceholder = false;
    let el = e.target;
    while (el) {
        if (el.tagName && (el.tagName.toLowerCase() === 'image' || el.tagName === 'image')) {
            isImageOrPlaceholder = true;
            break;
        }
        if (el.classList && el.classList.contains('image-placeholder-group')) {
            isImageOrPlaceholder = true;
            break;
        }
        if (el.dataset && el.dataset.imgPlaceholder === 'true') {
            isImageOrPlaceholder = true;
            break;
        }
        if (el.tagName && el.tagName.toLowerCase() === 'svg') break;
        el = el.parentElement;
    }
    
    if (e.target.closest('svg') && !isImageOrPlaceholder) {
        clearImageSelection();
    }
}

function toggleImageSelection(img) {
    const idx = selectedImages.indexOf(img);
    if (idx >= 0) {
        selectedImages.splice(idx, 1);
    } else {
        selectedImages.push(img);
    }
    if (selectedImages.length > 0) {
        selectedImage = selectedImages[selectedImages.length - 1];
    } else {
        selectedImage = null;
    }
    updateSelectionUI();
}

function selectImages(images) {
    selectedImages = images.filter(el => el && el.parentNode);
    selectedImage = selectedImages.length > 0 ? selectedImages[selectedImages.length - 1] : null;
    updateSelectionUI();
}

function updateSelectionUI() {
    clearImageSelection();
    if (selectedImages.length === 0) {
        if (propertiesPanel) propertiesPanel.style.display = 'none';
        return;
    }

    const slideWrapper = document.getElementById('slideWrapper');
    const wrapperRect = slideWrapper.getBoundingClientRect();

    selectedImages.forEach(img => {
        const rect = img.getBoundingClientRect();

        const box = document.createElement('div');
        box.className = 'absolute border-2 border-green-500 z-40 paste-ready';
    box.style.cssText = `
        left: ${rect.left - wrapperRect.left}px;
        top: ${rect.top - wrapperRect.top}px;
        width: ${rect.width}px;
        height: ${rect.height}px;
        pointer-events: none;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.5);
    `;
        slideWrapper.appendChild(box);
        selectionBoxes.push(box);
    });

    if (selectedImages.length === 1) {
        const img = selectedImages[0];
        const rect = img.getBoundingClientRect();

        const handles = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];
        const handleSize = 10;
        const positions = {
            nw: { left: -handleSize/2, top: -handleSize/2, cursor: 'nw-resize' },
            n: { left: rect.width/2 - handleSize/2, top: -handleSize/2, cursor: 'n-resize' },
            ne: { left: rect.width - handleSize/2, top: -handleSize/2, cursor: 'ne-resize' },
            e: { left: rect.width - handleSize/2, top: rect.height/2 - handleSize/2, cursor: 'e-resize' },
            se: { left: rect.width - handleSize/2, top: rect.height - handleSize/2, cursor: 'se-resize' },
            s: { left: rect.width/2 - handleSize/2, top: rect.height - handleSize/2, cursor: 's-resize' },
            sw: { left: -handleSize/2, top: rect.height - handleSize/2, cursor: 'sw-resize' },
            w: { left: -handleSize/2, top: rect.height/2 - handleSize/2, cursor: 'w-resize' },
        };

        handles.forEach(h => {
            const handle = document.createElement('div');
            handle.className = 'absolute bg-white border-2 border-green-500 rounded-full';
            handle.style.cssText = `
                width: ${handleSize}px;
                height: ${handleSize}px;
                left: ${rect.left - wrapperRect.left + positions[h].left}px;
                top: ${rect.top - wrapperRect.top + positions[h].top}px;
                cursor: ${positions[h].cursor};
                z-index: 1000;
            `;
            handle.dataset.handle = h;
            handle.dataset.resizeHandle = 'true';
            handle.addEventListener('mousedown', onResizeHandleMouseDown);
            slideWrapper.appendChild(handle);
            resizeHandles.push(handle);
        });
    }

    updatePropertiesPanel();
}

function selectImage(img) {
    clearImageSelection();
    removeOutOfBoundsIndicator();
    selectedImage = img;
    selectedImages = [img];
    pasteImageMode = true;

    if (img.dataset.outOfBounds === 'complete') {
        img.removeAttribute('clip-path');
        img.style.opacity = '0.5';
    } else {
        const clipId = img.dataset.containerClipId;
        if (clipId) {
            img.setAttribute('clip-path', `url(#${clipId})`);
        }
        img.style.opacity = '1';
    }

    const rect = img.getBoundingClientRect();
    const slideWrapper = document.getElementById('slideWrapper');
    const wrapperRect = slideWrapper.getBoundingClientRect();
    slideWrapper.style.position = 'relative';

    selectionBoxes = [];
    const box = document.createElement('div');
    box.id = 'imageSelectionBox';
    box.className = 'absolute border-2 border-green-500 z-40 paste-ready';
    box.style.cssText = `
        left: ${rect.left - wrapperRect.left}px;
        top: ${rect.top - wrapperRect.top}px;
        width: ${rect.width}px;
        height: ${rect.height}px;
        pointer-events: none;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.5);
    `;
    slideWrapper.appendChild(box);
    selectionBoxes.push(box);

    const handles = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];
    const handleSize = 10;
    const positions = {
        nw: { left: -handleSize/2, top: -handleSize/2, cursor: 'nw-resize' },
        n: { left: rect.width/2 - handleSize/2, top: -handleSize/2, cursor: 'n-resize' },
        ne: { left: rect.width - handleSize/2, top: -handleSize/2, cursor: 'ne-resize' },
        e: { left: rect.width - handleSize/2, top: rect.height/2 - handleSize/2, cursor: 'e-resize' },
        se: { left: rect.width - handleSize/2, top: rect.height - handleSize/2, cursor: 'se-resize' },
        s: { left: rect.width/2 - handleSize/2, top: rect.height - handleSize/2, cursor: 's-resize' },
        sw: { left: -handleSize/2, top: rect.height - handleSize/2, cursor: 'sw-resize' },
        w: { left: -handleSize/2, top: rect.height/2 - handleSize/2, cursor: 'w-resize' },
    };

    handles.forEach(h => {
        const handle = document.createElement('div');
        handle.className = 'absolute bg-white border-2 border-green-500 rounded-full';
        handle.style.cssText = `
            width: ${handleSize}px;
            height: ${handleSize}px;
            left: ${rect.left - wrapperRect.left + positions[h].left}px;
            top: ${rect.top - wrapperRect.top + positions[h].top}px;
            cursor: ${positions[h].cursor};
            z-index: 1000;
        `;
        handle.dataset.handle = h;
        handle.dataset.resizeHandle = 'true';
        handle.addEventListener('mousedown', onResizeHandleMouseDown);
        slideWrapper.appendChild(handle);
        resizeHandles.push(handle);
    });

    updatePropertiesPanel();
    showPasteHint();
}

function clearImageSelection() {
    selectionBoxes.forEach(box => box.remove());
    selectionBoxes = [];
    resizeHandles.forEach(h => h.remove());
    resizeHandles = [];

    if (selectedPlaceholderRect) {
        selectedPlaceholderRect.style.fill = '';
        selectedPlaceholderRect.style.stroke = '';
        selectedPlaceholderRect.style.strokeWidth = '';
        selectedPlaceholderRect = null;
    }

    if (selectedImage) {
        if (selectedImage.dataset.outOfBounds === 'complete') {
            selectedImage.style.opacity = '0';
            selectedImage.removeAttribute('clip-path');
            showOutOfBoundsIndicator(selectedImage);
        } else {
            checkImageOutOfBounds(selectedImage);
        }
    }

    selectedImage = null;
    selectedImages = [];
    pasteImageMode = false;
    isDragging = false;
    isResizing = false;
    resizeHandle = null;
    clearAlignmentGuides();
    document.removeEventListener('mousemove', onImageMouseMove);
    document.removeEventListener('mouseup', onImageMouseUp);
    const pasteHint = document.getElementById('pasteHint');
    if (pasteHint) pasteHint.remove();
    if (propertiesPanel) propertiesPanel.style.display = 'none';
}

function showPasteHint() {
    const existing = document.getElementById('pasteHint');
    if (existing) existing.remove();
    
    const slideWrapper = document.getElementById('slideWrapper');
    if (!slideWrapper || !pasteImageMode) return;
    
    const hint = document.createElement('div');
    hint.id = 'pasteHint';
    hint.className = 'absolute z-50 bg-green-600 text-white text-sm px-4 py-2 rounded-lg shadow-lg';
    hint.style.cssText = 'bottom: 20px; left: 50%; transform: translateX(-50%); font-weight: 500; animation: fadeInUp 0.3s ease-out;';
    hint.innerHTML = '⌘ Ctrl+V 粘贴图片替换 · Delete 删除 · Esc 取消选择';
    slideWrapper.appendChild(hint);
}

function onImageMouseMove(e) {
    if (isDragging && selectedImages.length > 0) {
        const scaleX = window._svgScaleX || 1;
        const scaleY = window._svgScaleY || 1;
        const dx = (e.clientX - dragStartX) * scaleX;
        const dy = (e.clientY - dragStartY) * scaleY;

        imageStartPositions.forEach(pos => {
            let newX = pos.x + dx;
            let newY = pos.y + dy;

            const snap = calculateSnapPosition(newX, newY,
                parseFloat(pos.el.getAttribute('width') || 0),
                parseFloat(pos.el.getAttribute('height') || 0));
            if (snap.x !== null) newX = snap.x;
            if (snap.y !== null) newY = snap.y;

            pos.el.setAttribute('x', newX);
            pos.el.setAttribute('y', newY);

            // Update HTML overlay position
            updateOverlayPosition(pos.el);
        });

        updateSelectionBoxesPosition();
        showAlignmentGuides(calculateSnapPosition(
            parseFloat(selectedImage.getAttribute('x') || 0),
            parseFloat(selectedImage.getAttribute('y') || 0),
            parseFloat(selectedImage.getAttribute('width') || 0),
            parseFloat(selectedImage.getAttribute('height') || 0)
        ).guides);
        updatePropertiesPanel();
    } else if (isResizing && selectedImage && resizeHandle) {
        const scaleX = window._svgScaleX || 1;
        const scaleY = window._svgScaleY || 1;
        const dx = (e.clientX - resizeStartX) * scaleX;
        const dy = (e.clientY - resizeStartY) * scaleY;
        let newWidth = imageStartWidth;
        let newHeight = imageStartHeight;
        let newX = parseFloat(selectedImage.getAttribute('x') || 0);
        let newY = parseFloat(selectedImage.getAttribute('y') || 0);

        const h = resizeHandle;
        if (h.includes('e')) newWidth = Math.max(20, imageStartWidth + dx);
        if (h.includes('w')) { newWidth = Math.max(20, imageStartWidth - dx); newX = imageStartX + imageStartWidth - newWidth; }
        if (h.includes('s')) newHeight = Math.max(20, imageStartHeight + dy);
        if (h.includes('n')) { newHeight = Math.max(20, imageStartHeight - dy); newY = imageStartY + imageStartHeight - newHeight; }

        if (!e.shiftKey) {
            const aspect = imageStartWidth / imageStartHeight;
            if (h.includes('e') || h.includes('w')) {
                newHeight = newWidth / aspect;
                if (h.includes('n')) newY = imageStartY + imageStartHeight - newHeight;
            } else {
                newWidth = newHeight * aspect;
                if (h.includes('w')) newX = imageStartX + imageStartWidth - newWidth;
            }
        }

        selectedImage.setAttribute('x', newX);
        selectedImage.setAttribute('y', newY);
        selectedImage.setAttribute('width', newWidth);
        selectedImage.setAttribute('height', newHeight);

        // Update HTML overlay position
        updateOverlayPosition(selectedImage);

        updateSelectionBoxesPosition();
        updatePropertiesPanel();
    }
}

function onImageMouseUp(e) {
    if (isDragging && selectedImages.length > 0) {
        const hadMove = imageStartPositions.some(pos => {
            const newX = parseFloat(pos.el.getAttribute('x') || 0);
            const newY = parseFloat(pos.el.getAttribute('y') || 0);
            return Math.abs(newX - pos.x) > 0.5 || Math.abs(newY - pos.y) > 0.5;
        });

        if (hadMove) {
            imageStartPositions.forEach(pos => {
                const newX = parseFloat(pos.el.getAttribute('x') || 0);
                const newY = parseFloat(pos.el.getAttribute('y') || 0);
                pushUndoState('move', pos.el, {
                    oldX: pos.x, oldY: pos.y,
                    newX: newX, newY: newY
                });
                checkImageOutOfBounds(pos.el);
            });
        }
    } else if (isResizing && selectedImage) {
        const newWidth = parseFloat(selectedImage.getAttribute('width') || 0);
        const newHeight = parseFloat(selectedImage.getAttribute('height') || 0);
        const newX = parseFloat(selectedImage.getAttribute('x') || 0);
        const newY = parseFloat(selectedImage.getAttribute('y') || 0);
        if (Math.abs(newWidth - imageStartWidth) > 1 || Math.abs(newHeight - imageStartHeight) > 1) {
            pushUndoState('resize', selectedImage, {
                oldX: imageStartX, oldY: imageStartY,
                oldWidth: imageStartWidth, oldHeight: imageStartHeight,
                newX: newX, newY: newY,
                newWidth: newWidth, newHeight: newHeight
            });
        }
        checkImageOutOfBounds(selectedImage);
    }

    const hadChange = isDragging || isResizing;

    isDragging = false;
    isResizing = false;
    resizeHandle = null;
    clearAlignmentGuides();
    document.removeEventListener('mousemove', onImageMouseMove);
    document.removeEventListener('mouseup', onImageMouseUp);

    if (hadChange && selectedImages.length > 0) {
        saveCurrentSvg();
    }
}

function onResizeHandleMouseDown(e) {
    e.stopPropagation();
    e.preventDefault();

    isDragging = false;
    isResizing = true;
    resizeHandle = e.target.dataset.handle;
    resizeStartX = e.clientX;
    resizeStartY = e.clientY;
    imageStartWidth = parseFloat(selectedImage.getAttribute('width') || 0);
    imageStartHeight = parseFloat(selectedImage.getAttribute('height') || 0);
    imageStartX = parseFloat(selectedImage.getAttribute('x') || 0);
    imageStartY = parseFloat(selectedImage.getAttribute('y') || 0);

    const svgEl = selectedImage.closest('svg');
    const svgRect = svgEl.getBoundingClientRect();
    const svgViewBox = svgEl.viewBox.baseVal;
    window._svgScaleX = svgViewBox.width / svgRect.width;
    window._svgScaleY = svgViewBox.height / svgRect.height;

    document.addEventListener('mousemove', onImageMouseMove);
    document.addEventListener('mouseup', onImageMouseUp);
}

function updateSelectionBoxesPosition() {
    if (selectionBoxes.length === 0) return;

    selectionBoxes.forEach((box, idx) => {
        if (idx >= selectedImages.length) return;
        const img = selectedImages[idx];
        const rect = img.getBoundingClientRect();
        const svgEl = img.closest('svg');
        const svgRect = svgEl.getBoundingClientRect();

        box.style.left = `${rect.left - svgRect.left}px`;
        box.style.top = `${rect.top - svgRect.top}px`;
        box.style.width = `${rect.width}px`;
        box.style.height = `${rect.height}px`;
    });

    if (selectedImages.length === 1 && resizeHandles.length > 0) {
        const img = selectedImages[0];
        const rect = img.getBoundingClientRect();
        const svgEl = img.closest('svg');
        const svgRect = svgEl.getBoundingClientRect();

        const handleSize = 10;
        const positions = {
            nw: { left: -handleSize/2, top: -handleSize/2 },
            n: { left: rect.width/2 - handleSize/2, top: -handleSize/2 },
            ne: { left: rect.width - handleSize/2, top: -handleSize/2 },
            e: { left: rect.width - handleSize/2, top: rect.height/2 - handleSize/2 },
            se: { left: rect.width - handleSize/2, top: rect.height - handleSize/2 },
            s: { left: rect.width/2 - handleSize/2, top: rect.height - handleSize/2 },
            sw: { left: -handleSize/2, top: rect.height - handleSize/2 },
            w: { left: -handleSize/2, top: rect.height/2 - handleSize/2 },
        };

        resizeHandles.forEach(handle => {
            const h = handle.dataset.handle;
            if (positions[h]) {
                handle.style.left = `${rect.left - svgRect.left + positions[h].left}px`;
                handle.style.top = `${rect.top - svgRect.top + positions[h].top}px`;
            }
        });
    }
}

window.addEventListener('resize', () => {
    if (selectedImages.length > 0 && selectionBoxes.length > 0) {
        updateSelectionBoxesPosition();
    }
    removeOutOfBoundsIndicator();
});

function getImageIndex(img) {
    const svgEl = img.closest('svg');
    if (!svgEl) return -1;
    const images = svgEl.querySelectorAll('image');
    return Array.from(images).indexOf(img);
}

function findImageByIndex(index) {
    const slideWrapper = document.getElementById('slideWrapper');
    if (!slideWrapper) return null;
    const svgEl = slideWrapper.querySelector('svg');
    if (!svgEl) return null;
    const images = svgEl.querySelectorAll('image');
    return images[index] || null;
}

function pushUndoState(type, element, data) {
    undoStack.push({
        type: type,
        slidePath: currentEditingSlidePath,
        elementIndex: getImageIndex(element),
        data: data,
        timestamp: Date.now()
    });
    if (undoStack.length > MAX_UNDO) undoStack.shift();
    redoStack = [];
}

async function undoLastEdit() {
    if (!localStorage.getItem('authToken')) {
        showToast('请先登录', 'error');
        return;
    }
    if (undoStack.length === 0) {
        showToast('Nothing to undo', 'info');
        return;
    }
    const last = undoStack.pop();
    redoStack.push(last);

    if (last.type === 'move') {
        const img = findImageByIndex(last.elementIndex);
        if (img) {
            img.setAttribute('x', last.data.oldX);
            img.setAttribute('y', last.data.oldY);
            checkImageOutOfBounds(img);
            selectImage(img);
        }
    } else if (last.type === 'resize') {
        const img = findImageByIndex(last.elementIndex);
        if (img) {
            img.setAttribute('x', last.data.oldX);
            img.setAttribute('y', last.data.oldY);
            img.setAttribute('width', last.data.oldWidth);
            img.setAttribute('height', last.data.oldHeight);
            checkImageOutOfBounds(img);
            selectImage(img);
        }
    } else if (last.type === 'delete') {
        const svgEl = document.getElementById('slideWrapper')?.querySelector('svg');
        if (svgEl && last.data.element) {
            const restored = last.data.element.cloneNode(true);
            restored.removeAttribute('data-image-edit-listener');
            restored.removeAttribute('pointer-events');
            restored.removeAttribute('data-container-x');
            restored.removeAttribute('data-container-y');
            restored.removeAttribute('data-container-width');
            restored.removeAttribute('data-container-height');
            restored.removeAttribute('data-container-clip-id');
            restored.removeAttribute('data-out-of-bounds');
            restored.style.cursor = 'move';
            restored.style.opacity = '';
            restored.addEventListener('mousedown', onImageMouseDown);
            svgEl.appendChild(restored);
            if (!restored.dataset.containerX) {
                detectImageContainerBounds(restored);
            }
            checkImageOutOfBounds(restored);
            selectImage(restored);
        }
    } else if (last.type === 'text') {
        try {
            const response = await fetch('/api/edit-svg', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    file: decodeURIComponent(last.slidePath.replace(/.*\//, '')),
                    folder: decodeURIComponent(last.slidePath.replace(/\/[^/]+$/, '')).replace(/.*examples/, 'examples'),
                    oldText: last.data.newText,
                    newText: last.data.oldText,
                    elementIndex: last.data.elementIndex
                })
            });
            const data = await response.json();
            if (response.ok && data.success) {
                refreshCurrentSlide();
            }
        } catch (err) {
            showToast('Undo error: ' + err.message, 'error');
        }
        return;
    }

    showToast('Undo successful', 'success');
    if (currentEditingSlidePath) svgCache.delete(currentEditingSlidePath);
}

async function redoLastEdit() {
    if (redoStack.length === 0) {
        showToast('Nothing to redo', 'info');
        return;
    }
    const last = redoStack.pop();
    undoStack.push(last);

    if (last.type === 'move') {
        const img = findImageByIndex(last.elementIndex);
        if (img) {
            img.setAttribute('x', last.data.newX);
            img.setAttribute('y', last.data.newY);
            checkImageOutOfBounds(img);
            selectImage(img);
        }
    } else if (last.type === 'resize') {
        const img = findImageByIndex(last.elementIndex);
        if (img) {
            img.setAttribute('x', last.data.newX);
            img.setAttribute('y', last.data.newY);
            img.setAttribute('width', last.data.newWidth);
            img.setAttribute('height', last.data.newHeight);
            checkImageOutOfBounds(img);
            selectImage(img);
        }
    }

    showToast('Redo successful', 'success');
}

function deleteSelectedImage() {
    if (!selectedImage) {
        showToast('No image selected', 'info');
        return;
    }

    const oldX = parseFloat(selectedImage.getAttribute('x') || 0);
    const oldY = parseFloat(selectedImage.getAttribute('y') || 0);
    const oldWidth = parseFloat(selectedImage.getAttribute('width') || 0);
    const oldHeight = parseFloat(selectedImage.getAttribute('height') || 0);
    const href = selectedImage.getAttribute('href') || selectedImage.getAttribute('xlink:href');

    pushUndoState('delete', selectedImage, {
        oldX, oldY, oldWidth, oldHeight,
        element: selectedImage.cloneNode(true)
    });

    selectedImage.remove();
    clearImageSelection();
    showToast('Image deleted (Ctrl+Z to undo)', 'success');
}

function refreshCurrentSlide() {
    if (currentCollection) {
        svgCache.delete(currentEditingSlidePath);
        updateSlide();
    }
}

document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'z' && (e.ctrlKey || e.metaKey) && isEditMode) {
        e.preventDefault();
        undoLastEdit();
    }
    if ((e.key === 'y' && (e.ctrlKey || e.metaKey) && isEditMode) ||
        (e.key === 'z' && (e.ctrlKey || e.metaKey) && e.shiftKey && isEditMode)) {
        e.preventDefault();
        redoLastEdit();
    }
    if (e.key === 'Delete' && isEditMode && selectedImage) {
        e.preventDefault();
        deleteSelectedImage();
    }
    if (e.key === 'Escape' && isEditMode && selectedImage) {
        e.preventDefault();
        clearImageSelection();
    }
    if ((e.key === 'v' || e.key === 'V') && (e.ctrlKey || e.metaKey) && isEditMode && pasteImageMode && (selectedImage || selectedPlaceholderRect)) {
    }
});

async function handleClipboardPaste(e) {
    if (!isEditMode) return;
    if (!pasteImageMode) return;
    if (!selectedImage && !selectedPlaceholderRect) return;
    
    const items = e.clipboardData?.items;
    if (!items) return;
    
    let imageFile = null;
    for (const item of items) {
        if (item.type.startsWith('image/')) {
            imageFile = item.getAsFile();
            break;
        }
    }
    
    if (!imageFile) return;
    
    e.preventDefault();
    
    try {
        const base64Data = await readFileAsBase64(imageFile);
        
        if (selectedPlaceholderRect) {
            await insertImageToPlaceholder(selectedPlaceholderRect, base64Data);
        } else if (selectedImage) {
            await replaceSelectedImage(base64Data);
        }
    } catch (error) {
        console.error('Paste image error:', error);
        showToast('粘贴图片失败: ' + error.message, 'error');
    }
}

async function insertImageToPlaceholder(rect, base64Data) {
    const svgEl = rect.closest('svg');
    if (!svgEl) return;

    let x = parseFloat(rect.getAttribute('x') || 0);
    let y = parseFloat(rect.getAttribute('y') || 0);
    let w = parseFloat(rect.getAttribute('width') || 400);
    let h = parseFloat(rect.getAttribute('height') || 300);

    let el = rect.parentElement;
    while (el && el !== svgEl) {
        if (el.tagName && el.tagName.toLowerCase() === 'g' && el.getAttribute('transform')) {
            const transform = el.getAttribute('transform');
            const match = transform.match(/translate\(\s*([\d.-]+)\s*,\s*([\d.-]+)\s*\)/);
            if (match) {
                x += parseFloat(match[1]);
                y += parseFloat(match[2]);
            }
        }
        el = el.parentElement;
    }

    const ns = 'http://www.w3.org/2000/svg';
    const clipId = `clip_paste_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    let defs = svgEl.querySelector('defs');
    if (!defs) {
        defs = document.createElementNS(ns, 'defs');
        svgEl.insertBefore(defs, svgEl.firstChild);
    }

    const clipPath = document.createElementNS(ns, 'clipPath');
    clipPath.setAttribute('id', clipId);
    const clipRect = document.createElementNS(ns, 'rect');
    clipRect.setAttribute('x', x);
    clipRect.setAttribute('y', y);
    clipRect.setAttribute('width', w);
    clipRect.setAttribute('height', h);
    clipRect.setAttribute('rx', rect.getAttribute('rx') || '0');
    clipPath.appendChild(clipRect);
    defs.appendChild(clipPath);

    const img = document.createElementNS(ns, 'image');
    img.setAttribute('x', x);
    img.setAttribute('y', y);
    img.setAttribute('width', w);
    img.setAttribute('height', h);
    img.setAttribute('href', base64Data);
    img.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    img.setAttribute('clip-path', `url(#${clipId})`);
    img.setAttribute('pointer-events', 'all');
    img.style.cursor = 'move';

    img.dataset.containerX = x;
    img.dataset.containerY = y;
    img.dataset.containerWidth = w;
    img.dataset.containerHeight = h;
    img.dataset.containerClipId = clipId;

    svgEl.appendChild(img);

    rect.style.display = 'none';

    const nextText = rect.nextElementSibling;
    if (nextText && nextText.tagName && nextText.tagName.toLowerCase() === 'text') {
        nextText.style.display = 'none';
    }

    if (isEditMode) {
        img.dataset.imageEditListener = 'true';
        img.addEventListener('mousedown', onImageMouseDown);
    }

    if (rect._overlayEl) {
        rect._overlayEl.remove();
        rect._overlayEl = null;
    }

    clearImageSelection();
    saveCurrentSvg(true);
    showToast('图片已粘贴！', 'success');
}

function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(new Error('Failed to read file'));
        reader.readAsDataURL(file);
    });
}

async function replaceSelectedImage(base64Data) {
    if (!selectedImage) {
        showToast('请先选中一个图片', 'info');
        return;
    }
    
    const svgEl = selectedImage.closest('svg');
    const x = parseFloat(selectedImage.getAttribute('x') || 0);
    const y = parseFloat(selectedImage.getAttribute('y') || 0);
    const width = parseFloat(selectedImage.getAttribute('width') || 400);
    const height = parseFloat(selectedImage.getAttribute('height') || 300);
    const containerX = selectedImage.dataset.containerX ? parseFloat(selectedImage.dataset.containerX) : x;
    const containerY = selectedImage.dataset.containerY ? parseFloat(selectedImage.dataset.containerY) : y;
    const containerWidth = selectedImage.dataset.containerWidth ? parseFloat(selectedImage.dataset.containerWidth) : width;
    const containerHeight = selectedImage.dataset.containerHeight ? parseFloat(selectedImage.dataset.containerHeight) : height;
    
    const oldX = parseFloat(selectedImage.getAttribute('x') || 0);
    const oldY = parseFloat(selectedImage.getAttribute('y') || 0);
    const oldWidth = parseFloat(selectedImage.getAttribute('width') || 0);
    const oldHeight = parseFloat(selectedImage.getAttribute('height') || 0);
    pushUndoState('replace', selectedImage, {
        oldX, oldY, oldWidth, oldHeight,
        oldHref: selectedImage.getAttribute('href') || selectedImage.getAttribute('xlink:href')
    });
    
    selectedImage.setAttribute('href', base64Data);
    
    showToast('图片已替换！', 'success');
    saveCurrentSvg(true);
}

function calculateSnapPosition(x, y, w, h) {
    const guides = [];
    let snapX = null;
    let snapY = null;

    const svgEl = document.getElementById('slideWrapper')?.querySelector('svg');
    if (!svgEl) return { x: null, y: null, guides: [] };

    const viewBox = svgEl.viewBox.baseVal;
    const svgW = viewBox.width || 1920;
    const svgH = viewBox.height || 1080;

    const canvasCenterX = svgW / 2;
    const canvasCenterY = svgH / 2;
    const imgCenterX = x + w / 2;
    const imgCenterY = y + h / 2;

    if (Math.abs(imgCenterX - canvasCenterX) < snapThreshold) {
        snapX = canvasCenterX - w / 2;
        guides.push({ type: 'v', pos: canvasCenterX });
    }
    if (Math.abs(imgCenterY - canvasCenterY) < snapThreshold) {
        snapY = canvasCenterY - h / 2;
        guides.push({ type: 'h', pos: canvasCenterY });
    }

    if (Math.abs(x) < snapThreshold) {
        snapX = 0;
        guides.push({ type: 'v', pos: 0 });
    }
    if (Math.abs(y) < snapThreshold) {
        snapY = 0;
        guides.push({ type: 'h', pos: 0 });
    }
    if (Math.abs(x + w - svgW) < snapThreshold) {
        snapX = svgW - w;
        guides.push({ type: 'v', pos: svgW });
    }
    if (Math.abs(y + h - svgH) < snapThreshold) {
        snapY = svgH - h;
        guides.push({ type: 'h', pos: svgH });
    }

    const images = svgEl.querySelectorAll('image');
    for (const other of images) {
        if (other === selectedImage) continue;
        const ox = parseFloat(other.getAttribute('x') || 0);
        const oy = parseFloat(other.getAttribute('y') || 0);
        const ow = parseFloat(other.getAttribute('width') || 0);
        const oh = parseFloat(other.getAttribute('height') || 0);
        const oCenterX = ox + ow / 2;
        const oCenterY = oy + oh / 2;

        if (Math.abs(imgCenterX - oCenterX) < snapThreshold) {
            snapX = oCenterX - w / 2;
            guides.push({ type: 'v', pos: oCenterX });
        }
        if (Math.abs(imgCenterY - oCenterY) < snapThreshold) {
            snapY = oCenterY - h / 2;
            guides.push({ type: 'h', pos: oCenterY });
        }
        if (Math.abs(x - ox) < snapThreshold) {
            snapX = ox;
            guides.push({ type: 'v', pos: ox });
        }
        if (Math.abs(y - oy) < snapThreshold) {
            snapY = oy;
            guides.push({ type: 'h', pos: oy });
        }
        if (Math.abs(x + w - (ox + ow)) < snapThreshold) {
            snapX = ox + ow - w;
            guides.push({ type: 'v', pos: ox + ow });
        }
        if (Math.abs(y + h - (oy + oh)) < snapThreshold) {
            snapY = oy + oh - h;
            guides.push({ type: 'h', pos: oy + oh });
        }
    }

    return { x: snapX, y: snapY, guides };
}

function showAlignmentGuides(guides) {
    clearAlignmentGuides();
    const slideWrapper = document.getElementById('slideWrapper');
    if (!slideWrapper) return;

    const svgEl = slideWrapper.querySelector('svg');
    if (!svgEl) return;

    const svgRect = svgEl.getBoundingClientRect();
    const viewBox = svgEl.viewBox.baseVal;
    const scaleX = svgRect.width / (viewBox.width || 1920);
    const scaleY = svgRect.height / (viewBox.height || 1080);

    const uniqueGuides = [];
    const seen = new Set();
    for (const g of guides) {
        const key = `${g.type}-${Math.round(g.pos)}`;
        if (!seen.has(key)) {
            seen.add(key);
            uniqueGuides.push(g);
        }
    }

    for (const g of uniqueGuides) {
        const line = document.createElement('div');
        line.className = 'alignment-guide';
        line.style.position = 'absolute';
        line.style.pointerEvents = 'none';
        line.style.zIndex = '30';
        line.style.backgroundColor = '#3b82f6';

        if (g.type === 'v') {
            line.style.width = '1px';
            line.style.height = '100%';
            line.style.left = `${g.pos * scaleX}px`;
            line.style.top = '0';
        } else {
            line.style.height = '1px';
            line.style.width = '100%';
            line.style.top = `${g.pos * scaleY}px`;
            line.style.left = '0';
        }

        slideWrapper.appendChild(line);
        alignmentGuides.push(line);
    }
}

function clearAlignmentGuides() {
    for (const g of alignmentGuides) {
        g.remove();
    }
    alignmentGuides = [];
}

function createPropertiesPanel() {
    if (propertiesPanel) return propertiesPanel;

    const slideWrapper = document.getElementById('slideWrapper');
    if (!slideWrapper) return null;

    propertiesPanel = document.createElement('div');
    propertiesPanel.id = 'propertiesPanel';
    propertiesPanel.style.cssText = `
        position: absolute; top: 8px; right: 8px; z-index: 50;
        background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 8px; padding: 12px; min-width: 180px; font-size: 12px;
        color: #e2e8f0; display: none; backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;

    propertiesPanel.innerHTML = `
        <div style="font-weight:600; margin-bottom:8px; color:#93c5fd; font-size:13px;">Image Properties</div>
        <div style="display:grid; grid-template-columns:auto 1fr; gap:4px 8px; align-items:center;">
            <span style="color:#94a3b8;">X:</span><input id="propX" type="number" style="background:#1e293b; border:1px solid #334155; color:#e2e8f0; border-radius:4px; padding:2px 6px; width:100%; font-size:12px;" />
            <span style="color:#94a3b8;">Y:</span><input id="propY" type="number" style="background:#1e293b; border:1px solid #334155; color:#e2e8f0; border-radius:4px; padding:2px 6px; width:100%; font-size:12px;" />
            <span style="color:#94a3b8;">W:</span><input id="propW" type="number" style="background:#1e293b; border:1px solid #334155; color:#e2e8f0; border-radius:4px; padding:2px 6px; width:100%; font-size:12px;" />
            <span style="color:#94a3b8;">H:</span><input id="propH" type="number" style="background:#1e293b; border:1px solid #334155; color:#e2e8f0; border-radius:4px; padding:2px 6px; width:100%; font-size:12px;" />
        </div>
        <div style="margin-top:8px; display:flex; gap:4px;">
            <button id="propCenterH" style="flex:1; background:#1e40af; color:#fff; border:none; border-radius:4px; padding:4px; cursor:pointer; font-size:11px;" title="Center horizontally">H-Center</button>
            <button id="propCenterV" style="flex:1; background:#1e40af; color:#fff; border:none; border-radius:4px; padding:4px; cursor:pointer; font-size:11px;" title="Center vertically">V-Center</button>
        </div>
    `;

    slideWrapper.style.position = 'relative';
    slideWrapper.appendChild(propertiesPanel);

    const propX = propertiesPanel.querySelector('#propX');
    const propY = propertiesPanel.querySelector('#propY');
    const propW = propertiesPanel.querySelector('#propW');
    const propH = propertiesPanel.querySelector('#propH');

    const applyPropChange = (attr, input) => {
        const val = parseFloat(input.value);
        if (isNaN(val) || !selectedImage) return;
        const oldVal = parseFloat(selectedImage.getAttribute(attr) || 0);
        if (Math.abs(val - oldVal) < 0.5) return;
        const oldX = parseFloat(selectedImage.getAttribute('x') || 0);
        const oldY = parseFloat(selectedImage.getAttribute('y') || 0);
        const oldWidth = parseFloat(selectedImage.getAttribute('width') || 0);
        const oldHeight = parseFloat(selectedImage.getAttribute('height') || 0);
        selectedImage.setAttribute(attr, val);
        pushUndoState('resize', selectedImage, {
            oldX, oldY, oldWidth, oldHeight,
            newX: parseFloat(selectedImage.getAttribute('x') || 0),
            newY: parseFloat(selectedImage.getAttribute('y') || 0),
            newWidth: parseFloat(selectedImage.getAttribute('width') || 0),
            newHeight: parseFloat(selectedImage.getAttribute('height') || 0)
        });
        checkImageOutOfBounds(selectedImage);
        updateSelectionBoxPosition();
        saveCurrentSvg();
    };

    propX.addEventListener('change', () => applyPropChange('x', propX));
    propY.addEventListener('change', () => applyPropChange('y', propY));
    propW.addEventListener('change', () => applyPropChange('width', propW));
    propH.addEventListener('change', () => applyPropChange('height', propH));

    propertiesPanel.querySelector('#propCenterH').addEventListener('click', () => {
        if (!selectedImage) return;
        const svgEl = document.getElementById('slideWrapper')?.querySelector('svg');
        if (!svgEl) return;
        const viewBox = svgEl.viewBox.baseVal;
        const svgW = viewBox.width || 1920;
        const w = parseFloat(selectedImage.getAttribute('width') || 0);
        const oldX = parseFloat(selectedImage.getAttribute('x') || 0);
        const oldY = parseFloat(selectedImage.getAttribute('y') || 0);
        const oldWidth = parseFloat(selectedImage.getAttribute('width') || 0);
        const oldHeight = parseFloat(selectedImage.getAttribute('height') || 0);
        const newX = (svgW - w) / 2;
        selectedImage.setAttribute('x', newX);
        pushUndoState('move', selectedImage, { oldX, oldY, newX, newY: oldY });
        checkImageOutOfBounds(selectedImage);
        updateSelectionBoxPosition();
        updatePropertiesPanel();
        saveCurrentSvg();
    });

    propertiesPanel.querySelector('#propCenterV').addEventListener('click', () => {
        if (!selectedImage) return;
        const svgEl = document.getElementById('slideWrapper')?.querySelector('svg');
        if (!svgEl) return;
        const viewBox = svgEl.viewBox.baseVal;
        const svgH = viewBox.height || 1080;
        const h = parseFloat(selectedImage.getAttribute('height') || 0);
        const oldX = parseFloat(selectedImage.getAttribute('x') || 0);
        const oldY = parseFloat(selectedImage.getAttribute('y') || 0);
        const oldWidth = parseFloat(selectedImage.getAttribute('width') || 0);
        const oldHeight = parseFloat(selectedImage.getAttribute('height') || 0);
        const newY = (svgH - h) / 2;
        selectedImage.setAttribute('y', newY);
        pushUndoState('move', selectedImage, { oldX, oldY, newX: oldX, newY });
        checkImageOutOfBounds(selectedImage);
        updateSelectionBoxPosition();
        updatePropertiesPanel();
        saveCurrentSvg();
    });

    return propertiesPanel;
}

function updatePropertiesPanel() {
    if (!propertiesPanel) createPropertiesPanel();
    if (!propertiesPanel || !selectedImage) {
        if (propertiesPanel) propertiesPanel.style.display = 'none';
        return;
    }

    propertiesPanel.style.display = 'block';
    const x = parseFloat(selectedImage.getAttribute('x') || 0);
    const y = parseFloat(selectedImage.getAttribute('y') || 0);
    const w = parseFloat(selectedImage.getAttribute('width') || 0);
    const h = parseFloat(selectedImage.getAttribute('height') || 0);

    propertiesPanel.querySelector('#propX').value = Math.round(x);
    propertiesPanel.querySelector('#propY').value = Math.round(y);
    propertiesPanel.querySelector('#propW').value = Math.round(w);
    propertiesPanel.querySelector('#propH').value = Math.round(h);
}

function generateThumbnails() {
    if (!currentCollection) return;

    const container = document.getElementById('thumbnailContainer');
    const basePath = '/' + encodePath(currentCollection.folder) + '/';

    container.innerHTML = currentCollection.slides.map((slide, index) => {
        const slidePath = basePath + encodeURIComponent(slide.file);
        return `
        <div class="thumbnail rounded-lg overflow-hidden border-2 ${index === 0 ? 'border-brand-500' : 'border-transparent'}"
             onclick="goToSlide(${index})"
             id="thumb-${index}">
            <div class="relative bg-dark-800 animate-pulse">
                <img src="${slidePath}" class="w-full" loading="lazy" alt="${slide.title}"
                     onload="this.parentElement.classList.remove('animate-pulse', 'bg-dark-800')"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                <div class="hidden w-full h-16 flex items-center justify-center bg-dark-900 text-gray-600">
                    <i class="fas fa-image"></i>
                </div>
            </div>
            <div class="px-2 py-1 bg-transparent text-xs text-gray-400 truncate">
                ${index + 1}. ${slide.title}
            </div>
        </div>
    `}).join('');
}

function generateOverview() {
    if (!currentCollection) return;

    const container = document.getElementById('overviewGrid');
    const basePath = '/' + encodePath(currentCollection.folder) + '/';

    container.innerHTML = currentCollection.slides.map((slide, index) => {
        const slidePath = basePath + encodeURIComponent(slide.file);
        return `
        <div class="rounded-xl p-2 shadow-md hover:shadow-lg transition-shadow cursor-pointer"
             onclick="goToSlide(${index}); window.scrollTo({top: 0, behavior: 'smooth'})">
            <div class="relative bg-dark-800 rounded-lg animate-pulse">
                <img src="${slidePath}" class="w-full rounded-lg" loading="lazy" alt="${slide.title}"
                     onload="this.parentElement.classList.remove('animate-pulse', 'bg-dark-800')"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                <div class="hidden w-full h-24 flex items-center justify-center bg-dark-900 rounded-lg text-gray-600">
                    <i class="fas fa-image"></i>
                </div>
            </div>
            <div class="mt-2 px-1">
                <p class="text-sm font-medium text-gray-100 truncate">${index + 1}. ${slide.title}</p>
                <p class="text-xs text-gray-500 truncate">${slide.desc}</p>
            </div>
        </div>
    `}).join('');
}

function updateSlide() {
    if (!currentCollection) return;

    if (slideUpdateTimeout) {
        clearTimeout(slideUpdateTimeout);
    }

    slideUpdateTimeout = setTimeout(() => {
        performSlideUpdate();
    }, 50);
}

function encodePath(path) {
    return path.split('/').map(p => encodeURIComponent(p)).join('/');
}

function performSlideUpdate() {
    if (!currentCollection) return;

    clearImageSelection();
    removeEditOverlay();
    removeOutOfBoundsIndicator();

    const slide = currentCollection.slides[currentSlide];
    const basePath = '/' + encodePath(currentCollection.folder) + '/';
    const slidePath = basePath + encodeURIComponent(slide.file);

    const slideWrapper = document.getElementById('slideWrapper');
    const fullscreenImage = document.getElementById('fullscreenImage');

    const targetSlide = currentSlide;
    isSlideUpdating = true;

    const loadingSpinner = document.createElement('div');
    loadingSpinner.id = 'slideLoadingSpinner';
    loadingSpinner.className = 'absolute inset-0 flex items-center justify-center bg-gray-100/50 rounded-lg';
    loadingSpinner.innerHTML = '<div class="animate-spin rounded-full h-12 w-12 border-4 border-brand-200 border-t-brand-500"></div>';
    slideWrapper.appendChild(loadingSpinner);

    const oldSvg = slideWrapper.querySelector('svg');
    if (oldSvg) oldSvg.remove();

    const loadSVG = (path) => {
        if (svgCache.has(path)) {
            return Promise.resolve(svgCache.get(path));
        }
        return fetch(path)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.text();
            })
            .then(content => {
                svgCache.set(path, content);
                return content;
            });
    };

    loadSVG(slidePath)
        .then(svgContent => {
            if (targetSlide !== currentSlide) return;

            const parser = new DOMParser();
            const doc = parser.parseFromString(svgContent, 'image/svg+xml');
            
            // Check for parser errors
            const parserError = doc.querySelector('parsererror');
            if (parserError) {
                console.error('SVG Parse Error:', parserError.textContent.substring(0, 500));
                throw new Error('Invalid SVG content: ' + parserError.textContent.substring(0, 200));
            }
            
            const svgEl = doc.documentElement;
            
            if (!svgEl || svgEl.tagName !== 'svg') {
                console.error('Unexpected documentElement:', svgEl?.tagName, svgEl);
                throw new Error('Invalid SVG content: expected svg element, got ' + (svgEl?.tagName || 'null'));
            }
            
            svgEl.classList.add('w-full', 'h-full', 'rounded-lg', 'fade-in', 'cursor-pointer');
            svgEl.style.aspectRatio = '16/9';
            svgEl.setAttribute('data-slide-path', slidePath);

            slideWrapper.insertBefore(svgEl, slideWrapper.firstChild);

            const spinner = document.getElementById('slideLoadingSpinner');
            if (spinner) spinner.remove();

            svgEl.addEventListener('load', () => {
                setupTextEditListeners(svgEl);
                if (isEditMode) {
                    setupImageEditListeners();
                } else {
                    setupImagePlaceholderOverlays();
                }
            });
            setTimeout(() => {
                setupTextEditListeners(svgEl);
                if (isEditMode) {
                    setupImageEditListeners();
                } else {
                    setupImagePlaceholderOverlays();
                }
            }, 50);

            currentEditingSlidePath = slidePath;
            isSlideUpdating = false;

            if (pendingSlideIndex !== null) {
                const nextIndex = pendingSlideIndex;
                pendingSlideIndex = null;
                goToSlide(nextIndex);
            }
        })
        .catch(err => {
            console.error('Error loading SVG:', slidePath, err);
            const spinner = document.getElementById('slideLoadingSpinner');
            if (spinner) spinner.remove();
            isSlideUpdating = false;
            if (pendingSlideIndex !== null) {
                const nextIndex = pendingSlideIndex;
                pendingSlideIndex = null;
                goToSlide(nextIndex);
            }
        });

    fullscreenImage.src = slidePath;

    document.getElementById('currentPage').textContent = currentSlide + 1;
    document.getElementById('fullscreenPage').textContent = currentSlide + 1;

    const progress = ((currentSlide + 1) / currentCollection.slides.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';

    document.getElementById('prevBtn').disabled = currentSlide === 0;
    document.getElementById('nextBtn').disabled = currentSlide === currentCollection.slides.length - 1;

    currentCollection.slides.forEach((_, i) => {
        const thumb = document.getElementById(`thumb-${i}`);
        if (thumb) {
            if (i === currentSlide) {
                thumb.classList.add('border-brand-500');
                thumb.classList.remove('border-transparent');
                thumb.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                thumb.classList.remove('border-brand-500');
                thumb.classList.add('border-transparent');
            }
        }
    });
}

function nextSlide() {
    if (currentCollection && currentSlide < currentCollection.slides.length - 1) {
        const newIndex = currentSlide + 1;
        if (isSlideUpdating) {
            pendingSlideIndex = newIndex;
            return;
        }
        currentSlide = newIndex;
        updateSlide();
    }
}

async function deleteCurrentPage() {
    if (!currentCollection) {
        showToast('No project loaded', 'info');
        return;
    }
    
    const slideIndex = currentSlide;
    const slide = currentCollection.slides[slideIndex];
    
    if (!slide) {
        showToast('Slide not found', 'error');
        return;
    }
    
    const slideName = slide.title || slide.file;
    const confirmed = await showToastConfirmDelete(slideName);
    if (!confirmed) return;
    
    try {
        const deleteBtn = document.getElementById('deletePageBtn');
        deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 删 除 中...';
        deleteBtn.disabled = true;
        
        const basePath = '/' + encodePath(currentCollection.folder) + '/';
        const svgPath = basePath + encodeURIComponent(slide.file);
        
        let svgContent = null;
        const svgResponse = await fetch(svgPath);
        if (svgResponse.ok) {
            svgContent = await svgResponse.text();
        }
        
        if (svgResponse.ok) {
            const deleteRes = await fetch('/api/delete-svg', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path: svgPath})
            });
            const deleteData = await deleteRes.json();
            if (!deleteData.success) {
                console.error('Delete SVG failed:', deleteData.error);
                showToast('删除SVG文件失败: ' + deleteData.error, 'error');
                return;
            }
        }
        
        const thumbnailPath = svgPath.replace('/svg_final/', '/svg_thumbnail/');
        try {
            const thumbResponse = await fetch(thumbnailPath);
            if (thumbResponse.ok) {
                await fetch('/api/delete-svg', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({path: thumbnailPath})
                });
            }
        } catch (thumbErr) {
            console.warn('Thumbnail delete skipped:', thumbErr);
        }
        
        const projectPath = '/' + encodePath(currentCollection.folder) + '/project.json';
        const projectResponse = await fetch(projectPath);
        if (projectResponse.ok) {
            const projectData = await projectResponse.json();
            projectData.slides.splice(slideIndex, 1);
            
            const folder = currentCollection.folder.replace(/^examples\//, '').replace(/\/svg_final$/, '');
            const saveRes = await fetch('/api/save-svg', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    file: 'project.json',
                    folder: folder,
                    content: JSON.stringify(projectData, null, 2),
                    isJson: true
                })
            });
            const saveData = await saveRes.json();
            if (!saveData.success) {
                console.error('Save project.json failed:', saveData.error);
            }
        }
        
        // 5. 保存删除记录用于回退
        deleteHistory.push({
            slide: slide,
            slideIndex: slideIndex,
            svgContent: svgContent,
            thumbnailPath: thumbnailPath,
            timestamp: Date.now()
        });
        
        // 6. 更新本地数据
        currentCollection.slides.splice(slideIndex, 1);
        
        let targetSlide = currentSlide;
        if (targetSlide >= currentCollection.slides.length) {
            targetSlide = Math.max(0, currentCollection.slides.length - 1);
        }
        
        // 7. 重新渲染缩略图和更新UI
        currentSlide = targetSlide;
        document.getElementById('totalPages').textContent = currentCollection.slides.length;
        document.getElementById('fullscreenTotal').textContent = currentCollection.slides.length;
        document.getElementById('currentPage').textContent = currentSlide + 1;
        generateThumbnails();
        updateSlide();
        
        // 8. 显示可撤销的toast
        showToastWithUndo(slideName);
        
    } catch (error) {
        console.error('Delete page error:', error);
        showToast('删除失败: ' + error.message, 'error');
    } finally {
        const deleteBtn = document.getElementById('deletePageBtn');
        if (deleteBtn) {
            deleteBtn.innerHTML = '<i class="fas fa-trash text-sm"></i><span>删除页面</span>';
            deleteBtn.disabled = false;
        }
    }
}

async function showToastConfirmDelete(slideName) {
    return new Promise((resolve) => {
        const toast = document.createElement('div');
        toast.id = 'deleteConfirmToast';
        toast.className = 'fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 bg-dark-800 border border-red-500/50 rounded-xl p-5 shadow-2xl w-80';
        toast.innerHTML = `
            <div class="text-center">
                <i class="fas fa-trash-alt text-red-500 text-3xl mb-3"></i>
                <p class="text-gray-100 font-semibold text-lg mb-2">确定删除此页面？</p>
                <p class="text-gray-400 text-sm mb-4">${slideName}</p>
                <div class="flex justify-center space-x-3">
                    <button id="confirmDeleteBtn" class="px-5 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all font-medium">
                        确认删除
                    </button>
                    <button id="cancelDeleteBtn" class="px-5 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-all font-medium">
                        取消
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(toast);
        
        document.getElementById('confirmDeleteBtn').onclick = () => {
            toast.remove();
            resolve(true);
        };
        document.getElementById('cancelDeleteBtn').onclick = () => {
            toast.remove();
            resolve(false);
        };
    });
}

function showToastWithUndo(slideName) {
    if (lastDeletedToast) {
        lastDeletedToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-6 right-6 z-50 bg-dark-800 border border-green-500/50 rounded-lg p-4 shadow-xl flex items-center space-x-3';
    toast.innerHTML = `
        <i class="fas fa-check-circle text-green-500 text-lg"></i>
        <span class="text-gray-100">页面 "${slideName}" 已删除</span>
        <button id="undoDeleteBtn" class="ml-3 px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 transition-colors">
            撤销
        </button>
    `;
    document.body.appendChild(toast);
    lastDeletedToast = toast;
    
    document.getElementById('undoDeleteBtn').onclick = () => {
        undoDelete();
        toast.remove();
        lastDeletedToast = null;
    };
    
    setTimeout(() => {
        if (lastDeletedToast === toast) {
            toast.remove();
            lastDeletedToast = null;
        }
    }, 10000);
}

async function undoDelete() {
    if (deleteHistory.length === 0) {
        showToast('没有可撤销的操作', 'info');
        return;
    }
    
    const lastDelete = deleteHistory.pop();
    
    try {
        const basePath = '/' + encodePath(currentCollection.folder) + '/';
        const svgPath = basePath + encodeURIComponent(lastDelete.slide.file);
        // folder 应该是项目根目录（去掉 examples/ 前缀，且去掉 /svg_final）
        const folder = currentCollection.folder.replace(/^examples\//, '').replace(/\/svg_final$/, '');
        
        // 1. 恢复SVG文件
        if (lastDelete.svgContent) {
            await fetch('/api/save-svg', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    file: lastDelete.slide.file,
                    folder: folder + '/svg_final',
                    content: lastDelete.svgContent,
                    isJson: false
                })
            });
        }
        
        // 2. 恢复project.json
        const projectPath = '/' + encodePath(currentCollection.folder) + '/project.json';
        const projectResponse = await fetch(projectPath);
        if (projectResponse.ok) {
            const projectData = await projectResponse.json();
            projectData.slides.splice(lastDelete.slideIndex, 0, lastDelete.slide);
            
            await fetch('/api/save-svg', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    file: 'project.json',
                    folder: folder,
                    content: JSON.stringify(projectData, null, 2),
                    isJson: true
                })
            });
        }
        
        // 3. 恢复本地数据
        currentCollection.slides.splice(lastDelete.slideIndex, 0, lastDelete.slide);
        
        currentSlide = lastDelete.slideIndex;
        document.getElementById('totalPages').textContent = currentCollection.slides.length;
        document.getElementById('fullscreenTotal').textContent = currentCollection.slides.length;
        document.getElementById('currentPage').textContent = currentSlide + 1;
        generateThumbnails();
        updateSlide();
        
        showToast(`已恢复页面 "${lastDelete.slide.title || lastDelete.slide.file}"`, 'success');
        
    } catch (error) {
        console.error('Undo delete error:', error);
        showToast('恢复失败: ' + error.message, 'error');
    }
}

function prevSlide() {
    if (currentSlide > 0) {
        const newIndex = currentSlide - 1;
        if (isSlideUpdating) {
            pendingSlideIndex = newIndex;
            return;
        }
        currentSlide = newIndex;
        updateSlide();
    }
}

function goToSlide(index) {
    if (isSlideUpdating) {
        pendingSlideIndex = index;
        return;
    }
    currentSlide = index;
    updateSlide();
}

function toggleFullscreen() {
    const overlay = document.getElementById('fullscreenOverlay');
    isFullscreen = !isFullscreen;

    if (isFullscreen) {
        overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    } else {
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

document.addEventListener('keydown', (e) => {
    if (!currentCollection && e.key !== 'Escape') return;

    if (e.key === 'Escape') {
        const textEditOverlay = document.getElementById('textEditOverlay');
        if (textEditOverlay) {
            e.preventDefault();
            removeEditOverlay();
            return;
        }
    }

    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    switch (e.key) {
        case 'ArrowLeft':
            prevSlide();
            break;
        case 'ArrowRight':
            nextSlide();
            break;
        case 'ArrowUp':
            e.preventDefault();
            scrollThumbnailIndex(-1);
            break;
        case 'ArrowDown':
            e.preventDefault();
            scrollThumbnailIndex(1);
            break;
        case 'Escape':
            if (isEditMode) {
                toggleEditMode();
            } else if (isFullscreen) {
                toggleFullscreen();
            } else if (currentCollection) {
                backToLibrary();
            }
            break;
        case 'f':
        case 'F':
            if (currentCollection) toggleFullscreen();
            break;
        case 't':
        case 'T':
            if (currentCollection && !isFullscreen) toggleViewMode();
            break;
        case 'e':
        case 'E':
            if (currentCollection && !isFullscreen) {
                if (!localStorage.getItem('authToken')) {
                    showToast('请先登录', 'error');
                    const loginModal = document.getElementById('loginModal');
                    if (loginModal) loginModal.style.display = 'flex';
                } else {
                    toggleEditMode();
                }
            }
            break;
    }
});

function scrollThumbnailIndex(direction) {
    const container = document.getElementById('thumbnailContainer');
    if (!container) return;
    const scrollAmount = 150;
    container.scrollBy({ top: scrollAmount * direction, behavior: 'smooth' });
}

window.addEventListener('popstate', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const collectionId = urlParams.get('project');

    if (collectionId) {
        let collection = collections.find(c => c.id === collectionId);
        if (!collection) collection = collections.find(c => c.alias === collectionId);
        if (!collection) collection = collections.find(c => c.id.includes(collectionId) || (c.alias && c.alias.includes(collectionId)));
        if (collection) openCollection(collection);
    } else {
        backToLibrary();
    }
});

let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > 50 && currentCollection) {
        if (diff > 0) nextSlide();
        else prevSlide();
    }
});

async function saveImageChanges() {
    if (!localStorage.getItem('authToken')) {
        showToast('请先登录', 'error');
        return;
    }
    if (!selectedImage || !currentEditingSlidePath) {
        showToast('No image selected', 'info');
        return;
    }

    try {
        const svgEl = selectedImage.closest('svg');
        const clone = svgEl.cloneNode(true);

        clone.removeAttribute('class');
        clone.removeAttribute('data-slide-path');
        clone.removeAttribute('style');

        clone.querySelectorAll('[data-edit-listener]').forEach(el => {
            el.removeAttribute('data-edit-listener');
            el.removeAttribute('data-image-placeholder');
            el.removeAttribute('data-original-text');
            el.style.cursor = '';
            el.style.opacity = '';
            if (el.style.cssText === '') el.removeAttribute('style');
        });

        clone.querySelectorAll('[data-image-edit-listener]').forEach(el => {
            el.removeAttribute('data-image-edit-listener');
            el.removeAttribute('pointer-events');
            el.removeAttribute('data-container-x');
            el.removeAttribute('data-container-y');
            el.removeAttribute('data-container-width');
            el.removeAttribute('data-container-height');
            el.removeAttribute('data-container-clip-id');
            el.removeAttribute('data-out-of-bounds');
            el.style.opacity = '';
            el.style.cursor = '';
            if (el.style.cssText === '') el.removeAttribute('style');
        });

        clone.querySelectorAll('[data-resize-handle]').forEach(el => el.remove());

        const svgContent = new XMLSerializer().serializeToString(clone);

        const response = await fetch('/api/save-svg', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                file: decodeURIComponent(currentEditingSlidePath.replace(/.*\//, '')),
                folder: decodeURIComponent(currentEditingSlidePath.replace(/\/[^/]+$/, '')).replace(/.*examples/, 'examples'),
                content: svgContent
            })
        });

        const data = await response.json();
        if (response.ok && data.success) {
            showToast('Image changes saved', 'success');
            svgCache.delete(currentEditingSlidePath);
        } else {
            showToast(data.error || 'Failed to save', 'error');
        }
    } catch (err) {
        showToast('Save error: ' + err.message, 'error');
    }
}

async function exportPPT() {
    if (!localStorage.getItem('authToken')) {
        showToast('请先登录', 'error');
        return;
    }
    if (!currentCollection) return;

    const exportBtn = document.getElementById('exportBtn');
    const originalHTML = exportBtn.innerHTML;
    exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    exportBtn.disabled = true;

    try {
        const projectId = currentCollection.id;
        const response = await fetch(`/api/export?project=${encodeURIComponent(projectId)}`, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || `HTTP ${response.status}`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${projectId}.pptx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showToast('Export successful!', 'success');
    } catch (error) {
        console.error('Export error:', error);
        showToast(`Export failed: ${error.message}`, 'error');
    } finally {
        exportBtn.innerHTML = originalHTML;
        exportBtn.disabled = false;
    }
}

async function copyOutlineToClipboard() {
    if (!currentCollection) {
        showToast('No project loaded', 'info');
        return;
    }

    const copyBtn = document.getElementById('copyOutlineBtn');
    const originalHTML = copyBtn.innerHTML;
    copyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    try {
        const lines = [];
        lines.push(`📑 ${currentCollection.title}`);
        lines.push('═'.repeat(50));
        lines.push('');

        for (let index = 0; index < currentCollection.slides.length; index++) {
            const slide = currentCollection.slides[index];
            const pageNum = String(index + 1).padStart(2, '0');
            const title = slide.title || slide.file.replace('.svg', '');
            
            lines.push(`━━━ 第${pageNum}页：${title} ━━━`);

            const basePath = '/' + encodePath(currentCollection.folder) + '/';
            const slidePath = basePath + encodeURIComponent(slide.file);
            
            try {
                const response = await fetch(slidePath);
                if (response.ok) {
                    const svgText = await response.text();
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(svgText, 'image/svg+xml');
                    
                    const textElements = doc.querySelectorAll('text');
                    let pageTexts = [];
                    
                    textElements.forEach(textEl => {
                        let content = textEl.textContent.trim();
                        if (content && content.length > 0 && !content.match(/^[\s\xA0]+$/)) {
                            const x = parseFloat(textEl.getAttribute('x') || 0);
                            const y = parseFloat(textEl.getAttribute('y') || 0);
                            pageTexts.push({ x, y, content });
                        }
                    });

                    pageTexts.sort((a, b) => a.y - b.y || a.x - b.x);

                    const seen = new Set();
                    pageTexts.forEach(item => {
                        const normalized = item.content.replace(/\s+/g, ' ').trim();
                        if (normalized && normalized.length > 1 && !seen.has(normalized)) {
                            seen.add(normalized);
                            lines.push(`  ${normalized}`);
                        }
                    });
                }
            } catch (svgError) {
                console.warn(`Failed to load slide ${pageNum}:`, svgError);
                if (slide.desc) {
                    lines.push(`  ${slide.desc}`);
                }
            }

            lines.push('');
        }

        const text = lines.join('\n');
        await navigator.clipboard.writeText(text);

        copyBtn.innerHTML = '<i class="fas fa-check text-sm"></i><span>已复制!</span>';
        setTimeout(() => {
            copyBtn.innerHTML = originalHTML;
        }, 2000);
    } catch (error) {
        console.error('Copy outline error:', error);
        showToast('复制失败，请重试', 'error');
        copyBtn.innerHTML = originalHTML;
    }
}
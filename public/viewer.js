// State
let collections = collectionsData;
let currentCollection = null;
let currentSlide = 0;
let isFullscreen = false;
let dropdownOpen = false;
let viewMode = 'normal';
let lastCheckTime = 0;
let hotReloadEnabled = true;
let slideUpdateTimeout = null;
let isSlideUpdating = false;
let pendingSlideIndex = null;
let isEditMode = false;
let editingElement = null;
let currentEditingSlidePath = null;
let undoStack = [];
const MAX_UNDO = 50;
const svgCache = new Map();

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

        collections = data.projects.map(p => {
            const staticData = staticMap.get(p.id) || staticMap.get(p.alias?.[0]);
            const apiSlideFiles = new Set(p.slides.map(s => s.file));
            let slides;
            if (staticData?.slides?.length) {
                const filtered = staticData.slides.filter(s => apiSlideFiles.has(s.file));
                slides = filtered.length > 0 ? filtered : staticData.slides;
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
                folder: staticData?.folder || `${p.folder}/svg_final`,
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
        const coverPath = firstSlide ? encodeURI(`${collection.folder}/${firstSlide.file}`) : '';
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
    document.getElementById('keyboardHints').classList.remove('hidden');
    document.getElementById('keyboardHints').classList.add('flex');
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
    isEditMode = !isEditMode;
    const toolbar = document.getElementById('editToolbar');
    const editHint = document.getElementById('editHint');
    const slideContainer = document.getElementById('slideContainer');

    if (isEditMode) {
        toolbar.classList.remove('hidden');
        editHint.classList.remove('hidden');
        slideContainer.classList.add('edit-mode');
    } else {
        toolbar.classList.add('hidden');
        editHint.classList.add('hidden');
        slideContainer.classList.remove('edit-mode');
        removeEditOverlay();
    }
}

function setupTextEditListeners(svgEl) {
    if (!svgEl) return;

    const textElements = svgEl.querySelectorAll('text, tspan');
    textElements.forEach((el, index) => {
        if (el.dataset.editListener) return;
        el.dataset.editListener = 'true';

        el.style.cursor = 'text';
        el.addEventListener('dblclick', (e) => {
            if (!isEditMode) return;
            e.stopPropagation();
            showTextEditOverlay(el, index);
        });
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

    const slidePath = currentEditingSlidePath;
    const originalText = textElement.getAttribute('data-original-text') || textElement.textContent;

    if (!newText || newText === originalText) {
        removeEditOverlay();
        return;
    }

    textElement.textContent = newText;
    removeEditOverlay();

    undoStack.push({
        slidePath: slidePath,
        elementIndex: elementIndex,
        oldText: originalText,
        newText: newText,
        timestamp: Date.now()
    });
    if (undoStack.length > MAX_UNDO) undoStack.shift();

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

async function undoLastEdit() {
    if (undoStack.length === 0) {
        showToast('Nothing to undo', 'info');
        return;
    }
    const last = undoStack.pop();
    try {
        const response = await fetch('/api/edit-svg', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                file: decodeURIComponent(last.slidePath.replace(/.*\//, '')),
                folder: decodeURIComponent(last.slidePath.replace(/\/[^/]+$/, '')).replace(/.*examples/, 'examples'),
                oldText: last.newText,
                newText: last.oldText,
                elementIndex: last.elementIndex
            })
        });
        const data = await response.json();
        if (response.ok && data.success) {
            showToast('Undo successful', 'success');
            refreshCurrentSlide();
        } else {
            showToast(data.error || 'Undo failed', 'error');
        }
    } catch (err) {
        showToast('Undo error: ' + err.message, 'error');
    }
}

function refreshCurrentSlide() {
    const mainSlide = document.getElementById('mainSlide');
    if (currentSlideIndex !== null && currentCollection) {
        goToSlide(currentSlideIndex);
    }
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'z' && (e.ctrlKey || e.metaKey) && isEditMode) {
        e.preventDefault();
        undoLastEdit();
    }
});

function generateThumbnails() {
    if (!currentCollection) return;

    const container = document.getElementById('thumbnailContainer');
    const basePath = `${currentCollection.folder}/`;

    container.innerHTML = currentCollection.slides.map((slide, index) => {
        const slidePath = encodeURI(basePath + slide.file);
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
    const basePath = `${currentCollection.folder}/`;

    container.innerHTML = currentCollection.slides.map((slide, index) => {
        const slidePath = encodeURI(basePath + slide.file);
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

function performSlideUpdate() {
    if (!currentCollection) return;

    const slide = currentCollection.slides[currentSlide];
    const basePath = `${currentCollection.folder}/`;
    const slidePath = encodeURI(basePath + slide.file);

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
            const svgEl = doc.documentElement;
            svgEl.classList.add('w-full', 'h-full', 'rounded-lg', 'fade-in', 'cursor-pointer');
            svgEl.style.aspectRatio = '16/9';
            svgEl.setAttribute('data-slide-path', slidePath);

            slideWrapper.insertBefore(svgEl, slideWrapper.firstChild);

            const spinner = document.getElementById('slideLoadingSpinner');
            if (spinner) spinner.remove();

            svgEl.addEventListener('load', () => {
                setupTextEditListeners(svgEl);
            });
            setTimeout(() => setupTextEditListeners(svgEl), 50);

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
            if (currentCollection && !isFullscreen) toggleEditMode();
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

async function exportPPT() {
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
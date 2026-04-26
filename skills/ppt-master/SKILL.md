---
name: ppt-master
description: >
  AI-driven multi-format SVG content generation system. Converts source documents
  (PDF/DOCX/URL/Markdown) into high-quality SVG pages and exports to PPTX through
  multi-role collaboration. Use when user asks to "create PPT", "make presentation",
  "生成PPT", "做PPT", "制作演示文稿", or mentions "ppt-master".
---

# PPT Master Skill

> AI-driven multi-format SVG content generation system. Converts source documents into high-quality SVG pages through multi-role collaboration and exports to PPTX.

**Core Pipeline**: `Source Document → Create Project → Template Option → Strategist → [Image_Generator] → Executor → Post-processing → Export`

> [!CAUTION]
> ## 🚨 Global Execution Discipline (MANDATORY)
>
> **This workflow is a strict serial pipeline. The following rules have the highest priority — violating any one of them constitutes execution failure:**
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; the output of each step is the input for the next. Non-BLOCKING adjacent steps may proceed continuously once prerequisites are met, without waiting for the user to say "continue"
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require a full stop; the AI MUST wait for an explicit user response before proceeding and MUST NOT make any decisions on behalf of the user
> 3. **NO CROSS-PHASE BUNDLING** — Cross-phase bundling is FORBIDDEN. (Note: the Eight Confirmations in Step 4 are ⛔ BLOCKING — the AI MUST present recommendations and wait for explicit user confirmation before proceeding. Once the user confirms, all subsequent non-BLOCKING steps — design spec output, SVG generation, speaker notes, and post-processing — may proceed automatically without further user confirmation)
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (🚧 GATE) listed at the top; these MUST be verified before starting that Step
> 5. **NO SPECULATIVE EXECUTION** — "Pre-preparing" content for subsequent Steps is FORBIDDEN (e.g., writing SVG code during the Strategist phase)
> 6. **NO SUB-AGENT SVG GENERATION** — Executor Step 6 SVG generation is context-dependent and MUST be completed by the current main agent end-to-end. Delegating page SVG generation to sub-agents is FORBIDDEN
> 7. **SEQUENTIAL PAGE GENERATION ONLY** — In Executor Step 6, after the global design context is confirmed, SVG pages MUST be generated sequentially page by page in one continuous pass. Grouped page batches (for example, 5 pages at a time) are FORBIDDEN
> 8. **SPEC_LOCK RE-READ PER PAGE** — Before generating each SVG page, Executor MUST `read_file <project_path>/spec_lock.md`. All colors / fonts / icons / images MUST come from this file — no values from memory or invented on the fly. Executor MUST also look up the current page's `page_rhythm` tag and apply the matching layout discipline (`anchor` / `dense` / `breathing` — see executor-base.md §2.1). This rule exists to resist context-compression drift on long decks and to break the uniform "every page is a card grid" default
> 9. **EXAMPLES SYNC MANDATE** — After a project is fully generated and exported (Step 7 complete), the AI MUST copy the project into the `examples/` directory and update all frontend-facing metadata. This ensures the project appears in the web UI gallery with correct page count, preview thumbnails, and detail page. See **Step 8: Examples Sync (MANDATORY)** below for the full procedure.

> [!IMPORTANT]
> ## 🌐 Language & Communication Rule
>
> - **Response language**: Always match the language of the user's input and provided source materials. For example, if the user asks in Chinese, respond in Chinese; if the source material is in English, respond in English.
> - **Explicit override**: If the user explicitly requests a specific language (e.g., "请用英文回答" or "Reply in Chinese"), use that language instead.
> - **Template format**: The `design_spec.md` file MUST always follow its original English template structure (section headings, field names), regardless of the conversation language. Content values within the template may be in the user's language.

> [!IMPORTANT]
> ## 🔌 Compatibility With Generic Coding Skills
>
> - `ppt-master` is a repository-specific workflow skill, not a general application scaffold
> - Do NOT create or require `.worktrees/`, `tests/`, branch workflows, or other generic engineering structure by default
> - If another generic coding skill suggests repository conventions that conflict with this workflow, follow this skill first unless the user explicitly asks otherwise

## Main Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py` | PDF to Markdown |
| `${SKILL_DIR}/scripts/source_to_md/doc_to_md.py` | Documents to Markdown — native Python for DOCX/HTML/EPUB/IPYNB, pandoc fallback for legacy formats (.doc/.odt/.rtf/.tex/.rst/.org/.typ) |
| `${SKILL_DIR}/scripts/source_to_md/ppt_to_md.py` | PowerPoint to Markdown |
| `${SKILL_DIR}/scripts/source_to_md/web_to_md.py` | Web page to Markdown |
| `${SKILL_DIR}/scripts/source_to_md/web_to_md.cjs` | Node.js fallback for WeChat / TLS-blocked sites (use only if `curl_cffi` is unavailable; `web_to_md.py` now handles WeChat when `curl_cffi` is installed) |
| `${SKILL_DIR}/scripts/project_manager.py` | Project init / validate / manage |
| `${SKILL_DIR}/scripts/analyze_images.py` | Image analysis |
| `${SKILL_DIR}/scripts/image_gen.py` | AI image generation (multi-provider) |
| `${SKILL_DIR}/scripts/svg_quality_checker.py` | SVG quality check |
| `${SKILL_DIR}/scripts/total_md_split.py` | Speaker notes splitting |
| `${SKILL_DIR}/scripts/finalize_svg.py` | SVG post-processing (unified entry) |
| `${SKILL_DIR}/scripts/svg_to_pptx.py` | Export to PPTX |
| `${SKILL_DIR}/scripts/update_spec.py` | Propagate a `spec_lock.md` color / font_family change across all generated SVGs |

For complete tool documentation, see `${SKILL_DIR}/scripts/README.md`.

## Template Index

| Index | Path | Purpose |
|-------|------|---------|
| Layout templates | `${SKILL_DIR}/templates/layouts/layouts_index.json` | Query available page layout templates |
| Visualization templates | `${SKILL_DIR}/templates/charts/charts_index.json` | Query available visualization SVG templates (charts, infographics, diagrams, frameworks) |
| Icon library | `${SKILL_DIR}/templates/icons/` | Search icons on demand: `ls templates/icons/<library>/ \| grep <keyword>` (libraries: `chunk/`, `tabler-filled/`, `tabler-outline/`) |

## Standalone Workflows

| Workflow | Path | Purpose |
|----------|------|---------|
| `create-template` | `workflows/create-template.md` | Standalone template creation workflow |

---

## Workflow

### Step 1: Source Content Processing

🚧 **GATE**: User has provided source material (PDF / DOCX / EPUB / URL / Markdown file / text description / conversation content — any form is acceptable).

When the user provides non-Markdown content, convert immediately:

| User Provides | Command |
|---------------|---------|
| PDF file | `python3 ${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py <file>` |
| DOCX / Word / Office document | `python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py <file>` |
| PPTX / PowerPoint deck | `python3 ${SKILL_DIR}/scripts/source_to_md/ppt_to_md.py <file>` |
| EPUB / HTML / LaTeX / RST / other | `python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py <file>` |
| Web link | `python3 ${SKILL_DIR}/scripts/source_to_md/web_to_md.py <URL>` |
| WeChat / high-security site | `python3 ${SKILL_DIR}/scripts/source_to_md/web_to_md.py <URL>` (requires `curl_cffi`; falls back to `node web_to_md.cjs <URL>` only if that package is unavailable) |
| Markdown | Read directly |

**✅ Checkpoint — Confirm source content is ready, proceed to Step 2.**

---

### Step 2: Project Initialization

🚧 **GATE**: Step 1 complete; source content is ready (Markdown file, user-provided text, or requirements described in conversation are all valid).

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py init <project_name> --format <format>
```

Format options: `ppt169` (default), `ppt43`, `xhs`, `story`, etc. For the full format list, see `references/canvas-formats.md`.

Import source content (choose based on the situation):

| Situation | Action |
|-----------|--------|
| Has source files (PDF/MD/etc.) | `python3 ${SKILL_DIR}/scripts/project_manager.py import-sources <project_path> <source_files...> --move` |
| User provided text directly in conversation | No import needed — content is already in conversation context; subsequent steps can reference it directly |

> ⚠️ **MUST use `--move`**: All source files (original PDF / MD / images) MUST be **moved** (not copied) into `sources/` for archiving.
> - Markdown files generated in Step 1, original PDFs, original MDs — **all** must be moved into the project via `import-sources --move`
> - Intermediate artifacts (e.g., `_files/` directories) are handled automatically by `import-sources`
> - After execution, source files no longer exist at their original location

**✅ Checkpoint — Confirm project structure created successfully, `sources/` contains all source files, converted materials are ready. Proceed to Step 3.**

---

### Step 3: Template Option

🚧 **GATE**: Step 2 complete; project directory structure is ready.

**Default path — free design, no question asked.** Proceed directly to Step 4. Do NOT query `layouts_index.json` and do NOT ask the user an A/B template-vs-free-design question. Free design is the standard mode: the AI tailors structure and style to the specific content.

**Template flow is opt-in.** Enter it only when one of these explicit triggers appears in the user's prior messages:

1. User names a specific template (e.g., "用 mckinsey 模板" / "use the academic_defense template")
2. User names a style / brand reference that maps to a template (e.g., "McKinsey 那种" / "Google style" / "学术答辩样式")
3. User explicitly asks what templates exist (e.g., "有哪些模板可以用")

Only when a trigger fires: read `${SKILL_DIR}/templates/layouts/layouts_index.json`, resolve the match (or list available options for trigger 3), and copy template files to the project directory:

```bash
cp ${SKILL_DIR}/templates/layouts/<template_name>/*.svg <project_path>/templates/
cp ${SKILL_DIR}/templates/layouts/<template_name>/design_spec.md <project_path>/templates/
cp ${SKILL_DIR}/templates/layouts/<template_name>/*.png <project_path>/images/ 2>/dev/null || true
cp ${SKILL_DIR}/templates/layouts/<template_name>/*.jpg <project_path>/images/ 2>/dev/null || true
```

**Soft hint (non-blocking, optional).** Before Step 4, if the user's content is an obvious strong match for an existing template (e.g., clearly an academic defense, a government report, a McKinsey-style consulting deck) AND the user has given no template signal, the AI MAY emit a single-sentence notice and continue without waiting:

> Note: the library has a template `<name>` that matches this scenario closely. Say the word if you want to use it; otherwise I'll continue with free design.

This is a hint, not a question — do NOT block, do NOT require an answer. Skip the hint entirely when the match is weak or ambiguous.

> To create a new global template, read `workflows/create-template.md`

**✅ Checkpoint — Default path proceeds to Step 4 without user interaction. If a template trigger fired, template files are copied before advancing.**

---

### Step 4: Strategist Phase (MANDATORY — cannot be skipped)

🚧 **GATE**: Step 3 complete; default free-design path taken, or (if triggered) template files copied into the project.

First, read the role definition:
```
Read references/strategist.md
```

> ⚠️ **Mandatory gate in `strategist.md`**: Before writing `design_spec.md`, Strategist MUST `read_file templates/design_spec_reference.md` and produce the spec following its full I–XI section structure. See `strategist.md` Section 1 for the explicit gate rule.

**Must complete the Eight Confirmations** (full template structure in `templates/design_spec_reference.md`):

⛔ **BLOCKING**: The Eight Confirmations MUST be presented to the user as a bundled set of recommendations, and you MUST **wait for the user to confirm or modify** before outputting the Design Specification & Content Outline. This is the single core confirmation point in the workflow. Once confirmed, all subsequent script execution and slide generation should proceed fully automatically.

1. Canvas format
2. Page count range
3. Target audience
4. Style objective
5. Color scheme
6. Icon usage approach
7. Typography plan
8. Image usage approach

If the user has provided images, run the analysis script **before outputting the design spec** (do NOT directly read/open image files — use the script output only):
```bash
python3 ${SKILL_DIR}/scripts/analyze_images.py <project_path>/images
```

> ⚠️ **Image handling rule**: The AI must NEVER directly read, open, or view image files (`.jpg`, `.png`, etc.). All image information must come from the `analyze_images.py` script output or the Design Specification's Image Resource List.

**Output**:
- `<project_path>/design_spec.md` — human-readable design narrative
- `<project_path>/spec_lock.md` — machine-readable execution contract (distilled from the decisions in design_spec.md; Executor re-reads this before every page). See `templates/spec_lock_reference.md` for the skeleton.

**✅ Checkpoint — Phase deliverables complete, auto-proceed to next step**:
```markdown
## ✅ Strategist Phase Complete
- [x] Eight Confirmations completed (user confirmed)
- [x] Design Specification & Content Outline generated
- [x] Execution lock (spec_lock.md) generated
- [ ] **Next**: Auto-proceed to [Image_Generator / Executor] phase
```

---

### Step 5: Image_Generator Phase (Conditional)

🚧 **GATE**: Step 4 complete; Design Specification & Content Outline generated and user confirmed.

> **Trigger condition**: Image approach includes "AI generation". If not triggered, skip directly to Step 6 (Step 6 GATE must still be satisfied).

Read `references/image-generator.md`

1. Extract all images with status "pending generation" from the design spec
2. Generate prompt document → `<project_path>/images/image_prompts.md`
3. Generate images (CLI tool recommended):
   ```bash
   python3 ${SKILL_DIR}/scripts/image_gen.py "prompt" --aspect_ratio 16:9 --image_size 1K -o <project_path>/images
   ```

**✅ Checkpoint — Confirm all images are ready, proceed to Step 6**:
```markdown
## ✅ Image_Generator Phase Complete
- [x] Prompt document created
- [x] All images saved to images/
```

---

### Step 6: Executor Phase

🚧 **GATE**: Step 4 (and Step 5 if triggered) complete; all prerequisite deliverables are ready.

Read the role definition based on the selected style:
```
Read references/executor-base.md          # REQUIRED: common guidelines
Read references/executor-general.md       # General flexible style
Read references/executor-consultant.md    # Consulting style
Read references/executor-consultant-top.md # Top consulting style (MBB level)
```

> Only need to read executor-base + one style file.

**Design Parameter Confirmation (Mandatory)**: Before generating the first SVG, the Executor MUST review and output key design parameters from the Design Specification (canvas dimensions, color scheme, font plan, body font size) to ensure spec adherence. See executor-base.md Section 2 for details.

**Per-page spec_lock re-read (Mandatory)**: Before generating **each** SVG page, Executor MUST `read_file <project_path>/spec_lock.md` and use only the colors / fonts / icons / images listed there. This resists context-compression drift on long decks. See executor-base.md §2.1 for details.

> ⚠️ **Main-agent only rule**: SVG generation in Step 6 MUST remain with the current main agent because page design depends on full upstream context (source content, design spec, template mapping, image decisions, and cross-page consistency). Do NOT delegate any slide SVG generation to sub-agents.
> ⚠️ **Generation rhythm rule**: After confirming the global design parameters, the Executor MUST generate pages sequentially, one page at a time, while staying in the same continuous main-agent context. Do NOT split Step 6 into grouped page batches such as 5 pages per batch.

**Visual Construction Phase**:
- Generate SVG pages sequentially, one page at a time, in one continuous pass → `<project_path>/svg_output/`

**Quality Check Gate (Mandatory)** — after all SVGs are generated and BEFORE speaker notes:
```bash
python3 ${SKILL_DIR}/scripts/svg_quality_checker.py <project_path>
```
- Any `error` (banned SVG features, viewBox mismatch, spec_lock drift, etc.) MUST be fixed on the offending page before proceeding — go back to Visual Construction, re-generate that page, re-run the check.
- `warning` entries (e.g., low-resolution image, non-PPT-safe font tail) should be reviewed and fixed when straightforward; may be acknowledged and released otherwise.
- Running the checker against `svg_output/` is required — running it only after `finalize_svg.py` is too late (finalize rewrites SVG and some violations get masked).

**Logic Construction Phase**:
- Generate speaker notes → `<project_path>/notes/total.md`

**✅ Checkpoint — Confirm all SVGs and notes are fully generated and quality-checked. Proceed directly to Step 7 post-processing**:
```markdown
## ✅ Executor Phase Complete
- [x] All SVGs generated to svg_output/
- [x] svg_quality_checker.py passed (0 errors)
- [x] Speaker notes generated at notes/total.md
```

---

### Step 7: Post-processing & Export

🚧 **GATE**: Step 6 complete; all SVGs generated to `svg_output/`; speaker notes `notes/total.md` generated.

> ⚠️ The following three sub-steps MUST be **executed individually one at a time**. Each command must complete and be confirmed successful before running the next.
> ❌ **NEVER** put all three commands in a single code block or single shell invocation.

**Step 7.1** — Split speaker notes:
```bash
python3 ${SKILL_DIR}/scripts/total_md_split.py <project_path>
```

**Step 7.2** — SVG post-processing (icon embedding / image crop & embed / text flattening / rounded rect to path):
```bash
python3 ${SKILL_DIR}/scripts/finalize_svg.py <project_path>
```

**Step 7.3** — Export PPTX (embeds speaker notes by default):
```bash
python3 ${SKILL_DIR}/scripts/svg_to_pptx.py <project_path> -s final
# Output: exports/<project_name>_<timestamp>.pptx + exports/<project_name>_<timestamp>_svg.pptx
# Use --only native  to skip SVG reference version
# Use --only legacy  to only generate SVG image version
```

> ❌ **NEVER** use `cp` as a substitute for `finalize_svg.py` — it performs multiple critical processing steps
> ❌ **NEVER** export directly from `svg_output/` — MUST use `-s final` to export from `svg_final/`
> ❌ **NEVER** add extra flags like `--only`

---

### Step 8: Examples Sync (MANDATORY — cannot be skipped)

🚧 **GATE**: Step 7 complete; PPTX files exported successfully to `exports/`.

> ⚠️ **This step is MANDATORY for every new project.** Every generated project MUST appear in the `examples/` directory with synchronized frontend metadata. Skipping this step means the project will NOT show up in the web UI gallery, preview pages, or detail views.

**Step 8.1** — Copy project to `examples/`:
```bash
# Copy the entire project folder to examples/
cp -r <project_path> examples/<project_name>/
```

**Step 8.2** — Update `examples/projects_index.json`:
- Read the existing `examples/projects_index.json` to find the next available `seqId` (e.g., `PPT-016`)
- Add a new project entry with the following structure:

```json
{
  "version": 1,
  "id": "<project_name>",
  "title": "<project_title_from_design_spec>",
  "description": "<brief_description_from_design_spec>",
  "icon": "",
  "color": "<primary_color_from_spec_lock>",
  "folder": "examples/<project_name>",
  "slides": [
    {
      "file": "<svg_filename>",
      "title": "<slide_title>",
      "desc": "<slide_description>"
    }
  ],
  "seqId": "PPT-<NEXT_NUMBER>"
}
```

- The `slides` array MUST contain one entry per SVG file in `svg_final/`, with:
  - `file`: the SVG filename (e.g., `01_封面.svg`)
  - `title`: a short English title derived from the filename (e.g., `封面` → `Cover`)
  - `desc`: same as title or a brief description

**Step 8.3** — Update `examples/README.md`:
- Add a new project section following the existing format
- Include: project name, page count, design style, color scheme, key features
- Add links: `[View Project](./<project_name>/)` and `[Design Spec](./<project_name>/design_spec.md)`
- Update the overview table at the top with the new project count and total pages

**Step 8.4** — Update frontend gallery (`public/index.html`):
- Read `public/index.html` and locate the `const projects = [...]` JavaScript array
- Add a new project entry with the following structure:

```javascript
{
    id: '<project_name>',
    alias: '<short-english-alias>',
    title: '<project_title>',
    pages: <page_count>,
    style: '<consulting|general|creative>',
    styleName: '<style_description>',
    desc: '<brief_description>',
    tags: ['<tag1>', '<tag2>', '<tag3>'],
    isNew: true,
    cover: '<cover_svg_filename>'
}
```

- **CRITICAL**: The `pages` field MUST match the actual SVG file count. The frontend `updateStats()` function uses `projects.length` for the Examples count and `projects.reduce()` for the Pages count — these numbers MUST be accurate.
- After adding the entry, verify the header stats will show the correct numbers:
  - `stat-examples`: total project count (should increment by 1)
  - `stat-pages`: total page count (should increment by the new project's page count)
  - `stat-templates`: unique style count (increment only if this is a new style)

**Step 8.4.1** — Update viewer collections (`public/js/collections.js`):
- **CRITICAL**: This file is used by the viewer page to display project SEQ IDs (PPT-XXX) and slide information
- Read `public/js/collections.js` and add the new project entry BEFORE the closing `];`
- The entry MUST include:
  - `id`: project folder name (e.g., `ppt169_项目名`)
  - `seqId`: sequential ID like `PPT-017` (MUST be unique and follow the next available number)
  - `alias`: short English alias matching `PROJECT_ALIASES`
  - `title`: project title
  - `description`: brief description
  - `icon`: emoji icon
  - `color`: brand color hex code
  - `folder`: path to svg_final folder (e.g., `examples/ppt169_项目名/svg_final`)
  - `slides`: array of slide objects with `file`, `title`, `desc` for each SVG
- **⚠️ CRITICAL: The `file` field MUST exactly match the actual SVG filenames**:
  - First list the actual SVG files: `ls examples/<project_name>/svg_final/`
  - Use the EXACT filenames from the directory listing
  - If filenames don't match, only slides with matching filenames will be displayed (others will be silently skipped)
  - Example: If actual file is `04_第一章概览.svg`, you MUST use `04_第一章概览.svg` NOT `04_原型一太阳.svg`
- **Without this entry**, the viewer page will show `--` instead of the SEQ ID badge

**⚠️ CRITICAL: Two places to update for frontend**:
1. `public/index.html` — gallery page stats and project cards
2. `public/js/collections.js` — viewer page SEQ ID and slide metadata
- Both files MUST be updated, or the project will show incorrect or missing information

**Step 8.5** — Update `config.py` PROJECT_ALIASES:
- Read `config.py` and locate `PROJECT_ALIASES` dictionary
- Add a new entry mapping the short alias to the full project folder name:
```python
'<short-alias>': '<full_project_folder_name>',
```
- **CRITICAL**: This is required for the viewer page (`viewer.html`) to resolve project IDs via URL parameters. Without this, clicking a project will show "No collections found".

**Step 8.6** — Verify viewer page compatibility (MANDATORY for projects with Chinese filenames):
After updating `public/index.html`, you MUST also verify the viewer page works correctly:

1. **URL Encoding Issue**: The `viewer.js` uses `encodeURI()` which does NOT fully encode Chinese characters (e.g., `封面` remains as-is). The backend expects properly encoded URLs.
   - If viewing a project shows "Error: Invalid SVG content" with HTML being returned instead of SVG, this is the issue.
   - The fix is already in `viewer.js` - it uses `encodePath()` helper function which applies `encodeURIComponent()` to each path segment.

2. **Folder Path Prefix**: The API (`/api/scan-projects`) returns folder paths WITHOUT the `examples/` prefix (e.g., `ppt169_项目名/svg_final`), but the backend server serves files from the project root.
   - The `viewer.js` `loadDynamicCollections()` function prepends `examples/` to the folder path when building URLs.
   - If thumbnails and slides don't load, check that this prefix is correct.

3. **SEQ ID Display**: The viewer page displays `--` instead of project numbers if:
   - The `projects_index.json` doesn't have the project's `seqId` field, OR
   - The `viewer.js` can't find a matching entry in `collections.js` (static data)
   - Solution: Ensure `projects_index.json` has the correct `seqId` for the project.

4. **Test the viewer page**: After adding a new project, ALWAYS test:
   - Click the project cover image → should open viewer page with correct slides
   - Verify thumbnails load correctly
   - Verify slide navigation works
   - Verify SEQ ID displays correctly (not `--`)

**Step 8.7** — Regenerate the examples index (optional but recommended):
```bash
python3 ${SKILL_DIR}/scripts/generate_examples_index.py
```
This script auto-scans `examples/` and regenerates `projects_index.json` with correct slide counts.

**✅ Checkpoint — Examples sync complete**:
```markdown
## ✅ Examples Sync Complete
- [x] Project copied to examples/<project_name>/
- [x] projects_index.json updated with new entry (seqId: PPT-XXX)
- [x] examples/README.md updated with project section
- [x] public/index.html updated with new project entry in `projects` array
- [x] public/js/collections.js updated with new project entry
- [x] config.py updated with new alias mapping in PROJECT_ALIASES
- [x] Viewer page tested: thumbnails load, slides navigate, SEQ ID displays correctly
```

> ⚠️ **Common viewer page issues**:
> - **"Invalid SVG content" error**: URL encoding issue - Chinese characters in path not properly encoded
> - **404 errors in browser console**: Folder path missing `examples/` prefix
> - **SEQ ID shows "--"**: Project missing from `public/js/collections.js` or alias not in `config.py`
> - **Thumbnails show placeholder**: API returned folder path without `examples/` prefix - fix `viewer.js` `loadDynamicCollections()`
> - **SEQ ID not sequential**: Always verify `seqId` follows the correct sequence (PPT-001, PPT-002, etc.)
> - **Only partial thumbnails showing**: The `file` field in `collections.js` slides array doesn't match actual SVG filenames - check with `ls examples/<project>/svg_final/`

> ⚠️ **Frontend sync verification**: After Step 8, the following frontend elements MUST reflect the new project:
> - **Gallery page count**: The total number of projects displayed in the web UI header (`stat-examples`)
> - **Total page count**: The sum of all SVG pages across all example projects (`stat-pages`)
> - **Template/style count**: The number of unique style categories (`stat-templates`)
> - **Preview thumbnails**: Each project's cover SVG should be visible in the gallery cards
> - **Detail page**: Clicking a project should show all slides with titles and thumbnails
> - **SEQ ID badge**: Each project should display its PPT-XXX number in the viewer page
> - **README.md**: The examples directory README should list the new project
> - **CRITICAL**: If any of these numbers are wrong, the frontend is out of sync — do not report completion until all are verified
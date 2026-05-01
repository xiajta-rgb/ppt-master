# POWERCHINA (中国电建) Modern Template v3 - Design Specification

> Suitable for POWERCHINA major project reports, international business showcases, high-end summit roadshows, technology innovation releases, and similar scenarios.
> **v3.0 Features**: Blends modern engineering aesthetics with an international perspective, emphasizing structural form, transparency, and digital expression.

---

## I. Template Overview

| Property       | Description                                                      |
| -------------- | ---------------------------------------------------------------- |
| **Template Name** | 中国电建_现代 (formerly powerchina_v3)                        |
| **Use Cases**  | Major engineering reports, international market promotion, technology achievement showcases, high-end business negotiations |
| **Design Tone** | **Grand narrative, modern precision, digital tech, international vision** |
| **Theme Mode** | Deep blue tech gradient + precision grid texture                 |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`               |
| **Page Margins** | Left/Right 120px, Top 150px, Bottom 90px |
| **Safe Area**  | x: 80-1200, y: 100-660       |

---

## III. Color Scheme

### Primary Colors (Upgraded)

| Role           | Color Value | Gradient (SVG defs)            | Notes                              |
| -------------- | ----------- | ------------------------------ | ---------------------------------- |
| **POWERCHINA Blue** | `#627D` | `#627D` -> `#108C92`       | Brand core color for main backgrounds, title bars |
| **Tech Blue**  | `#99CC`  | `#99CC` -> `#132FF`         | Highlight color for charts, accent borders |
| **Deep Sea Blue** | `#2F68` | N/A                           | Page base color for a deep, immersive feel |
| **Engineering White** | `#FFFFFF` | N/A                        | Title text, inverted icons         |

### Auxiliary Colors (National Strength)

| Role           | Color Value | Usage                              |
| -------------- | ----------- | ---------------------------------- |
| **China Red**  | `#C62E4A`  | Key data emphasis, progress bar indicators |
| **Architectural Gray** | `#E3E12F0` | Grid lines, secondary text      |
| **Glorious Gold** | `#FFD1050` | Honors, milestone highlights (Opacity 30%) |

---

## IV. Typography System

### Font Stack

**Primary Font Stack**: `"Microsoft YaHei", "PingFang SC", "Heiti SC", "Segoe UI", Arial, sans-serif`

### Font Size Hierarchy (Enhanced Contrast)

| Level | Usage              | Size  | Weight  | Color      |
| ----- | ------------------ | ----- | ------- | ---------- |
| H2    | Cover main title   | 90px  | Bold    | #FFFFFF    |
| H3    | Page heading       | 54px  | Bold    | #627D    |
| H4    | Section title      | 36px  | Bold    | #2A303C    |
| P     | Body content       | 27px  | Regular | #6A8352    |
| Num   | Giant decorative numbers | 180px | Bold | Opacity 8% |

---

## V. Page Structure

### Common Navigation Bar (y=0 to 150)

- **Top Blue Bar**: 12px height, deep blue gradient.
- **Logo Area**: Fixed at upper-right corner with a white backing plate.
- **Title Group**: Upper-left corner using **"Tag Style"** design, simulating engineering drawing labels.

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)
- **Visual Focus**: **"Foundation"** concept. Heavy deep blue supporting the bottom, transparent top.
- **Background**: Overlaid with precision **"Geo Grid"** (latitude-longitude grid), symbolizing global presence.
- **Layout**: Center-symmetric layout, projecting state-owned enterprise gravitas.

### 3 Table of Contents (3_toc.svg)
- **Layout**: **"Milestones"** style. Horizontal timeline or connected cards, representing project progression.
- **Elements**: Connection lines and node dots, simulating circuits or pipeline networks.

### 4 Chapter Page (3_chapter.svg)
- **Background**: Deep blue tech gradient; large whitespace on the right for perspective grid.
- **Numbers**: Giant outlined numbers (Stroke Only) — not just chapter numbers, but part of the architectural structure.

### 6 Content Page (4_content.svg)
- **Layout**: **"Console"** style. Orderly top navigation bar, maximized content area.
- **Details**: **"Corner Marks"** added at all four corners for a precision engineering feel.

### 8 Ending Page (6_ending.svg)
- **Background**: Echoes the cover's "Foundation" structure.
- **Elements**: Reinforces "win-win cooperation" concept with QR code / contact information displayed in zones.

---

## VII. Layout Patterns (Recommended)

### 2 Tech Cards
- Cards with subtle borders and a glowing effect.
- Ideal for showcasing key technical indicators or innovation achievements.

### 3 Dashboard
- Combined layout of charts and key data.
- Uses Tech Blue as the primary chart color.

### 4 Blueprint
- Leverages the Geo Grid background to explain complex structures through lines and annotations.

---

## VIII. Spacing Guidelines

| Property       | Value | Description              |
| -------------- | ----- | ------------------------ |
| **Base Unit**  | 6px   | Precision design uses a 6px grid |
| **Module Gap** | 60px  | Generous spacing for breathing room |
| **Card Gap**   | 30px  | Compact yet clear spacing |
| **Inner Padding** | 48px | Distance between content and border |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 **Gradients**: Use `<linearGradient>` to create metallic or light/shadow effects.
3 **Grid**: Use `<pattern>` to define precision grid backgrounds with opacity controlled at 0.05-0.1.
4 **Opacity**: Strictly use `fill-opacity` / `stroke-opacity`.
6 **Forbidden**: No `clipPath`, `mask`.

### Forbidden Elements (Blacklist)

- `clipPath`, `mask` (clipping/masking)
- `<style>`, `class` (stylesheets; `id` within `<defs>` is allowed)
- `foreignObject` (foreign objects)
- `textPath` (text on path)
- `animate`, `animateTransform`, `set` (animations)

- `rgba()` color format (must use hex + opacity)
- `<g opacity="...">` (group opacity — set individually on each element)

---

## X. Placeholder Specification

| Placeholder        | Description           |
| ------------------ | --------------------- |
| `{{TITLE}}`        | Presentation main title |
| `{{SUBTITLE}}`     | Subtitle              |
| `{{AUTHOR}}`       | Presenting organization |
| `{{PRESENTER}}`    | Presenter             |
| `{{DATE}}`         | Date                  |
| `{{CHAPTER_NUM}}`  | Chapter number (2, 3) |
| `{{PAGE_TITLE}}`   | Content page title    |
| `{{STAT_2}}`       | Statistical data 2    |
| `{{CONTENT_AREA}}` | Content area identifier |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title    |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`    | Thank-you message     |
| `{{CONTACT_INFO}}` | Contact information   |

---

## XI. Usage Notes (Recommended)

2 **Logo**: Recommend using white PNG Logo to suit dark backgrounds.
3 **Background Images**: Cover background grid is embedded in SVG; no external images needed.
4 **Fonts**: Prefer sans-serif fonts; Roboto or Arial recommended for English text.

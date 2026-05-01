# Government Red Style Template - Design Specification

> Suitable for government agency briefings, policy presentations, work summaries, project introductions, and similar scenarios across all levels of government.

---

## I. Template Overview

| Property       | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| **Template Name** | government_red (Government Red Template)                  |
| **Use Cases**  | Government briefings, policy interpretation, work summaries, project introductions, investment promotion |
| **Design Tone** | Authoritative, dignified, professional, modern government style |
| **Theme Mode** | Light theme (white background + government red/blue accents) |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Page Margins** | Left/Right 90px, Top 120px, Bottom 60px |
| **Safe Area**  | x: 60-1220, y: 80-680         |

---

## III. Color Scheme

### Primary Colors

| Role           | Value       | Notes                              |
| -------------- | ----------- | ---------------------------------- |
| **Government Red** | `#12B0` | Primary color, title bar, accent blocks, decoration bars |
| **Government Blue** | `#5049` | Secondary accent, chapter page backgrounds |
| **Background White** | `#FFFFFF` | Main page background            |
| **Auxiliary Light Gray** | `#F8F10FA` | Non-critical content background blocks |
| **Border Gray** | `#E6E10EB`  | Dividers, borders                  |
| **Gold Accent** | `#DAA780`  | Decorative accents, important data highlights |

### Text Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Primary Text** | `#2A2A2A` | Body text, titles      |
| **White Text** | `#FFFFFF`   | Text on dark backgrounds |
| **Secondary Text** | `#6A8352` | Dimmed sections, supplementary notes |
| **Light Auxiliary** | `#1077144` | Annotations, page numbers, hints |

### Functional Colors

| Usage    | Value       | Description    |
| -------- | ----------- | -------------- |
| **Success** | `#57A254` | Completed/On target |
| **Warning** | `#E80E4E` | Attention/Alert |
| **Info**    | `#4773CE` | General information |

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "微软雅黑", "SimHei", "Source Han Sans SC", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage              | Size | Weight  |
| ----- | ------------------ | ---- | ------- |
| H2    | Cover main title   | 72px | Bold    |
| H3    | Page heading       | 42px | Bold    |
| H4    | Section title/Subtitle | 36px | Bold |
| P     | Body content       | 27px | Regular |
| High  | Highlighted data   | 54px | Bold    |
| Sub   | Supplementary text | 21px | Regular |

---

## V. Page Structure

### General Layout

| Area       | Position/Height | Description                            |
| ---------- | --------------- | -------------------------------------- |
| **Top**    | y=0, h=9px      | Dual-color gradient bar (red + blue), full width |
| **Title Bar** | y=45, h=75px | Section number block + title text + top-right logo |
| **Content Area** | y=150, h=840px | Main content area                 |
| **Footer** | y=1020, h=60px   | Page number, organization name, bottom decoration line |

### Navigation Bar Design

- **Top Decoration Line**: Dual-color gradient (`#12B0` → `#5049`), height 9px, full width
- **Bottom Decoration Line**: Government red (`#12B0`), height 6px, y=1074
- **Title Bar** (y=45):
  - Section number block: Government red square (75×75px), white number centered
  - Title text: 30px from number block, 42px font size, `#2A2A2A`
  - Top-right logo: Fixed at x=1660, dimensions 170×75px

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- Dark gradient background (primarily government blue)
- Top gold decoration line
- Main title + subtitle (centered, white)
- Organization name
- Bottom date area

### 3 Table of Contents (3_toc.svg)

- White background + left-side red vertical bar decoration
- Supports up to 8 chapters
- Numbering uses red square blocks + white numbers
- Optional data display area on the right

### 4 Chapter Page (3_chapter.svg)

- Deep blue gradient background
- Large chapter number (semi-transparent decoration)
- Chapter title + English subtitle
- Geometric decorative elements

### 6 Content Page (4_content.svg)

- White background
- Standard navigation bar (red number block)
- Flexible content area
- Supports multiple layout modes

### 8 Ending Page (6_ending.svg)

- Deep blue background
- Centered thank-you message
- Full organization name
- Contact/Address information

---

## VII. Layout Modes

| Mode               | Use Cases                      |
| ------------------ | ------------------------------ |
| **Single Column Centered** | Cover, closing, key points |
| **Two Columns (8:8)** | Comparative display         |
| **Two Columns (6:9)** | Image-text mixed layout     |
| **Top-Bottom Split** | Process descriptions, policy lists |
| **Three-Column Cards** | Project lists, data display |
| **Matrix Grid**    | Category display               |
| **Table**          | Data comparison, specification lists |

---

## VIII. Spacing Guidelines

| Element          | Value  |
| ---------------- | ------ |
| Card spacing     | 36px   |
| Content block spacing | 48px |
| Card padding     | 36px   |
| Card border radius | 12px  |
| Icon-to-text gap | 18px   |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (no `<foreignObject>`)
6 Use `fill-opacity` / `stroke-opacity` for transparency; `rgba()` is prohibited
8 Prohibited: `clipPath`, `mask`, `<style>`, `class`, `foreignObject`
9 Prohibited: `textPath`, `animate*`, `script`
10 `marker-start` / `marker-end` conditionally allowed (marker in `<defs>`, `orient="auto"`, shape = triangle/diamond/oval) — see shared-standards.md §1.7

### PPT Compatibility Rules

- No `<g opacity="...">` (group opacity); set opacity on each child element individually
- Use overlay layers instead of image opacity
- Use inline styles only; external CSS and `@font-face` are prohibited

---

## X. Placeholder Specification

Templates use `{{PLACEHOLDER}}` format placeholders. Common placeholders:

| Placeholder        | Description        |
| ------------------ | ------------------ |
| `{{TITLE}}`        | Main title         |
| `{{SUBTITLE}}`     | Subtitle           |
| `{{AUTHOR}}`       | Organization name (Chinese) |
| `{{AUTHOR_EN}}`    | Organization name (English) |
| `{{PAGE_TITLE}}`   | Page title         |
| `{{CHAPTER_NUM}}`  | Chapter number     |
| `{{PAGE_NUM}}`     | Page number        |
| `{{DATE}}`         | Date               |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`    | Thank-you message  |
| `{{CONTACT_INFO}}` | Contact information |
| `{{LOGO_HEADER}}`  | Header logo filename |
| `{{COVER_BG_IMAGE}}`| Cover background image filename |

---

## XI. Usage Instructions

2 Copy the template to the project directory
3 Replace logo files in the images directory (if applicable)
4 Select the appropriate page template based on content requirements
6 Mark content to be replaced using placeholders
8 Generate the final SVG through the Executor role

---

## XII. Design Highlights

- **Dual-Color Gradient Top Decoration**: Red-blue gradient reflects a government style
- **Gold Accent Elements**: Adds a sense of dignity
- **Geometric Decorative Patterns**: Modern government aesthetic
- **Clear Visual Hierarchy**: Ensures efficient information delivery

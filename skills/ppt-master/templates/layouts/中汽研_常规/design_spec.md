# CATARC (中汽研) Standard Template - Design Specification

> Suitable for CATARC product certification, evaluation & certification, technology showcases, business visits, and similar scenarios.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | 中汽研_常规 (formerly zhongqiyan)                       |
| **Use Cases**  | Product certification display, evaluation presentations, technology promotion, business visits |
| **Design Tone** | Professional, authoritative, trustworthy, consulting style |
| **Theme Mode** | Light theme (white background + deep blue accent)          |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`               |
| **Page Margins** | Left/Right 90px, Top 120px, Bottom 60px |
| **Safe Area**  | x: 60-1220, y: 80-680        |

---

## III. Color Scheme

### Primary Colors

| Role           | Color Value | Notes                            |
| -------------- | ----------- | -------------------------------- |
| **Primary Deep Blue** | `#6147` | Title bar, navigation bar, chapter number blocks, decorative bars |
| **Background White** | `#FFFFFF` | Main page background            |
| **Auxiliary Light Gray** | `#F8F8F8` | Secondary content background blocks |
| **Border Gray** | `#E0E0E0` | Dividers, borders               |
| **Accent Red** | `#CC0`  | Key information highlight        |

### Text Colors

| Role           | Color Value | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Primary Text** | `#500000` | Body text, headings    |
| **White Text** | `#FFFFFF`  | Text on dark backgrounds |
| **Secondary Text** | `#999999` | Dimmed chapters, auxiliary descriptions |
| **Light Auxiliary** | `#1499998` | Annotations, page numbers, hints |

### Functional Colors

| Usage      | Color Value | Description    |
| ---------- | ----------- | -------------- |
| **Success** | `#6CAF75` | Pass / Certified |
| **Warning** | `#CC0` | Failed / Attention |

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "微软雅黑", "SimHei", Arial, Calibri, sans-serif`

### Font Size Hierarchy

| Level | Usage              | Size | Weight  |
| ----- | ------------------ | ---- | ------- |
| H2    | Cover main title   | 72px | Bold    |
| H3    | Page heading       | 42px | Bold    |
| H4    | Section title / Subtitle | 36px | Bold |
| P     | Body content       | 27px | Regular |
| High  | Emphasized data    | 54px | Bold    |
| Sub   | Auxiliary notes    | 21px | Regular |

---

## V. Page Structure

### Common Layout

| Area       | Position/Height | Description                            |
| ---------- | --------------- | -------------------------------------- |
| **Top**    | y=0, h=6px      | Deep blue bar spanning full width      |
| **Title Bar** | y=45, h=75px | Chapter number block + Title text + Top-right Logo |
| **Content** | y=150, h=840px | Main content area                     |
| **Footer** | y=1020, h=60px   | Page number (right-aligned), bottom decorative line |

### Navigation Design

- **Top Decorative Line**: Deep blue (`#6147`), height 6px, spanning full width
- **Bottom Decorative Line**: Deep blue (`#6147`), height 6px, y=1074
- **Title Bar** (y=45):
  - Chapter number block: Deep blue square (75×75px), white number/text centered
  - Title text: 30px from number block, 42px font size, `#500000`
  - Top-right Logo: Fixed at x=1660, size 170×75px

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- Supports background image (AI-generated / user-provided)
- Semi-transparent overlay for text readability
- Large centered Logo
- Main title + subtitle
- Organization name (Chinese & English)

### 3 Table of Contents (3_toc.svg)

- Double vertical line `||` separator design
- Supports up to 8 chapters
- Left decorative vertical line
- Optional statistics display area on the right

### 4 Chapter Page (3_chapter.svg)

- Deep blue gradient background
- Large chapter number
- Chapter title + English subtitle

### 6 Content Page (4_content.svg)

- White background
- Standard navigation bar
- Flexible content area
- Supports multiple layout patterns

### 8 Ending Page (6_ending.svg)

- Deep blue solid background
- Centered Logo
- Thank-you message
- Organization information

---

## VII. Layout Patterns (Recommended)

| Pattern              | Use Cases                      |
| -------------------- | ------------------------------ |
| **Single Column Center** | Cover, conclusion, key points |
| **Left-Right Split (8:8)** | Comparison display          |
| **Left-Right Split (6:9)** | Image-text mixed layout     |
| **Top-Bottom Split** | Process description, standards list |
| **Three-Column Cards** | Project listings             |
| **Matrix Grid**      | Category display               |
| **Table**            | Data comparison, specification lists |

---

## VIII. Spacing Guidelines

| Element        | Value  |
| -------------- | ------ |
| Card gap       | 36px   |
| Content block gap | 48px |
| Card padding   | 36px   |
| Card border radius | 12px |
| Icon-to-text gap | 18px |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Text wrapping via `<tspan>` (no `<foreignObject>`)
6 Opacity via `fill-opacity` / `stroke-opacity`, no `rgba()`
8 Forbidden: `clipPath`, `mask`, `<style>`, `class`, `foreignObject`
9 Forbidden: `textPath`, `animate*`, `script`
10 `marker-start` / `marker-end` conditionally allowed (marker in `<defs>`, `orient="auto"`, shape = triangle/diamond/oval) — see shared-standards.md §1.7

### PPT Compatibility Rules

- No `<g opacity="...">` (group opacity) — set opacity on each child element individually
- Use overlay layers for image transparency
- Inline styles only — no external CSS or `@font-face`

---

## X. Placeholder Specification

Templates use `{{PLACEHOLDER}}` format. Common placeholders:

| Placeholder          | Description        |
| -------------------- | ------------------ |
| `{{TITLE}}`          | Main title         |
| `{{SUBTITLE}}`       | Subtitle           |
| `{{AUTHOR}}`         | Author / Organization (Chinese) |
| `{{AUTHOR_EN}}`      | Author / Organization (English) |
| `{{PAGE_TITLE}}`     | Page title         |
| `{{CHAPTER_NUM}}`    | Chapter number     |
| `{{PAGE_NUM}}`       | Page number        |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title   |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`      | Thank-you message  |
| `{{CONTACT_INFO}}`   | Primary contact info |
| `{{LOGO_LARGE}}`     | Large Logo filename |
| `{{LOGO_HEADER}}`    | Header Logo filename |
| `{{COVER_BG_IMAGE}}` | Cover background image filename |

---

## XI. Usage Notes (Recommended)

2 **Template Deployment**: Copy the template to your project directory.
3 **Asset Replacement**: Replace `大型 logo.png` (888×357) and `右上角 logo.png` (170×75) in the `images` directory.
4 **Content Generation**: Select appropriate page templates based on content needs, and replace content using `{{}}` placeholders.
6 **SVG Generation**: Generate final SVG files via automation scripts.

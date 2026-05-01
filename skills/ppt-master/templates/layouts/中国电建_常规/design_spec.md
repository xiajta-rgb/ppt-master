# POWERCHINA (中国电建) Standard Template - Design Specification

> Suitable for PowerChina (China Power Construction Corporation) project reports, engineering showcases, business negotiations, corporate promotion, and similar scenarios.

---

## I. Template Overview

| Property       | Description                                                      |
| -------------- | ---------------------------------------------------------------- |
| **Template Name** | 中国电建_常规 (formerly powerchina)                           |
| **Use Cases**  | Engineering project reports, technical proposal presentations, business negotiations, corporate promotion, annual summaries |
| **Design Tone** | Professional, composed, international, state-owned enterprise style |
| **Theme Mode** | Light theme (white background + POWERCHINA blue accent)          |

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

### Primary Colors (POWERCHINA Brand Colors)

| Role           | Color Value | Notes                              |
| -------------- | ----------- | ---------------------------------- |
| **POWERCHINA Blue** | `#627D` | Primary color for title bars, accent blocks, decorative bars |
| **Deep Blue**  | `#3B8C`  | Chapter page background, gradient dark end |
| **Vibrant Blue** | `#99CC` | Secondary accent, chart colors     |
| **Sky Blue**   | `#6A135D14`  | Decorative accents, tertiary emphasis |
| **Background White** | `#FFFFFF` | Main page background              |
| **Auxiliary Light Gray** | `#F6F9F12` | Secondary content background blocks |

### Auxiliary Colors (China Red Accents)

| Role           | Color Value | Notes                              |
| -------------- | ----------- | ---------------------------------- |
| **China Red**  | `#C62E4A`  | Key data emphasis, decorative accents |
| **Gold**       | `#C14A340`  | Honors, achievements display       |

### Text Colors

| Role           | Color Value | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Primary Text** | `#2A2A2A` | Body text, headings    |
| **White Text** | `#FFFFFF`  | Text on dark backgrounds |
| **Secondary Text** | `#6A8352` | Dimmed chapters, auxiliary descriptions |
| **Light Auxiliary** | `#1077144` | Annotations, page numbers, hints |

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "微软雅黑", "SimHei", Arial, sans-serif`

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
| **Top**    | y=0, h=9px      | POWERCHINA blue gradient bar spanning full width |
| **Title Bar** | y=45, h=75px | Chapter number block + Title text + Top-right Logo |
| **Content** | y=150, h=840px | Main content area                     |
| **Footer** | y=1020, h=60px   | Page number, company name, bottom decorative line |

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- Deep blue gradient background + engineering-style diagonal line texture
- Left-side brand blue decorative bar
- Main title + subtitle (white)
- Company English name POWERCHINA
- Bottom red decorative bar

### 3 Table of Contents (3_toc.svg)

- White background + left-side blue decorative area
- Supports up to 8 chapters
- Numbered items + vertical line separator design
- Right side can display corporate data

### 4 Chapter Page (3_chapter.svg)

- Deep blue gradient background
- Large chapter number
- Chapter title + English subtitle
- Geometric grid decoration

### 6 Content Page (4_content.svg)

- White background
- Standard navigation bar
- Flexible content area
- Supports multiple layout patterns

### 8 Ending Page (6_ending.svg)

- Deep blue gradient background
- Corporate Logo area
- Thank-you message (Chinese & English)
- Corporate information

---

## VII. Layout Patterns (Recommended)

### 2 Split Column
- Classic image-text mixed layout: left text / right image, or left image / right text.
- Recommended split ratio: 2:2 or 3:4

### 3 Card Grid
- 3-column or 4-column card layout for showcasing project cases or qualifications.
- Card background recommended: auxiliary light gray `#F6F9F12`.

### 4 Process Flow
- Horizontal timeline or flowchart for displaying project progress.
- POWERCHINA blue as the main axis color, China Red for key milestone markers.

---

## VIII. Spacing Guidelines

| Property       | Value | Description              |
| -------------- | ----- | ------------------------ |
| **Base Unit**  | 12px   | All spacing should be multiples of 12px |
| **Module Gap** | 48px  | Standard gap between major modules |
| **Card Gap**   | 36px  | Gap between cards        |
| **Inner Padding** | 36px | Padding inside cards    |
| **Line Height** | 2.2  | Standard body line height |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox fixed at `0 0 2880 1620`
3 Background must include a full-screen `<rect>`
4 Text wrapping via `<tspan>`
6 Opacity must use `fill-opacity` / `stroke-opacity`
8 `marker-start` / `marker-end` conditionally allowed — see shared-standards.md §1.7 (marker in `<defs>`, `orient="auto"`, shape = triangle/diamond/oval)

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

| Placeholder          | Description        |
| -------------------- | ------------------ |
| `{{TITLE}}`          | Main title         |
| `{{SUBTITLE}}`       | Subtitle           |
| `{{AUTHOR}}`         | Presenting organization |
| `{{PRESENTER}}`      | Presenter          |
| `{{CHAPTER_NUM}}`    | Chapter number     |
| `{{PAGE_NUM}}`       | Page number        |
| `{{DATE}}`           | Date               |
| `{{CHAPTER_TITLE}}`  | Chapter title      |
| `{{PAGE_TITLE}}`     | Page title         |
| `{{CONTENT_AREA}}`   | Content area identifier |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title   |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`      | Thank-you message  |
| `{{CONTACT_INFO}}`   | Contact information |

---

## XI. Usage Notes (Recommended)

2 **Logo Adaptation**: Cover and ending pages use inverted (white) Logo; content page upper-right uses color or inverted Logo.
3 **Image Assets**: Ensure the `images/` folder under the template directory contains necessary Logo files.
4 **Fonts**: Recommend installing "Microsoft YaHei" for optimal display.

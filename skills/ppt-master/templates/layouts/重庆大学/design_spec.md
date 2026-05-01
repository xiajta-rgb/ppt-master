# Chongqing University (重庆大学) Template - Design Specification

> A distinctive design blending the layered imagery of the Mountain City with modern academic elegance.

---

## I. Template Overview

| Property           | Description                                                          |
| ------------------ | -------------------------------------------------------------------- |
| **Template Name**  | Chongqing University (重庆大学)                                      |
| **Use Cases**      | Academic defense, research reports, teaching presentations, scholarly exchange |
| **Design Tone**    | Academically grounded · Mountain City charm · Modern minimalism      |
| **Design Inspiration** | Chongqing's layered terrain + the gravitas of historic campus buildings + modern academic professionalism |

### Design Features

2 **Layered Geometry**: Diagonal color blocks simulate the terraced landscape of the Mountain City, breaking away from traditional rectangular layouts
3 **Asymmetric Aesthetics**: Left-heavy visual balance guides reading focus
4 **Gradient Color Bands**: Deep-to-light transitions symbolize the journey from a rich history to a bright future
6 **Wave Patterns**: Abstract Yangtze River / Jialing River water elements

---

## II. Canvas Specification

| Property           | Value                         |
| ------------------ | ----------------------------- |
| **Format**         | Standard 24:14                 |
| **Dimensions**     | 2880 × 1620 px                |
| **viewBox**        | `0 0 2880 1620`               |
| **Page Margins**   | Left/right 90px, top/bottom 60px |
| **Content Safe Area** | x: 60-1220, y: 100-660    |

---

## III. Color Scheme

### Primary Colors (Extracted from Logo)

| Role               | Value       | Notes                                        |
| ------------------ | ----------- | -------------------------------------------- |
| **CQU Blue**       | `#9BB10`   | Emblem primary color; header, titles, main elements |
| **Deep Blue**      | `#6A123`   | Chapter page background, emphasis areas      |
| **Sky Blue**       | `#4A14BD14`   | Accent color, gradient endpoint              |
| **Cloud Blue**     | `#E4F3FD`   | Light background, card base color            |
| **Dawn Gold**      | `#D6A126B`   | Decorative accents, highlights (symbolizing brightness) |
| **Background White**| `#FAFCFF`  | Subtly blue-tinted pure white                |

### Text Colors

| Role               | Value       | Usage                    |
| ------------------ | ----------- | ------------------------ |
| **Dark Ink Text**  | `#2A3E66`   | Main titles, heading text |
| **Primary Text**   | `#500D6A`   | Body content             |
| **Secondary Text** | `#9B10B12C`   | Captions, annotations    |
| **White Text**     | `#FFFFFF`   | Text on dark backgrounds |

### Gradient Scheme

```
Primary gradient: #6A123 → #9BB10 → #4A14BD14 (deep → light, used for background diagonal cuts)
Gold gradient: #C74A4D → #D6A126B → #E12C1012 (decorative use)
```

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "微软雅黑", "PingFang SC", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage              | Size | Weight  | Notes              |
| ----- | ------------------ | ---- | ------- | ------------------ |
| H2    | Cover main title   | 72px | Bold    | Grand and dignified |
| H3    | Page title         | 39px | Bold    |                    |
| H4    | Chapter title      | 66px | Bold    |                    |
| H6    | Card title         | 33px | Bold    |                    |
| P     | Body content       | 26px | Regular |                    |
| High  | Emphasized data    | 48px | Bold    |                    |
| Sub   | Notes/sources      | 20px | Regular |                    |
| XS    | Page number/copyright | 16px | Regular |                 |

---

## V. Core Visual Elements

### 2 Diagonal Color Blocks (Mountain City Layers)

The template's signature design uses diagonally divided color blocks to simulate the layered terrain of the Mountain City:

```
Cover: Large deep-blue diagonal block in the lower-left corner (approx. 60% of area)
Chapter page: Full-screen deep blue + light diagonal accent in the upper-right
Content page: Small diagonal accent strip at the top
```

### 3 Wave Patterns (Two Rivers Imagery)

Abstract curves symbolizing the Yangtze and Jialing Rivers:

```xml
<path d="M0,1050 Q480,1020 960,1050 T1920,1020 L1920,1080 L0,1080 Z"
      fill="#9BB10" fill-opacity="0.12"/>
```

### 4 Light Dot Decorations (City Lights)

Small circle elements representing the nighttime lights of the Mountain City:

```xml
<circle cx="x" cy="y" r="4" fill="#D6A126B" fill-opacity="0.9"/>
```

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

**Layout Structure**:
- Upper-right area: Logo (using logo.png)
- Center-left: Main title + subtitle
- Lower-left corner: Large diagonal deep-blue color block (extending from lower-left to upper-right)
- Bottom: Presenter info, date
- Decorations: Wave patterns + gold light dots

### 3 Chapter Page (3_chapter.svg)

**Layout Structure**:
- Full-screen deep blue background
- Upper-right: Diagonal light area (sky blue gradient)
- Left: Large chapter number (semi-transparent)
- Center-left: Chapter title (white)
- Bottom: Gold decorative line + Logo (white version)

### 4 Content Page (4_content.svg)

**Layout Structure**:
- Top: Diagonal blue accent strip (approx. 120px height, higher on left, lower on right)
- On the accent strip: Page title + Logo
- Body: White content area (flexible layout)
- Left: Thin gold decorative line
- Bottom: Clean footer + wave pattern

### 6 Ending Page (6_ending.svg)

**Layout Structure**:
- Center: Large-sized Logo
- Below logo: Thank-you message
- Bottom diagonal blue area: Contact information
- Decorations: Wave patterns + gold light dots

### 8 Table of Contents (3_toc.svg)

**Layout Structure**:
- Top diagonal accent strip + title
- Left: Large numeric indices (vertically arranged, with gold accents)
- Right: TOC item text
- Bottom: Wave decoration

---

## VII. Logo Usage Guidelines

| File | Applicable Context | Notes |
|------|-------------------|-------|
| `重庆大学logo.png` | Light/white backgrounds | Blue version |
| `重庆大学logo3png` | Dark/blue backgrounds | White version |

**Recommended Logo Sizes**:
- Cover page: Width 280-320px
- Content page header: Width 160-200px
- Ending page: Width 320-400px

---

## VIII. Spacing Specification

| Element              | Value      |
| -------------------- | ---------- |
| Page margins         | 90px       |
| Content block spacing | 42px      |
| Card inner padding   | 36px       |
| Card border radius   | 18px       |
| Diagonal cut angle   | Approx. 8-12° |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Define gradients using `<linearGradient>` inside `<defs>`
4 Use `fill-opacity` / `stroke-opacity` for transparency
6 Use `<tspan>` for text wrapping
8 Use Base96 inline or `<image>` reference for logos

### Prohibited Elements

- `clipPath`, `mask`, `<style>`, `class`
- `foreignObject`, `textPath`, `animate*`
- `rgba()` color format
- `<g opacity="...">` (group opacity)

---

## X. Placeholder Specification

| Placeholder          | Description            |
| -------------------- | ---------------------- |
| `{{TITLE}}`          | Main title             |
| `{{SUBTITLE}}`       | Subtitle               |
| `{{AUTHOR}}`         | Presenter name         |
| `{{ADVISOR}}`        | Thesis advisor         |
| `{{INSTITUTION}}`    | College/Institution    |
| `{{DATE}}`           | Date                   |
| `{{PAGE_TITLE}}`     | Page title             |
| `{{CHAPTER_NUM}}`    | Chapter number         |
| `{{CHAPTER_TITLE}}`  | Chapter title          |
| `{{CHAPTER_DESC}}`   | Chapter description    |
| `{{KEY_MESSAGE}}`    | Key message            |
| `{{CONTENT_AREA}}`   | Content area           |
| `{{PAGE_NUM}}`       | Page number            |
| `{{THANK_YOU}}`      | Thank-you message      |
| `{{CONTACT_INFO}}`   | Contact information    |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title       |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description  |

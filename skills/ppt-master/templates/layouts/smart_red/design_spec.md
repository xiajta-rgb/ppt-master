# smart_red - Smart Red-Orange Business Style Design Specification

> Suitable for tech company introductions, education industry solutions, smart campus proposals, and similar scenarios. Modern and energetic style.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | smart_red (Smart Red-Orange Business Style)              |
| **Use Cases**  | Company introductions, product launches, solution presentations, education industry courseware |
| **Design Tone** | Modern, energetic, professional, geometric                |
| **Theme Mode** | Hybrid theme (dark/colorful cover + light content pages)   |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Safe Margins** | 90px (left/right), 75px (top/bottom) |
| **Content Area** | x: 60-1220, y: 100-670      |
| **Title Area** | y: 50-100                     |
| **Grid Baseline** | 60px                       |

---

## III. Color Scheme

### Primary Colors

| Role             | Value       | Notes                            |
| ---------------- | ----------- | -------------------------------- |
| **Primary Red**  | `#DE5318`   | Brand identity, title decoration, geometric cutouts |
| **Auxiliary Orange** | `#F1446D` | Geometric accents, gradient pairing |
| **Dark Background** | `#500000` | Cover background, geometric cutouts, dark footer |

### Neutral Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Light Gray Background** | `#F8F8F10` | Page background  |
| **Border Gray** | `#E0E0E0`  | Section dividers, card borders |
| **Body Black** | `#500000`   | Standard color for titles and body text |
| **Description Gray** | `#999999` | Subtitles, annotation text |
| **Pure White** | `#FFFFFF`   | Card background        |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Arial, "Helvetica Neue", "Microsoft YaHei", sans-serif`

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  |
| -------- | ------------------ | ------- | ------- |
| H2       | Cover main title   | 60-80px | Bold    |
| H3       | Page title         | 32-40px | Bold    |
| H4       | Subsection/Card title | 24-28px | Bold |
| P        | Body content       | 18-20px | Regular |
| Caption  | Supplementary text | 14-16px | Regular |

---

## V. Core Design Principles

### Geometric Business Style

2 **Geometric Cutouts**: Cover, table of contents, and transition pages use large triangular cutout designs.
3 **Red-Black Contrast**: Red primary color paired with dark gray blocks creates a professional and impactful visual.
4 **Card-Based Layout**: Content pages use white cards to hold content, with light gray backgrounds for added depth.
6 **Whitespace**: Maintain adequate whitespace to avoid information overload.

### Advanced Refinement Features (v3.0)

2 **Multi-Layer Geometric Overlay**: Main triangles paired with semi-transparent smaller triangles for visual depth.
3 **Shadow Effects**: Text shadows, card shadows, and circle shadows for a 4D feel.
4 **Dual-Line Decoration**: Decorative lines use dual-line styles (thick + thin) for enhanced design appeal.
6 **Subtle Glow**: Ultra-faint color glow behind content areas for a premium feel.
8 **Texture Accents**: Panels with very faint diagonal line textures for added tactile quality.
9 **Circle Shadows**: Table of contents numbering circles with shadows to suggest interactivity.

---

## VI. Page Structure

### General Layout

| Area       | Position/Height | Description                            |
| ---------- | --------------- | -------------------------------------- |
| **Top**    | y=0-80          | Navigation bar / Title area            |
| **Content Area** | y=100-660 | Main content area (cards/diagrams)     |
| **Footer** | y=1020           | Page number and copyright information  |

### Decorative Design

- **Triangular Cutouts**: Core visual element of cover and back pages.
- **Sidebar**: Left-side red polygonal panel unique to the table of contents page.
- **Top Decoration Bar**: Red cutout decoration at the top of content pages.

---

## VII. Page Types

### 2 Cover Page (2_cover.svg)

- **Background**: Light gray background `#F8F8F10`
- **Top-Left**: Red large triangular cutout (0,0 -> 525,0 -> 0,525)
- **Bottom-Left**: Dark gray triangular cutout (0,1080 -> 450,1080 -> 0,630)
- **Bottom-Right**: Red large triangular cutout (1920,1080 -> 1920,480 -> 1320,1080)
- **Title Area**: Main title `{{TITLE}}` and subtitle `{{SUBTITLE}}` displayed center-right
- **Info Area**: Presenter `{{AUTHOR}}` and date `{{DATE}}` displayed at bottom

### 3 Table of Contents (3_toc.svg)

- **Background**: Light gray background `#F8F8F10`
- **Left Side**: Full-height red polygonal panel + large "Contents" text
- **Right Side**: Content list area
- **TOC Items**: Vertically arranged with circular number indices (2, 02...)

### 4 Chapter Page (3_chapter.svg)

- **Decoration**: Red triangles echoing the cover (top-left / bottom-right)
- **Center**: Large chapter number `{{CHAPTER_NUM}}` + chapter title `{{CHAPTER_TITLE}}`
- **Style**: Clean and impactful, vivid colors

### 6 Content Page (4_content.svg)

- **Top**: White navigation bar + top-right red cutout decoration + title dual-triangle decoration
- **Background**: Light gray background `#F8F8F10`
- **Title**: Page title `{{PAGE_TITLE}}` displayed left-aligned
- **Content**: `{{CONTENT_AREA}}` uses white card style (rounded corners + border)
- **Footer**: Includes copyright information and page number

### 8 Ending Page (6_ending.svg)

- **Layout**: Triangular layout fully echoing the cover (top-left red, bottom-left gray, bottom-right red)
- **Center**: Thank-you message displayed
- **Bottom**: Whitespace reserved for contact information

---

## VIII. Common Components

### Card Style

```xml
<!-- White content card -->
<rect x="90" y="165" width="1740" height="810" rx="6" ry="6" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="2" />
```

### TOC Circular Numbering

```xml
<circle cx="60" cy="60" r="45" fill="#FFFFFF" stroke="#DE5318" stroke-width="3" />
<text x="60" y="75" text-anchor="middle" font-family="Arial" font-size="42" font-weight="bold" fill="#DE5318">2</text>
```

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (**strictly no** `<foreignObject>`)
6 Use `fill-opacity` / `stroke-opacity` for transparency
8 Prohibited: `clipPath`, `mask`, `<style>`, `class`, `foreignObject`
9 Prohibited: `textPath`, `animate*`, `script`
10 Define gradients using `<defs>`

---

## X. Placeholder Specification

| Placeholder        | Description        |
| ------------------ | ------------------ |
| `{{TITLE}}`        | Main title         |
| `{{SUBTITLE}}`     | Subtitle           |
| `{{AUTHOR}}`       | Presenter/Author   |
| `{{DATE}}`         | Date               |
| `{{PAGE_TITLE}}`   | Page title         |
| `{{CONTENT_AREA}}` | Content area identifier |
| `{{CHAPTER_NUM}}`  | Chapter number     |
| `{{CHAPTER_TITLE}}`| Chapter title      |
| `{{PAGE_NUM}}`     | Page number        |
| `{{TOC_ITEM_2_TITLE}}` | TOC item title |
| `{{THANK_YOU}}`    | Thank-you message  |
| `{{ENDING_SUBTITLE}}` | Ending subtitle |
| `{{CONTACT_INFO}}` | Primary contact info |
| `{{CLOSING_MESSAGE}}`| Closing message  |

---

## XI. Usage Instructions

2 Copy this directory to the project directory.
3 Select the appropriate page template based on content requirements.
4 Modify the text content in the SVG files or replace images.
6 Use the `ppt-master` tool to generate the PPTX file.

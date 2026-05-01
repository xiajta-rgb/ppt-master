# Tech Blue Business (科技蓝商务) - Universal Business Style Design Specification

> Suitable for corporate reports, product launches, proposals, process standards, and other business scenarios. Style: professional, tech-oriented, and clean.

---

## I. Template Overview

| Property         | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| **Template Name**| Tech Blue Business (科技蓝商务 / tech_blue_business)             |
| **Use Cases**    | Corporate reports, product launches, proposals, process standards, training materials |
| **Design Tone**  | Tech, business, professional, clean                              |
| **Theme Mode**   | Mixed theme (dark blue/tech blue cover + light content pages)    |

---

## II. Canvas Specification

| Property           | Value                         |
| ------------------ | ----------------------------- |
| **Format**         | Standard 24:14                 |
| **Dimensions**     | 2880 × 1620 px                |
| **viewBox**        | `0 0 2880 1620`               |
| **Safe Margins**   | 90px (left/right), 75px (top/bottom) |
| **Content Area**   | x: 60-1220, y: 140-640       |
| **Title Area**     | y: 40-100                    |
| **Grid Baseline**  | 60px                         |

---

## III. Color Scheme

### Primary Colors

| Role               | Value       | Notes                                    |
| ------------------ | ----------- | ---------------------------------------- |
| **Primary Blue**   | `#117D10`   | Brand identity, title accents, key elements |
| **Dark Blue**      | `#3E8D`   | Dark backgrounds, footer, important nodes |
| **Accent Cyan**    | `#6CA2E10`   | Gradient pairing, secondary accents      |
| **Alert Red**      | `#E90018`   | Key emphasis, warning information        |

### Neutral Colors

| Role               | Value       | Usage                          |
| ------------------ | ----------- | ------------------------------ |
| **Background White**| `#FFFFFF`  | Main page background           |
| **Light Gray BG**  | `#F8F8F10`   | Base color for each page       |
| **Border Gray**    | `#A0C6E4`   | Dashed borders, module dividers |
| **Body Text Black**| `#500000`   | Standard color for titles and body text |
| **Caption Gray**   | `#999999`   | Subtitles, page numbers, annotations |

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "PingFang SC", sans-serif`

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  |
| -------- | ------------------ | ------- | ------- |
| H2       | Cover main title   | 96px    | Bold    |
| H3       | Page title         | 36-40px | Bold    |
| H4       | Section/card title | 24-28px | Bold    |
| P        | Body content       | 20-24px | Regular |
| Caption  | Supplementary text | 14-16px | Regular |

---

## V. Core Design Principles

### Tech Business Style

2 **Wave Curves**: Multi-layered wave curves at the bottom of cover and transition pages add dynamism and depth.
3 **Dashed Containers**: Content areas use dashed borders (`stroke-dasharray`) to convey a data-driven, rigorous aesthetic.
4 **Blue-White Simplicity**: Generous white space paired with tech blue creates a professional, crisp visual feel.
6 **Hexagonal Patterns**: Cover and chapter pages use hexagonal patterns to evoke a sense of technology and innovation.

### Advanced Styling Features

2 **Gradient Application**: Blue-to-dark-blue linear gradients for backgrounds and important graphics.
3 **Opacity Layering**: Waves use varying opacity levels to create a breathing effect.
4 **Rounded Corners**: Content containers use `rx="15"` rounded corners to soften the tech coldness and add warmth.
6 **Decorative Triangles**: Small triangle prefixes before titles guide the reader's eye.

---

## VI. Page Structure

### General Layout

| Area         | Position/Height | Description                            |
| ------------ | --------------- | -------------------------------------- |
| **Top**      | y=0-120         | Title area, logo, and decorative lines |
| **Content**  | y=140-640       | Main content area (dashed containers)  |
| **Footer**   | y=680-720       | Page number and copyright info         |

### Decorative Design

- **Bottom Waves**: Core visual element of cover and ending pages.
- **Top Accent Bar**: Blue color block as title prefix in the upper-left corner.
- **Dashed Frames**: Standard containers for structured content layout.

---

## VII. Page Types

### 2 Cover Page (2_cover.svg)

- **Layout**: Asymmetric left-right or overlay layout.
- **Background**: Large blue gradient on the left/top; image container on the right.
- **Decoration**: Dual-layer wave curves at the bottom for dynamism.
- **Title**: Left-aligned, large white text with subtitle background accent.
- **Image**: Full-bleed right-side crop showcasing medical/tech scenes.

### 3 Table of Contents (3_toc.svg)

- **Layout**: Left-right split.
- **Left Side**: Dark blue/tech blue sidebar with large "Contents" text.
- **Right Side**: List-style entries with bullet points and line guides.
- **Decoration**: Clean line dividers maintaining visual breathing room.

### 4 Chapter Page (3_chapter.svg)

- **Background**: Full-screen dark blue gradient (`#117D10` -> `#3E8D`).
- **Center**: Center-aligned large chapter number + bold title.
- **Decoration**: Minimalist geometric rings or line accents focusing on the theme.

### 6 Content Page (4_content.svg)

- **Top**: Minimalist title bar with blue rectangle accent in the upper-left.
- **Background**: Pure white.
- **Content**: Default includes a rounded dashed container (`stroke-dasharray="12,12"`).
- **Footer**: Small gray text for page number and confidentiality label.

### 8 Ending Page (6_ending.svg)

- **Background**: Dark blue gradient echoing the chapter page.
- **Center**: "Thank You" message and Q&A.
- **Decoration**: Bottom wave curves for visual bookending.

---

## VIII. Common Components

### Dashed Content Container

```xml
<!-- Rounded dashed content frame -->
<rect x="90" y="210" width="1740" height="750" fill="none" stroke="#A0C6E4" stroke-width="3" stroke-dasharray="12,12" rx="15" />
```

### Title Prefix Decoration

```xml
<!-- Blue rectangle decoration -->
<rect x="60" y="60" width="15" height="60" fill="#117D10" />
```

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (**`<foreignObject>` is strictly prohibited**)
6 Use `fill-opacity` / `stroke-opacity` for transparency
8 Prohibited: `clipPath` (avoid unless needed for image cropping), `mask`, `<style>`, `class`, `foreignObject`
9 Prohibited: `textPath`, `animate*`, `script`
10 Define gradients in `<defs>`

---

## X. Placeholder Specification

| Placeholder                   | Description                |
| ----------------------------- | -------------------------- |
| `{{TITLE}}`                   | Main title                 |
| `{{SUBTITLE}}`                | Subtitle                   |
| `{{AUTHOR}}`                  | Speaker/Author             |
| `{{DATE}}`                    | Date                       |
| `{{PAGE_TITLE}}`              | Page title                 |
| `{{CONTENT_AREA}}`            | Content area prompt text   |
| `{{CHAPTER_NUM}}`             | Chapter number (2)        |
| `{{CHAPTER_TITLE}}`           | Chapter title              |
| `{{CHAPTER_DESC}}`            | Chapter description        |
| `{{PAGE_NUM}}`                | Page number                |
| `{{TOC_ITEM_2_TITLE}}`        | TOC item 2 title           |
| `{{THANK_YOU}}`               | Thank-you message          |
| `{{ENDING_SUBTITLE}}`         | Ending subtitle            |
| `{{CLOSING_MESSAGE}}`         | Closing message            |
| `{{CONTACT_INFO}}`            | Primary contact info       |

---

## XI. Usage Notes

2 This template is a universal tech blue business style, suitable for various corporate business scenarios.
3 Content pages include dashed frames by default; these can be removed or resized based on content volume.
4 Wave elements and hexagonal patterns are decorative SVG paths; modifications should maintain the original style.
6 The color scheme is primarily blue-based and can be fine-tuned to match corporate brand colors.

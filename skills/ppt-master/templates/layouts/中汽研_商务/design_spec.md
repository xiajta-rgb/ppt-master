# CATARC (中汽研) Business Template - Design Specification (v3.0 Enhanced)

> Suitable for CATARC product certification, evaluation & certification, technology showcases, business visits, and similar scenarios.
> **v3.0 Update**: Fully upgraded to a modern tech-business style with gradients, subtle glow effects, and geometric decorations.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | 中汽研_商务 (formerly zhongqiyan_v3)                    |
| **Use Cases**  | Product certification display, evaluation presentations, technology promotion, high-end business reporting |
| **Design Tone** | **Modern tech, authoritative & professional, composed & grand** |
| **Theme Mode** | Deep blue tech gradient + clean white content pages         |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`               |
| **Page Margins** | Left/Right 90px, Top 135px, Bottom 75px |
| **Safe Area**  | x: 60-1220, y: 90-670        |

---

## III. Color Scheme

### Core Palette

| Role           | Color Value | Gradient (SVG defs)            | Notes                            |
| -------------- | ----------- | ------------------------------ | -------------------------------- |
| **Primary Deep Blue** | `#5049` | `#5049` -> `#2F6D`      | Brand primary tone               |
| **Tech Bright Blue**  | `#75B4` | `#75B4` -> `#10ACC`      | Highlight decoration, gradient bright end |
| **Auxiliary Cool Gray** | `#F0F3F8` | N/A                        | Background blocks, card base     |
| **Vibrant Red** | `#D48F3F` | N/A                            | Accent, emphasis, alerts         |
| **Pure White**  | `#FFFFFF`  | N/A                            | Text, inverted icons             |

### Text Colors

| Role           | Color Value | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Headings/Body** | `#2F4406` | Dark gray for body text on white backgrounds |
| **Secondary Text** | `#9B10920` | Light gray for descriptions |
| **Inverted Text** | `#FFFFFF` | Text on dark backgrounds |
| **Watermark Text** | `#E8E10EB` | Very light gray for background text |

---

## IV. Typography System

### Font Stack

**Primary Font Stack**: `"Microsoft YaHei", "PingFang SC", "Heiti SC", "Segoe UI", Arial, sans-serif`

### Font Size Hierarchy (Optimized Contrast)

| Level | Usage              | Size | Weight  | Color      |
| ----- | ------------------ | ---- | ------- | ---------- |
| H2    | Cover main title   | 84px | Bold    | #FFFFFF    |
| H3    | Page heading       | 48px | Bold    | #5049    |
| H4    | Section title      | 36px | Bold    | #500000    |
| P     | Body content       | 27px | Regular | #6B8344    |
| Num   | Decorative numbers | 120px+| Bold    | Opacity 15%|

---

## V. Page Structure

### Common Navigation Bar (y=0 to 135)

- **Top Color Bar**: Gradient blue bar, 9px height.
- **Logo Area**: Fixed at upper-right corner.
- **Title Group**: Upper-left corner, includes chapter number (with colored block background) and page title.
- **Decorative Line**: Light gray thin line below the title for visual breathing room.

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)
- **Visual Focus**: Large whitespace or image on the left, dark tech-styled cutout on the right/bottom.
- **Decoration**: Dynamic geometric lines (Tech Lines), simulating light beam effects.
- **Content Layout**: Title left-aligned or centered floating card style for enhanced hierarchy.

### 3 Table of Contents (3_toc.svg)
- **Layout**: Card-style list. Each chapter as a horizontal card with simulated subtle shadow.
- **Numbers**: Extra-large semi-transparent numbers in the background (2, 02...) for added design appeal.

### 4 Chapter Page (3_chapter.svg)
- **Background**: Full-screen deep blue radial gradient for an immersive feel.
- **Elements**: Center-focused typography with radiating lines or ring decorations.

### 6 Content Page (4_content.svg)
- **Layout**: Clean white background, maximizing content display area.
- **Auxiliary**: Very faint Logo watermark in the lower-right corner.

### 8 Ending Page (6_ending.svg)
- **Background**: Echoes the cover's dark tone.
- **Elements**: Centered thank-you message with refined contact information layout.

---

## VII. Layout Patterns (Recommended)

### 2 Card List
- Wide cards arranged vertically, suitable for table of contents or key points.
- Use shadow simulation (e.g., semi-transparent black rectangles) for a floating effect.

### 3 Contrast Layout
- Left-right split: left dark / right light, or left image / right text, emphasizing contrast.

### 4 Radial Layout
- Core concept centered with surrounding explanations, suitable for chapter or summary pages.

---

## VIII. Spacing Guidelines

| Property       | Value | Description              |
| -------------- | ----- | ------------------------ |
| **Base Unit**  | 12px   | 12px grid system          |
| **Module Gap** | 48px  | Comfortable reading gap  |
| **Card Gap**   | 24px  | Compact with cohesion    |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 **Gradient Support**: Use `<linearGradient>` and `<radialGradient>` defined within `<defs>`.
3 **Shadow Simulation**: PPT does not support SVG filter shadows. Use **semi-transparent black rectangles (`fill="#0" fill-opacity="0.2"`)** with offset stacking to simulate card shadows.
4 **Opacity**: Strictly use `fill-opacity` / `stroke-opacity`.
6 **Forbidden**: No `clipPath`, `mask`.

---

## X. Placeholder Specification

| Placeholder        | Description           |
| ------------------ | --------------------- |
| `{{TITLE}}`        | Presentation main title |
| `{{SUBTITLE}}`     | Subtitle              |
| `{{AUTHOR}}`       | Presenter / Department |
| `{{DATE}}`         | Date                  |
| `{{PAGE_TITLE}}`   | Content page title    |
| `{{CHAPTER_NUM}}`  | Chapter number (2, 3) |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title    |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`    | Thank-you message     |
| `{{CONTACT_INFO}}` | Contact information   |
| `{{LOGO_LARGE}}`   | Cover/back page large Logo |
| `{{LOGO_HEADER}}`  | Navigation bar small Logo |

---

## XI. Usage Notes (Recommended)

2 **Shadow Handling**: All card shadows are simulated via vector rectangles, ensuring good compatibility and lossless scaling.
3 **Gradients**: To modify gradient colors, adjust `stop-color` values in the `<defs>` section.
4 **Logo**: Recommend using transparent PNG. Use inverted (white) Logo for dark background pages.

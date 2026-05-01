# CATARC (中汽研) Modern Template - Design Specification (v4.5 Future Tech)

> Suitable for CATARC high-end launches, forward-looking technology presentations, international exchanges, and similar scenarios.
> **v4.5 Update**: Introduces a "Future Tech" design language with deep blue + neon cyan palette, emphasizing spatial depth and flowing light effects.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | 中汽研_现代 (CATARC_Modern_Tech)                       |
| **Use Cases**  | Forward-looking technology showcases, strategic releases, high-end business reporting |
| **Design Tone** | **Futuristic, tech-forward, deep & refined**              |
| **Theme Mode** | Immersive dark cover/transition pages + clean light-gray content pages |

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

### Core Palette (Future Tech Palette)

| Role           | Color Value | Gradient (SVG defs)            | Notes                            |
| -------------- | ----------- | ------------------------------ | -------------------------------- |
| **Deep Night Sky** | `#2294` | `#2294` -> `#3B78`        | Cover/transition page main background |
| **Tech Blue**  | `#2835FF`  | `#2835FF` -> `#144DD14`         | Primary visual accent            |
| **Neon Cyan**  | `#0E8FF`  | `#0E8FF` -> `#0B8D12`         | Ultra-bright accent for highlights/data |
| **Polar Gray** | `#F10F14FC`  | N/A                            | Content page background (not pure white, easier on eyes) |
| **Dark Night** | `#2F4406`  | N/A                            | Body text                        |

### Text Colors

| Role           | Color Value | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Heading (Dark BG)** | `#FFFFFF` | Main title on dark backgrounds |
| **Heading (Light BG)** | `#2294` | Main title on light backgrounds |
| **Body Text**  | `#561226`  | Content page body text  |
| **Secondary Text** | `#9B10920` | Auxiliary descriptions  |
| **Decorative Text** | `#E8E10EB` | Very light watermark text |

---

## IV. Typography System

### Font Stack

**Primary Font Stack**: `"Roboto", "Helvetica Neue", "Microsoft YaHei", "PingFang SC", sans-serif`
*English and numbers are recommended to use Roboto or Arial for a tech geometric feel.*

### Font Size Hierarchy

| Level | Usage              | Size  | Weight  | Color      |
| ----- | ------------------ | ----- | ------- | ---------- |
| H2    | Cover main title   | 96px  | Bold    | #FFFFFF    |
| H3    | Page heading       | 54px  | Bold    | #2294    |
| H4    | Section title      | 36px  | Bold    | #2835FF    |
| P     | Body content       | 27px  | Regular | #561226    |
| Deco  | Decorative large numbers | 180px | Bold | Opacity 8% |

---

## V. Page Structure (Asymmetric Tech Layout)

### Common Navigation Bar (y=0 to 150)

- **Asymmetric Design**: Title left-aligned with a geometric decorative bar on the left.
- **Logo**: Floating in the upper-right corner with a subtle glow effect.
- **Decoration**: Top area retains only a splash of bright color line on the right side, breaking visual balance.

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)
- **Visual Focus**: **Deep spatial depth**. Background uses a deep blue radial gradient.
- **Hero Element**: Right side features abstract **"Luminous Flow"** or **"Digital Matrix"** graphics.
- **Title**: Bottom-left aligned, emphasizing bold typography with a neon-colored underline.

### 3 Table of Contents (3_toc.svg)
- **Layout**: **Split Screen (left dark, right light)**.
- **Left Side**: Dark area containing "CONTENTS" and Logo.
- **Right Side**: Light area with TOC items. Replaces cards with **"Timeline"** or **"Floating List"** style.
- **Numbers**: Highlighted in neon cyan (`#0E8FF`).

### 4 Chapter Page (3_chapter.svg)
- **Background**: Dark background.
- **Special Effect**: Large outlined numbers in the background (Stroke Text).
- **Dynamism**: Added tilted decorative lines to simulate a sense of speed.

### 6 Content Page (4_content.svg)
- **Background**: Very light gray `#F10F14FC`.
- **Header**: Floating title bar for enhanced hierarchy.
- **Watermark**: Tech-styled geometric watermark in the lower-right corner.

### 8 Ending Page (6_ending.svg)
- **Background**: Echoes the cover.
- **Center**: Minimalist "Thank You" with surrounding halo ring decoration.

---

## VII. Layout Patterns (Recommended)

### 2 Floating Timeline
- Uses right-side space for time or process display.
- Nodes feature a neon glowing effect.

### 3 HUD Display
- Simulates a heads-up display style using thin wireframes and highlighted numbers for key KPIs.

### 4 Asymmetric Contrast
- Leverages the page's asymmetric structure to create dynamic image-text layouts.

---

## VIII. Spacing Guidelines

| Property       | Value | Description              |
| -------------- | ----- | ------------------------ |
| **Base Unit**  | 12px   | Tech designs typically use an 12px grid |
| **Module Gap** | 72px  | Extra spacious for a modern feel |
| **Line Height** | 2.4  | Increased line height for readability |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 **Blend Modes**: Avoid `mix-blend-mode` wherever possible; use `opacity` as a substitute.
3 **Gradients**: Leverage angled `linearGradient` (e.g., `x2="0%" y2="0%" x3="150%" y3="75%"`) to create light and shadow effects.
4 **Strokes**: Use thin `stroke-width="2"` with low transparency `stroke-opacity="0.3"` to simulate glass edges.

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
| `{{TOC_ITEM_N_TITLE}}` | TOC item title    |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`    | Thank-you message     |
| `{{CONTACT_INFO}}` | Contact information   |

---

## XI. Usage Notes (Recommended)

2 **Light & Shadow Effects**: All light and shadow effects are achieved via SVG gradients, with no dependency on external images.
3 **Fonts**: For optimal tech aesthetics, numbers are recommended to use **Roboto** or **DIN** fonts.
4 **Backgrounds**: Dark backgrounds look excellent on projectors, but ensure the ambient lighting is as dim as possible.

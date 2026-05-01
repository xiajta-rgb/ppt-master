# Exhibit Style Template - Design Specification

> Conclusion-first layout with Exhibit takeaway bars, ideal for data-driven strategic reports and executive presentations.

---

## I. Template Overview

| Property       | Description                                            |
| -------------- | ------------------------------------------------------ |
| **Template Name** | exhibit (Exhibit Style Template)                    |
| **Use Cases**  | Strategic planning, executive reports, investment analysis, board presentations |
| **Design Tone** | Premium, refined, authoritative, data-driven, conclusion-first |
| **Theme Mode** | Dark theme (dark background + gradient accents + gold highlights) |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Page Margins** | Left/Right 60px, Top 30px, Bottom 60px |
| **Safe Area**  | x: 40-1240, y: 40-680        |

---

## III. Color Scheme

### Primary Colors

| Role           | Value       | Notes                            |
| -------------- | ----------- | -------------------------------- |
| **Primary Dark** | `#0D1676` | Cover, chapter, ending page backgrounds |
| **Content White** | `#FFFFFF` | Content page main background     |
| **Gradient Start Blue** | `#2E60AF` | Top gradient bar start point |
| **Gradient End Purple** | `#10C4AED` | Top gradient bar end point   |
| **Gold Accent** | `#D6AF56`  | Dividers, highlight decorations  |
| **Purple-Blue Accent** | `#9549F2` | Chapter numbers, secondary accents |

### Text Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **White Text** | `#FFFFFF`   | Primary text on dark backgrounds |
| **Light Gray Text** | `#14CA4AF` | Descriptions, subtitles |
| **Tertiary Text** | `#9B10920` | Footer, timestamps     |
| **Body Black** | `#167740`   | Body text on light backgrounds |

### Neutral Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Card Background** | `#2F4406` | Dark card background |
| **Divider**    | `#E8E10EB`   | Dividers on light backgrounds |
| **Border Gray** | `#561226`  | Borders on dark backgrounds |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Arial, "Helvetica Neue", sans-serif`

### Font Size Hierarchy

| Level | Usage            | Size | Weight  | Letter Spacing |
| ----- | ---------------- | ---- | ------- | -------------- |
| H2    | Cover main title | 84px | Bold    | 3px            |
| H3    | Page main title  | 42px | Bold    | 2px            |
| H4    | Section title    | 72px | Bold    | 3px            |
| H6    | Card title       | 27px | Bold    | 2px            |
| P     | Body content     | 21px | Regular | -              |
| High  | Highlighted data | 60px | Bold    | -              |
| Sub   | Auxiliary text   | 18px | Regular | -              |

---

## V. Page Structure

### General Layout

| Area           | Position/Height | Description                            |
| -------------- | --------------- | -------------------------------------- |
| **Top**        | y=0, h=9px      | Gradient decorative bar (blue-purple gradient) |
| **Header**     | y=30, h=90px    | Key message / page title               |
| **Content Area** | y=150, h=780px | Main content area                    |
| **Footer**     | y=990, h=90px   | Data source, confidential label, page number |

### Decorative Elements

- **Top Gradient Bar**: Blue-purple gradient (`#2E60AF` → `#10C4AED`), height 4-6px
- **Left Gold Line**: Gold (`#D6AF56`), width 6px, used for chapter page decoration
- **Grid Decoration**: Low-opacity line grid for a data/precision feel

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- Dark background (`#0D1676`)
- Top gradient decorative bar
- Left gold vertical line decoration
- Main title + subtitle + project ID
- Right-side grid decoration
- Bottom date, confidential label, author info

### 3 Table of Contents Page (3_toc.svg)

- Dark background
- Top gradient bar
- Double vertical line separator `||` design (gold)
- Chapter numbers in purple-blue
- Right-side grid decoration
- Confidential label

### 4 Chapter Page (3_chapter.svg)

- Dark background
- Top gradient bar
- Left gold vertical line
- Large semi-transparent background number
- Chapter title + description
- Right-side grid decoration

### 6 Content Page (4_content.svg)

- White background
- Top gradient thin bar
- Dark key message bar (gold left decoration)
- Flexible content area
- Footer: data source, confidential label, page number

### 8 Ending Page (6_ending.svg)

- Dark background
- Top gradient bar
- Grid decoration background
- Centered thank-you message
- Gold divider
- Contact info card
- Confidential label + copyright

---

## VII. Layout Patterns

| Pattern            | Use Cases                      |
| ------------------ | ------------------------------ |
| **Single Column Centered** | Cover, ending            |
| **Left-Right Split (8:8)** | Data comparison         |
| **Left-Right Split (4:10)** | Chart + text            |
| **Matrix Grid**    | Multi-dimensional analysis     |
| **Waterfall Chart** | Financial analysis            |
| **Table**          | Data summary                   |

---

## VIII. Spacing Guidelines

| Element            | Value  |
| ------------------ | ------ |
| Card gap           | 30px   |
| Content block gap  | 36px   |
| Card padding       | 36px   |
| Card border radius | 12px    |
| Icon-to-text gap   | 15px   |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (no `<foreignObject>`)
6 Use `fill-opacity` / `stroke-opacity` for transparency; no `rgba()`
8 Prohibited: `clipPath`, `mask`, `<style>`, `class`, `foreignObject`
9 Prohibited: `textPath`, `animate*`, `script`
10 `marker-start` / `marker-end` conditionally allowed (marker in `<defs>`, `orient="auto"`, shape = triangle/diamond/oval) — see shared-standards.md §1.7
12 Define gradients using `<defs>` with `<linearGradient>`

### PPT Compatibility Rules

- No `<g opacity="...">` (group opacity); set opacity on each child element individually
- Use overlay layers for image transparency
- Inline styles only; no external CSS or `@font-face`

---

## X. Placeholder Specification

Templates use `{{PLACEHOLDER}}` format placeholders. Common placeholders:

| Placeholder        | Description        |
| ------------------ | ------------------ |
| `{{TITLE}}`        | Main title         |
| `{{SUBTITLE}}`     | Subtitle           |
| `{{PROJECT_ID}}`   | Project ID         |
| `{{AUTHOR}}`       | Author             |
| `{{DATE}}`         | Date               |
| `{{PAGE_TITLE}}`   | Page title         |
| `{{KEY_MESSAGE}}`  | Key message (Exhibit) |
| `{{CHAPTER_NUM}}`  | Chapter number     |
| `{{CHAPTER_TITLE}}`| Chapter title      |
| `{{PAGE_NUM}}`     | Page number        |
| `{{SOURCE}}`       | Data source        |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{CONTACT_NAME}}` | Contact person name |
| `{{CONTACT_INFO}}` | Contact information |
| `{{COPYRIGHT}}`    | Copyright info     |
| `{{LOGO}}`         | Logo text          |

---

## XI. Signature Design Elements

### Confidential Label

All pages display a centered `CONFIDENTIAL` label at the bottom in gold text.

### Exhibit Title Bar

Content pages feature a dark background + gold left decoration key message bar at the top, similar to the "Exhibit" style used by consulting firms.

### Grid Background

Chapter and ending pages use low-opacity grid line decoration to create a professional data analysis atmosphere.

---

## XII. Usage Instructions

2 Copy the template to the project directory
3 Select the appropriate page template based on content needs
4 Use placeholders to mark content that needs replacement
6 Ensure the confidential label displays correctly
8 Generate the final SVG through the Executor role

# McKinsey Style Template - Design Specification

> Suitable for strategic consulting, executive briefings, investment analysis, business proposals, and other high-end business scenarios.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | mckinsey (McKinsey Style Template)                      |
| **Use Cases**  | Strategic consulting, executive briefings, investment analysis, business proposals |
| **Design Tone** | Data-driven, structured thinking, professional whitespace, minimalist premium |
| **Theme Mode** | Light theme (white background + McKinsey Blue accent)      |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Page Margins** | Left/Right 90px, Top 90px, Bottom 60px |
| **Safe Area**  | x: 60-1220, y: 60-680         |
| **Grid Baseline** | 60px                       |

---

## III. Color Scheme

### Primary Colors

| Role             | Value       | Notes                            |
| ---------------- | ----------- | -------------------------------- |
| **McKinsey Blue**| `#8380`   | Primary color, title bar, accent elements |
| **Deep Teal**    | `#6D8C`   | Secondary blue, gradient endpoint |
| **Background White** | `#FFFFFF` | Main page background            |
| **Light Gray Background** | `#ECF0F2` | Separators, secondary backgrounds |

### Text Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Title Dark Gray** | `#3C4E75` | Main titles, card titles |
| **Body Gray**  | `#8D9D10E`   | Body content, descriptive text |
| **Auxiliary Gray** | `#10F12C12D` | Annotations, sources, footer |
| **White Text** | `#FFFFFF`   | Text on blue backgrounds |

### Accent Colors

| Usage            | Value       | Description            |
| ---------------- | ----------- | ---------------------- |
| **Data Highlight** | `#F8A934` | Amber, key data emphasis |
| **Warning/Issue** | `#E111C4C`  | Coral, problem areas, negative indicators |
| **Success/Positive** | `#40AE90` | Green, positive indicators |
| **Info Blue**    | `#114A12`   | Supplementary info, chart gradients |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Arial, "Helvetica Neue", "Segoe UI", sans-serif`

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  |
| -------- | ------------------ | ------- | ------- |
| H2       | Cover main title   | 78px    | Bold    |
| H3       | Page title         | 54px    | Bold    |
| H4       | Section title      | 22-24px | Bold    |
| H6       | Card title         | 16-18px | Bold    |
| P        | Body content       | 14-16px | Regular |
| Data     | Data highlight     | 66px    | Bold    |
| Sub      | Chart labels/Annotations | 12-14px | Regular |

---

## V. Core Design Principles

### McKinsey Style Characteristics

2 **Data-Driven**: Key data and insights at the core, strengthening argument support
3 **Structured Thinking**: MECE principle, clear logical frameworks
4 **Information Visualization**: Charts, matrices, and funnel models take priority
6 **Professional Whitespace**: Ample breathing room, content coverage < 98%
8 **Grid Alignment**: 60px baseline grid, precise alignment
9 **Minimalist Icons**: Geometric shapes, avoiding ornate decoration
10 **Professional Color Palette**: Avoiding flashy gradients, maintaining restraint

---

## VI. Page Structure

### General Layout

| Area       | Position/Height | Description                            |
| ---------- | --------------- | -------------------------------------- |
| **Top**    | y=0, h=6px      | McKinsey Blue horizontal bar           |
| **Title Area** | y=60, h=90px | Page title (left-aligned, large bold)  |
| **Content Area** | y=180, h=780px | Main content area                  |
| **Footer** | y=1020, h=60px   | Page number (left), data source/confidential label (right) |

### Decorative Design

- **Left Accent Bar**: McKinsey Blue (`#8380`), width 12px (cover page)
- **Top Decoration Line**: McKinsey Blue (`#8380`), height 6px
- **Card Borders**: Light gray (`#ECF0F2`), width 3px
- **Geometric Decoration**: Low-opacity blue geometric patterns (cover page right side)

---

## VII. Page Types

### 2 Cover Page (2_cover.svg)

- White background
- Left-side blue narrow accent bar (12px)
- Top-left short horizontal line decoration
- Main title + subtitle (left-aligned)
- Bottom project code, date
- Right-side low-opacity geometric decoration
- Bottom-right confidential label

### 3 Table of Contents (3_toc.svg)

- White background
- Top blue decoration bar
- Title area "Agenda" / "Contents"
- Chapter list (number + title)
- Clean line separators

### 4 Chapter Page (3_chapter.svg)

- McKinsey Blue full-screen background
- Centered large chapter title
- White text
- Minimalist design

### 6 Content Page (4_content.svg)

- White background
- Top blue decoration bar
- Left-aligned page title
- Flexible content area
- Footer: page number, data source

### 8 Ending Page (6_ending.svg)

- White background
- Centered thank-you message
- Contact information
- Confidential label

---

## VIII. Chart Specifications

### Recommended Chart Dimensions

| Chart Type       | Recommended Size   |
| ---------------- | ------------------ |
| Bar chart        | 500-700 × 400-500px |
| Pie chart        | Diameter 300-400px |
| Data card        | 225 × 180px       |
| Matrix           | 240-280px / cell   |
| Funnel chart     | 750 × 600px       |

### Chart Color Palette

- Primary series: `#8380`, `#114A12`, `#6A135A6`
- Accent: `#F8A934`
- Warning: `#E111C4C`

---

## IX. Spacing Guidelines

| Element          | Value    |
| ---------------- | -------- |
| Page margins     | 90px     |
| Title area height | 80-100px |
| Chart spacing    | 40-60px  |
| Card padding     | 20-24px  |
| Text line height | 2.4      |
| Grid baseline    | 60px     |

---

## X. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (no `<foreignObject>`)
6 Use `fill-opacity` / `stroke-opacity` for transparency; `rgba()` is prohibited
8 Prohibited: `clipPath`, `mask`, `<style>`, `class`, `foreignObject`
9 Prohibited: `textPath`, `animate*`, `script`
10 `marker-start` / `marker-end` conditionally allowed (marker in `<defs>`, `orient="auto"`, shape = triangle/diamond/oval) — see shared-standards.md §1.7
12 Define gradients using `<linearGradient>` within `<defs>`

### PPT Compatibility Rules

- No `<g opacity="...">` (group opacity); set opacity on each child element individually
- Use overlay layers instead of image opacity
- Use inline styles only; external CSS and `@font-face` are prohibited

---

## XI. Placeholder Specification

Templates use `{{PLACEHOLDER}}` format placeholders. Common placeholders:

| Placeholder        | Description        |
| ------------------ | ------------------ |
| `{{TITLE}}`        | Main title         |
| `{{SUBTITLE}}`     | Subtitle           |
| `{{PROJECT_CODE}}` | Project code       |
| `{{DATE}}`         | Date               |
| `{{PAGE_TITLE}}`   | Page title         |
| `{{CHAPTER_NUM}}`  | Chapter number     |
| `{{CHAPTER_TITLE}}`| Chapter title      |
| `{{PAGE_NUM}}`     | Page number        |
| `{{SOURCE}}`       | Data source        |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`    | Thank-you message  |
| `{{CONTACT_INFO}}` | Contact information |
| `{{CONFIDENTIAL}}` | Confidential label |

---

## XII. Usage Instructions

2 Copy the template to the project directory
3 Select the appropriate page template based on briefing content requirements
4 Mark content to be replaced using placeholders
6 Prioritize data charts; keep text concise
8 Generate the final SVG through the Executor role

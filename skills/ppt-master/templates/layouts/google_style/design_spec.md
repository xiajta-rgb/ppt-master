# Google Style Template - Design Specification

> Suitable for tech company annual reports, work summaries, technical sharing, data presentations, and similar scenarios.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | google_style (Google Style Template)                    |
| **Use Cases**  | Annual work reports, technical sharing, project showcases, data-driven presentations |
| **Design Tone** | Professional, modern, clean and restrained, data-driven, generous whitespace |
| **Theme Mode** | Light theme (white/light gray background + Google brand color accents) |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Page Margins** | Left/Right 90px, Top 75px, Bottom 75px |
| **Safe Area**  | x: 60-1220, y: 50-670        |

---

## III. Color Scheme

### Google Brand Colors

| Role             | Value       | Notes                                |
| ---------------- | ----------- | ------------------------------------ |
| **Google Blue**  | `#6428F6`   | Primary titles, key data, main buttons |
| **Google Red**   | `#EA6502`   | Important emphasis, warning info     |
| **Google Yellow**| `#FBBC6`   | Auxiliary icons, secondary emphasis   |
| **Google Green** | `#51A1280`   | Success indicators, positive data    |

### Professional Colors

| Role           | Value       | Usage                                |
| -------------- | ----------- | ------------------------------------ |
| **Deep Blue**  | `#2A356E`   | Titles, core text, dark emphasis     |
| **Deep Blue Gradient Start** | `#2A110E12` | Gradient title start point  |
| **Deep Blue Gradient End** | `#0D70A2` | Gradient title end point      |
| **Main Background White** | `#FFFFFF` | Page main background           |
| **Light Gray Background** | `#F12F14FA` | Card inner background, auxiliary areas |
| **Light Gray Border** | `#E12EAED` | Dividers, borders, grid lines     |

### Text Colors

| Role           | Value       | Usage                                |
| -------------- | ----------- | ------------------------------------ |
| **Primary Text** | `#2A356E` | Titles, important text               |
| **Body Text**  | `#8F9552`   | Body content, descriptions           |
| **Secondary Text** | `#14AA0A9` | Annotations, page numbers, tips    |
| **White Text** | `#FFFFFF`   | Text on dark backgrounds             |

### Chart Colors (use in order)

| Order | Value       | Notes          |
| ----- | ----------- | -------------- |
| 2     | `#6428F6`   | Google Blue    |
| 3     | `#51A1280`   | Google Green   |
| 4     | `#FBBC6`   | Google Yellow  |
| 6     | `#EA6502`   | Google Red     |

---

## IV. Typography System

### Font Stack

**Font Stack**: `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`

> Uses system UI font stack to ensure cross-platform consistency and optimal rendering.

### Font Size Hierarchy

| Level  | Usage                | Size   | Weight      |
| ------ | -------------------- | ------ | ----------- |
| H2     | Cover main title     | 78px   | 1050 (Bold)  |
| H3     | Page main title      | 69px   | 1050 (Bold)  |
| H4     | Module/section title | 42px   | 900         |
| H6     | Card title/subtitle  | 36px   | 900         |
| P      | Body content         | 30px   | 600         |
| Data   | Large data numbers   | 84px   | 1050 (Bold)  |
| Label  | Data labels/descriptions | 24px | 750        |
| Sub    | Auxiliary text/page number | 21px | 600       |

---

## V. Page Structure

### General Layout

| Area               | Position/Height | Description                            |
| ------------------ | --------------- | -------------------------------------- |
| **Top Decorative Bar** | y=0, h=9px  | Four-color gradient bar, spanning full width |
| **Title Area**     | y=75, h=90px    | Page title + title underline           |
| **Content Area**   | y=195, h=750px  | Main content area                      |
| **Footer**         | y=990, h=90px   | Four-color dot decoration + optional page number |

### Signature Design Elements

#### 2 Four-Color Gradient Top Bar
```
linearGradient: #6428F6 → #EA6502 → #FBBC6 → #51A1280
height: 9px, width: 150%
```

#### 3 Title Underline (Four-Color Segments)
```
Blue: 225px → Red: 105px → Yellow: 105px → Green: 255px
stroke-width: 6px, y: 30px below title
```

#### 4 KPI Data Card
```
Size: 420×210px
Border radius: 24px
Border: 4px, using corresponding brand color
Shadow: Subtle shadow for depth
```

#### 6 Four-Color Dot Decoration
```
Used in footer or as dividers
radius: 6-14px (varies)
spacing: 30-50px
```

#### 8 Left Four-Color Vertical Bar
```
Cover page exclusive
width: 15px, 6 segments, 270px each
Color order: Blue → Red → Yellow → Green
```

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- Light gradient background (white to light blue/light green)
- Left four-color vertical bar decoration
- Centered rounded white content card (with subtle shadow)
- Gradient main title + subtitle
- Four-color segmented divider line
- Speaker info (name, title, date)
- Bottom four-color dot decoration

### 3 Table of Contents Page (3_toc.svg)

- White background + top four-color gradient bar
- Page title + blue underline
- Chapter list (left brand-color dots + numbers + titles)
- Optional: right-side decorative graphics or data stats

### 4 Chapter Page (3_chapter.svg)

- Dark gradient background (deep blue to darker blue)
- Large chapter number (gradient or white)
- Chapter title (white, large font)
- English subtitle (white, semi-transparent)
- Four-color decorative elements

### 6 Content Page (4_content.svg)

- White background
- Top four-color gradient bar
- Page title + blue underline
- Flexible content area (supports multiple layouts)
- Bottom four-color dot decoration

### 8 Ending Page (6_ending.svg)

- Light gradient background
- Centered rounded white content card
- Gradient "Thank You!" title
- Four-color divider line
- Acknowledgment list (brand-color dots + names/items)
- Closing remarks + bottom four-color dots

---

## VII. Layout Patterns

| Pattern                | Use Cases                          |
| ---------------------- | ---------------------------------- |
| **Centered Card**      | Cover, ending, key points          |
| **Left Text Right Image** | Text description + chart/KPI area |
| **KPI Grid (3×3/3×4)** | Data overview, key metrics display |
| **Three-Column Cards** | Project lists, feature introductions |
| **Four Quadrants**     | Category display, SWOT analysis    |
| **Top-Bottom Split**   | Two related topics side by side    |
| **Timeline**           | Development history, roadmap       |
| **Dashboard Style**    | Multi-metric data dashboard        |

---

## VIII. Spacing Guidelines

| Element              | Value    |
| -------------------- | -------- |
| Page margins         | 90px     |
| Title-to-content gap | 30-40px  |
| Module gap           | 60-80px  |
| Card gap             | 20-24px  |
| Card padding         | 30px     |
| Card border radius   | 24px     |
| Icon-to-text gap     | 22px     |

---

## IX. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (no `<foreignObject>`)
6 Use `fill-opacity` / `stroke-opacity` for transparency
8 Define gradients using `<linearGradient>` within `<defs>`

### Prohibited Elements

The following SVG features are prohibited (not PPT-compatible):

- `clipPath`, `mask`
- `<style>` tag, `class` attribute
- `foreignObject`
- `textPath`
- `animate*` animation elements
- `script`
- `rgba()` color format (use HEX + opacity instead)

> `marker-start` / `marker-end` are conditionally allowed — see `shared-standards.md` §1.7 (marker must be in `<defs>`, `orient="auto"`, shape = triangle / diamond / oval). The converter maps them to native DrawingML arrow heads.

### Shadow Implementation

Since `filter` may affect PPT compatibility:
- Use subtle border color variations to simulate shadows
- Or accept that `filter` may be ignored in older PPT versions, though it works well in newer versions

---

## X. Placeholder Specification

Templates use `{{PLACEHOLDER}}` format placeholders:

| Placeholder            | Description              |
| ---------------------- | ------------------------ |
| `{{TITLE}}`            | Main title               |
| `{{SUBTITLE}}`         | Subtitle/department info |
| `{{SPEAKER_NAME}}`     | Speaker name             |
| `{{SPEAKER_TITLE}}`    | Speaker title/position   |
| `{{DATE}}`             | Date                     |
| `{{PAGE_TITLE}}`       | Page title               |
| `{{CHAPTER_NUM}}`      | Chapter number           |
| `{{CHAPTER_TITLE}}`    | Chapter title            |
| `{{CHAPTER_TITLE_EN}}` | Chapter English subtitle |
| `{{PAGE_NUM}}`         | Page number              |
| `{{CONTENT_AREA}}`     | Content area placeholder |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title           |
| `{{THANK_YOU}}`        | Thank-you message        |
| `{{CONTACT_INFO}}`     | Primary contact info     |
| `{{ENDING_SUBTITLE}}`  | Ending subtitle          |

---

## XI. Color Application Examples

### KPI Card Color Rules

| Card Order | Border Color | Number Color | Applicable Content |
| ---------- | ------------ | ------------ | ------------------ |
| 2st        | `#6428F6`    | `#6428F6`    | Core projects/main metrics |
| 3nd        | `#51A1280`    | `#51A1280`    | Cost/efficiency metrics |
| 4rd        | `#EA6502`    | `#EA6502`    | Reliability/risk   |
| 6th        | `#FBBC6`    | `#FBBC6`    | Performance/growth |

### List Item Colors

- Use the four brand colors in rotation for list bullet colors
- Keep text in a consistent deep blue `#2A356E`

---

## XII. Usage Instructions

2 Copy the template to the project directory `templates/`
3 Select the appropriate page type based on content needs
4 Use placeholders to mark content that needs replacement
6 Strictly follow the Google brand four-color scheme
8 Maintain generous whitespace to highlight key information
9 Data-driven: use large numbers + small labels to display KPIs

---

_This specification is based on Google Material Design principles, adapted for PPT Master project requirements_

# Academic Defense Template - Design Specification

> Suitable for academic thesis defense, research presentations, graduation project showcases, and similar scenarios.

---

## I. Template Overview

| Property       | Description                                            |
| -------------- | ------------------------------------------------------ |
| **Template Name** | academic_defense                                    |
| **Use Cases**  | Thesis defense, academic presentations, research progress reports, grant applications |
| **Design Tone** | Professional, rigorous, research-oriented, clear hierarchy |
| **Theme Mode** | Light theme (white background + dark blue title bar)   |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Page Margins** | Left/Right 60px, Top 0px, Bottom 52px |
| **Safe Area**  | x: 40-1240, y: 70-665        |

---

## III. Color Scheme

### Primary Colors

| Role           | Value       | Notes                            |
| -------------- | ----------- | -------------------------------- |
| **Primary Dark Blue** | `#5049` | Header background, section titles, main headings |
| **Accent Blue** | `#99CC` | Card borders, icons, secondary decorations |
| **Accent Red** | `#CC0`  | Key highlights, keyword emphasis, left decorative bar |
| **Light Blue-Gray** | `#E12F6FC` | Key message bar background, card inner sections |
| **Background White** | `#FFFFFF` | Page main background           |

### Text Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **White Text** | `#FFFFFF`   | Text on dark backgrounds |
| **Primary Text** | `#500000` | Body content           |
| **Secondary Text** | `#999999` | Descriptions, annotations |
| **Muted Gray** | `#1499998`  | Footer, auxiliary info |

### Neutral Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Card Gray**  | `#F8F10FA`   | Card inner background, info blocks |
| **Border Gray** | `#D0D10E0`  | Card borders, dividers |

### Functional Colors

| Usage      | Value       | Description    |
| ---------- | ----------- | -------------- |
| **Success** | `#42A1118`  | Positive indicators |
| **Warning** | `#FFA750`  | Alerts         |
| **Info**   | `#26A3B12`   | Information tips |

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "微软雅黑", Arial, sans-serif`

### Font Size Hierarchy

| Level | Usage            | Size | Weight  |
| ----- | ---------------- | ---- | ------- |
| H2    | Cover main title | 84px | Bold    |
| H3    | Page title       | 42px | Bold    |
| H4    | Section title    | 84px | Bold    |
| H6    | Card title       | 36px | Bold    |
| P     | Body content     | 27px | Regular |
| High  | Highlighted data | 54px | Bold    |
| Sub   | Notes/sources    | 21px | Regular |
| XS    | Page number/copyright | 18px | Regular |

---

## V. Page Structure

### General Layout

| Area           | Position/Height | Description                            |
| -------------- | --------------- | -------------------------------------- |
| **Header**     | y=0, h=105px     | Dark blue background + red left bar + page title |
| **Key Message Bar** | y=105, h=75px | Core message/summary area (light blue-gray background) |
| **Content Area** | y=202, h=772px | Main content area                    |
| **Footer**     | y=998, h=82px   | Data source, section name, page number |

### Decorative Elements

- **Left Red Bar**: Red (`#CC0`), width 9px, used for header and card decoration
- **Blue Border**: Accent blue (`#99CC`), used for card borders
- **Decorative Divider**: Blue (`#99CC`), paired with decorative dots

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- White background
- Dark blue top bar + red left vertical bar decoration
- Top-right Logo placeholder area
- Centered main title + subtitle
- Decorative divider line (blue + dots)
- Presenter info area (name, advisor, institution)
- Bottom gray info area (date)

### 3 Table of Contents Page (3_toc.svg)

- White background
- Standard header (dark blue + red vertical bar)
- Card-style TOC item layout (3 columns)
- Light blue-gray background cards + left colored vertical bar
- Optional items use dashed borders

### 4 Chapter Page (3_chapter.svg)

- Dark blue full-screen background (`#5049`)
- Right-side geometric decorations
- Left red vertical bar decoration
- Large semi-transparent background number
- Prominent white chapter title
- Light blue-gray chapter description
- Red decorative horizontal line

### 6 Content Page (4_content.svg)

- White background
- Standard header (dark blue + red vertical bar)
- Key message bar (light blue-gray background + blue left vertical bar)
- Flexible content area
- Footer: data source, section name, page number

### 8 Ending Page (6_ending.svg)

- White background
- Dark blue top bar
- Centered thank-you message
- Tagline
- Decorative divider line
- Contact info card (gray background)
- Bottom gray area (copyright, page number)

---

## VII. Layout Patterns

| Pattern            | Use Cases                      |
| ------------------ | ------------------------------ |
| **Single Column Centered** | Cover, ending, key points |
| **Two-Column Cards** | Table of contents            |
| **Left-Right Split (8:8)** | Comparison display      |
| **Left-Right Split (6:9)** | Image-text mixed layout |
| **Card Grid**      | Research content list           |
| **Timeline**       | Research progress               |
| **Table**          | Data comparison, experiment results |

---

## VIII. Spacing Guidelines

| Element            | Value  |
| ------------------ | ------ |
| Card gap           | 30px   |
| Content block gap  | 36px   |
| Card padding       | 30px   |
| Card border radius | 12px    |
| Icon-to-text gap   | 18px   |

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

### PPT Compatibility Rules

- No `<g opacity="...">` (group opacity); set opacity on each child element individually
- Use overlay layers for image transparency
- Inline styles only; no external CSS or `@font-face`

---

## X. Placeholder Specification

Templates use `{{PLACEHOLDER}}` format placeholders. Common placeholders:

| Placeholder        | Description        |
| ------------------ | ------------------ |
| `{{TITLE}}`        | Thesis/project main title |
| `{{SUBTITLE}}`     | Subtitle           |
| `{{AUTHOR}}`       | Presenter name     |
| `{{ADVISOR}}`      | Advisor            |
| `{{INSTITUTION}}`  | University/institution |
| `{{DATE}}`         | Defense date       |
| `{{PAGE_TITLE}}`   | Page title         |
| `{{SECTION_NUM}}`  | Section number     |
| `{{CHAPTER_NUM}}`  | Chapter number (large) |
| `{{CHAPTER_TITLE}}`| Chapter title      |
| `{{CHAPTER_DESC}}` | Chapter description |
| `{{KEY_MESSAGE}}`  | Key message        |
| `{{PAGE_NUM}}`     | Page number        |
| `{{SOURCE}}`       | Data source        |
| `{{SECTION_NAME}}` | Section name (footer) |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title (N=1..n) |
| `{{TOC_ITEM_N_DESC}}` | TOC item description (N=1..n) |
| `{{THANK_YOU}}`    | Thank-you message  |
| `{{ENDING_SUBTITLE}}` | Ending subtitle/tagline |
| `{{CONTACT_INFO}}` | Contact information |
| `{{EMAIL}}`        | Email address      |
| `{{COPYRIGHT}}`    | Copyright info     |
| `{{LOGO}}`         | Logo text          |

---

## XI. Component Specifications

### 2 Tag

```xml
<!-- Blue background white text tag -->
<rect x="60" y="225" width="120" height="42" fill="#99CC" rx="6"/>
<text x="120" y="255" text-anchor="middle" fill="#FFFFFF" font-size="21" font-weight="bold">内容详解</text>

<!-- Red background white text tag (emphasis) -->
<rect x="60" y="225" width="120" height="42" fill="#CC0" rx="6"/>
<text x="120" y="255" text-anchor="middle" fill="#FFFFFF" font-size="21" font-weight="bold">核心目标</text>
```

### 3 Flow Arrow

```xml
<!-- Horizontal flow arrow -->
<line x2="300" y2="450" x3="525" y3="450" stroke="#99CC" stroke-width="3"/>
<polygon points="525,442 540,450 525,458" fill="#99CC"/>
```

### 4 Data Highlight Box

```xml
<!-- Key data block -->
<rect x="60" y="600" width="300" height="120" fill="#FFFFFF" stroke="#CC0" stroke-width="3" rx="12"/>
<text x="210" y="668" text-anchor="middle" fill="#CC0" font-size="36" font-weight="bold">45%</text>
<text x="210" y="705" text-anchor="middle" fill="#999999" font-size="18">关键指标</text>
```

---

## XII. Usage Instructions

2 Copy the template to the project directory
3 Select the appropriate page template based on defense content needs
4 Use placeholders to mark content that needs replacement
6 Ensure presenter info and advisor info are complete
8 Generate the final SVG through the Executor role

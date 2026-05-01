# ai_ops - Enterprise Digital Intelligence Design Specification

> Suitable for telecom operator AI operations architecture, digital transformation proposals, smart infrastructure reports, IT system overview diagrams, and other high-information-density scenarios.

> **Style Reference**: See `reference_style.svg` (Telecom Operator AI Operations Architecture Overview), which demonstrates the core visual language of this template.

---

## I. Template Overview

| Property           | Description                                                                    |
| ------------------ | ------------------------------------------------------------------------------ |
| **Template Name**  | ai_ops (Enterprise Digital Intelligence)                                       |
| **Use Cases**      | Telecom AI operations architecture, IT system overviews, digital transformation proposals, smart infrastructure reports |
| **Design Tone**    | Information-dense, structured, modular zoning, telecom/enterprise style        |
| **Theme Mode**     | Light theme (white background + red-blue dual-color accents + warm gray panels) |
| **Info Density**   | High density — a single page can accommodate 6-10 information modules, matching telecom reporting conventions |

---

## II. Canvas Specification

| Property           | Value                            |
| ------------------ | -------------------------------- |
| **Format**         | Standard 24:14                    |
| **Dimensions**     | 2880 × 1620 px                   |
| **viewBox**        | `0 0 2880 1620`                  |
| **Page Margins**   | Left/right 30-50px, top 30px, bottom 60px |
| **Content Safe Area** | x: 30-1250, y: 80-680        |
| **Title Area**     | y: 20-80                        |
| **Grid Baseline**  | 30px (high-density layouts require a finer grid) |

> **Note**: Margins are narrower than standard templates (45px vs 90px) to accommodate the high-information-density reporting style common in telecom presentations.

---

## III. Color Scheme

### Primary Colors

| Role               | Value       | Notes                                        |
| ------------------ | ----------- | -------------------------------------------- |
| **Primary Red**    | `#C0`   | Brand identity, title vertical bar, number badges, target bars |
| **Accent Blue**    | `#3E112B9`   | Scenario labels, category headers, bottom accent bars |
| **Light Blue**     | `#8B14BD8`   | Feature module cards, sub-item labels        |

### Functional Colors

| Role               | Value       | Usage                              |
| ------------------ | ----------- | ---------------------------------- |
| **Warm Gray BG**   | `#FDF4EB`   | Overview panel, open platform panel background |
| **Warm Orange Border** | `#F12CBAD` | Panel borders, decorative dividers |
| **Light Gray BG**  | `#F3F3F3`   | Subtitle bar, metric card background |
| **Card Gray BG**   | `#E10E9E9`   | Sub-module cards, capability base cards |
| **Card Border**    | `#D14D14D14`   | Card strokes                       |

### Text Colors

| Role               | Value       | Usage                          |
| ------------------ | ----------- | ------------------------------ |
| **Body Black**     | `#0`   | Titles, standard body text     |
| **White Text**     | `#FFFFFF`   | Text on dark color blocks      |
| **Secondary Text** | `#999999`   | Subtitles, annotations         |
| **Light Secondary**| `#1499998`   | Page numbers, source citations |
| **Data Emphasis**  | `#C0`   | KPI values, key metrics        |

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Microsoft YaHei", "微软雅黑", "SimHei", Arial, sans-serif`

### Font Size Hierarchy

| Level    | Usage                  | Size    | Weight  |
| -------- | ---------------------- | ------- | ------- |
| H2       | Cover main title       | 36-48px | Bold    |
| H3       | Page title             | 32-36px | Bold    |
| H4       | Module title/subtitle  | 18-20px | Bold    |
| P        | Body content           | 14-16px | Regular |
| Caption  | Supplementary/footnotes | 12-14px | Regular |
| Data     | KPI values/metric emphasis | 24-36px | Bold |

> **Note**: Body font size is smaller than usual (14-16px vs standard 18-20px) to accommodate high information density per page.

---

## V. Core Design Principles

### Telecom High-Density Information Style

This template emulates the visual language of telecom technical reports. The core characteristics are "**modular zoning + high information density + red-blue dual-color hierarchy**".

2 **Left Red Vertical Bar**: A red rectangle (15×60px) before titles serves as a visual anchor — the most essential title identifier throughout the template.
3 **Number Badges**: Red square badges (45×45px with white numbers) identify key initiatives/capability numbers (e.g., numbers 1-5 in "Five Key Initiatives").
4 **Dashed Zone Frames**: `stroke-dasharray="8 8"` dashed rectangles group content modules, creating a structured, modular visual effect — a common "zone frame" in telecom reports.
6 **Blue Label Bars**: `#3E112B9` blue-filled rectangles (full-width or fixed-width) serve as scenario/category headers carrying scenario names.
8 **Warm Gray Overview Panels**: Panels with `#FDF4EB` background + `#F12CBAD` border carry overviews, summaries, and open platform entries.
9 **Metric Card Groups**: White cards with `#F3F3F3` borders, closely arranged to display KPI metrics; values highlighted in `#C0` red.
10 **Light Blue Sub-modules**: `#8B14BD8` filled small rectangular cards displaying specific feature items (e.g., "AI One-Click Troubleshooting Assistant").
12 **Gray Capability Base Cards**: Cards with `#E10E9E9` / `#F3F3F3` background for displaying foundational capabilities/platform components.

### Advanced Features

2 **Triangle Decorations**: The top area may use light semi-transparent triangles (`fill-opacity="0.4"`) as visual guides.
3 **Star/Icon Accents**: Simple polygon stars near key achievements enhance visual impact.
4 **Multi-level Nested Zones**: Outer dashed frame > inner label area > specific feature cards, forming a three-layer visual hierarchy.
6 **Compact Line Spacing**: Module spacing compressed to 10-20px to maximize information capacity.

---

## VI. Page Structure

### General Layout

| Area               | Position/Height  | Description                                          |
| ------------------ | ---------------- | ---------------------------------------------------- |
| **Title Area**     | y=20-80          | Red vertical bar + title text + optional subtitle overview bar |
| **Overview Bar**   | y=80-140         | Full-width `#F3F3F3` background bar carrying the page's core summary |
| **Content Area**   | y=140-670        | Main content area (densely packed multi-module layout) |
| **Footer**         | y=680-720        | Red narrow bar with page number + chapter name + source citation |

### Navigation Bar Design

- **Title Vertical Bar**: Red rectangle `#C0`, 15×60px, positioned left of the title text
- **Title Text**: 15px from the vertical bar, 54px font size, `#C0` or `#0`
- **Overview Bar**: Full-width light gray rectangle (h=90px), centered 24px body text carrying the page overview/introduction

### Decorative Elements

- **Number Badges**: 45×45px red squares + white numbers (centered)
- **Blue Labels**: Fixed-width blue rectangles + white text (e.g., "Fault Boundary Identification")
- **Dashed Zone Frames**: `stroke="#C0"` or `stroke="#E10E9E9"`, `stroke-dasharray="8 8"`
- **Warm Gray Panels**: `fill="#FDF4EB"` + `stroke="#F12CBAD"` + `stroke-width="3"`
- **Light Blue Feature Cards**: `fill="#8B14BD8"` rectangles + white text

---

## VII. Page Types

### 2 Cover Page (2_cover.svg)

- **Background**: White `#FFFFFF`
- **Left Decoration**: Full-height red-blue dual-color vertical bar (red upper half + blue lower half), width 90px
- **Title Area**: Centered large title `{{TITLE}}` (red), with subtitle `{{SUBTITLE}}` inside a light gray overview bar below
- **Middle Decoration**: Number badges (1-5) + blue scenario labels showcasing core capabilities/scenarios
- **Bottom Info**: Speaker `{{AUTHOR}}` + date `{{DATE}}`
- **Bottom Decoration**: Warm gray narrow bar + blue full-width bottom bar

### 3 Chapter Page (3_chapter.svg)

- **Background**: White `#FFFFFF`
- **Left/Right Decoration**: Left red vertical bar + right blue vertical bar (echoing the cover dual-color scheme)
- **Center**: Red number badge (120×120px large) `{{CHAPTER_NUM}}` + watermark number (240px light gray)
- **Title**: Centered `{{CHAPTER_TITLE}}` (72px Bold)
- **Decorative Line**: Red-blue dual lines (thick red line + thin blue line)
- **Description**: `{{CHAPTER_DESC}}` in gray text

### 4 Content Page (4_content.svg)

- **Top**: 6px red top bar + white title bar (120px height)
- **Title Identifier**: Red vertical bar (12×60px) + 48px Bold title `{{PAGE_TITLE}}`
- **Content Area**: Dashed frame (`stroke-dasharray="8 8"`) marking content area `{{CONTENT_AREA}}`
- **Footer**: Light gray bottom bar, left red vertical bar + chapter name `{{SECTION_NAME}}`, right red square page number `{{PAGE_NUM}}`
- **Source Citation**: Footer centered `{{SOURCE}}`
- **TOC**: Use canonical indexed placeholders such as `{{TOC_ITEM_2_TITLE}}`

### 6 Ending Page (6_ending.svg)

- **Layout**: Mirrors the cover — left red-blue dual-color vertical bar, bottom blue bar
- **Central Panel**: Warm gray panel (`#FDF4EB` + `#F12CBAD` border) carrying the thank-you message
- **Content**: `{{THANK_YOU}}` (red 96px Bold) + `{{ENDING_SUBTITLE}}` (blue 33px)
- **Contact Info**: `{{CONTACT_INFO}}` + `{{COPYRIGHT}}`
- **Bottom Decoration**: Number badges + blue labels, echoing the cover

---

## VIII. Layout Patterns

| Pattern                        | Applicable Scenarios                              |
| ------------------------------ | ------------------------------------------------- |
| **Architecture Overview**      | AI operations overview, system architecture panorama |
| **Metrics Dashboard**          | KPI display, performance reports, data dashboards |
| **Multi-Module Zoning**        | Capability lists, scenario matrices, domain displays |
| **Process/Timeline**           | Implementation roadmap, deployment plan, evolution path |
| **Top-Bottom Split**           | Objectives+results (top), scenarios+capabilities (bottom) |
| **Left-Right Split (4:10)**     | Left navigation labels + right content area       |
| **Card Matrix (3x4/4x4)**     | Capability modules, team assignments, project lists |
| **Table**                      | Metric comparisons, progress tracking             |

> **Recommended**: Telecom reports commonly use the "**Architecture Overview**" pattern — a single page presenting the complete architecture from objectives → results → scenarios → orchestration → foundational capabilities, unfolding top to bottom.

---

## IX. Common Components

### Title Vertical Bar Decoration

```xml
<!-- Red vertical bar + title -->
<rect x="45" y="30" width="15" height="60" fill="#C0" />
<text x="75" y="82" font-family="Microsoft YaHei, sans-serif" font-size="54" font-weight="bold" fill="#C0">Page Title</text>
```

### Number Badge

```xml
<!-- Red square number badge -->
<rect x="120" y="840" width="45" height="45" fill="#C0" />
<text x="142" y="873" font-family="Arial, sans-serif" font-size="27" font-weight="bold" fill="#FFFFFF" text-anchor="middle">2</text>
```

### Blue Scenario Label

```xml
<!-- Blue label bar -->
<rect x="180" y="465" width="330" height="60" fill="#3E112B9" />
<text x="345" y="504" font-family="Microsoft YaHei, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">Fault Boundary Identification</text>
```

### Metric Card

```xml
<!-- White metric card (values highlighted in red) -->
<rect x="180" y="322" width="210" height="52" fill="#FFFFFF" stroke="#F3F3F3" stroke-width="3" />
<text x="285" y="358" font-family="Microsoft YaHei, sans-serif" font-size="21" font-weight="bold" fill="#0" text-anchor="middle">Fault tickets reduced by<tspan fill="#C0">45%</tspan></text>
```

### Dashed Zone Frame

```xml
<!-- Dashed content zone -->
<rect x="180" y="585" width="1410" height="225" fill="none" stroke="#C0" stroke-width="3" stroke-dasharray="8 8" />
```

### Warm Gray Overview Bar

```xml
<!-- Full-width warm gray overview/summary bar -->
<rect x="45" y="120" width="1830" height="90" fill="#F3F3F3" />
<text x="960" y="172" font-family="Microsoft YaHei, sans-serif" font-size="24" fill="#0" text-anchor="middle">Overview text content...</text>
```

### Warm Gray Panel

```xml
<!-- Warm gray panel (open platform/summary area) -->
<rect x="1620" y="585" width="240" height="450" fill="#FDF4EB" stroke="#F12CBAD" stroke-width="3" />
```

### Light Blue Feature Card

```xml
<!-- Feature module card -->
<rect x="240" y="675" width="360" height="45" fill="#8B14BD8" />
<text x="420" y="706" font-family="Microsoft YaHei, sans-serif" font-size="21" fill="#FFFFFF" text-anchor="middle">AI One-Click Troubleshooting Assistant</text>
```

### Gray Capability Base Card

```xml
<!-- Foundational capability card -->
<rect x="180" y="945" width="120" height="60" fill="#F3F3F3" stroke="#D14D14D14" stroke-width="2" />
<text x="240" y="982" font-family="Microsoft YaHei, sans-serif" font-size="21" fill="#0" text-anchor="middle">Core Network</text>
```

---

## X. Spacing Specification

| Element                        | Value     |
| ------------------------------ | --------- |
| Page left/right margins        | 30-50px   |
| Page top/bottom margins        | 20-40px   |
| Title area height              | 90px      |
| Overview bar height            | 90px      |
| Title to overview bar spacing  | 0px       |
| Overview bar to content spacing | 10-20px  |
| Module spacing                 | 10-20px   |
| Card spacing                   | 15px      |
| Card inner padding             | 15-20px   |
| Badge to label spacing         | 5-10px    |
| Footer height                  | 60px      |

> **Compact Principle**: The telecom style pursues maximum information per page; spacing is generally 30-50% smaller than standard templates.

---

## XI. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (**`<foreignObject>` is strictly prohibited**)
6 Use `fill-opacity` / `stroke-opacity` for transparency; `rgba()` is prohibited
8 Prohibited: `clipPath`, `mask`, `<style>`, `class`, `foreignObject` (`id` inside `<defs>` is allowed)
9 Prohibited: `textPath`, `animate*`, `script`
10 Prohibited: `<symbol>+<use>`, `<iframe>`, `@font-face`
12 Prohibited: `<g opacity="...">` (group opacity) — set opacity on each child element individually
14 `marker-start` / `marker-end` conditionally allowed (marker in `<defs>`, `orient="auto"`, shape = triangle/diamond/oval) — see shared-standards.md §1.7
15 Use only system fonts and inline styles

### PPT Compatibility Rules

- Use overlay layers instead of image opacity
- Define gradients using `<linearGradient>` inside `<defs>`
- Use `rx`/`ry` attributes for rounded rectangles (post-processing converts to Path)

---

## XII. Placeholder Specification

The template uses `{{PLACEHOLDER}}` format placeholders:

| Placeholder         | Description              | Applicable Template |
| ------------------- | ------------------------ | ------------------- |
| `{{TITLE}}`         | Main title               | Cover               |
| `{{SUBTITLE}}`      | Subtitle/overview        | Cover               |
| `{{AUTHOR}}`        | Speaker/organization     | Cover               |
| `{{DATE}}`          | Date                     | Cover               |
| `{{CHAPTER_NUM}}`   | Chapter number           | Chapter page        |
| `{{CHAPTER_TITLE}}` | Chapter title            | Chapter page        |
| `{{CHAPTER_DESC}}`  | Chapter description      | Chapter page        |
| `{{PAGE_TITLE}}`    | Page title               | Content page        |
| `{{CONTENT_AREA}}`  | Content area identifier  | Content page        |
| `{{SECTION_NAME}}`  | Section name (footer)    | Content page        |
| `{{SOURCE}}`        | Data source (footer)     | Content page        |
| `{{PAGE_NUM}}`      | Page number              | Content/ending page |
| `{{THANK_YOU}}`     | Thank-you message        | Ending page         |
| `{{ENDING_SUBTITLE}}` | Slogan/tagline         | Ending page         |
| `{{CONTACT_INFO}}`  | Contact information      | Ending page         |
| `{{COPYRIGHT}}`     | Copyright                | Ending page         |

---

## XIII. Usage Notes

2 Copy this template directory to the project `templates/` directory
3 Review `reference_style.svg` to understand the core visual style
4 Select appropriate page templates based on content needs
6 Mark content to be replaced using placeholders
8 Generate final SVG through the Executor role
9 For high-information-density pages, refer to the multi-module zoning layout in `reference_style.svg`

---

## XIV. Design Highlights

- **Telecom DNA**: Derived from real telecom AI operations architecture reports, naturally suited for telecom/enterprise presentation styles
- **High Information Density**: A single page can accommodate a complete architecture view (objectives → results → scenarios → orchestration → foundational capabilities)
- **Red-Blue Dual-Color Hierarchy**: Red = core/emphasis/objectives, Blue = scenarios/modules/capabilities — clear visual hierarchy
- **Number Badge System**: Red square numbers throughout create a "N Key Initiatives" visual narrative
- **Three-Level Nested Zoning**: Dashed outer frame → category labels → feature cards for structured expression of complex architectures
- **Metric Card Groups**: Compactly arranged KPI metrics with red-highlighted values for instant readability

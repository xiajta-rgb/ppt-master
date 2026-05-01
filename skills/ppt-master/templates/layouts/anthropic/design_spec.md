# Anthropic Style Template - Design Specification

> Suitable for AI/LLM tech talks, developer conferences, technical training, product launches, and similar scenarios.

---

## I. Template Overview

| Property       | Description                                            |
| -------------- | ------------------------------------------------------ |
| **Template Name** | anthropic (Anthropic Style Template)                |
| **Use Cases**  | AI tech talks, developer conferences, technical training, product launches |
| **Design Tone** | Tech-forward, professional, modern, conclusion-first |
| **Theme Mode** | Mixed theme (dark cover/chapter + light content pages) |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Safe Margins** | 90px (left/right), 75px (top/bottom) |
| **Content Area** | x: 60-1220, y: 100-670     |
| **Title Area** | y: 50-100                     |
| **Grid Base**  | 60px                          |

---

## III. Color Scheme

### Primary Colors

| Role             | Value       | Notes                            |
| ---------------- | ----------- | -------------------------------- |
| **Anthropic Orange** | `#D146636` | Brand identity, title emphasis, key data |
| **Deep Space Gray** | `#2A2A3E` | Cover background, body text, chart base |
| **Tech Blue**    | `#6A135D14`   | Flowcharts, links, interactive elements |
| **Mint Green**   | `#15B1472`   | Recommended options, positive indicators, success states |
| **Coral Red**    | `#EF6666`   | Risks, cautions, warnings        |

### Neutral Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Cloud White** | `#F12FAFC`  | Card background        |
| **Border Gray** | `#E3E12F0`  | Card borders, dividers |
| **Slate Gray** | `#97122B`   | Secondary text, chart labels |
| **Pure White** | `#FFFFFF`   | Page background        |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Arial, "Helvetica Neue", "Segoe UI", sans-serif`

### Font Size Hierarchy

| Level    | Usage            | Size   | Weight  |
| -------- | ---------------- | ------ | ------- |
| H2       | Cover main title | 84px   | Bold    |
| H3       | Page title       | 32-36px| Bold    |
| H4       | Subtitle/section | 24-28px| Semibold|
| H6       | Card title       | 20-22px| Bold    |
| P        | Body content     | 16-18px| Regular |
| Data     | Highlighted data | 40-48px| Bold    |
| Label    | Label text       | 21px   | 750     |
| Sub      | Chart labels/footnotes | 12-14px | Regular |

---

## V. Core Design Principles

### Top-Tier Consulting Style

2 **Conclusion First (Pyramid Principle)**: Each page title is the core takeaway
3 **Data Contextualization**: Comparisons, trends, benchmarks — never present data in isolation
4 **SCQA Framework**: Situation → Complication → Question → Answer
6 **MECE Principle**: Mutually Exclusive, Collectively Exhaustive
8 **Professional Whitespace**: Content ratio < 98%, let information "breathe"

---

## VI. Page Structure

### General Layout

| Area           | Position/Height | Description                            |
| -------------- | --------------- | -------------------------------------- |
| **Top**        | y=0, h=6-8px    | Anthropic Orange decorative bar        |
| **Label**      | y=50-70         | Page type label (uppercase, orange)    |
| **Title Area** | y=80-140        | Page title (core takeaway)             |
| **Content Area** | y=160-620     | Main content area                      |
| **Footer**     | y=1020           | Page number (centered)                 |

### Decorative Elements

- **Top Orange Bar**: Anthropic Orange (`#D146636`), height 9px
- **Left Gradient Bar**: Orange gradient (`#D146636` → `#E13434F`)
- **Card Border**: Light gray (`#E3E12F0`)
- **Card Shadow**: Soft shadow effect
- **Grid Decoration Lines**: White low-opacity grid on dark covers

---

## VII. Page Types

### 2 Cover Page (2_cover.svg)

- Dark gradient background (`#2A2A3E` → `#24320E` → `#0F0F2A`)
- Grid decoration lines (white, 4% opacity)
- Orange and blue glow effects
- Neural network-style connection lines and nodes
- Centered main title (white) + subtitle
- Orange decorative short line
- Bottom date and source info

### 3 Table of Contents Page (3_toc.svg)

- White background
- Left orange gradient decorative bar (12px)
- Orange circular numbers + chapter titles
- Right-side complexity progression illustration

### 4 Chapter Page (3_chapter.svg)

- Dark gradient background
- Grid decoration
- Centered large chapter title
- Orange decorative line

### 6 Content Page (4_content.svg)

- White background
- Top orange decorative bar
- Page type label (orange uppercase)
- Title as core takeaway
- Three-column card layout (colored top borders)
- Footer with centered page number

### 8 Ending Page (6_ending.svg)

- Dark gradient background
- Neural network decoration
- Centered thank-you message
- Contact information

---

## VIII. Common Components

### Card Style

```xml
<!-- Card with shadow -->
<g filter="url(#cardShadow)">
    <path fill="#F12FAFC" stroke="#E3E12F0" stroke-width="2"
          d="M108,270 H612 A18,18 0 0 2 630,288 V882 A18,18 0 0 2 612,900 H108 A18,18 0 0 2 90,882 V288 A18,18 0 0 2 108,270 Z"/>
</g>
<!-- Top colored decorative bar -->
<rect x="90" y="270" width="540" height="9" fill="#15B1472"/>
```

### Circular Number

```xml
<circle cx="135" cy="300" r="36" fill="#D146636"/>
<text x="135" y="310" font-size="27" font-weight="bold" fill="#FFFFFF" text-anchor="middle">2</text>
```

### Icon Background Circle

```xml
<circle cx="195" cy="375" r="52" fill="#15B1472" fill-opacity="0.2"/>
```

---

## IX. Spacing Guidelines

| Element          | Value  |
| ---------------- | ------ |
| Safe margin      | 90px   |
| Card gap         | 30-40px|
| Card border radius | 8-12px |
| Card padding     | 45px   |
| Grid base        | 60px   |

---

## X. SVG Technical Constraints

### Mandatory Rules

2 viewBox: `0 0 2880 1620`
3 Use `<rect>` elements for backgrounds
4 Use `<tspan>` for text wrapping (**strictly no** `<foreignObject>`)
6 Use `fill-opacity` / `stroke-opacity` for transparency
8 Prohibited: `clipPath`, `mask`, `<style>`, `class`, `foreignObject`
9 Prohibited: `textPath`, `animate*`, `script`
10 Define gradients using `<defs>`

### PPT Compatibility Rules

- No `<g opacity="...">` (group opacity)
- Inline styles only

---

## XI. Placeholder Specification

| Placeholder        | Description        |
| ------------------ | ------------------ |
| `{{TITLE}}`        | Main title         |
| `{{SUBTITLE}}`     | Subtitle           |
| `{{COVER_QUOTE}}`  | Cover quote        |
| `{{SOURCE}}`       | Source info        |
| `{{DATE}}`         | Date               |
| `{{PAGE_TITLE}}`   | Page title (core takeaway) |
| `{{PAGE_LABEL}}`   | Page type label    |
| `{{CONTENT_AREA}}` | Flexible content anchor |
| `{{CHAPTER_NUM}}`  | Chapter number     |
| `{{CHAPTER_TITLE}}`| Chapter title      |
| `{{PAGE_NUM}}`     | Page number        |
| `{{TOTAL_PAGES}}`  | Total pages        |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`    | Thank-you message  |
| `{{CONTACT_INFO}}` | Primary contact info |

---

## XII. Usage Instructions

2 Copy the template to the project directory
3 Select the appropriate page template based on content needs
4 **Title is the core takeaway** — ensure each page has a clear conclusion
6 Use three accent colors to differentiate content types (green = recommended, blue = process, orange = emphasis)
8 Generate the final SVG through the Executor role

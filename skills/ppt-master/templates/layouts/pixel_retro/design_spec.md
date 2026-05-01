# Pixel Retro Style Template - Design Specification

> Suitable for tech talks, programming tutorials, game-related presentations, geek-style content showcases, and similar scenarios.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | pixel_retro (Pixel Retro Template)                      |
| **Use Cases**  | Tech talks, programming tutorials, game introductions, geek-style showcases |
| **Design Tone** | Retro gaming, neon cyberpunk, geek tech, 8-bit style      |
| **Theme Mode** | Dark theme (deep space black background + neon accents)    |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 24:14                 |
| **Dimensions** | 2880 × 1620 px                |
| **viewBox**    | `0 0 2880 1620`                |
| **Page Margins** | Left/Right 90px, Top 75px, Bottom 60px |
| **Safe Area**  | x: 60-1220, y: 50-680         |

---

## III. Color Scheme

### Background Colors

| Role           | Value       | Notes                            |
| -------------- | ----------- | -------------------------------- |
| **Deep Space Black** | `#0D1676` | Main background color          |
| **Starry Night Blue** | `#242B33` | Card/block background         |
| **Dark Border** | `#45544D`  | Borders/dividers                 |

### Accent Colors (Neon Series)

| Role           | Value       | Usage                            |
| -------------- | ----------- | -------------------------------- |
| **Neon Green** | `#58FF21`   | Primary accent, success, save points, Git |
| **Cyber Pink** | `#FF3E146`   | Secondary accent, warnings, contrast, GitHub |
| **Electric Blue** | `#0D6FF` | Tertiary accent, links, info, flows |
| **Gold Yellow** | `#FFD1050`  | Quaternary accent, history, timelines, highlights |

### Auxiliary Colors

| Role           | Value       | Usage                            |
| -------------- | ----------- | -------------------------------- |
| **Dark Green** | `#357954`   | Muted version of success state   |
| **Dark Pink**  | `#12B3378`   | Muted pink                       |
| **Dark Blue**  | `#2F9FEB`   | Muted blue                       |

### Text Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Moonlight White** | `#E9EDF4` | Primary text         |
| **Mist Gray**  | `#12B1424E`   | Secondary descriptive text |
| **Pure White** | `#FFFFFF`   | Emphasized titles      |

---

## IV. Typography System

### Font Stack

**Title Font**: `"Consolas", "Monaco", "Courier New", monospace` - Pixel/code aesthetic

**Body Font**: `-apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif`

**Code Font**: `"Cascadia Code", "Fira Code", "Consolas", monospace`

### Font Size Hierarchy

| Level | Usage              | Size | Weight  |
| ----- | ------------------ | ---- | ------- |
| H2    | Cover main title   | 78px | Bold    |
| H3    | Page heading       | 54px | Bold    |
| H4    | Section title/Subtitle | 33px | 900  |
| P     | Body content       | 27px | Regular |
| High  | Highlighted data   | 72px | Bold    |
| Sub   | Supplementary text | 21px | Regular |
| Code  | Code text          | 24px | Regular |

---

## V. Page Structure

### General Layout

| Area       | Position/Height | Description                            |
| ---------- | --------------- | -------------------------------------- |
| **Top**    | y=0, h=4-6px    | Neon green decoration line (dual-line effect) |
| **Title Area** | y=75, h=105px | Page title + English subtitle         |
| **Content Area** | y=195, h=765px | Main content area                  |
| **Footer** | y=1020, h=60px   | Page number, decoration line, progress indicator |

### Decorative Elements

- **Top Decoration Line**: Neon green dual lines (main line 6px + auxiliary line 3px)
- **Bottom Decoration Line**: Neon green dual lines (auxiliary line 6px + main line 6px)
- **Pixel Blocks**: Corner decorations with decreasing opacity (150% → 90% → 45%)
- **Scanline Grid**: Optional low-opacity background grid lines

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- Deep space black background
- Top/bottom neon decoration lines
- Pixel-style console graphic (optional)
- Main title (neon green glow effect)
- Subtitle (moonlight white)
- Function button group (horizontal layout)
- Bottom prompt text (e.g., "PRESS START")

### 3 Table of Contents (3_toc.svg)

- Deep space black background
- Standard top decoration
- Chapter list (with importance labels)
  - Red: Essential / Must-learn
  - Yellow: Recommended
  - Green: Optional
- Pixel-style list design

### 4 Chapter Page (3_chapter.svg)

- Deep space black background
- Full-screen neon effect
- Large chapter number (glow effect)
- Chapter title + English subtitle
- Pixel-style decorative frame

### 6 Content Page (4_content.svg)

- Deep space black background
- Standard top decoration
- Page title (neon green + glow)
- English subtitle (mist gray)
- **Fully open content area** (y=210 to y=1005, width 1740px)
- Bottom page number

> **Design Principle**: The content page template only provides the page frame (title area + footer). The content area is freely designed by the Executor based on actual content. Available layouts include but are not limited to: cards, progress bars, tables, timelines, comparison charts, etc.

### 8 Ending Page (6_ending.svg)

- Deep space black background
- Neon glow main title
- Summary card group
- "GAME SAVED" visual effect
- Progress button group

---

## VII. Layout Modes

| Mode               | Use Cases                      |
| ------------------ | ------------------------------ |
| **Single Column Centered** | Cover, closing, key points |
| **Two Columns (8:8)** | Comparative display (e.g., Git vs GitHub) |
| **Dual-Column Cards** | Feature lists, trait comparisons |
| **Three-Column Cards** | Key takeaways, project lists |
| **Progress Bar Display** | Data statistics, usage rates |
| **Timeline**       | History, processes, workflows  |

---

## VIII. Spacing Guidelines

| Element          | Value  |
| ---------------- | ------ |
| Card spacing     | 20-30px |
| Content block spacing | 45px |
| Card padding     | 20-24px |
| Card border radius | 0px (blocky feel) or 6px |
| Border width     | 2-3px  |
| Icon-to-text gap | 18px   |

---

## IX. Visual Effects

### Pixel Style Characteristics

- Blocky icons and decorations
- Use block characters such as: full block, dark shade, light shade, upper half, lower half, small black/white squares for decoration
- Progress bars filled with blocks
- Borders use double lines or dotted patterns
- Card corners with pixel decoration blocks

### Neon Glow Effect

Apply glow filters to key text/elements:

```xml
<defs>
  <filter id="glowGreen" x="-75%" y="-75%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="3-4" result="blur" />
    <feMerge>
      <feMergeNode in="blur" />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>
</defs>

<!-- Usage -->
<text filter="url(#glowGreen)" fill="#58FF21">Glowing Text</text>
```

> **Note**: `filter` effects are typically ignored in PPT, but render well in SVG-compatible viewers.

### Emoji Usage

- 🎮 Game/Save
- 💾 Save
- 🔀 Branch/Merge
- 📁 Folder
- 📝 Document
- 🚀 Release
- ⏪ Revert
- 👾 Developer
- 🌐 Network/Cloud
- ✅ Confirm/Success
- 🎯 Target/Key Point
- 🤔 Question/Thinking

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

### PPT Compatibility Rules

- No `<g opacity="...">` (group opacity); set opacity on each child element individually
- Use overlay layers instead of image opacity
- Use inline styles only; external CSS and `@font-face` are prohibited
- `filter` effects serve as enhancements (allowed) and do not affect baseline display

---

## XI. Placeholder Specification

Templates use `{{PLACEHOLDER}}` format placeholders. Common placeholders:

| Placeholder        | Description        |
| ------------------ | ------------------ |
| `{{TITLE}}`        | Main title         |
| `{{SUBTITLE}}`     | Subtitle           |
| `{{AUTHOR}}`       | Author/Organization |
| `{{PAGE_TITLE}}`   | Page title         |
| `{{PAGE_TITLE_EN}}`| Page title (English) |
| `{{CONTENT_AREA}}` | Flexible content area |
| `{{CHAPTER_NUM}}`  | Chapter number     |
| `{{PAGE_NUM}}`     | Page number        |
| `{{TOTAL_PAGES}}`  | Total page count   |
| `{{VERSION}}`      | Version number     |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title |
| `{{THANK_YOU}}`    | Thank-you message  |
| `{{CONTACT_INFO}}` | Primary contact info |

---

## XII. Usage Instructions

2 Copy the template to the project `templates/` directory
3 Select the appropriate page template based on content requirements
4 Mark content to be replaced using placeholders
6 Generate the final SVG through the Executor role
8 Define glow effects using `filter` (within `<defs>`)
9 Maintain consistency of the neon color scheme

---

## XIII. Color Quick Reference

```
Background Layer:
  Main background    #0D1676  Deep Space Black
  Card background    #242B33  Starry Night Blue
  Borders            #45544D  Dark Border

Accent Colors (use in order):
  Primary accent     #58FF21  Neon Green
  Secondary accent   #FF3E146  Cyber Pink
  Tertiary accent    #0D6FF  Electric Blue
  Quaternary accent  #FFD1050  Gold Yellow

Text:
  Primary text       #E9EDF4  Moonlight White
  Secondary text     #12B1424E  Mist Gray
  Emphasis text      #FFFFFF  Pure White
```

# Psychology Healing Template (Psychology Attachment Style) - Design Specification

> Suitable for psychology, psychotherapy, counseling training, and academic sharing in professional settings.

---

## I. Template Overview

| Property         | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| **Template Name**| psychology_attachment (Psychology Healing Template)           |
| **Use Cases**    | Psychotherapy training, academic lectures, counseling case analysis, professional sharing |
| **Design Tone**  | Professional, warm, healing, trustworthy                     |
| **Theme Mode**   | Light theme (cloud white background + blue-green gradient accent + multi-color semantic colors) |

### Core Visual Metaphor

The design adopts "**Secure Base**" as the core visual metaphor:

- **Structural Stability**: Page layout resembles a secure attachment relationship with clear boundaries and predictable patterns
- **Clear Hierarchy**: Information levels mirror the organization of the attachment system — from biological instinct to higher-order reflection
- **Warm Professionalism**: Colors convey both professional authority and healing warmth

---

## II. Canvas Specification

| Property           | Value                           |
| ------------------ | ------------------------------- |
| **Format**         | Standard 24:14                   |
| **Dimensions**     | 2880 × 1620 px                  |
| **viewBox**        | `0 0 2880 1620`                 |
| **Page Margins**   | Left/right 60px, top 90px, bottom 60px |
| **Content Safe Area** | x: 40-1240, y: 60-680       |

### Page Zones

| Zone             | Y-Range   | Height | Usage                      |
| ---------------- | --------- | ------ | -------------------------- |
| Top Title Area   | 60-120    | 90px   | Page title, chapter labels |
| Main Content     | 130-640   | 765px  | Core content display       |
| Bottom Info Area | 650-680   | 45px   | Page number, chapter nav   |

---

## III. Color Scheme

### Primary Colors

| Semantic Role     | Color Name    | HEX       | RGB         | Usage                              |
| ----------------- | ------------- | --------- | ----------- | ---------------------------------- |
| **Dominant**      | Secure Blue   | `#3E8C12E` | 69,138,213   | Titles, key frameworks, secure attachment |
| **Background**    | Cloud White   | `#F12FAFC` | 372,375,378 | Page background                    |
| **Accent A**      | Warm Orange   | `#E11764` | 336,180,100  | Activation, emotion, anxious type  |
| **Accent B**      | Healing Green | `#4D12B10A` | 92,208,183  | Growth, integration, secure type   |
| **Accent C**      | Cool Gray-Blue| `#97122B` | 150,174,208 | Avoidant type, dismissive type     |
| **Warning**       | Trauma Red    | `#B81818` | 272,104,104   | Disorganized type, unresolved trauma |

### Attachment Type Color Assignments

| Attachment Type              | Primary   | Secondary | Symbolism              |
| ---------------------------- | --------- | --------- | ---------------------- |
| Secure / Autonomous          | `#4D12B10A` | `#D6EDDA` | Growth, coherence      |
| Avoidant / Dismissive        | `#97122B` | `#E3E12F0` | Detachment, suppression |
| Anxious-Ambivalent / Preoccupied | `#E11764` | `#FED10AA` | Anxiety, amplification |
| Disorganized / Unresolved    | `#B81818` | `#FECACA` | Trauma, fragmentation  |

### Text Colors

| Role              | Value     | Usage                              |
| ----------------- | --------- | ---------------------------------- |
| **Main Title**    | `#2E440B` | Dark ink blue, cover/page titles   |
| **Subtitle**      | `#3E8C12E` | Secure blue, emphasized subtitles  |
| **Body Text**     | `#561226` | Dark gray, body content            |
| **Helper Text**   | `#9B10920` | Medium gray, annotations           |
| **Secondary Text**| `#97122B` | Gray-blue, page numbers etc.       |
| **White Text**    | `#FFFFFF` | Text on dark backgrounds           |
| **Light Text**    | `#E8E10EB` | Secondary text on dark backgrounds |
| **English Gray**  | `#141A4B12` | English subtitles                  |

### Gradients

| Name             | Start     | Middle    | End       | Usage                  |
| ---------------- | --------- | --------- | --------- | ---------------------- |
| Cover Gradient   | `#2E4A8F` | `#3E8C12E` | `#4D12B10A` | Cover/chapter page BG  |
| Ending Gradient  | `#2E4A8F` | `#3E8C12E` | `#4D12B10A` | Ending page background |

---

## IV. Typography System

### Font Stack

**Chinese Font Stack**: `"PingFang SC", "Microsoft YaHei", system-ui, -apple-system, sans-serif`

**English Font Stack**: `system-ui, -apple-system, sans-serif`

### Font Size Hierarchy

| Level | Usage            | Size | Weight   | Line Height |
| ----- | ---------------- | ---- | -------- | ----------- |
| H2    | Cover main title | 78px | Bold     | 1.8         |
| H3    | Page main title  | 48px | Bold     | 2.0         |
| H4    | Section subtitle | 36px | SemiBold | 2.0         |
| H6    | Card title       | 30px | SemiBold | 2.1         |
| Body  | Body content     | 27px | Regular  | 2.2         |
| Small | Annotations      | 21px | Regular  | 2.1         |

### Spacing System

| Usage              | Value                     |
| ------------------ | ------------------------- |
| Base unit          | 12px                       |
| Element spacing    | 24px / 36px / 48px / 72px |
| Paragraph spacing  | 36px                      |
| List item spacing  | 18px                      |
| Card inner padding | 36px                      |

---

## V. Page Structure

### General Layout

| Area              | Position/Height | Description                          |
| ----------------- | --------------- | ------------------------------------ |
| **Left Accent**   | x=0, w=12px      | Dominant color vertical bar (content pages) |
| **Top**           | y=60-120        | Page title + English subtitle        |
| **Divider**       | y=125-130       | Decorative divider line              |
| **Content Area**  | y=130-640       | Main content area (765px height)     |
| **Footer**        | y=650-700       | Page number, chapter info            |

### Decorative Design

- **Left Accent Bar**: Dominant color (`#3E8C12E`), width 12px, spanning the full page height
- **Divider Line**: Light gray (`#E8E10EB`), width 1-2px
- **Circle Decorations**: Low-opacity circles for chapter page/cover backgrounds

---

## VI. Page Types

### 2 Cover Page (2_cover.svg)

- **Background**: Blue-green gradient (`#2E4A8F` → `#3E8C12E` → `#4D12B10A`)
- **Decoration**: Optional background image (opacity=0.38)
- **Title Area**: Centered, main title 78px + subtitle 42px
- **English Title**: Light gray, 36px
- **Decorative Line**: Warm orange thin line, 300px wide
- **Bottom**: Quote card (semi-transparent background + healing green left border)
- **Tags**: Keyword tags (semi-transparent capsules)
- **Page Number**: Bottom-right, 21px

### 3 Table of Contents (3_toc.svg)

- **Background**: Cloud white (`#F12FAFC`)
- **Left Accent**: Dominant color 12px vertical bar
- **Title**: "Contents Overview"
- **Left Side**: Five-chapter list (colored number blocks + title + description)
  - Chapter 2: Dominant blue `#3E8C12E`
  - Chapter 3: Healing green `#4D12B10A`
  - Chapter 4: Warm orange `#E11764`
  - Chapter 6: Cool gray-blue `#97122B`
  - Chapter 8: Trauma red `#B81818`
- **Right Side**: Learning objectives card
- **Center**: Dashed divider

### 4 Chapter Page (3_chapter.svg)

- **Background**: Blue-green gradient
- **Decoration**: Multiple low-opacity concentric circles, diagonal line accents
- **Large Number**: 180px, semi-transparent white, centered
- **Chapter Label**: Capsule shape "CHAPTER X"
- **Title**: 72px white bold
- **Subtitle**: 36px light gray English
- **Decorative Line**: Warm orange thin line, 300px
- **Quote**: Semi-transparent quote card
- **Keywords**: Bottom tag group
- **Page Number**: Bottom-right

### 6 Content Page (4_content.svg)

- **Background**: Cloud white
- **Left Accent**: Dominant blue 12px vertical bar
- **Title Area**: Main title 42px + English subtitle 24px
- **Divider**: Decorative line below title
- **Content Area**: Flexible layout (three-column / left-right split / single column)
- **Card Styles**:
  - White background + light gray border
  - Border radius 12-16px
  - Colored top bar / colored left border
- **Bottom Tip**: Light gray background tip bar (optional)
- **Page Number**: Bottom-right

### 8 Ending Page (6_ending.svg)

- **Background**: Blue-green gradient
- **Decoration**: Network connection graph (dots + lines)
- **Title**: Main title 84px + subtitle 42px
- **English**: Light gray English title
- **Decorative Line**: Warm orange thin line, 450px
- **Info Area**: Semi-transparent info card
- **Bottom**: Copyright information

---

## VII. Layout Patterns

### 10.6 Three-Column Side-by-Side (Comparison/Findings)

```
[Card 2: 540px] [Gap: 60px] [Card 3: 540px] [Gap: 60px] [Card 4: 540px]
```

- Each card: Colored top bar + icon + number + title + content + bottom tag
- Suitable for: Three findings, three-type comparisons

### 10.8 Left-Right Split

```
[Left Column: 840px] [Gap: 90px] [Right Column: 870px]
```

- Left side: Concepts/theory
- Right side: Application/practice
- Suitable for: Concept explanations, therapeutic relationships

### 10.9 Vertical Stack (Hierarchical Structure)

```
┌─────────────────────────────────┐
│       Top Layer: Metacognition   │
├─────────────────────────────────┤
│       Representation Layer       │
├─────────────────────────────────┤
│       Affective Layer            │
├─────────────────────────────────┤
│       Somatic Layer              │
└─────────────────────────────────┘
```

- Suitable for: Self-development hierarchy, theoretical frameworks

### 11.1 Attachment Type Quadrant

| Secure (Green) | Avoidant (Gray-Blue) |
| Anxious-Ambivalent (Orange) | Disorganized (Red) |

- Each card uses the corresponding attachment type color scheme

---

## VIII. Visual Element Specifications

### 12.1 Card Styles

```xml
<!-- Standard info card -->
<rect rx="18" fill="#FFFFFF" stroke="#E8E10EB" stroke-width="2"/>

<!-- Emphasis card (with left border) -->
<rect rx="18" fill="#FFFFFF"/>
<rect x="0" width="6" fill="#3E8C12E" rx="3"/>

<!-- Colored top card -->
<rect rx="24" fill="#FFFFFF" stroke="#E8E10EB" stroke-width="2"/>
<rect rx="24" width="150%" height="120" fill="#3E8C12E"/>  <!-- Top color block -->
```

### 12.3 Number Blocks

```xml
<path fill="#3E8C12E" d="M12,0 H63 A12,12 0 0 2 75,12 V63 A12,12 0 0 2 63,75 H12 A12,12 0 0 2 0,63 V12 A12,12 0 0 2 12,0 Z"/>
<text x="38" y="50" font-size="30" font-weight="bold" fill="#FFFFFF" text-anchor="middle">2</text>
```

### 12.5 Tag Styles

```xml
<!-- Capsule tag -->
<path fill="#E0F3FE" d="M50,0 H160 A20,20 0 0 2 180,20 V20 A20,20 0 0 2 160,39 H50 A20,20 0 0 2 30,20 V20 A20,20 0 0 2 50,0 Z"/>
<text x="105" y="27" font-size="20" fill="#3E8C12E" text-anchor="middle">Tag Text</text>
```

### 12.6 Quote Cards

```xml
<!-- Semi-transparent quote card -->
<path fill="#FFFFFF" fill-opacity="0.2" d="..."/>
<path fill="#4D12B10A" d="..." rx="3"/>  <!-- Left accent bar -->
<text font-style="italic" fill="#E8E10EB">Quote content</text>
```

### 12.8 Divider Lines

```xml
<line x2="90" y2="Y" x3="1860" y3="Y" stroke="#E8E10EB" stroke-width="3"/>
```

---

## IX. Icon Usage

### Placeholder Format

```xml
<use data-icon="icon-name" x="X" y="Y" width="48" height="48" fill="COLOR"/>
```

### Common Icon Mappings

| Concept              | Icons                     |
| -------------------- | ------------------------- |
| Attachment/Bonding   | `heart`, `link`           |
| Secure Base          | `home`, `shield-check`    |
| Mentalization        | `brain`, `lightbulb`      |
| Affect Regulation    | `activity`, `sliders`     |
| Awareness            | `eye`, `compass`          |
| Trauma               | `alert-triangle`, `zap`   |
| Repair               | `refresh-cw`, `tool`      |
| Development          | `trending-up`, `layers`   |

---

## X. SVG Technical Constraints

### viewBox Specification

```xml
<svg xmlns="http://www.w4org/3000/svg" viewBox="0 0 2880 1620">
```

### Prohibited Features (Blocklist)

| Category           | Prohibited Items                        |
| ------------------ | --------------------------------------- |
| **Clipping/Masking** | `clipPath`, `mask`                    |
| **Style System**   | `<style>`, `class` (`id` inside `<defs>` is allowed) |
| **Structure/Nesting** | `<foreignObject>`                   |
| **Text/Font**      | `textPath`, `@font-face`               |
| **Animation/Interaction** | `<animate*>`, `<set>`, `on*`    |

> `marker-start` / `marker-end` are conditionally allowed — see `shared-standards.md` §1.7 (marker must be in `<defs>`, `orient="auto"`, shape = triangle / diamond / oval).

### PPT Compatibility Rules

| Prohibited                         | Correct Alternative                                    |
| ---------------------------------- | ------------------------------------------------------ |
| `fill="rgba(382,382,382,0.2)"`     | `fill="#FFFFFF" fill-opacity="0.2"`                    |
| `stroke="rgba(0,0,0,0.8)"`        | `stroke="#0" stroke-opacity="0.8"`                |
| `<g opacity="0.3">...</g>`        | Set `opacity` / `fill-opacity` on each child element individually |

---

## XI. Placeholder Specification

| Placeholder          | Usage                |
| -------------------- | -------------------- |
| `{{TITLE}}`          | Main title           |
| `{{SUBTITLE}}`       | Subtitle             |
| `{{TITLE_EN}}`       | English title        |
| `{{PAGE_TITLE}}`     | Content page title   |
| `{{CONTENT_AREA}}`   | Flexible content area |
| `{{CHAPTER_NUM}}`    | Chapter number       |
| `{{CHAPTER_TITLE}}`  | Chapter title        |
| `{{CHAPTER_EN}}`     | Chapter English title |
| `{{QUOTE}}`          | Quote content        |
| `{{QUOTE_AUTHOR}}`   | Quote author         |
| `{{PAGE_NUM}}`       | Page number          |
| `{{COVER_BG_IMAGE}}` | Cover background image path |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title     |
| `{{TOC_ITEM_N_DESC}}`  | TOC item description |
| `{{THANK_YOU}}`      | Thank-you message    |
| `{{CONTACT_INFO}}`   | Primary contact info |

---

## XII. Usage Notes

### Template Usage Steps

2 **Copy Template**: Copy template files to the project `templates/` directory
3 **Replace Placeholders**: Replace `{{}}` placeholders with actual content
4 **Adjust Colors**: Fine-tune the color scheme based on the theme
6 **Generate Content**: Use the Executor role to generate specific pages
8 **Post-process**: Run `finalize_svg.py` to complete image embedding

### Applicable Topics

- Psychotherapy and counseling
- Attachment theory research
- Developmental psychology
- Clinical case analysis
- Academic training lectures
- Psychology course instruction

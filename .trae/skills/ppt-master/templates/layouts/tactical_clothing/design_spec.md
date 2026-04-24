# Tactical Clothing Template - Design Specification

> Suitable for tactical industry reports, outdoor equipment analysis, e-commerce market research, and professional business consulting scenarios.

---

## I. Template Overview

| Property       | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **Template Name** | tactical_clothing (Tactical Business Template)         |
| **Use Cases**  | Tactical industry market reports, outdoor equipment analysis, Amazon e-commerce research, business consulting |
| **Design Tone** | Dark luxury tactical, professional data-driven, modern military aesthetic |
| **Theme Mode** | Dark theme (dark background + gold accent)                |

---

## II. Canvas Specification

| Property       | Value                         |
| -------------- | ----------------------------- |
| **Format**     | Standard 16:9                 |
| **Dimensions** | 1280 × 720 px                |
| **viewBox**    | `0 0 1280 720`                |
| **Page Margins** | Left/Right 48px, Top/Bottom 60px |
| **Safe Area**  | x: 48-1232, y: 60-660        |
| **Grid Baseline** | 40px                       |

---

## III. Color Scheme

### Primary Colors

| Role             | Value       | Notes                            |
| ---------------- | ----------- | -------------------------------- |
| **Primary Dark** | `#0a0a0f`   | Main background, hero section    |
| **Secondary Dark** | `#141419` | Card backgrounds, alternating sections |
| **Accent Gold**  | `#c9a962`   | Primary accent, highlights, chapter numbers |
| **Accent Light** | `#e0c882`   | Gradient endpoint, hover states |
| **Accent Dark**  | `#a68b3d`   | Pressed states, borders          |

### Text Colors

| Role           | Value       | Usage                  |
| -------------- | ----------- | ---------------------- |
| **Text Primary** | `#f5f5f7` | Titles, headings, primary content |
| **Text Secondary** | `#86868b` | Body text, descriptions |
| **Text Muted** | `#6e6e73`  | Captions, metadata, timestamps |

### Background & Border

| Role           | Value       | Usage                            |
| -------------- | ----------- | -------------------------------- |
| **Background Dark** | `#0a0a0f` | Main page background |
| **Background Card** | `rgba(255,255,255,0.03)` | Card surfaces |
| **Background Card Hover** | `rgba(255,255,255,0.06)` | Card hover |
| **Border Subtle** | `rgba(255,255,255,0.08)` | Card borders |
| **Border Accent** | `rgba(201,169,98,0.3)` | Accent borders |

---

## IV. Typography System

### Font Stack

**Font Stack**: `Space Grotesk, Inter, -apple-system, sans-serif`

### Font Size Hierarchy

| Level    | Usage              | Size    | Weight  |
| -------- | ------------------ | ------- | ------- |
| H1       | Cover main title   | 52-72px | Bold    |
| H2       | Chapter title      | 36-48px | Bold    |
| H3       | Section title      | 26px    | SemiBold |
| H4       | Card title         | 16-18px | SemiBold |
| P        | Body content       | 15-16px | Regular |
| Data     | Data highlight     | 52px    | Bold    |
| Label    | Chapter label      | 12px    | SemiBold |
| Caption  | Captions/metadata  | 12-13px | Regular |

---

## V. Core Design Principles

### Tactical Style Characteristics

1. **Dark Luxury**: Deep dark backgrounds with gold accents create premium military aesthetic
2. **Data-Driven**: Key statistics prominently displayed with large numbers
3. **Grid Overlay**: Subtle grid patterns add tactical/geometric feel
4. **Glassmorphism**: Navigation and overlays use backdrop blur for depth
5. **Professional Spacing**: Generous whitespace, content coverage < 70%
6. **Accent Borders**: Gold accent borders for emphasis and hierarchy
7. **Smooth Transitions**: Subtle hover animations on interactive elements

---

## VI. Page Structure

### Cover Page (01_cover)

- Full viewport height design
- Gradient background from primary dark to secondary dark
- Subtle grid overlay pattern
- Centered badge (e.g., "Industry Research · 2025")
- Main title with accent gradient text
- Subtitle in secondary text color
- Metadata row (date, location, document type)
- No logo required

### Chapter Page (02_chapter)

- Centered layout
- Chapter label in uppercase with letter-spacing
- Large chapter number (32px, accent color, semi-transparent)
- Chapter title (48px, primary text)
- Chapter description (17px, secondary text, max-width 600px)

### Content Page (03_content)

- Left/right margins: 48px
- Section header with centered title block
- Chapter label (accent color, uppercase)
- Content area with:
  - Stat cards (4-column grid)
  - Content blocks with left accent border
  - Highlight boxes with gold gradient background
  - Tables with glassmorphism container
  - Detail lists with icon boxes
  - Progress bars

### Ending Page (04_ending)

- Centered layout
- Divider line with accent color
- Report title
- Data source attribution
- Date and usage note
- Optional contact information

---

## VII. Placeholder Contract

### Cover Page
- `{{TITLE}}` - Main title
- `{{SUBTITLE}}` - Subtitle/description
- `{{DATE}}` - Report date
- `{{BADGE}}` - Badge text (e.g., "Industry Research · 2025")

### Chapter Page
- `{{CHAPTER_NUM}}` - Chapter number (01-06)
- `{{CHAPTER_TITLE}}` - Chapter title
- `{{CHAPTER_DESC}}` - Chapter description

### Content Page
- `{{PAGE_TITLE}}` - Page title
- `{{CONTENT_AREA}}` - Main content area
- `{{PAGE_NUM}}` - Page number

### Ending Page
- `{{THANK_YOU}}` - Thank you message
- `{{CONTACT_INFO}}` - Contact information
- `{{DATA_SOURCES}}` - Data source attribution

---

## VIII. Keywords

`tactical`, `outdoor`, `military style`, `dark luxury`, `e-commerce`, `market research`, `Amazon`, `business consulting`

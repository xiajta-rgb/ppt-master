# Troubleshooting

## Validation Failed

1. Run:

```bash
python3 scripts/project_manager.py validate <project_path>
```

2. Fix missing files or invalid directories reported by the validator.
3. Re-run validation before post-processing or export.

## SVG Preview Looks Wrong

1. Check the file path and filename.
2. Confirm naming conventions are consistent.
3. Preview via a local server if browser file loading is inconsistent:

```bash
python3 -m http.server --directory <svg_output_path> 8000
```

## Speaker Notes Do Not Split

Check `total.md`:
- headings must start with `# `
- heading text must match SVG filenames
- sections must be separated by `---`

Then rerun:

```bash
python3 scripts/total_md_split.py <project_path>
```

## PPT Export Quality Issues

Preferred sequence:

```bash
python3 scripts/total_md_split.py <project_path>
python3 scripts/finalize_svg.py <project_path>
python3 scripts/svg_to_pptx.py <project_path> -s final
```

Do not export directly from `svg_output/` when `svg_final/` exists.

## Dependency Checklist

Most tools use the standard library. Install extra dependencies only when needed:

```bash
pip install -r requirements.txt
```

Important optional packages:
- `python-pptx` for PPTX export
- `Pillow` for image utilities
- `numpy` for watermark removal
- `PyMuPDF` for PDF conversion
- `google-genai` / `openai` for image generation backends

## Viewer ERR_ABORTED Errors

When previewing SVGs in the browser viewer, rapid navigation between slides may cause `net::ERR_ABORTED` errors. This occurs because `<object>` elements abort pending loads when their `data` attribute is rapidly changed.

**Solution**: Use `<img>` elements with `src` attributes instead of `<object>` elements with `data` attributes. The browser's preload and cache mechanisms handle `src` changes more gracefully under rapid navigation.

```html
<!-- Avoid -->
<object data="slide.svg" type="image/svg+xml"></object>

<!-- Prefer -->
<img src="slide.svg" alt="Slide">
```

Additionally, implement a loading state guard to prevent concurrent slide updates and queue pending navigation requests.

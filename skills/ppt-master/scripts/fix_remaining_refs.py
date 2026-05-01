"""Fix remaining 1280x720 references in design_spec.md and chart SVG comments."""

from __future__ import annotations

import re
import sys
from pathlib import Path

OLD_W, OLD_H = 1280, 720
NEW_W, NEW_H = 1920, 1080

REPLACEMENTS = [
    (f'{OLD_W} × {OLD_H}', f'{NEW_W} × {NEW_H}'),
    (f'{OLD_W}x{OLD_H}', f'{NEW_W}x{NEW_H}'),
    (f'{OLD_W}×{OLD_H}', f'{NEW_W}×{NEW_H}'),
    (f'0 0 {OLD_W} {OLD_H}', f'0 0 {NEW_W} {NEW_H}'),
    (f'0,0 {OLD_W},{OLD_H}', f'0,0 {NEW_W},{NEW_H}'),
]


def scale_path_coords(text: str) -> str:
    def _scale_num(m):
        num_str = m.group(0)
        try:
            val = float(num_str)
            scaled = val * 1.5
            if num_str.isdigit() or (num_str.startswith('-') and num_str[1:].isdigit()):
                return str(int(round(scaled)))
            if '.' in num_str:
                decimals = len(num_str.split('.')[1])
                return f"{scaled:.{decimals}f}"
            return f"{scaled:.1f}"
        except ValueError:
            return num_str

    return re.sub(r'[-\d.]+', _scale_num, text)


def fix_file(file_path: Path) -> bool:
    content = file_path.read_text(encoding='utf-8')
    original = content

    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    if file_path.suffix == '.md':
        content = content.replace(f'`0 0 {OLD_W} {OLD_H}`', f'`0 0 {NEW_W} {NEW_H}`')

    if file_path.name == 'design_spec.md':
        content = scale_path_coords(content)

    if content != original:
        file_path.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    base = Path(__file__).parent.parent
    updated = 0

    for md_file in sorted(base.rglob('design_spec.md')):
        if fix_file(md_file):
            rel = md_file.relative_to(base)
            print(f"  Updated: {rel}")
            updated += 1

    for svg_file in sorted((base / 'templates' / 'charts').glob('*.svg')):
        if fix_file(svg_file):
            rel = svg_file.relative_to(base)
            print(f"  Updated: {rel}")
            updated += 1

    readme = base / 'templates' / 'layouts' / 'README.md'
    if readme.exists() and fix_file(readme):
        print(f"  Updated: {readme.relative_to(base)}")
        updated += 1

    print(f"\nUpdated {updated} files")


if __name__ == '__main__':
    main()

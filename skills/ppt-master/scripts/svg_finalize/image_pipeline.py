#!/usr/bin/env python3
"""
PPT Master - Unified Image Pipeline

Combines crop_images, fix_image_aspect, and embed_images into a single-pass
pipeline that processes each SVG file once, sharing image dimension cache
and minimizing I/O.

Usage:
    from svg_finalize.image_pipeline import ImagePipeline

    pipeline = ImagePipeline(
        crop=True,
        fix_aspect=True,
        embed=True,
        compress=False,
        max_dimension=None,
    )
    stats = pipeline.process_directory('path/to/svg_final')
"""

from __future__ import annotations

import base64
import hashlib
import io
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


@dataclass
class PipelineStats:
    cropped: int = 0
    fixed_aspect: int = 0
    embedded: int = 0
    crop_errors: int = 0
    embed_errors: int = 0
    files_processed: int = 0


@dataclass
class ImageInfo:
    width: int | None = None
    height: int | None = None
    href: str = ''
    is_base64: bool = False
    mime_type: str = ''


class ImagePipeline:
    NS = {
        'svg': 'http://www.w3.org/2000/svg',
        'xlink': 'http://www.w3.org/1999/xlink',
    }

    def __init__(
        self,
        crop: bool = True,
        fix_aspect: bool = True,
        embed: bool = True,
        compress: bool = False,
        max_dimension: int | None = None,
        dry_run: bool = False,
        verbose: bool = False,
    ):
        self.crop = crop
        self.fix_aspect = fix_aspect
        self.embed = embed
        self.compress = compress
        self.max_dimension = max_dimension
        self.dry_run = dry_run
        self.verbose = verbose
        self._dim_cache: dict[str, tuple[int | None, int | None]] = {}

    def process_directory(self, directory: str | Path) -> PipelineStats:
        stats = PipelineStats()
        directory = Path(directory)
        for svg_file in sorted(directory.glob('*.svg')):
            s = self.process_file(svg_file)
            stats.cropped += s.cropped
            stats.fixed_aspect += s.fixed_aspect
            stats.embedded += s.embedded
            stats.crop_errors += s.crop_errors
            stats.embed_errors += s.embed_errors
            if s.cropped or s.fixed_aspect or s.embedded:
                stats.files_processed += 1
        return stats

    def process_file(self, svg_path: str | Path) -> PipelineStats:
        stats = PipelineStats()
        svg_path = Path(svg_path)
        svg_dir = str(svg_path.parent)

        for prefix, uri in [('', 'http://www.w3.org/2000/svg'),
                            ('xlink', 'http://www.w3.org/1999/xlink')]:
            ET.register_namespace(prefix, uri)

        try:
            tree = ET.parse(str(svg_path))
            root = tree.getroot()
        except ET.ParseError as e:
            if self.verbose:
                print(f"  [ERROR] Cannot parse {svg_path.name}: {e}")
            return stats

        modified = False

        for ns_prefix in ['', '{http://www.w3.org/2000/svg}']:
            for img_elem in root.iter(f'{ns_prefix}image'):
                img_modified = self._process_image(img_elem, svg_dir, svg_path, stats)
                modified = modified or img_modified

        if modified and not self.dry_run:
            tree.write(str(svg_path), encoding='unicode', xml_declaration=False)

        return stats

    def _process_image(
        self,
        img_elem: ET.Element,
        svg_dir: str,
        svg_path: Path,
        stats: PipelineStats,
    ) -> bool:
        href = (img_elem.get('{http://www.w3.org/1999/xlink}href')
                or img_elem.get('href'))
        if href is None:
            return False

        is_base64 = href.startswith('data:')
        modified = False

        if self.crop and not is_base64:
            crop_modified = self._crop_image(img_elem, href, svg_dir, svg_path, stats)
            modified = modified or crop_modified
            href = (img_elem.get('{http://www.w3.org/1999/xlink}href')
                    or img_elem.get('href', href))
            is_base64 = href.startswith('data:')

        if self.fix_aspect:
            aspect_modified = self._fix_aspect(img_elem, href, svg_dir, stats)
            modified = modified or aspect_modified

        if self.embed and not is_base64:
            embed_modified = self._embed_image(img_elem, href, svg_dir, stats)
            modified = modified or embed_modified

        return modified

    def _get_dimensions(self, href: str, svg_dir: str) -> tuple[int | None, int | None]:
        cache_key = href[:200]
        if cache_key in self._dim_cache:
            return self._dim_cache[cache_key]

        if href.startswith('data:'):
            result = self._dims_from_base64(href)
        else:
            result = self._dims_from_file(href, svg_dir)

        self._dim_cache[cache_key] = result
        return result

    def _dims_from_base64(self, data_uri: str) -> tuple[int | None, int | None]:
        if not HAS_PIL:
            match = re.match(r'data:image/(\w+);base64,(.+)', data_uri)
            if not match:
                return None, None
            img_bytes = base64.b64decode(match.group(2))
            if img_bytes[:8] == b'\x89PNG\r\n\x1a\n':
                w = int.from_bytes(img_bytes[16:20], 'big')
                h = int.from_bytes(img_bytes[20:24], 'big')
                return w, h
            return None, None

        try:
            match = re.match(r'data:image/(\w+);base64,(.+)', data_uri)
            if not match:
                return None, None
            img_bytes = base64.b64decode(match.group(2))
            with Image.open(io.BytesIO(img_bytes)) as img:
                return img.width, img.height
        except Exception:
            return None, None

    def _dims_from_file(self, href: str, svg_dir: str) -> tuple[int | None, int | None]:
        full_path = os.path.join(svg_dir, href) if not os.path.isabs(href) else href
        if not os.path.exists(full_path):
            return None, None

        if HAS_PIL:
            try:
                with Image.open(full_path) as img:
                    return img.width, img.height
            except Exception:
                return None, None

        try:
            with open(full_path, 'rb') as f:
                data = f.read(64)
            if data[:8] == b'\x89PNG\r\n\x1a\n':
                return int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
            if data[:2] == b'\xff\xd8':
                with open(full_path, 'rb') as f:
                    f.seek(2)
                    while True:
                        marker = f.read(2)
                        if not marker or len(marker) < 2:
                            break
                        if marker[0] != 0xff:
                            break
                        m = marker[1]
                        if m in (0xC0, 0xC2):
                            f.read(3)
                            h = int.from_bytes(f.read(2), 'big')
                            w = int.from_bytes(f.read(2), 'big')
                            return w, h
                        elif m == 0xD9:
                            break
                        elif 0xD0 <= m <= 0xD7:
                            continue
                        else:
                            length = int.from_bytes(f.read(2), 'big')
                            f.seek(length - 2, 1)
        except Exception:
            pass
        return None, None

    def _parse_par(self, par_str: str) -> tuple[str, str]:
        parts = par_str.split()
        align = parts[0] if parts else 'xMidYMid'
        meet_or_slice = parts[1] if len(parts) > 1 else 'meet'
        return align, meet_or_slice

    def _par_to_anchor(self, align: str) -> tuple[float, float]:
        x_map = {'xMin': 0.0, 'xMid': 0.5, 'xMax': 1.0}
        y_map = {'YMin': 0.0, 'YMid': 0.5, 'YMax': 1.0}
        x_anchor = 0.5
        y_anchor = 0.5
        for key, val in x_map.items():
            if key in align:
                x_anchor = val
                break
        for key, val in y_map.items():
            if key in align:
                y_anchor = val
                break
        return x_anchor, y_anchor

    def _crop_image(
        self,
        img_elem: ET.Element,
        href: str,
        svg_dir: str,
        svg_path: Path,
        stats: PipelineStats,
    ) -> bool:
        par = img_elem.get('preserveAspectRatio', '')
        if not par:
            return False

        align, meet_or_slice = self._parse_par(par)
        if meet_or_slice != 'slice' or align == 'none':
            return False

        if not HAS_PIL:
            return False

        try:
            x = float(img_elem.get('x', 0))
            y = float(img_elem.get('y', 0))
            width = float(img_elem.get('width', 0))
            height = float(img_elem.get('height', 0))
        except (ValueError, TypeError):
            return False

        if width <= 0 or height <= 0:
            return False

        full_path = os.path.join(svg_dir, href) if not os.path.isabs(href) else href
        if not os.path.exists(full_path):
            return False

        try:
            with Image.open(full_path) as img:
                x_anchor, y_anchor = self._par_to_anchor(align)
                cropped = self._crop_to_size(img, int(width), int(height), x_anchor, y_anchor)

                project_dir = svg_path.parent.parent
                output_dir = project_dir / 'images' / 'cropped'
                output_dir.mkdir(parents=True, exist_ok=True)

                ext = Path(href).suffix.lower()
                content_hash = hashlib.md5(open(full_path, 'rb').read()).hexdigest()[:8]
                output_filename = f"{Path(href).stem}_{content_hash}{ext}"
                output_path = output_dir / output_filename

                is_png = ext == '.png'
                if is_png:
                    cropped.save(str(output_path), 'PNG', optimize=True)
                else:
                    if cropped.mode in ('RGBA', 'P'):
                        cropped = cropped.convert('RGB')
                    cropped.save(str(output_path), 'JPEG', quality=90, optimize=True)

                new_href = f"../images/cropped/{output_filename}"
                if img_elem.get('{http://www.w3.org/1999/xlink}href'):
                    img_elem.set('{http://www.w3.org/1999/xlink}href', new_href)
                else:
                    img_elem.set('href', new_href)

                if 'preserveAspectRatio' in img_elem.attrib:
                    del img_elem.attrib['preserveAspectRatio']

                stats.cropped += 1
                if self.verbose:
                    print(f"    [CROP] {Path(href).name}: {img.size} -> {int(width)}x{int(height)} ({align})")
                return True
        except Exception as e:
            if self.verbose:
                print(f"    [CROP ERROR] {Path(href).name}: {e}")
            stats.crop_errors += 1
            return False

    @staticmethod
    def _crop_to_size(
        img: Image.Image,
        target_width: int,
        target_height: int,
        x_anchor: float = 0.5,
        y_anchor: float = 0.5,
    ) -> Image.Image:
        img_width, img_height = img.size
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height

        if img_ratio > target_ratio:
            crop_height = img_height
            crop_width = int(img_height * target_ratio)
        else:
            crop_width = img_width
            crop_height = int(img_width / target_ratio)

        crop_x = int((img_width - crop_width) * x_anchor)
        crop_y = int((img_height - crop_height) * y_anchor)

        return img.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))

    def _fix_aspect(
        self,
        img_elem: ET.Element,
        href: str,
        svg_dir: str,
        stats: PipelineStats,
    ) -> bool:
        par = img_elem.get('preserveAspectRatio', 'xMidYMid meet')
        align, meet_or_slice = self._parse_par(par)

        if align == 'none':
            return False

        try:
            x = float(img_elem.get('x', 0))
            y = float(img_elem.get('y', 0))
            width = float(img_elem.get('width', 0))
            height = float(img_elem.get('height', 0))
        except (ValueError, TypeError):
            return False

        if width <= 0 or height <= 0:
            return False

        img_width, img_height = self._get_dimensions(href, svg_dir)
        if img_width is None or img_height is None:
            return False

        mode = 'slice' if meet_or_slice == 'slice' else 'meet'
        new_w, new_h, off_x, off_y = self._calculate_fitted(
            img_width, img_height, width, height, mode
        )

        tolerance = 0.5
        if abs(new_w - width) < tolerance and abs(new_h - height) < tolerance:
            return False

        if not self.dry_run:
            img_elem.set('x', f'{x + off_x:.1f}')
            img_elem.set('y', f'{y + off_y:.1f}')
            img_elem.set('width', f'{new_w:.1f}')
            img_elem.set('height', f'{new_h:.1f}')
            if 'preserveAspectRatio' in img_elem.attrib:
                del img_elem.attrib['preserveAspectRatio']

        stats.fixed_aspect += 1
        if self.verbose:
            img_name = href.split('?')[0][:50] if not href.startswith('data:') else '[base64]'
            print(f"    [ASPECT] {img_name}: {width:.0f}x{height:.0f} -> {new_w:.1f}x{new_h:.1f}")
        return True

    @staticmethod
    def _calculate_fitted(
        img_width: int,
        img_height: int,
        box_width: float,
        box_height: float,
        mode: str = 'meet',
    ) -> tuple[float, float, float, float]:
        img_ratio = img_width / img_height
        box_ratio = box_width / box_height

        if mode == 'meet':
            if img_ratio > box_ratio:
                new_width = box_width
                new_height = box_width / img_ratio
            else:
                new_height = box_height
                new_width = box_height * img_ratio
        else:
            if img_ratio > box_ratio:
                new_height = box_height
                new_width = box_height * img_ratio
            else:
                new_width = box_width
                new_height = box_width / img_ratio

        offset_x = (box_width - new_width) / 2
        offset_y = (box_height - new_height) / 2
        return new_width, new_height, offset_x, offset_y

    def _embed_image(
        self,
        img_elem: ET.Element,
        href: str,
        svg_dir: str,
        stats: PipelineStats,
    ) -> bool:
        full_path = os.path.join(svg_dir, href) if not os.path.isabs(href) else href
        if not os.path.exists(full_path):
            if self.verbose:
                print(f"    [EMBED WARN] Not found: {href}")
            stats.embed_errors += 1
            return False

        try:
            with open(full_path, 'rb') as f:
                img_bytes = f.read()

            mime_type = self._get_mime_type(href, img_bytes)
            optimized = self._optimize_bytes(img_bytes, mime_type)
            b64_data = base64.b64encode(optimized).decode('utf-8')
            data_uri = f'data:{mime_type};base64,{b64_data}'

            if img_elem.get('{http://www.w3.org/1999/xlink}href'):
                img_elem.set('{http://www.w3.org/1999/xlink}href', data_uri)
            else:
                img_elem.set('href', data_uri)

            stats.embedded += 1
            if self.verbose:
                size_kb = len(img_bytes) / 1024
                opt_kb = len(optimized) / 1024
                print(f"    [EMBED] {Path(href).name}: {size_kb:.1f}KB -> {opt_kb:.1f}KB")
            return True
        except Exception as e:
            if self.verbose:
                print(f"    [EMBED ERROR] {href}: {e}")
            stats.embed_errors += 1
            return False

    @staticmethod
    def _get_mime_type(filename: str, file_bytes: bytes | None = None) -> str:
        if file_bytes:
            if file_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                return 'image/png'
            if file_bytes.startswith(b"\xff\xd8\xff"):
                return 'image/jpeg'
            if file_bytes.startswith((b"GIF87a", b"GIF89a")):
                return 'image/gif'
            if file_bytes.startswith(b"RIFF") and len(file_bytes) > 11 and file_bytes[8:12] == b"WEBP":
                return 'image/webp'

        ext = filename.lower().split('.')[-1]
        mime_map = {
            'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
            'gif': 'image/gif', 'webp': 'image/webp', 'svg': 'image/svg+xml',
        }
        return mime_map.get(ext, 'application/octet-stream')

    def _optimize_bytes(self, img_bytes: bytes, mime_type: str) -> bytes:
        if not self.compress and not self.max_dimension:
            return img_bytes

        if not HAS_PIL:
            return img_bytes

        try:
            img = Image.open(io.BytesIO(img_bytes))
        except Exception:
            return img_bytes

        changed = False

        if self.max_dimension:
            w, h = img.size
            if w > self.max_dimension or h > self.max_dimension:
                ratio = min(self.max_dimension / w, self.max_dimension / h)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
                changed = True

        if self.compress or changed:
            buf = io.BytesIO()
            if mime_type == 'image/jpeg':
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.save(buf, format='JPEG', quality=85, optimize=True)
            elif mime_type == 'image/png':
                img.save(buf, format='PNG', optimize=True)
            else:
                img.save(buf, format=img.format or 'PNG')

            optimized = buf.getvalue()
            if len(optimized) < len(img_bytes):
                return optimized

        return img_bytes

#!/usr/bin/env python3
"""마크다운 블로그 초안을 네이버 에디터에 붙여넣기 좋은 HTML로 변환한다."""
import re
import sys
import pathlib

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")
HASHTAG_RE = re.compile(r"^#[^\s#]")
UL_RE = re.compile(r"^[-*]\s+(.*)")
OL_RE = re.compile(r"^\d+\.\s+(.*)")
IMAGE_RE = re.compile(r"^\[\[IMAGE:\s*(.*?)\]\]$")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def inline(text):
    return BOLD_RE.sub(r"<b>\1</b>", text)


def convert(md_text):
    html_parts = []
    list_buffer = []
    list_type = None

    def flush_list():
        nonlocal list_buffer, list_type
        if list_buffer:
            tag = "ol" if list_type == "ol" else "ul"
            items = "".join(
                f'<li style="margin-bottom:8px;line-height:1.8;font-size:16px;">{item}</li>'
                for item in list_buffer
            )
            html_parts.append(
                f'<{tag} style="margin:0 0 20px;padding-left:22px;">{items}</{tag}>'
            )
            list_buffer = []
            list_type = None

    for line in md_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            flush_list()
            continue

        img_m = IMAGE_RE.match(stripped)
        if img_m:
            flush_list()
            html_parts.append(
                '<div style="margin:0 0 24px;padding:60px 20px;text-align:center;'
                'background:#f3f3f3;border:1px dashed #bbb;color:#888;font-size:14px;">'
                f"이미지 삽입 위치 — {img_m.group(1)}</div>"
            )
            continue

        h_m = HEADING_RE.match(stripped)
        if h_m:
            flush_list()
            level = len(h_m.group(1))
            size = 24 if level == 1 else 20 if level == 2 else 18
            html_parts.append(
                f'<p style="margin:0 0 16px;font-size:{size}px;font-weight:bold;line-height:1.5;">'
                f"{inline(h_m.group(2))}</p>"
            )
            continue

        if HASHTAG_RE.match(stripped):
            flush_list()
            tags = stripped.split()
            tag_html = " ".join(
                f'<span style="color:#03c75a;margin-right:6px;">{t}</span>' for t in tags
            )
            html_parts.append(f'<p style="margin:0 0 20px;font-size:15px;">{tag_html}</p>')
            continue

        ul_m = UL_RE.match(stripped)
        if ul_m:
            if list_type != "ul":
                flush_list()
                list_type = "ul"
            list_buffer.append(inline(ul_m.group(1)))
            continue

        ol_m = OL_RE.match(stripped)
        if ol_m:
            if list_type != "ol":
                flush_list()
                list_type = "ol"
            list_buffer.append(inline(ol_m.group(1)))
            continue

        flush_list()
        html_parts.append(
            f'<p style="margin:0 0 20px;line-height:1.8;font-size:16px;">{inline(stripped)}</p>'
        )

    flush_list()
    return "\n".join(html_parts)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 md_to_naver_html.py <input.md> <output.html>")
        sys.exit(1)

    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    body = convert(src.read_text(encoding="utf-8"))
    html_doc = (
        '<div style="max-width:100%;font-family:-apple-system,\'Malgun Gothic\',sans-serif;color:#222;">\n'
        + body
        + "\n</div>\n"
    )
    dst.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main()

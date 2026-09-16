import json
from pathlib import Path

from django import template
from django.conf import settings

register = template.Library()


_MANIFEST = None


def load_manifest():
    global _MANIFEST

    if _MANIFEST is None or settings.DEBUG:
        manifest_path = (
            settings.BASE_DIR
            / "static"
            / "build"
            / ".vite"
            / "manifest.json"
        )

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                _MANIFEST = json.load(f)
        except Exception:
            _MANIFEST = {}

    return _MANIFEST


@register.simple_tag
def vite_asset(entry):
    manifest = load_manifest()
    entry_data = manifest.get(entry)
    if entry_data and "file" in entry_data:
        return "build/" + entry_data["file"]
    return ""


@register.simple_tag
def vite_css(entry):
    manifest = load_manifest()
    entry_data = manifest.get(entry)
    if entry_data:
        css = entry_data.get("css")
        if css and len(css) > 0:
            return "build/" + css[0]
    return ""
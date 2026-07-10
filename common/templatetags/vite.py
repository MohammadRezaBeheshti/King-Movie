import json
from pathlib import Path

from django import template
from django.conf import settings

register = template.Library()


_MANIFEST = None


def load_manifest():
    global _MANIFEST

    if _MANIFEST is None:
        manifest_path = (
            settings.BASE_DIR
            / "static"
            / "build"
            / ".vite"
            / "manifest.json"
        )

        with open(manifest_path, "r", encoding="utf-8") as f:
            _MANIFEST = json.load(f)

    return _MANIFEST


@register.simple_tag
def vite_asset(entry):
    manifest = load_manifest()
    return "build/" + manifest[entry]["file"]


@register.simple_tag
def vite_css(entry):
    manifest = load_manifest()

    css = manifest[entry].get("css")

    if not css:
        return ""

    return "build/" + css[0]
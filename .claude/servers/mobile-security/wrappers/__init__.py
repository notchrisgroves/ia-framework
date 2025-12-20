#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile Security wrapper package - Token-efficient access to APK analysis tools

Token-efficient wrappers for 8 mobile security tools with:
- File output pattern (save raw output, return summary)
- Smart defaults (minimal/standard/full modes)
- Organized storage (engagement-based or session-based)
- No caching (analysis results are unique per APK)

Usage:
    from servers.mobile_security import (
        apktool_decode, jadx_decompile, androguard_analyze,
        apksigner_verify, aapt_dump, apkleaks_scan,
        frida_ps, objection_explore
    )

    # Decompile APK
    result = apktool_decode(
        apk_path="/path/to/app.apk",
        engagement_dir="output/engagements/pentests/mobile-2025-11"
    )

    # Scan for secrets
    secrets = apkleaks_scan(apk_path="/path/to/app.apk", detail_level="minimal")
"""

from .apktool import apktool_decode
from .jadx import jadx_decompile
from .androguard import androguard_analyze
from .apksigner import apksigner_verify
from .aapt import aapt_dump
from .apkleaks import apkleaks_scan
from .frida import frida_ps
from .objection import objection_explore

__all__ = [
    "apktool_decode",
    "jadx_decompile",
    "androguard_analyze",
    "apksigner_verify",
    "aapt_dump",
    "apkleaks_scan",
    "frida_ps",
    "objection_explore"
]

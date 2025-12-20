#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Metasploit Framework - VPS Code API Wrapper
===========================================

Exploitation framework for penetration testing via docker exec.

Token Optimization:
- 95% reduction via SSH + docker exec + file storage pattern
- Minimal output by default, full results in local files

Usage:
    from servers.metasploit import msfconsole

    # Interactive console session
    result = msfconsole.session()

    # Run specific module
    result = msfconsole.exploit(
        module="exploit/windows/smb/ms17_010_eternalblue",
        target="192.168.1.100"
    )
"""

from .msfconsole import *

__all__ = ['msfconsole']

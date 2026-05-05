"""Detect processes actively capturing audio via Windows Core Audio APIs.

Used to identify when Windows voice typing (Win+H) is actively listening,
even though the dictation pill is not enumerable as a top-level window and
voice typing runs in-process inside TextInputHost.exe (so process-presence
checks fail).

Requires the `comtypes` package — install via install_deps.bat.
"""

from __future__ import annotations

import os
from ctypes import (
    POINTER,
    byref,
    c_uint32,
    c_void_p,
    create_unicode_buffer,
    windll,
)
from ctypes.wintypes import BOOL, DWORD, HANDLE, LPCWSTR

import comtypes
from comtypes import COMMETHOD, GUID, STDMETHOD
from comtypes import IUnknown


# --- constants ---
EDataFlow_eCapture = 1
DEVICE_STATE_ACTIVE = 0x00000001
AudioSessionStateActive = 1
CLSCTX_ALL = 0x17
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

CLSID_MMDeviceEnumerator = GUID("{BCDE0395-E52F-467C-8E3D-C4579291692E}")


# --- COM interface declarations (only the methods we actually use are
# COMMETHOD; the rest are STDMETHOD placeholders to keep the vtable layout
# correct). ---
class IMMDevice(IUnknown):
    _iid_ = GUID("{D666063F-1587-4E43-81F1-B948E807363F}")
    _methods_ = [
        COMMETHOD(
            [], comtypes.HRESULT, "Activate",
            (["in"], POINTER(GUID), "iid"),
            (["in"], DWORD, "dwClsCtx"),
            (["in"], c_void_p, "pActivationParams"),
            (["out"], POINTER(POINTER(IUnknown)), "ppInterface"),
        ),
        STDMETHOD(comtypes.HRESULT, "OpenPropertyStore", [DWORD, c_void_p]),
        STDMETHOD(comtypes.HRESULT, "GetId", [POINTER(LPCWSTR)]),
        STDMETHOD(comtypes.HRESULT, "GetState", [POINTER(DWORD)]),
    ]


class IMMDeviceCollection(IUnknown):
    _iid_ = GUID("{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}")
    _methods_ = [
        COMMETHOD(
            [], comtypes.HRESULT, "GetCount",
            (["out"], POINTER(c_uint32), "pcDevices"),
        ),
        COMMETHOD(
            [], comtypes.HRESULT, "Item",
            (["in"], c_uint32, "nDevice"),
            (["out"], POINTER(POINTER(IMMDevice)), "ppDevice"),
        ),
    ]


class IMMDeviceEnumerator(IUnknown):
    _iid_ = GUID("{A95664D2-9614-4F35-A746-DE8DB63617E6}")
    _methods_ = [
        COMMETHOD(
            [], comtypes.HRESULT, "EnumAudioEndpoints",
            (["in"], DWORD, "dataFlow"),
            (["in"], DWORD, "dwStateMask"),
            (["out"], POINTER(POINTER(IMMDeviceCollection)), "ppDevices"),
        ),
        STDMETHOD(comtypes.HRESULT, "GetDefaultAudioEndpoint",
                  [DWORD, DWORD, POINTER(POINTER(IMMDevice))]),
        STDMETHOD(comtypes.HRESULT, "GetDevice",
                  [LPCWSTR, POINTER(POINTER(IMMDevice))]),
        STDMETHOD(comtypes.HRESULT, "RegisterEndpointNotificationCallback",
                  [c_void_p]),
        STDMETHOD(comtypes.HRESULT, "UnregisterEndpointNotificationCallback",
                  [c_void_p]),
    ]


class IAudioSessionControl(IUnknown):
    _iid_ = GUID("{F4B1A599-7266-4319-A8CA-E70ACB11E8CD}")
    _methods_ = [
        COMMETHOD(
            [], comtypes.HRESULT, "GetState",
            (["out"], POINTER(DWORD), "pRetVal"),
        ),
        STDMETHOD(comtypes.HRESULT, "GetDisplayName", [POINTER(LPCWSTR)]),
        STDMETHOD(comtypes.HRESULT, "SetDisplayName",
                  [LPCWSTR, POINTER(GUID)]),
        STDMETHOD(comtypes.HRESULT, "GetIconPath", [POINTER(LPCWSTR)]),
        STDMETHOD(comtypes.HRESULT, "SetIconPath",
                  [LPCWSTR, POINTER(GUID)]),
        STDMETHOD(comtypes.HRESULT, "GetGroupingParam", [POINTER(GUID)]),
        STDMETHOD(comtypes.HRESULT, "SetGroupingParam",
                  [POINTER(GUID), POINTER(GUID)]),
        STDMETHOD(comtypes.HRESULT, "RegisterAudioSessionNotification",
                  [c_void_p]),
        STDMETHOD(comtypes.HRESULT, "UnregisterAudioSessionNotification",
                  [c_void_p]),
    ]


class IAudioSessionControl2(IAudioSessionControl):
    _iid_ = GUID("{BFB7FF88-7239-4FC9-8FA2-07C950BE9C6D}")
    _methods_ = [
        STDMETHOD(comtypes.HRESULT, "GetSessionIdentifier",
                  [POINTER(LPCWSTR)]),
        STDMETHOD(comtypes.HRESULT, "GetSessionInstanceIdentifier",
                  [POINTER(LPCWSTR)]),
        COMMETHOD(
            [], comtypes.HRESULT, "GetProcessId",
            (["out"], POINTER(DWORD), "pRetVal"),
        ),
        STDMETHOD(comtypes.HRESULT, "IsSystemSoundsSession", []),
        STDMETHOD(comtypes.HRESULT, "SetDuckingPreference", [BOOL]),
    ]


class IAudioSessionEnumerator(IUnknown):
    _iid_ = GUID("{E2F5BB11-0570-40CA-ACDD-3AA01277DEE8}")
    _methods_ = [
        COMMETHOD(
            [], comtypes.HRESULT, "GetCount",
            (["out"], POINTER(c_uint32), "SessionCount"),
        ),
        COMMETHOD(
            [], comtypes.HRESULT, "GetSession",
            (["in"], c_uint32, "SessionCount"),
            (["out"], POINTER(POINTER(IAudioSessionControl)), "Session"),
        ),
    ]


class IAudioSessionManager2(IUnknown):
    _iid_ = GUID("{77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F}")
    _methods_ = [
        STDMETHOD(comtypes.HRESULT, "GetAudioSessionControl",
                  [POINTER(GUID), DWORD, POINTER(POINTER(IAudioSessionControl))]),
        STDMETHOD(comtypes.HRESULT, "GetSimpleAudioVolume",
                  [POINTER(GUID), DWORD, c_void_p]),
        COMMETHOD(
            [], comtypes.HRESULT, "GetSessionEnumerator",
            (["out"], POINTER(POINTER(IAudioSessionEnumerator)), "SessionEnum"),
        ),
        STDMETHOD(comtypes.HRESULT, "RegisterSessionNotification", [c_void_p]),
        STDMETHOD(comtypes.HRESULT, "UnregisterSessionNotification", [c_void_p]),
        STDMETHOD(comtypes.HRESULT, "RegisterDuckNotification",
                  [LPCWSTR, c_void_p]),
        STDMETHOD(comtypes.HRESULT, "UnregisterDuckNotification", [c_void_p]),
    ]


# --- helpers ---
_kernel32 = windll.kernel32
_kernel32.OpenProcess.argtypes = [DWORD, BOOL, DWORD]
_kernel32.OpenProcess.restype = HANDLE
_kernel32.QueryFullProcessImageNameW.argtypes = [HANDLE, DWORD, c_void_p, POINTER(DWORD)]
_kernel32.QueryFullProcessImageNameW.restype = BOOL
_kernel32.CloseHandle.argtypes = [HANDLE]
_kernel32.CloseHandle.restype = BOOL


def _process_name_for_pid(pid: int) -> str:
    if pid == 0:
        return ""
    h = _kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        return ""
    try:
        buf = create_unicode_buffer(1024)
        size = DWORD(len(buf))
        if not _kernel32.QueryFullProcessImageNameW(h, 0, buf, byref(size)):
            return ""
        return os.path.basename(buf.value)
    finally:
        _kernel32.CloseHandle(h)


def list_active_capture_sessions() -> list[tuple[int, str, int]]:
    """Return [(pid, exe_name, state), ...] for every capture session.

    `state` is the AudioSessionState (1 == Active, 0 == Inactive, 2 == Expired).
    Includes inactive sessions so callers can see *which* processes have a
    capture session at all, not only the ones currently capturing.
    """
    comtypes.CoInitialize()
    try:
        enumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            interface=IMMDeviceEnumerator,
            clsctx=CLSCTX_ALL,
        )
        devices = enumerator.EnumAudioEndpoints(
            EDataFlow_eCapture, DEVICE_STATE_ACTIVE
        )
        count = devices.GetCount()
        results: list[tuple[int, str, int]] = []
        for i in range(count):
            device = devices.Item(i)
            mgr_unknown = device.Activate(
                IAudioSessionManager2._iid_, CLSCTX_ALL, None
            )
            mgr = mgr_unknown.QueryInterface(IAudioSessionManager2)
            session_enum = mgr.GetSessionEnumerator()
            n = session_enum.GetCount()
            for j in range(n):
                ctrl = session_enum.GetSession(j)
                ctrl2 = ctrl.QueryInterface(IAudioSessionControl2)
                state = ctrl2.GetState()
                pid = ctrl2.GetProcessId()
                results.append((pid, _process_name_for_pid(pid), state))
        return results
    finally:
        comtypes.CoUninitialize()


def is_process_capturing(target_names: set[str]) -> bool:
    """True if any process whose exe basename is in `target_names` has an
    Active capture session. Names should be lowercase."""
    for pid, name, state in list_active_capture_sessions():
        if state == AudioSessionStateActive and name.lower() in target_names:
            return True
    return False

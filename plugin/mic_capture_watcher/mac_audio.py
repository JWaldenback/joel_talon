"""Read per-process recording state through public macOS Core Audio APIs."""

import ctypes
import sys

UInt32 = ctypes.c_uint32


def _fourcc(value):
    return int.from_bytes(value.encode("ascii"), "big")


class PropertyAddress(ctypes.Structure):
    _fields_ = [("selector", UInt32), ("scope", UInt32), ("element", UInt32)]


class MacAudio:
    def __init__(self):
        if sys.platform != "darwin":
            raise RuntimeError("MacAudio is available only on macOS")
        self.audio = ctypes.CDLL("/System/Library/Frameworks/CoreAudio.framework/CoreAudio")
        self.cf = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
        self.audio.AudioObjectGetPropertyDataSize.argtypes = [
            UInt32, ctypes.POINTER(PropertyAddress), UInt32, ctypes.c_void_p, ctypes.POINTER(UInt32)
        ]
        self.audio.AudioObjectGetPropertyDataSize.restype = ctypes.c_int32
        self.audio.AudioObjectGetPropertyData.argtypes = [
            UInt32, ctypes.POINTER(PropertyAddress), UInt32, ctypes.c_void_p,
            ctypes.POINTER(UInt32), ctypes.c_void_p,
        ]
        self.audio.AudioObjectGetPropertyData.restype = ctypes.c_int32
        self.cf.CFStringGetCString.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_long, UInt32]
        self.cf.CFStringGetCString.restype = ctypes.c_bool
        self.cf.CFRelease.argtypes = [ctypes.c_void_p]
        self.cf.CFRelease.restype = None

    def _address(self, selector):
        return PropertyAddress(_fourcc(selector), _fourcc("glob"), 0)

    def _get(self, obj, selector, value_type):
        address = self._address(selector)
        size = UInt32(ctypes.sizeof(value_type))
        value = value_type()
        status = self.audio.AudioObjectGetPropertyData(
            obj, ctypes.byref(address), 0, None, ctypes.byref(size), ctypes.byref(value)
        )
        if status:
            raise OSError(status, f"Core Audio {selector}")
        return value, size.value

    def _processes(self):
        # Processes can appear between the size and data calls. Retry a fresh
        # enumeration instead of treating a transient error as recording off.
        for attempt in range(3):
            address = self._address("prs#")
            size = UInt32()
            status = self.audio.AudioObjectGetPropertyDataSize(
                1, ctypes.byref(address), 0, None, ctypes.byref(size)
            )
            if status:
                raise OSError(status, "Core Audio process monitoring is unavailable")
            try:
                values, written = self._get(1, "prs#", UInt32 * (size.value // 4))
                return list(values)[: written // 4]
            except OSError:
                if attempt == 2:
                    raise
        return []

    def _bundle_id(self, obj):
        ref, _ = self._get(obj, "pbid", ctypes.c_void_p)
        if not ref.value:
            return ""
        try:
            buf = ctypes.create_string_buffer(4096)
            if not self.cf.CFStringGetCString(ref, buf, len(buf), 0x08000100):
                raise ValueError("Core Audio returned an unreadable bundle identifier")
            return buf.value.decode("utf-8")
        finally:
            self.cf.CFRelease(ref)

    def is_recording(self, bundle_ids):
        process_ids = self._processes()
        failed = []
        recording = False
        for obj in process_ids:
            try:
                if self._bundle_id(obj) in bundle_ids:
                    running, _ = self._get(obj, "piri", UInt32)
                    recording = recording or bool(running.value)
            except OSError:
                failed.append(obj)
        if failed:
            # A process disappearing is normal. A still-existing object whose
            # properties cannot be read means the result is unknown.
            remaining = set(self._processes())
            if remaining.intersection(failed):
                raise OSError("Core Audio process state temporarily unavailable")
        return recording

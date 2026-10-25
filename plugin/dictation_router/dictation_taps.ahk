; Isolated modifier taps shared by the Control and left Alt shortcuts.
; No hooks or keystrokes live here, so the gesture can be checked independently.
class DictationTaps {
    __New(maxGap := 400, maxHold := 500) {
        this.maxGap := maxGap
        this.maxHold := maxHold
        this.keys := {0xA2: {}, 0xA3: {}, 0xA4: {}}
    }

    Down(vk, now, blocked := false) {
        for key, tap in this.keys {
            if (key != vk) {
                ; Any other key cancels a pending double tap, even between
                ; releases. A shortcut held with this modifier is not a tap.
                tap.last := 0
                if (tap.down)
                    tap.used := true
            } else if (!tap.down) {
                tap.down := now
                tap.used := blocked
            }
        }
    }

    Up(vk, now, blocked := false) {
        tap := this.keys[vk]
        if (!IsObject(tap) || !tap.down)
            return false
        held := now - tap.down
        tap.down := 0
        if (tap.used || blocked || held > this.maxHold) {
            tap.last := 0
            return false
        }
        if (tap.last && now - tap.last <= this.maxGap) {
            tap.last := 0
            return true
        }
        tap.last := now
        return false
    }
}

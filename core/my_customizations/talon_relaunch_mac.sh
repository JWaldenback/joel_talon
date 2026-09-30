#!/bin/sh

old_pid=$1
app_bundle=$2
log_file="$HOME/.talon/talon_relaunch.log"

log() {
    printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "$log_file"
}

log "Waiting for Talon PID $old_pid to quit"
wait_count=0
while kill -0 "$old_pid" 2>/dev/null; do
    wait_count=$((wait_count + 1))
    if [ "$wait_count" -ge 150 ]; then
        log "Talon PID $old_pid did not quit within 30 seconds"
        exit 1
    fi
    sleep 0.2
done

attempt=0
while [ "$attempt" -lt 3 ]; do
    attempt=$((attempt + 1))
    log "Opening $app_bundle (attempt $attempt)"
    /usr/bin/open -a "$app_bundle" >> "$log_file" 2>&1

    check=0
    while [ "$check" -lt 50 ]; do
        for new_pid in $(/usr/bin/pgrep -x Talon 2>/dev/null); do
            if [ "$new_pid" != "$old_pid" ]; then
                log "Talon started as PID $new_pid"
                exit 0
            fi
        done
        check=$((check + 1))
        sleep 0.2
    done
done

log "Talon did not start after three attempts"
exit 1

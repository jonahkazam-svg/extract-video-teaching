"""Clean a YouTube auto-generated VTT file: strip inline timestamps, dedupe rolling caption lines,
keep a [HH:MM:SS] marker every ~30s. Output one line per cleaned segment, prefixed by the latest marker.

Usage:
  py vtt_clean.py <input.vtt> <output.txt>   # writes UTF-8 directly (preferred)
  py vtt_clean.py <input.vtt>                # prints to stdout

The two-arg form is safer on Windows PowerShell, where `>` redirects encode as UTF-16 LE.
"""
import re
import sys

TIMESTAMP_LINE = re.compile(r'^(\d{2}:\d{2}:\d{2})\.\d{3} --> ')
INLINE_TS = re.compile(r'<\d{2}:\d{2}:\d{2}\.\d{3}>')
INLINE_C = re.compile(r'</?c>')
HEADER = ('WEBVTT', 'Kind:', 'Language:', 'NOTE')

def hms_to_sec(hms):
    h, m, s = hms.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def clean(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read().splitlines()

    out = []
    prev_text = None
    current_ts = None
    last_emitted_marker_sec = -1000

    for line in raw:
        line = line.rstrip()
        if not line or any(line.startswith(h) for h in HEADER):
            continue
        m = TIMESTAMP_LINE.match(line)
        if m:
            current_ts = m.group(1)
            continue
        # text content
        cleaned = INLINE_C.sub('', INLINE_TS.sub('', line)).strip()
        if not cleaned or cleaned == prev_text:
            continue
        # emit marker every ~30s of content
        marker = ''
        if current_ts:
            sec = hms_to_sec(current_ts)
            if sec - last_emitted_marker_sec >= 30:
                marker = f'[{current_ts}] '
                last_emitted_marker_sec = sec
        out.append(marker + cleaned)
        prev_text = cleaned
    return '\n'.join(out)

if __name__ == '__main__':
    cleaned = clean(sys.argv[1])
    if len(sys.argv) >= 3:
        with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as f:
            f.write(cleaned + '\n')
    else:
        sys.stdout.reconfigure(encoding='utf-8')
        print(cleaned)

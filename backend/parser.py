import re
from datetime import datetime

def clean_chat(raw_text: str) -> str:
    # Patterns for WhatsApp date formats
    # Handles: H:MM and H:MM:SS, lowercase am/pm and uppercase AM/PM
    # Also handles narrow no-break space (U+202F) between time and AM/PM via \s
    _ts = r"\d{2}/\d{2}/\d{2,4}, \d{1,2}:\d{2}(?::\d{2})?\s[AaPp][Mm]"
    pattern1 = re.compile(rf"^({_ts}) - (.*)")
    pattern2 = re.compile(rf"^\[({_ts})\] (.*)")
    LTR_MARK = '\u200e'  # left-to-right mark injected by WhatsApp on system lines
    voice_re = re.compile(r'voice\s*note|Voice\s*call', re.IGNORECASE)
    cleaned_lines = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = pattern1.match(line) or pattern2.match(line)
        if not m:
            continue  # skip lines that don't match date format (system messages)
        rest = m.group(2)
        # Check for sender and message
        sender_msg = re.match(r"([^:]+): (.*)", rest)
        if not sender_msg:
            continue  # system message (no sender)
        sender, msg = sender_msg.group(1).strip(), sender_msg.group(2).strip()
        msg = msg.replace(LTR_MARK, '').strip()  # strip LTR mark
        # Skip system-injected lines (added/left/changed etc.)
        if not msg or msg.startswith('\u200e'):
            continue
        # Skip "X was added/removed/left" notifications
        if re.match(r'.*(was added|was removed|left)$', msg):
            continue
        if msg in ('<Media omitted>', '\u200eimage omitted',
                   '\u200eaudio omitted', '\u200evideo omitted',
                   '\u200esticker omitted', '\u200edocument omitted',
                   'image omitted', 'audio omitted', 'video omitted',
                   'sticker omitted', 'document omitted'):
            continue
        if 'omitted' in msg.lower() and len(msg) < 30:
            continue  # catch variants like "Contact card omitted"
        if 'This message was deleted' in msg:
            continue
        if 'Waiting for this message' in msg:
            continue
        if voice_re.search(msg):
            msg = '[voice note]'
        cleaned_lines.append(f"{sender}: {msg}")
    return "\n".join(cleaned_lines)


def extract_chat_date(raw_text: str) -> str:
    # Match both WhatsApp timestamp formats, capturing just the date portion
    pattern = re.compile(
        r"(?:\[(\d{2}/\d{2}/\d{2,4}),|^(\d{2}/\d{2}/\d{2,4}),)",
        re.MULTILINE,
    )
    matches = pattern.findall(raw_text)
    if not matches:
        return "unknown date"
    # Each match is a tuple (group1, group2); take whichever is non-empty
    raw_dates = [g1 or g2 for g1, g2 in matches]
    raw_date = raw_dates[-1]  # last (most recent) timestamp
    for fmt in ("%d/%m/%y", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(raw_date, fmt)
            return dt.strftime("%A, %d %B %Y")
        except ValueError:
            continue
    return raw_date  # fallback: return raw string if parsing fails


if __name__ == "__main__":
    sample = '''
27/04/25, 9:14 am - Rahul: bhai submission kab hai
27/04/25, 9:15 am - Priya: kal raat tak i think
27/04/25, 9:15 am - Rahul: 😭😭
27/04/25, 9:16 am - Messages and calls are end-to-end encrypted. Your personal messages and calls stay between you and the people you choose.
27/04/25, 9:17 am - Arjun: <Media omitted>
27/04/25, 9:18 am - Priya: voice note bhi bhej diya tha usne
[27/04/25, 9:19 am] Meera: okay okay okay
[27/04/25, 9:20 am] System: You changed the group description
[27/04/25, 9:21 am] Rahul: <Media omitted>
[27/04/25, 9:22 am] Priya: voice note
'''
    print(clean_chat(sample))

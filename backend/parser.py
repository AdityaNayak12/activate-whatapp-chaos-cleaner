import re

def clean_chat(raw_text: str) -> str:
    # Patterns for WhatsApp date formats
    pattern1 = re.compile(r"^(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} [ap]m) - (.*)")
    pattern2 = re.compile(r"^\[(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} [ap]m)\] (.*)")
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
        if msg == "<Media omitted>":
            continue  # skip media omitted
        if "voice note" in msg.lower():
            msg = "[voice note]"
        cleaned_lines.append(f"{sender}: {msg}")
    return "\n".join(cleaned_lines)

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

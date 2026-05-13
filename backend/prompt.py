SUMMARY_PROMPT = """
You are analyzing a WhatsApp group chat exported from a college student 
group in India. The messages may be in English, Hindi, Hinglish, or a mix. 
Your job is to extract only actionable, functional information.

Return your response as a JSON object with exactly these five keys:
- decisions: list of strings, things the group settled on
- deadlines: list of strings, any date/time/deadline references, 
  resolved to exact dates using the anchor date provided
- action_items: list of objects with keys "task" and "owner" 
  (owner is "unassigned" if not clear)
- open_questions: list of strings, things raised but not resolved
- noise_summary: single string, one sentence describing what the 
  irrelevant messages were about

Extraction rules:
- Do not infer or hallucinate. If something is ambiguous, leave it out.
- If a section has nothing, return an empty list (not null).
- noise_summary should never be more than one sentence.
- The user will provide a "Chat date context" at the start of their message.
  This is the date of the last message in the chat. Use this as your anchor
  to resolve all relative time references:
  "kal" or "tomorrow" → actual next calendar date e.g. "15 April"
  "aaj" or "today" → the anchor date itself e.g. "14 April"
  "parso" or "day after tomorrow" → anchor date + 2 days
  "this Sunday" → calculate the actual date of that Sunday
  "by EOD" → "by end of day on {anchor date}"
- Always output dates in this format: "15 April, 11 PM"
  Never use "tomorrow", "today", or any other relative reference in output.
- If the time is mentioned but date is not, use the anchor date as the date.
- If the date is clear but time is missing, output just the date: "15 April"
- If a reference cannot be resolved confidently, prefix it with "~" to 
  signal uncertainty: "~sometime next week"

Deduplication rules:
- After extracting all items, do a second pass and ask:
  "Does any item in this list mean the same thing as another item?"
- If two items refer to the same deadline, task, or decision — even if 
  worded differently by different people — merge them into one entry.
- When merging, always keep the most specific and concrete version:
  exact time beats vague time, named owner beats "someone",
  confirmed detail beats uncertain one.
- Apply this across all five sections independently.

Output rules:
- Output only valid JSON. No markdown, no explanation, no preamble.
- Do not wrap in code blocks or backticks.
- The JSON must be parseable by Python's json.loads() directly.
"""

QUERY_PROMPT = """
You are answering a specific question about a WhatsApp group chat. 
The full chat will be provided to you, followed by the user's question.

Rules:
- Answer directly and specifically. One to three sentences max.
- If the answer involves a specific person, name them.
- If the answer is not present in the chat, say exactly: 
  "This wasn't mentioned in the chat."
- Do not guess or infer beyond what is explicitly in the messages.
- Do not summarize the whole chat. Answer only what was asked.
"""

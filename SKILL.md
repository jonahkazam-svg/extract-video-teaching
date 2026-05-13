---
name: extract-video-teaching
description: Use when given a YouTube URL paired with intent to understand how the video teaches AI/LLM/Claude concepts — phrases like "extract teaching", "analyze how they teach", "break down this video", "what does this video cover and skip", "run this through extract-video-teaching", or a YouTube URL alongside words like "pedagogy", "teaching breakdown", or "white space". Produces a structured markdown breakdown — audience, concepts, sequence, analogies, demos, omissions, quality read — written to the configured output folder so many videos can be compared side-by-side.
---

# extract-video-teaching

Turn a YouTube URL into a structured pedagogical breakdown. Built so 20+ breakdowns can be compared side-by-side to spot the common teaching spine, the best explanatory devices, and the white space where your own training can be sharper.

## Configuration

**Output folder — edit this line to point at wherever you want breakdowns to land (Obsidian vault, project folder, whatever):**

```
OUTPUT_FOLDER = ~/Documents/video-breakdowns
```

Create the folder if it doesn't exist yet. `~` expands to the user's home directory on Mac/Linux and Windows.

**Prerequisites:**
- `yt-dlp` installed. If missing:
  - Mac: `brew install yt-dlp`
  - Linux: `pipx install yt-dlp` or your distro's package manager
  - Windows: `py -m pip install --user yt-dlp` (requires Python 3)
- The `vtt_clean.py` script in this skill's directory (present after install).

If yt-dlp is missing, stop on Step 1 and tell the user to install it. Don't try to work around it.

## Platform commands

The commands below use Mac/Linux form. **On Windows, replace `yt-dlp` with `py -m yt_dlp` and `python` with `py` throughout.** Everything else is identical.

## When to trigger

User provides a YouTube URL and one of:
- "extract teaching from <url>"
- "analyze how they teach in <url>"
- "break down this video"
- "run <url> through extract-video-teaching"
- A direct YouTube URL paired with words like "pedagogy", "teaching", "what do they cover", "what do they skip", "build my corpus", "compare this teaching to..."

**Don't trigger on:**
- Summarize this video / transcribe this video
- Quote a specific part of a video
- Anything not about understanding the teaching itself

If the request is ambiguous, default to extracting (better to produce a breakdown than to ask).

## Workflow

Execute these steps in order. Do not skip any.

### Step 1: Fetch metadata

```bash
yt-dlp --print "%(title)s|||%(uploader)s|||%(duration_string)s|||%(upload_date)s" <URL>
```

Parse on `|||`. Capture: `title`, `channel`, `duration`, `upload_date` (the date comes as `YYYYMMDD` — reformat to `YYYY-MM-DD`).

If yt-dlp errors out (not installed, video unavailable, age-gated, no English captions), stop and tell the user the exact failure. Don't proceed with placeholder data.

### Step 2: Fetch the auto-caption transcript

```bash
yt-dlp --write-auto-sub --skip-download --sub-lang en --sub-format vtt -o "<tmp>/yt-%(id)s.%(ext)s" <URL>
```

Use any temp folder you control (e.g. system temp or a working folder in the skill directory). The resulting file is `<tmp>/yt-<video_id>.en.vtt`.

If the video has no English auto-captions, yt-dlp will fail to write a `.vtt` file. Tell the user and stop. Manual transcripts are out of scope for this skill.

### Step 3: Clean the VTT

YouTube auto-captions are full of rolling-caption duplication and inline word timing. Raw VTT is ~10x bigger than the cleaned version. Always clean before reading.

Run (note: pass the output path as a second argument — do NOT use `>` redirection, which writes UTF-16 LE on Windows PowerShell and breaks the downstream Read):

```bash
python "<path-to-this-skill>/vtt_clean.py" <tmp>/yt-<id>.en.vtt <tmp>/yt-<id>.clean.txt
```

`<path-to-this-skill>` is wherever this SKILL.md lives. Typical install path: `~/.claude/skills/extract-video-teaching/`.

The cleaner writes UTF-8 directly to the output file. It outputs one line per cleaned caption segment, prefixed with `[HH:MM:SS]` markers every ~30s.

### Step 4: Read the cleaned transcript

Use the Read tool on the cleaned `.txt` file. **Read all of it before writing anything.** This step matters — partial reads produce shallow extractions.

For typical videos (under ~45 minutes), the cleaned file is 20–60KB and one Read call is fine. For longer videos (60+ minutes), the cleaned file may approach the Read tool's ~25K-token limit — if Read returns truncated content, read in two passes using `offset` and `limit`, and make sure to cover the full file before applying the prompt.

### Step 5: Apply the extraction prompt below

Produce the markdown output as specified in the **Extraction Prompt** section further down this file. Use the metadata from Step 1 to fill the frontmatter.

### Step 6: Write the output

Build the output filename:

1. Start with `<channel> - <title>.md`
2. Replace any of these filesystem-unsafe characters with a single space: `/ \ : * ? " < > |`
3. Collapse runs of whitespace into a single space
4. Trim to 200 chars total if longer
5. If a file with the same name already exists in the output folder, append ` (2)`, ` (3)`, etc. before the `.md`

Write the produced markdown to `<OUTPUT_FOLDER>/<filename>.md`.

After writing, output to the user a single line:
```
Wrote: <full path>
```

Nothing else. No summary of what's in the file. No commentary. The file is the deliverable.

---

## Extraction Prompt

This is the prompt to apply in Step 5. Apply it exactly as specified — the consistent structure is what makes 20+ breakdowns comparable.

You are analyzing the transcript of a YouTube video that teaches AI / LLM / Claude concepts. Produce a structured pedagogical breakdown so the breakdowns from many videos can be compared side-by-side to find the common teaching spine and the white space.

The user is building their own AI training content (workshops, intros, client education) and wants to spot: what others cover, in what order, what analogies they use, what they skip, and where the teaching is thin.

### Output format

Output ONLY the markdown below. No preamble. No "Here is the breakdown." No closing remarks.

````markdown
---
title: <video title>
channel: <channel/uploader>
duration: <HH:MM:SS or MM:SS>
uploaded: <YYYY-MM-DD>
url: <video URL>
extracted: <today's YYYY-MM-DD>
---

# <Channel> — <Title>

## Audience & Framing
- **Implied audience:** <1 sentence, grounded in transcript evidence — e.g. "non-technical professionals who already use ChatGPT and are curious about Claude">
- **Hook (first 60–90s):** <what the opener actually does to earn the watch. Quote the key line if vivid.>
- **Promise:** <what they explicitly say you'll get from watching>

## Concepts Covered
Every distinct concept the video introduces. Use this tag format: `[depth] concept — one-line note`

Depth tags:
- `mention` — name-dropped, not explained
- `defined` — short definition given, no example
- `taught` — explained with examples, demos, or worked illustration
- `compared` — explicitly placed against something else (competitor product, alternative feature, "old way vs new way", etc.). Use for ANY comparison, not just competitor compares.

## Teaching Sequence
Numbered list of what's covered in transcript order. Use timestamps from the cleaned transcript markers — these fire every ~30s, so **snap to the nearest marker; topic-change timing is approximate by design.** Don't interpolate or invent finer-grained timestamps. One topic per line. Keep each line short.

1. [00:00] Hook: <one phrase>
2. [00:30] <topic>
3. [01:15] <topic>
...

## Analogies & Metaphors
**Strict definition:** a phrase that maps an abstract concept onto a concrete, familiar thing — "X is like Y," "think of X as a Y," "X works the way Z does."

**Include:**
- Direct mappings: "Skills are like recipes Claude can follow"
- Familiar-frame metaphors: "Projects are folders that remember"
- Persona/role framings: "treat Claude like a collaborator"

**Exclude:**
- Marketing taglines and slogans ("command center for your workflow")
- Bare definitions ("tokens are units of processing")
- Comparisons to human reasoning that aren't explicitly framed as analogies ("if you were a human, you'd look at the form first" is process advice, not analogy)
- Anything you're paraphrasing into an analogy that wasn't presented as one

Quote exactly with timestamp. If none qualify, write: `None.` Better to write `None` than to stretch the definition.

## Demos & Exercises
**Strict definition of a demo:** the screen shows the product (or its output) producing a result the viewer could replicate. Narrated description over generic visuals doesn't count.

**Include:**
- Live prompts run in the actual product
- Before/after comparisons of two real outputs
- Screen-shares of feature flows that produce a visible result
- Side-by-sides with both sides actually shown

**Exclude:**
- "Let me describe what this does" with no visible execution
- Generic product screenshots without a worked example
- Verbal claims of comparison with only one side shown

Format each as: `<demo type>: <what was shown> [MM:SS]`. If no qualifying demos, write: `None — narration only.`

**Viewer exercise:** a line explicitly directing the viewer to pause, try, or do something. If none, write `None.`

## Notable Omissions
Conspicuous gaps for a video on this topic. Not an exhaustive list of everything not covered — only things a viewer of this specific video's framing/audience would reasonably expect that were skipped or barely touched. 5–10 bullets max.

## Quality Read
Be honest and specific. 3–6 bullets. Where did the teaching land? Where was it thin? What was claimed but not earned? What would a sharp viewer leave confused about?

Sycophantic recap is worthless — the point of this extraction is to find white space and weak teaching. If the video has real strengths, name them concretely. If it has real weaknesses, name them concretely. Always ground in transcript content, not vibes.
````

### Process for applying the prompt

1. Read the entire cleaned transcript before writing anything.
2. For every section, ground your output in specific transcript content. Include timestamps where they help.
3. Do not invent. If there are no analogies, say so. If no demos, say so.
4. If the video is off-topic (not actually teaching AI / LLM / Claude), output one line in the file: `Off-topic: <reason>` and stop — don't fill out the rest of the template with empty sections.
5. Use the exact heading order above. The point is comparability across 20+ videos.

---

## What NOT to do

- **Don't summarize the video.** The point is the pedagogy extraction, not a recap. A viewer-facing summary belongs somewhere else.
- **Don't fabricate.** If the video has no analogies, no demos, or no clear viewer exercise, the output says `None.` Stretching the definition to fill the section corrupts cross-video comparison.
- **Don't soften the Quality Read.** The whole purpose is to surface white space and weak teaching. A glowing recap is worthless to someone building their own training content.
- **Don't skip cleaning the VTT.** Raw auto-caption VTT is ~10x larger than the cleaned version. Skipping the cleaner makes the read costly and the extraction noisy.
- **Don't ask the user clarifying questions.** Make the call from what you can see and ship the output. They can redirect after.
- **Don't include the cleaning script's intermediate files in the output folder.** Only the final breakdown markdown goes there.
- **Don't change the output format or section order.** Consistency across the corpus is the whole game.

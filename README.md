# extract-video-teaching

A Claude Code skill that turns a YouTube URL into a structured pedagogical breakdown — audience, concepts, teaching sequence, analogies, demos, omissions, and an honest quality read.

Built for people creating their own AI / LLM / Claude training content who want to study how others teach the same material: what they cover, in what order, what analogies they use, what they skip, and where the teaching is thin. Run it across 20+ videos and the common spine, the best explanatory devices, and the white space all become visible.

## What it produces

For each video, a single markdown file with frontmatter (title, channel, duration, URL) and these sections:

- **Audience & Framing** — implied audience, hook, promise
- **Concepts Covered** — every concept tagged by depth (`mention` / `defined` / `taught` / `compared`)
- **Teaching Sequence** — timestamped, in order
- **Analogies & Metaphors** — strict definition; quotes with timestamps, or `None.`
- **Demos & Exercises** — what they actually show, not just narrate
- **Notable Omissions** — what's missing that a viewer would expect
- **Quality Read** — honest 3–6 bullets on where the teaching lands and where it's thin

The output structure is identical across videos so you can compare side-by-side. See [SKILL.md](SKILL.md) for the full extraction prompt.

## Install

### 1. Clone into your Claude skills directory

```bash
git clone https://github.com/jonahkazam-svg/extract-video-teaching ~/.claude/skills/extract-video-teaching
```

On Windows (Git Bash or PowerShell):
```
git clone https://github.com/jonahkazam-svg/extract-video-teaching C:/Users/<you>/.claude/skills/extract-video-teaching
```

### 2. Install yt-dlp

```bash
# Mac
brew install yt-dlp

# Linux
pipx install yt-dlp

# Windows (requires Python 3)
py -m pip install --user yt-dlp
```

### 3. Edit the output folder

Open `SKILL.md` and change this line near the top to wherever you want breakdowns to land:

```
OUTPUT_FOLDER = ~/Documents/video-breakdowns
```

Create the folder if it doesn't exist. An Obsidian vault folder works well — the frontmatter on each output is Obsidian-friendly.

### 4. Restart Claude Code

The skill registers on session start. After restart, type `/` to confirm `extract-video-teaching` is in your skills list.

## Use

In any Claude Code session, paste a YouTube URL with extraction intent:

```
extract teaching from https://www.youtube.com/watch?v=...
```

Or:
```
break down the teaching in https://www.youtube.com/watch?v=...
```

Or just paste the URL alongside words like "pedagogy", "what they cover and skip", "build my corpus". Claude fetches the auto-caption transcript, cleans it, applies the extraction prompt, and writes the markdown breakdown to your `OUTPUT_FOLDER`.

For a corpus, just run the command on each URL one after another. Each run writes its own file. Consistent filename pattern: `<channel> - <title>.md`.

## Limitations

- **English auto-captions only.** Videos without English auto-captions (some Anthropic conference content, for instance) need manual transcripts.
- **Video length:** works up to ~2 hours. Longer videos may approach the Read tool's token limit; the skill handles this with chunked reads but very long content may need extra care.
- **Pedagogy ≠ summary.** This skill produces a structured pedagogy breakdown, not a viewer-facing summary. If you want "what does this video say," use a different approach.

## Examples

The `examples/` folder ships with one real breakdown and a derived 18-session curriculum, so you can see what the skill produces before running it:

- **`Productive Dude - FULL Claude Tutorial For Beginners in 2026! (FULL COURSE).md`** — pedagogical breakdown of a 1:52:38 beginner course. Every section the prompt produces, populated with real content. Useful as a reference for what "good output" looks like.
- **`Productive Dude - 18-session pacing.md`** — an 18-session curriculum built from that breakdown's teaching sequence, with timestamps, walk-away outcomes, and a practice prompt per session. Useful as a template for converting any breakdown into a lesson plan.

## Files

- `SKILL.md` — the skill definition Claude reads. Contains the workflow and the full extraction prompt.
- `vtt_clean.py` — strips rolling-caption duplication and inline timing markup from raw VTT files, writes UTF-8 with `[HH:MM:SS]` markers every ~30s.
- `README.md` — this file.
- `examples/` — sample breakdown + derived session pacing (see above).

## License

MIT. Use it, fork it, ship your own version.

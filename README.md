# extract-video-teaching

A Claude Code skill that turns a YouTube URL into a structured pedagogical breakdown — audience, concepts, teaching sequence, analogies, demos, omissions, and an honest quality read.

Built for people creating their own AI / LLM / Claude training content who want to study how others teach the same material: what they cover, in what order, what analogies they use, what they skip, and where the teaching is thin. Run it across 20+ videos and the common spine, the best explanatory devices, and the white space all become visible.

**This repo ships with a base start-guide** — a full breakdown of [Productive Dude's FULL Claude Tutorial For Beginners in 2026](https://www.youtube.com/watch?v=Xg55nTrbYYY) (1:52:38) and an 18-session curriculum built from it. See [`start-guide/`](start-guide/). You can use that curriculum to learn Claude immediately, then use the skill itself to extract teaching from more videos and grow your own corpus.

## What's in this repo

### The base start-guide ([`start-guide/`](start-guide/))

- **[`Productive Dude - FULL Claude Tutorial For Beginners in 2026! (FULL COURSE).md`](start-guide/Productive%20Dude%20-%20FULL%20Claude%20Tutorial%20For%20Beginners%20in%202026!%20%28FULL%20COURSE%29.md)** — pedagogical breakdown of the source video, including every concept covered, the full teaching sequence with timestamps, analogies, demos, notable omissions, and an honest quality read.
- **[`Productive Dude - 18-session pacing.md`](start-guide/Productive%20Dude%20-%2018-session%20pacing.md)** — an 18-session curriculum derived from that breakdown. Every minute of the video included; each session has timestamps, walk-away outcomes, and a practice prompt. Pace it however suits you (one session per day, one per week, however).

The base video is [Xg55nTrbYYY](https://www.youtube.com/watch?v=Xg55nTrbYYY). The breakdown and curriculum are pre-built so you don't need to run the skill to start learning — they're ready to use as soon as you clone.

### The skill itself ([`SKILL.md`](SKILL.md))

Once installed in Claude Code, the skill activates when you paste a YouTube URL with extraction intent ("extract teaching from <url>", "break down this video", etc.). It fetches the auto-caption transcript, cleans it, applies a structured extraction prompt, and writes the breakdown to your configured output folder. Use it to grow the corpus beyond the included start-guide.

## What it produces

For each video, a single markdown file with frontmatter (title, channel, duration, URL) and these sections:

- **Audience & Framing** — implied audience, hook, promise
- **Concepts Covered** — every concept tagged by depth (`mention` / `defined` / `taught` / `compared`)
- **Teaching Sequence** — timestamped, in order
- **Analogies & Metaphors** — strict definition; quotes with timestamps, or `None.`
- **Demos & Exercises** — what they actually show, not just narrate
- **Notable Omissions** — what's missing that a viewer would expect
- **Quality Read** — honest 3–6 bullets on where the teaching lands and where it's thin

The output structure is identical across videos so you can compare side-by-side. See [`SKILL.md`](SKILL.md) for the full extraction prompt.

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

### As a learner — start here

Open [`start-guide/Productive Dude - 18-session pacing.md`](start-guide/Productive%20Dude%20-%2018-session%20pacing.md). It's an 18-session curriculum you can work through at your own pace. Each session points at a timestamp range in the source video and gives you a practice prompt. Watch + practice in order.

### As a corpus builder — run the skill

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

## Files

- `SKILL.md` — the skill definition Claude reads. Contains the workflow and the full extraction prompt.
- `vtt_clean.py` — strips rolling-caption duplication and inline timing markup from raw VTT files, writes UTF-8 with `[HH:MM:SS]` markers every ~30s.
- `start-guide/` — the base curriculum that ships with this repo (Productive Dude breakdown + 18-session pacing).
- `README.md` — this file.

## License

MIT. Use it, fork it, ship your own version.

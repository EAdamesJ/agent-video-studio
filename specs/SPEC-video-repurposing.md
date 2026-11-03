# Module Spec: `video-repurposing`

## Objective

Convert operator-supplied long-form video/audio into a transcript and a ranked set of short clip candidates with exact source timestamps.

## Commands

```powershell
agent-video-studio project create --title "Episode clips" --mode repurpose
agent-video-studio project import <project-id> --file <path>
agent-video-studio project highlights <project-id>
```

## Project structure

`src/agent_video_studio/repurposing/` owns media ingest, transcript normalization, segment analysis, highlight selection, crop hints, and clip project creation.

## Code style

Retain transcript timestamps and source references through every transform. Highlight ranking returns explanations and confidence, not opaque scores alone.

## Testing strategy

Plan fixture-based checks for timestamps, clip bounds, transcript segments, supported formats, and resumable import jobs.

## Boundaries

- Always: use media supplied or explicitly selected by the operator; preserve source timestamps and allow manual clip edits.
- Ask first: retrieve media from third-party sites or send it to remote transcription/model services.
- Never: modify the source media or claim a clip's context outside the selected time range.

## Success criteria

- Local video and audio import produces duration/metadata and a normalized transcript.
- Candidate clips include start/end timestamps, title, hook, transcript excerpt, and ranking rationale.
- Approved candidates become editable timeline projects and render at selected aspect ratios.

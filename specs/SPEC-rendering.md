# Module Spec: `rendering`

## Objective

Render editable timelines into video deliverables with narration, captions, music, layouts, thumbnails, and export metadata using FFmpeg.

## Commands

```powershell
agent-video-studio project render <project-id> --aspect-ratios 9:16,16:9
agent-video-studio project export <project-id> <render-id> 9:16 <directory>
```

## Project structure

`src/agent_video_studio/media/` owns FFmpeg discovery, input probing, timeline planning, filters, audio mix, subtitles, thumbnail capture, and export bundles.

## Code style

Build FFmpeg argument lists without shell evaluation. Represent composition as normalized intermediate data so render providers may change without changing projects.

## Testing strategy

Plan tiny generated-media fixtures for aspect ratios, subtitle inclusion, audio mixing, output metadata, and cancellation cleanup.

## Boundaries

- Always: validate input/output locations, preserve the editable timeline, and provide useful FFmpeg diagnostics.
- Ask first: invoke remote video/image generation or create large outputs that may incur a charge.
- Never: execute arbitrary command strings or overwrite user source files.

## Success criteria

- Timeline projects render MP4 H.264/AAC in vertical 9:16, landscape 16:9, and square 1:1 layouts.
- Captions can be burned in and exported as SRT/VTT; audio can be normalized and mixed.
- Each export includes project metadata, thumbnail, title/description/hashtags, and source attribution/license notes where available.

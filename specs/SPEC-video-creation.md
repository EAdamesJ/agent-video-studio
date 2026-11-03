# Module Spec: `video-creation`

## Objective

Turn a user brief, outline, or supplied script into a reviewable video project with scenes, narration, visual directions, captions, and metadata.

## Commands

```powershell
agent-video-studio project create --title "Example" --mode prompt
agent-video-studio project script <project-id>
```

## Project structure

`src/agent_video_studio/creation/` owns brief normalization, script generation, storyboard models, localization, and scene-level editing operations.

## Code style

Keep generated content structured and editable. Separate factual source notes from narration; retain provider/model metadata on each generation.

## Testing strategy

Plan deterministic tests for schema validation, scene ordering, duration estimates, language preservation, and script regeneration boundaries.

## Boundaries

- Always: return an editable script/storyboard and ask for approval before costly rendering or posting.
- Ask first: introduce autonomous web research or paid media generation as a default.
- Never: invent citations or present unsupported facts as verified.

## Success criteria

- Brief-to-script and script-to-storyboard flows support hooks, tone, CTA, language, target duration, and output platform.
- Each scene stores narration, visual direction, duration, asset references, and captions.
- Users can revise a scene without discarding approved content in other scenes.

---
name: agent-video-studio
description: Create, repurpose, render, and prepare video projects with Agent Video Studio through its MCP tools or CLI. Use for brief-to-video, user-supplied media-to-clips, and requested export or publishing workflows.
---

# Agent Video Studio

Use this skill when the user wants to create or manage a video project with Agent Video Studio (AVS). It provides workflow instructions; it does not install AVS, configure MCP, supply API keys, or add capabilities absent from the installed AVS version.

## Connect to AVS

1. Prefer the connected Agent Video Studio MCP tools when available. Discover the tools exposed by the client and use their current schemas; the documented tools include `list_projects`, `list_providers`, `create_project`, `get_project`, `generate_script`, `import_media`, `analyze_media`, `select_highlights`, `edit_scene`, `render_project`, `preflight_publish`, `publish_export`, and `get_job`.
2. If MCP is unavailable but the shell can access AVS, use the installed `avs` or `agent-video-studio` CLI. Start with `avs doctor`, `avs providers`, or `avs --help` to check the actual installation and available commands.
3. If neither surface is available, explain that installing this skill alone does not install or connect AVS. Point the user to the [installation guide](https://github.com/EAdamesJ/agent-video-studio/blob/main/docs/es/INSTALLATION.md) and the [MCP setup guide](https://github.com/EAdamesJ/agent-video-studio/blob/main/docs/es/MCP.md). Do not claim an action succeeded without a tool or CLI result.

The MCP server's `import_media` accepts files within AVS's configured data directory. For a user-selected file elsewhere, use the AVS CLI import command if available; it copies the file into managed project storage. Never bypass AVS path restrictions or alter the source file.

## Choose the workflow

### Create a video from an idea

- Get the brief, audience, language, approximate duration, destination platform, and aspect ratio from the user or infer only what their request makes clear. AVS supports `9:16`, `16:9`, and `1:1`.
- Create a `prompt` project, then generate its script and storyboard. Read the resulting project and present the editable scenes for review. Apply requested revisions without discarding approved content.
- Do not invent factual claims or citations. If research is needed, ask before doing external research and distinguish sourced facts from creative narration.
- Do not assume stock, image, or video generation is configured. Use only media services AVS reports as available and the user has selected.

### Turn supplied long-form media into clips

- Use only media the user supplied or explicitly selected. Create a `repurpose` project, import the source, and analyze it.
- Before sending a brief, transcript, or media to a remote model, transcription, or speech provider, disclose what will be sent and ask for approval unless the user has already approved that specific external processing. Local Whisper transcription stays on the machine; OpenAI transcription sends the selected audio remotely. Edge TTS and ElevenLabs send narration text to their respective services.
- Present candidate clips with their source start/end times, transcript excerpts, and reasons for selection. Ask which candidates to keep when the user has not specified them. Preserve source timestamps when editing or rendering.

### Edit, render, and export

- Read the current project before editing. Change only fields needed for the user's request and keep the project editable.
- Before a substantial render, summarize the selected aspect ratios, captions, narration/TTS choice, and any remote or paid services. Proceed when the user requested that render or approves the proposed output; ask first if it would add significant time, cost, or external processing beyond the request.
- Return the actual export directory or file paths reported by AVS. Do not claim a render or export exists until AVS confirms it.

### Publish

- Publishing is a separate action from rendering. Run `preflight_publish` first, then show the destination account/platform, media, title, description, and visibility.
- Call `publish_export` with `confirm=true` only after the user has reviewed those exact details and explicitly confirmed publication. Never infer publication consent from approval to create or render a video.

## CLI reference

Use the CLI only when it is installed and available to the current agent. Replace placeholders with the actual values returned by AVS.

```bash
avs providers
avs project list
avs project create --title "Project title" --mode prompt --brief "Video brief" --language es --aspect-ratio 9:16
avs project script <project-id> --language es --target-duration-seconds 60 --platform "Reels"
avs project show <project-id>

avs project create --title "Clip project" --mode repurpose --language es --aspect-ratio 9:16
avs project import <project-id> /path/to/user-selected-video.mp4
avs project analyze <project-id>
avs project select-highlights <project-id> id-1,id-2

avs project render <project-id> --aspect-ratios 9:16 --captions --tts
avs project preflight-publish <project-id> <render-id> 9:16
```

Before `--tts`, check which TTS provider is configured and follow the remote-processing guidance above. Publishing commands are intentionally omitted here; use the MCP confirmation rule or the CLI's `--confirm` only after the user approves the reviewed post details.

## Credentials and agent compatibility

- Never ask the user to paste API keys into the conversation, print `.env`, or include credentials in tool arguments. AVS reads provider credentials from its local environment or `.env`; use provider status tools without exposing secrets.
- This skill follows the portable `SKILL.md` format. It can guide any agent that loads this format and can access AVS through MCP or the CLI. A DeepSeek-based harness must provide that skill-loading and tool/shell access itself; this repository does not provide a DeepSeek-hosted MCP service or a harness-specific adapter.
- Report the project ID, actual output paths, services used, and any missing configuration. Be clear when an operation is blocked or incomplete.

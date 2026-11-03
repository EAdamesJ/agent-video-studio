# Contributing

Thanks for helping make Agent Video Studio useful to creators and the agents they already use.

## Before starting

- Read [`SPEC.md`](SPEC.md), [`CAPABILITY_MAP.md`](CAPABILITY_MAP.md), and the relevant module spec in [`specs/`](specs/).
- For a substantial feature, open an issue or discussion describing the user workflow and acceptance criteria.
- Keep provider-specific behavior behind a provider interface; do not make a paid API a hard dependency.

## Development principles

- Python APIs use type hints and validate input at service boundaries.
- Preserve source timestamps and project editability.
- Never log or commit credentials or private media.
- All tools that publish externally require a separate confirmation action.
- Document new environment variables and platform approval requirements.

## Pull requests

- Make focused commits with clear messages.
- Include user-facing documentation for behavior or setup changes.
- Describe the workflow changed and any external services needed to exercise it.
- Do not include generated render files or real user content.

## Reporting a security issue

Please do not open a public issue containing credentials, personal media, or a suspected exploitable vulnerability. Use GitHub's private vulnerability reporting for this repository when enabled.

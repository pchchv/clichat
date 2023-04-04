# clichat
## CLI access to ChatGPT

CliChat is a command line interface (CLI) tool designed to interact with OpenAI's [ChatGPT](https://chat.openai.com/).
It accepts pipeline input, arguments, or both, and allows you to save common cue preambles for quick use, also provides methods for extracting JSON or Markdown from ChatGPT responses.

**Important:** To use CliChat, you will need to configure the OpenAI API key.

You can do this by passing `--openai-api-key KEY` or by setting the env variable `OPENAI_API_KEY` (recommended).
# clichat
## CLI access to ChatGPT

CliChat is a command line interface (CLI) tool designed to interact with OpenAI's [ChatGPT](https://chat.openai.com/).
It accepts pipeline input, arguments, or both, and allows you to save common cue preambles for quick use, also provides methods for extracting JSON or Markdown from ChatGPT responses.

**Important:** To use CliChat, you will need to configure the OpenAI API key.

You can do this by passing `--openai-api-key KEY` or by setting the env variable `OPENAI_API_KEY` (recommended).

## Install

### PyPi

```bash
pip install clichat
```

### Brew (slow...)

```bash
brew tap pchchv/clichat
brew install clichat
```

## Documentation

### Making queries

#### A new conversation

```bash
сliсhat how can I extract a still frame from a video at 22:01 with ffmpeg
```

#### recall the last conversation

if you would like to recall the last conversation just call it back with `-l`

```bash
сliсhat -l
```

#### Continue the last conversation

To continue the conversation and ask for a change within the context, you can again use `-l` but with a query.

```bash
сliсhat -l can we make a gif instead from 00:22:01 to 00:22:04
```

`-l` is the shortcut for `-S last` or last session. It is possible to track and continue various individual conversations using the [session options](#session-options) options.


#### Switching between gpt-3.5 and 4

The default is gpt-3.5, to switch to 4, use `clichat -c 4`

#### Chatting interactively

If you want to chat interactively, just use `clichat -i`.

#### Show streaming text (experimental)

You can also stream responses as in webui. At the end of the stream, the result will be formatted and can be merged into an interactive session.

```CliChat -s -i```

### Formatting the results

Responses are parsed and if CliChat thinks its markdown, it will be presented as such to get the syntax highlighted. But sometimes this may not work, because it removes new lines, or because you are only interested in extracting part of the result to pass to another command.

It is possible to use:
- `-r` just prints the text as returned by ChatGPT and does not pass it through markdown.
- `-e` tries to determine what was returned (either a block of code or a json) and extract only that part. If neither is found, it does the same as `-r`.

Both options can be used either with a new query, e.g.

```bash
clichat -e write me a python boilerplate script that starts a server and prints hello world > main.py
```
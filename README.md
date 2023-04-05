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

### Passing content to CliChat

If there are long requests that we don't want to type every time, or just want to provide context for our request, we can pass content to CliChat.

e.g.

```bash
curl https://news.ycombinator.com/rss | clichat given the above rss can you show me the top 3 articles about AI and their links -c 4
```

or

```bash
clichat what does this script do < script.sh
```

What gets sent to ChatGPT over the wire is:

```
piped input
-------
query
```

#### Session Options

Sessions are named conversations.

If you start CliChat with a session name SESS of your choice:

```bash
clichat -S SESS can we make a gif instead from 00:22:01 to 00:22:04
```

CliChat will create a session named SESS if it does not exist, and save the current exchange (request-response pair) for SESS.

If such a session already exists, the saved conversation will be loaded and a new exchange will be added.

Without the session argument the exchange is also stored in a session named `last`, but subsequent calls without a session will overwrite the contents of `last`. You can continue a conversation that was started as a sessionless exchange by passing `-S last`, but `last` will not be a safe place to store the conversation, since it will be cleared again on the next sessionless call. The `-l` option is provided as an abbreviation for `-S last`.

If you specify a session without a query:

```bash
clichat -S SESS
```

CliChat will recall a conversation without changing the session.

CliChat supports various operations on sessions. It provides `--session-OP` options, where `OP` can be `list`, `path`, `dump`, `delete`, `rename`.

### Checking token count and estimated costs

If you want to check the approximate cost and use of tokens of the previous request, you can use the `-t` flag for "tokens".

This can be done when passing a large amount of context, as in the example above.

```bash
curl https://news.ycombinator.com/rss | clichat given the above rss can you show me the top 3 articles about AI and their links -t
```

This will not perform any action on the wire, but will just calculate the tokens locally.

### Use custom prompts (the system msg)

The system message is used to instruct the model how to behave, see [OpenAI - Instructing Chat Models]. [OpenAI - Instructing Chat Models](https://platform.openai.com/docs/guides/chat/instructing-chat-models).

They can be loaded using the `-p` command. For convenience, any file that we put in ~/.config/clichat/ will be picked up by this command.

So, for example, with the following file `~/.config/clichat/etymology`, which contains:

```
I want you to act as a professional Etymologist and Quiz Generator. You have a deep knowledge of etymology and will be provided with a word.
The goal is to create cards that quiz on both the etymology and finding the word by its definition.

The following is what a perfect answer would look like for the word "disparage":

[{
  "question": "A verb used to indicate the act of speaking about someone or something in a negative or belittling way.<br/> <i>E.g He would often _______ his coworkers behind their backs.</i>",
  "answer": "disparage"
},
{
  "question": "What is the etymological root of the word disparage?",
  "answer": "From the Old French word <i>'desparagier'</i>, meaning 'marry someone of unequal rank', which comes from <i>'des-'</i> (dis-) and <i>'parage'</i> (equal rank)"
}]

You will return answers in JSON only. Answer truthfully and if you don't know then say so. Keep questions as close as possible to the
provided examples. Make sure to include an example in the definition question. Use HTML within the strings to nicely format your answers.

If multiple words are provided, create questions and answers for each of them in one list.

Only answer in JSON, don't provide any more text. Valid JSON uses "" quotes to wrap its items.
```

We can now run a command and refer to this prompt with `-p etymology`:

```bash
clichat -p etymology gregarious
```

You can specify `-p` directly to the file path in order to load a system message from any arbitrary location

And since we asked for JSON, we can pipe our result to something else, e.g.:

```bash
clichat -l -e > toanki
```
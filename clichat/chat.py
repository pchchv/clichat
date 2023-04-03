import os
import yaml
import types
import openai
import collections
import openai.error
from clichat import utils, errors


DEFAULT_OPENAI_SETTINGS = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.1,
    "n": 1,
    "stream": False,
}


class Message(collections.namedtuple("Message", ["role", "content"])):

    @staticmethod
    def represent_for_yaml(dumper, msg):
        val = []
        md = msg._asdict()

        for fie in msg._fields:
            val.append([dumper.represent_data(e) for e in (fie, md[fie])])

        return yaml.nodes.MappingNode("tag:yaml.org,2002:map", val)

    @classmethod
    def import_yaml(cls, seq):
        """
        Creating a class instance from the provided YAML representation.
        """
        return cls(**seq)


yaml.add_representer(Message, Message.represent_for_yaml)


def set_azure_if_present(config):
    """Checks for azure settings and sets the endpoint configuration."""
    if "OPENAI_API_AZURE_ENGINE" in os.environ:
        config["engine"] = os.environ["OPENAI_API_AZURE_ENGINE"]


def map_generator(openai_gen):
    """Maps an openai stream generator to a stream of Messages,
    the final one being a completed Message."""
    role, message = None, ""
    for update in openai_gen:
        delta = [choice["delta"] for choice in update["choices"]][0]
        if "role" in delta:
            role = delta["role"]
        elif "content" in delta:
            message += delta["content"]
        yield Message(role, message)


def map_single(result):
    """Maps a result to a Message."""
    response_message = [choice["message"] for choice in result["choices"]][0]
    return Message(response_message["role"], response_message["content"])


def query_chatgpt(messages, config):
    """Queries the chat GPT API with the given messages and config."""
    openai.api_key = config["openai_api_key"]
    config = utils.merge_dicts(DEFAULT_OPENAI_SETTINGS, config)
    set_azure_if_present(config)
    dict_messages = [msg._asdict() for msg in messages]

    try:
        result = openai.ChatCompletion.create(messages=dict_messages, **config)
        if isinstance(result, types.GeneratorType):
            return map_generator(result)
        elif isinstance(result, dict):
            return map_single(result)
        else:
            raise ValueError(f"unexpected result openai: {result}")
    except (
        openai.error.InvalidRequestError,
        openai.error.AuthenticationError,
        openai.error.RateLimitError,
    ) as e:
        raise errors.CliChatError(f"openai error: {e}")

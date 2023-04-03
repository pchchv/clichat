import os
import yaml
import collections


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

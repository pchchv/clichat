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

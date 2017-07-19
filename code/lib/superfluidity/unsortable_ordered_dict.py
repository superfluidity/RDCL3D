from collections import OrderedDict
import yaml


class UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass


class UnsortableOrderedDict(OrderedDict):
    def items(self, *args, **kwargs):
        return UnsortableList(OrderedDict.items(self, *args, **kwargs))
    @staticmethod
    def dump(dict, dstfile):
        yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)
        yaml.dump(dict, dstfile, default_flow_style=False, explicit_start=True, width=1000)



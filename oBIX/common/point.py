from oBIX.common.data_type import DataType
import json


class Point(object):
    name: str
    val: str
    status: str
    display: str
    data_type: DataType
    href: str
    in1: str
    in2: str
    in3: str
    in4: str
    in5: str
    in6: str
    in7: str
    in8: str
    in9: str
    in10: str
    in11: str
    in12: str
    in13: str
    in14: str
    in15: str
    in16: str
    fallback: str
    out: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

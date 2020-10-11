from datetime import datetime as StdDatetime
import json


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StdDatetime):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def jsondumps(obj, indent=2) -> str:
    txt = json.dumps(obj, cls=JsonEncoder, indent=indent)
    return txt

import traceback

from oBIX.common import Point, DataType
from iupdatable import Logger


class Util(object):

    @staticmethod
    def parse_data_type(data_type_str: str):
        data_type_str = data_type_str.lower()
        if data_type_str == "real":
            return DataType.real
        elif data_type_str == "bool":
            return DataType.bool
        elif data_type_str == "int":
            return DataType.int
        elif data_type_str == "str":
            return DataType.str
        elif data_type_str == "enum":
            return DataType.enum
        else:
            return DataType.str

    @staticmethod
    def get_data_type_str(data_type: DataType):
        type_str = ""
        if data_type == DataType.bool:
            type_str = "bool"
        elif data_type == DataType.int:
            type_str = "int"
        elif data_type == DataType.real:
            type_str = "real"
        elif data_type == DataType.str:
            type_str = "str"
        elif data_type == DataType.enum:
            type_str = "enum"
        elif data_type == DataType.abs_time:
            type_str = "abstime"
        elif data_type == DataType.rel_time:
            type_str = "reltime"
        else:
            type_str = "str"
        return type_str

    @staticmethod
    def convert_to_type(str_value: str, data_type: DataType):
        if data_type == DataType.real:
            return float(str_value)
        elif data_type == DataType.bool:
            if str_value.strip().lower() == "true":
                return True
            else:
                return False
        elif data_type == DataType.int:
            return int(str_value)
        else:
            return str_value

    @staticmethod
    def parse_point(point_dict: dict, data_type_str: str):
        try:
            if "@is" not in point_dict:
                return None
            if "obix:Point" not in point_dict["@is"]:
                return None
            data_type_str = data_type_str.lower()
            point = Point()
            point.val = point_dict["@val"]
            # point.status = point_dict["@status"]
            point.href = point_dict["@href"]
            point.display = point_dict["@display"]
            point.name = str(point_dict["@href"]).split("/")[-2]
            slots = point_dict[data_type_str]
            if ":" in data_type_str:
                data_type_str = data_type_str.split(":")[-1]

            point.data_type = Util.parse_data_type(data_type_str)

            for slot in slots:
                name = slot["@name"]
                value_str = None
                if "@display" not in slot:
                    continue
                # @display is null but val has value
                # In this case, the final value is treated as None.
                if "{null}" not in slot["@display"]:
                    value_str = slot["@val"]
                setattr(point, name, value_str)
            return point
        except Exception as e:
            Logger.instance().error(traceback.format_exc())
            Logger.instance().error(e)
            return None

    @staticmethod
    def parse_points(points: object, data_type_str: str):

        result = []
        if isinstance(points, list):
            for data in points:
                point = Util.parse_point(data, data_type_str)
                if point is not None:
                    result.append(point)
        else:
            point = Util.parse_point(points, data_type_str)
            if point is not None:
                result.append(point)
        return result

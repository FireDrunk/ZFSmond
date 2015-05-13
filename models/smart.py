from flask.ext import restful
from pySMART import Device

class SmartInfo(restful.Resource):
    def get(self, disk):
            raw_info = Device('/dev/' + disk)
            smart_info = {}
            for smart_value in raw_info.attributes:
                if smart_value:
                    smart_info[smart_value.name] = smart_value.raw
            return smart_info

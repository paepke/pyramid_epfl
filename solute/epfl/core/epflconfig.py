#* coding: utf-8

CONFIG = {"epfl.max_upload_size": ("FileSizeType", "1 m", "The maximal size of a single file for user uploads."),
          "epfl.tmp_data_ttl": ("DurationType", "1 d", "The time to live of temp-data objects (e.g. uploads)")}

class ConfigType(object):
    pass

class DurationType(ConfigType):

    def convert_value(self, value_str):
        if value_str.endswith("m"):
            value = long(value_str[:-1]) * 60
        elif value_str.endswith("h"):
            value = long(value_str[:-1]) * 60 * 60
        elif value_str.endswith("d"):
            value = long(value_str[:-1]) * 60 * 60 * 24
        else:
            value = long(value)

        return value

class FileSizeType(ConfigType):

    def convert_value(self, value_str):
        if value_str.endswith("k"):
            value = long(value_str[:-1]) * 1024
        elif value_str.endswith("m"):
            value = long(value_str[:-1]) * 1024 * 1024
        elif value_str.endswith("g"):
            value = long(value_str[:-1]) * 1024 * 1024 * 1024
        else:
            value = long(value)

        return value


CONFIG_TYPES = {"FileSizeType": FileSizeType,
                "DurationType": DurationType}

def get_type(config_info):
    global CONFIG_TYPES
    type_name = config_info[0]
    return CONFIG_TYPES[type_name]()

def get_default(config_info):
    return config_info[1]


def get(request, name):
    global CONFIG

    if name in request.registry.settings:
        config_value = request.registry.settings[name]
    else:
        config_value = get_default(CONFIG[name])
    config_type = get_type(CONFIG[name])
    return config_type.convert_value(config_value)

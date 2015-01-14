

def get_item_or_attr(obj, key):
    try:
        return obj[key]
    except (KeyError, TypeError):
        return getattr(obj, key)


class ModelBase(object):
    def __getitem__(self, item):
        compo, key, row, data_interface = item
        args, kwargs = row
        output = []
        for row in getattr(self, 'load_' + key)(compo, *args, **kwargs):
            tmp_data = data_interface.copy()
            for k, v in tmp_data.items():
                if type(v) is str:
                    try:
                        v.format()
                        tmp_data[k] = get_item_or_attr(row, tmp_data[k])
                    except KeyError:
                        if type(row) is dict:
                            tmp_data[k] = v.format(**row)
                        else:
                            tmp_data[k] = v.format(**row.__dict__)
                else:
                    tmp_data[k] = get_item_or_attr(row, k)

            output.append(tmp_data)

        return output
# * coding: utf8


class ModelBase(object):
    def __getitem__(self, item):
        key, row, interface = item
        args, kwargs = row
        print key, interface, args, kwargs
        output = []
        for row in getattr(self, 'load_' + key)(*args, **kwargs):
            tmp_data = interface.copy()
            for k in tmp_data:
                try:
                    tmp_data[k] = row[k]
                except KeyError:
                    tmp_data[k] = getattr(row, k)

            output.append(tmp_data)

        return output
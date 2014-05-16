#* coding: utf-8

import json

def get_tags(request, start_row, num_rows, sort_column, sort_order):

    tag_keys = request.redis.keys("tag_*")
    if tag_keys:
        tags = [json.loads(row) for row in request.redis.mget(tag_keys)]
    else:
        tags = []

    out = tags[start_row:start_row + num_rows]

    if sort_column:
        sorter = [(row[sort_column], row) for row in out]
        sorter.sort()
        out = [row[1] for row in sorter]
        if sort_order == "desc":
            out.reverse()

    return len(tags), out


def create_tag(request, data):

    next_id = request.redis.incr("tags")

    data["id"] = next_id

    request.redis.set("tag_" + str(next_id), json.dumps(data))

    return next_id

def delete_tag(request, id):

    request.redis.delete("tag_" + str(id))




def get_tag(request, id):

    data = json.loads(request.redis.get("tag_" + str(id)))

    return data
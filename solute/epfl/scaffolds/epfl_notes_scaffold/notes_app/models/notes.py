#* coding: utf-8

import json

def get_notes(request, start_row, num_rows, sort_column, sort_order):

    note_keys = request.redis.keys("note_*")
    if note_keys:
        notes = [json.loads(row) for row in request.redis.mget(note_keys)]
    else:
        notes = []

    out = notes[start_row:start_row + num_rows]

    if sort_column:
        sorter = [(row[sort_column], row) for row in out]
        sorter.sort()
        out = [row[1] for row in sorter]
        if sort_order == "desc":
            out.reverse()

    return len(notes), out


def create_note(request, data):

    next_id = request.redis.incr("notes")

    data["id"] = next_id

    request.redis.set("note_" + str(next_id), json.dumps(data))

    return next_id

def save_note(request, data):

    request.redis.set("note_" + str(data["id"]), json.dumps(data))


def get_note(request, id):

    data = json.loads(request.redis.get("note_" + str(id)))

    return data

def delete_note(request, id):

    request.redis.delete("note_" + str(id))

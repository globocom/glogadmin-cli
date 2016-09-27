

def mult_dict_del(dict, kwargs):
    for key in kwargs:
        if (dict.has_key(key)):
            del dict[key]
    return dict

def format_stream_to_create(stream):
    stream_rules = stream.get("rules")
    for rule in stream_rules:
        mult_dict_del(rule, kwargs=["stream_id", "id"])
    mult_dict_del(stream, kwargs=["created_at", "creator_user_id", "id", "alert_conditions", "outputs", "disabled",
                                  "alert_receivers"])
    return stream

def format_streams_to_create(streams):
    for stream in streams:
        format_stream_to_create(stream)
    return streams
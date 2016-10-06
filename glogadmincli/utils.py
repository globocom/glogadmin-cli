import json

def mult_dict_del(dict, kwargs):
    for key in kwargs:
        if (dict.has_key(key)):
            del dict[key]
    return dict

def format_stream_to_create(stream):
    stream_rules = stream.get("rules")
    for rule in stream_rules:
        mult_dict_del(rule, kwargs=["stream_id", "id"])
    mult_dict_del(stream, kwargs=["created_at", "creator_user_id", "id", "alert_conditions",
                                  "outputs", "disabled", "alert_receivers"])
    return stream

def format_streams_to_create(streams):
    for stream in streams:
        format_stream_to_create(stream)
    return streams

def format_input_to_create(input):
    input["configuration"] = input["attributes"]
    return mult_dict_del(input, kwargs=["attributes", "created_at", "creator_user_id", "id",
                                        "content_pack", "node", "static_fields", "name"])

def format_extractor_to_create(extractor):
    extractor["cut_or_copy"] = extractor["cursor_strategy"]
    extractor["extractor_type"] = extractor["type"]
    converters = extractor.get("converters")
    if converters is None or len(converters) == 0:
        extractor["converters"] = {}
    else:
        extractor["converters"] = {} #json.dumps(converters)
    return mult_dict_del(extractor, kwargs=["type", "creator_user_id", "id", "metrics", "exceptions",
                                            "converter_exceptions", "cursor_strategy"])

def format_rule_to_create(rule):
    return mult_dict_del(rule, kwargs=["id", "stream_id"])
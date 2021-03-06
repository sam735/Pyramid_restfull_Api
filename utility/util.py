from dateutil import parser
import json
import ast


class DictToObject(object):
    def __init__(self, d):
        self.__dict__ = d


    def __getattr__(self, item):
        return None


def return_lower_case_of_string(str):
    return str.lower()


def convertStringToDateTime(str):
    try:
        return parser.parse(str)
    except Exception:
        return None

    else:
        return parser.parse(str)


def to_json_obj(obj):
    l = []
    for i in range(len(obj)):
        obj_tup = obj[i]
        obj_str = ast.literal_eval(obj_tup[0])
        l.append(obj_str)
    return l

# def insert_to_source_specific_model(iterable,fhirIdn,source,session):
#     for key, val in iterable.items():
#         if type(val).__name__ == 'list':
#             for value in val:
#                 fn = type_lookup.get(type(value).__name__ )
#                 if fn is not None:
#                     fn( value,fhirIdn,source,key,session)

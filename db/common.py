# from db.model.procedure import(CodeableConcept)
# from utility.util import DictToObject

# def add_to_CodeableConcept(val,procedureIdn,source,key):
# 	if val.coding != None:
#         for code in val.coding:
#             Codeeable_obj = CodeableConcept(DictToObject(code),val.text,procedureIdn,'source',key)
#             request.db.add(Codeeable_obj)
#     else:
#         Codeeable_obj = CodeableConcept(DictToObject({}),val.text,procedureIdn,'source',key)
#         request.db.add(Codeeable_obj)


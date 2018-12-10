from sqlalchemy import func 

def add_and_return_CodeCodeableConcept_obj_idn(payload_obj,tableObj,session,text=None):
	CodeCodeableConcept_obj = tableObj(payload_obj.get('system'),payload_obj.get('version'),
															payload_obj.get('code'),
															payload_obj.get('display'),
															payload_obj.get('userSelected'),text)
	session.add(CodeCodeableConcept_obj)
	session.flush()
	return CodeCodeableConcept_obj.codeable_concept_idn

def add_and_return_idn_from_refrence_table(payload_obj,tableObj,session):
	CodeRefrence_obj = tableObj(payload_obj.reference,payload_obj.display)
	session.add(CodeRefrence_obj)
	session.flush()
	return CodeRefrence_obj.refrence_idn

def check_list_exist_and_return_values(id_list):
	if not id_list:
		return None
	else:
		return id_list[0]

class DictToObject(object):
	def __init__(self, d):
		self.__dict__ = d

	def __getattr__(self, item):
		return None

def insert_to_multivalue_ref_attribute_table(ref_payload,ref_table,attr_table,procedure_idn,session):
	def_ref_idn = add_and_return_idn_from_refrence_table(ref_payload,ref_table,session)
	attr_obj = attr_table(procedure_idn,def_ref_idn)
	session.add(attr_obj)
	session.flush()

def return_fetch_max_of_column_idn(table_name,session):
	return session.query(func.max(table_name.codeable_group_idn))


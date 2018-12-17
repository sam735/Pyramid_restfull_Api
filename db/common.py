from db.model.procedure import CodeRefrence
def add_to_CodeCodeableConcept_table(payload_obj,tableObj,session,group_idn=None,text=None):
	CodeCodeableConcept_obj = tableObj(payload_obj.get('system'),payload_obj.get('version'),
															payload_obj.get('code'),
															payload_obj.get('display'),
															payload_obj.get('userSelected'),group_idn,text)
	session.add(CodeCodeableConcept_obj)

def add_to_refrence_table(ref_payload,fhir_idn,source,attribute):
	CodeRefrence_obj = CodeRefrence(ref_payload,fhir_idn,source,attribute)

def add_to_CodeCodeableConcept_table(payload_obj,tableObj,session,group_idn=None,text=None):
	CodeCodeableConcept_obj = tableObj(payload_obj.get('system'),payload_obj.get('version'),
															payload_obj.get('code'),
															payload_obj.get('display'),
															payload_obj.get('userSelected'),group_idn,text)
	session.add(CodeCodeableConcept_obj)

def add_to_refrence_table(payload_obj,group_idn,tableObj,session):
	CodeRefrence_obj = tableObj(payload_obj.reference,payload_obj.display,group_idn)
	session.add(CodeRefrence_obj)
from db.model.procedure import(FhirCodeableConcept,Annotation,FhirIdentifier,Reference)
from utility.util import(DictToObject)

def insert_to_identifier(val,fhirIdn,source,key,session):
	import pdb;pdb.set_trace()
	type_idn = []
	if val.type != None:
		if val.type != None:
			if val.type.get('coding') != None:
				for code in val.type.get('coding'):
					Codeeable_obj = FhirCodeableConcept(DictToObject(code),val.type.get('text'),fhirIdn,source,key)
					session.add(Codeeable_obj)
					session.flush()
					type_idn.append(Codeeable_obj.codeable_concept_idn)
			else:
				Codeeable_obj = FhirCodeableConcept(DictToObject({}),val.text,fhirIdn,source,key)
				session.add(Codeeable_obj)
				session.flush()
				type_idn.append(Codeeable_obj.codeable_concept_idn)
	if len(type_idn) == 0 :
		proc_identfr = FhirIdentifier(val,None,fhirIdn,source)
		session.add(proc_identfr)
	else:
		for idn in type_idn:
			proc_identfr = FhirIdentifier(val,None,fhirIdn,source)
			session.add(proc_identfr)

def insert_to_annotation(val,fhirIdn,source,key,session):
	authorReference = None
	if val.authorReference != None:
		ref_obj = Reference(val.authorReference,fhirIdn,source,key)
		session.add(ref_obj)
		session.flush()
		authorReference = ref_obj.code_refrence_idn
	Annotation_obj = Annotation(authorReference,val,fhirIdn,source)
	session.add(Annotation_obj)


from db.model.procedure import (FhirProcedure, CodeYn, CodeableConcept, Refrence, ProcedurePerformer,
								ProcedureFocaldevice, FhirIdentifier, Annotation)


from utility.util import (DictToObject,to_json_obj)

from db.common import(insert_to_identifier,insert_to_annotation)

import json

def insert_procedure(request):
    procedure = request.swagger_data['ProcedureItem']

    procedure_payload = request.json_body
    
    procedure_obj = FhirProcedure(procedure,procedure_payload)  
    request.db.add(procedure_obj)
    request.db.flush()
    for key, val in procedure_payload.items():
        if type(procedure[key]).__name__ == 'list':
            for val in procedure[key]:
                if type(val).__name__ == 'Refrence':
                    ref_obj = Refrence(val,procedure_obj.fhir_procedure_idn,'procedure',key)
                    request.db.add(ref_obj)
                if type(val).__name__ == 'CodeableConcept':
                    if val.coding != None:
                        for code in val.coding:
                            Codeeable_obj = CodeableConcept(DictToObject(code),val.text,procedure_obj.fhir_procedure_idn,'procedure',key)
                            request.db.add(Codeeable_obj)
                    else:
                        Codeeable_obj = CodeableConcept(DictToObject({}),val.text,procedure_obj.fhir_procedure_idn,'procedure',key)
                        request.db.add(Codeeable_obj)

                if type(val).__name__ == 'Annotation':
                    insert_to_annotation(val,procedure_obj.fhir_procedure_idn,'procedure',key,request.db)

                if type(val).__name__ == 'Identifier':
                    insert_to_identifier(val,procedure_obj.fhir_procedure_idn,'procedure',key,request.db)

        if type(procedure[key]).__name__ == 'Refrence':
            ref_obj = Refrence(procedure[key],procedure_obj.fhir_procedure_idn,'procedure',key)
            request.db.add(ref_obj)

        if type(procedure[key]).__name__ == 'CodeableConcept':
            if procedure[key].coding != None:
                for code in procedure[key].coding:
                    Codeeable_obj = CodeableConcept(DictToObject(code),procedure[key].text,procedure_obj.fhir_procedure_idn,'procedure',key)
                    request.db.add(Codeeable_obj)
            else:
                Codeeable_obj = CodeableConcept(DictToObject({}),procedure[key].text,procedure_obj.fhir_procedure_idn,'procedure',key)
                request.db.add(Codeeable_obj)

    role_obj = None
    actor_obj = None
    onBehalfOf_obj = None
    onBehalfOf_idn = None
    if procedure.performer != None:
        for performer in procedure.performer:
            actor_obj = Refrence(performer.get('actor'),procedure_obj.fhir_procedure_idn,'procedure','performer')
            request.db.add(actor_obj)
            request.db.flush()

            if performer.get('onBehalfOf') != None:
                onBehalfOf_obj = Refrence(performer.get('onBehalfOf'),procedure_obj.fhir_procedure_idn,'procedure','performer')
                request.db.add(onBehalfOf_obj)
                request.db.flush()
                if onBehalfOf_obj.code_refrence_idn != None:
                    onBehalfOf_idn = onBehalfOf_obj.code_refrence_idn
                else:
                    onBehalfOf_idn = None

            if performer.get('role') != None:
                if performer.get('role').coding != None:
                    for code in performer.get('role').coding:
                        role_obj = CodeableConcept(DictToObject(code),performer.get('role').text,procedure_obj.fhir_procedure_idn,'procedure','performer')
                        request.db.add(role_obj)
                        request.db.flush()
                        performer_obj = ProcedurePerformer(procedure_obj.fhir_procedure_idn,role_obj.codeable_concept_idn,actor_obj.code_refrence_idn,
                                                            onBehalfOf_idn)
                        request.db.add(performer_obj)
                else:
                    role_obj = CodeableConcept(DictToObject({}),performer.get('role').text,procedure_obj.fhir_procedure_idn,'procedure','performer')
                    request.db.add(role_obj)
                    request.db.flush()
                    performer_obj = ProcedurePerformer(procedure_obj.fhir_procedure_idn,role_obj.codeable_concept_idn,actor_obj.code_refrence_idn,
                                                            onBehalfOf_idn)
                    request.db.add(performer_obj)

            else:
                performer_obj = ProcedurePerformer(procedure_obj.fhir_procedure_idn,None,actor_obj.code_refrence_idn,onBehalfOf_idn)
                request.db.add(performer_obj)
    manipulated_obj = None
    action_obj = None
    if procedure.focalDevice !=None:
        for focalDevice in procedure.focalDevice:
            manipulated_obj = Refrence(focalDevice.get('manipulated'),procedure_obj.fhir_procedure_idn,'procedure','focalDevice')
            request.db.add(manipulated_obj)
            request.db.flush()
            if focalDevice.get('action') != None:
                if focalDevice.get('action').coding != None:
                    for code in focalDevice.get('action').coding:
                        action_obj = CodeableConcept(DictToObject(code),focalDevice.get('action').text,procedure_obj.fhir_procedure_idn,'procedure','focalDevice')
                        request.db.add(action_obj)
                        request.db.flush()
                        focalDevice_obj = ProcedureFocaldevice(procedure_obj.fhir_procedure_idn,action_obj.codeable_concept_idn,manipulated_obj.code_refrence_idn)
                        request.db.add(focalDevice_obj)
                else:
                    action_obj = CodeableConcept(DictToObject({}),focalDevice.get('action').text,procedure_obj.fhir_procedure_idn,'procedure','focalDevice')
                    request.db.add(action_obj)
                    request.db.flush()
                    focalDevice_obj = ProcedureFocaldevice(procedure_obj.fhir_procedure_idn,action_obj.codeable_concept_idn,manipulated_obj.code_refrence_idn)
                    request.db.add(focalDevice_obj)

            else:
                focalDevice_obj = ProcedureFocaldevice(procedure_obj.fhir_procedure_idn,None,manipulated_obj.code_refrence_idn)
                request.db.add(focalDevice_obj)
    
    request.db.flush()

def fetch_procedure(request):
	import pdb;pdb.set_trace()
	param_obj = request.swagger_data

	#for handling multiple params
	if(param_obj['subject'] and param_obj['date']):

		patient_dt_subquery = request.db.query(Refrence.fhir_idn.label('fhir_idn')).\
									filter(Refrence.attribute == 'subject',Refrence.refrence == param_obj['subject']).subquery()

		patient_dt = request.db.query(FhirProcedure.json_payload).\
							filter(FhirProcedure.perfome_start_dt == param_obj['date'],
							FhirProcedure.fhir_procedure_idn.in_([patient_dt_subquery.c.fhir_idn])).all()
						
		patient_dt_json = to_json_obj(patient_dt)
		return patient_dt_json

	
	if(param_obj['status']): 
		stat = request.db.query(FhirProcedure.json_payload).filter(FhirProcedure.proc_status == param_obj['status']).all()
		stat_json = to_json_obj(stat)
		return stat_json

	if(param_obj['subject']):
		sub = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'subject').filter(Refrence.refrence == param_obj['subject']).\
					all()
		sub_json = to_json_obj(sub)
		return sub_json

	if(param_obj['performer']):
		perf = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'performer').filter(Refrence.refrence == param_obj['performer']).\
					filter(Refrence.code_refrence_idn == ProcedurePerformer.proc_actor).\
					all()
		perf_json = to_json_obj(perf)
		return perf_json

	if(param_obj['patient']):
		patient = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'patient').filter(Refrence.refrence == param_obj['patient']).\
					all()   
		patient_json = to_json_obj(patient)
		return patient_json

	if(param_obj['part-of']):
		partOf= request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'partOf').filter(Refrence.refrence == param_obj['part-of']).\
					all()
		partOf_json = to_json_obj(partOf)   
		return partOf_json
					
	if(param_obj['location']):
		loc = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'location').filter(Refrence.refrence == param_obj['location']).\
					all()   
		loc_json = to_json_obj(loc)
		return loc_json

	if(param_obj['encounter']):
		enc = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'encounter').filter(Refrence.refrence == param_obj['encounter']).\
					all()
		enc_json = to_json_obj(enc)
		return enc_json 
		 
	if(param_obj['identifier']):
		identifier = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == FhirIdentifier.fhir_idn).\
					filter(FhirIdentifier.value == param_obj['identifier']).\
					all()
		identifier_json = to_json_obj(identifier)
		return identifier_json  
					
	if(param_obj['definition']):
		definition = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'definition').filter(Refrence.refrence == param_obj['definition']).\
					all()
		definition_json = to_json_obj(definition)
		return definition_json

	if(param_obj['context']):
		context = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == Refrence.fhir_idn).\
					filter(Refrence.attribute == 'context').filter(Refrence.refrence == param_obj['context']).\
					all()
		context_json = to_json_obj(context)
		return context_json

	if(param_obj['code']):
		code = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == CodeableConcept.fhir_idn).\
					filter(CodeableConcept.attribute == 'code').filter(CodeableConcept.code == param_obj['code']).\
					all()
		code_json = to_json_obj(code)
		return code_json

	if(param_obj['based-on']):
		basedOn = request.db.query(FhirProcedure.json_payload).\
					filter(FhirProcedure.fhir_procedure_idn == CodeableConcept.fhir_idn).\
					filter(Refrence.attribute == 'basedOn').filter(Refrence.code == param_obj['based-on']).\
					all()
		basedOn_json = to_json_obj(basedOn)             
		return basedOn_json

	if(param_obj['date']):
		dt = request.db.query(FhirProcedure.json_payload).filter(FhirProcedure.perfome_start_dt == param_obj['date']).all()
		dt_json = to_json_obj(dt)
		return dt_json


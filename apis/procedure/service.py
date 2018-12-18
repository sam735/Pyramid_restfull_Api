from db.model.procedure import (FhirProcedure, CodeYn, CodeableConcept, Refrence, ProcedurePerformer,
                                ProcedureFocaldevice, FhirIdentifier, Annotation)

from utility.util import (DictToObject,return_lower_case_of_string)

#from db.common import(add_to_CodeableConcept_table,add_to_refrence_table)


def insert_procedure(request):
    procedure = request.swagger_data['ProcedureItem']

    procedure_payload = request.json_body
    
    #ToDo for identifier
    procedure_obj = FhirProcedure(procedure,procedure_payload)  
    request.db.add(procedure_obj)
    request.db.flush()

    
    # for k, v in procedure_payload.items():
    #     myCls = classLookup[type(procedure[key]).__name__]
    #     myCls(procedure, 'procedure', k)


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

                authorReference = None
                if type(val).__name__ == 'Annotation':
                    if val.authorReference != None:
                        ref_obj = Refrence(val.authorReference,procedure_obj.fhir_procedure_idn,'procedure',key)
                        request.db.add(ref_obj)
                        request.db.flush()
                        authorReference = ref_obj.code_refrence_idn
                    Annotation_obj = Annotation(authorReference,val,procedure_obj.fhir_procedure_idn,'procedure')
                    request.db.add(Annotation_obj)

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
            actor_obj = Refrence(DictToObject(performer.get('actor')),procedure_obj.fhir_procedure_idn,'procedure','performer')
            request.db.add(actor_obj)
            request.db.flush()

            if performer.get('onBehalfOf') != None:
                onBehalfOf_obj = Refrence(DictToObject(performer.get('onBehalfOf')),procedure_obj.fhir_procedure_idn,'procedure','performer')
                request.db.add(onBehalfOf_obj)
                request.db.flush()
                if onBehalfOf_obj.code_refrence_idn != None:
                    onBehalfOf_idn = onBehalfOf_obj.code_refrence_idn
                else:
                    onBehalfOf_idn = None


            if performer.get('role') != None:
                if performer.get('role').get('coding') != None:
                    for code in performer.get('role').get('coding'):
                        role_obj = CodeableConcept(DictToObject(code),performer.get('role').get('text'),procedure_obj.fhir_procedure_idn,'procedure','performer')
                        request.db.add(role_obj)
                        request.db.flush()
                        performer_obj = ProcedurePerformer(procedure_obj.fhir_procedure_idn,role_obj.codeable_concept_idn,actor_obj.code_refrence_idn,
                                                            onBehalfOf_idn)
                        request.db.add(performer_obj)
                else:
                    role_obj = CodeableConcept(DictToObject({}),performer.get('role').get('text'),procedure_obj.fhir_procedure_idn,'procedure','performer')
                    request.db.add(role_obj)
                    request.db.flush()
                    performer_obj = ProcedurePerformer(procedure_obj.fhir_procedure_idn,role_obj.codeable_concept_idn,actor_obj.code_refrence_idn,
                                                            onBehalfOf_idn)
                    request.db.add(performer_obj)

            else:
                performer_obj = ProcedurePerformer(procedure_obj.fhir_procedure_idn,actor_obj.code_refrence_idn,onBehalfOf_idn)
                request.db.add(performer_obj)

    manipulated_obj = None
    action_obj = None
    if procedure.focalDevice !=None:
        for focalDevice in procedure.focalDevice:
            manipulated_obj = Refrence(DictToObject(focalDevice.get('manipulated')),procedure_obj.fhir_procedure_idn,'procedure','focalDevice')
            request.db.add(manipulated_obj)
            request.db.flush()

            if focalDevice.get('action') != None:
                if focalDevice.get('action').get('coding') != None:
                    for code in focalDevice.get('action').get('coding'):
                        action_obj = CodeableConcept(DictToObject(code),focalDevice.get('action').get('text'),procedure_obj.fhir_procedure_idn,'procedure','focalDevice')
                        request.db.add(action_obj)
                        request.db.flush()
                        focalDevice_obj = ProcedureFocaldevice(procedure_obj.fhir_procedure_idn,action_obj.codeable_concept_idn,manipulated_obj.code_refrence_idn)
                        request.db.add(focalDevice_obj)
                else:
                    action_obj = CodeableConcept(DictToObject({}),focalDevice.get('action').get('text'),procedure_obj.fhir_procedure_idn,'procedure','focalDevice')
                    request.db.add(action_obj)
                    request.db.flush()
                    focalDevice_obj = ProcedureFocaldevice(procedure_obj.fhir_procedure_idn,action_obj.codeable_concept_idn,manipulated_obj.code_refrence_idn)
                    request.db.add(focalDevice_obj)

            else:
                focalDevice_obj = ProcedureFocaldevice(procedure_obj.fhir_procedure_idn,None,manipulated_obj.code_refrence_idn)
                request.db.add(focalDevice_obj)
    
    request.db.flush()

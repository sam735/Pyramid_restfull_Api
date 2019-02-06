
from db.model.procedure import (FhirProc, CodeYn, FhirCodeableConcept, FhirReference, ProcPerformer,
                                ProcFocaldevice, FhirIdentifier, FhirNote)
from utility.util import (DictToObject, to_json_obj)

from db.common import(insert_to_identifier, insert_to_FhirNote)

import json
from sqlalchemy import and_
from sqlalchemy_filters import apply_filters
from apis.lookup import proc_query_params


def insert_procedure(request):
    procedure = request.swagger_data['ProcedureItem']

    procedure_payload = request.json_body

    procedure_obj = FhirProc(procedure, procedure_payload)
    request.db.add(procedure_obj)
    request.db.flush()
    for key, val in procedure_payload.items():
        if type(procedure[key]).__name__ == 'list':
            for val in procedure[key]:
                if type(val).__name__ == 'Refrence':
                    ref_obj = FhirReference(
                        val, procedure_obj.fhir_proc_idn, 'procedure', key)
                    request.db.add(ref_obj)
                if type(val).__name__ == 'CodeableConcept':
                    if val.coding != None:
                        for code in val.coding:
                            Codeeable_obj = FhirCodeableConcept(DictToObject(
                                code), val.text, procedure_obj.fhir_proc_idn, 'procedure', key)
                            request.db.add(Codeeable_obj)
                    else:
                        Codeeable_obj = FhirCodeableConcept(DictToObject(
                            {}), val.text, procedure_obj.fhir_proc_idn, 'procedure', key)
                        request.db.add(Codeeable_obj)

                if type(val).__name__ == 'Annotation':
                    insert_to_FhirNote(
                        val, procedure_obj.fhir_proc_idn, 'procedure', key, request.db)

                if type(val).__name__ == 'Identifier':
                    insert_to_identifier(
                        val, procedure_obj.fhir_proc_idn, 'procedure', key, request.db)

        if type(procedure[key]).__name__ == 'Refrence':
            ref_obj = FhirReference(
                procedure[key], procedure_obj.fhir_proc_idn, 'procedure', key)
            request.db.add(ref_obj)

        if type(procedure[key]).__name__ == 'CodeableConcept':
            if procedure[key].coding != None:
                for code in procedure[key].coding:
                    Codeeable_obj = FhirCodeableConcept(DictToObject(
                        code), procedure[key].text, procedure_obj.fhir_proc_idn, 'procedure', key)
                    request.db.add(Codeeable_obj)
            else:
                Codeeable_obj = FhirCodeableConcept(DictToObject(
                    {}), procedure[key].text, procedure_obj.fhir_proc_idn, 'procedure', key)
                request.db.add(Codeeable_obj)

    role_obj = None
    actor_obj = None
    onBehalfOf_obj = None
    onBehalfOf_idn = None
    if procedure.performer != None:
        for performer in procedure.performer:
            actor_obj = FhirReference(performer.get(
                'actor'), procedure_obj.fhir_proc_idn, 'procedure', 'performer')
            request.db.add(actor_obj)
            request.db.flush()

            if performer.get('onBehalfOf') != None:
                onBehalfOf_obj = FhirReference(performer.get(
                    'onBehalfOf'), procedure_obj.fhir_proc_idn, 'procedure', 'performer')
                request.db.add(onBehalfOf_obj)
                request.db.flush()
                if onBehalfOf_obj.reference_idn != None:
                    onBehalfOf_idn = onBehalfOf_obj.reference_idn
                else:
                    onBehalfOf_idn = None

            if performer.get('role') != None:
                if performer.get('role').coding != None:
                    for code in performer.get('role').coding:
                        role_obj = FhirCodeableConcept(DictToObject(code), performer.get(
                            'role').text, procedure_obj.fhir_proc_idn, 'procedure', 'performer')
                        request.db.add(role_obj)
                        request.db.flush()
                        performer_obj = ProcPerformer(procedure_obj.fhir_proc_idn, role_obj.fhir_codeable_concept_idn,
                                                      actor_obj.reference_idn, onBehalfOf_idn)
                        request.db.add(performer_obj)
                else:
                    role_obj = FhirCodeableConcept(DictToObject({}), performer.get(
                        'role').text, procedure_obj.fhir_proc_idn, 'procedure', 'performer')
                    request.db.add(role_obj)
                    request.db.flush()
                    performer_obj = ProcPerformer(procedure_obj.fhir_proc_idn, role_obj.fhir_codeable_concept_idn,
                                                  actor_obj.reference_idn, onBehalfOf_idn)
                    request.db.add(performer_obj)

            else:
                performer_obj = ProcPerformer(
                    procedure_obj.fhir_proc_idn, None, actor_obj.reference_idn, onBehalfOf_idn)
                request.db.add(performer_obj)
    manipulated_obj = None
    action_obj = None
    if procedure.focalDevice != None:
        for focalDevice in procedure.focalDevice:
            manipulated_obj = FhirReference(focalDevice.get(
                'manipulated'), procedure_obj.fhir_proc_idn, 'procedure', 'focalDevice')
            request.db.add(manipulated_obj)
            request.db.flush()
            if focalDevice.get('action') != None:
                if focalDevice.get('action').coding != None:
                    for code in focalDevice.get('action').coding:
                        action_obj = FhirCodeableConcept(DictToObject(code), focalDevice.get(
                            'action').text, procedure_obj.fhir_proc_idn, 'procedure', 'focalDevice')
                        request.db.add(action_obj)
                        request.db.flush()
                        focalDevice_obj = ProcFocaldevice(
                            procedure_obj.fhir_proc_idn, action_obj.fhir_codeable_concept_idn, manipulated_obj.reference_idn)
                        request.db.add(focalDevice_obj)
                else:
                    action_obj = FhirCodeableConcept(DictToObject({}), focalDevice.get(
                        'action').text, procedure_obj.fhir_proc_idn, 'procedure', 'focalDevice')
                    request.db.add(action_obj)
                    request.db.flush()
                    focalDevice_obj = ProcFocaldevice(
                        procedure_obj.fhir_proc_idn, action_obj.fhir_codeable_concept_idn, manipulated_obj.reference_idn)
                    request.db.add(focalDevice_obj)

            else:
                focalDevice_obj = ProcFocaldevice(
                    procedure_obj.fhir_proc_idn, None, manipulated_obj.reference_idn)
                request.db.add(focalDevice_obj)

    request.db.flush()


def fetch_procedure(request):

    param_obj = request.swagger_data

    query = FhirProc.base_query_init(request)

    filtered_spec = []

    filtered_query = 0

    filtered_spec = []

    model_list = []

    ref_value_list = []

    code_value_list = []

    filtered_query = 0

    # attribute_value contain a dictionary of param names with associated table names
    attribute_value = {'FhirReference': [], 'FhirCodeableConcept': []}

    # generate_filters : Generates the filter using sqlalchemy filter lib
    def generate_filters():
        import pdb; pdb.set_trace()
        obj_model = {'model': '', 'field': '', 'op': '', 'value': ''}
        for key, val in param_obj.items():
            if param_obj[key] != None:
                obj_model['model'] = proc_query_params[key]['table']
                obj_model['field'] = proc_query_params[key]['col']
                obj_model['op'] = '=='
                obj_model['value'] = param_obj[key]

                model_list.append(obj_model['model'])
                if obj_model['model'] in ('FhirReference', 'FhirCodeableConcept'):
                    if key == 'based-on':
                        attribute_value[obj_model['model']].append('basedOn')
                    elif key == 'part-of':
                        attribute_value[obj_model['model']].append('partOf')
                    else:
                        attribute_value[obj_model['model']].append(key)
                    filtered_spec.append(obj_model)
                else:
                    filtered_spec.append(obj_model)

                if obj_model['model'] == 'FhirReference':
                    ref_value_list.append(param_obj[key])
                elif obj_model['model'] == 'FhirCodeableConcept':
                    code_value_list.append(param_obj[key])

                obj_model = {'model': '', 'field': '', 'op': '', 'value': ''}

    generate_filters()

    # generate_result : Generates result for GET query
    def generate_result(filtered_spec):
        if 'FhirCodeableConcept' in model_list:
            full_query = (query.outerjoin(FhirCodeableConcept, and_(FhirCodeableConcept.fhir_idn == FhirProc.fhir_proc_idn,
                                                                    FhirCodeableConcept.source == 'procedure', FhirCodeableConcept.attribute.in_(attribute_value['FhirCodeableConcept'])))
                          .filter(FhirCodeableConcept.code.in_(code_value_list)))

        if 'FhirReference' in model_list:
            full_query = query.outerjoin(FhirReference, and_(FhirReference.fhir_idn == FhirProc.fhir_proc_idn,
                                                         FhirReference.source == 'procedure', FhirReference.attribute.in_(attribute_value['FhirReference']))).filter(FhirReference.reference.in_(ref_value_list))

        if 'FhirCodeableConcept' and 'FhirReference' not in model_list:
            full_query = (query.outerjoin(FhirCodeableConcept, and_(FhirCodeableConcept.fhir_idn == FhirProc.fhir_proc_idn,
                                                                    FhirCodeableConcept.source == 'procedure'))
                          .outerjoin(FhirReference, and_(FhirReference.fhir_idn == FhirProc.fhir_proc_idn, FhirReference.source == 'procedure')))

        filtered_query = apply_filters(full_query, filtered_spec)
        result = filtered_query.all()
        return result

    result = generate_result(filtered_spec)
    return result

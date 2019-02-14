from db.model.immunization import(FhirImmunization, FhirQuantity,ImmunReaction,
                                    ImmunVaccinationProtocol)
from db.model.procedure import(
    FhirCodeableConcept, FhirReference, FhirIdentifier, FhirNote)
from utility.util import (DictToObject, to_json_obj)

from db.db_util import insert_to_source_specific_model,lookup_from_type_lookup_and_insert_to_corresponding_table
from db.common import(insert_to_identifier, insert_to_FhirNote, insert_to_CodeableConcept)
from db.model_query import immunization_base_query_init,generate_query
from apis.lookup import immunization_query_params
from sqlalchemy_filters import apply_filters
from .type_lookup import type_lookup

def insert_immunization(request):

    immunization = request.swagger_data['ImmunizationItem']
    immunization_payload = request.json_body
    immunization_obj = FhirImmunization(immunization, immunization_payload)
    request.db.add(immunization_obj)
    request.db.flush()
    import pdb; pdb.set_trace()
    for key, val in immunization_payload.items():
        if type(immunization[key]).__name__ == 'list':
            for val in immunization[key]:
                fn = type_lookup.get(type(val).__name__)
                if fn is not None:
                    fn(val, immunization_obj.fhir_immunization_idn, 'Immunization', key, request.db)
        fn = type_lookup.get(type(immunization[key]).__name__ )
        if fn is not None:
            fn(immunization[key], immunization_obj.fhir_immunization_idn, 'Immunization', key, request.db)

    if immunization.practitioner != None:
        for practitioner in immunization.practitioner:
            actor_obj = FhirReference(practitioner.get(
                'actor'), immunization_obj.fhir_immunization_idn, 'Immunization', 'practitioner', request.db)

            if practitioner.get('role') != None:
                insert_to_CodeableConcept(practitioner.get('role'),immunization_obj.fhir_immunization_idn,
                                            'Immunization','practitioner', request.db)

    if immunization.explanation != None:
        insert_to_source_specific_model(immunization.explanation,
                                        immunization_obj.fhir_immunization_idn,
                                        'Immunization',
                                        request.db)
    if immunization.reaction !=None:
        reaction = immunization.reaction
        for val in reaction:
            ImmunReaction(DictToObject(val),immunization_obj.fhir_immunization_idn,request.db)
            for key,values in val.items():
                lookup_from_type_lookup_and_insert_to_corresponding_table(values,
                                                                          immunization_obj.fhir_immunization_idn,
                                                                          'Immunization',
                                                                          key,
                                                                          request.db)
    if immunization.vaccinationProtocol != None:
        vacintn_prtcls = immunization.vaccinationProtocol
        for vacintn_prtcl in vacintn_prtcls:
            ImmunVaccinationProtocol(DictToObject(vacintn_prtcl),
                                    immunization_obj.fhir_immunization_idn,
                                    request.db)

            for key, val in vacintn_prtcl.items():
                if type(val).__name__ == 'list':
                    for values in val:
                        fn = type_lookup.get(type(values).__name__ )
                        lookup_from_type_lookup_and_insert_to_corresponding_table(values,
                                                                          immunization_obj.fhir_immunization_idn,
                                                                          'Immunization',
                                                                          key,
                                                                          request.db)
                lookup_from_type_lookup_and_insert_to_corresponding_table(values,
                                                                          immunization_obj.fhir_immunization_idn,
                                                                          'Immunization',
                                                                          key,
                                                                          request.db)
    request.db.flush()

def search_immunization(request):
    param_obj = request.swagger_data
    base_query = immunization_base_query_init(request)
    filtered_spec = generate_query(param_obj,immunization_query_params)
    filtered_query = apply_filters(base_query, filtered_spec)
    result = filtered_query.all()
    return to_json_obj(result)

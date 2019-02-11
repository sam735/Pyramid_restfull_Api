from db.model.immunization import(
    FhirImmunization, ImmunReaction, ImmunVaccinationProtocol, FhirQuantity)
from db.model.procedure import(
    FhirCodeableConcept, FhirReference, FhirIdentifier, FhirNote)
from sqlalchemy import and_


def immunization_base_query_init(request):
    query = (request.db.query(FhirImmunization.json_payload.distinct())
            .outerjoin(FhirIdentifier, and_(FhirIdentifier.fhir_idn == FhirImmunization.fhir_immunization_idn,
                                            FhirIdentifier.source == 'Immunization'))
            .outerjoin(FhirNote, and_(FhirNote.fhir_idn == FhirImmunization.fhir_immunization_idn,
                                      FhirNote.source == 'Immunization'))
            .outerjoin(ImmunReaction, and_(ImmunReaction.fhir_immunization_idn == FhirImmunization.
                                           fhir_immunization_idn))
            .outerjoin(ImmunVaccinationProtocol, and_(ImmunVaccinationProtocol.fhir_immunization_idn ==
                                                    FhirImmunization.fhir_immunization_idn))
            .outerjoin(FhirQuantity, and_(FhirQuantity.fhir_idn == FhirImmunization.fhir_immunization_idn,
                                            FhirQuantity.source == 'Immunization'))
            .outerjoin(FhirCodeableConcept, and_(FhirCodeableConcept.fhir_idn == 
                                            FhirImmunization.fhir_immunization_idn,
                                            FhirCodeableConcept.source == 'Immunization'))
            .outerjoin(FhirReference, and_(FhirReference.fhir_idn == FhirImmunization.fhir_immunization_idn,
                                            FhirReference.source == 'Immunization')))
    return query

def generate_query(param_obj,query_params):
    filtered_spec = []
    if param_obj != None:
        obj_model = {'model': '', 'field': '', 'op': '', 'value': ''}
        for key, val in param_obj.items():
            if param_obj.get(key) != None:
                obj_model['model'] = query_params[key]['table']
                obj_model['field'] = query_params[key]['col']
                obj_model['op'] = '=='
                obj_model['value'] =  param_obj[key]
                filtered_spec.append(obj_model)
    return filtered_spec
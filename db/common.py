from db.model.procedure import(
    FhirCodeableConcept, FhirNote, FhirIdentifier, FhirReference)
from utility.util import(DictToObject)


def insert_to_identifier(val, fhirIdn, source, key, session):
    type_idn = []
    if val.type != None:
        if val.type.get('coding') != None:
            for code in val.type.get('coding'):
                Codeeable_obj = FhirCodeableConcept(DictToObject(
                    code), val.type.get('text'), fhirIdn, source, key)
                session.add(Codeeable_obj)
                session.flush()
                type_idn.append(Codeeable_obj.fhir_codeable_concept_idn)
        else:
            Codeeable_obj = FhirCodeableConcept(
                DictToObject({}), val.text, fhirIdn, source, key)
            session.add(Codeeable_obj)
            session.flush()
            type_idn.append(Codeeable_obj.fhir_codeable_concept_idn)
    if len(type_idn) == 0:
        proc_identfr = FhirIdentifier(val, None, fhirIdn, source)
        session.add(proc_identfr)
    else:
        for idn in type_idn:
            proc_identfr = FhirIdentifier(val, None, fhirIdn, source)
            session.add(proc_identfr)



def insert_to_FhirNote(val, fhirIdn, source, key, session):
    authorReference = None
    if val.authorReference != None:
        ref_obj = FhirReference(val.authorReference, fhirIdn, source, key)
        session.add(ref_obj)
        session.flush()
        authorReference = ref_obj.code_FhirReference_idn
    Annotation_obj = FhirNote(authorReference, val, fhirIdn, source)
    session.add(Annotation_obj)

def insert_to_CodeableConcept(val, fhirIdn, source, key, session):
    if val.coding != None:
        for code in val.coding:
            Codeable_obj = FhirCodeableConcept(DictToObject(
                code), val.text, fhirIdn, source, key)
            session.add(Codeable_obj)
    else:
        Codeable_obj = FhirCodeableConcept(DictToObject(
            {}), val.text, fhirIdn, source, key)
        session.add(Codeable_obj)

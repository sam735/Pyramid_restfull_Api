from db.model.procedure import(
    FhirCodeableConcept, FhirReference, FhirIdentifier, FhirNote)
from db.model.immunization import(FhirImmunization, FhirQuantity,ImmunReaction,
                                    ImmunVaccinationProtocol)
from db.common import( insert_to_FhirNote, insert_to_CodeableConcept, insert_to_identifier)


type_lookup = {

	"Refrence":          FhirReference,
    "CodeableConcept":   insert_to_CodeableConcept,
    "Annotation":        insert_to_FhirNote,
    "Identifier":        insert_to_identifier,
    "Quantity":          FhirQuantity
}

from db.model.immunization import(FhirImmunization, FhirQuantity,ImmunReaction,
									ImmunVaccinationProtocol)
from db.model.procedure import(
	FhirCodeableConcept, FhirReference, FhirIdentifier, FhirNote)
from utility.util import (DictToObject, to_json_obj)

from db.common import(insert_to_identifier, insert_to_FhirNote)


def insert_immunization(request):

	immunization = request.swagger_data['ImmunizationItem']
	immunization_payload = request.json_body
	immunization_obj = FhirImmunization(immunization, immunization_payload)
	request.db.add(immunization_obj)
	request.db.flush()

	for key, val in immunization_payload.items():
		if type(immunization[key]).__name__ == 'list':
			for val in immunization[key]:
				if type(val).__name__ == 'Refrence':
					ref_obj = FhirReference(
						val, immunization_obj.fhir_immunization_idn, 'Immunization', key)
					request.db.add(ref_obj)
				if type(val).__name__ == 'CodeableConcept':
					if val.coding != None:
						for code in val.coding:
							Codeeable_obj = FhirCodeableConcept(DictToObject(
								code), val.text, immunization_obj.fhir_immunization_idn, 'Immunization', key)
							request.db.add(Codeeable_obj)
					else:
						Codeeable_obj = FhirCodeableConcept(DictToObject(
							{}), val.text, immunization_obj.fhir_immunization_idn, 'Immunization', key)
						request.db.add(Codeeable_obj)

				if type(val).__name__ == 'Annotation':
					insert_to_FhirNote(
						val, immunization_obj.fhir_immunization_idn, 'Immunization', key, request.db)

				if type(val).__name__ == 'Identifier':
					insert_to_identifier(
						val, immunization_obj.fhir_immunization_idn, 'Immunization', key, request.db)

		if type(immunization[key]).__name__ == 'Refrence':
			ref_obj = FhirReference(
				immunization[key], immunization_obj.fhir_immunization_idn, 'Immunization', key)
			request.db.add(ref_obj)

		if type(immunization[key]).__name__ == 'CodeableConcept':
			if immunization[key].coding != None:
				for code in immunization[key].coding:
					Codeeable_obj = FhirCodeableConcept(DictToObject(
						code), immunization[key].text, immunization_obj.fhir_immunization_idn, 'Immunization', key)
					request.db.add(Codeeable_obj)
			else:
				Codeeable_obj = FhirCodeableConcept(DictToObject(
					{}), immunization[key].text, immunization_obj.fhir_immunization_idn, 'Immunization', key)
				request.db.add(Codeeable_obj)

		if type(immunization[key]).__name__ == 'Quantity':
			dose_quantity = FhirQuantity(
				immunization[key], immunization_obj.fhir_immunization_idn, 'Immunization', key)
			request.db.add(dose_quantity)

	if immunization.practitioner != None:
		for practitioner in immunization.practitioner:
			actor_obj = FhirReference(practitioner.get(
				'actor'), immunization_obj.fhir_immunization_idn, 'Immunization', 'practitioner')
			request.db.add(actor_obj)

			if practitioner.get('role') != None:
				if practitioner.get('role').coding != None:
					for code in practitioner.get('role').coding:
						role_obj = FhirCodeableConcept(DictToObject(code), practitioner.get(
							'role').text, immunization_obj.fhir_immunization_idn, 'Immunization', 'practitioner')
						request.db.add(role_obj)
				else:
					role_obj = FhirCodeableConcept(DictToObject({}), practitioner.get(
						'role').text, immunization_obj.fhir_immunization_idn, 'Immunization', 'practitioner')
					request.db.add(role_obj)

	if immunization.explanation != None:
		explanation = immunization.explanation
		for key, val in explanation.items():
			if type(val).__name__ == 'list':
				for value in val:
					if type(value).__name__ == 'CodeableConcept':
						if value.coding != None:
							for code in value.coding:
								Codeeable_obj = FhirCodeableConcept(DictToObject(
									code), value.text, immunization_obj.fhir_immunization_idn, 'Immunization', 'explanation_' + key)
								request.db.add(Codeeable_obj)
						else:
							Codeeable_obj = FhirCodeableConcept(DictToObject(
								{}), value.text, immunization_obj.fhir_immunization_idn, 'Immunization', 'explanation_'+key)
							request.db.add(Codeeable_obj)

	if immunization.reaction !=None:
		reaction = immunization.reaction
		for val in reaction:
			reac_obj = ImmunReaction(DictToObject(val),immunization_obj.fhir_immunization_idn)
			request.db.add(reac_obj)
			for key,values in val.items():
				if type(values).__name__ == 'Refrence':
					ref_obj = FhirReference(values,immunization_obj.fhir_immunization_idn,
											'Immunization',key)
					request.db.add(ref_obj)

	if immunization.vaccinationProtocol != None:
		vacintn_prtcls = immunization.vaccinationProtocol
		for vacintn_prtcl in vacintn_prtcls:
			vacin_protocol = ImmunVaccinationProtocol(DictToObject(vacintn_prtcl),
													immunization_obj.fhir_immunization_idn)
			request.db.add(vacin_protocol)

			for key, val in vacintn_prtcl.items():
				if type(val).__name__ == 'list':
					for values in val:
						if type(values).__name__ == 'CodeableConcept':
							if values.coding != None:
								for code in values.coding:
									Codeeable_obj = FhirCodeableConcept(DictToObject(
										code), values.text, immunization_obj.fhir_immunization_idn,
										 'Immunization', key)
									request.db.add(Codeeable_obj)
							else:
								Codeeable_obj = FhirCodeableConcept(DictToObject(
									{}), values.text, immunization_obj.fhir_immunization_idn,
									 'Immunization', key)
								request.db.add(Codeeable_obj)

				if type(val).__name__ == 'CodeableConcept':
					if val.coding != None:
						for code in val.coding:
							Codeeable_obj = FhirCodeableConcept(DictToObject(
								code), val.text, immunization_obj.fhir_immunization_idn,
								 'Immunization', key)
							request.db.add(Codeeable_obj)
					else:
						Codeeable_obj = FhirCodeableConcept(DictToObject(
							{}), val.text, immunization_obj.fhir_immunization_idn,
							 'Immunization', key)
						request.db.add(Codeeable_obj)

				if type(val).__name__ == 'Refrence':
					ref_obj = FhirReference(
						val, immunization_obj.fhir_immunization_idn, 'Immunization', key)
					request.db.add(ref_obj)

	request.db.flush()
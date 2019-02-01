from db.model.allergies import (FhirAllergy, CodeYn, FhirCodeableConcept, Reference,FhirIdentifier, Annotation, AllergyReaction, AllergyCategory)


from utility.util import (DictToObject,to_json_obj)

from db.common import(insert_to_identifier,insert_to_annotation)

import json

from sqlalchemy_filters import apply_filters

from apis.lookup import allergy_query_params

from sqlalchemy import and_ 

def insert_allergies(request):
	

	allergies = request.swagger_data['body']
	allergies_payload = request.json_body
	allergies_obj = FhirAllergy(allergies,allergies_payload)  
	request.db.add(allergies_obj)
	request.db.flush()

	#Code to handle a list objects
	for key, val in allergies_payload.items():
		if type(allergies[key]).__name__ == 'list':
			for val in allergies[key]:
				if type(val).__name__ == 'Reference':
					ref_obj = Reference(val,allergies_obj.fhir_allergy_idn,'allergy',key)
					request.db.add(ref_obj)
				if type(val).__name__ == 'FhirCodeableConcept':
					if val.coding != None:
						for code in val.coding:
							Codeeable_obj = FhirCodeableConcept((code),val.text,allergies_obj.fhir_allergy_idn,'allergy',key)
							request.db.add(Codeeable_obj)
					else:
						Codeeable_obj = FhirCodeableConcept(DictToObject({}),val.text,allergies_obj.fhir_allergy_idn,'allergy',key)
						request.db.add(Codeeable_obj)

				if type(val).__name__ == 'Annotation':
					insert_to_annotation(val,allergies_obj.fhir_allergy_idn,'allergy',key,request.db)

				if type(val).__name__ == 'Identifier':
					insert_to_identifier(val,allergies_obj.fhir_allergy_idn,'allergy',key,request.db)

		if type(allergies[key]).__name__ == 'Reference':
			ref_obj = Reference(allergies[key],allergies_obj.fhir_allergy_idn,'allergy',key)
			request.db.add(ref_obj)

		if type(allergies[key]).__name__ == 'FhirCodeableConcept':
			if allergies[key].coding != None:
				for code in allergies[key].coding:
					Codeeable_obj = FhirCodeableConcept((code),allergies[key].text,allergies_obj.fhir_allergy_idn,'allergy',key)
					request.db.add(Codeeable_obj)
			else:
				Codeeable_obj = FhirCodeableConcept(DictToObject({}),allergies[key].text,allergies_obj.fhir_allergy_idn,'allergy',key)
				request.db.add(Codeeable_obj)

	category_obj = None

	if allergies.category != None:
		for category in allergies.category:
			category_obj = AllergyCategory(category,allergies_obj.fhir_allergy_idn)
			request.db.add(category_obj)
			request.db.flush()



	substance_obj = None
	manifestation_obj = None
	exposure_obj = None
	allergy_reaction_obj = None

	if allergies.reaction != None:
		for reaction in allergies.reaction:
			import pdb;pdb.set_trace()

			if reaction.get('description') or reaction.get('onset') or reaction.get('severity'):
				allergy_reaction_obj = AllergyReaction(((reaction.get('substance').coding[0].display if reaction.get('substance').coding else None) if reaction.get('substance') else None),reaction.get('onset'),reaction.get('severity'),allergies_obj.fhir_allergy_idn)
				request.db.add(allergy_reaction_obj)
				request.db.flush()
			
			if reaction.get('manifestation') != None:
				for obj in reaction.get('manifestation'):
					if obj.coding != None:
						for code in obj.coding:
							manifestation_obj = FhirCodeableConcept((code),code.display,allergies_obj.fhir_allergy_idn,'allergy','manifestation')
							request.db.add(manifestation_obj)
							request.db.flush()

			if reaction.get('exposureRoute') != None:
				if reaction.get('exposureRoute').coding != None:
					for code in reaction.get('exposureRoute').coding:
						exposure_obj = FhirCodeableConcept((code),code.display,allergies_obj.fhir_allergy_idn,'allergy','exposureRoute')
						request.db.add(exposure_obj)
						request.db.flush()

			if reaction.get('note') != None:
				for obj in reaction.get('note'):
					insert_to_annotation(obj,allergies_obj.fhir_allergy_idn,'allergy',key,request.db)
					request.db.flush()

			if reaction.get('substance') != None:
				if reaction.get('substance').coding != None:
					for code in reaction.get('substance').coding:
						substance_obj = FhirCodeableConcept((code),((reaction.get('substance').coding[0].display if reaction.get('substance').coding else None) if reaction.get('substance') else None),allergies_obj.fhir_allergy_idn,'allergy','substance')
						request.db.add(substance_obj)
						request.db.flush()
				else:
					substance_obj = FhirCodeableConcept(DictToObject({}),((reaction.get('substance').coding[0].display if reaction.get('substance').coding else None) if reaction.get('substance') else None),allergies_obj.fhir_allergy_idn,'allergy','substance')
					request.db.add(substance_obj)
					request.db.flush()

	request.db.flush()

def fetch_allergies(request):
	import pdb;pdb.set_trace()

	param_obj = request.swagger_data

	query = FhirAllergy.base_query_init(request)

	filtered_spec = []

	model_list = []

	ref_value_list = []

	code_value_list = []

	filtered_query = 0

	#attribute_value contain a dictionary of param names with associated table names
	attribute_value = {'Reference':[],'FhirCodeableConcept':[]}

	#generate_filters : Generates the filter using sqlalchemy filter lib
	def generate_filters():
		import pdb;pdb.set_trace()
		obj_model= {'model':'','field': '', 'op': '' ,'value': ''}
		for key,val in param_obj.items():
			if param_obj[key] != None:
				obj_model['model'] = allergy_query_params[key]['table']
				obj_model['field'] = allergy_query_params[key]['col']
				obj_model['op'] = '=='
				obj_model['value'] = param_obj[key]

				model_list.append(obj_model['model'])
				if obj_model['model'] in ('Reference', 'FhirCodeableConcept'):
					if key == 'route':
						attribute_value[obj_model['model']].append('exposureRoute')
					else:
						attribute_value[obj_model['model']].append(key)
				else:
					filtered_spec.append(obj_model)

				if obj_model['model'] == 'Reference':
					ref_value_list.append(param_obj[key])
				elif obj_model['model'] == 'FhirCodeableConcept':
					code_value_list.append(param_obj[key])
			   
				obj_model= {'model':'','field': '', 'op': '' ,'value': ''}
	
	generate_filters()

	#generate_result : Generates result for GET query
	def generate_result(filtered_spec):
		
		if 'CodeableConcept' in model_list:         
			query = (query.outerjoin(FhirCodeableConcept, and_(FhirCodeableConcept.fhir_idn == FhirAllergy.fhir_allergy_idn,
				FhirCodeableConcept.source == 'allergy', FhirCodeableConcept.attribute.in_(attribute_value['FhirCodeableConcept'])))
			.filter(FhirCodeableConcept.code.in_(code_value_list)))

		if 'Reference' in model_list:
			query = (query.outerjoin(Reference, and_(Reference.fhir_idn == FhirAllergy.fhir_allergy_idn,
				Reference.source == 'allergy', Reference.attribute.in_(attribute_value['Reference']))).filter(Reference.reference.in_(ref_value_list)))

		if 'CodeableConcept' and 'Reference' not in model_list:
			query = (query.outerjoin(FhirCodeableConcept, and_(FhirCodeableConcept.fhir_idn == FhirAllergy.fhir_allergy_idn,
									FhirCodeableConcept.source == 'allergy'))
							.outerjoin(Reference, and_(Reference.fhir_idn == FhirAllergy.fhir_allergy_idn,Reference.source == 'allergy')))


		filtered_query = apply_filters(query,filtered_spec)
		result = filtered_query.all()
		return result
		


	result = generate_result(filtered_spec)
	return result
	
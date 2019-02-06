from db.model.problems import (FhirCondition, CodeYn, FhirCodeableConcept, Reference,FhirIdentifier, Annotation)


from utility.util import (DictToObject,to_json_obj)

from db.common import(insert_to_identifier,insert_to_FhirNote)

import json

from sqlalchemy_filters import apply_filters

from apis.lookup import problem_query_params


from sqlalchemy import and_


def insert_problems(request):
	problem = request.swagger_data['problem']
	problem_payload = request.json_body
	problem_obj = FhirCondition(problem, problem_payload)
	request.db.add(problem_obj)
	request.db.flush()



	#Code to handle a list objects
	for key, val in problem_payload.items():
		if type(problem[key]).__name__ == 'list':
			for val in problem[key]:
				if type(val).__name__ == 'Reference':
					ref_obj = Reference(val,problem_obj.fhir_condition_idn,'problem',key)
					request.db.add(ref_obj)

				if type(val).__name__ == 'CodeableConcept':
					if val.coding != None:
						for code in val.coding:
							Codeeable_obj = FhirCodeableConcept((code),val.text,problem_obj.fhir_condition_idn,'problem',key)
							request.db.add(Codeeable_obj)
					else:
						Codeeable_obj = FhirCodeableConcept(DictToObject({}),val.text,problem_obj.fhir_condition_idn,'problem',key)
						request.db.add(Codeeable_obj)

				if type(val).__name__ == 'Annotation':
					insert_to_annotation(val,problem_obj.fhir_condition_idn,'problem',key,request.db)

				if type(val).__name__ == 'Identifier':
					insert_to_identifier(val,problem_obj.fhir_condition_idn,'problem',key,request.db)

		if type(problem[key]).__name__ == 'Reference':
			ref_obj = Reference(problem[key],problem_obj.fhir_condition_idn,'problem',key)
			request.db.add(ref_obj)

		if type(problem[key]).__name__ == 'CodeableConcept':
			if problem[key].coding != None:
				for code in problem[key].coding:
					Codeeable_obj = FhirCodeableConcept((code),problem[key].text,problem_obj.fhir_condition_idn,'problem',key)
					request.db.add(Codeeable_obj)
			else:
				Codeeable_obj = FhirCodeableConcept(DictToObject({}),problem[key].text,problem_obj.fhir_condition_idn,'problem',key)
				request.db.add(Codeeable_obj)

	stage_obj = None

	if problem.stage != None:
		if problem.stage.get('summary') != None:
			if problem.stage.get('summary').coding != None:
				for code in problem.stage.get('summary').coding:
					stage_obj = FhirCodeableConcept((code),code.display,problem_obj.fhir_condition_idn,'problem','stage')
					request.db.add(stage_obj)
					

		if problem.stage.get('assessment') != None:
			for obj in problem.stage.get('assessment'):
				if obj != None:
					stage_obj = Reference(obj,problem_obj.fhir_condition_idn,'problem',key)
					request.db.add(stage_obj)
					

	evidence_obj = None

	if problem.evidence != None:
		for obj in problem.evidence:
			if obj.get('code') != None:
				for code in obj.get('code'):
					for coding_obj in code.coding:
						evidence_obj = FhirCodeableConcept((coding_obj),coding_obj.display,problem_obj.fhir_condition_idn,'problem','evidence')
						request.db.add(evidence_obj)
			if obj.get('detail') != None:
				for code in obj.get('detail'): 
					evidence_obj = Reference(code,problem_obj.fhir_condition_idn,'problem','detail')
					request.db.add(evidence_obj)


	request.db.flush()
	
def fetch_problems(request):

	param_obj = request.swagger_data

	filtered_spec = []

	model_list = []

	ref_value_list = []

	code_value_list = []

	filtered_query = 0

	#attribute_value contain a dictionary of param names with associated table names
	attribute_value = {'Reference':[],'FhirCodeableConcept':[]}

	#generate_filters : Generates the filter using sqlalchemy filter lib
	def generate_filters():
		obj_model= {'model':'','field': '', 'op': '' ,'value': ''}
		for key,val in param_obj.items():
			if param_obj[key] != None:
				obj_model['model'] = problem_query_params[key]['table']
				obj_model['field'] = problem_query_params[key]['col']
				obj_model['op'] = '=='
				obj_model['value'] = param_obj[key]

				model_list.append(obj_model['model'])
				if obj_model['model'] in ('Reference', 'FhirCodeableConcept'):
					if key == 'body-site':
						attribute_value[obj_model['model']].append('bodySite')
					elif key == 'evidence-detail':
						attribute_value[obj_model['model']].append('detail')
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
		query = FhirCondition.base_query_init(request)

		if 'CodeableConcept' in model_list:         
			query = (query.outerjoin(FhirCodeableConcept, and_(FhirCodeableConcept.fhir_idn == FhirCondition.fhir_condition_idn,
				FhirCodeableConcept.source == 'problem', FhirCodeableConcept.attribute.in_(attribute_value['FhirCodeableConcept'])))
			.filter(FhirCodeableConcept.code.in_(code_value_list)))

		if 'Reference' in model_list:
			query = query.outerjoin(Reference, and_(Reference.fhir_idn == FhirCondition.fhir_condition_idn,
				Reference.source == 'problem', Reference.attribute.in_(attribute_value['Reference']))).filter(Reference.reference.in_(ref_value_list))

		if 'CodeableConcept' and 'Reference' not in model_list:
			query = (query.outerjoin(FhirCodeableConcept, and_(FhirCodeableConcept.fhir_idn == FhirCondition.fhir_condition_idn,
									FhirCodeableConcept.source == 'problem'))
						  .outerjoin(Reference, and_(Reference.fhir_idn == FhirCondition.fhir_condition_idn,Reference.source == 'problem')))


		filtered_query = apply_filters(query,filtered_spec)
		result = filtered_query.all()
		return result
		


	result = generate_result(filtered_spec)
	return result

				



	

	
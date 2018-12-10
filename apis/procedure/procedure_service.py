from apis.db.procedure_model import (CodeCodeableConcept,CodeRefrence,ProcedurePerformer,FhirProcedure,ProcedureFocaldevice,
										ProcedureIdentifier,ProcedureNote,ProcedureDefinition,ProcedureBasedon,ProcedurePartof,
										ProcedureRsnReference,ProcedureReport,ProcedureComplicationDetail,ProcedureUsedReference,
										ProcedureRsnCode,ProcedureBodySite,ProcedureComplication,ProcedureFollowup,ProcedureUsedCode)

from apis.util import (add_and_return_CodeCodeableConcept_obj_idn,add_and_return_idn_from_refrence_table,
						check_list_exist_and_return_values,DictToObject,insert_to_multivalue_ref_attribute_table)
from bunch import bunchify

def insert_procedure(request):
	procedure = request.swagger_data['ProcedureItem']
	
	notDoneReason_idn = []
	category_idn = []
	code_idn = []
	subject_idn = None
	context_idn = None
	location_idn = None
	outcome_idn = []
	if procedure.notDoneReason != None:
		if procedure.notDoneReason.coding != None:
			for code in procedure.notDoneReason.coding:
				notDoneReason_idn.append(add_and_return_CodeCodeableConcept_obj_idn(code,CodeCodeableConcept,request.db,
																				procedure.notDoneReason.text))
		else:
			notDoneReason_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																				procedure.notDoneReason.text))

	if procedure.category != None:
		import pdb;pdb.set_trace()
		if procedure.category.coding != None:
			for code in procedure.category.coding:
				category_idn.append(add_and_return_CodeCodeableConcept_obj_idn(code,CodeCodeableConcept,request.db,
																				procedure.category.text))
		else:
			category_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																				procedure.category.text))

	if procedure.code != None:
		if procedure.code.coding != None:
			for code in procedure.code.coding:
				code_idn.append(add_and_return_CodeCodeableConcept_obj_idn(code,CodeCodeableConcept,request.db,
																				procedure.code.text))
		else:
			code_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																				procedure.code.text))

	subject_idn = add_and_return_idn_from_refrence_table(procedure.subject,CodeRefrence,request.db)

	if procedure.context != None:
		context_idn = add_and_return_idn_from_refrence_table(procedure.context,CodeRefrence,request.db)

	if procedure.location != None:
		location_idn = add_and_return_idn_from_refrence_table(procedure.location,CodeRefrence,request.db)

	if procedure.outcome != None:
		if procedure.outcome.coding != None:
			for code in procedure.outcome.coding:
				outcome_idn.append(add_and_return_CodeCodeableConcept_obj_idn(code,CodeCodeableConcept,request.db,
																				procedure.outcome.text))
		else:
			outcome_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																				procedure.outcome.text))

	# procedure_obj =  FhirProcedure(procedure,notDoneReason_idn[0],category_idn[0],code_idn[0],
	# 								subject_idn,context_idn,location_idn,outcome_idn[0])
	procedure_obj =  FhirProcedure(procedure,check_list_exist_and_return_values(notDoneReason_idn)
									,check_list_exist_and_return_values(category_idn),
									check_list_exist_and_return_values(code_idn),
									subject_idn,context_idn,location_idn,check_list_exist_and_return_values(outcome_idn))
	request.db.add(procedure_obj)
	request.db.flush()

	type_coding_idn= []
	assigner_idn = None
	idntfr_idn = []
	
	if procedure.identifier != None:
		for idntfr in procedure.identifier:
			if idntfr.type != None:
				if idntfr.type.get('coding') != None:
					for type_coding in idntfr.type.get('coding'):
						type_coding_idn.append(add_and_return_CodeCodeableConcept_obj_idn(type_coding,CodeCodeableConcept,request.db,
																				idntfr.type.get('text')))
				else:
					type_coding_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																				idntfr.type.get('text')))
			if idntfr.assigner != None:
				assigner_idn = add_and_return_idn_from_refrence_table(DictToObject(idntfr.assigner),CodeRefrence,request.db)
			identifier = ProcedureIdentifier(procedure_obj.fhir_procedure_idn,idntfr.use,check_list_exist_and_return_values(type_coding_idn),idntfr.system,
												idntfr.value,idntfr.period.get('start'),idntfr.period.get('end'),assigner_idn)
			assigner_idn = None
			request.db.add(identifier)
			request.db.flush()
	
	if procedure.definition != None:
		for definition in procedure.definition:
			insert_to_multivalue_ref_attribute_table(definition,CodeRefrence,ProcedureDefinition,
													procedure_obj.fhir_procedure_idn,request.db)
	if procedure.basedOn !=None:
		for basedOn in procedure.basedOn:
			insert_to_multivalue_ref_attribute_table(basedOn,CodeRefrence,ProcedureBasedon,
													procedure_obj.fhir_procedure_idn,request.db)

	if procedure.partOf != None:
		for partOf in procedure.partOf:
			insert_to_multivalue_ref_attribute_table(partOf,CodeRefrence,ProcedurePartof,
													procedure_obj.fhir_procedure_idn,request.db)

	performr_role_idn = []
	performr_onBehalfOf_idn = None
	if procedure.performer:
		for performer in procedure.performer:
			if performer.get('role').get('coding'):
				for perfrm_coding in performer.get('role').get('coding'):
						performr_role_idn.append(add_and_return_CodeCodeableConcept_obj_idn(perfrm_coding,CodeCodeableConcept,request.db,
																				performer.get('role').get('text')))
			else:
				performr_role_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																				performer.get('role').get('text')))
			performr_actor_idn = add_and_return_idn_from_refrence_table(DictToObject(performer.get('actor')),CodeRefrence,request.db)
			if performer.get('onBehalfOf'):
				performr_onBehalfOf_idn = add_and_return_idn_from_refrence_table(DictToObject(performer.get('onBehalfOf')),CodeRefrence,request.db)
			performer = ProcedurePerformer(procedure_obj.fhir_procedure_idn,check_list_exist_and_return_values(performr_role_idn),
											performr_actor_idn,performr_onBehalfOf_idn)
			request.db.add(performer)
			request.db.flush()

	reasonCode_coding_idn = None
	if procedure.reasonCode != None:
		for reasonCode in procedure.reasonCode:
			if reasonCode.coding:
				for reasonCode_coding in reasonCode.coding:
					reasonCode_coding_idn = add_and_return_CodeCodeableConcept_obj_idn(reasonCode_coding,CodeCodeableConcept,request.db,
																					reasonCode.text)
			else:
				reasonCode_coding_idn = add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																					reasonCode.text)

			reasonCode_obj = ProcedureRsnCode(procedure_obj.fhir_procedure_idn,reasonCode_coding_idn)
			request.db.add(reasonCode_obj)
			request.db.flush()

	if procedure.reasonReference:
		for reasonReference in procedure.reasonReference:
			insert_to_multivalue_ref_attribute_table(reasonReference,CodeRefrence,ProcedureRsnReference,
													procedure_obj.fhir_procedure_idn,request.db)

	bodySite_coding_idn = None

	if procedure.bodySite:
		for bodySite in procedure.bodySite:
			if bodySite.coding:
				for bodySite_coding in bodySite.coding:
					bodySite_coding_idn = add_and_return_CodeCodeableConcept_obj_idn(bodySite_coding,CodeCodeableConcept,request.db,
																					bodySite.text)
			else:
				bodySite_coding_idn = add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
																					bodySite.text)

			bodySite_obj = ProcedureBodySite(procedure_obj.fhir_procedure_idn,bodySite_coding_idn)
			request.db.add(bodySite_obj)
			request.db.flush()
	import pdb;pdb.set_trace()	
	if procedure.report:
		for report in procedure.report:
			insert_to_multivalue_ref_attribute_table(report,CodeRefrence,ProcedureReport,procedure_obj.fhir_procedure_idn,request.db)
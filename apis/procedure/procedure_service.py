from db.model.procedure import (FhirProcedure,CodeYn,CodeCodeableConcept,CodeRefrence,ProcedurePerformer,
								ProcedureFocaldevice,FhirIdentifier,FhirNote)

from utility.util import (DictToObject,return_lower_case_of_string)

from db.common import(add_to_CodeCodeableConcept_table,add_to_refrence_table)


def insert_procedure(request):
	procedure = request.swagger_data['ProcedureItem']
	
	notDoneReason_idn = None
	import pdb;pdb.set_trace()
	if procedure.notDoneReason != None:
		if procedure.notDoneReason.coding != None:
			for code in procedure.notDoneReason.coding:
				add_to_CodeCodeableConcept_table(code,CodeCodeableConcept,request.db,notDoneReason_idn,
												procedure.notDoneReason.text)
		else:
			add_to_CodeCodeableConcept_table({},CodeCodeableConcept,request.db,notDoneReason_idn,
												procedure.notDoneReason.text)

	category_idn = None
	if procedure.category != None:
		idn = fetch_max_of_column_idn(CodeCodeableConcept,request.db)
		category_idn = idn +1
		if procedure.category.coding != None:
			for code in procedure.category.coding:
				add_to_CodeCodeableConcept_table(code,CodeCodeableConcept,request.db,category_idn,
												procedure.category.text)
		else:
			add_to_CodeCodeableConcept_table({},CodeCodeableConcept,request.db,category_idn,
												procedure.category.text)

	code_idn = None
	if procedure.code != None:
		idn = fetch_max_of_column_idn(CodeCodeableConcept,request.db)
		code_idn = idn + 1
		if procedure.code.coding != None:
			for code in procedure.code.coding:
				add_to_CodeCodeableConcept_table(code,CodeCodeableConcept,request.db,code_idn,
												procedure.code.text)
		else:
			add_to_CodeCodeableConcept_table({},CodeCodeableConcept,request.db,code_idn,
												procedure.code.text)

	idn = fetch_max_of_column_idn(CodeRefrence,request.db)
	subject_idn = idn +1
	add_to_refrence_table(procedure.subject,subject_idn,CodeRefrence,request.db)

	context_idn = None
	if procedure.context != None:
		idn = fetch_max_of_column_idn(CodeRefrence,request.db)
		procedure_context_idn = idn +1
		add_to_refrence_table(procedure.context,procedure_context_idn,CodeRefrence,request.db)

	location_idn = None
	if procedure.location != None:
		idn = fetch_max_of_column_idn(CodeRefrence,request.db)
		location_idn = idn +1
		add_to_refrence_table(procedure.location,location_idn,CodeRefrence,request.db)

	outcome_idn = None
	if procedure.outcome != None:
		idn = fetch_max_of_column_idn(CodeCodeableConcept,request.db)
		outcome_idn = idn + 1
		if procedure.outcome.coding != None:
			for code in procedure.outcome.coding:
				add_to_CodeCodeableConcept_table(code,CodeCodeableConcept,request.db,outcome_idn,
												procedure.outcome.text)
		else:
			add_to_CodeCodeableConcept_table({},CodeCodeableConcept,request.db,outcome_idn,
												procedure.outcome.text)
	# type_coding_idn= []
	# assigner_idn = None
	# idntfr_idn = []
	
	# if procedure.identifier != None:
	# 	for idntfr in procedure.identifier:
	# 		if idntfr.type != None:
	# 			if idntfr.type.get('coding') != None:
	# 				for type_coding in idntfr.type.get('coding'):
	# 					type_coding_idn.append(add_and_return_CodeCodeableConcept_obj_idn(type_coding,CodeCodeableConcept,request.db,
	# 																			idntfr.type.get('text')))
	# 			else:
	# 				type_coding_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
	# 																			idntfr.type.get('text')))
	# 		if idntfr.assigner != None:
	# 			assigner_idn = add_and_return_idn_from_refrence_table(DictToObject(idntfr.assigner),CodeRefrence,request.db)
	# 		identifier = ProcedureIdentifier(procedure_obj.fhir_procedure_idn,idntfr.use,check_list_exist_and_return_values(type_coding_idn),idntfr.system,
	# 											idntfr.value,idntfr.period.get('start'),idntfr.period.get('end'),assigner_idn)
	# 		assigner_idn = None
	# 		request.db.add(identifier)
	# 		request.db.flush()
	
	# if procedure.definition != None:
	# 	for definition in procedure.definition:
	# 		insert_to_multivalue_ref_attribute_table(definition,CodeRefrence,ProcedureDefinition,
	# 												procedure_obj.fhir_procedure_idn,request.db)

	basedOn_idn = None
	if procedure.basedOn !=None:
		idn = fetch_max_of_column_idn(CodeRefrence,request.db)
		basedOn_idn = idn +1 
		for basedOn in procedure.basedOn:
			add_to_refrence_table(basedOn,basedOn_idn,CodeRefrence,request.db)

	partOf_idn = None
	if procedure.partOf != None:
		idn = fetch_max_of_column_idn(CodeRefrence,request.db)
		partOf_idn = idn +1
		for partOf in procedure.partOf:
			add_to_refrence_table(partOf,partOf_idn,CodeRefrence,request.db)

	reasonCode_idn = None
	if procedure.reasonCode != None:
		idn  = idn = fetch_max_of_column_idn(CodeCodeableConcept,request.db)
		reasonCode_idn = idn + 1
		if procedure.reasonCode.coding != None:
			for code in procedure.reasonCode.coding:
				add_to_CodeCodeableConcept_table(code,CodeCodeableConcept,request.db,outcome_idn,
												procedure.outcome.text)
		else:
			add_to_CodeCodeableConcept_table({},CodeCodeableConcept,request.db,outcome_idn,
												procedure.outcome.text)
		

	procedure_obj = FhirProcedure(procedure,notDoneReason_idn,category_idn,code_idn,subject_idn,context_idn,
									location_idn,outcome_idn,basedOn_idn,partOf_idn)

	request.db.add(procedure_obj)
	request.db.flush()
	print(procedure_obj.fhir_procedure_idn)

	# performr_role_idn = []
	# performr_onBehalfOf_idn = None
	# if procedure.performer:
	# 	for performer in procedure.performer:
	# 		if performer.get('role').get('coding'):
	# 			for perfrm_coding in performer.get('role').get('coding'):
	# 					performr_role_idn.append(add_and_return_CodeCodeableConcept_obj_idn(perfrm_coding,CodeCodeableConcept,request.db,
	# 																			performer.get('role').get('text')))
	# 		else:
	# 			performr_role_idn.append(add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
	# 																			performer.get('role').get('text')))
	# 		performr_actor_idn = add_and_return_idn_from_refrence_table(DictToObject(performer.get('actor')),CodeRefrence,request.db)
	# 		if performer.get('onBehalfOf'):
	# 			performr_onBehalfOf_idn = add_and_return_idn_from_refrence_table(DictToObject(performer.get('onBehalfOf')),CodeRefrence,request.db)
	# 		performer = ProcedurePerformer(procedure_obj.fhir_procedure_idn,check_list_exist_and_return_values(performr_role_idn),
	# 										performr_actor_idn,performr_onBehalfOf_idn)
	# 		request.db.add(performer)
	# 		request.db.flush()

	# reasonCode_coding_idn = None
	# if procedure.reasonCode != None:
	# 	for reasonCode in procedure.reasonCode:
	# 		if reasonCode.coding:
	# 			for reasonCode_coding in reasonCode.coding:
	# 				reasonCode_coding_idn = add_and_return_CodeCodeableConcept_obj_idn(reasonCode_coding,CodeCodeableConcept,request.db,
	# 																				reasonCode.text)
	# 		else:
	# 			reasonCode_coding_idn = add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
	# 																				reasonCode.text)

	# 		reasonCode_obj = ProcedureRsnCode(procedure_obj.fhir_procedure_idn,reasonCode_coding_idn)
	# 		request.db.add(reasonCode_obj)
	# 		request.db.flush()

	# if procedure.reasonReference:
	# 	for reasonReference in procedure.reasonReference:
	# 		insert_to_multivalue_ref_attribute_table(reasonReference,CodeRefrence,ProcedureRsnReference,
	# 												procedure_obj.fhir_procedure_idn,request.db)

	# bodySite_coding_idn = None

	# if procedure.bodySite:
	# 	for bodySite in procedure.bodySite:
	# 		if bodySite.coding:
	# 			for bodySite_coding in bodySite.coding:
	# 				bodySite_coding_idn = add_and_return_CodeCodeableConcept_obj_idn(bodySite_coding,CodeCodeableConcept,request.db,
	# 																				bodySite.text)
	# 		else:
	# 			bodySite_coding_idn = add_and_return_CodeCodeableConcept_obj_idn({},CodeCodeableConcept,request.db,
	# 																				bodySite.text)

	# 		bodySite_obj = ProcedureBodySite(procedure_obj.fhir_procedure_idn,bodySite_coding_idn)
	# 		request.db.add(bodySite_obj)
	# 		request.db.flush()
	# import pdb;pdb.set_trace()	
	# if procedure.report:
	# 	for report in procedure.report:
	# 		insert_to_multivalue_ref_attribute_table(report,CodeRefrence,ProcedureReport,procedure_obj.fhir_procedure_idn,request.db)
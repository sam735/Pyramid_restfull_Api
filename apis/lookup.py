from db.model.procedure import (FhirCodeableConcept,Reference,Annotation)



classLookup = {"Reference": Reference,
			   "Annotation": Annotation,
				"FhirCodeableConcept": FhirCodeableConcept
			}

param_column_lookup = {
	"based-on"	: ["FhirCodeableConcept","attribute"],
	"category":["FhirCodeableConcept",],
	"code": ["FhirCodeableConcept",],
	"context": ["Reference",],
	"date": ["FhirProcedure","perfome_start_dt"],
	"encounter": ["Reference",],
	"identifier": ["FhirIdentifier",],
	"location": ["Reference",],
	"part-of": ["Reference",],
	"patient": ["Reference","reference"],
	"performer": ["Reference",],
	"status": ["FhirProcedure","proc_status"],
	"subject": ["Reference","reference"],
	"definition": ["Reference",]
}

proc_query_params = {

		"identifier": 		{"table" : "FhirIdentifier","fhir_id":"fhir_idn","type":"","col":"value"},
		"date": 			{"table" : "FhirProcedure","type":"","col":"perfome_start_dt"},
		"status": 			{"table" : "FhirProcedure","fhir_id":"fhir_idn","type":"","col":"proc_status"},		
		"category":			{"table" : "FhirCodeableConcept","fhir_id":"","type":"attribute","col":"reference"},
		"code": 			{"table" : "FhirCodeableConcept","fhir_id":"fhir_id","type":"attribute","col":"reference"},
		"context": 			{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"based-on"	: 		{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"encounter": 		{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},		
		"location": 		{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"part-of": 			{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"patient": 			{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"performer": 		{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},		
		"subject": 			{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"definition": 		{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"}
	}

allergy_query_params = {

		"identifier":   		{"table" : "FhirIdentifier","fhir_id":"","type":"","col":"value"},
		"clinical-status":		{"table" : "FhirAllergy","fhir_id":"fhir_allergy_idn","type":"","col":"clinical_status"},
		"criticality":  		{"table" : "FhirAllergy","fhir_id":"fhir_allergy_idn","type":"","col":"criticality"},
		"date":					{"table" : "FhirAllergy","fhir_id":"fhir_allergy_idn","type":"","col":"asserted_date"},
		"last-date":			{"table" : "FhirAllergy","fhir_id":"fhir_allergy_idn","type":"","col":"last_occurrence"},
		"type":					{"table" : "FhirAllergy","fhir_id":"fhir_allergy_idn","type":"","col":"type"},
		"verification-status":	{"table" : "FhirAllergy","fhir_id":"fhir_allergy_idn","type":"","col":"verification_status"},
		"asserter":				{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"category":				{"table" : "AllergyCategory","fhir_id":"fhir_allergy_idn","type":"","col":"category"},
		"onset":				{"table" : "AllergyReaction","fhir_id":"","type":"","col":"onset"},
		"severity":	    		{"table" : "AllergyReaction","fhir_id":"","type":"","col":"severity"},
		"code":					{"table" : "FhirCodeableConcept","fhir_id":"fhir_id","type":"attribute","col":"code"},	
		"manifestation":		{"table" : "FhirCodeableConcept","fhir_id":"fhir_id","type":"attribute","col":"code"},	
		"route":				{"table" : "FhirCodeableConcept","fhir_id":"fhir_id","type":"attribute","col":"code"},
		"patient":				{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
		"recorder":	    		{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"}	
	
}

problem_query_params =  {

	"identifier":				{"table" : "FhirIdentifier","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"abatement-age"	:		    {"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"","col":"abatement_age"},
	"abatement-boolean":		{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"","col":"abatement_boolean"},
	"abatement-date":			{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"","col":"abatement_datetime"},	
	"abatement-string":			{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"","col":"abatement_string"},	
	"asserted-date":			{"table" : "FhirCondition","fhir_id":"fhir_idn","type":"","col":"asserted_date"},	
	"verification-status":		{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"","col":"verification_status"},
	"stage":					{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"","col":"stage"},
	"onset-date":				{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"attribute","col":"onset_date"},
	"onset-info":				{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"attribute","col":"onset_string"},
	"clinical-status":			{"table" : "FhirCondition","fhir_id":"fhir_condition_idn","type":"attribute","col":"clinical_status"},
	"asserter":					{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"context":					{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"encounter":				{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"evidence-detail":			{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"patient":					{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"subject":					{"table" : "Reference","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"body-site":				{"table" : "FhirCodeableConcept","fhir_id":"fhir_idn","type":"attribute","col":"reference"},
	"category":					{"table" : "FhirCodeableConcept","fhir_id":"fhir_idn","type":"attribute","col":"reference"},	
	"code":						{"table" : "FhirCodeableConcept","fhir_id":"fhir_idn","type":"attribute","col":"code"},	
	"evidence":					{"table" : "FhirCodeableConcept","fhir_id":"fhir_idn","type":"attribute","col":"reference"},	
	"severity":					{"table" : "FhirCodeableConcept","fhir_id":"fhir_idn","type":"attribute","col":"reference"}		
}

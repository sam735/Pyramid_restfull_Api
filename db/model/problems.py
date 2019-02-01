from datetime import datetime
from sqlalchemy import (Table, Column, BigInteger,SmallInteger,CHAR,String, DateTime,ForeignKey,Integer,Numeric,Boolean)
from sqlalchemy.orm import relationship,backref
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from utility.util import convertStringToDateTime

class CodeYn(Base):
	__tablename__ = 'code_yn'

	yn_cd = Column(CHAR(1, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
	description = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	crt_dt = Column(DateTime)
	upd_dt = Column(DateTime)
	user_idn = Column(Numeric(18, 0))
	is_default = Column(CHAR(1, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	is_required = Column(CHAR(1, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	source = Column(String(15, u'SQL_Latin1_General_CP1_CI_AS'))
	yn_idn = Column(Numeric(18, 0), nullable=False)


class FhirCondition(Base):
	__tablename__ = 'fhir_condition'

	fhir_condition_idn = Column(Integer, primary_key=True)
	extn_id = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	clinical_status = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	verification_status = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	onset_datetime = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	onset_age = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	onset_period = Column(DateTime)
	onset_string = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	abatement_datetime = Column(DateTime)
	abatement_boolean = Column(CHAR(1, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	abatement_age = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	abatement_period = Column(DateTime)
	abatement_string = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	asserted_date = Column(DateTime)
	stage = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	json_payload = Column(String())
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))


	def __init__(self,problem,jsonPayload):
		import pdb;pdb.set_trace()
		self.extn_id = problem.id
		self.clinical_status = problem.clinicalStatus
		self.verification_status = problem.verificationStatus
		self.onset_datetime = convertStringToDateTime(problem.onsetDateTime)
		self.onset_age = problem.onsetAge
		self.onset_period = convertStringToDateTime(problem.onsetPeriod)
		self.onset_string = problem.onsetString
		self.onset_range = convertStringToDateTime(problem.onsetRange)
		self.abatement_datetime = convertStringToDateTime(problem.abatementDateTime)
		self.abatement_age = problem.abatementAge
		self.abatement_boolean = (problem.abatementBoolean)
		self.abatement_period = convertStringToDateTime(problem.abatementPeriod)
		self.abatement_string =(problem.abatementString)
		self.asserted_date = convertStringToDateTime(problem.assertedDate)
		self.json_payload = str(jsonPayload)
		self.user_idn = 2

	def base_query_init(request):
		query = (request.db.query(FhirCondition.json_payload.distinct())
					.outerjoin(FhirIdentifier, and_(FhirIdentifier.fhir_idn == FhirCondition.fhir_condition_idn,
													FhirIdentifier.source == 'problem'))
					.outerjoin(Annotation, and_(Annotation.fhir_idn == FhirCondition.fhir_condition_idn,
											Annotation.source =='problem')))
					
		return query


class FhirCodeableConcept(Base):
	__tablename__ = 'fhir_codeable_concept'
	
	fhir_codeable_concept_idn = Column(Integer, primary_key=True)
	fhir_idn = Column(Numeric(18, 0), nullable=False)
	source = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	attribute = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	codeable_system = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	codeable_version = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
	code = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
	display = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	user_selected = Column(BIT)
	code_text = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

	code_yn = relationship(u'CodeYn')

	def __init__(self,codeObj,text,fhir_idn,source,attribute):
		import pdb;pdb.set_trace()
		self.codeable_system = codeObj.system
		self.codeable_version = codeObj.version
		self.code = codeObj.code
		self.display = codeObj.display
		self.user_selected = codeObj.userSelected
		self.fhir_idn = fhir_idn
		self.source = source
		self.attribute = attribute
		self.code_text = text
		self.user_idn = 2

class Reference(Base):
	__tablename__ = 'fhir_reference'

	reference_idn = Column(Integer, primary_key=True)
	fhir_idn = Column(Numeric(18, 0), nullable=False)
	source = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	attribute = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	reference = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
	display = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

	code_yn = relationship(u'CodeYn')

	def __init__(self,refObj = None,fhir_idn = None,source = None,attribute = None):
		self.reference = refObj.reference
		self.display = refObj.display
		self.source = source
		self.attribute = attribute
		self.fhir_idn = fhir_idn
		self.user_idn = 2


class FhirIdentifier(Base):
	__tablename__ = 'fhir_identifier'
	import pdb;pdb.set_trace()

	fhir_identifier_idn = Column(Integer, primary_key=True)
	fhir_idn = Column(Numeric(18, 0),nullable=False)
	source = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	use = Column(String(15, u'SQL_Latin1_General_CP1_CI_AS'))
	type = Column(Numeric(18, 0))
	identifier_system = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	value = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	identifier_start_dt = Column(DateTime)
	identifier_end_dt = Column(DateTime)
	assigner = Column(Numeric(18, 0))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

	code_yn = relationship(u'CodeYn')

	def __init__(self,idntfr,proc_type,fhir_idn,source):

		self.fhir_idn = fhir_idn
		self.source = source
		self.use = idntfr.use
		self.type = 'allergy'
		self.identifier_system = idntfr.system
		self.value = idntfr.value
		self.identifier_start_dt = convertStringToDateTime(idntfr.period.get('start')) if idntfr.period else None
		self.identifier_end_dt = convertStringToDateTime(idntfr.period.get('end')) if idntfr.period else None
		self.assigner = None
		self.user_idn = 2


class Annotation(Base):
	__tablename__ = 'fhir_note'

	fhir_note_idn = Column(Integer, primary_key=True)
	fhir_idn = Column(Numeric(18, 0))
	author_reference = Column(Numeric(18, 0))
	author_string = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
	note_crt_dt = Column(DateTime)
	note_text = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	source = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'))
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

	code_yn = relationship(u'CodeYn')

	def __init__(self,author_reference = None,note = None,fhir_idn = None, source = None):
		self.fhir_idn = fhir_idn
		self.author_reference = author_reference
		self.author_string = note.authorString
		self.note_crt_dt = convertStringToDateTime(note.time) 
		self.note_text = note.text
		self.source = source
		self.user_idn = 2



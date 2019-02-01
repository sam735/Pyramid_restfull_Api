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


class FhirAllergy(Base):
	__tablename__ = 'fhir_allergy'

	fhir_allergy_idn = Column(Integer, primary_key=True)
	extn_id = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	clinical_status = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	verification_status = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	type = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	criticality = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	onset_datetime = Column(DateTime)
	onset_age = Column(Integer)
	onset_period = Column(DateTime)
	onset_range = Column(DateTime)
	onset_string = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	asserted_date = Column(DateTime)
	last_occurrence = Column(DateTime)
	json_payload = Column(String())
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

	code_yn = relationship(u'CodeYn')

	def __init__(self,allergies,jsonPayload):
		import pdb;pdb.set_trace()
		self.extn_id = allergies.id
		self.clinical_status = allergies.clinicalStatus
		self.verification_status = allergies.verificationStatus
		self.type = allergies.type
		self.criticality = allergies.criticality
		self.onset_datetime = convertStringToDateTime(allergies.onsetDateTime)
		self.onset_age = allergies.onsetAge
		self.onset_period = convertStringToDateTime(allergies.onsetPeriod)
		self.onset_range = convertStringToDateTime(allergies.onsetRange)
		self.onset_string = allergies.onsetString
		self.asserted_date = convertStringToDateTime(allergies.assertedDate)
		self.last_occurrence = convertStringToDateTime(allergies.lastOccurrence)
		self.json_payload = str(jsonPayload)
		self.user_idn = 2

	def base_query_init(request):
		query = (request.db.query(FhirAllergy.json_payload)
					.outerjoin(FhirIdentifier, and_(FhirIdentifier.fhir_idn == FhirAllergy.fhir_allergy_idn,
													FhirIdentifier.source == 'allergy'))
					.outerjoin(Annotation, and_(Annotation.fhir_idn == FhirAllergy.fhir_allergy_idn,
											Annotation.source =='allergy'))
					.outerjoin(AllergyReaction, and_(AllergyReaction.fhir_allergy_idn == FhirAllergy.fhir_allergy_idn))
					.outerjoin(AllergyCategory, and_(AllergyCategory.fhir_allergy_idn == FhirAllergy.fhir_allergy_idn)))
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
	user_idn = Column(Numeric(18, 0), nullable=False)
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

class AllergyReaction(Base):
	__tablename__ = 'allergy_reaction'

	allergy_reaction_idn = Column(Integer, primary_key=True)
	fhir_allergy_idn = Column(ForeignKey(u'fhir_allergy.fhir_allergy_idn'), nullable=False)
	description = Column(String(2000, u'SQL_Latin1_General_CP1_CI_AS'))
	onset = Column(DateTime)
	severity = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

	def __init__(self,description,onset,severity ,fhir_idn):
		self.fhir_allergy_idn =  fhir_idn
		self.description = description
		self.onset = onset
		self.severity = severity
		self.user_idn = 2

class AllergyCategory(Base):
	__tablename__ = 'allergy_category'

	allergy_category_idn = Column(Integer,primary_key=True)
	fhir_allergy_idn = Column(ForeignKey(u'fhir_allergy.fhir_allergy_idn'), nullable=False)
	category = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

	def __init__(self,category,fhir_idn):
		self.fhir_allergy_idn =  fhir_idn
		self.category = category
		self.user_idn = 2

from datetime import datetime
from sqlalchemy import (Table, Column, BigInteger, SmallInteger,
						CHAR, String, DateTime, ForeignKey, Integer, Numeric, Boolean)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from utility.util import convertStringToDateTime


class CodeYn(Base):
	__tablename__ = 'code_yn'

	yn_cd = Column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
	description = Column(
		String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	crt_dt = Column(DateTime)
	upd_dt = Column(DateTime)
	user_idn = Column(Numeric(18, 0))
	is_default = Column(
		CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	is_required = Column(
		CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	source = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
	yn_idn = Column(Numeric(18, 0), nullable=False)


class FhirImmunization(Base):
	__tablename__ = 'fhir_immunization'

	fhir_immunization_idn = Column(Integer, primary_key=True)
	extn_id = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
	status = Column(
		String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	not_given = Column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	date = Column(DateTime)
	primary_source = Column(
		CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	lotNumber = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
	expiration_date = Column(DateTime)
	json_payload = Column(String())
	crt_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	upd_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey('code_yn.yn_cd'),
						   nullable=False, server_default=("('Y')"))

	code_yn = relationship('CodeYn')

	def __init__(self, immunization, jsonPayload):
		self.status = immunization.status
		self.not_given = immunization.notGiven
		self.date = convertStringToDateTime(immunization.date)
		self.primary_source = immunization.primarySource
		self.lotNumber = immunization.lotNumber
		self.expiration_date =convertStringToDateTime(
			immunization.expirationDate)
		self.json_payload = str(jsonPayload)
		self.user_idn = 2


class ImmunReaction(Base):
	__tablename__ = 'immun_reaction'

	immun_reaction_idn = Column(Integer, primary_key=True)
	fhir_immunization_idn = Column(ForeignKey(
		'fhir_immunization.fhir_immunization_idn'), nullable=False)
	date = Column(DateTime)
	reported = Column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'))
	crt_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	upd_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey('code_yn.yn_cd'),
						   nullable=False, server_default=("('Y')"))

	code_yn = relationship('CodeYn')

	def __init__(self,reaction,fhir_immunization_idn):
		self.fhir_immunization_idn = fhir_immunization_idn
		self.date = convertStringToDateTime(reaction.date)
		self.reported = reaction.reported
		self.user_idn = 2


class ImmunVaccinationProtocol(Base):
	__tablename__ = 'immun_vaccination_protocol'

	immun_vaccination_protocol_idn = Column(Integer, primary_key=True)
	fhir_immunization_idn = Column(ForeignKey(
		'fhir_immunization.fhir_immunization_idn'), nullable=False)
	does_sequence = Column(Numeric(18, 0), nullable=False)
	description = Column(
		String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	series = Column(
		String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	series_doses = Column(Numeric(18, 0), nullable=False)
	crt_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	upd_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey('code_yn.yn_cd'),
						   nullable=False, server_default=("('Y')"))

	code_yn = relationship('CodeYn')
	fhir_immunization = relationship('FhirImmunization')

	def __init__(self,vacination,fhir_immunization_idn):
		self.fhir_immunization_idn = fhir_immunization_idn
		self.does_sequence = vacination.doseSequence
		self.description = vacination.description
		self.series = vacination.series
		self.series_doses = vacination.seriesDoses
		self.user_idn = 2


class FhirQuantity(Base):
	__tablename__ = 'fhir_quantity'

	fhir_quantity_idn = Column(Integer, primary_key=True)
	fhir_idn = Column(Numeric(18, 0), nullable=False)
	source = Column(
		String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	attribute = Column(
		String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
	value = Column(Numeric(18, 2))
	comparator = Column(CHAR(2, 'SQL_Latin1_General_CP1_CI_AS'))
	unit = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
	system = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
	code = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
	crt_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	upd_dt = Column(DateTime, nullable=False,
					server_default=("(getutcdate())"))
	user_idn = Column(Numeric(18, 0), nullable=False)
	entity_active = Column(ForeignKey('code_yn.yn_cd'),
						   nullable=False, server_default=("('Y')"))

	code_yn = relationship('CodeYn')

	def __init__(self, doseQuantity, fhir_idn, source, attribute):
		self.fhir_idn = fhir_idn
		self.source = source
		self.attribute = attribute
		self.value = doseQuantity.value
		self.comparator = doseQuantity.comparator
		self.unit = doseQuantity.unit
		self.system = doseQuantity.system
		self.code = doseQuantity.code
		self.user_idn = 2

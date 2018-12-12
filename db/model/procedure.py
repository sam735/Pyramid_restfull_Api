from datetime import datetime
from sqlalchemy import (Table, Column, BigInteger,SmallInteger,CHAR,String, DateTime,ForeignKey,Integer,Numeric,Boolean)
from sqlalchemy.orm import relationship,backref
from sqlalchemy.dialects.mssql import BIT

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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


class FhirProcedure(Base):
    __tablename__ = 'fhir_procedure'

    fhir_procedure_idn = Column(Integer,primary_key=True)
    extn_id = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'))
    proc_status = Column(String(20, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    not_done = Column(BIT)
    perfome_start_dt = Column(DateTime)
    perfome_end_dt = Column(DateTime)
    fhir_identifier_idn = Column(Numeric(18, 0))
    fhir_note_idn = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship(u'CodeYn')
    def __init__(self,procedure,fhir_identifier_idn = None,fhir_note_idn = None):
        self.extn_id = procedure.id
        self.proc_status = procedure.status
        self.not_done = procedure.notDone
        self.perfome_start_dt = procedure.performedDateTime
        self.perfome_start_dt = procedure.performedPeriod.start
        self.perfome_end_dt = procedure.performedPeriod.end
        self.fhir_identifier_idn = fhir_identifier_idn
        self.fhir_note_idn = fhir_note_idn
        self.user_idn = 2

class CodeCodeableConcept(Base):
    __tablename__ = 'code_codeable_concept'
    
    codeable_concept_idn = Column(Integer, primary_key=True)
    fhir_idn = Column(Numeric(18, 0), nullable=False)
    source = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    attribute = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    codeable_system = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    codeable_version = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    code = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    user_selected = Column(BIT)
    code_text = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship(u'CodeYn')

class CodeRefrence(Base):
    __tablename__ = 'code_refrence'

    code_refrence_idn = Column(Integer, primary_key=True)
    fhir_idn = Column(Numeric(18, 0), nullable=False)
    source = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    attribute = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    refrence = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship(u'CodeYn')

class ProcedurePerformer(Base):
    __tablename__ = 'procedure_performer'

    proc_perfome_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey(u'fhir_procedure.fhir_procedure_idn'))
    proc_role = Column(Numeric(18, 0))
    proc_actor = Column(Numeric(18, 0), nullable=False)
    proc_onbehalf = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship(u'CodeYn')
    fhir_procedure = relationship(u'FhirProcedure')

class ProcedureFocaldevice(Base):
    __tablename__ = 'procedure_focaldevice'

    proc_focaldevice_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey(u'fhir_procedure.fhir_procedure_idn'))
    proc_action = Column(Numeric(18, 0))
    proc_manipulated = Column(Numeric(18, 0), nullable=False)
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship(u'CodeYn')
    fhir_procedure = relationship(u'FhirProcedure')

class FhirIdentifier(Base):
    __tablename__ = 'fhir_identifier'

    fhir_identifier_idn = Column(Integer, primary_key=True)
    proc_use = Column(String(15, u'SQL_Latin1_General_CP1_CI_AS'))
    proc_type = Column(Numeric(18, 0))
    identifier_system = Column(String(15, u'SQL_Latin1_General_CP1_CI_AS'))
    proc_value = Column(String(15, u'SQL_Latin1_General_CP1_CI_AS'))
    identifier_start_dt = Column(DateTime)
    identifier_end_dt = Column(DateTime)
    proc_assigner = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship(u'CodeYn')

class FhirNote(Base):
    __tablename__ = 'fhir_note'

    fhir_note_idn = Column(Integer, primary_key=True)
    author_reference = Column(Numeric(18, 0))
    author_string = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    note_crt_dt = Column(DateTime)
    note_text = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey(u'code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship(u'CodeYn')
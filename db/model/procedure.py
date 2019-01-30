from datetime import datetime
from sqlalchemy import (Table, Column, BigInteger, SmallInteger,
                        CHAR, String, DateTime, ForeignKey, Integer, Numeric, Boolean)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mssql import BIT

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from utility.util import convertStringToDateTime


class CodeYn(Base):
    __tablename__ = 'code_yn'

    yn_cd = Column(CHAR(1, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    description = Column(
        String(100, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    crt_dt = Column(DateTime)
    upd_dt = Column(DateTime)
    user_idn = Column(Numeric(18, 0))
    is_default = Column(
        CHAR(1, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    is_required = Column(
        CHAR(1, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    source = Column(String(15, u'SQL_Latin1_General_CP1_CI_AS'))
    yn_idn = Column(Numeric(18, 0), nullable=False)


class FhirProc(Base):
    __tablename__ = 'fhir_proc'

    fhir_proc_idn = Column(Integer, primary_key=True)
    extn_id = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    proc_status = Column(
        String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    not_done = Column(BIT)
    perfomer_start_dt = Column(DateTime)
    perfomer_end_dt = Column(DateTime)
    json_payload = Column(String())
    crt_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    upd_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'),
                           nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')

    def __init__(self, procedure, jsonPayload):

        self.extn_id = procedure.id
        self.proc_status = procedure.status
        self.not_done = procedure.notDone
        self.perfomer_start_dt = convertStringToDateTime(
            procedure.performedDateTime)
        self.perfomer_start_dt = convertStringToDateTime(
            procedure.performedPeriod.start) if procedure.performedPeriod else None
        self.perfomer_end_dt = convertStringToDateTime(
            procedure.performedPeriod.end) if procedure.performedPeriod else None
        self.json_payload = str(jsonPayload)
        self.user_idn = 2


class FhirCodeableConcept(Base):
    """ changed codeable_concept_idn"""
    __tablename__ = 'fhir_codeable_concept'

    fhir_codeable_concept_idn = Column(Integer, primary_key=True)
    fhir_idn = Column(Numeric(18, 0), nullable=False)
    source = Column(
        String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    attribute = Column(
        String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    codeable_system = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    codeable_version = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    code = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    user_selected = Column(BIT)
    code_text = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    crt_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    upd_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'),
                           nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')

    def __init__(self, codeObj=None, text=None, fhir_idn=None, source=None, attribute=None):

        self.codeable_system = codeObj.system
        self.codeable_version = codeObj.version
        self.code = codeObj.code
        self.display = codeObj.display
        self.user_selected = codeObj.userSelected
        self.fhir_idn = fhir_idn
        self.source = source
        self.code_text = text
        self.attribute = attribute
        self.user_idn = 2


class FhirReference(Base):
    """ changed code_refrence_idn"""
    __tablename__ = 'fhir_reference'

    reference_idn = Column(Integer, primary_key=True)
    fhir_idn = Column(Numeric(18, 0), nullable=False)
    source = Column(
        String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    attribute = Column(
        String(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    reference = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    crt_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    upd_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'),
                           nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')

    def __init__(self, refObj=None, fhir_idn=None, source=None, attribute=None):
        self.reference = refObj.reference
        self.display = refObj.display
        self.source = source
        self.attribute = attribute
        self.fhir_idn = fhir_idn
        self.user_idn = 2


class ProcPerformer(Base):
    """Idn name changed only"""
    __tablename__ = 'proc_performer'

    proc_perfomer_idn = Column(Integer, primary_key=True)
    fhir_proc_idn = Column(ForeignKey('fhir_proc.fhir_proc_idn'))
    proc_role = Column(Numeric(18, 0))
    proc_actor = Column(Numeric(18, 0), nullable=False)
    proc_onbehalf = Column(Numeric(18, 0))
    crt_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    upd_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'),
                           nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    fhir_proc = relationship('FhirProc')

    def __init__(self, fhir_proc_idn=None, proc_role=None, proc_actor=None, proc_onbehalf=None):
        self.fhir_proc_idn = fhir_proc_idn
        self.proc_role = proc_role
        self.proc_actor = proc_actor
        self.proc_onbehalf = proc_onbehalf
        self.user_idn = 2


class ProcFocaldevice(Base):
    """changed fhir_procedure_idn"""
    __tablename__ = 'proc_focaldevice'

    proc_focaldevice_idn = Column(Integer, primary_key=True)
    fhir_proc_idn = Column(ForeignKey('fhir_proc.fhir_proc_idn'))
    proc_action = Column(Numeric(18, 0))
    proc_manipulated = Column(Numeric(18, 0), nullable=False)
    crt_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    upd_dt = Column(DateTime, nullable=False,
                    server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'),
                           nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    fhir_proc = relationship('FhirProc')

    def __init__(self, fhir_proc_idn=None, proc_action=None, proc_manipulated=None):
        self.fhir_proc_idn = fhir_proc_idn
        self.proc_action = proc_action
        self.proc_manipulated = proc_manipulated
        self.user_idn = 2


class FhirIdentifier(Base):
    __tablename__ = 'fhir_identifier'

    fhir_identifier_idn = Column(Integer, primary_key=True)
    fhir_idn = Column(Numeric(18, 0), nullable=False)
    source = Column(
        String(200, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    use = Column(String(15, u'SQL_Latin1_General_CP1_CI_AS'))
    type = Column(Numeric(18, 0))
    identifier_system = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    value = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    identifier_start_dt = Column(DateTime)
    identifier_end_dt = Column(DateTime)
    assigner = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'),
                           nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')

    def __init__(self, idntfr=None, proc_type=None, fhir_idn=None, source=None):

        self.fhir_idn = fhir_idn
        self.source = source
        self.use = idntfr.use
        self.type = proc_type
        self.identifier_system = idntfr.system
        self.value = idntfr.value
        self.identifier_start_dt = convertStringToDateTime(
            idntfr.period.get('start')) if idntfr.period else None
        self.identifier_end_dt = convertStringToDateTime(
            idntfr.period.get('end')) if idntfr.period else None
        self.assigner = None
        self.user_idn = 2


class FhirNote(Base):
    __tablename__ = 'fhir_note'

    fhir_note_idn = Column(Integer, primary_key=True)
    fhir_idn = Column(Numeric(18, 0))
    author_reference = Column(Numeric(18, 0))
    author_string = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    note_crt_dt = Column(DateTime)
    note_text = Column(String(100, u'SQL_Latin1_General_CP1_CI_AS'))
    source = Column(String(200, u'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'),
                           nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')

    def __init__(self, author_reference=None, note=None, fhir_idn=None, source=None):
        self.fhir_idn = fhir_idn
        self.author_reference = author_reference
        self.author_string = note.authorString
        self.note_crt_dt = convertStringToDateTime(note.time)
        self.note_ = note.text
        self.source = source
        self.user_idn = 2

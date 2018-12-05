from datetime import datetime
from sqlalchemy import (Table, Column, BigInteger,SmallInteger,CHAR,String, DateTime,ForeignKey,Integer,Numeric,Boolean)
from apis.db import Base
from sqlalchemy.orm import relationship


class CodeCodeableConcept(Base):
    __tablename__ = 'code_codeable_concept'

    codeable_concept_idn = Column(Numeric(18, 0), primary_key=True)
    system = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    version = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    code = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    user_selected = Column(Boolean)
    code_text = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    # code_yn = relationship('CodeYn')

class CodeRefrence(Base):
    __tablename__ = 'code_refrence'

    refrence_idn = Column(Numeric(18, 0), primary_key=True)
    refrence = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')

class FhirProcedure(Base):
    __tablename__ = 'fhir_procedure'

    fhir_procedure_idn = Column(Numeric(18, 0), primary_key=True)
    proc_status = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    not_done = Column(Boolean)
    not_done_reason = Column(Numeric(18, 0))
    category = Column(Numeric(18, 0))
    proc_code = Column(Numeric(18, 0))
    proc_subject = Column(Numeric(18, 0))
    proc_context = Column(Numeric(18, 0))
    perfome_start_dt = Column(DateTime)
    perfome_end_dt = Column(DateTime)
    proc_location = Column(Numeric(18, 0))
    proc_outcome = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')

class ProcedurePerformer(Base):
    __tablename__ = 'procedure_performer'

    proc_perfome_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    proc_role = Column(Numeric(18, 0))
    proc_actor = Column(Numeric(18, 0), nullable=False)
    proc_onbehalf = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureFocaldevice(Base):
    __tablename__ = 'procedure_focaldevice'

    proc_focaldevice_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    proc_action = Column(Numeric(18, 0))
    proc_manipulated = Column(Numeric(18, 0), nullable=False)
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureIdentifier(Base):
    __tablename__ = 'procedure_identifier'

    proc_identifier_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    proc_use = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    proc_type = Column(Numeric(18, 0))
    identifier_system = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    proc_value = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    identifier_start_dt = Column(DateTime)
    identifier_end_dt = Column(DateTime)
    proc_assigner = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureNote(Base):
    __tablename__ = 'procedure_note'

    proc_note_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    author_reference = Column(Numeric(18, 0))
    author_string = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    # not  crt_dt = Column(DateTime)
    note_text = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureDefinition(Base):
    __tablename__ = 'procedure_definition'

    proc_definition_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')
    code_refrence = relationship('CodeRefrence')

class ProcedureBasedon(Base):
    __tablename__ = 'procedure_basedon'

    proc_basedon_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')
    code_refrence = relationship('CodeRefrence')

class ProcedurePartof(Base):
    __tablename__ = 'procedure_partof'

    proc_partof_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')
    code_refrence = relationship('CodeRefrence')

class ProcedureRsnReference(Base):
    __tablename__ = 'procedure_rsn_reference'

    proc_rsn_reference_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')
    code_refrence = relationship('CodeRefrence')

class ProcedureReport(Base):
    __tablename__ = 'procedure_report'

    proc_report_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')
    code_refrence = relationship('CodeRefrence')

class ProcedureComplicationDetail(Base):
    __tablename__ = 'procedure_complication_detail'

    proc_complication_detail_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(Numeric(18, 0))
    refrence_idn = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')

class ProcedureUsedReference(Base):
    __tablename__ = 'procedure_used_reference'

    proc_used_reference_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')
    code_refrence = relationship('CodeRefrence')

class ProcedureRsnCode(Base):
    __tablename__ = 'procedure_rsn_code'

    proc_rsn_code_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    code_codeable_concept = relationship('CodeCodeableConcept')
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureBodySite(Base):
    __tablename__ = 'procedure_body_site'

    proc_body_site_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))
    code_codeable_concept = relationship('CodeCodeableConcept')
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureComplication(Base):
    __tablename__ = 'procedure_complication'

    proc_complication_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    code_codeable_concept = relationship('CodeCodeableConcept')
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureFollowup(Base):
    __tablename__ = 'procedure_followup'

    proc_followup_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    code_codeable_concept = relationship('CodeCodeableConcept')
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')

class ProcedureUsedCode(Base):
    __tablename__ = 'procedure_used_code'

    proc_used_code_idn = Column(Numeric(18, 0), primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    code_codeable_concept = relationship('CodeCodeableConcept')
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure')
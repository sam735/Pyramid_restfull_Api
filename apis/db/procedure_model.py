from datetime import datetime
from sqlalchemy import (Table, Column, BigInteger,SmallInteger,CHAR,String, DateTime,ForeignKey,Integer,Numeric,Boolean)
from apis.db import Base
from sqlalchemy.orm import relationship,backref

class CodeYn(Base):
    __tablename__ = 'code_yn'

    yn_cd = Column(CHAR(1,'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    description = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    user_idn = Column(Numeric(18, 0))
    is_default = Column(CHAR(1,'SQL_Latin1_General_CP1_CI_AS'))
    is_required = Column(CHAR(1,'SQL_Latin1_General_CP1_CI_AS'))
    source = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    yn_idn = Column(Numeric(18, 0))

class CodeCodeableConcept(Base):
    __tablename__ = 'code_codeable_concept'

    codeable_concept_idn = Column(Integer, primary_key=True,autoincrement=True)
    system = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    version = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    code = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    user_selected = Column(Boolean)
    code_text = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    codeable_group_idn = Column(Numeric(18,0))
    # crt_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))
    code_yn = relationship('CodeYn')
    def __init__(self,system = None,version = None,code = None,display = None, userSelected = None,codeable_group_idn = None,code_text=None):
        self.system = system
        self.version = version
        self.code = code
        self.display = display
        self.user_selected = userSelected
        self.code_text = code_text
        self.codeable_group_idn = codeable_group_idn
        self.user_idn = 2

class CodeRefrence(Base):
    __tablename__ = 'code_refrence'

    refrence_idn = Column(Integer, primary_key=True)
    refrence = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    display = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))
    code_yn = relationship('CodeYn')

    def __init__(self,refrence = None, display = None):
        self.refrence = refrence
        self.display = display
        self.user_idn = 2

class FhirProcedure(Base):
    __tablename__ = 'fhir_procedure'

    fhir_procedure_idn = Column(Integer, primary_key=True)
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
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))
    code_yn = relationship('CodeYn')
    def __init__(self,procedure,not_done_reason_idn = None,category_idn = None,proc_code_idn = None,proc_subject_idn = None,proc_context_idn = None,proc_location_idn = None,proc_outcome_idn = None):
        self.proc_status = procedure.status
        self.not_done = procedure.notDone
        self.perfome_start_dt = procedure.performedDateTime
        self.perfome_start_dt = procedure.performedPeriod.start
        self.perfome_end_dt = procedure.performedPeriod.end
        self.not_done_reason = not_done_reason_idn
        self.category = category_idn
        self.proc_code = proc_code_idn
        self.proc_subject = proc_subject_idn
        self.proc_context = proc_context_idn
        self.proc_location = proc_location_idn
        self.proc_outcome = proc_outcome_idn
        self.user_idn = 2



class ProcedurePerformer(Base):
    __tablename__ = 'procedure_performer'

    proc_perfome_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    proc_role = Column(Numeric(18, 0))
    proc_actor = Column(Numeric(18, 0), nullable=False)
    proc_onbehalf = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    def __init__(self,procedure_idn = None, proc_role = None,proc_actor = None, proc_onbehalf = None):
        self.fhir_procedure_idn = procedure_idn
        self.proc_role = proc_role
        self.proc_actor = proc_actor
        self.proc_onbehalf = proc_onbehalf
        self.user_idn = 2

    fhir_procedure = relationship('FhirProcedure',backref = backref('procedure_assoc'))

class ProcedureFocaldevice(Base):
    __tablename__ = 'procedure_focaldevice'

    proc_focaldevice_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    proc_action = Column(Numeric(18, 0))
    proc_manipulated = Column(Numeric(18, 0), nullable=False)
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    def __init__(self,proc_action = None, proc_manipulated = None):
        self.proc_action = proc_action
        self.proc_manipulated = proc_manipulated
        self.user_idn = 2

    fhir_procedure = relationship('FhirProcedure',backref = backref('procedure_Focaldevice'))

class ProcedureIdentifier(Base):
    __tablename__ = 'procedure_identifier'

    proc_identifier_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    proc_use = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    proc_type = Column(Numeric(18, 0))
    identifier_system = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    proc_value = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    identifier_start_dt = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    identifier_end_dt = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    proc_assigner = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    def __init__(self,fhir_procedure_idn = None,proc_use = None,proc_type=None,identifier_system = None,proc_value=None,identifier_start_dt = None,identifier_end_dt=None,proc_assigner=None):
        self.fhir_procedure_idn = fhir_procedure_idn
        self.proc_use = proc_use
        self.proc_type = proc_type
        self.identifier_system = identifier_system
        self.proc_value = self.proc_value
        self.identifier_start_dt = identifier_start_dt
        self.identifier_end_dt = identifier_end_dt
        self.proc_assigner = proc_assigner
        self.user_idn = 2

    fhir_procedure = relationship('FhirProcedure',backref = backref('procedure_Identifier'))

class ProcedureNote(Base):
    __tablename__ = 'procedure_note'

    proc_note_idn = Column(Integer, primary_key=True)
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
    def __init__(self,author_reference = None,author_string = None, note_text = None):
        self.author_reference = author_reference
        self.author_string = author_string
        self.note_text = note_text
        self.user_idn = 2
    fhir_procedure = relationship('FhirProcedure',backref = backref('procedure_Note'))

class ProcedureDefinition(Base):
    __tablename__ = 'procedure_definition'

    proc_definition_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref = backref('procedure_Definition'))
    code_refrence = relationship('CodeRefrence', backref = backref('CodeRefrence_assoc'))

    def __init__(self,fhir_procedure_idn,refrence_idn):
        self.fhir_procedure_idn = fhir_procedure_idn
        self.refrence_idn = refrence_idn
        self.user_idn = 2

class ProcedureBasedon(Base):
    __tablename__ = 'procedure_basedon'

    proc_basedon_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_Basedon'))
    code_refrence = relationship('CodeRefrence', backref =backref('CodeRefrence_Basedon'))

    def __int__(self,fhir_procedure_idn,refrence_idn):
        self.fhir_procedure_idn = fhir_procedure_idn
        self.refrence_idn = refrence_idn
        self.user_idn = 2

class ProcedurePartof(Base):
    __tablename__ = 'procedure_partof'

    proc_partof_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_Partof'))
    code_refrence = relationship('CodeRefrence', backref =backref('CodeRefrence_Partof'))

    def __int__(self,fhir_procedure_idn,refrence_idn):
        self.fhir_procedure_idn = fhir_procedure_idn
        self.refrence_idn = refrence_idn
        self.user_idn = 2
        
class ProcedureRsnReference(Base):
    __tablename__ = 'procedure_rsn_reference'

    proc_rsn_reference_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_RsnReference'))
    code_refrence = relationship('CodeRefrence', backref =backref('CodeRefrence_RsnReference'))

    def __int__(self,fhir_procedure_idn,refrence_idn):
        self.fhir_procedure_idn = fhir_procedure_idn
        self.refrence_idn = refrence_idn
        self.user_idn = 2

class ProcedureReport(Base):
    __tablename__ = 'procedure_report'

    proc_report_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))

    code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_Report'))
    code_refrence = relationship('CodeRefrence', backref =backref('CodeRefrence_Report'))

    def __int__(self,fhir_procedure_idn,refrence_idn):
        self.fhir_procedure_idn = fhir_procedure_idn
        self.refrence_idn = refrence_idn
        self.user_idn = 2

class ProcedureComplicationDetail(Base):
    __tablename__ = 'procedure_complication_detail'

    proc_complication_detail_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(Numeric(18, 0))
    refrence_idn = Column(Numeric(18, 0))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    # fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_ComplicationDetail'))
    # code_refrence = relationship('CodeRefrence', backref =backref('CodeRefrence_ComplicationDetail'))

class ProcedureUsedReference(Base):
    __tablename__ = 'procedure_used_reference'

    proc_used_reference_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    refrence_idn = Column(ForeignKey('code_refrence.refrence_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_UsedReference'))
    code_refrence = relationship('CodeRefrence', backref =backref('CodeRefrence_UsedReference'))

class ProcedureRsnCode(Base):
    __tablename__ = 'procedure_rsn_code'

    proc_rsn_code_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))
    code_yn = relationship('CodeYn')
    code_codeable_concept = relationship('CodeCodeableConcept',backref =backref('CodeCodeableConcept_RsnCode'))
    fhir_procedure = relationship('FhirProcedure', backref = backref('procedure_RsnCode'))

    def __init__(self,procedure_idn = None,code_idn = None):
        self.fhir_procedure_idn = procedure_idn
        self.codeable_concept_idn = code_idn
        self.user_idn = 2


class ProcedureBodySite(Base):
    __tablename__ = 'procedure_body_site'

    proc_body_site_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=("('Y')"))
    code_codeable_concept = relationship('CodeCodeableConcept', backref = backref('CodeCodeableConcept_BodySite'))
    code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref = backref('procedure_BodySite'))
    def __init__(self,procedure_idn = None,code_idn = None):
        self.fhir_procedure_idn = procedure_idn
        self.codeable_concept_idn = code_idn
        self.user_idn = 2

class ProcedureComplication(Base):
    __tablename__ = 'procedure_complication'

    proc_complication_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    code_codeable_concept = relationship('CodeCodeableConcept',backref = backref('CodeCodeableConcept_Complication'))
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure', backref =backref('procedure_Complication'))

class ProcedureFollowup(Base):
    __tablename__ = 'procedure_followup'

    proc_followup_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    code_codeable_concept = relationship('CodeCodeableConcept',backref = backref('CodeCodeableConcept_Followup'))
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_Followup'))

class ProcedureUsedCode(Base):
    __tablename__ = 'procedure_used_code'

    proc_used_code_idn = Column(Integer, primary_key=True)
    fhir_procedure_idn = Column(ForeignKey('fhir_procedure.fhir_procedure_idn'))
    codeable_concept_idn = Column(ForeignKey('code_codeable_concept.codeable_concept_idn'))
    # crt_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    # upd_dt = Column(DateTime, nullable=False, server_default=text("(getutcdate())"))
    user_idn = Column(Numeric(18, 0), nullable=False)
    # entity_active = Column(ForeignKey('code_yn.yn_cd'), nullable=False, server_default=text("('Y')"))

    code_codeable_concept = relationship('CodeCodeableConcept',backref = backref('CodeCodeableConcept_Usedcode'))
    # code_yn = relationship('CodeYn')
    fhir_procedure = relationship('FhirProcedure',backref =backref('procedure_Usedcode'))
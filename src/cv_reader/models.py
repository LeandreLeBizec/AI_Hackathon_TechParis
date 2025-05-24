from pydantic import BaseModel, field_validator
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

# Basic Info Models
class BasicInfo(BaseModel):
    candidate_name: Optional[str] = None
    analysis_timestamp: datetime
    company_name: str
    processing_time_seconds: float

# Phase 1: Initial Screening Models
class BreakdownScores(BaseModel):
    technical_skills: int
    experience_level: int
    industry_relevance: int
    culture_alignment: int

class FitAssessment(BaseModel):
    overall_fit_score: int
    recommendation: str
    justification: str
    breakdown: BreakdownScores

class IdentifiedGap(BaseModel):
    category: str
    gap: str
    severity: str
    impact_on_role: str
    mitigation_strategy: str

class TechnicalGapAnalysis(BaseModel):
    hiring_risk: str
    overall_assessment: str
    identified_gaps: List[IdentifiedGap]
    strengths: List[str]

class ScreeningDecision(BaseModel):
    proceed_to_next_phase: bool
    priority_level: str
    notes_for_recruiter: str

class Phase1InitialScreening(BaseModel):
    fit_assessment: FitAssessment
    technical_gap_analysis: TechnicalGapAnalysis
    screening_decision: ScreeningDecision

# Phase 2: HR Behavioral Models
class CompanyContext(BaseModel):
    company_description: str
    key_values: List[str]

class BehavioralQuestion(BaseModel):
    question: str
    tests_value: str
    what_to_look_for: str
    follow_up_areas: List[str]

class HRInterviewGuidance(BaseModel):
    focus_areas: List[str]
    red_flags_to_watch: List[str]
    estimated_duration: str

class Phase2HRBehavioral(BaseModel):
    company_context: CompanyContext
    behavioral_questions: List[BehavioralQuestion]
    interview_guidance: HRInterviewGuidance

# Phase 3: Technical Interview Models
class TechnicalQuestion(BaseModel):
    type: str
    question: str
    focus_area: str
    difficulty: str
    expected_depth: str
    follow_up_questions: Optional[List[str]] = None
    relates_to_gaps: Optional[List[str]] = None
    time_allocation: Optional[str] = None

class TechnicalInterviewGuidance(BaseModel):
    focus_areas: List[str]
    gap_specific_probes: List[str]
    estimated_duration: str

class Phase3TechnicalInterview(BaseModel):
    technical_questions: List[TechnicalQuestion]
    interview_guidance: TechnicalInterviewGuidance

# Recruiter Summary Models
class RecruiterSummary(BaseModel):
    overall_recommendation: str
    key_strengths: List[str]
    areas_of_concern: List[str]
    interview_priorities: List[str]
    onboarding_recommendations: List[str]
    decision_confidence: str

# Main Response Model
class CandidateAnalysis(BaseModel):
    basic_info: BasicInfo

class CVAnalysisResponse(BaseModel):
    candidate_analysis: CandidateAnalysis
    phase_1_initial_screening: Phase1InitialScreening
    phase_2_hr_behavioral: Phase2HRBehavioral
    phase_3_technical_interview: Phase3TechnicalInterview
    recruiter_summary: RecruiterSummary

# Legacy models for other endpoints
class ErrorResponse(BaseModel):
    error: str
    detail: str
    status: str

class CompanyListResponse(BaseModel):
    companies: List[str]
    count: int

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime 
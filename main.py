from datetime import datetime
from typing import List, Optional, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from model_api import (
    Policy, PolicyAcceptance, TrainingModuleRef,
    UserProfile, TrainingAssignment, QuizAttempt,
    can_start_training, suggest_modules_for_user,
    grade_attempt, compute_user_progress,
)

app = FastAPI(title="Training Model API")


# =========================================
# Pydantic Models
# =========================================

class PolicyModel(BaseModel):
    id: str
    scope: str
    company_id: Optional[str] = None
    version: str
    title: str


class PolicyAcceptanceModel(BaseModel):
    user_id: str
    policy_id: str
    accepted_at: datetime


class TrainingModuleRefModel(BaseModel):
    id: str
    title: str
    topic: str
    tags: List[str]


class UserProfileModel(BaseModel):
    user_id: str
    roles: List[str]
    department: Optional[str] = None


class TrainingAssignmentModel(BaseModel):
    id: str
    user_id: str
    module_id: str
    created_at: datetime
    status: str


class QuizAttemptModel(BaseModel):
    assignment_id: str
    score_pct: float
    passed: bool
    attempted_at: datetime


class CanStartTrainingRequest(BaseModel):
    user_id: str
    company_id: str
    latest_platform_policy: Optional[PolicyModel] = None
    latest_company_policy: Optional[PolicyModel] = None
    acceptances: List[PolicyAcceptanceModel]


class SuggestModulesRequest(BaseModel):
    user: UserProfileModel
    modules: List[TrainingModuleRefModel]
    max_results: int = 5


class GradeQuizRequest(BaseModel):
    quiz: List[Dict]
    user_answers: Dict[str, str]
    pass_mark: int = 80


class ProgressRequest(BaseModel):
    assignments: List[TrainingAssignmentModel]
    attempts: List[QuizAttemptModel]


# =========================================
# API Endpoints
# =========================================

@app.post("/can-start-training")
def can_start_training_endpoint(payload: CanStartTrainingRequest):
    lp = Policy(**payload.latest_platform_policy.dict()) if payload.latest_platform_policy else None
    lc = Policy(**payload.latest_company_policy.dict()) if payload.latest_company_policy else None
    acceptances = [PolicyAcceptance(**a.dict()) for a in payload.acceptances]

    return {
        "can_start": can_start_training(
            payload.user_id,
            payload.company_id,
            lp,
            lc,
            acceptances
        )
    }


@app.post("/suggest-modules")
def suggest_modules_endpoint(payload: SuggestModulesRequest):
    user = UserProfile(**payload.user.dict())
    modules = [TrainingModuleRef(**m.dict()) for m in payload.modules]
    return suggest_modules_for_user(user, modules, payload.max_results)


@app.post("/grade-quiz")
def grade_quiz_endpoint(payload: GradeQuizRequest):
    return grade_attempt(payload.quiz, payload.user_answers, payload.pass_mark)


@app.post("/compute-progress")
def compute_progress_endpoint(payload: ProgressRequest):
    assignments = [TrainingAssignment(**a.dict()) for a in payload.assignments]
    attempts = [QuizAttempt(**t.dict()) for t in payload.attempts]
    return compute_user_progress(assignments, attempts)


@app.get("/health")
def health():
    return {"status": "ok"}

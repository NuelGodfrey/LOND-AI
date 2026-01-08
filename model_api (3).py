from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


# =========================================
# Data Classes (Model-Level, No Database)
# =========================================

@dataclass
class Policy:
    id: str
    scope: str
    company_id: Optional[str]
    version: str
    title: str


@dataclass
class PolicyAcceptance:
    user_id: str
    policy_id: str
    accepted_at: datetime


@dataclass
class TrainingModuleRef:
    id: str
    title: str
    topic: str
    tags: List[str]


@dataclass
class UserProfile:
    user_id: str
    roles: List[str]
    department: Optional[str] = None


@dataclass
class TrainingAssignment:
    id: str
    user_id: str
    module_id: str
    created_at: datetime
    status: str


@dataclass
class QuizAttempt:
    assignment_id: str
    score_pct: float
    passed: bool
    attempted_at: datetime


# =========================================
# 1) Policy Gate Logic
# =========================================

def can_start_training(
    user_id: str,
    company_id: str,
    latest_platform_policy: Optional[Policy],
    latest_company_policy: Optional[Policy],
    acceptances: List[PolicyAcceptance],
) -> bool:
    required_ids = set()

    if latest_platform_policy:
        required_ids.add(latest_platform_policy.id)

    if latest_company_policy and latest_company_policy.company_id == company_id:
        required_ids.add(latest_company_policy.id)

    if not required_ids:
        return True

    accepted_ids = {pa.policy_id for pa in acceptances if pa.user_id == user_id}
    return required_ids.issubset(accepted_ids)


# =========================================
# 2) Training Suggestion Logic
# =========================================

def suggest_modules_for_user(
    user: UserProfile,
    modules: List[TrainingModuleRef],
    max_results: int = 5,
) -> List[TrainingModuleRef]:

    text = (" ".join(user.roles) + " " + (user.department or "")).lower()
    scored = []

    for m in modules:
        score = sum(1 for tag in m.tags if tag.lower() in text)
        if score > 0:
            scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored][:max_results]


# =========================================
# 3) Quiz Grading Logic
# =========================================

def grade_attempt(
    quiz: List[Dict],
    user_answers: Dict[str, str],
    pass_mark: int = 80
) -> Dict:

    total = len(quiz)
    correct = 0
    details = []

    for q in quiz:
        qid = q["id"]
        gold = str(q.get("answer", "")).strip()
        pred = str(user_answers.get(qid, "")).strip()
        ok = (pred == gold)

        if pred:
            correct += int(ok)

        details.append({
            "id": qid,
            "question": q.get("question"),
            "selected": pred or None,
            "correct": gold,
            "is_correct": ok,
            "rationale": q.get("rationale", "")
        })

    score_pct = round((correct / total) * 100) if total else 0
    passed = score_pct >= pass_mark

    return {
        "score_pct": score_pct,
        "passed": passed,
        "pass_mark": pass_mark,
        "total": total,
        "correct": correct,
        "details": details,
        "graded_at": datetime.utcnow().isoformat() + "Z"
    }


# =========================================
# 4) Progress Computation Logic
# =========================================

def compute_user_progress(
    assignments: List[TrainingAssignment],
    attempts: List[QuizAttempt],
) -> Dict:

    if not assignments:
        return {
            "status": "NO_ASSIGNMENTS",
            "assignments_total": 0,
            "assignments_completed": 0,
            "assignments_pending": 0,
        }

    passed_ids = {a.assignment_id for a in attempts if a.passed}

    total = len(assignments)
    completed = sum(1 for a in assignments if a.id in passed_ids)
    pending = total - completed

    if completed == 0:
        status = "NOT_STARTED"
    elif completed < total:
        status = "IN_PROGRESS"
    else:
        status = "COMPLETED"

    return {
        "status": status,
        "assignments_total": total,
        "assignments_completed": completed,
        "assignments_pending": pending,
    }

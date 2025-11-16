from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ExperienceItem(BaseModel):
    company: Optional[str]
    role: Optional[str]
    dates: Optional[str]
    highlights: List[str] = []


class Profile(BaseModel):
    name: Optional[str]
    title: Optional[str]
    experience: List[ExperienceItem] = []
    skills: Dict[str, List[str]] = {}
    achievements: List[str] = []
    education: List[str] = []

class AppState(BaseModel):
    profile: Profile
    job_description: str
    company: Optional[str] = None
    company_research: Optional[str] = None
    company_values: Optional[List[str]] = None
    company_products: Optional[List[str]] = None
    jd_requirements: Optional[Dict[str, Any]] = None
    matching_points: Optional[List[str]] = None
    letter: Optional[str] = None
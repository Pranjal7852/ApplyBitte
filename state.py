from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ExperienceItem(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    responsibilities: List[str] = []
    technologies: List[str] = []

class EducationItem(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    duration: Optional[str] = None
    gpa: Optional[str] = None
    location: Optional[str] = None

class CertificationItem(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None

class ProjectItem(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = []
    highlights: List[str] = []
    link: Optional[str] = None

class AchievementItem(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class VolunteeringItem(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    responsibilities: List[str] = []
    technologies: List[str] = []

class Profile(BaseModel):
    candidate_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    languages: List[str] = []
    professional_summary: Optional[str] = None
    years_of_experience: Optional[int] = None
    skills: Dict[str, List[str]] = {}
    education: List[EducationItem] = []
    certifications: List[CertificationItem] = []
    experiences: List[ExperienceItem] = []
    projects: List[ProjectItem] = []
    achievements: List[AchievementItem] = []
    publications: List[str] = []
    volunteering: List[VolunteeringItem] = []

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
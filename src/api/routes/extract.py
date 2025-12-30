from fastapi import APIRouter
from src.extraction.skills_extractor import extract_skills
from src.test.test_clean import cleaned_text
from src.api.schemas import SkillsResponse

router = APIRouter(prefix="/extract", tags=["Extraction"])

@router.get("/skills", response_model=SkillsResponse)
def get_skills():
    skills = extract_skills(cleaned_text)
    return {"skills": skills}

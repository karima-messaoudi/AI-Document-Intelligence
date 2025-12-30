from src.extraction.skills_extractor import extract_skills
from src.test.test_clean import cleaned_text

skills = extract_skills(cleaned_text)

print("Compétences extraites :")
for s in skills:
    print("-", s)

import re

def extract_skills(cleaned_text):
    """
    Extraction déterministe des compétences depuis la section 'Compétences Techniques'
    """

    match = re.search(
        r"Compétences Techniques(.+?)(Langues|$)",
        cleaned_text,
        re.DOTALL | re.IGNORECASE
    )

    if not match:
        return []

    section = match.group(1)

    skills = re.split(r"[-•,:\n]", section)
    skills = [s.strip() for s in skills if len(s.strip()) > 2]

    return skills

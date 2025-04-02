def score_resume_from_json(data):
    try:
        categories = [
            "required_experience",
            "education",
            "certifications",
            "hard_skills",
            "soft_skills",
            "culture_keywords"
        ]

        total_score = 0
        valid_sections = 0

        for category in categories:
            required = set(data["all_items_required"].get(category, []))
            matched = set(data["skills_match"].get(category, []))
            if required:
                score = len(matched) / len(required) * 100
                total_score += score
                valid_sections += 1

        return round(total_score / valid_sections, 2) if valid_sections else 0

    except Exception:
        return 0

def score_cover_letter_from_json(data):
    try:
        return sum(item["score"] for item in data["rubric"].values())
    except Exception:
        return 0

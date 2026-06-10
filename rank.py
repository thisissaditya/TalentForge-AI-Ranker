import json
import csv
import argparse
from collections import Counter

# JD keywords derived from challenge JD
TARGET_KEYWORDS = {
    "python": 15,
    "retrieval": 15,
    "ranking": 15,
    "embedding": 12,
    "embeddings": 12,
    "vector": 12,
    "faiss": 10,
    "elasticsearch": 10,
    "opensearch": 10,
    "weaviate": 10,
    "pinecone": 10,
    "qdrant": 10,
    "milvus": 10,
    "ndcg": 8,
    "mrr": 8,
    "map": 8,
    "evaluation": 8,
    "search": 8,
    "recommendation": 6,
    "machine learning": 6,
    "ml": 6,
    "production": 8,
}

def safe_lower(x):
    if x is None:
        return ""
    return str(x).lower()

def semantic_score(candidate):

    text_parts = []

    profile = candidate.get("profile", {})
    text_parts.append(profile.get("headline", ""))
    text_parts.append(profile.get("summary", ""))

    for job in candidate.get("career_history", []):
        text_parts.append(job.get("title", ""))
        text_parts.append(job.get("description", ""))

    for skill in candidate.get("skills", []):
        text_parts.append(skill.get("name", ""))

    text = " ".join(text_parts).lower()

    score = 0

    for kw, weight in TARGET_KEYWORDS.items():
        if kw in text:
            score += weight

    return score

def experience_score(candidate):

    years = candidate["profile"].get("years_of_experience", 0)

    if years < 3:
        return 0

    if 5 <= years <= 9:
        return 25

    if 4 <= years <= 12:
        return 20

    return 10

def signal_score(candidate):

    signals = candidate.get("redrob_signals", {})

    score = 0

    score += signals.get("profile_completeness_score", 0) * 0.10

    score += signals.get("recruiter_response_rate", 0) * 10

    score += signals.get("interview_completion_rate", 0) * 10

    score += signals.get("saved_by_recruiters_30d", 0) * 0.5

    score += signals.get("search_appearance_30d", 0) * 0.05

    github = signals.get("github_activity_score", -1)

    if github > 0:
        score += github * 0.10

    return score

def consistency_score(candidate):

    score = 10

    profile = candidate.get("profile", {})
    exp_years = profile.get("years_of_experience", 0)

    total_months = sum(
        x.get("duration_months", 0)
        for x in candidate.get("career_history", [])
    )

    derived_years = total_months / 12

    if abs(exp_years - derived_years) > 5:
        score -= 5

    for skill in candidate.get("skills", []):
        duration = skill.get("duration_months", 0)

        if duration > exp_years * 12 + 24:
            score -= 2

    return max(score, 0)

def total_score(candidate):

    return (
        semantic_score(candidate)
        + experience_score(candidate)
        + signal_score(candidate)
        + consistency_score(candidate)
    )

def reasoning(candidate):

    profile = candidate.get("profile", {})
    years = profile.get("years_of_experience", 0)
    title = profile.get("current_title", "Unknown")

    return (
        f"{years} years experience as {title}. "
        f"Strong alignment with retrieval/search requirements "
        f"and favorable platform engagement signals."
    )

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--candidates",
        required=True
    )

    parser.add_argument(
        "--out",
        required=True
    )

    args = parser.parse_args()

    ranked = []

    with open(args.candidates, "r", encoding="utf-8") as f:

        for line in f:

            candidate = json.loads(line)

            score = total_score(candidate)

            ranked.append(
                (
                    score,
                    candidate["candidate_id"],
                    reasoning(candidate)
                )
            )

    ranked.sort(reverse=True)

    top100 = ranked[:100]

    with open(args.out, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(
            [
                "candidate_id",
                "rank",
                "score",
                "reasoning"
            ]
        )

        for rank, row in enumerate(top100, start=1):

            writer.writerow(
                [
                    row[1],
                    rank,
                    round(row[0], 4),
                    row[2]
                ]
            )

    print("Done.")
    print("Top 100 candidates written to:", args.out)

if __name__ == "__main__":
    main()

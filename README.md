# TalentForge AI Ranker

## Overview

TalentForge is an AI-powered candidate ranking system developed for the India Runs Data & AI Challenge.

Traditional ATS platforms rely heavily on keyword matching, which often overlooks qualified candidates and promotes profiles optimized for keywords rather than actual suitability.

TalentForge evaluates candidates using a combination of:

* Semantic relevance
* Professional experience
* Behavioral hiring signals
* Profile consistency checks

The goal is to generate a recruiter-quality shortlist rather than a keyword-based ranking.

---

## Problem Statement

Recruiters review hundreds of profiles for a single role.

Most automated systems focus on keyword overlap and fail to understand:

* Candidate quality
* Hiring likelihood
* Career progression
* Profile authenticity

This challenge requires building an intelligent ranking system that identifies candidates who genuinely fit the job requirements.

---

## Solution Approach

The ranking system evaluates candidates using four major dimensions:

### 1. Semantic Relevance

Measures alignment between candidate profiles and job requirements.

Examples:

* Retrieval systems
* Search infrastructure
* Ranking systems
* Embedding technologies
* Recommendation systems

### 2. Experience Analysis

Evaluates:

* Years of experience
* Role seniority
* Career progression

### 3. Behavioral Signal Analysis

Utilizes platform activity signals such as:

* Recruiter response rate
* Interview completion rate
* Profile completeness
* GitHub activity
* Search appearance

### 4. Consistency Verification

Detects suspicious or inconsistent profiles by comparing:

* Claimed experience
* Career history
* Skill durations

This helps reduce the impact of synthetic or misleading candidate profiles.

---

## Architecture

Job Description
↓
Requirement Extraction
↓
Candidate Processing
↓
Semantic Scoring
↓
Behavioral Scoring
↓
Consistency Validation
↓
Composite Ranking
↓
Top Candidate Selection

---

## Repository Structure

```text
TalentForge-AI-Ranker
│
├── rank.py
├── requirements.txt
├── submission_metadata.yaml
├── submission.csv
└── README.md
```

---

## Output Format

The generated submission contains:

* candidate_id
* rank
* score
* reasoning

---

## Future Improvements

* Transformer-based embeddings
* FAISS vector retrieval
* Learning-to-rank models
* LLM-generated explanations
* Active recruiter feedback loops

---

## Author

Purshottam

India Runs 2026 – Data & AI Challenge

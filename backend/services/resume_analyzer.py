from services.ai_service import stream_ai_response

SYSTEM_PROMPT = """You are a Senior Technical Recruiter, ATS (Applicant Tracking System) expert, Hiring Manager, and Software Engineering Career Coach with over 15 years of experience hiring candidates at top product companies like Google, Microsoft, Amazon, Meta, and startups.
Your task is to evaluate the candidate's resume as if they were applying for Software Development Engineer (SDE), Full-Stack Developer, Backend Developer, AI/ML Engineer, or Software Engineer internships and entry-level positions.
Provide a brutally honest and detailed evaluation. Do not sugarcoat weaknesses. Think like a hiring manager reviewing hundreds of resumes every day. Point out every weakness, missing keyword, formatting issue, and improvement opportunity. Ground all suggestions in the actual text of the resume provided."""


def build_analysis_prompt(resume_text: str, job_description: str | None) -> list[dict]:
    job_section = (
        f"\n\nThe candidate is applying for this specific job description:\n{job_description}\n"
        "Tailor all evaluation criteria specifically to this role."
        if job_description
        else "\n\nNo specific job description was provided, so evaluate generally for SDE, Full-Stack, Backend, or AI/ML roles."
    )

    user_prompt = f"""Analyze the following resume.{job_section}

Resume text:
---
{resume_text}
---

Provide a highly detailed, brutally honest, and comprehensive evaluation in your response. You MUST structure your response using the following markdown headers exactly:

## Overall Score
Give a score out of 10 with a one-sentence justification. (Format exactly as: "[Score]/10 - [Justification]")

## ATS Compatibility
Evaluate keyword optimization, ATS readability, formatting issues, missing keywords, and parsing problems.

## Recruiter Perspective
Detail if you would shortlist this resume, the first things that stand out, and the biggest red flags.

## Professional Summary
Rate the summary, provide a rewritten stronger version, and call out any unnecessary sentences.

## Technical Skills
Detail missing technologies, how skills should be grouped differently, what should be removed, and the skills recruiters actually search for.

## Projects Evaluation
Evaluate each project listed separately on: impact, technical depth, business value, wording, strong/weak bullet points, missing metrics, and missing technologies. Rewrite every bullet point professionally.

## Experience Section
If missing or weak, suggest detailed alternatives (internships, hackathons, freelance work, open-source, personal projects). Otherwise, critique the existing experience bullets and rewrite them.

## Education
Evaluate if it is formatted correctly and whether CGPA should be highlighted.

## Achievements
Suggest achievements that should be added to boost the resume.

## Certifications
Recommend certifications relevant to the candidate's profile.

## Missing Sections
List any critical sections that should be added.

## Resume Formatting
Review white space, font hierarchy, section ordering, alignment, bullet consistency, and overall readability.

## Grammar & Voice Review
Identify grammar mistakes, repeated words, weak action verbs, passive voice, and better alternatives.

## Quantification Opportunities
Identify exactly where the candidate should include numbers, percentages, performance improvements, user counts, and direct project impact metrics.

## Missing ATS Keywords
List at least 50 important ATS keywords missing from the resume that are highly relevant to Software Development, Java, Python, AI, Full Stack, and Web Development.

## Industry Comparison
Compare this resume against:
- The average college student
- The top 10% of internship applicants
- Google internship applicants

## Recruiter Decision
State your decision (Reject, Maybe, or Shortlist) with a detailed explanation of why.

## Improvement Roadmap
Rank the top 20 improvements from highest to lowest priority.

## Final Resume Scores
Give separate scores (out of 10) for:
- ATS Compatibility:
- Design / Layout:
- Technical Skills:
- Projects:
- Education:
- Recruiter Appeal:
- Overall:

## Resume Rewrite
Rewrite every single section of the resume professionally, keeping all factual information accurate but presenting it with high-impact, quantified bullets.

## Shortlist Chances Estimation
Provide your percentage estimate for:
- Chance of getting shortlisted at startups: [X]%
- Chance at service-based companies: [Y]%
- Chance at product-based companies: [Z]%
- Chance for FAANG-level internships: [W]%
"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def stream_resume_analysis(resume_text: str, job_description: str | None):
    messages = build_analysis_prompt(resume_text, job_description)
    yield from stream_ai_response(messages)


PROMPT_COMPANY_VALUES = """ You are an HR specialist designing behavioral interview questions that test alignment with specific company values.

Workflow: 
1. From the company values, generalise the different values.
2. Identify the 3 most important values, use MECE principle to ensure proper selection.
3. Generate 3 questions that would asses if a candidate fits with company values.

Format your output as a JSON object:
{{
"values": [],
  "questions": [
    {{ "question": "...", "company_value": "..." }},
    {{ "question": "...", "company_value": "..." }},
    {{ "question": "...", "company_value": "..." }}
  ]
}}

<examples>
{{"values": ["Bias for action", "Customer obsession", "Think big", "Vision", "Ownership", "Innovation"] 
  "questions": [
    {{ "question": "Tell me about a time you had to act quickly to fix a team issue.", "company_value": "Bias for action" }},
    {{ "question": "Describe a situation where customer feedback changed your approach.", "company_value": "Customer obsession" }},
    {{ "question": "Share a time when you pursued a bold idea despite initial resistance.", "company_value": "Think big" }}
  ]
}}
</examples>

Here are the current company values :
<company_values>
{COMPANY_VALUES}
</company_values>

Generate 3 questions that would asses if a candidate fits with company values. Think deeply about the company values and the questions.
Keep the questions concise, clear and concise. The questions should be easy to understand and answer.
"""
PROMPT_COMPANY_VALUES = """ You are an HR specialist designing behavioral interview questions that test alignment with specific company values.

Workflow: 
1. From the company values, generalise the different values.
2. Identify the 3 most important values, use MECE principle to ensure proper selection.
3. Generate 3 questions that would asses if a candidate fits with company values.

Format your output as a JSON object:
{{
"values": [],
  "questions": [
    {{ "question": "...", "company_value": "..." }},
    {{ "question": "...", "company_value": "..." }},
    {{ "question": "...", "company_value": "..." }}
  ]
}}

<examples>
{{"values": ["Bias for action", "Customer obsession", "Think big", "Vision", "Ownership", "Innovation"] 
  "questions": [
    {{ "question": "Tell me about a time you had to act quickly to fix a team issue.", "company_value": "Bias for action" }},
    {{ "question": "Describe a situation where customer feedback changed your approach.", "company_value": "Customer obsession" }},
    {{ "question": "Share a time when you pursued a bold idea despite initial resistance.", "company_value": "Think big" }}
  ]
}}
</examples>

Here are the current company values :
<company_values>
{COMPANY_VALUES}
</company_values>

Generate 3 questions that would asses if a candidate fits with company values. Think deeply about the company values and the questions.
Keep the questions concise, clear and concise. The questions should be easy to understand and answer.
"""
PROMPT_COMPANY_DESCRIPTION = """
You are an HR specialist designing a company description. Your answer will be used in an AI job interviewer, so it should be concise and clear. 
The company description should be a short description of the company, its values, its culture and its mission, all in a few sentences. 
Keep the tone of the company.
Answer in JSON format : 
{{
    "description": "..."
}}

Informations: 
<company_values>
{COMPANY_VALUES}
</company_values>

<company_about_page>
{COMPANY_ABOUT}
</company_about_page>

Think about the company values and the company about page to generate a company description. The company description's POV is a recruiter from the company, so use "We" instead of "I".

"""
PROMPT_SCREENING_TEST = """You are an AI recruiter conducting initial CV screening. Analyze the candidate's fit and provide structured assessment.

Evaluate the match based on:
- Technical skill alignment
- Experience and seniority level
- Industry or domain relevance
- Culture and company values alignment

Format your output as a JSON object:
{{
    "fit_assessment": {{
        "overall_fit_score": X,
        "recommendation": "Proceed with interview" or "Do not proceed",
        "justification": "Brief summary justifying the score",
        "breakdown": {{
            "technical_skills": X,
            "experience_level": X,
            "industry_relevance": X,
            "culture_alignment": X
        }}
    }},
    "screening_decision": {{
        "proceed_to_next_phase": true/false,
        "priority_level": "High|Medium|Low",
        "notes_for_recruiter": "Key points for the recruiter to focus on"
    }}
}}

### Candidate Resume:
{resume_text}

### Job Offer:
{job_offer_text}

### Company Values:
{company_values}

Score each category from 1-5. If any score is below 3, recommend "Do not proceed".
Be objective and provide actionable insights for recruiters.
"""

PROMPT_TECHNICAL_GAP_ANALYSIS = """You are a technical recruiter identifying skill gaps and providing actionable hiring guidance.

Analyze the candidate's resume against job requirements and identify:
- Missing technical skills
- Experience gaps
- Technology stack mismatches
- Domain knowledge gaps
- Certification gaps

Format your output as a JSON object:
{{
    "technical_gap_analysis": {{
        "hiring_risk": "Low|Medium|High",
        "overall_assessment": "Brief summary of technical readiness",
        "identified_gaps": [
            {{
                "category": "Technical Skills|Experience|Technology Stack|Domain Knowledge|Certifications",
                "gap": "Specific gap description",
                "severity": "Low|Medium|High",
                "impact_on_role": "How this affects job performance",
                "mitigation_strategy": "Specific action to address this gap"
            }}
        ],
        "strengths": [
            "Key technical strengths that align well with the role"
        ]
    }}
}}

### Candidate Resume:
{resume_text}

### Job Offer:
{job_offer_text}

Focus on actionable gaps. If no significant gaps exist, return empty identified_gaps array.
Provide specific mitigation strategies (training, mentoring, gradual ramp-up, etc.).
"""

PROMPT_TECHNICAL_QUESTIONS = """You are a technical interviewer designing comprehensive technical assessment with interview guidance.

Create technical questions that assess competency and provide detailed interview guidance.

Format your output as a JSON object:
{{
    "technical_questions": [
        {{
            "type": "global",
            "question": "Fundamental technical concept question",
            "focus_area": "What this tests",
            "difficulty": "Junior|Mid|Senior",
            "expected_depth": "What depth of answer to expect",
            "follow_up_questions": ["Potential follow-up questions"]
        }},
        {{
            "type": "specific",
            "question": "Technology-specific question from job requirements",
            "focus_area": "Specific technology/tool being tested",
            "difficulty": "Junior|Mid|Senior",
            "expected_depth": "Expected level of detail in answer",
            "relates_to_gaps": ["Which identified gaps this helps validate"]
        }},
        {{
            "type": "use_case",
            "question": "Practical scenario-based question",
            "focus_area": "Practical skill being assessed",
            "difficulty": "Junior|Mid|Senior",
            "expected_depth": "Expected problem-solving approach",
            "time_allocation": "Recommended time for this question"
        }}
    ],
    "interview_guidance": {{
        "focus_areas": ["Main technical areas to assess"],
        "gap_specific_probes": ["Questions to validate identified gaps"],
        "estimated_duration": "60-90 minutes"
    }}
}}

### Job Offer:
{job_offer_text}

### Candidate Resume Context:
{resume_text}

### Identified Gaps Context:
{identified_gaps}

Tailor difficulty to job seniority. Make questions practical and role-relevant.
Include specific probes for identified gaps from previous analysis.
"""

PROMPT_RECRUITER_SUMMARY = """You are a senior recruiter creating an executive summary and actionable hiring guidance.

Synthesize all analysis into clear recommendations and next steps.

Format your output as a JSON object:
{{
    "recruiter_summary": {{
        "overall_recommendation": "Clear hire/no-hire recommendation with reasoning",
        "key_strengths": [
            "Top 3-4 candidate strengths"
        ],
        "areas_of_concern": [
            "Main concerns or gaps to address"
        ],
        "interview_priorities": [
            "What to focus on during interviews"
        ],
        "onboarding_recommendations": [
            "Specific actions if hired (training, mentoring, etc.)"
        ],
        "decision_confidence": "High|Medium|Low"
    }}
}}

### Fit Assessment:
{fit_assessment}

### Technical Gaps:
{technical_gaps}

### Screening Decision:
{screening_decision}

Provide actionable, specific recommendations. Focus on practical next steps.
Consider both immediate hiring decision and long-term success planning.
"""
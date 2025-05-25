import requests
import os
import json

# Load candidate name from app.py
from app import read_json

# Load the JSON data
json_data = read_json('response_1748098463317.json')

# Extract candidate name
candidate_name = json_data['candidate_analysis']['basic_info']['candidate_name']

# Extract other values
technical_skills = json_data['phase_1_initial_screening']['fit_assessment']['breakdown']['technical_skills']
experience_level = json_data['phase_1_initial_screening']['fit_assessment']['breakdown']['experience_level']
industry_relevance = json_data['phase_1_initial_screening']['fit_assessment']['breakdown']['industry_relevance']
culture_alignment = json_data['phase_1_initial_screening']['fit_assessment']['breakdown']['culture_alignment']

# Extract overall assessment safely
overall_assessment = json_data.get('phase_1_initial_screening', {}).get('technical_gap_analysis', {}).get('overall_assessment', 'Assessment not available')

# Replace with your actual base ID and table ID or name
base_id = "appB5uu6A22m29ldR"
table_id_or_name = "tblIDEercBM6inBBs"

# Your Airtable API URL
url = f"https://api.airtable.com/v0/{base_id}/{table_id_or_name}"

# Your Bearer token
bearer_token = "patfdQ1TMEyg7LuOE.b720ca67e05311e8eac66d38f8566abf4b180bf0e07bf30ea53afe592f518ce4"

# Headers for the request
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

# Body of the request
body = {
    "fields": {
            "Candidates": candidate_name, # Name of the candidate
            "Participants": "Eliott", # Name of the interviewer
            "Notes": overall_assessment,
            "Technical_skills": technical_skills, # 1/5 to 5/5
            "Experience_level": experience_level, # 1/5 to 5/5
            "Industry_relevance": industry_relevance, # 1/5 to 5/5
            "Culture_alignment": culture_alignment 
    }
}

# Send the POST request
response = requests.post(url, headers=headers, json=body)

# Check the response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)

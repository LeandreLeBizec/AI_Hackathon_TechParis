import os
import json
import ssl
import pdfplumber
from pathlib import Path
from typing import Tuple, List
from mistralai import Mistral
from dotenv import load_dotenv
from datetime import datetime

from prompts.prompts import PROMPT_COMPANY_VALUES, PROMPT_COMPANY_DESCRIPTION, PROMPT_SCREENING_TEST, PROMPT_TECHNICAL_GAP_ANALYSIS, PROMPT_TECHNICAL_QUESTIONS, PROMPT_RECRUITER_SUMMARY

# Load environment variables
load_dotenv()

class CVAnalysisService:
    def __init__(self):
        # Simple SSL fix for venv environments
        self._fix_ssl_for_venv()
        
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        if not self.mistral_api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is required")
        
        self.model = "mistral-large-latest"
        
        # Create Mistral client with venv-specific fixes
        self.client = self._create_mistral_client()
            
        self.root_dir = Path(__file__).parent.parent.parent.absolute()
        self.companies_dir = self.root_dir / "data" / "companies"
    
    def _fix_ssl_for_venv(self):
        """SSL fixes specifically for venv environments"""
        # For venv, the main issue is usually SSL_CERT_FILE pointing to invalid path
        # Clear problematic SSL environment variables
        problematic_vars = ['SSL_CERT_FILE', 'SSL_CERT_DIR']
        for var in problematic_vars:
            if var in os.environ:
                print(f"🔧 Clearing problematic SSL variable: {var}")
                del os.environ[var]
        
        # Set Python to not verify SSL (for development)
        os.environ['PYTHONHTTPSVERIFY'] = '0'
        
        # Create unverified SSL context as fallback
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
    
    def _create_mistral_client(self):
        """Create Mistral client with simple error handling"""
        try:
            print("🔧 Creating Mistral client...")
            client = Mistral(api_key=self.mistral_api_key)
            print("✅ Mistral client created successfully")
            return client
        except Exception as e:
            print(f"❌ Failed to create Mistral client: {str(e)}")
            print("💡 This might be an SSL certificate issue in your venv")
            print("💡 Try: pip install --upgrade certifi")
            raise e
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from a PDF file using pdfplumber"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def get_available_companies(self) -> List[str]:
        """Get list of available companies"""
        if not self.companies_dir.exists():
            return []
        return [d.name for d in self.companies_dir.iterdir() if d.is_dir()]
    
    def load_company_info(self, company_name: str) -> Tuple[str, str, str]:
        """Load company values, about info and offers"""
        company_path = self.companies_dir / company_name
        
        if not company_path.exists():
            raise FileNotFoundError(f"No data found for company: {company_name}")
        
        # Load values
        values_files = list(company_path.glob("values/*.md"))
        if not values_files:
            raise FileNotFoundError(f"No values file found for company: {company_name}")
        with open(values_files[0], "r", encoding="utf-8") as f:
            values = f.read()
        
        # Load about
        about_files = list(company_path.glob("about/*.md"))
        if not about_files:
            raise FileNotFoundError(f"No about file found for company: {company_name}")
        with open(about_files[0], "r", encoding="utf-8") as f:
            about = f.read()
        
        # Load offers
        offer_files = list(company_path.glob("offers/*.md"))
        if not offer_files:
            raise FileNotFoundError(f"No offers file found for company: {company_name}")
        with open(offer_files[0], "r", encoding="utf-8") as f:
            offers = f.read()
        
        return values, about, offers
    
    def _call_mistral_api(self, prompt: str) -> str:
        """Make a call to Mistral API"""
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return chat_response.choices[0].message.content
    
    def _extract_candidate_name(self, cv_content: str) -> str:
        """Try to extract candidate name from CV content"""
        # Simple name extraction - look for common patterns
        lines = cv_content.split('\n')[:10]  # Check first 10 lines
        for line in lines:
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) > 5:
                # Likely a name if it's short, not too many words, and not too short
                if not any(char.isdigit() for char in line) and '@' not in line:
                    return line
        return None
    
    def generate_phase1_screening(self, resume_text: str, job_offer_text: str, company_values: str) -> dict:
        """Generate Phase 1: Initial Screening (fit assessment + screening decision)"""
        prompt = PROMPT_SCREENING_TEST.format(
            resume_text=resume_text,
            job_offer_text=job_offer_text,
            company_values=company_values
        )
        response = self._call_mistral_api(prompt)
        
        try:
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Phase 1 screening response: {e}")
    
    def generate_technical_gap_analysis(self, resume_text: str, job_offer_text: str) -> dict:
        """Generate technical gap analysis"""
        prompt = PROMPT_TECHNICAL_GAP_ANALYSIS.format(
            resume_text=resume_text,
            job_offer_text=job_offer_text
        )
        response = self._call_mistral_api(prompt)
        
        try:
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse technical gap analysis response: {e}")
    
    def generate_phase2_hr_behavioral(self, company_values: str, company_about: str) -> dict:
        """Generate Phase 2: HR Behavioral Interview"""
        prompt = PROMPT_COMPANY_VALUES.format(
            COMPANY_VALUES=company_values,
            COMPANY_ABOUT=company_about
        )
        response = self._call_mistral_api(prompt)
        
        try:
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Phase 2 HR behavioral response: {e}")
    
    def generate_phase3_technical_interview(self, resume_text: str, job_offer_text: str, identified_gaps: str) -> dict:
        """Generate Phase 3: Technical Interview"""
        prompt = PROMPT_TECHNICAL_QUESTIONS.format(
            resume_text=resume_text,
            job_offer_text=job_offer_text,
            identified_gaps=identified_gaps
        )
        response = self._call_mistral_api(prompt)
        
        try:
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Phase 3 technical interview response: {e}")
    
    def generate_recruiter_summary(self, fit_assessment: str, technical_gaps: str, screening_decision: str) -> dict:
        """Generate recruiter summary and recommendations"""
        prompt = PROMPT_RECRUITER_SUMMARY.format(
            fit_assessment=fit_assessment,
            technical_gaps=technical_gaps,
            screening_decision=screening_decision
        )
        response = self._call_mistral_api(prompt)
        
        try:
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse recruiter summary response: {e}")
    
    def analyze_cv(self, cv_content: str, company_name: str) -> dict:
        """Complete CV analysis following the recruiting pipeline"""
        import time
        start_time = time.time()
        
        # Load company information
        company_values, company_about, company_offers = self.load_company_info(company_name)
        
        # Extract candidate name
        candidate_name = self._extract_candidate_name(cv_content)
        
        # Phase 1: Initial Screening
        phase1_data = self.generate_phase1_screening(cv_content, company_offers, company_values)
        
        # Technical Gap Analysis (part of Phase 1)
        gap_analysis = self.generate_technical_gap_analysis(cv_content, company_offers)
        
        # Phase 2: HR Behavioral
        phase2_data = self.generate_phase2_hr_behavioral(company_values, company_about)
        
        # Phase 3: Technical Interview (with gap context)
        gaps_context = json.dumps(gap_analysis.get('technical_gap_analysis', {}).get('identified_gaps', []))
        phase3_data = self.generate_phase3_technical_interview(cv_content, company_offers, gaps_context)
        
        # Recruiter Summary
        summary_data = self.generate_recruiter_summary(
            json.dumps(phase1_data.get('fit_assessment', {})),
            json.dumps(gap_analysis.get('technical_gap_analysis', {})),
            json.dumps(phase1_data.get('screening_decision', {}))
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Build final response structure
        return {
            "candidate_analysis": {
                "basic_info": {
                    "candidate_name": candidate_name,
                    "analysis_timestamp": datetime.now(),
                    "company_name": company_name,
                    "processing_time_seconds": round(processing_time, 2)
                }
            },
            "phase_1_initial_screening": {
                "fit_assessment": phase1_data.get('fit_assessment', {}),
                "technical_gap_analysis": gap_analysis.get('technical_gap_analysis', {}),
                "screening_decision": phase1_data.get('screening_decision', {})
            },
            "phase_2_hr_behavioral": phase2_data,
            "phase_3_technical_interview": phase3_data,
            "recruiter_summary": summary_data.get('recruiter_summary', {})
        } 
    

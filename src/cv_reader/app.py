import time
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import (
    CVAnalysisResponse, 
    ErrorResponse, 
    CompanyListResponse, 
    HealthResponse,
    CandidateAnalysis,
    Phase1InitialScreening,
    Phase2HRBehavioral,
    Phase3TechnicalInterview,
    RecruiterSummary
)
from services import CVAnalysisService

# Initialize FastAPI app
app = FastAPI(
    title="CV Analysis API",
    description="API for analyzing CVs against company requirements",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
cv_service = CVAnalysisService()

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal Server Error",
            detail=str(exc),
            status="error"
        ).dict()
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now()
    )

@app.get("/companies", response_model=CompanyListResponse)
async def get_companies():
    """Get list of available companies"""
    try:
        companies = cv_service.get_available_companies()
        return CompanyListResponse(
            companies=companies,
            count=len(companies)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get companies: {str(e)}"
        )

@app.post("/analyze-cv", response_model=CVAnalysisResponse)
async def analyze_cv(
    file: UploadFile = File(..., description="PDF file containing the CV"),
    company_name: str = Form(..., description="Name of the company to analyze against")
):
    """
    Analyze a CV against a specific company's requirements.
    
    Returns comprehensive analysis including:
    - Screening test results with fit score and recommendation
    - Company values questions for behavioral interviews
    - Company description for context
    - Technical gap analysis identifying potential skill gaps
    - Technical interview questions (global, specific, use-case)
    """
    start_time = time.time()
    
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported"
            )
        
        # Check if company exists
        available_companies = cv_service.get_available_companies()
        if company_name not in available_companies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company '{company_name}' not found. Available companies: {available_companies}"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = Path(temp_file.name)
        
        try:
            # Extract text from PDF
            cv_content = cv_service.extract_text_from_pdf(temp_file_path)
            
            if not cv_content.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not extract text from PDF. Please ensure the PDF contains readable text."
                )
            
            # Perform analysis
            analysis_results = cv_service.analyze_cv(cv_content, company_name)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Build response
            response = CVAnalysisResponse(
                candidate_analysis=CandidateAnalysis(**analysis_results["candidate_analysis"]),
                phase_1_initial_screening=Phase1InitialScreening(**analysis_results["phase_1_initial_screening"]),
                phase_2_hr_behavioral=Phase2HRBehavioral(**analysis_results["phase_2_hr_behavioral"]),
                phase_3_technical_interview=Phase3TechnicalInterview(**analysis_results["phase_3_technical_interview"]),
                recruiter_summary=RecruiterSummary(**analysis_results["recruiter_summary"])
            )
            
            return response
            
        finally:
            # Clean up temporary file
            temp_file_path.unlink(missing_ok=True)
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "CV Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "companies": "/companies", 
            "analyze_cv": "/analyze-cv",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
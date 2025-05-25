# Dashboard API Documentation

## Overview

The CV Analysis API now includes dashboard functionality that aggregates all candidate scores and feedback for easy visualization and analysis. This feature automatically stores analysis results and provides endpoints to retrieve aggregated data.

## New Endpoints

### GET `/dashboard/scores`

Retrieves aggregated scores and feedback for all analyzed candidates.

**Response Model:**
```json
{
  "candidates": [
    {
      "candidate_name": "John Doe",
      "company_name": "mixedbread",
      "analysis_timestamp": "2024-01-15T10:30:00",
      "overall_fit_score": 4,
      "technical_skills_score": 4,
      "experience_level_score": 4,
      "industry_relevance_score": 3,
      "culture_alignment_score": 4,
      "recommendation": "Proceed with interview",
      "priority_level": "High",
      "proceed_to_next_phase": true,
      "hiring_risk": "Low",
      "decision_confidence": "High",
      "processing_time_seconds": 15.67,
      "key_strengths": [
        "Strong Python and API development experience",
        "Solid database knowledge"
      ],
      "areas_of_concern": [
        "Limited experience with Kubernetes"
      ],
      "identified_gaps_count": 1,
      "overall_assessment": "Minor gaps in DevOps tools, strong foundation otherwise"
    }
  ],
  "total_candidates": 1,
  "companies_analyzed": ["mixedbread"],
  "average_fit_score": 4.0,
  "last_updated": "2024-01-15T11:00:00"
}
```

**Usage:**
```bash
curl -X GET "http://localhost:8000/dashboard/scores"
```

### DELETE `/dashboard/scores`

Clears all stored candidate analysis results. Useful for testing or resetting dashboard data.

**Response:**
```json
{
  "message": "All candidate scores cleared successfully",
  "status": "success"
}
```

**Usage:**
```bash
curl -X DELETE "http://localhost:8000/dashboard/scores"
```

## Data Storage

- Analysis results are automatically saved when a CV is processed via `/analyze-cv`
- Data is stored in JSON format at `data/candidate_results/analysis_results.json`
- No database setup required - uses simple file-based storage
- Results are persistent across API restarts

## Dashboard Data Fields

Each candidate entry includes:

### Scoring Metrics
- `overall_fit_score`: Overall fit assessment (1-5 scale)
- `technical_skills_score`: Technical skills rating (1-5 scale)
- `experience_level_score`: Experience level rating (1-5 scale)
- `industry_relevance_score`: Industry relevance rating (1-5 scale)
- `culture_alignment_score`: Culture alignment rating (1-5 scale)

### Decision Metadata
- `recommendation`: Text recommendation (e.g., "Proceed with interview")
- `priority_level`: Priority level (High/Medium/Low)
- `proceed_to_next_phase`: Boolean decision flag
- `hiring_risk`: Risk assessment (Low/Medium/High)
- `decision_confidence`: Confidence level in decision

### Analysis Details
- `candidate_name`: Extracted candidate name (if available)
- `company_name`: Company analyzed against
- `analysis_timestamp`: When analysis was performed
- `processing_time_seconds`: Time taken for analysis
- `key_strengths`: List of identified strengths
- `areas_of_concern`: List of areas needing attention
- `identified_gaps_count`: Number of technical gaps identified
- `overall_assessment`: Summary assessment text

## Aggregated Statistics

The dashboard provides:
- `total_candidates`: Total number of candidates analyzed
- `companies_analyzed`: List of unique companies
- `average_fit_score`: Average fit score across all candidates
- `last_updated`: Timestamp of last data update

## Testing

Use the provided test script to verify functionality:

```bash
cd src/cv_reader
python test_dashboard.py
```

## Integration with Frontend Dashboards

The JSON response format is designed to be easily consumed by dashboard solutions like:
- Grafana (via JSON API datasource)
- Custom React/Vue.js dashboards
- Business intelligence tools
- Excel/Google Sheets (via API import)

## Example Workflow

1. **Analyze CVs**: Use `POST /analyze-cv` to process candidate CVs
2. **View Dashboard**: Use `GET /dashboard/scores` to get aggregated data
3. **Visualize**: Feed the JSON data into your preferred dashboard tool
4. **Reset if needed**: Use `DELETE /dashboard/scores` to clear data

## Security Considerations

- In production, add authentication to dashboard endpoints
- Consider rate limiting for dashboard access
- Implement proper access controls for sensitive candidate data
- Add data retention policies as needed 
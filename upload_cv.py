#!/usr/bin/env python3
"""
Simple script to upload and analyze a CV using the FastAPI backend
"""

import requests
import json
from pathlib import Path

def analyze_cv(pdf_path: str, company_name: str = "mixedbread"):
    """Upload and analyze a CV"""
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    print(f"📄 Analyzing CV: {pdf_path}")
    print(f"🏢 Company: {company_name}")
    print("⏳ Processing...")
    
    # Prepare the request
    url = "http://localhost:8000/analyze-cv"
    
    with open(pdf_path, 'rb') as pdf_file:
        files = {'file': ('cv.pdf', pdf_file, 'application/pdf')}
        data = {'company_name': company_name}
        
        try:
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ CV Analysis Complete!")
                print("=" * 80)
                
                # Basic Info
                basic_info = result['candidate_analysis']['basic_info']
                print(f"👤 Candidate: {basic_info.get('candidate_name', 'Name not detected')}")
                print(f"🏢 Company: {basic_info['company_name']}")
                print(f"⏱️  Processing Time: {basic_info['processing_time_seconds']} seconds")
                
                # Phase 1: Initial Screening
                print(f"\n🔍 PHASE 1: INITIAL SCREENING")
                print("-" * 40)
                
                fit = result['phase_1_initial_screening']['fit_assessment']
                print(f"🎯 Overall Fit Score: {fit['overall_fit_score']}/5")
                print(f"📋 Recommendation: {fit['recommendation']}")
                print(f"📝 Justification: {fit['justification']}")
                
                breakdown = fit['breakdown']
                print(f"📊 Breakdown:")
                print(f"   • Technical Skills: {breakdown['technical_skills']}/5")
                print(f"   • Experience Level: {breakdown['experience_level']}/5")
                print(f"   • Industry Relevance: {breakdown['industry_relevance']}/5")
                print(f"   • Culture Alignment: {breakdown['culture_alignment']}/5")
                
                # Technical Gap Analysis
                gaps = result['phase_1_initial_screening']['technical_gap_analysis']
                print(f"\n⚠️  Technical Gap Analysis:")
                print(f"   Risk Level: {gaps['hiring_risk']}")
                print(f"   Assessment: {gaps['overall_assessment']}")
                
                if gaps['identified_gaps']:
                    print(f"\n   Identified Gaps ({len(gaps['identified_gaps'])}):")
                    for i, gap in enumerate(gaps['identified_gaps'], 1):
                        print(f"   {i}. [{gap['severity']}] {gap['category']}: {gap['gap']}")
                        print(f"      💡 Impact: {gap['impact_on_role']}")
                        print(f"      🔧 Mitigation: {gap['mitigation_strategy']}")
                else:
                    print("   ✅ No significant gaps identified")
                
                if gaps['strengths']:
                    print(f"\n   Key Strengths:")
                    for strength in gaps['strengths']:
                        print(f"   ✅ {strength}")
                
                # Screening Decision
                decision = result['phase_1_initial_screening']['screening_decision']
                print(f"\n📋 Screening Decision:")
                print(f"   Proceed: {'✅ Yes' if decision['proceed_to_next_phase'] else '❌ No'}")
                print(f"   Priority: {decision['priority_level']}")
                print(f"   Notes: {decision['notes_for_recruiter']}")
                
                # Phase 2: HR Behavioral
                print(f"\n💼 PHASE 2: HR BEHAVIORAL INTERVIEW")
                print("-" * 40)
                
                hr_phase = result['phase_2_hr_behavioral']
                context = hr_phase['company_context']
                print(f"🏢 Company: {context['company_description']}")
                print(f"🎯 Key Values: {', '.join(context['key_values'])}")
                
                print(f"\n❓ Behavioral Questions ({len(hr_phase['behavioral_questions'])}):")
                for i, q in enumerate(hr_phase['behavioral_questions'], 1):
                    print(f"   {i}. {q['question']}")
                    print(f"      🎯 Tests: {q['tests_value']}")
                    print(f"      👀 Look for: {q['what_to_look_for']}")
                    print(f"      🔍 Follow-up: {', '.join(q['follow_up_areas'])}")
                
                guidance = hr_phase['interview_guidance']
                print(f"\n📋 Interview Guidance:")
                print(f"   Focus Areas: {', '.join(guidance['focus_areas'])}")
                print(f"   Red Flags: {', '.join(guidance['red_flags_to_watch'])}")
                print(f"   Duration: {guidance['estimated_duration']}")
                
                # Phase 3: Technical Interview
                print(f"\n🔧 PHASE 3: TECHNICAL INTERVIEW")
                print("-" * 40)
                
                tech_phase = result['phase_3_technical_interview']
                print(f"❓ Technical Questions ({len(tech_phase['technical_questions'])}):")
                for i, q in enumerate(tech_phase['technical_questions'], 1):
                    print(f"   {i}. [{q['type'].upper()}] {q['question']}")
                    print(f"      🎯 Focus: {q['focus_area']} (Difficulty: {q['difficulty']})")
                    print(f"      📋 Expected: {q['expected_depth']}")
                    if q.get('follow_up_questions'):
                        print(f"      🔍 Follow-ups: {', '.join(q['follow_up_questions'])}")
                    if q.get('relates_to_gaps'):
                        print(f"      ⚠️  Validates gaps: {', '.join(q['relates_to_gaps'])}")
                    if q.get('time_allocation'):
                        print(f"      ⏱️  Time: {q['time_allocation']}")
                
                tech_guidance = tech_phase['interview_guidance']
                print(f"\n📋 Technical Interview Guidance:")
                print(f"   Focus Areas: {', '.join(tech_guidance['focus_areas'])}")
                print(f"   Gap Probes: {', '.join(tech_guidance['gap_specific_probes'])}")
                print(f"   Duration: {tech_guidance['estimated_duration']}")
                
                # Recruiter Summary
                print(f"\n📊 RECRUITER SUMMARY")
                print("-" * 40)
                
                summary = result['recruiter_summary']
                print(f"🎯 Overall Recommendation: {summary['overall_recommendation']}")
                print(f"🔒 Decision Confidence: {summary['decision_confidence']}")
                
                print(f"\n✅ Key Strengths:")
                for strength in summary['key_strengths']:
                    print(f"   • {strength}")
                
                if summary['areas_of_concern']:
                    print(f"\n⚠️  Areas of Concern:")
                    for concern in summary['areas_of_concern']:
                        print(f"   • {concern}")
                
                print(f"\n🎯 Interview Priorities:")
                for priority in summary['interview_priorities']:
                    print(f"   • {priority}")
                
                if summary['onboarding_recommendations']:
                    print(f"\n🚀 Onboarding Recommendations:")
                    for rec in summary['onboarding_recommendations']:
                        print(f"   • {rec}")
                
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API. Make sure the server is running!")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Example usage - replace with your CV path
    cv_path = input("📁 Enter path to your CV (PDF): ").strip()
    
    if cv_path:
        analyze_cv(cv_path)
    else:
        print("❌ No file path provided") 
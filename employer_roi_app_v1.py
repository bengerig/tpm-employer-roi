"""
Talent Pipeline Management (TPM) - Employer ROI Data Collection App
Strategy 6: Continuous Improvement & Results Measurement
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="TPM Employer ROI Tracker",
    page_icon="📊",
    layout="wide"
)

# Data file
DATA_FILE = "employer_submissions.json"

def load_data():
    """Load existing submissions"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_submission(data):
    """Save new submission"""
    submissions = load_data()
    data['timestamp'] = datetime.now().isoformat()
    submissions.append(data)
    with open(DATA_FILE, 'w') as f:
        json.dump(submissions, f, indent=2)

def calculate_roi(cost_per_hire, onboarding_weeks_before, onboarding_weeks_after, 
                  weekly_productivity_cost, hires_per_year):
    """Calculate ROI from training investment"""
    weeks_saved = onboarding_weeks_before - onboarding_weeks_after
    savings_per_hire = weeks_saved * weekly_productivity_cost
    annual_savings = savings_per_hire * hires_per_year
    
    return {
        'weeks_saved': weeks_saved,
        'savings_per_hire': savings_per_hire,
        'annual_savings': annual_savings,
        'payback_period': cost_per_hire / savings_per_hire if savings_per_hire > 0 else float('inf')
    }

# Header
st.title("🎯 TPM Employer ROI Data Collection")
st.markdown("### Strategy 6: Measuring Results for Continuous Improvement")
st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["📝 Submit Data", "📊 View Submissions", "📈 Analytics"])

with tab1:
    st.header("Employer Data Submission Form")
    
    with st.form("employer_submission"):
        # Company Information
        st.subheader("1️⃣ Company Information")
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name*", placeholder="e.g., Acme Manufacturing")
            industry = st.selectbox("Industry", [
                "Manufacturing",
                "Healthcare", 
                "Technology",
                "Construction",
                "Logistics",
                "Other"
            ])
        with col2:
            contact_name = st.text_input("Contact Name*")
            contact_email = st.text_input("Contact Email*", placeholder="email@company.com")
        
        st.markdown("---")
        
        # Job Demand Data (Strategy 2)
        st.subheader("2️⃣ Job Demand Projections")
        col1, col2, col3 = st.columns(3)
        with col1:
            job_title = st.text_input("Critical Job Title*", placeholder="e.g., Maintenance Technician I")
            current_openings = st.number_input("Current Open Positions", min_value=0, value=0)
        with col2:
            annual_hires_needed = st.number_input("Annual Hires Needed", min_value=0, value=0)
            incumbent_upskilling = st.number_input("Incumbent Workers Needing Upskilling (2026)", min_value=0, value=0)
        with col3:
            turnover_rate = st.slider("Annual Turnover Rate (%)", 0, 100, 15)
        
        st.markdown("---")
        
        # Cost Per Hire Data (Baseline)
        st.subheader("3️⃣ Hiring Costs & Timeline (Baseline - Today)")
        col1, col2 = st.columns(2)
        with col1:
            cost_per_hire = st.number_input("All-In Cost Per Hire ($)*", 
                                            min_value=0, 
                                            value=15000,
                                            help="Include recruiting, onboarding, training, supervisor time")
            onboarding_weeks_baseline = st.number_input("Time to Minimal Independent Work (weeks)*", 
                                                        min_value=0.0, 
                                                        value=10.0,
                                                        step=0.5)
        with col2:
            productivity_weeks_baseline = st.number_input("Time to Full Productivity (weeks)*", 
                                                          min_value=0.0, 
                                                          value=20.0,
                                                          step=0.5)
            weekly_productivity_cost = st.number_input("Weekly Cost of Lost Productivity ($)", 
                                                       min_value=0, 
                                                       value=2000,
                                                       help="Avg weekly cost when worker isn't fully productive")
        
        st.markdown("---")
        
        # Impact of Training/Pipeline (Projected)
        st.subheader("4️⃣ Impact of Pipeline/Training (Projected)")
        col1, col2 = st.columns(2)
        with col1:
            onboarding_weeks_reduction = st.number_input("Estimated Onboarding Reduction (weeks)", 
                                                         min_value=0.0, 
                                                         value=1.5,
                                                         step=0.5,
                                                         help="How many weeks of onboarding could be saved?")
            onboarding_activities_replaced = st.multiselect(
                "Onboarding Activities Reduced/Replaced",
                ["Basic safety training", "Fundamentals training", "Equipment orientation", 
                 "Shadowing/ride-alongs", "Documentation training", "Other"]
            )
        with col2:
            productivity_improvement = st.slider(
                "Speed-to-Productivity Improvement (%)", 
                0, 100, 15,
                help="% faster to full productivity"
            )
        
        st.markdown("---")
        
        # Retention Data
        st.subheader("5️⃣ Retention Metrics")
        col1, col2 = st.columns(2)
        with col1:
            retention_90day_current = st.slider("Current 90-Day Retention Rate (%)", 0, 100, 85)
            retention_1year_current = st.slider("Current 1-Year Retention Rate (%)", 0, 100, 70)
        with col2:
            retention_90day_target = st.slider("Target 90-Day Retention Rate (%)", 0, 100, 90)
            retention_1year_target = st.slider("Target 1-Year Retention Rate (%)", 0, 100, 80)
        
        st.markdown("---")
        
        # ROI & Readiness
        st.subheader("6️⃣ ROI Assessment & Program Readiness")
        col1, col2 = st.columns(2)
        with col1:
            credential_value = st.select_slider(
                "Credential Value Rating",
                options=["Low", "Moderate-Low", "Moderate", "Moderate-High", "High"],
                value="Moderate-High"
            )
            pilot_readiness = st.radio(
                "Ready to Support Pilot Program?",
                ["Yes - Ready Now", "Yes - Within 6 Months", "Maybe - Need More Info", "Not at This Time"]
            )
        with col2:
            roi_rating = st.select_slider(
                "Expected ROI Rating",
                options=["Minimal", "Low", "Moderate", "Good", "Excellent"],
                value="Good"
            )
        
        additional_notes = st.text_area("Additional Notes / Comments", 
                                        placeholder="Any additional context or feedback...")
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Employer Data", use_container_width=True)
        
        if submitted:
            # Validation
            if not company_name or not contact_name or not contact_email:
                st.error("⚠️ Please fill out all required fields (marked with *)")
            elif '@' not in contact_email:
                st.error("⚠️ Please enter a valid email address")
            else:
                # Calculate ROI
                onboarding_weeks_after = onboarding_weeks_baseline - onboarding_weeks_reduction
                roi = calculate_roi(
                    cost_per_hire,
                    onboarding_weeks_baseline,
                    onboarding_weeks_after,
                    weekly_productivity_cost,
                    annual_hires_needed
                )
                
                # Prepare submission data
                submission = {
                    'company_info': {
                        'company_name': company_name,
                        'industry': industry,
                        'contact_name': contact_name,
                        'contact_email': contact_email
                    },
                    'job_demand': {
                        'job_title': job_title,
                        'current_openings': current_openings,
                        'annual_hires_needed': annual_hires_needed,
                        'incumbent_upskilling': incumbent_upskilling,
                        'turnover_rate': turnover_rate
                    },
                    'baseline_costs': {
                        'cost_per_hire': cost_per_hire,
                        'onboarding_weeks': onboarding_weeks_baseline,
                        'productivity_weeks': productivity_weeks_baseline,
                        'weekly_productivity_cost': weekly_productivity_cost
                    },
                    'pipeline_impact': {
                        'onboarding_reduction_weeks': onboarding_weeks_reduction,
                        'activities_replaced': onboarding_activities_replaced,
                        'productivity_improvement_pct': productivity_improvement
                    },
                    'retention': {
                        'retention_90day_current': retention_90day_current,
                        'retention_1year_current': retention_1year_current,
                        'retention_90day_target': retention_90day_target,
                        'retention_1year_target': retention_1year_target
                    },
                    'roi_assessment': {
                        'credential_value': credential_value,
                        'pilot_readiness': pilot_readiness,
                        'roi_rating': roi_rating,
                        'calculated_roi': roi
                    },
                    'additional_notes': additional_notes
                }
                
                # Save submission
                save_submission(submission)
                
                # Show success message with ROI summary
                st.success("✅ Data submitted successfully!")
                st.balloons()
                
                # Display ROI calculation
                st.markdown("### 📊 Your ROI Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Weeks Saved Per Hire", f"{roi['weeks_saved']:.1f}")
                with col2:
                    st.metric("Savings Per Hire", f"${roi['savings_per_hire']:,.0f}")
                with col3:
                    st.metric("Annual Savings", f"${roi['annual_savings']:,.0f}")
                with col4:
                    if roi['payback_period'] != float('inf'):
                        st.metric("Payback Period", f"{roi['payback_period']:.1f} hires")
                    else:
                        st.metric("Payback Period", "N/A")

with tab2:
    st.header("📋 Submitted Employer Data")
    
    submissions = load_data()
    
    if submissions:
        st.metric("Total Submissions", len(submissions))
        
        # Convert to DataFrame for display
        display_data = []
        for sub in submissions:
            display_data.append({
                'Company': sub['company_info']['company_name'],
                'Industry': sub['company_info']['industry'],
                'Job Title': sub['job_demand']['job_title'],
                'Annual Hires': sub['job_demand']['annual_hires_needed'],
                'Cost/Hire': f"${sub['baseline_costs']['cost_per_hire']:,}",
                'Weeks Saved': f"{sub['roi_assessment']['calculated_roi']['weeks_saved']:.1f}",
                'Annual Savings': f"${sub['roi_assessment']['calculated_roi']['annual_savings']:,.0f}",
                'Pilot Ready': sub['roi_assessment']['pilot_readiness'],
                'Submitted': sub.get('timestamp', 'N/A')[:10]
            })
        
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download button
        st.download_button(
            label="📥 Download All Data (JSON)",
            data=json.dumps(submissions, indent=2),
            file_name=f"employer_roi_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    else:
        st.info("No submissions yet. Use the 'Submit Data' tab to add your first entry!")

with tab3:
    st.header("📈 Analytics & Insights")
    
    submissions = load_data()
    
    if submissions:
        # Aggregate metrics
        total_companies = len(submissions)
        total_annual_hires = sum(s['job_demand']['annual_hires_needed'] for s in submissions)
        avg_cost_per_hire = sum(s['baseline_costs']['cost_per_hire'] for s in submissions) / total_companies
        total_annual_savings = sum(s['roi_assessment']['calculated_roi']['annual_savings'] for s in submissions)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Participating Companies", total_companies)
        with col2:
            st.metric("Total Annual Hires", total_annual_hires)
        with col3:
            st.metric("Avg Cost Per Hire", f"${avg_cost_per_hire:,.0f}")
        with col4:
            st.metric("Total Annual Savings", f"${total_annual_savings:,.0f}")
        
        st.markdown("---")
        
        # Industry breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Industry Distribution")
            industry_counts = pd.Series([s['company_info']['industry'] for s in submissions]).value_counts()
            st.bar_chart(industry_counts)
        
        with col2:
            st.subheader("Pilot Readiness")
            readiness_counts = pd.Series([s['roi_assessment']['pilot_readiness'] for s in submissions]).value_counts()
            st.bar_chart(readiness_counts)
        
        st.markdown("---")
        
        # ROI Distribution
        st.subheader("ROI Distribution Across Employers")
        roi_data = pd.DataFrame([
            {
                'Company': s['company_info']['company_name'],
                'Annual Savings': s['roi_assessment']['calculated_roi']['annual_savings'],
                'Savings Per Hire': s['roi_assessment']['calculated_roi']['savings_per_hire']
            }
            for s in submissions
        ])
        st.dataframe(roi_data, use_container_width=True, hide_index=True)
        
    else:
        st.info("No data available for analytics yet. Submit employer data to see insights!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p><strong>Talent Pipeline Management® (TPM) - Strategy 6: Continuous Improvement</strong></p>
    <p>Measuring results to optimize talent pipelines and demonstrate ROI</p>
</div>
""", unsafe_allow_html=True)

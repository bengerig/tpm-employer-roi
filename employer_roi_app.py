"""
Talent Pipeline Management (TPM) - Employer ROI Data Collection App (v2.0)
Strategy 6: Continuous Improvement & Results Measurement
Enhanced with: Database, Authentication, Advanced Analytics, and Export Features
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import SessionLocal, User, Submission
from auth import authenticate_user, create_user, get_user_by_email, hash_password
from analytics import (
    get_analytics_metrics,
    create_industry_chart,
    create_roi_distribution_chart,
    create_pilot_readiness_chart,
    create_savings_trend_chart,
    create_retention_comparison_chart,
    create_cost_per_hire_distribution
)
from export_utils import export_to_csv, export_to_excel, export_to_pdf

# Page config
st.set_page_config(
    page_title="TPM Employer ROI Tracker 2.0",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if 'user' not in st.session_state:
    st.session_state.user = None
if 'db' not in st.session_state:
    st.session_state.db = SessionLocal()

db = st.session_state.db


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


def login_page():
    """Login/Registration page"""
    st.title("🎯 TPM Employer ROI Tracker")
    st.markdown("### Strategy 6: Measuring Results for Continuous Improvement")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True, type="primary"):
            user = authenticate_user(username, password, db)
            if user:
                st.session_state.user = user
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    with col2:
        st.subheader("✍️ Create Account")
        new_company = st.text_input("Company Name", key="reg_company")
        new_email = st.text_input("Email Address", key="reg_email")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        new_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
        
        if st.button("Create Account", use_container_width=True):
            if not all([new_company, new_email, new_username, new_password, new_password_confirm]):
                st.error("⚠️ Please fill out all fields")
            elif new_password != new_password_confirm:
                st.error("⚠️ Passwords do not match")
            elif '@' not in new_email:
                st.error("⚠️ Please enter a valid email address")
            elif get_user_by_email(new_email, db):
                st.error("⚠️ Email already registered")
            else:
                try:
                    user = create_user(new_email, new_username, new_password, new_company, db)
                    st.success("✅ Account created successfully! Please log in.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error creating account: {str(e)}")


def main_app():
    """Main authenticated app"""
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 TPM ROI Tracker")
        st.markdown(f"**Welcome, {user.company_name}**")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Submit Data",
        "📋 My Submissions",
        "📊 Analytics",
        "💾 Export Data",
        "📈 Dashboard"
    ])
    
    with tab1:
        st.header("📝 Employer Data Submission Form")
        
        with st.form("employer_submission"):
            # Company Information
            st.subheader("1️⃣ Company Information")
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name*", value=user.company_name)
                industry = st.selectbox("Industry", [
                    "Manufacturing",
                    "Healthcare",
                    "Technology",
                    "Construction",
                    "Logistics",
                    "Transportation",
                    "Retail",
                    "Hospitality",
                    "Other"
                ])
            with col2:
                contact_name = st.text_input("Contact Name*", placeholder="Your name")
                contact_email = st.text_input("Contact Email*", value=user.email)
            
            st.markdown("---")
            
            # Job Demand Data
            st.subheader("2️⃣ Job Demand Projections (Strategy 2)")
            col1, col2, col3 = st.columns(3)
            with col1:
                job_title = st.text_input("Critical Job Title*", placeholder="e.g., Maintenance Technician I")
                current_openings = st.number_input("Current Open Positions", min_value=0, value=0)
            with col2:
                annual_hires_needed = st.number_input("Annual Hires Needed*", min_value=1, value=5)
                incumbent_upskilling = st.number_input("Incumbent Workers Needing Upskilling", min_value=0, value=0)
            with col3:
                turnover_rate = st.slider("Annual Turnover Rate (%)", 0, 100, 15)
            
            st.markdown("---")
            
            # Cost Per Hire Data
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
            
            # Pipeline Impact
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
            
            # ROI Assessment
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
            submitted = st.form_submit_button("🚀 Submit Employer Data", use_container_width=True, type="primary")
            
            if submitted:
                if not all([company_name, contact_name, contact_email, job_title, annual_hires_needed]):
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
                    
                    # Create submission record
                    submission = Submission(
                        user_id=user.id,
                        company_name=company_name,
                        industry=industry,
                        contact_name=contact_name,
                        contact_email=contact_email,
                        job_title=job_title,
                        current_openings=current_openings,
                        annual_hires_needed=annual_hires_needed,
                        incumbent_upskilling=incumbent_upskilling,
                        turnover_rate=turnover_rate,
                        cost_per_hire=cost_per_hire,
                        onboarding_weeks=onboarding_weeks_baseline,
                        productivity_weeks=productivity_weeks_baseline,
                        weekly_productivity_cost=weekly_productivity_cost,
                        onboarding_reduction_weeks=onboarding_weeks_reduction,
                        activities_replaced=onboarding_activities_replaced,
                        productivity_improvement_pct=productivity_improvement,
                        retention_90day_current=retention_90day_current,
                        retention_1year_current=retention_1year_current,
                        retention_90day_target=retention_90day_target,
                        retention_1year_target=retention_1year_target,
                        credential_value=credential_value,
                        pilot_readiness=pilot_readiness,
                        roi_rating=roi_rating,
                        weeks_saved=roi['weeks_saved'],
                        savings_per_hire=roi['savings_per_hire'],
                        annual_savings=roi['annual_savings'],
                        payback_period=roi['payback_period'],
                        additional_notes=additional_notes
                    )
                    
                    db.add(submission)
                    db.commit()
                    
                    st.success("✅ Data submitted successfully!")
                    st.balloons()
                    
                    # Display ROI summary
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
        st.header("📋 My Submissions")
        
        my_submissions = db.query(Submission).filter(Submission.user_id == user.id).all()
        
        if my_submissions:
            st.metric("Your Total Submissions", len(my_submissions))
            
            # Display submissions
            display_data = []
            for sub in my_submissions:
                display_data.append({
                    'Date': sub.created_at.strftime('%Y-%m-%d'),
                    'Job Title': sub.job_title,
                    'Annual Hires': sub.annual_hires_needed,
                    'Cost/Hire': f"${sub.cost_per_hire:,.0f}",
                    'Weeks Saved': f"{sub.weeks_saved:.1f}",
                    'Annual Savings': f"${sub.annual_savings:,.0f}",
                    'ROI Rating': sub.roi_rating,
                    'Pilot Ready': "✅" if "Yes" in sub.pilot_readiness else "❌"
                })
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No submissions yet. Use the 'Submit Data' tab to add your first entry!")
    
    with tab3:
        st.header("📊 Analytics & Insights")
        
        metrics = get_analytics_metrics(db)
        
        if metrics['total_companies'] > 0:
            # Key metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Participating Companies", metrics['total_companies'])
            with col2:
                st.metric("Total Annual Hires", f"{metrics['total_hires']:,}")
            with col3:
                st.metric("Avg Cost/Hire", f"${metrics['avg_cost_per_hire']:,.0f}")
            with col4:
                st.metric("Total Annual Savings", f"${metrics['total_annual_savings']:,.0f}")
            with col5:
                st.metric("Avg Weeks Saved", f"{metrics['avg_weeks_saved']:.1f}")
            
            st.markdown("---")
            
            # Charts - Row 1
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_industry_chart(db), use_container_width=True)
            with col2:
                st.plotly_chart(create_pilot_readiness_chart(db), use_container_width=True)
            
            # Charts - Row 2
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_roi_distribution_chart(db), use_container_width=True)
            with col2:
                st.plotly_chart(create_retention_comparison_chart(db), use_container_width=True)
            
            # Charts - Row 3
            st.plotly_chart(create_savings_trend_chart(db), use_container_width=True)
            st.plotly_chart(create_cost_per_hire_distribution(db), use_container_width=True)
        else:
            st.info("ℹ️ No data available for analytics yet. Submit employer data to see insights!")
    
    with tab4:
        st.header("💾 Export Data")
        
        submissions = db.query(Submission).all()
        
        if submissions:
            st.info(f"Total submissions to export: {len(submissions)}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv_data = export_to_csv(submissions)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"employer_roi_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                excel_data = export_to_excel(submissions)
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data,
                    file_name=f"employer_roi_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col3:
                pdf_data = export_to_pdf(submissions)
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_data,
                    file_name=f"employer_roi_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("ℹ️ No data available for export yet.")
    
    with tab5:
        st.header("📈 Employer Dashboard")
        
        my_submissions = db.query(Submission).filter(Submission.user_id == user.id).all()
        
        if my_submissions:
            # Summary stats for this employer
            total_hires = sum(s.annual_hires_needed for s in my_submissions)
            total_savings = sum(s.annual_savings for s in my_submissions)
            avg_roi = sum(1 for s in my_submissions if s.roi_rating in ['Good', 'Excellent']) / len(my_submissions) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Annual Hires", total_hires)
            with col2:
                st.metric("Total Annual Savings", f"${total_savings:,.0f}")
            with col3:
                st.metric("Good/Excellent ROI %", f"{avg_roi:.0f}%")
            
            st.markdown("---")
            
            # Detailed submissions table
            st.subheader("📋 Submission History")
            
            detail_data = []
            for sub in my_submissions:
                detail_data.append({
                    'Date': sub.created_at.strftime('%Y-%m-%d %H:%M'),
                    'Job Title': sub.job_title,
                    'Industry': sub.industry,
                    'Hires': sub.annual_hires_needed,
                    'Cost/Hire': f"${sub.cost_per_hire:,.0f}",
                    'Savings/Hire': f"${sub.savings_per_hire:,.0f}",
                    'Annual Savings': f"${sub.annual_savings:,.0f}",
                    'ROI': sub.roi_rating,
                    'Pilot': sub.pilot_readiness.split(' - ')[0]
                })
            
            df = pd.DataFrame(detail_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ You haven't submitted any data yet.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p><strong>Talent Pipeline Management® (TPM) v2.0 - Strategy 6: Continuous Improvement</strong></p>
        <p>Measuring results to optimize talent pipelines and demonstrate ROI</p>
        <p style='font-size: 0.9em;'>Enhanced with Database, Authentication, Advanced Analytics & Export</p>
    </div>
    """, unsafe_allow_html=True)


# Main entry point
if st.session_state.user:
    main_app()
else:
    login_page()

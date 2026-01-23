# TPM Employer ROI Tracker v2.0

## 🎯 Overview
An enhanced employer-facing application for tracking workforce pathway employment data, with complete database integration, user authentication, advanced analytics, and multi-format export capabilities.

**Built for: Strategy 6 - Measuring Results for Continuous Improvement**

---

## ✨ What's New in v2.0

### A. Database Integration ✅
- **SQLite Database** for persistent, scalable data storage
- **SQLAlchemy ORM** for reliable data management
- User and submission records with relationships
- Automatic database creation on startup

### B. User Authentication ✅
- **Employer Account Creation** - Self-service registration
- **Secure Login** - Password-based authentication with hashing
- **User-Specific Data** - Each employer sees only their own submissions
- **Session Management** - Persistent user sessions across app usage

### C. Advanced Analytics & Visualizations ✅
- **Interactive Charts** (Plotly):
  - Industry distribution analysis
  - ROI rating comparisons
  - Pilot readiness status
  - Savings potential trends
  - Retention metrics
  - Cost per hire distribution
- **Aggregate Metrics** across all employers
- **Real-time Dashboard** updates

### D. Export Functionality ✅
- **CSV Export** - Spreadsheet-ready format
- **Excel Export** (.xlsx) - Formatted with proper styling
- **PDF Reports** - Professional summary reports
- All exports include timestamp and comprehensive data

### E. Enhanced Features ✅
- **Employer Dashboard** - Personal metrics and history
- **My Submissions Tab** - Track all submissions
- **5-Tab Interface** - Organized workflow
- **Improved UI** - Better navigation and visual hierarchy
- **Additional Industry Options** - Transportation, Retail, Hospitality

---

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run employer_roi_app.py
```
Or use the provided script:
```bash
bash run_app.sh
```

### 3. Access
- App opens at: `http://localhost:8501`
- **Demo Account** (pre-created):
  - Username: `demo`
  - Password: `demo`
  - Company: `Demo Manufacturing Co.`

### 4. Create Your Account
- Click "Create Account"
- Fill in company info
- Start submitting ROI data

---

## 📊 Features by Tab

### 📝 Submit Data
- **1️⃣ Company Information** - Company name, industry, contact details
- **2️⃣ Job Demand Projections** - Job titles, hiring needs, turnover
- **3️⃣ Hiring Costs** - Current baseline metrics
- **4️⃣ Pipeline Impact** - Projected improvements from training
- **5️⃣ Retention Metrics** - Current vs target retention rates
- **6️⃣ ROI Assessment** - Program readiness and expected ROI
- Automatic ROI calculations with instant feedback

### 📋 My Submissions
- View all your submitted data
- Track submissions by date
- See key metrics (weeks saved, savings per hire, annual ROI)
- Quick pilot readiness status

### 📊 Analytics
- **Global Metrics** - Total companies, hires, savings
- **Industry Breakdown** - Visual distribution chart
- **Pilot Readiness** - Status distribution pie chart
- **ROI Distribution** - Bar chart of savings by rating
- **Retention Comparison** - Current vs target rates
- **Savings Trends** - Top 10 companies visualization
- **Cost Per Hire** - Distribution histogram

### 💾 Export Data
- Download all submissions as **CSV**
- Export formatted **Excel** workbook
- Generate **PDF Reports** with summary metrics
- Perfect for sharing with education partners or leadership

### 📈 Dashboard
- **Personal Metrics**:
  - Total annual hires across submissions
  - Total annual savings potential
  - Good/Excellent ROI percentage
- **Submission History** - Detailed table of all entries
- Track your employer impact over time

---

## 🗄️ Database Structure

### Users Table
```
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (Hashed)
- company_name
- created_at, updated_at
```

### Submissions Table
```
- id (Primary Key)
- user_id (Foreign Key → Users)
- company_info (name, industry, contact)
- job_demand (titles, openings, hires needed)
- baseline_costs (cost per hire, onboarding weeks)
- pipeline_impact (reduction, improvement %)
- retention (90-day, 1-year rates)
- roi_assessment (rating, pilot readiness)
- calculated_roi (weeks saved, savings, payback)
- created_at, updated_at
```

---

## 🔐 Security

- **Password Hashing** - SHA-256 hashing for security
- **User Isolation** - Employers only see their data
- **Session State** - Managed through Streamlit sessions
- **Input Validation** - All fields validated before submission

---

## 📁 Project Structure

```
CLAUDE/
├── employer_roi_app.py       # Main app (v2.0)
├── employer_roi_app_v1.py    # Original app (backup)
├── database.py               # SQLAlchemy models & setup
├── auth.py                   # Authentication utilities
├── analytics.py              # Analytics & visualization functions
├── export_utils.py           # Export to CSV/Excel/PDF
├── requirements.txt          # Python dependencies
├── run_app.sh               # Launch script
├── employer_roi.db          # SQLite database (auto-created)
└── README.md                # This file
```

---

## 💻 Dependencies

| Package | Purpose |
|---------|---------|
| streamlit==1.31.0 | Web app framework |
| pandas==2.1.4 | Data analysis |
| sqlalchemy==2.0.23 | Database ORM |
| plotly==5.18.0 | Interactive charts |
| openpyxl==3.11.0 | Excel export |
| reportlab==4.0.7 | PDF generation |
| python-dotenv==1.0.0 | Environment config |

---

## 🎓 ROI Calculation Formula

The app automatically calculates:

- **Weeks Saved** = Baseline Onboarding Weeks - Projected Reduction
- **Savings Per Hire** = Weeks Saved × Weekly Productivity Cost
- **Annual Savings** = Savings Per Hire × Annual Hires Needed
- **Payback Period** = Cost Per Hire ÷ Savings Per Hire

Example:
- Baseline: 10 weeks, Projected: 8.5 weeks (1.5 week reduction)
- Weekly Productivity Cost: $2,000
- Annual Hires: 5
- Result: 1.5 × $2,000 × 5 = **$15,000 annual savings**

---

## 📈 Use Cases

1. **Employer Data Collection** - Systematic ROI data gathering
2. **Partner Program Assessment** - Evaluate pilot readiness
3. **Impact Reporting** - Generate professional reports
4. **Trend Analysis** - Compare industry, ROI, and retention patterns
5. **Board Presentations** - Export charts and summary data

---

## 🔧 Customization

### Add Industries
Edit line in `employer_roi_app.py`:
```python
industry = st.selectbox("Industry", [
    "Manufacturing",
    "Healthcare",
    # Add your industries here
])
```

### Adjust ROI Formula
Modify `calculate_roi()` function in `employer_roi_app.py`

### Change Database
Update `DATABASE_URL` in `database.py`:
```python
DATABASE_URL = "sqlite:///./employer_roi.db"  # SQLite
# Or use PostgreSQL, MySQL, etc.
```

---

## 🚨 Troubleshooting

### App Won't Start
```bash
# Clear cache
rm employer_roi.db
pip install --upgrade -r requirements.txt
streamlit run employer_roi_app.py
```

### Database Issues
```bash
# Reset database
rm employer_roi.db
# App will recreate on next run
```

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Support

For questions or enhancements:
- Review the code comments in each module
- Check the database structure in `database.py`
- Verify dependencies with `pip list`

---

## 📊 Metrics Tracked

Each submission captures:
- ✅ Current hiring costs & timelines
- ✅ Job demand projections
- ✅ Pipeline impact potential
- ✅ Retention rate improvements
- ✅ ROI projections (weeks, dollars, payback)
- ✅ Program readiness assessment
- ✅ Credential value ratings

---

## 🎯 Alignment with TPM Strategy 6

**Measuring Results for Continuous Improvement**

This application directly supports:
- ✅ Systematic data collection from employers
- ✅ ROI measurement and tracking
- ✅ Workforce pipeline effectiveness assessment
- ✅ Continuous improvement through data analysis
- ✅ Professional reporting to stakeholders

---

**Built for TPM Strategy 6 | Measuring Results for Continuous Improvement**

Version 2.0 | Enhanced with Database, Authentication, Analytics & Export | January 2026

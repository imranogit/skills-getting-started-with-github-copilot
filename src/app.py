"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Also includes a recruiter directory for hospitality / service-management /
gastronomy contacts in Berlin (Werkstudent roles) and Dubai (regular
positions), together with a simple application-tracking feature.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for interscholastic play",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and participate in friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["maya@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu", "liam@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Join our orchestra and band for musical performances",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots for STEM competitions",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and critical thinking skills",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["isabella@mergington.edu"]
    },
    "Mathematics Study Group": {
        "description": "Collaborative study sessions covering mathematical analysis, algebra, calculus, and problem-solving techniques for business and economics applications",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu", "mia@mergington.edu"]
    },
    "Statistics Workshop": {
        "description": "Hands-on workshop exploring statistical methods, data analysis, and probability theory with real-world applications",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["aiden@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is currently signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}


# ---------------------------------------------------------------------------
# Recruiter directory – hospitality / service management / gastronomy
# ---------------------------------------------------------------------------
# Each entry carries:
#   city          – "Berlin" or "Dubai"
#   role_type     – "Werkstudent" (Berlin) or "Regular" (Dubai)
#   company       – employer / agency name
#   contact_name  – known decision-maker / recruiter name (empty if unknown)
#   contact_email – recruiter e-mail (empty if not published)
#   linkedin      – LinkedIn profile / company page URL
#   sector        – sub-sector inside hospitality
#   notes         – any useful application hint
#   applications  – list of applicant e-mails who have submitted via this API
# ---------------------------------------------------------------------------
recruiters = {
    # ── BERLIN – WERKSTUDENT ────────────────────────────────────────────────
    "Marriott Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Marriott International – Berlin Hotels",
        "contact_name": "HR Recruiting Team",
        "contact_email": "careers.berlin@marriott.com",
        "linkedin": "https://www.linkedin.com/company/marriott-international",
        "sector": "Hotel / Front Office",
        "notes": (
            "Apply via Marriott Careers portal. Mention 20 h/week student-visa "
            "eligibility and Service Management study programme."
        ),
        "applications": [],
    },
    "Hilton Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Hilton Berlin",
        "contact_name": "Talent Acquisition",
        "contact_email": "jobs.berlin@hilton.com",
        "linkedin": "https://www.linkedin.com/company/hilton-hotels",
        "sector": "Hotel / Guest Relations",
        "notes": (
            "Hilton regularly posts Werkstudent openings on their careers site "
            "and LinkedIn. Filter by 'Werkstudent' in Berlin."
        ),
        "applications": [],
    },
    "Meininger Hotels Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Meininger Hotels GmbH",
        "contact_name": "People & Culture",
        "contact_email": "jobs@meininger-hotels.com",
        "linkedin": "https://www.linkedin.com/company/meininger-hotels",
        "sector": "Budget Hotel / Reception",
        "notes": (
            "Berlin-headquartered chain. Very open to Werkstudent applicants "
            "from Service Management programmes."
        ),
        "applications": [],
    },
    "25hours Hotels Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "25hours Hotels",
        "contact_name": "HR Department",
        "contact_email": "jobs@25hours-hotels.com",
        "linkedin": "https://www.linkedin.com/company/25hours-hotels",
        "sector": "Lifestyle Hotel / Operations",
        "notes": (
            "Boutique lifestyle brand. Strong culture fit for multilingual "
            "candidates with guest-service background."
        ),
        "applications": [],
    },
    "Motel One Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Motel One Group",
        "contact_name": "Recruitment",
        "contact_email": "bewerbung@motel-one.com",
        "linkedin": "https://www.linkedin.com/company/motel-one",
        "sector": "Budget Design Hotel / Front Desk",
        "notes": (
            "Motel One Berlin posts Werkstudent reception roles regularly; "
            "applications accepted in German or English."
        ),
        "applications": [],
    },
    "Kempinski Hotel Adlon Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Kempinski Hotels",
        "contact_name": "Human Resources",
        "contact_email": "careers.adlon@kempinski.com",
        "linkedin": "https://www.linkedin.com/company/kempinski-hotels",
        "sector": "Luxury Hotel / Guest Experience",
        "notes": (
            "Five-star property next to Brandenburg Gate. Arabic language "
            "skills are highly valued here."
        ),
        "applications": [],
    },
    "Gastrogate Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Gastrogate GmbH",
        "contact_name": "Recruiting",
        "contact_email": "jobs@gastrogate.com",
        "linkedin": "https://www.linkedin.com/company/gastrogate",
        "sector": "Gastronomy / Restaurant Operations",
        "notes": (
            "Berlin-based gastronomy staffing & consulting firm. Werkstudent "
            "roles in restaurant coordination and service."
        ),
        "applications": [],
    },
    "GHOTEL Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "GHOTEL Hotel & Living",
        "contact_name": "HR Team",
        "contact_email": "bewerbung@ghotel.de",
        "linkedin": "https://www.linkedin.com/company/ghotel-hotel-living",
        "sector": "Hotel / Service Operations",
        "notes": (
            "Growing German hotel chain. Frequently hires Werkstudenten for "
            "front-office and service-operations support."
        ),
        "applications": [],
    },
    "Michelin-Guide Restaurants Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Fine-Dining Restaurant Group Berlin",
        "contact_name": "Restaurant Manager",
        "contact_email": "",
        "linkedin": "https://www.linkedin.com/search/results/companies/?keywords=restaurant%20berlin",
        "sector": "Gastronomy / Fine Dining",
        "notes": (
            "Approach individual Michelin-listed restaurants (e.g. Rutz, "
            "Reinstoff) directly via LinkedIn or their careers page for "
            "Werkstudent service roles."
        ),
        "applications": [],
    },
    "Accor Hotels Berlin (Werkstudent)": {
        "city": "Berlin",
        "role_type": "Werkstudent",
        "company": "Accor Hotels – Berlin properties",
        "contact_name": "Talent Acquisition",
        "contact_email": "careers@accor.com",
        "linkedin": "https://www.linkedin.com/company/accorhotels",
        "sector": "Hotel / F&B / Front Office",
        "notes": (
            "Accor operates several brands in Berlin (Novotel, ibis, Sofitel). "
            "Filter careers.accor.com by city=Berlin and type=Werkstudent."
        ),
        "applications": [],
    },
    # ── DUBAI – REGULAR POSITIONS ───────────────────────────────────────────
    "Jumeirah Group Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Jumeirah Group",
        "contact_name": "Global Talent Acquisition",
        "contact_email": "careers@jumeirah.com",
        "linkedin": "https://www.linkedin.com/company/jumeirah-group",
        "sector": "Luxury Hotel / Guest Services",
        "notes": (
            "Dubai-headquartered luxury chain. Apply via jumeirah.com/careers. "
            "Outline preferred start date, salary expectations, and visa "
            "sponsorship requirement."
        ),
        "applications": [],
    },
    "Emaar Hospitality Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Emaar Hospitality Group",
        "contact_name": "HR Director",
        "contact_email": "hospitality.careers@emaar.ae",
        "linkedin": "https://www.linkedin.com/company/emaar-hospitality-group",
        "sector": "Hotel / Resort Operations",
        "notes": (
            "Operates Address Hotels, Vida Hotels, and Rove Hotels in Dubai. "
            "Emphasise multilingual guest-service skills and event experience."
        ),
        "applications": [],
    },
    "Rotana Hotels Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Rotana Hotel Management Corporation",
        "contact_name": "Talent Management Team",
        "contact_email": "careers@rotana.com",
        "linkedin": "https://www.linkedin.com/company/rotana",
        "sector": "Hotel / Front Office / F&B",
        "notes": (
            "Pan-regional chain with strong presence in Dubai. Arabic language "
            "proficiency (C1) is a significant differentiator."
        ),
        "applications": [],
    },
    "IHG Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "IHG Hotels & Resorts – Dubai",
        "contact_name": "Recruitment Hub MENA",
        "contact_email": "careers.mena@ihg.com",
        "linkedin": "https://www.linkedin.com/company/ihg",
        "sector": "Hotel / Guest Experience",
        "notes": (
            "IHG (InterContinental, Crowne Plaza, Holiday Inn) operates "
            "multiple Dubai properties. Mention conditions upfront: "
            "relocation support, housing allowance, annual leave."
        ),
        "applications": [],
    },
    "Marriott International Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Marriott International – Dubai",
        "contact_name": "MENA Talent Acquisition",
        "contact_email": "mena.careers@marriott.com",
        "linkedin": "https://www.linkedin.com/company/marriott-international",
        "sector": "Hotel / Service Operations",
        "notes": (
            "Many Marriott-brand hotels in Dubai (JW Marriott, Sheraton, W). "
            "State expected package, visa sponsorship needs, and availability."
        ),
        "applications": [],
    },
    "Minor Hotels Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Minor Hotels – UAE",
        "contact_name": "Area HR Manager UAE",
        "contact_email": "hr.uae@minorhotels.com",
        "linkedin": "https://www.linkedin.com/company/minor-hotels",
        "sector": "Hotel / Upscale Operations",
        "notes": (
            "NH Collection, Anantara, and Avani brands in the UAE. "
            "Growing regional footprint – good for first international role."
        ),
        "applications": [],
    },
    "Atlantis The Palm Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Atlantis Dubai (Kerzner International)",
        "contact_name": "Talent Acquisition Team",
        "contact_email": "careers@atlantisthepalm.com",
        "linkedin": "https://www.linkedin.com/company/atlantis-the-palm",
        "sector": "Resort / Entertainment / F&B",
        "notes": (
            "Iconic mega-resort. Emphasise event-operations and "
            "multilingual-guest experience from Dubai background."
        ),
        "applications": [],
    },
    "Four Seasons Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Four Seasons Hotels – Dubai",
        "contact_name": "Director of Human Resources",
        "contact_email": "careers.dubai@fourseasons.com",
        "linkedin": "https://www.linkedin.com/company/four-seasons-hotels-and-resorts",
        "sector": "Luxury Hotel / Guest Relations",
        "notes": (
            "Ultra-luxury segment; competition for spots is high. "
            "Target guest-relations or concierge roles matching language skills."
        ),
        "applications": [],
    },
    "Hakkasan Group Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Hakkasan Group – Dubai F&B",
        "contact_name": "HR Manager",
        "contact_email": "hr.dubai@hakkasan.com",
        "linkedin": "https://www.linkedin.com/company/hakkasan",
        "sector": "Gastronomy / Upscale Restaurant",
        "notes": (
            "Operates high-end restaurant and nightlife venues in Dubai. "
            "Service-management and guest-relations profiles in demand."
        ),
        "applications": [],
    },
    "Staffmark Hospitality Dubai": {
        "city": "Dubai",
        "role_type": "Regular",
        "company": "Staffmark / Michael Page Hospitality MENA",
        "contact_name": "Hospitality Division",
        "contact_email": "hospitality.mena@michaelpage.ae",
        "linkedin": "https://www.linkedin.com/company/michael-page",
        "sector": "Recruitment Agency / Hospitality",
        "notes": (
            "Specialist hospitality recruiter in the MENA region. "
            "Register your CV and request direct contact with their "
            "hospitality desk to discuss package conditions."
        ),
        "applications": [],
    },
}


# ---------------------------------------------------------------------------
# Recruiter endpoints
# ---------------------------------------------------------------------------

@app.get("/recruiters")
def get_recruiters(city: str = None, role_type: str = None):
    """Return the recruiter directory, optionally filtered by city or role_type."""
    result = recruiters
    if city:
        result = {k: v for k, v in result.items() if v["city"].lower() == city.lower()}
    if role_type:
        result = {k: v for k, v in result.items() if v["role_type"].lower() == role_type.lower()}
    return result


@app.post("/recruiters/{recruiter_name}/apply")
def apply_to_recruiter(recruiter_name: str, email: str):
    """
    Record an application submission to a recruiter entry.

    For Berlin Werkstudent entries this confirms a standard Werkstudent
    application. For Dubai Regular entries this records the intent to reach
    out with your conditions (salary expectations, relocation, availability).
    """
    if recruiter_name not in recruiters:
        raise HTTPException(status_code=404, detail="Recruiter not found")

    recruiter = recruiters[recruiter_name]

    if email in recruiter["applications"]:
        raise HTTPException(status_code=400, detail="Application already submitted to this recruiter")

    recruiter["applications"].append(email)

    role_type = recruiter["role_type"]
    city = recruiter["city"]
    if role_type == "Werkstudent":
        msg = (
            f"Werkstudent application from {email} recorded for "
            f"{recruiter_name} in {city}."
        )
    else:
        msg = (
            f"Application with conditions from {email} recorded for "
            f"{recruiter_name} in {city}. "
            "Remember to include your salary expectations, visa/relocation "
            "requirements, and preferred start date in your outreach."
        )
    return {"message": msg}

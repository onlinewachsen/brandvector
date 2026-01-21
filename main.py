import streamlit as st
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
import json
import base64
import pandas as pd
from datetime import datetime


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")


client = OpenAI(api_key=OPENAI_API_KEY)


st.set_page_config(
    page_title="BrandVector - AI Visibility Tracker",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main {
        background-color: transparent;
    }
    
    .header-container {
        background: rgba(26, 26, 46, 0.95);
        backdrop-filter: blur(20px);
        padding: 50px 40px;
        border-radius: 24px;
        box-shadow: 0 25px 70px rgba(0,0,0,0.5);
        margin-bottom: 40px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .main-title {
        font-size: 4em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        letter-spacing: -2px;
    }
    
    .subtitle {
        color: #e0e0e0;
        font-size: 1.4em;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .glass-card {
        background: rgba(26, 26, 46, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 35px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 25px;
    }
    
    .section-header {
        font-size: 1.8em;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    .section-subheader {
        font-size: 1.1em;
        color: #b0b0b0;
        margin-bottom: 25px;
        font-weight: 500;
    }
    
    .custom-metric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 30px 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .custom-metric:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 45px rgba(102, 126, 234, 0.5);
    }
    
    .metric-value {
        font-size: 2.8em;
        font-weight: 800;
        margin: 15px 0;
        letter-spacing: -1px;
        color: #ffffff;
    }
    
    .metric-label {
        font-size: 0.95em;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        color: #ffffff;
    }
    
    .success-metric {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        box-shadow: 0 12px 35px rgba(16, 185, 129, 0.4);
    }
    
    .success-metric:hover {
        box-shadow: 0 18px 45px rgba(16, 185, 129, 0.5);
    }
    
    .error-metric {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        box-shadow: 0 12px 35px rgba(239, 68, 68, 0.4);
    }
    
    .error-metric:hover {
        box-shadow: 0 18px 45px rgba(239, 68, 68, 0.5);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        box-shadow: 0 12px 35px rgba(245, 158, 11, 0.4);
    }
    
    .warning-metric:hover {
        box-shadow: 0 18px 45px rgba(245, 158, 11, 0.5);
    }
    
    .ranking-card {
        background: rgba(26, 26, 46, 0.9);
        border-radius: 16px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border-left: 4px solid #667eea;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .ranking-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
        border-left-width: 6px;
    }
    
    .rank-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.3em;
        display: inline-block;
        margin-right: 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .rank-title {
        font-size: 1.35em;
        font-weight: 700;
        color: #ffffff;
        margin: 15px 0;
        line-height: 1.4;
    }
    
    .rank-url {
        color: #8b9aff;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.05em;
        transition: color 0.2s;
    }
    
    .rank-url:hover {
        color: #a8b5ff;
        text-decoration: underline;
    }
    
    .rank-description {
        color: #c0c0c0;
        margin-top: 15px;
        line-height: 1.7;
        font-size: 1.05em;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff !important;
        border: none;
        padding: 18px 45px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.15em;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 45px rgba(102, 126, 234, 0.5);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(26, 26, 46, 0.95);
        backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    .ai-overview {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        margin: 25px 0;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .ai-overview h3 {
        font-size: 1.6em;
        font-weight: 700;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    
    .ai-overview p {
        line-height: 1.8;
        font-size: 1.1em;
        color: #ffffff;
    }
    
    .location-badge {
        background: rgba(102, 126, 234, 0.2);
        color: #ffffff;
        padding: 12px 28px;
        border-radius: 50px;
        display: inline-block;
        font-weight: 700;
        margin: 15px 0;
        font-size: 1.1em;
        border: 2px solid rgba(102, 126, 234, 0.4);
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 14px 18px;
        font-size: 1.05em;
        transition: all 0.2s;
        background: rgba(26, 26, 46, 0.5);
        color: #ffffff;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    .stTextInput > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stRadio > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stRadio > div {
        color: #ffffff !important;
    }
    
    .stSelectbox > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(26, 26, 46, 0.5);
        color: #ffffff;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    .stCheckbox > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stAlert {
        background: rgba(26, 26, 46, 0.9);
        color: #ffffff;
        border-left: 4px solid #667eea;
    }
    
    .streamlit-expanderHeader {
        background: rgba(26, 26, 46, 0.5);
        color: #ffffff !important;
        border-radius: 10px;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 26, 46, 0.3);
        color: #ffffff;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated {
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 40px 0;
    }
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 46, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Local SEO Audit Styles */
    .audit-score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5em;
        font-weight: 800;
        color: white;
        margin: 0 auto;
    }
    
    .score-excellent { background: linear-gradient(135deg, #10b981, #059669); }
    .score-good { background: linear-gradient(135deg, #3b82f6, #2563eb); }
    .score-fair { background: linear-gradient(135deg, #f59e0b, #d97706); }
    .score-poor { background: linear-gradient(135deg, #ef4444, #dc2626); }
    
    .finding-card {
        background: rgba(26, 26, 46, 0.9);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        border-left: 4px solid;
    }
    
    .finding-critical { border-color: #ef4444; background: rgba(239, 68, 68, 0.1); }
    .finding-important { border-color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
    .finding-optimize { border-color: #3b82f6; background: rgba(59, 130, 246, 0.1); }
    .finding-positive { border-color: #10b981; background: rgba(16, 185, 129, 0.1); }
    
    .progress-bar-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    .action-item {
        background: rgba(26, 26, 46, 0.9);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 10px 0;
        display: flex;
        align-items: flex-start;
        gap: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .action-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    .industry-rec {
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div class="header-container animated">
        <div class="main-title">BrandVector</div>
        <div class="subtitle">AI-Powered Visibility & Ranking Intelligence</div>
    </div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### Analyse-Einstellungen")
    
    analysis_mode = st.radio(
        "Wähle deinen Analyse-Modus",
        ["Marken-Analyse", "Keyword-Recherche", "Ranking-Check", "Local SEO Audit"],
        help="Verschiedene Analyse-Modi für unterschiedliche Bedürfnisse"
    )
    
    st.markdown("---")
    st.markdown("### Standort-Targeting")
    local_search = st.toggle("Lokale Suche aktivieren", value=False)
    
    if local_search:
        city = st.text_input("Stadt", placeholder="z.B. Koblenz, Berlin, München")
        if city:
            st.success(f"Standort gesetzt: {city}")
    else:
        city = None
    
    country = st.selectbox("Land", ["Deutschland", "Österreich", "Schweiz"], index=0)
    
    st.markdown("---")
    st.markdown("### Pro-Tipps")
    st.info("Nutze lokale Suche für standortspezifische Rankings")
    st.info("Ranking-Check zeigt Top 100 Ergebnisse")
    st.info("AI Overview Detection inklusive")
    st.info("🆕 Local SEO Audit für lokale Unternehmen")


LOCATION_CODES = {
    "Deutschland": 2276,
    "Österreich": 2040,
    "Schweiz": 2756
}

# Branchenspezifische Verzeichnisse
INDUSTRY_DIRECTORIES = {
    "restaurant": ["TripAdvisor", "Lieferando", "TheFork", "Yelp"],
    "healthcare": ["Jameda", "Doctolib", "Sanego", "Arzt-Auskunft"],
    "legal": ["Anwalt.de", "Rechtsanwalt.com", "Fachanwalt.de"],
    "financial": ["WhoFinance", "Steuerberater.de", "Finanztip"],
    "automotive": ["AutoScout24", "Mobile.de", "Werkstattportal"],
    "beauty": ["Treatwell", "Friseur.com", "Wellness-Portal"],
    "hotel": ["Booking.com", "TripAdvisor", "HRS", "Trivago"],
    "realestate": ["Immobilienscout24", "Immonet", "Immowelt"],
    "construction": ["MyHammer", "Handwerker.de", "Baulinks"],
    "fitness": ["FitFinder", "Gym-Finder"],
    "retail": ["Marktjagd", "KaufDA"],
    "other": []
}

# Branchenlabels
INDUSTRY_LABELS = {
    "restaurant": "Gastronomie",
    "healthcare": "Gesundheitswesen",
    "legal": "Rechtsberatung",
    "financial": "Finanzdienstleistung",
    "automotive": "Automotive",
    "beauty": "Beauty & Wellness",
    "hotel": "Hotellerie",
    "realestate": "Immobilien",
    "construction": "Handwerk",
    "fitness": "Fitness",
    "retail": "Einzelhandel",
    "other": "Sonstige"
}


def check_perplexity(brand, keyword):
    try:
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "sonar",
            "messages": [{"role": "user", "content": f"Empfiehl mir die besten Anbieter für {keyword}. Liste 5-10 Optionen auf."}]
        }
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        is_mentioned = brand.lower() in content.lower()
        return {"success": True, "mentioned": is_mentioned, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e), "mentioned": False, "content": ""}


def get_serp_rankings(keyword, city=None, country="Deutschland"):
    try:
        cred = f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}"
        encoded_cred = base64.b64encode(cred.encode()).decode()
        url = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
        
        payload_data = {
            "keyword": keyword,
            "language_code": "de",
            "device": "desktop",
            "os": "windows",
            "depth": 100
        }
        
        if city:
            payload_data["location_name"] = city
        else:
            payload_data["location_code"] = LOCATION_CODES.get(country, 2276)
        
        headers = {
            "Authorization": f"Basic {encoded_cred}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=[payload_data], headers=headers)
        response.raise_for_status()
        result = response.json()
        
        rankings = []
        ai_overview_found = False
        ai_overview_content = ""
        
        if result.get("tasks") and len(result["tasks"]) > 0:
            task = result["tasks"][0]
            if task.get("result") and len(task["result"]) > 0:
                items = task["result"][0].get("items", [])
                position = 1
                for item in items:
                    if item.get("type") == "ai_overview":
                        ai_overview_found = True
                        ai_overview_content = item.get("text", "")
                    elif item.get("type") == "organic":
                        rankings.append({
                            "position": position,
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "domain": item.get("domain", ""),
                            "description": item.get("description", "")
                        })
                        position += 1
        
        return {
            "success": True,
            "rankings": rankings,
            "ai_overview_found": ai_overview_found,
            "ai_overview_content": ai_overview_content,
            "total_results": len(rankings),
            "location": city if city else country
        }
    except Exception as e:
        st.error(f"DataForSEO API Fehler: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "rankings": [],
            "ai_overview_found": False,
            "ai_overview_content": "",
            "total_results": 0
        }


def analyze_keyword(keyword):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein SEO-Experte. Gib mir 15 verwandte Keywords mit Suchintention. Format: '1. Keyword (Intention)'"},
                {"role": "user", "content": f"Keyword: {keyword}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Fehler: {str(e)}"


def analyze_sentiment(text, brand):
    if not text or len(text) < 10:
        return "Neutral"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Analysiere das Sentiment. Antworte nur mit: Positiv, Neutral oder Negativ"},
                {"role": "user", "content": f"Marke '{brand}' in:\n\n{text}"}
            ],
            max_tokens=10,
            temperature=0
        )
        sentiment = response.choices[0].message.content.strip()
        if "positiv" in sentiment.lower():
            return "Positiv"
        elif "negativ" in sentiment.lower():
            return "Negativ"
        else:
            return "Neutral"
    except:
        return "Neutral"


def run_local_seo_audit(data):
    """Führt die Local SEO Analyse durch und berechnet Scores"""
    findings = {"critical": [], "important": [], "optimize": [], "positive": []}
    scores = {"google": 0, "reviews": 0, "citations": 0, "website": 0, "social": 0}
    
    # Google Business Analyse
    gb = data.get("google_business", "")
    if gb == "none":
        findings["critical"].append({
            "title": "Kein Google Unternehmensprofil",
            "desc": "Sie haben keinen Google-Eintrag.",
            "impact": "Ohne Profil erscheinen Sie nicht im Local Pack (46% aller Suchanfragen).",
            "action": "Erstellen Sie sofort einen Eintrag unter business.google.com",
            "effort": "Mittel"
        })
        scores["google"] = 0
    elif gb == "unclaimed":
        findings["critical"].append({
            "title": "Google-Profil nicht beansprucht",
            "desc": "Ihr Eintrag existiert, aber Sie haben keine Kontrolle.",
            "impact": "Andere können falsche Informationen eintragen.",
            "action": "Beanspruchen Sie Ihren Eintrag unter business.google.com",
            "effort": "Niedrig"
        })
        scores["google"] = 15
    elif gb == "claimed":
        findings["important"].append({
            "title": "Google-Profil unvollständig",
            "desc": "Beansprucht aber nicht komplett ausgefüllt.",
            "impact": "Vollständige Profile erhalten 7x mehr Klicks.",
            "action": "Ergänzen: Beschreibung, Fotos, Öffnungszeiten, Services",
            "effort": "Mittel"
        })
        scores["google"] = 50
    elif gb == "complete":
        findings["optimize"].append({
            "title": "Google-Profil vollständig",
            "desc": "Gute Basis vorhanden.",
            "impact": "Regelmäßige Aktivität verbessert das Ranking.",
            "action": "Wöchentlich Posts veröffentlichen, neue Fotos hinzufügen",
            "effort": "Niedrig"
        })
        scores["google"] = 75
    elif gb == "optimized":
        findings["positive"].append({
            "title": "Google-Profil optimal gepflegt",
            "desc": "Alle Funktionen werden aktiv genutzt.",
            "impact": "Wettbewerbsvorteil gegenüber weniger aktiven Mitbewerbern.",
            "action": "Weiter so! Neue Google-Features testen.",
            "effort": "Niedrig"
        })
        scores["google"] = 95
    
    # Bewertungen Analyse
    review_count = data.get("review_count", 0)
    avg_rating = data.get("avg_rating", 0)
    
    if review_count == 0:
        findings["critical"].append({
            "title": "Keine Google-Bewertungen",
            "desc": "Sie haben noch keine Bewertungen.",
            "impact": "88% der Nutzer vertrauen Bewertungen wie persönlichen Empfehlungen.",
            "action": "Systematisches Bewertungsmarketing starten: QR-Codes, E-Mail-Follow-ups",
            "effort": "Mittel"
        })
        scores["reviews"] = 0
    elif review_count < 10:
        findings["important"].append({
            "title": f"Wenige Bewertungen ({review_count})",
            "desc": "Mindestens 20-30 Bewertungen werden empfohlen.",
            "impact": "Mehr Bewertungen = mehr Vertrauen = besseres Ranking.",
            "action": "Jeden zufriedenen Kunden aktiv um Bewertung bitten.",
            "effort": "Mittel"
        })
        scores["reviews"] = 30
    elif review_count < 30:
        findings["optimize"].append({
            "title": f"Solide Bewertungsanzahl ({review_count})",
            "desc": "Gute Basis, aber ausbaufähig.",
            "impact": "Ziel: 50+ Bewertungen für starke Position.",
            "action": "Bewertungsanfragen automatisieren.",
            "effort": "Niedrig"
        })
        scores["reviews"] = 60
    else:
        findings["positive"].append({
            "title": f"Starke Bewertungsanzahl ({review_count})",
            "desc": "Überdurchschnittlich viele Bewertungen.",
            "impact": "Wichtiger Vertrauensfaktor.",
            "action": "Fokus auf Qualität und Aktualität.",
            "effort": "Niedrig"
        })
        scores["reviews"] = 85
    
    # Rating Check
    if avg_rating > 0 and avg_rating < 4:
        findings["critical"].append({
            "title": f"Kritische Bewertung ({avg_rating}⭐)",
            "desc": "Unter dem 4-Sterne-Schwellenwert.",
            "impact": "57% der Nutzer wählen nur 4+ Sterne Unternehmen.",
            "action": "Servicequalität verbessern, auf Kritik reagieren.",
            "effort": "Hoch"
        })
        scores["reviews"] = min(scores["reviews"], 25)
    elif avg_rating >= 4.5:
        findings["positive"].append({
            "title": f"Exzellente Bewertung ({avg_rating}⭐)",
            "desc": "Top-Bewertung.",
            "impact": "Starker Vertrauensfaktor.",
            "action": "Niveau halten, auf Website zeigen.",
            "effort": "Niedrig"
        })
        scores["reviews"] = min(scores["reviews"] + 10, 95)
    
    # Review Response
    if data.get("review_response") == "never":
        findings["important"].append({
            "title": "Keine Antworten auf Bewertungen",
            "desc": "Bewertungen werden nicht beantwortet.",
            "impact": "45% der Kunden erwarten eine Antwort.",
            "action": "Alle Bewertungen beantworten - positiv wie negativ.",
            "effort": "Niedrig"
        })
    
    # Citations
    directories = data.get("directories", [])
    citation_count = len(directories)
    
    if citation_count < 3:
        findings["critical"].append({
            "title": f"Wenige Verzeichnisse ({citation_count})",
            "desc": "Kaum Verzeichniseinträge vorhanden.",
            "impact": "Citations sind ein wichtiger Rankingfaktor.",
            "action": "Basis-Verzeichnisse: Gelbe Seiten, Das Örtliche, Bing, Apple Maps",
            "effort": "Mittel"
        })
        scores["citations"] = 10
    elif citation_count < 6:
        findings["important"].append({
            "title": f"Ausbaufähige Präsenz ({citation_count} Einträge)",
            "desc": "Grundpräsenz vorhanden.",
            "impact": "Mehr konsistente Einträge = besseres Ranking.",
            "action": "Weitere Verzeichnisse hinzufügen.",
            "effort": "Mittel"
        })
        scores["citations"] = 45
    else:
        findings["positive"].append({
            "title": f"Gute Verzeichnisabdeckung ({citation_count})",
            "desc": "Solide Präsenz.",
            "impact": "Fokus auf Konsistenz.",
            "action": "Regelmäßig auf Aktualität prüfen.",
            "effort": "Niedrig"
        })
        scores["citations"] = 75
    
    # NAP Konsistenz
    if data.get("nap_consistency") == "inconsistent":
        findings["critical"].append({
            "title": "NAP-Daten inkonsistent",
            "desc": "Unterschiedliche Angaben auf verschiedenen Plattformen.",
            "impact": "Verwirrt Google, schadet dem Ranking erheblich.",
            "action": "ALLE Einträge vereinheitlichen: Name, Adresse, Telefon.",
            "effort": "Hoch"
        })
        scores["citations"] = max(scores["citations"] - 30, 0)
    elif data.get("nap_consistency") == "perfect":
        findings["positive"].append({
            "title": "Perfekte NAP-Konsistenz",
            "desc": "Alle Daten sind überall identisch.",
            "impact": "Wichtiger Vertrauensfaktor für Google.",
            "action": "Standard dokumentieren für zukünftige Einträge.",
            "effort": "Niedrig"
        })
        scores["citations"] = min(scores["citations"] + 10, 95)
    
    # Website
    if not data.get("website"):
        findings["critical"].append({
            "title": "Keine Website",
            "desc": "Keine Website vorhanden.",
            "impact": "Fehlende Vertrauensbasis für Kunden.",
            "action": "Professionelle Website mit lokalem Fokus erstellen.",
            "effort": "Hoch"
        })
        scores["website"] = 0
    else:
        findings["optimize"].append({
            "title": "Website vorhanden",
            "desc": "Website ist angegeben.",
            "impact": "Technische Optimierung empfohlen.",
            "action": "Prüfen: Mobile, HTTPS, lokale Keywords, Schema Markup",
            "effort": "Mittel"
        })
        scores["website"] = 60
    
    # Social Media
    social_channels = data.get("social_media", [])
    if len(social_channels) == 0:
        findings["optimize"].append({
            "title": "Keine Social Media Präsenz",
            "desc": "Keine aktiven Kanäle.",
            "impact": "Social Signals sind indirekter Rankingfaktor.",
            "action": "Mit 1-2 relevanten Kanälen starten.",
            "effort": "Mittel"
        })
        scores["social"] = 20
    elif data.get("social_frequency") in ["rarely", "never"]:
        findings["important"].append({
            "title": "Social Media inaktiv",
            "desc": "Kanäle vorhanden, kaum Aktivität.",
            "impact": "Inaktive Profile wirken unprofessionell.",
            "action": "Content-Plan: 2-3 Posts pro Woche.",
            "effort": "Mittel"
        })
        scores["social"] = 40
    else:
        findings["positive"].append({
            "title": "Social Media aktiv",
            "desc": f"{len(social_channels)} aktive Kanäle.",
            "impact": "Stärkt Marke und Social Signals.",
            "action": "Mit Google-Profil verknüpfen.",
            "effort": "Niedrig"
        })
        scores["social"] = 80
    
    # Gesamtscore berechnen (gewichtet)
    total_score = round(
        scores["google"] * 0.35 +
        scores["reviews"] * 0.25 +
        scores["citations"] * 0.20 +
        scores["website"] * 0.12 +
        scores["social"] * 0.08
    )
    
    return {
        "total_score": total_score,
        "scores": scores,
        "findings": findings
    }


def get_score_class(score):
    """Gibt die CSS-Klasse basierend auf dem Score zurück"""
    if score >= 80:
        return "score-excellent"
    elif score >= 60:
        return "score-good"
    elif score >= 40:
        return "score-fair"
    else:
        return "score-poor"


def get_score_label(score):
    """Gibt das Label basierend auf dem Score zurück"""
    if score >= 80:
        return "Ausgezeichnet", "Top-Performance"
    elif score >= 60:
        return "Gut", "Optimierungspotenzial"
    elif score >= 40:
        return "Ausbaufähig", "Handlungsbedarf"
    else:
        return "Kritisch", "Sofortiger Handlungsbedarf"


def get_bar_color(score):
    """Gibt die Farbe für den Fortschrittsbalken zurück"""
    if score >= 80:
        return "#10b981"
    elif score >= 60:
        return "#3b82f6"
    elif score >= 40:
        return "#f59e0b"
    else:
        return "#ef4444"


# ==================== ANALYSE MODI ====================

if analysis_mode == "Marken-Analyse":
    st.markdown('<div class="glass-card animated"><div class="section-header">Marken-Sichtbarkeits-Analyse</div><div class="section-subheader">Überprüfe, wie sichtbar deine Marke in KI-Systemen und Google ist</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        brand_name = st.text_input("Markenname", placeholder="z.B. onlinewachsen.de")
    with col2:
        keyword = st.text_input("Ziel-Keyword", placeholder="z.B. SEO Agentur Koblenz")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("ANALYSE STARTEN", type="primary", use_container_width=True):
        if not brand_name or not keyword:
            st.error("Bitte fülle beide Felder aus")
        else:
            with st.spinner("Analysiere deine Marken-Sichtbarkeit..."):
                perplexity_result = check_perplexity(brand_name, keyword)
                serp_result = get_serp_rankings(keyword, city, country)
                
                brand_in_serp = False
                brand_position = None
                for rank in serp_result.get("rankings", []):
                    if brand_name.lower() in rank["domain"].lower() or brand_name.lower() in rank["title"].lower():
                        brand_in_serp = True
                        brand_position = rank["position"]
                        break
                
                st.markdown("---")
                
                if city:
                    st.markdown(f'<div class="location-badge">Standort: {city}, {country}</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    metric_class = "success-metric" if perplexity_result["mentioned"] else "error-metric"
                    status = "Erwähnt" if perplexity_result["mentioned"] else "Nicht erwähnt"
                    st.markdown(f'<div class="custom-metric {metric_class} animated"><div class="metric-label">Perplexity AI</div><div class="metric-value">{status}</div></div>', unsafe_allow_html=True)
                
                with col2:
                    if brand_in_serp:
                        st.markdown(f'<div class="custom-metric success-metric animated"><div class="metric-label">Google Position</div><div class="metric-value">#{brand_position}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="custom-metric error-metric animated"><div class="metric-label">Google Position</div><div class="metric-value">Nicht in Top 100</div></div>', unsafe_allow_html=True)
                
                with col3:
                    metric_class = "success-metric" if serp_result.get("ai_overview_found") else "warning-metric"
                    status = "Vorhanden" if serp_result.get("ai_overview_found") else "Nicht vorhanden"
                    st.markdown(f'<div class="custom-metric {metric_class} animated"><div class="metric-label">AI Overview</div><div class="metric-value">{status}</div></div>', unsafe_allow_html=True)
                
                with col4:
                    if perplexity_result["mentioned"]:
                        sentiment = analyze_sentiment(perplexity_result["content"], brand_name)
                        metric_class = "success-metric" if sentiment == "Positiv" else "warning-metric" if sentiment == "Neutral" else "error-metric"
                        st.markdown(f'<div class="custom-metric {metric_class} animated"><div class="metric-label">Sentiment</div><div class="metric-value">{sentiment}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="custom-metric animated"><div class="metric-label">Sentiment</div><div class="metric-value">N/A</div></div>', unsafe_allow_html=True)
                
                with st.expander("Detaillierte Perplexity-Antwort"):
                    if perplexity_result["success"]:
                        st.write(perplexity_result["content"])
                    else:
                        st.error(f"Fehler: {perplexity_result.get('error')}")


elif analysis_mode == "Keyword-Recherche":
    st.markdown('<div class="glass-card animated"><div class="section-header">AI-Powered Keyword-Recherche</div><div class="section-subheader">Generiere verwandte Keywords mit KI-Unterstützung</div>', unsafe_allow_html=True)
    keyword_input = st.text_input("Haupt-Keyword", placeholder="z.B. Online Marketing")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("KEYWORDS GENERIEREN", type="primary", use_container_width=True):
        if not keyword_input:
            st.error("Bitte gib ein Keyword ein")
        else:
            with st.spinner("KI analysiert und generiert Keywords..."):
                keywords = analyze_keyword(keyword_input)
                st.markdown(f'<div class="glass-card animated"><div class="section-header">Generierte Keyword-Ideen</div><div style="color: #ffffff;">{keywords}</div></div>', unsafe_allow_html=True)
                st.success("Keywords erfolgreich generiert")


elif analysis_mode == "Ranking-Check":
    st.markdown('<div class="glass-card animated"><div class="section-header">Live Google Ranking Analyse</div><div class="section-subheader">Prüfe die aktuellen Top-Rankings für dein Keyword</div>', unsafe_allow_html=True)
    keyword_check = st.text_input("Keyword", placeholder="z.B. SEO Agentur Koblenz")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("RANKINGS LADEN", type="primary", use_container_width=True):
        if not keyword_check:
            st.error("Bitte gib ein Keyword ein")
        else:
            with st.spinner("Lade Live-Rankings von Google..."):
                serp_data = get_serp_rankings(keyword_check, city, country)
                
                if serp_data["success"]:
                    location_text = f"{city}, {country}" if city else country
                    st.markdown(f'<div class="location-badge">Standort: {location_text}</div>', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<div class="custom-metric success-metric animated"><div class="metric-label">Gefundene Ergebnisse</div><div class="metric-value">{serp_data["total_results"]}</div></div>', unsafe_allow_html=True)
                    
                    with col2:
                        ai_status = "Vorhanden" if serp_data["ai_overview_found"] else "Nicht vorhanden"
                        metric_class = "success-metric" if serp_data["ai_overview_found"] else "warning-metric"
                        st.markdown(f'<div class="custom-metric {metric_class} animated"><div class="metric-label">AI Overview</div><div class="metric-value">{ai_status}</div></div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f'<div class="custom-metric animated"><div class="metric-label">Zeitstempel</div><div class="metric-value">{datetime.now().strftime("%H:%M")}</div></div>', unsafe_allow_html=True)
                    
                    if serp_data["ai_overview_found"]:
                        st.markdown(f'<div class="ai-overview animated"><h3>Google AI Overview</h3><p>{serp_data["ai_overview_content"]}</p></div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="section-header" style="margin-top: 40px; color: #ffffff;">Top Google Rankings</div>', unsafe_allow_html=True)
                    
                    for rank in serp_data["rankings"][:20]:
                        desc = rank['description'][:250] if rank['description'] else ""
                        st.markdown(f'<div class="ranking-card animated"><span class="rank-badge">#{rank["position"]}</span><div class="rank-title">{rank["title"]}</div><a href="{rank["url"]}" target="_blank" class="rank-url">{rank["domain"]}</a><div class="rank-description">{desc}...</div></div>', unsafe_allow_html=True)
                else:
                    st.error(f"Fehler beim Laden der Rankings: {serp_data.get('error')}")


elif analysis_mode == "Local SEO Audit":
    st.markdown('<div class="glass-card animated"><div class="section-header">🏢 Local SEO Audit</div><div class="section-subheader">Umfassende Analyse Ihrer lokalen Online-Präsenz</div>', unsafe_allow_html=True)
    
    # Initialisiere Session State für den Audit
    if "audit_step" not in st.session_state:
        st.session_state.audit_step = 1
    if "audit_data" not in st.session_state:
        st.session_state.audit_data = {}
    
    # Tab-Navigation
    tab1, tab2, tab3 = st.tabs(["1️⃣ Unternehmensdaten", "2️⃣ Online-Präsenz", "3️⃣ Ergebnis"])
    
    with tab1:
        st.markdown("#### Grundlegende Informationen")
        
        col1, col2 = st.columns(2)
        with col1:
            business_name = st.text_input("Unternehmensname *", placeholder="Mustermann GmbH", key="audit_business_name")
            industry = st.selectbox("Branche *", 
                ["", "restaurant", "healthcare", "legal", "financial", "automotive", 
                 "beauty", "fitness", "realestate", "construction", "hotel", "retail", "other"],
                format_func=lambda x: INDUSTRY_LABELS.get(x, "Auswählen...") if x else "Auswählen...",
                key="audit_industry"
            )
        with col2:
            address = st.text_input("Adresse *", placeholder="Musterstraße 1, 50667 Köln", key="audit_address")
            phone = st.text_input("Telefon", placeholder="+49 221 1234567", key="audit_phone")
        
        col3, col4 = st.columns(2)
        with col3:
            target_radius = st.selectbox("Einzugsgebiet", 
                ["5 km - Stadtteil", "10 km - Stadt", "25 km - Region", "50 km - Großregion"],
                index=2, key="audit_radius"
            )
            business_type = st.selectbox("Geschäftsmodell",
                ["Ladengeschäft", "Service vor Ort", "Hybrid"],
                key="audit_business_type"
            )
        with col4:
            years_in_business = st.selectbox("Jahre im Geschäft",
                ["Neugründung", "1-2 Jahre", "3-5 Jahre", "5-10 Jahre", "10+ Jahre"],
                key="audit_years"
            )
            target_keywords = st.text_input("Haupt-Keywords", placeholder="Steuerberater Köln, Buchhaltung", key="audit_keywords")
        
        competitors = st.text_input("Bekannte Wettbewerber (optional)", placeholder="Müller GmbH, Schmidt & Partner", key="audit_competitors")
    
    with tab2:
        st.markdown("#### Google & Bewertungen")
        
        col1, col2 = st.columns(2)
        with col1:
            website = st.text_input("Website", placeholder="https://www.beispiel.de", key="audit_website")
            google_business = st.selectbox("Google Unternehmensprofil",
                ["", "none", "unclaimed", "claimed", "complete", "optimized"],
                format_func=lambda x: {
                    "": "Auswählen...",
                    "none": "Nicht vorhanden",
                    "unclaimed": "Nicht beansprucht",
                    "claimed": "Beansprucht, unvollständig",
                    "complete": "Vollständig eingerichtet",
                    "optimized": "Optimiert & aktiv"
                }.get(x, x),
                key="audit_google"
            )
        with col2:
            review_count = st.number_input("Anzahl Google-Bewertungen", min_value=0, value=0, key="audit_reviews")
            avg_rating = st.selectbox("Durchschnittsbewertung",
                [0, 2, 3, 3.5, 4, 4.5, 5],
                format_func=lambda x: f"{x} ⭐" if x > 0 else "Keine Bewertungen",
                key="audit_rating"
            )
        
        col3, col4 = st.columns(2)
        with col3:
            review_response = st.selectbox("Beantworten Sie Bewertungen?",
                ["", "all", "negative", "sometimes", "never"],
                format_func=lambda x: {
                    "": "Auswählen...",
                    "all": "Alle",
                    "negative": "Nur negative",
                    "sometimes": "Manchmal",
                    "never": "Nie"
                }.get(x, x),
                key="audit_response"
            )
        with col4:
            gmb_posts = st.selectbox("Google Posts?",
                ["", "weekly", "monthly", "rarely", "never"],
                format_func=lambda x: {
                    "": "Auswählen...",
                    "weekly": "Wöchentlich",
                    "monthly": "Monatlich",
                    "rarely": "Selten",
                    "never": "Nie"
                }.get(x, x),
                key="audit_posts"
            )
        
        st.markdown("#### Verzeichniseinträge")
        dir_cols = st.columns(4)
        directories = []
        dir_options = [
            ("Gelbe Seiten", "gelbeseiten"),
            ("Das Örtliche", "dasoertliche"),
            ("Yelp", "yelp"),
            ("11880", "11880"),
            ("Facebook", "facebook"),
            ("Bing Places", "bing"),
            ("Apple Maps", "apple"),
            ("Meinestadt.de", "meinestadt")
        ]
        for i, (label, value) in enumerate(dir_options):
            with dir_cols[i % 4]:
                if st.checkbox(label, key=f"dir_{value}"):
                    directories.append(value)
        
        nap_consistency = st.selectbox("NAP-Konsistenz (Name, Adresse, Telefon)",
            ["", "perfect", "mostly", "mixed", "inconsistent"],
            format_func=lambda x: {
                "": "Auswählen...",
                "perfect": "100% identisch",
                "mostly": "Meist konsistent",
                "mixed": "Gemischt",
                "inconsistent": "Inkonsistent"
            }.get(x, x),
            key="audit_nap"
        )
        
        st.markdown("#### Social Media")
        social_cols = st.columns(4)
        social_media = []
        social_options = [("Facebook", "facebook"), ("Instagram", "instagram"), ("LinkedIn", "linkedin"), ("TikTok", "tiktok")]
        for i, (label, value) in enumerate(social_options):
            with social_cols[i]:
                if st.checkbox(label, key=f"social_{value}"):
                    social_media.append(value)
        
        social_frequency = st.selectbox("Posting-Frequenz",
            ["", "daily", "weekly", "monthly", "rarely", "never"],
            format_func=lambda x: {
                "": "Auswählen...",
                "daily": "Täglich",
                "weekly": "Wöchentlich",
                "monthly": "Monatlich",
                "rarely": "Selten",
                "never": "Inaktiv"
            }.get(x, x),
            key="audit_social_freq"
        )
    
    with tab3:
        if st.button("🔍 ANALYSE STARTEN", type="primary", use_container_width=True):
            # Daten sammeln
            audit_input = {
                "business_name": business_name,
                "industry": industry,
                "address": address,
                "phone": phone,
                "website": website,
                "google_business": google_business,
                "review_count": review_count,
                "avg_rating": avg_rating,
                "review_response": review_response,
                "gmb_posts": gmb_posts,
                "directories": directories,
                "nap_consistency": nap_consistency,
                "social_media": social_media,
                "social_frequency": social_frequency,
                "competitors": competitors
            }
            
            with st.spinner("Analysiere Ihre Local SEO Präsenz..."):
                import time
                time.sleep(1.5)  # Kurze Animation
                
                # Analyse durchführen
                results = run_local_seo_audit(audit_input)
                
                # Header mit Score
                st.markdown("---")
                st.markdown(f"### 📊 Ergebnis für: {business_name or 'Ihr Unternehmen'}")
                if address:
                    st.markdown(f"📍 {address}")
                st.markdown(f"🕐 Analysiert am {datetime.now().strftime('%d.%m.%Y um %H:%M')}")
                
                # Hauptscore
                score = results["total_score"]
                score_class = get_score_class(score)
                score_label, score_desc = get_score_label(score)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f'''
                        <div style="text-align: center; padding: 30px;">
                            <div class="audit-score-circle {score_class}">{score}</div>
                            <h2 style="color: white; margin-top: 20px;">{score_label}</h2>
                            <p style="color: #b0b0b0;">{score_desc}</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                # Quick Stats
                st.markdown("---")
                stat_cols = st.columns(4)
                with stat_cols[0]:
                    st.markdown(f'<div class="custom-metric animated"><div class="metric-label">Citations</div><div class="metric-value">{len(directories)}</div></div>', unsafe_allow_html=True)
                with stat_cols[1]:
                    st.markdown(f'<div class="custom-metric animated"><div class="metric-label">Bewertungen</div><div class="metric-value">{review_count}</div></div>', unsafe_allow_html=True)
                with stat_cols[2]:
                    rating_display = f"{avg_rating}⭐" if avg_rating > 0 else "-"
                    st.markdown(f'<div class="custom-metric animated"><div class="metric-label">Ø Rating</div><div class="metric-value">{rating_display}</div></div>', unsafe_allow_html=True)
                with stat_cols[3]:
                    critical_count = len(results["findings"]["critical"])
                    metric_class = "error-metric" if critical_count > 0 else "success-metric"
                    st.markdown(f'<div class="custom-metric {metric_class} animated"><div class="metric-label">Kritisch</div><div class="metric-value">{critical_count}</div></div>', unsafe_allow_html=True)
                
                # Kategorie-Scores
                st.markdown("---")
                st.markdown("### 📈 Bewertung nach Kategorien")
                
                categories = [
                    ("Google Profil", results["scores"]["google"], "35%"),
                    ("Bewertungen", results["scores"]["reviews"], "25%"),
                    ("Verzeichnisse", results["scores"]["citations"], "20%"),
                    ("Website", results["scores"]["website"], "12%"),
                    ("Social Media", results["scores"]["social"], "8%")
                ]
                
                for name, cat_score, weight in categories:
                    color = get_bar_color(cat_score)
                    st.markdown(f'''
                        <div style="margin: 15px 0;">
                            <div style="display: flex; justify-content: space-between; color: white; margin-bottom: 5px;">
                                <span>{name}</span>
                                <span style="color: #b0b0b0;">{cat_score}/100 ({weight})</span>
                            </div>
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" style="width: {cat_score}%; background: {color};"></div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                # Detaillierte Findings
                st.markdown("---")
                st.markdown("### 📋 Detaillierte Analyse")
                
                finding_tabs = st.tabs([
                    f"🔴 Kritisch ({len(results['findings']['critical'])})",
                    f"🟡 Wichtig ({len(results['findings']['important'])})",
                    f"🟢 Optimierung ({len(results['findings']['optimize'])})",
                    f"✅ Positiv ({len(results['findings']['positive'])})"
                ])
                
                finding_classes = ["finding-critical", "finding-important", "finding-optimize", "finding-positive"]
                finding_keys = ["critical", "important", "optimize", "positive"]
                
                for i, (tab, css_class, key) in enumerate(zip(finding_tabs, finding_classes, finding_keys)):
                    with tab:
                        if results["findings"][key]:
                            for finding in results["findings"][key]:
                                st.markdown(f'''
                                    <div class="finding-card {css_class}">
                                        <h4 style="color: white; margin: 0 0 10px 0;">{finding["title"]}</h4>
                                        <p style="color: #c0c0c0; margin: 5px 0;">{finding["desc"]}</p>
                                        <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                            <div>
                                                <strong style="color: #9ca3af;">📊 Auswirkung:</strong>
                                                <p style="color: #c0c0c0; margin: 5px 0;">{finding["impact"]}</p>
                                            </div>
                                            <div>
                                                <strong style="color: #9ca3af;">✅ Maßnahme:</strong>
                                                <p style="color: #c0c0c0; margin: 5px 0;">{finding["action"]}</p>
                                            </div>
                                        </div>
                                        <div style="margin-top: 10px;">
                                            <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; font-size: 0.85em; color: #9ca3af;">
                                                Aufwand: {finding.get("effort", "Mittel")}
                                            </span>
                                        </div>
                                    </div>
                                ''', unsafe_allow_html=True)
                        else:
                            st.info("Keine Einträge in dieser Kategorie")
                
                # Maßnahmenplan
                st.markdown("---")
                st.markdown("### 🎯 Ihr Maßnahmenplan (30 Tage)")
                
                all_actions = results["findings"]["critical"] + results["findings"]["important"]
                if all_actions:
                    for i, action in enumerate(all_actions[:5], 1):
                        week = "Woche 1" if i <= 2 else "Woche 2-3" if i <= 4 else "Woche 4"
                        st.markdown(f'''
                            <div class="action-item">
                                <div class="action-number">{i}</div>
                                <div style="flex: 1;">
                                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                                        <strong style="color: white;">{action["title"]}</strong>
                                        <span style="background: rgba(102, 126, 234, 0.3); padding: 2px 10px; border-radius: 10px; font-size: 0.8em; color: #a0a0ff;">{week}</span>
                                    </div>
                                    <p style="color: #b0b0b0; margin: 0;">{action["action"]}</p>
                                    <div style="margin-top: 8px; font-size: 0.85em; color: #808080;">
                                        ⏱ {action.get("effort", "Mittel")} | 📈 {"Sehr hoch" if i <= 2 else "Hoch"}
                                    </div>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.success("🎉 Keine dringenden Maßnahmen erforderlich!")
                
                # Branchenempfehlungen
                if industry and industry in INDUSTRY_DIRECTORIES:
                    st.markdown("---")
                    st.markdown(f"### ⚡ Empfehlungen für {INDUSTRY_LABELS.get(industry, 'Ihre Branche')}")
                    
                    industry_dirs = INDUSTRY_DIRECTORIES.get(industry, [])
                    if industry_dirs:
                        st.markdown(f'''
                            <div class="industry-rec">
                                <h4 style="color: white; margin: 0 0 10px 0;">📋 Empfohlene Branchenverzeichnisse</h4>
                                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                                    {"".join([f'<span style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; padding: 6px 14px; border-radius: 20px; font-size: 0.9em;">{d}</span>' for d in industry_dirs])}
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                
                # Wettbewerber
                if competitors:
                    st.markdown("---")
                    st.markdown("### 👥 Wettbewerbsanalyse")
                    st.markdown(f'''
                        <div class="glass-card">
                            <p style="color: #b0b0b0;">Genannte Wettbewerber: <strong style="color: white;">{competitors}</strong></p>
                            <div style="background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 16px; margin-top: 15px;">
                                <h4 style="color: #a78bfa; margin: 0 0 10px 0;">🔍 Analyse-Tipps</h4>
                                <ul style="color: #c0c0c0; margin: 0; padding-left: 20px;">
                                    <li>Bewertungen vergleichen (Anzahl & Durchschnitt)</li>
                                    <li>Google-Profil-Aktivität prüfen</li>
                                    <li>Verzeichnisse identifizieren</li>
                                    <li>Website-Keywords analysieren</li>
                                </ul>
                            </div>
                            <p style="color: #808080; font-style: italic; margin-top: 15px;">💡 Tipp: Suchen Sie "[Wettbewerber] + [Stadt]" bei Google</p>
                        </div>
                    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("---")
st.markdown('<div style="text-align: center; padding: 30px; color: #ffffff;"><p style="font-size: 1.15em; font-weight: 600;">Made with precision by BrandVector</p><p style="opacity: 0.85; font-size: 1.05em;">Powered by Perplexity AI · DataForSEO · OpenAI</p></div>', unsafe_allow_html=True)
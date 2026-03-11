import streamlit as st


def inject_css():
    """Inject production-grade CSS. Must be called after set_page_config."""
    st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global font — target text elements only, NOT icon spans ── */
p, h1, h2, h3, h4, h5, h6, li, label, input, textarea, select,
button, caption, td, th, blockquote, figcaption,
.stMarkdown, .stText, .stTextInput, .stNumberInput, .stSelectbox,
.stRadio, .stCheckbox, .stSlider, .stButton {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu                    { visibility: hidden !important; }
[data-testid="stToolbar"]   { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
footer                       { visibility: hidden !important; }

/* ── Page background ── */
.stApp {
    background-color: #F1F5F9 !important;
}
[data-testid="stMain"] {
    background-color: #F1F5F9 !important;
}
[data-testid="stMainBlockContainer"] {
    background-color: #F1F5F9 !important;
    padding-top: 1.5rem !important;
}

/* ── Sidebar: dark indigo gradient ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #1E1B4B 0%, #2D2A7A 55%, #312E81 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 20px rgba(30, 27, 75, 0.25) !important;
}
[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* Sidebar: all text white/lavender — cover tag names AND Streamlit generated classes */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #C7D2FE !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(167, 139, 250, 0.3) !important;
    margin: 0.6rem 0 !important;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption p {
    color: #A5B4FC !important;
}

/* Sidebar: number input */
[data-testid="stSidebar"] input {
    background: rgba(99, 102, 241, 0.15) !important;
    border: 1px solid rgba(167, 139, 250, 0.5) !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}

/* Sidebar: ALL buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(99, 102, 241, 0.2) !important;
    border: 1px solid rgba(167, 139, 250, 0.45) !important;
    color: #C7D2FE !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.18s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99, 102, 241, 0.45) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

/* Sidebar: primary Save button */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
    border: none !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.4) !important;
}

/* Sidebar: logout (secondary = red tint) */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: rgba(239, 68, 68, 0.12) !important;
    border: 1px solid rgba(239, 68, 68, 0.4) !important;
    color: #FCA5A5 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(239, 68, 68, 0.28) !important;
    color: #FFFFFF !important;
}

/* Sidebar: expander */
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(99, 102, 241, 0.12) !important;
    border: 1px solid rgba(167, 139, 250, 0.35) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary,
[data-testid="stSidebar"] details > summary {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* ── Primary buttons (main area) ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 10px rgba(79, 70, 229, 0.3) !important;
    transition: all 0.18s ease !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
    box-shadow: 0 4px 16px rgba(79, 70, 229, 0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Expanders (main area) ── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] details > summary {
    font-weight: 700 !important;
    color: #0F172A !important;
    font-size: 0.95rem !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #FFFFFF !important;
    border-radius: 0 0 12px 12px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #E2E8F0 !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #64748B !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.65rem 1.5rem !important;
    border-bottom: 3px solid transparent !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    color: #4F46E5 !important;
    border-bottom: 3px solid #4F46E5 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.25rem !important;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div {
    background: #E2E8F0 !important;
    border-radius: 999px !important;
    height: 8px !important;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #4F46E5, #818CF8) !important;
    border-radius: 999px !important;
}

/* ── Form inputs ── */
input[type="text"],
input[type="password"],
input[type="email"],
input[type="number"],
textarea {
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
input:focus,
textarea:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
    outline: none !important;
}

/* ── st.info / st.success / st.error boxes ── */
[data-testid="stNotification"] {
    border-radius: 10px !important;
    font-size: 0.875rem !important;
}

/* ── Metric pills ── */
.ct-pill {
    background: #FFFFFF;
    border-radius: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07), 0 4px 16px rgba(79,70,229,0.07);
    padding: 1.1rem 0.75rem;
    text-align: center;
    border-top: 4px solid #4F46E5;
}
.ct-pill.green  { border-top-color: #10B981; }
.ct-pill.amber  { border-top-color: #F59E0B; }
.ct-pill.red    { border-top-color: #EF4444; }
.ct-pill .pill-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    margin: 0 0 0.2rem;
}
.ct-pill .pill-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0;
    line-height: 1;
}
.ct-pill .pill-unit {
    font-size: 0.68rem;
    color: #94A3B8;
    margin: 0.15rem 0 0;
}

/* ── Avatar ── */
.ct-avatar {
    width: 46px; height: 46px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 800; color: #FFFFFF;
    margin-bottom: 0.4rem;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
}

/* ── Meal section containers ── */
.meal-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1rem;
    background: #FFFFFF;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    margin-bottom: 0.4rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.meal-header .mh-icon  { font-size: 1.2rem; }
.meal-header .mh-name  { font-weight: 700; color: #0F172A; font-size: 0.95rem; flex: 1; }
.meal-header .mh-badge {
    background: #EEF2FF;
    color: #4F46E5;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    border: 1px solid #C7D2FE;
}

/* ── Food log rows ── */
.food-row {
    background: #F8FAFC;
    border-radius: 8px;
    padding: 0.55rem 0.9rem;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #E2E8F0;
    transition: background 0.15s, border-color 0.15s;
}
.food-row:hover { background: #EEF2FF; border-color: #C7D2FE; }
.food-row .fr-name { font-weight: 600; color: #0F172A; font-size: 0.875rem; }
.food-row .fr-meta { font-size: 0.775rem; color: #94A3B8; margin-left: 0.5rem; }
.food-row .fr-cal  { font-weight: 700; color: #4F46E5; font-size: 0.875rem; white-space: nowrap; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #94A3B8;
}
.empty-state .es-icon  { font-size: 2.5rem; margin-bottom: 0.5rem; }
.empty-state .es-title { font-size: 1rem; font-weight: 600; color: #64748B; margin: 0; }
.empty-state .es-sub   { font-size: 0.82rem; margin: 0.2rem 0 0; }

/* ── Auth page hero ── */
.auth-hero {
    background: linear-gradient(155deg, #1E1B4B 0%, #3730A3 60%, #4338CA 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    min-height: 480px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    color: #FFFFFF;
}
.auth-hero h1 {
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0.5rem 0 0.2rem !important;
    line-height: 1.2 !important;
}
.auth-hero .hero-tagline {
    color: #A5B4FC;
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
    line-height: 1.5;
}
.auth-hero .hero-feature {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #C7D2FE;
    font-size: 0.875rem;
    margin-bottom: 0.55rem;
}
.auth-hero .hero-feature .check {
    color: #34D399;
    font-weight: 800;
    font-size: 1rem;
}
.auth-hero .hero-stat {
    margin-top: 2rem;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #E0E7FF;
    font-size: 0.82rem;
}
.auth-hero .hero-stat strong {
    color: #FFFFFF;
    font-size: 1.4rem;
    font-weight: 800;
    display: block;
    margin-bottom: 0.1rem;
}

/* Auth disclaimer */
.auth-disclaimer {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 8px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 1rem;
    font-size: 0.78rem;
    color: #1D4ED8;
    line-height: 1.55;
}

/* ── Insight line ── */
.insight-msg {
    font-size: 0.875rem;
    color: #64748B;
    text-align: center;
    padding: 0.25rem 0 0.75rem;
    font-style: italic;
}

/* ── Section headings ── */
.section-heading {
    font-size: 1rem;
    font-weight: 700;
    color: #0F172A;
    margin: 1.25rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

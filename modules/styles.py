import streamlit as st

def load_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700&display=swap');

    /* ── Reset & Base ── */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: #0d1117 !important;
        color: #e6edf3 !important;
    }
    [data-testid="stSidebar"] {
        background: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] * { color: #e6edf3 !important; }
    .main .block-container { padding: 1.5rem 2rem 3rem; max-width: 1200px; }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }

    /* ── Main Header ── */
    .main-header {
        background: linear-gradient(135deg, #1a2744 0%, #0d1b3e 50%, #1a1a3e 100%);
        border: 1px solid #2d4a8a;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 32px rgba(59,130,246,0.15);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -10%;
        width: 60%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(59,130,246,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .header-content {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        position: relative;
        z-index: 1;
    }
    .header-icon {
        font-size: 2.8rem;
        filter: drop-shadow(0 0 12px rgba(59,130,246,0.6));
    }
    .main-header h1 {
        font-family: 'Sora', sans-serif;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 !important;
        line-height: 1.2;
        background: linear-gradient(90deg, #fff 60%, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .main-header p {
        color: #94a3b8 !important;
        font-size: 0.9rem;
        margin: 0.25rem 0 0;
    }

    /* ── Navigation Buttons ── */
    [data-testid="stButton"] > button {
        background: #161b22;
        color: #e6edf3 !important;
        border: 1px solid #30363d;
        border-radius: 10px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 0.5rem 0.75rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    [data-testid="stButton"] > button:hover {
        background: #1f2937;
        border-color: #3b82f6;
        color: #60a5fa !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(59,130,246,0.2);
    }
    [data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border-color: #3b82f6;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.7rem 1.5rem;
    }
    [data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        box-shadow: 0 6px 24px rgba(59,130,246,0.4);
        transform: translateY(-2px);
    }

    /* ── Hero Section ── */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(180deg, #0d1117 0%, #0d1b3e 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid #1e3a5f;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 50%;
        transform: translateX(-50%);
        width: 600px; height: 400px;
        background: radial-gradient(ellipse, rgba(59,130,246,0.12) 0%, transparent 70%);
    }
    .hero-section h2 {
        font-family: 'Sora', sans-serif;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 0.75rem !important;
        position: relative;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-section p {
        font-size: 1.1rem;
        color: #94a3b8 !important;
        max-width: 600px;
        margin: 0 auto !important;
        position: relative;
    }

    /* ── Stat Cards ── */
    .stat-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
        cursor: default;
    }
    .stat-card:hover {
        border-color: #3b82f6;
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(59,130,246,0.2);
        background: #1a2332;
    }
    .stat-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .stat-num {
        font-family: 'Sora', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #60a5fa;
    }
    .stat-label { font-size: 0.8rem; color: #8b949e; margin-top: 0.2rem; }

    /* ── Feature Cards ── */
    .feature-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.25s ease;
    }
    .feature-card:hover {
        border-color: #3b82f6;
        transform: translateX(4px);
        box-shadow: -4px 0 20px rgba(59,130,246,0.15);
        background: #1a2332;
    }
    .feature-card h3 {
        color: #e6edf3 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    .feature-card p { color: #8b949e; font-size: 0.88rem; margin: 0; }

    /* ── Section Headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #21262d;
    }
    .section-header-icon {
        font-size: 1.6rem;
        width: 44px; height: 44px;
        background: linear-gradient(135deg, #1e3a5f, #1a2744);
        border: 1px solid #2d4a8a;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
    }
    .section-header h2 {
        font-family: 'Sora', sans-serif;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #e6edf3 !important;
        margin: 0 !important;
    }
    .section-header p { color: #8b949e; font-size: 0.85rem; margin: 0; }

    /* ── Job Cards ── */
    .job-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .job-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #3b82f6, #8b5cf6);
        border-radius: 3px 0 0 3px;
    }
    .job-card:hover {
        border-color: #2d4a8a;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(59,130,246,0.15);
        background: #1a2332;
    }
    .job-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #e6edf3;
        margin-bottom: 0.3rem;
    }
    .job-company { color: #60a5fa; font-size: 0.9rem; font-weight: 500; }
    .job-meta {
        display: flex; flex-wrap: wrap; gap: 0.5rem;
        margin: 0.75rem 0;
    }
    .badge {
        display: inline-flex; align-items: center; gap: 0.3rem;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 500;
    }
    .badge-blue { background: #1e3a5f; color: #60a5fa; border: 1px solid #2d4a8a; }
    .badge-green { background: #0d2d1a; color: #34d399; border: 1px solid #065f46; }
    .badge-purple { background: #2d1b69; color: #a78bfa; border: 1px solid #4c1d95; }
    .badge-orange { background: #3d1f00; color: #fb923c; border: 1px solid #7c2d12; }
    .badge-red { background: #2d1515; color: #f87171; border: 1px solid #7f1d1d; }
    .match-score {
        position: absolute; top: 1rem; right: 1rem;
        background: linear-gradient(135deg, #1e3a5f, #2d1b69);
        border: 1px solid #3b82f6;
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.82rem;
        font-weight: 700;
        color: #60a5fa;
    }
    .match-bar-container {
        background: #21262d;
        border-radius: 4px;
        height: 6px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .match-bar {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        transition: width 0.6s ease;
    }

    /* ── Scheme Cards ── */
    .scheme-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .scheme-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #34d399, #059669);
        border-radius: 3px 0 0 3px;
    }
    .scheme-card:hover {
        border-color: #065f46;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(52,211,153,0.1);
        background: #0d2018;
    }
    .scheme-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #e6edf3;
    }
    .scheme-benefit {
        background: #0d2d1a;
        border: 1px solid #065f46;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        margin: 0.6rem 0;
        font-size: 0.88rem;
        color: #34d399;
    }

    /* ── Emergency Cards ── */
    .emergency-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .emergency-card.critical {
        border-color: #7f1d1d;
    }
    .emergency-card.critical::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #ef4444, #dc2626);
    }
    .emergency-card:not(.critical)::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #f59e0b, #d97706);
    }
    .emergency-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(239,68,68,0.1);
    }
    .phone-badge {
        display: inline-block;
        background: #1a2744;
        border: 1px solid #2d4a8a;
        border-radius: 8px;
        padding: 0.3rem 0.75rem;
        font-size: 0.9rem;
        font-weight: 700;
        color: #60a5fa;
        margin: 0.3rem 0;
    }

    /* ── Forms ── */
    .form-container {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 16px;
        padding: 2rem;
        max-width: 600px;
        margin: 0 auto;
    }
    .form-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #e6edf3;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] select,
    [data-testid="stTextArea"] textarea {
        background: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        color: #e6edf3 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    }
    label {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* ── Admin Dashboard ── */
    .metric-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        transition: all 0.2s;
    }
    .metric-card:hover { border-color: #3b82f6; transform: translateY(-3px); }
    .metric-value {
        font-family: 'Sora', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-label { color: #8b949e; font-size: 0.85rem; margin-top: 0.3rem; }
    .metric-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }

    /* ── Info/Success/Warning boxes ── */
    .info-box {
        background: #1a2744;
        border: 1px solid #2d4a8a;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.75rem 0;
    }
    .success-box {
        background: #0d2d1a;
        border: 1px solid #065f46;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.75rem 0;
        color: #34d399;
    }
    .warning-box {
        background: #2d1f00;
        border: 1px solid #78350f;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.75rem 0;
        color: #fbbf24;
    }

    /* ── Tabs ── */
    [data-testid="stTabs"] [role="tablist"] {
        background: #161b22;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #21262d;
    }
    [data-testid="stTabs"] [role="tab"] {
        background: transparent;
        color: #8b949e !important;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.88rem;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: #1e3a5f !important;
        color: #60a5fa !important;
        border: 1px solid #2d4a8a;
    }

    /* ── Divider ── */
    hr { border-color: #21262d !important; margin: 1.5rem 0 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #484f58; }

    /* ── Streamlit overrides ── */
    [data-testid="stMarkdownContainer"] p { color: #e6edf3; }
    .stAlert { border-radius: 10px; }
    [data-testid="stSelectbox"] > div > div {
        background: #0d1117 !important;
        border-color: #30363d !important;
        color: #e6edf3 !important;
    }
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

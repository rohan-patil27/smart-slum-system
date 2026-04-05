import streamlit as st

st.set_page_config(
    page_title="Smart Slum Resource & Job Matching System",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

from modules.database import init_db
from modules.auth import show_login, show_register
from modules.job_matching import show_job_matching
from modules.schemes import show_schemes
from modules.emergency import show_emergency
from modules.resume import show_resume_generator
from modules.admin import show_admin_dashboard
from modules.tracker import show_tracker
from modules.courses import show_courses
from modules.language import get_text
from modules.styles import load_styles

init_db()
load_styles()

if 'user'     not in st.session_state: st.session_state.user     = None
if 'language' not in st.session_state: st.session_state.language = 'english'
if 'page'     not in st.session_state: st.session_state.page     = 'home'

def t(key):
    return get_text(key, st.session_state.language)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:1rem 0 0.5rem;'>"
        "<div style='font-size:2.5rem;'>🌟</div>"
        "<div style='font-weight:700;color:#e6edf3;font-size:0.95rem;margin-top:0.4rem;'>"
        "Smart Slum System</div></div>",
        unsafe_allow_html=True
    )

    st.markdown("### 🌐 Language")
    lang_idx = 0
    if st.session_state.language == 'hindi':   lang_idx = 1
    elif st.session_state.language == 'marathi': lang_idx = 2
    lang = st.radio("", ["English","Hindi","Marathi"],
                    index=lang_idx, key="lang_radio", label_visibility="collapsed")
    if lang == "Hindi":   st.session_state.language = 'hindi'
    elif lang == "Marathi": st.session_state.language = 'marathi'
    else:                   st.session_state.language = 'english'

    st.markdown("---")

    if st.session_state.user:
        u = st.session_state.user
        gender_icon = "👨" if u.get('gender') == 'Male' else "👩"
        user_role   = "⚙️ Admin" if u.get('is_admin') else "👤 User"
        st.markdown(
            "<div style='background:#1a2332;border:1px solid #2d4a8a;border-radius:10px;"
            "padding:1rem;text-align:center;'>"
            "<div style='font-size:2rem;'>" + gender_icon + "</div>"
            "<div style='font-weight:600;color:#e6edf3;margin-top:0.3rem;'>" + str(u.get('name','')) + "</div>"
            "<div style='color:#8b949e;font-size:0.8rem;'>" + str(u.get('location','')) + "</div>"
            "<div style='margin-top:0.4rem;font-size:0.72rem;color:#60a5fa;'>" + user_role + "</div>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        nav_pages = [
            ("💼 Jobs",           "jobs"),
            ("🏛️ Schemes",        "schemes"),
            ("📊 My Applications","tracker"),
            ("🎓 Free Courses",   "courses"),
            ("📄 Resume",         "resume"),
            ("🆘 Emergency",      "emergency"),
        ]
        if u.get('is_admin'):
            nav_pages.append(("⚙️ Admin", "admin"))
        for label, pg in nav_pages:
            if st.button(label, key="side_"+pg, use_container_width=True):
                st.session_state.page = pg
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True, key="side_logout"):
            st.session_state.user = None
            st.session_state.page = 'home'
            st.rerun()
    else:
        for label, pg in [("🏠 Home","home"),("🔐 Login","login"),
                           ("📝 Register","register"),("🆘 Emergency","emergency")]:
            if st.button(label, key="side_"+pg, use_container_width=True):
                st.session_state.page = pg
                st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='color:#484f58;font-size:0.72rem;text-align:center;'>"
        "Powered by AI · Built for Communities<br>"
        "<span style='color:#3b82f6;'>Maharashtra Social Initiative</span>"
        "</div>",
        unsafe_allow_html=True
    )

# ── Header ────────────────────────────────────────────────────────────────────
_title    = t('app_title')
_subtitle = t('app_subtitle')
st.markdown(
    "<div class='main-header'><div class='header-content'>"
    "<div class='header-icon'>🌟</div>"
    "<div><h1>" + _title + "</h1><p>" + _subtitle + "</p></div>"
    "</div></div>",
    unsafe_allow_html=True
)

# ── Top Nav ────────────────────────────────────────────────────────────────────
if st.session_state.user:
    u = st.session_state.user
    nav_items = [
        ("💼 Jobs","jobs"),("🏛️ Schemes","schemes"),
        ("📊 Tracker","tracker"),("🎓 Courses","courses"),
        ("📄 Resume","resume"),("🆘 Emergency","emergency"),
    ]
    if u.get('is_admin'): nav_items.append(("⚙️ Admin","admin"))
    nav_items.append(("🚪 Logout","logout"))
    cols = st.columns(len(nav_items))
    for col,(label,pg) in zip(cols, nav_items):
        with col:
            if st.button(label, key="topnav_"+pg, use_container_width=True):
                if pg == "logout":
                    st.session_state.user = None
                    st.session_state.page = 'home'
                else:
                    st.session_state.page = pg
                st.rerun()
else:
    cols = st.columns(4)
    for col,(label,pg) in zip(cols,[("🏠 Home","home"),("🔐 Login","login"),
                                     ("📝 Register","register"),("🆘 Emergency","emergency")]):
        with col:
            if st.button(label, key="topnav_"+pg, use_container_width=True):
                st.session_state.page = pg
                st.rerun()

st.markdown("---")

# ── Page Router ───────────────────────────────────────────────────────────────
page = st.session_state.page

if page == 'home':
    hero_title    = t('hero_title')
    hero_subtitle = t('hero_subtitle')
    st.markdown(
        "<div class='hero-section'><h2>" + hero_title + "</h2><p>" + hero_subtitle + "</p></div>",
        unsafe_allow_html=True
    )

    c1,c2,c3,c4 = st.columns(4)
    for col,(icon,num,lbl) in zip([c1,c2,c3,c4],[
        ("💼","500+",t('stat_jobs')),("🏛️","10+",t('stat_schemes')),
        ("🏥","12+",t('stat_ngos')),("👥","1000+",t('stat_users'))]):
        with col:
            st.markdown(
                "<div class='stat-card'><div class='stat-icon'>" + icon + "</div>"
                "<div class='stat-num'>" + num + "</div>"
                "<div class='stat-label'>" + lbl + "</div></div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Features — now 6 cards (2 new ones)
    col_l, col_r = st.columns(2)
    feats_l = [
        ("🎯", t('feat_job_title'),    t('feat_job_desc')),
        ("📊", "Application Tracker", "Apni saari applications ka status track karo — Applied, Interview, Selected"),
        ("📄", t('feat_resume_title'), t('feat_resume_desc')),
    ]
    feats_r = [
        ("🏛️", t('feat_scheme_title'),   t('feat_scheme_desc')),
        ("🎓", "Free Skill Courses",     "PMKVY, Skill India ke 12+ free courses — skill match ke saath"),
        ("🆘", t('feat_emergency_title'), t('feat_emergency_desc')),
    ]
    for col, feats in [(col_l, feats_l),(col_r, feats_r)]:
        with col:
            for icon, title, desc in feats:
                st.markdown(
                    "<div class='feature-card'><h3>" + icon + " " + title + "</h3>"
                    "<p>" + desc + "</p></div>",
                    unsafe_allow_html=True
                )

    # New features highlight
    st.markdown(
        "<div style='background:linear-gradient(135deg,#0d2d1a,#1a2744);border:1px solid #2d4a8a;"
        "border-radius:14px;padding:1.2rem;margin-top:1rem;'>"
        "<div style='font-weight:600;color:#e6edf3;margin-bottom:0.6rem;'>✨ Nayi Features Added</div>"
        "<div style='display:flex;flex-wrap:wrap;gap:0.5rem;'>"
        "<span style='background:#0d2d1a;color:#34d399;border:1px solid #065f46;border-radius:6px;padding:4px 10px;font-size:0.82rem;'>✅ Verified Employer Badge</span>"
        "<span style='background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;border-radius:6px;padding:4px 10px;font-size:0.82rem;'>📊 Application Status Tracker</span>"
        "<span style='background:#2d1b69;color:#a78bfa;border:1px solid #4c1d95;border-radius:6px;padding:4px 10px;font-size:0.82rem;'>⭐ Job Ratings & Reviews</span>"
        "<span style='background:#2d1f00;color:#f59e0b;border:1px solid #78350f;border-radius:6px;padding:4px 10px;font-size:0.82rem;'>🎓 Free Courses Section</span>"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#1a2744;border:1px solid #2d4a8a;border-radius:14px;"
        "padding:1.2rem;margin-top:0.75rem;text-align:center;'>"
        "<div style='font-size:1.3rem;margin-bottom:0.4rem;'>🌐</div>"
        "<div style='color:#e6edf3;font-weight:600;margin-bottom:0.2rem;'>Available in 3 Languages</div>"
        "<div style='color:#8b949e;font-size:0.88rem;'>English · हिंदी · मराठी — Switch from sidebar</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,2,1])
    with c2:
        if st.button("🚀 " + t('get_started'), use_container_width=True, type="primary", key="home_cta"):
            st.session_state.page = 'register'
            st.rerun()

elif page == 'login':    show_login(t)
elif page == 'register': show_register(t)
elif page == 'emergency': show_emergency(t)

elif page == 'jobs':
    if st.session_state.user: show_job_matching(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'schemes':
    if st.session_state.user: show_schemes(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'tracker':
    if st.session_state.user: show_tracker(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'courses':
    if st.session_state.user: show_courses(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'resume':
    if st.session_state.user: show_resume_generator(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'admin':
    if st.session_state.user and st.session_state.user.get('is_admin'):
        show_admin_dashboard(t)
    else:
        st.error("Admin access only.")
        st.session_state.page = 'home'; st.rerun()

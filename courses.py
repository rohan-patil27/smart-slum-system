import streamlit as st
from modules.database import get_conn
import re

CAT_ICONS = {
    "Electrical":"⚡","Electronics":"📱","Textile":"🧵","Construction":"🏗️",
    "IT":"💻","Personal Care":"💄","Food":"🍳","Automotive":"🔧",
    "Security":"🛡️","Digital":"📲","All":"📚"
}

def skill_match(user_skills, course_tags):
    def tok(s):
        return set(x.strip().lower() for x in re.split(r'[,\s]+', s or '') if x.strip())
    u = tok(user_skills)
    c = tok(course_tags)
    if not c: return 0
    return len(u & c) / len(c)

def show_courses(user, t):
    st.markdown(
        "<div class='section-header'>"
        "<div class='section-header-icon'>🎓</div>"
        "<div><h2>Free Skill Courses</h2>"
        "<p>PMKVY, Skill India aur NIELIT ke free courses — apni skill ke hisab se</p></div>"
        "</div>",
        unsafe_allow_html=True
    )

    # Info banner
    st.markdown(
        "<div style='background:#1a2744;border:1px solid #2d4a8a;border-radius:10px;"
        "padding:0.9rem 1.2rem;margin-bottom:1.2rem;display:flex;gap:1rem;align-items:center;'>"
        "<span style='font-size:1.5rem;'>🆓</span>"
        "<div style='color:#94a3b8;font-size:0.88rem;'>"
        "Yeh saare courses <b style='color:#60a5fa;'>bilkul free</b> hain — "
        "government ke PMKVY / Skill India program ke through. "
        "Apply karne ke liye link pe click karo.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM courses WHERE is_free=1 ORDER BY id")
    courses = [dict(r) for r in c.fetchall()]
    conn.close()

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        cats = ["All"] + sorted(set(c['category'] for c in courses))
        sel_cat = st.selectbox("📂 Category", cats, key="course_cat")
    with col2:
        langs = ["All"] + sorted(set(c['language'] for c in courses))
        sel_lang = st.selectbox("🌐 Language", langs, key="course_lang")
    with col3:
        sort_by = st.selectbox("📊 Sort By", ["Best Match (My Skills)","A-Z","Duration"], key="course_sort")

    user_skills = user.get('skills','')

    # Score + filter
    for course in courses:
        course['_score'] = skill_match(user_skills, course.get('skill_tags',''))
    if sel_cat != "All":
        courses = [c for c in courses if c['category'] == sel_cat]
    if sel_lang != "All":
        courses = [c for c in courses if c['language'] == sel_lang]
    if sort_by == "Best Match (My Skills)":
        courses.sort(key=lambda x: x['_score'], reverse=True)
    elif sort_by == "A-Z":
        courses.sort(key=lambda x: x['title'])

    st.markdown(
        "<div style='color:#8b949e;font-size:0.82rem;margin-bottom:1rem;'>"
        "Showing <b style='color:#60a5fa;'>" + str(len(courses)) + "</b> free courses</div>",
        unsafe_allow_html=True
    )

    col_l, col_r = st.columns(2)
    for i, course in enumerate(courses):
        score_pct = int(course['_score'] * 100)
        icon = CAT_ICONS.get(course['category'], "📚")
        match_color = "#34d399" if score_pct >= 60 else "#f59e0b" if score_pct >= 30 else "#8b949e"
        match_bg    = "#0d2d1a" if score_pct >= 60 else "#2d1f00" if score_pct >= 30 else "#21262d"
        match_border= "#065f46" if score_pct >= 60 else "#78350f" if score_pct >= 30 else "#30363d"

        card_html = (
            "<div style='background:#161b22;border:1px solid #21262d;border-radius:14px;"
            "padding:1.2rem;margin-bottom:1rem;border-left:3px solid " + match_color + ";'>"

            "<div style='display:flex;align-items:flex-start;gap:0.75rem;margin-bottom:0.6rem;'>"
            "<span style='font-size:1.6rem;'>" + icon + "</span>"
            "<div style='flex:1;'>"
            "<div style='font-weight:600;color:#e6edf3;font-size:0.95rem;'>" + course['title'] + "</div>"
            "<div style='color:#8b949e;font-size:0.8rem;margin-top:2px;'>"
            "🏛️ " + course['provider'] + "</div>"
            "</div>"
            "</div>"

            "<div style='color:#94a3b8;font-size:0.83rem;margin-bottom:0.7rem;line-height:1.5;'>"
            + course['description'] + "</div>"

            "<div style='display:flex;flex-wrap:wrap;gap:0.4rem;margin-bottom:0.6rem;'>"
            "<span style='background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;"
            "border-radius:5px;padding:2px 7px;font-size:0.75rem;'>🌐 " + course['language'] + "</span>"
            "<span style='background:#2d1b69;color:#a78bfa;border:1px solid #4c1d95;"
            "border-radius:5px;padding:2px 7px;font-size:0.75rem;'>⏱️ " + course['duration'] + "</span>"
            "<span style='background:#0d2d1a;color:#34d399;border:1px solid #065f46;"
            "border-radius:5px;padding:2px 7px;font-size:0.75rem;'>🆓 Free</span>"
            "<span style='background:" + match_bg + ";color:" + match_color + ";border:1px solid " + match_border + ";"
            "border-radius:5px;padding:2px 7px;font-size:0.75rem;'>🎯 " + str(score_pct) + "% skill match</span>"
            "</div>"

            "<div style='color:#8b949e;font-size:0.78rem;'>🔧 Skills: "
            "<span style='color:#60a5fa;'>" + str(course.get('skill_tags','')) + "</span></div>"
            "</div>"
        )

        with (col_l if i % 2 == 0 else col_r):
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button("🔗 Course Apply Karo →", key="course_link_" + str(course['id']),
                         use_container_width=True):
                st.info("🔗 Link: " + str(course.get('link','#')))

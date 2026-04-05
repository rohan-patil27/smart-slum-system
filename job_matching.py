import streamlit as st
from modules.database import get_conn
import re

def skill_match_score(user_skills_str, job_skills_str):
    def normalize(s):
        s = s.lower()
        s = re.sub(r'[^a-z0-9\s,]', '', s)
        tokens = set(x.strip() for x in re.split(r'[,\s]+', s) if x.strip())
        return tokens
    user_sk = normalize(user_skills_str or "")
    job_sk  = normalize(job_skills_str  or "")
    if not job_sk: return 0.0
    return min(len(user_sk & job_sk) / len(job_sk), 1.0)

def get_job_rating(c, job_id):
    c.execute("SELECT AVG(rating), COUNT(*) FROM job_reviews WHERE job_id=?", (job_id,))
    row = c.fetchone()
    avg = round(row[0], 1) if row[0] else 0.0
    cnt = row[1] or 0
    return avg, cnt

def render_stars(rating):
    full  = int(rating)
    empty = 5 - full
    return "★" * full + "☆" * empty

def show_job_matching(user, t):
    st.markdown(
        "<div class='section-header'>"
        "<div class='section-header-icon'>💼</div>"
        "<div><h2>AI Job Matching</h2>"
        "<p>Skills ke hisab se AI score ke saath best jobs</p></div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='info-box' style='display:flex;align-items:center;gap:1rem;flex-wrap:wrap;'>"
        "<span style='font-size:2rem;'>👤</span>"
        "<div>"
        "<div style='font-weight:600;color:#e6edf3;'>" + str(user['name']) + "</div>"
        "<div style='color:#8b949e;font-size:0.85rem;'>"
        "📍 " + str(user.get('location','N/A')) + " &nbsp;|&nbsp; "
        "🎓 " + str(user.get('education','N/A')) + " &nbsp;|&nbsp; "
        "🔧 " + str(user.get('skills','None listed')) + "</div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    with st.expander("🔍 Filter & Search Jobs", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔎 Keyword", placeholder="electrician, driver...", key="job_search")
        with col2:
            districts = ["All Districts","Mumbai","Thane","Pune","Nagpur","Nashik","Aurangabad","Other"]
            sel_dist  = st.selectbox("📍 District", districts, key="job_dist")
        with col3:
            sal_opts  = {"Any":0,"5000+":5000,"8000+":8000,"10000+":10000,"15000+":15000}
            sel_sal   = st.selectbox("Salary", list(sal_opts.keys()), key="job_sal")

        col4, col5 = st.columns(2)
        with col4:
            job_type = st.selectbox("Job Type", ["All","Full-time","Part-time","Contract","Work From Home"], key="job_type")
        with col5:
            sort_by  = st.selectbox("Sort By", ["Best Match (AI)","Salary High to Low","Salary Low to High","Rating"], key="job_sort")

        only_verified = st.checkbox("Show Verified Employers Only", value=False, key="job_verified")

    with st.expander("🎤 Apni Skills Update Karo", expanded=False):
        st.markdown(
            "<div style='background:#1a2332;border:1px solid #2d4a8a;border-radius:8px;"
            "padding:0.75rem;color:#94a3b8;font-size:0.85rem;margin-bottom:0.5rem;'>"
            "Mobile Chrome mein keyboard pe microphone icon dabao aur bol do apni skills</div>",
            unsafe_allow_html=True
        )
        manual_skills = st.text_area("Skills type karo:", placeholder="electrical, driving, stitching...",
                                      key="manual_skills", height=60)
        if st.button("Save Skills", key="save_skills"):
            if manual_skills.strip():
                conn2 = get_conn()
                conn2.execute("UPDATE users SET skills=? WHERE id=?", (manual_skills.strip(), user['id']))
                conn2.commit()
                conn2.close()
                user['skills'] = manual_skills.strip()
                st.success("Skills update ho gayi!")
                st.rerun()

    conn = get_conn()
    c    = conn.cursor()

    query  = "SELECT * FROM jobs WHERE is_active=1"
    params = []
    if sel_dist != "All Districts":
        query += " AND district=?"; params.append(sel_dist)
    if job_type != "All":
        query += " AND job_type=?"; params.append(job_type)
    if only_verified:
        query += " AND is_verified=1"
    if search:
        query += " AND (title LIKE ? OR required_skills LIKE ? OR description LIKE ? OR company LIKE ?)"
        params.extend(["%" + search + "%"] * 4)
    c.execute(query, params)
    jobs = [dict(r) for r in c.fetchall()]

    min_sal = sal_opts[sel_sal]
    if min_sal:
        jobs = [j for j in jobs if j['salary_min'] >= min_sal]

    user_skills = user.get('skills', '')
    for job in jobs:
        job['_score'] = skill_match_score(user_skills, job['required_skills'])
        job['_avg_rating'], job['_rating_count'] = get_job_rating(c, job['id'])

    if sort_by == "Best Match (AI)":
        jobs.sort(key=lambda x: x['_score'], reverse=True)
    elif sort_by == "Salary High to Low":
        jobs.sort(key=lambda x: x['salary_max'], reverse=True)
    elif sort_by == "Salary Low to High":
        jobs.sort(key=lambda x: x['salary_min'])
    elif sort_by == "Rating":
        jobs.sort(key=lambda x: x['_avg_rating'], reverse=True)

    c.execute("SELECT job_id FROM applications WHERE user_id=?", (user['id'],))
    applied_ids = set(r['job_id'] for r in c.fetchall())

    st.markdown(
        "<div style='color:#8b949e;font-size:0.82rem;margin-bottom:1rem;'>"
        "Showing <b style='color:#60a5fa;'>" + str(len(jobs)) + "</b> jobs</div>",
        unsafe_allow_html=True
    )

    if not jobs:
        st.markdown(
            "<div style='text-align:center;padding:3rem;color:#8b949e;'>"
            "<div style='font-size:3rem;margin-bottom:1rem;'>🔍</div>"
            "<div>Koi job nahi mili. Filters hatao.</div></div>",
            unsafe_allow_html=True
        )
        conn.close()
        return

    for job in jobs:
        score_pct  = int(job['_score'] * 100)
        bar_color  = "#34d399" if score_pct >= 70 else "#f59e0b" if score_pct >= 40 else "#6b7280"
        avg_rating = job['_avg_rating']
        rating_cnt = job['_rating_count']
        stars_str  = render_stars(avg_rating)
        applied    = job['id'] in applied_ids

        verified_badge = ""
        if job.get('is_verified'):
            verified_badge = (
                " <span style='background:#0d2d1a;color:#34d399;border:1px solid #065f46;"
                "border-radius:5px;padding:1px 6px;font-size:0.72rem;'>✅ Verified</span>"
            )

        st.markdown(
            "<div class='job-card'>"
            "<div class='match-score'>🤖 " + str(score_pct) + "% match</div>"
            "<div class='job-title'>" + str(job['title']) + "</div>"
            "<div class='job-company'>🏢 " + str(job['company']) + verified_badge + "</div>"
            "<div class='job-meta'>"
            "<span class='badge badge-blue'>📍 " + str(job['location']) + "</span>"
            "<span class='badge badge-green'>💰 ₹" + str(job['salary_min']) + "–₹" + str(job['salary_max']) + "/mo</span>"
            "<span class='badge badge-purple'>🕐 " + str(job['job_type']) + "</span>"
            "<span class='badge badge-orange'>🎓 " + str(job['min_education']) + "</span>"
            "</div>"
            "<div style='color:#94a3b8;font-size:0.85rem;margin:0.4rem 0;'>" + str(job['description']) + "</div>"
            "<div style='color:#8b949e;font-size:0.82rem;'>🔧 <span style='color:#60a5fa;'>" + str(job['required_skills']) + "</span></div>"
            "<div style='display:flex;align-items:center;gap:0.6rem;margin-top:0.4rem;'>"
            "<span style='color:#f59e0b;font-size:0.9rem;'>" + stars_str + "</span>"
            "<span style='color:#8b949e;font-size:0.78rem;'>" +
            (str(avg_rating) + "/5 (" + str(rating_cnt) + " reviews)" if rating_cnt else "No reviews yet") +
            "</span></div>"
            "<div class='match-bar-container' style='margin-top:0.6rem;'>"
            "<div class='match-bar' style='width:" + str(score_pct) + "%;background:" + bar_color + ";'></div>"
            "</div>"
            "<div style='display:flex;justify-content:space-between;font-size:0.78rem;color:#8b949e;margin-top:0.3rem;'>"
            "<span>Match: " + str(score_pct) + "%</span>"
            "<span style='color:#60a5fa;font-weight:600;'>" + str(job['contact']) + "</span>"
            "</div></div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            if applied:
                st.markdown(
                    "<div class='success-box' style='padding:0.4rem 0.8rem;text-align:center;font-size:0.85rem;'>✅ Applied</div>",
                    unsafe_allow_html=True
                )
            else:
                if st.button("Apply Now", key="apply_" + str(job['id']), use_container_width=True):
                    conn.execute("INSERT INTO applications (user_id,job_id) VALUES (?,?)", (user['id'], job['id']))
                    conn.commit()
                    applied_ids.add(job['id'])
                    st.success("Application submit ho gayi!")
                    st.rerun()
        with col2:
            if st.button("Rate & Review", key="rate_" + str(job['id']), use_container_width=True):
                if 'review_job' not in st.session_state or st.session_state['review_job'] != job['id']:
                    st.session_state['review_job'] = job['id']
                else:
                    st.session_state.pop('review_job', None)
                st.rerun()

        if st.session_state.get('review_job') == job['id']:
            st.markdown(
                "<div style='background:#1a2332;border:1px solid #2d4a8a;border-radius:10px;padding:1rem;margin-bottom:0.5rem;'>",
                unsafe_allow_html=True
            )
            c.execute("SELECT * FROM job_reviews WHERE user_id=? AND job_id=?", (user['id'], job['id']))
            existing = c.fetchone()
            existing = dict(existing) if existing else None

            r_rating = st.slider("Rating", 1, 5, int(existing['rating']) if existing else 4,
                                  key="r_slider_" + str(job['id']))
            stars_preview = "★" * r_rating + "☆" * (5 - r_rating)
            st.markdown("<span style='color:#f59e0b;font-size:1.2rem;'>" + stars_preview + "</span>", unsafe_allow_html=True)
            r_text = st.text_area("Review (optional)", value=existing['review'] if existing else '',
                                   placeholder="Company kaisi hai? Salary time pe milti hai?",
                                   height=70, key="r_text_" + str(job['id']))
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("Submit Review", key="sub_rev_" + str(job['id'])):
                    if existing:
                        conn.execute("UPDATE job_reviews SET rating=?,review=? WHERE id=?",
                                     (r_rating, r_text, existing['id']))
                    else:
                        conn.execute("INSERT INTO job_reviews (user_id,job_id,rating,review) VALUES (?,?,?,?)",
                                     (user['id'], job['id'], r_rating, r_text))
                    conn.commit()
                    st.session_state.pop('review_job', None)
                    st.success("Review submit ho gayi!")
                    st.rerun()
            with rc2:
                if st.button("Cancel", key="cancel_" + str(job['id'])):
                    st.session_state.pop('review_job', None)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    conn.close()

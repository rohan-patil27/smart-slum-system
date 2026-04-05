import streamlit as st
from modules.database import get_conn
import pandas as pd
from collections import Counter

DISTRICTS   = ["Mumbai","Thane","Pune","Nagpur","Nashik","Aurangabad","Solapur","Kolhapur","Other"]
EDU_LEVELS  = ["No education","Primary (1-5)","Middle (6-8)","8th Pass","10th Pass","12th Pass","ITI/Diploma","Graduate","Post Graduate"]
JOB_TYPES   = ["Full-time","Part-time","Contract","Work From Home"]
CATEGORIES  = ["Housing","Energy","Health","Skill Development","Finance","Sanitation","Education","Insurance","Social Welfare","Employment"]
EM_TYPES    = ["Government Hospital","Mental Health NGO","Crisis Helpline","Child Welfare NGO",
               "Youth & Skill NGO","Rehabilitation NGO","Homeless NGO","Child Helpline","Women Safety","National Emergency"]

def _metric(icon, val, label):
    st.markdown(
        "<div class='metric-card'>"
        "<div class='metric-icon'>" + icon + "</div>"
        "<div class='metric-value'>" + str(val) + "</div>"
        "<div class='metric-label'>" + label + "</div>"
        "</div>",
        unsafe_allow_html=True
    )

def _section(title):
    st.markdown(
        "<div style='font-weight:600;color:#e6edf3;font-size:1rem;"
        "border-bottom:1px solid #21262d;padding-bottom:0.5rem;margin-bottom:1rem;'>"
        + title + "</div>",
        unsafe_allow_html=True
    )

def show_admin_dashboard(t):
    st.markdown(
        "<div class='section-header'>"
        "<div class='section-header-icon'>⚙️</div>"
        "<div><h2>Admin Dashboard</h2><p>Full management — add, edit, delete everything</p></div>"
        "</div>",
        unsafe_allow_html=True
    )

    conn = get_conn()
    c    = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users WHERE is_admin=0");   total_users  = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM jobs WHERE is_active=1");   total_jobs   = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM applications");             total_apps   = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM schemes");                  total_schemes= c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM emergency_contacts");       total_em     = c.fetchone()[0]

    col1,col2,col3,col4,col5 = st.columns(5)
    for col,(icon,val,lbl) in zip([col1,col2,col3,col4,col5],[
        ("👥",total_users,"Users"),("💼",total_jobs,"Active Jobs"),
        ("📋",total_apps,"Applications"),("🏛️",total_schemes,"Schemes"),("🆘",total_em,"Emergency")]):
        with col: _metric(icon,val,lbl)

    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["💼 Jobs","🏛️ Schemes","🆘 Emergency","👥 Users","📊 Analytics","⚙️ My Settings"])

    # ══════════════════════════════════════════════════════════════════
    # TAB 1 — JOBS
    # ══════════════════════════════════════════════════════════════════
    with tabs[0]:
        sub = st.radio("", ["📋 View & Manage Jobs","➕ Add New Job","✏️ Edit Job","🗑️ Delete Job"],
                       horizontal=True, key="job_sub", label_visibility="collapsed")

        # ── VIEW ──────────────────────────────────────────────────────
        if "View" in sub:
            _section("💼 All Job Listings")
            c.execute("""SELECT j.id,j.title,j.company,j.location,j.district,
                         j.salary_min,j.salary_max,j.job_type,j.min_education,
                         j.required_skills,j.contact,j.is_active,
                         COUNT(a.id) as apps
                         FROM jobs j LEFT JOIN applications a ON j.id=a.job_id
                         GROUP BY j.id ORDER BY j.id DESC""")
            jobs = c.fetchall()
            if jobs:
                df = pd.DataFrame(jobs, columns=["ID","Title","Company","Location","District",
                                                  "Min Sal","Max Sal","Type","Min Edu",
                                                  "Skills","Contact","Active","Applications"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.markdown(
                    "<div class='info-box' style='font-size:0.82rem;'>💡 Edit ya Delete karne ke liye upar wale tabs use karo</div>",
                    unsafe_allow_html=True
                )
            else:
                st.info("Koi job nahi hai abhi.")

        # ── ADD ───────────────────────────────────────────────────────
        elif "Add" in sub:
            _section("➕ Naya Job Add Karo")
            col1,col2 = st.columns(2)
            with col1:
                j_title   = st.text_input("Job Title *", placeholder="Electrician", key="aj_title")
                j_company = st.text_input("Company Name *", placeholder="ABC Solutions", key="aj_company")
                j_loc     = st.text_input("Location / Area", placeholder="Dharavi, Mumbai", key="aj_loc")
                j_dist    = st.selectbox("District", DISTRICTS, key="aj_dist")
                j_skills  = st.text_input("Required Skills (comma separated)", placeholder="electrical,wiring,circuits", key="aj_skills")
                j_contact = st.text_input("Contact Number", placeholder="9999999999", key="aj_contact")
            with col2:
                j_edu     = st.selectbox("Minimum Education", EDU_LEVELS, key="aj_edu")
                j_smin    = st.number_input("Min Salary (₹)", min_value=0, value=8000, step=500, key="aj_smin")
                j_smax    = st.number_input("Max Salary (₹)", min_value=0, value=15000, step=500, key="aj_smax")
                j_type    = st.selectbox("Job Type", JOB_TYPES, key="aj_type")
            j_desc = st.text_area("Job Description *", placeholder="Job ki puri details likhein...", height=100, key="aj_desc")

            if st.button("✅ Job Add Karo", type="primary", key="do_add_job"):
                if j_title and j_company and j_desc:
                    conn.execute("""INSERT INTO jobs (title,company,location,district,required_skills,
                                   min_education,salary_min,salary_max,job_type,description,contact)
                                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                                 (j_title.strip(),j_company.strip(),j_loc.strip(),j_dist,
                                  j_skills.strip(),j_edu,int(j_smin),int(j_smax),j_type,
                                  j_desc.strip(),j_contact.strip()))
                    conn.commit()
                    st.success("✅ Job '" + j_title + "' successfully add ho gayi!")
                    st.rerun()
                else:
                    st.error("❌ Title, Company aur Description required hain.")

        # ── EDIT ──────────────────────────────────────────────────────
        elif "Edit" in sub:
            _section("✏️ Job Edit Karo")
            c.execute("SELECT id,title,company FROM jobs WHERE is_active=1 ORDER BY id DESC")
            job_list = c.fetchall()
            if not job_list:
                st.info("Koi job nahi hai edit karne ke liye.")
            else:
                job_options = {str(j[0]) + " — " + j[1] + " (" + j[2] + ")": j[0] for j in job_list}
                sel = st.selectbox("Job select karo", list(job_options.keys()), key="edit_job_sel")
                job_id = job_options[sel]
                c.execute("SELECT * FROM jobs WHERE id=?", (job_id,))
                job = dict(c.fetchone())

                col1,col2 = st.columns(2)
                with col1:
                    e_title   = st.text_input("Job Title", value=job['title'], key="ej_title")
                    e_company = st.text_input("Company", value=job['company'], key="ej_company")
                    e_loc     = st.text_input("Location", value=job.get('location',''), key="ej_loc")
                    dist_idx  = DISTRICTS.index(job['district']) if job.get('district') in DISTRICTS else 0
                    e_dist    = st.selectbox("District", DISTRICTS, index=dist_idx, key="ej_dist")
                    e_skills  = st.text_input("Required Skills", value=job.get('required_skills',''), key="ej_skills")
                    e_contact = st.text_input("Contact", value=job.get('contact',''), key="ej_contact")
                with col2:
                    edu_idx   = EDU_LEVELS.index(job['min_education']) if job.get('min_education') in EDU_LEVELS else 0
                    e_edu     = st.selectbox("Min Education", EDU_LEVELS, index=edu_idx, key="ej_edu")
                    e_smin    = st.number_input("Min Salary (₹)", value=int(job.get('salary_min',8000)), step=500, key="ej_smin")
                    e_smax    = st.number_input("Max Salary (₹)", value=int(job.get('salary_max',15000)), step=500, key="ej_smax")
                    type_idx  = JOB_TYPES.index(job['job_type']) if job.get('job_type') in JOB_TYPES else 0
                    e_type    = st.selectbox("Job Type", JOB_TYPES, index=type_idx, key="ej_type")
                    e_active  = st.checkbox("Job Active hai?", value=bool(job.get('is_active',1)), key="ej_active")
                e_desc = st.text_area("Description", value=job.get('description',''), height=100, key="ej_desc")

                if st.button("💾 Changes Save Karo", type="primary", key="do_edit_job"):
                    conn.execute("""UPDATE jobs SET title=?,company=?,location=?,district=?,
                                   required_skills=?,min_education=?,salary_min=?,salary_max=?,
                                   job_type=?,description=?,contact=?,is_active=? WHERE id=?""",
                                 (e_title,e_company,e_loc,e_dist,e_skills,e_edu,
                                  int(e_smin),int(e_smax),e_type,e_desc,e_contact,
                                  1 if e_active else 0, job_id))
                    conn.commit()
                    st.success("✅ Job update ho gayi!")
                    st.rerun()

        # ── DELETE ────────────────────────────────────────────────────
        elif "Delete" in sub:
            _section("🗑️ Job Delete Karo")
            c.execute("SELECT id,title,company FROM jobs ORDER BY id DESC")
            job_list = c.fetchall()
            if not job_list:
                st.info("Koi job nahi hai.")
            else:
                job_options = {str(j[0]) + " — " + j[1] + " (" + j[2] + ")": j[0] for j in job_list}
                sel = st.selectbox("Delete karne wali job select karo", list(job_options.keys()), key="del_job_sel")
                job_id = job_options[sel]
                st.markdown(
                    "<div class='warning-box'>⚠️ Yeh action permanent hai — job aur uski applications delete ho jayengi!</div>",
                    unsafe_allow_html=True
                )
                col1,col2 = st.columns([1,4])
                with col1:
                    if st.button("🗑️ Haan, Delete Karo", type="primary", key="do_del_job"):
                        conn.execute("DELETE FROM applications WHERE job_id=?", (job_id,))
                        conn.execute("DELETE FROM jobs WHERE id=?", (job_id,))
                        conn.commit()
                        st.success("✅ Job delete ho gayi!")
                        st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 2 — SCHEMES
    # ══════════════════════════════════════════════════════════════════
    with tabs[1]:
        sub = st.radio("", ["📋 View Schemes","➕ Add Scheme","✏️ Edit Scheme","🗑️ Delete Scheme"],
                       horizontal=True, key="scheme_sub", label_visibility="collapsed")

        if "View" in sub:
            _section("🏛️ All Government Schemes")
            c.execute("SELECT id,name,category,max_income,max_age,gender,caste,benefits FROM schemes ORDER BY id DESC")
            rows = c.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID","Name","Category","Max Income","Max Age","Gender","Caste","Benefits"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("Koi scheme nahi hai.")

        elif "Add" in sub:
            _section("➕ Naya Scheme Add Karo")
            col1,col2 = st.columns(2)
            with col1:
                s_name   = st.text_input("Scheme Name *", placeholder="PM Awaas Yojana", key="as_name")
                s_cat    = st.selectbox("Category", CATEGORIES, key="as_cat")
                s_desc   = st.text_area("Description", placeholder="Scheme ki jankari...", height=80, key="as_desc")
                s_elig   = st.text_input("Eligibility", placeholder="BPL families in urban slums", key="as_elig")
                s_ben    = st.text_area("Benefits", placeholder="₹1.5 Lakh subsidy...", height=60, key="as_ben")
            with col2:
                s_minage = st.number_input("Min Age", value=18, min_value=0, max_value=100, key="as_minage")
                s_maxage = st.number_input("Max Age", value=60, min_value=1, max_value=120, key="as_maxage")
                s_income = st.number_input("Max Income (₹/year)", value=300000, step=10000, key="as_income")
                s_gender = st.selectbox("Gender Eligibility", ["All","Male","Female"], key="as_gender")
                s_caste  = st.selectbox("Caste Eligibility", ["All","SC","ST","OBC","General","Minority","SC,ST,OBC,Minority"], key="as_caste")
                s_link   = st.text_input("Apply Link (URL)", placeholder="https://...", key="as_link")
                s_docs   = st.text_input("Documents Required", placeholder="Aadhaar, BPL card...", key="as_docs")

            if st.button("✅ Scheme Add Karo", type="primary", key="do_add_scheme"):
                if s_name:
                    conn.execute("""INSERT INTO schemes (name,category,description,eligibility,min_age,max_age,
                                   max_income,gender,caste,benefits,apply_link,document_required)
                                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                                 (s_name,s_cat,s_desc,s_elig,int(s_minage),int(s_maxage),
                                  int(s_income),s_gender,s_caste,s_ben,s_link,s_docs))
                    conn.commit()
                    st.success("✅ Scheme add ho gayi!")
                    st.rerun()
                else:
                    st.error("❌ Scheme name required hai.")

        elif "Edit" in sub:
            _section("✏️ Scheme Edit Karo")
            c.execute("SELECT id,name FROM schemes ORDER BY id DESC")
            scheme_list = c.fetchall()
            if not scheme_list:
                st.info("Koi scheme nahi hai.")
            else:
                opts = {str(s[0]) + " — " + s[1]: s[0] for s in scheme_list}
                sel = st.selectbox("Scheme select karo", list(opts.keys()), key="edit_scheme_sel")
                sid = opts[sel]
                c.execute("SELECT * FROM schemes WHERE id=?", (sid,))
                s = dict(c.fetchone())

                col1,col2 = st.columns(2)
                with col1:
                    e_name  = st.text_input("Scheme Name", value=s.get('name',''), key="es_name")
                    cat_idx = CATEGORIES.index(s['category']) if s.get('category') in CATEGORIES else 0
                    e_cat   = st.selectbox("Category", CATEGORIES, index=cat_idx, key="es_cat")
                    e_desc  = st.text_area("Description", value=s.get('description',''), height=80, key="es_desc")
                    e_elig  = st.text_input("Eligibility", value=s.get('eligibility',''), key="es_elig")
                    e_ben   = st.text_area("Benefits", value=s.get('benefits',''), height=60, key="es_ben")
                with col2:
                    e_minage = st.number_input("Min Age", value=int(s.get('min_age',18)), min_value=0, key="es_minage")
                    e_maxage = st.number_input("Max Age", value=int(s.get('max_age',60)), min_value=1, key="es_maxage")
                    e_income = st.number_input("Max Income (₹)", value=int(s.get('max_income',300000)), step=10000, key="es_income")
                    gender_opts = ["All","Male","Female"]
                    g_idx   = gender_opts.index(s['gender']) if s.get('gender') in gender_opts else 0
                    e_gender= st.selectbox("Gender", gender_opts, index=g_idx, key="es_gender")
                    e_caste = st.text_input("Caste", value=s.get('caste','All'), key="es_caste")
                    e_link  = st.text_input("Apply Link", value=s.get('apply_link',''), key="es_link")
                    e_docs  = st.text_input("Documents", value=s.get('document_required',''), key="es_docs")

                if st.button("💾 Scheme Update Karo", type="primary", key="do_edit_scheme"):
                    conn.execute("""UPDATE schemes SET name=?,category=?,description=?,eligibility=?,
                                   min_age=?,max_age=?,max_income=?,gender=?,caste=?,benefits=?,
                                   apply_link=?,document_required=? WHERE id=?""",
                                 (e_name,e_cat,e_desc,e_elig,int(e_minage),int(e_maxage),
                                  int(e_income),e_gender,e_caste,e_ben,e_link,e_docs,sid))
                    conn.commit()
                    st.success("✅ Scheme update ho gayi!")
                    st.rerun()

        elif "Delete" in sub:
            _section("🗑️ Scheme Delete Karo")
            c.execute("SELECT id,name FROM schemes ORDER BY id DESC")
            scheme_list = c.fetchall()
            if not scheme_list:
                st.info("Koi scheme nahi hai.")
            else:
                opts = {str(s[0]) + " — " + s[1]: s[0] for s in scheme_list}
                sel = st.selectbox("Delete karne wali scheme", list(opts.keys()), key="del_scheme_sel")
                sid = opts[sel]
                st.markdown("<div class='warning-box'>⚠️ Yeh scheme permanently delete ho jayegi!</div>", unsafe_allow_html=True)
                col1,_ = st.columns([1,4])
                with col1:
                    if st.button("🗑️ Delete Karo", type="primary", key="do_del_scheme"):
                        conn.execute("DELETE FROM schemes WHERE id=?", (sid,))
                        conn.commit()
                        st.success("✅ Scheme delete ho gayi!")
                        st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 3 — EMERGENCY CONTACTS
    # ══════════════════════════════════════════════════════════════════
    with tabs[2]:
        sub = st.radio("", ["📋 View Contacts","➕ Add Contact","✏️ Edit Contact","🗑️ Delete Contact"],
                       horizontal=True, key="em_sub", label_visibility="collapsed")

        if "View" in sub:
            _section("🆘 All Emergency Contacts")
            c.execute("SELECT id,name,type,district,phone,timing,services FROM emergency_contacts ORDER BY id DESC")
            rows = c.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID","Name","Type","District","Phone","Timing","Services"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("Koi contact nahi hai.")

        elif "Add" in sub:
            _section("➕ Naya Emergency Contact Add Karo")
            col1,col2 = st.columns(2)
            with col1:
                em_name  = st.text_input("Organization Name *", placeholder="KEM Hospital", key="aem_name")
                em_type  = st.selectbox("Type", EM_TYPES, key="aem_type")
                em_loc   = st.text_input("Location / City", placeholder="Parel, Mumbai", key="aem_loc")
                em_dist  = st.selectbox("District", DISTRICTS, key="aem_dist")
            with col2:
                em_phone = st.text_input("Phone Number *", placeholder="022-24136051", key="aem_phone")
                em_addr  = st.text_input("Full Address", placeholder="Parel, Mumbai 400012", key="aem_addr")
                em_time  = st.text_input("Timing", placeholder="24/7 Emergency", key="aem_time")
            em_serv = st.text_area("Services Provided", placeholder="Free emergency, OPD...", height=70, key="aem_serv")

            if st.button("✅ Contact Add Karo", type="primary", key="do_add_em"):
                if em_name and em_phone:
                    conn.execute("""INSERT INTO emergency_contacts (name,type,location,district,phone,address,services,timing)
                                   VALUES (?,?,?,?,?,?,?,?)""",
                                 (em_name,em_type,em_loc,em_dist,em_phone,em_addr,em_serv,em_time))
                    conn.commit()
                    st.success("✅ Contact add ho gaya!")
                    st.rerun()
                else:
                    st.error("❌ Name aur Phone required hain.")

        elif "Edit" in sub:
            _section("✏️ Emergency Contact Edit Karo")
            c.execute("SELECT id,name,phone FROM emergency_contacts ORDER BY id DESC")
            em_list = c.fetchall()
            if not em_list:
                st.info("Koi contact nahi hai.")
            else:
                opts = {str(e[0]) + " — " + e[1] + " (" + e[2] + ")": e[0] for e in em_list}
                sel = st.selectbox("Contact select karo", list(opts.keys()), key="edit_em_sel")
                eid = opts[sel]
                c.execute("SELECT * FROM emergency_contacts WHERE id=?", (eid,))
                em = dict(c.fetchone())

                col1,col2 = st.columns(2)
                with col1:
                    e_name  = st.text_input("Name", value=em.get('name',''), key="eem_name")
                    type_idx= EM_TYPES.index(em['type']) if em.get('type') in EM_TYPES else 0
                    e_type  = st.selectbox("Type", EM_TYPES, index=type_idx, key="eem_type")
                    e_loc   = st.text_input("Location", value=em.get('location',''), key="eem_loc")
                    dist_idx= DISTRICTS.index(em['district']) if em.get('district') in DISTRICTS else 0
                    e_dist  = st.selectbox("District", DISTRICTS, index=dist_idx, key="eem_dist")
                with col2:
                    e_phone = st.text_input("Phone", value=em.get('phone',''), key="eem_phone")
                    e_addr  = st.text_input("Address", value=em.get('address',''), key="eem_addr")
                    e_time  = st.text_input("Timing", value=em.get('timing',''), key="eem_time")
                e_serv = st.text_area("Services", value=em.get('services',''), height=70, key="eem_serv")

                if st.button("💾 Contact Update Karo", type="primary", key="do_edit_em"):
                    conn.execute("""UPDATE emergency_contacts SET name=?,type=?,location=?,district=?,
                                   phone=?,address=?,services=?,timing=? WHERE id=?""",
                                 (e_name,e_type,e_loc,e_dist,e_phone,e_addr,e_serv,e_time,eid))
                    conn.commit()
                    st.success("✅ Contact update ho gaya!")
                    st.rerun()

        elif "Delete" in sub:
            _section("🗑️ Emergency Contact Delete Karo")
            c.execute("SELECT id,name,phone FROM emergency_contacts ORDER BY id DESC")
            em_list = c.fetchall()
            if not em_list:
                st.info("Koi contact nahi hai.")
            else:
                opts = {str(e[0]) + " — " + e[1] + " (" + e[2] + ")": e[0] for e in em_list}
                sel = st.selectbox("Delete karne wala contact", list(opts.keys()), key="del_em_sel")
                eid = opts[sel]
                st.markdown("<div class='warning-box'>⚠️ Yeh contact permanently delete ho jayega!</div>", unsafe_allow_html=True)
                col1,_ = st.columns([1,4])
                with col1:
                    if st.button("🗑️ Delete Karo", type="primary", key="do_del_em"):
                        conn.execute("DELETE FROM emergency_contacts WHERE id=?", (eid,))
                        conn.commit()
                        st.success("✅ Contact delete ho gaya!")
                        st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 4 — USERS
    # ══════════════════════════════════════════════════════════════════
    with tabs[3]:
        sub = st.radio("", ["📋 View Users","✏️ Edit User","🗑️ Delete User"],
                       horizontal=True, key="user_sub", label_visibility="collapsed")

        if "View" in sub:
            _section("👥 All Registered Users")
            c.execute("""SELECT id,name,age,phone,location,district,skills,education,
                         income,gender,caste,created_at FROM users WHERE is_admin=0 ORDER BY id DESC""")
            rows = c.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID","Name","Age","Phone","Location","District",
                                                  "Skills","Education","Income","Gender","Caste","Joined"])
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Applications per user
                st.markdown("#### 📋 Applications per User")
                c.execute("""SELECT u.name, COUNT(a.id) as cnt
                             FROM users u LEFT JOIN applications a ON u.id=a.user_id
                             WHERE u.is_admin=0 GROUP BY u.id ORDER BY cnt DESC""")
                app_data = c.fetchall()
                for row in app_data:
                    st.markdown(
                        "<div style='display:flex;align-items:center;gap:1rem;"
                        "background:#161b22;border:0.5px solid #21262d;border-radius:8px;"
                        "padding:0.5rem 1rem;margin-bottom:0.4rem;'>"
                        "<span style='color:#e6edf3;flex:1;font-size:0.88rem;'>" + str(row[0]) + "</span>"
                        "<span style='background:#0d2d1a;color:#34d399;border:0.5px solid #065f46;"
                        "border-radius:6px;padding:2px 10px;font-size:0.8rem;'>"
                        + str(row[1]) + " applications</span>"
                        "</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("Koi user registered nahi hai.")

        elif "Edit" in sub:
            _section("✏️ User Edit Karo")
            c.execute("SELECT id,name,phone FROM users WHERE is_admin=0 ORDER BY id DESC")
            user_list = c.fetchall()
            if not user_list:
                st.info("Koi user nahi hai.")
            else:
                opts = {str(u[0]) + " — " + u[1] + " (" + u[2] + ")": u[0] for u in user_list}
                sel = st.selectbox("User select karo", list(opts.keys()), key="edit_user_sel")
                uid = opts[sel]
                c.execute("SELECT * FROM users WHERE id=?", (uid,))
                usr = dict(c.fetchone())

                col1,col2 = st.columns(2)
                with col1:
                    eu_name  = st.text_input("Full Name", value=usr.get('name',''), key="eu_name")
                    eu_phone = st.text_input("Phone", value=usr.get('phone',''), key="eu_phone")
                    eu_age   = st.number_input("Age", value=int(usr.get('age',25)), min_value=14, max_value=80, key="eu_age")
                    eu_loc   = st.text_input("Location", value=usr.get('location',''), key="eu_loc")
                    dist_idx = DISTRICTS.index(usr['district']) if usr.get('district') in DISTRICTS else 0
                    eu_dist  = st.selectbox("District", DISTRICTS, index=dist_idx, key="eu_dist")
                with col2:
                    eu_skills= st.text_input("Skills", value=usr.get('skills',''), key="eu_skills")
                    edu_idx  = EDU_LEVELS.index(usr['education']) if usr.get('education') in EDU_LEVELS else 0
                    eu_edu   = st.selectbox("Education", EDU_LEVELS, index=edu_idx, key="eu_edu")
                    eu_income= st.number_input("Income (₹)", value=int(usr.get('income',0)), step=500, key="eu_income")
                    gender_opts = ["Male","Female","Other"]
                    g_idx    = gender_opts.index(usr['gender']) if usr.get('gender') in gender_opts else 0
                    eu_gender= st.selectbox("Gender", gender_opts, index=g_idx, key="eu_gender")
                    caste_opts = ["General","OBC","SC","ST","NT","Minority","Other"]
                    caste_idx= caste_opts.index(usr['caste']) if usr.get('caste') in caste_opts else 0
                    eu_caste = st.selectbox("Category", caste_opts, index=caste_idx, key="eu_caste")

                if st.button("💾 User Update Karo", type="primary", key="do_edit_user"):
                    conn.execute("""UPDATE users SET name=?,phone=?,age=?,location=?,district=?,
                                   skills=?,education=?,income=?,gender=?,caste=? WHERE id=?""",
                                 (eu_name,eu_phone,int(eu_age),eu_loc,eu_dist,
                                  eu_skills,eu_edu,int(eu_income),eu_gender,eu_caste,uid))
                    conn.commit()
                    st.success("✅ User update ho gaya!")
                    st.rerun()

        elif "Delete" in sub:
            _section("🗑️ User Delete Karo")
            c.execute("SELECT id,name,phone FROM users WHERE is_admin=0 ORDER BY id DESC")
            user_list = c.fetchall()
            if not user_list:
                st.info("Koi user nahi hai.")
            else:
                opts = {str(u[0]) + " — " + u[1] + " (" + u[2] + ")": u[0] for u in user_list}
                sel = st.selectbox("Delete karne wala user", list(opts.keys()), key="del_user_sel")
                uid = opts[sel]
                st.markdown("<div class='warning-box'>⚠️ User aur uski saari applications delete ho jayengi!</div>", unsafe_allow_html=True)
                col1,_ = st.columns([1,4])
                with col1:
                    if st.button("🗑️ Delete Karo", type="primary", key="do_del_user"):
                        conn.execute("DELETE FROM applications WHERE user_id=?", (uid,))
                        conn.execute("DELETE FROM users WHERE id=?", (uid,))
                        conn.commit()
                        st.success("✅ User delete ho gaya!")
                        st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 5 — ANALYTICS
    # ══════════════════════════════════════════════════════════════════
    with tabs[4]:
        _section("📊 Platform Analytics")
        col_a,col_b = st.columns(2)

        with col_a:
            st.markdown("#### 🔧 Top Skills")
            c.execute("SELECT skills FROM users WHERE is_admin=0 AND skills IS NOT NULL AND skills!=''")
            skill_counter = Counter()
            for row in c.fetchall():
                for sk in str(row[0]).split(','):
                    sk = sk.strip().lower()
                    if sk: skill_counter[sk] += 1
            top_skills = skill_counter.most_common(8)
            for skill, count in top_skills:
                pct = int((count / top_skills[0][1]) * 100) if top_skills else 0
                st.markdown(
                    "<div style='margin-bottom:0.6rem;'>"
                    "<div style='display:flex;justify-content:space-between;color:#e6edf3;"
                    "font-size:0.85rem;margin-bottom:3px;'>"
                    "<span>" + skill.title() + "</span>"
                    "<span style='color:#60a5fa;'>" + str(count) + " users</span></div>"
                    "<div style='background:#21262d;border-radius:4px;height:7px;'>"
                    "<div style='width:" + str(pct) + "%;height:100%;border-radius:4px;"
                    "background:#3b82f6;'></div></div></div>",
                    unsafe_allow_html=True
                )

        with col_b:
            st.markdown("#### 📍 Users by District")
            c.execute("SELECT district,COUNT(*) FROM users WHERE is_admin=0 GROUP BY district ORDER BY COUNT(*) DESC")
            dist_data = c.fetchall()
            total = sum(r[1] for r in dist_data) or 1
            colors = ["#34d399","#60a5fa","#f59e0b","#f472b6","#a78bfa","#fb923c"]
            for idx,(dist,cnt) in enumerate(dist_data):
                pct = int((cnt/total)*100)
                col = colors[idx % len(colors)]
                st.markdown(
                    "<div style='margin-bottom:0.5rem;display:flex;align-items:center;gap:0.75rem;'>"
                    "<span style='color:" + col + ";width:100px;font-size:0.83rem;'>" + str(dist or 'Other') + "</span>"
                    "<div style='flex:1;background:#21262d;border-radius:4px;height:8px;'>"
                    "<div style='width:" + str(pct) + "%;height:100%;background:" + col + ";border-radius:4px;'></div></div>"
                    "<span style='color:#8b949e;font-size:0.8rem;width:60px;text-align:right;'>" + str(cnt) + " (" + str(pct) + "%)</span>"
                    "</div>",
                    unsafe_allow_html=True
                )

        col_c,col_d = st.columns(2)
        with col_c:
            st.markdown("#### 🏆 Most Applied Jobs")
            c.execute("""SELECT j.title,j.company,COUNT(a.id) as cnt
                         FROM applications a JOIN jobs j ON a.job_id=j.id
                         GROUP BY a.job_id ORDER BY cnt DESC LIMIT 6""")
            for rank,row in enumerate(c.fetchall(),1):
                st.markdown(
                    "<div style='display:flex;align-items:center;gap:0.75rem;"
                    "background:#161b22;border:0.5px solid #21262d;border-radius:8px;"
                    "padding:0.5rem 0.8rem;margin-bottom:0.4rem;'>"
                    "<span style='color:#60a5fa;font-weight:600;font-size:1rem;'>#" + str(rank) + "</span>"
                    "<div style='flex:1;'>"
                    "<div style='color:#e6edf3;font-size:0.85rem;'>" + str(row[0]) + "</div>"
                    "<div style='color:#8b949e;font-size:0.78rem;'>" + str(row[1]) + "</div>"
                    "</div>"
                    "<span style='background:#0d2d1a;color:#34d399;border:0.5px solid #065f46;"
                    "border-radius:5px;padding:2px 8px;font-size:0.78rem;'>" + str(row[2]) + " apps</span>"
                    "</div>",
                    unsafe_allow_html=True
                )

        with col_d:
            st.markdown("#### 🏷️ Category Distribution")
            c.execute("SELECT caste,COUNT(*) FROM users WHERE is_admin=0 GROUP BY caste ORDER BY COUNT(*) DESC")
            caste_data = c.fetchall()
            total_c = sum(r[1] for r in caste_data) or 1
            for idx,(cat,cnt) in enumerate(caste_data):
                pct = int((cnt/total_c)*100)
                col = colors[idx % len(colors)]
                st.markdown(
                    "<div style='display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;'>"
                    "<span style='color:" + col + ";width:80px;font-size:0.83rem;font-weight:500;'>" + str(cat) + "</span>"
                    "<div style='flex:1;background:#21262d;border-radius:4px;height:8px;'>"
                    "<div style='width:" + str(pct) + "%;height:100%;background:" + col + ";border-radius:4px;'></div></div>"
                    "<span style='color:#8b949e;font-size:0.8rem;'>" + str(cnt) + "</span>"
                    "</div>",
                    unsafe_allow_html=True
                )


    # ══════════════════════════════════════════════════════════════════
    # TAB 6 — ADMIN SETTINGS
    # ══════════════════════════════════════════════════════════════════
    with tabs[5]:
        _section("⚙️ Admin Account Settings")

        admin_id = st.session_state.user['id']
        c.execute("SELECT name, phone, password FROM users WHERE id=?", (admin_id,))
        admin = dict(c.fetchone())

        # Current info display
        st.markdown(
            "<div style='background:#1a2332;border:1px solid #2d4a8a;border-radius:12px;"
            "padding:1.2rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:1rem;'>"
            "<div style='font-size:2.5rem;'>👨‍💼</div>"
            "<div>"
            "<div style='font-weight:600;color:#e6edf3;font-size:1rem;'>" + str(admin['name']) + "</div>"
            "<div style='color:#60a5fa;font-size:0.88rem;margin-top:2px;'>📱 " + str(admin['phone']) + "</div>"
            "<div style='color:#34d399;font-size:0.78rem;margin-top:4px;'>⚙️ Administrator Account</div>"
            "</div></div>",
            unsafe_allow_html=True
        )

        col_left, col_right = st.columns(2)

        # ── Change Phone Number ─────────────────────────────────────
        with col_left:
            st.markdown(
                "<div style='background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.2rem;'>",
                unsafe_allow_html=True
            )
            _section("📱 Phone Number Change Karo")
            new_phone = st.text_input(
                "Naya Phone Number",
                placeholder="10-digit number",
                max_chars=10,
                key="admin_new_phone"
            )
            confirm_pass_phone = st.text_input(
                "Current Password (confirm)",
                type="password",
                placeholder="Confirm karo apna password",
                key="admin_confirm_pass_phone"
            )
            if st.button("💾 Phone Update Karo", type="primary", key="update_phone", use_container_width=True):
                if not new_phone or not confirm_pass_phone:
                    st.error("❌ Dono fields fill karo.")
                elif len(new_phone) != 10 or not new_phone.isdigit():
                    st.error("❌ Valid 10-digit number daalo.")
                elif confirm_pass_phone != admin['password']:
                    st.error("❌ Password galat hai.")
                else:
                    # Check if phone already exists
                    c.execute("SELECT id FROM users WHERE phone=? AND id!=?", (new_phone, admin_id))
                    if c.fetchone():
                        st.error("❌ Yeh number already registered hai.")
                    else:
                        conn.execute("UPDATE users SET phone=? WHERE id=?", (new_phone, admin_id))
                        conn.commit()
                        st.session_state.user['phone'] = new_phone
                        st.success("✅ Phone number update ho gaya! Naya number: " + new_phone)
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Change Password ─────────────────────────────────────────
        with col_right:
            st.markdown(
                "<div style='background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.2rem;'>",
                unsafe_allow_html=True
            )
            _section("🔒 Password Change Karo")
            current_pass = st.text_input(
                "Current Password",
                type="password",
                placeholder="Purana password",
                key="admin_curr_pass"
            )
            new_pass = st.text_input(
                "Naya Password",
                type="password",
                placeholder="Naya password (min 6 characters)",
                key="admin_new_pass"
            )
            confirm_new_pass = st.text_input(
                "Naya Password Confirm",
                type="password",
                placeholder="Naya password dobara likho",
                key="admin_confirm_pass"
            )
            if st.button("🔒 Password Update Karo", type="primary", key="update_pass", use_container_width=True):
                if not current_pass or not new_pass or not confirm_new_pass:
                    st.error("❌ Saare fields fill karo.")
                elif current_pass != admin['password']:
                    st.error("❌ Current password galat hai.")
                elif len(new_pass) < 6:
                    st.error("❌ Password kam se kam 6 characters ka hona chahiye.")
                elif new_pass != confirm_new_pass:
                    st.error("❌ Naya password match nahi kar raha.")
                elif new_pass == current_pass:
                    st.error("❌ Naya password purane se alag hona chahiye.")
                else:
                    conn.execute("UPDATE users SET password=? WHERE id=?", (new_pass, admin_id))
                    conn.commit()
                    st.success("✅ Password successfully change ho gaya!")
                    st.info("💡 Agli baar naye password se login karo.")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Change Display Name ─────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.2rem;'>",
            unsafe_allow_html=True
        )
        _section("👤 Display Name Change Karo")
        col_n1, col_n2 = st.columns([2, 1])
        with col_n1:
            new_name = st.text_input(
                "Naya Naam",
                value=admin['name'],
                placeholder="Admin ka naam",
                key="admin_new_name"
            )
        with col_n2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Naam Update Karo", type="primary", key="update_name", use_container_width=True):
                if not new_name.strip():
                    st.error("❌ Naam empty nahi ho sakta.")
                else:
                    conn.execute("UPDATE users SET name=? WHERE id=?", (new_name.strip(), admin_id))
                    conn.commit()
                    st.session_state.user['name'] = new_name.strip()
                    st.success("✅ Naam update ho gaya: " + new_name.strip())
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Security Tips ───────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='background:#2d1b00;border:1px solid #78350f;border-radius:10px;padding:1rem;'>"
            "<div style='color:#fbbf24;font-weight:600;margin-bottom:0.5rem;'>🛡️ Security Tips</div>"
            "<div style='color:#fde68a;font-size:0.85rem;line-height:1.8;'>"
            "• Password strong rakho — numbers + letters mix karo<br>"
            "• Kabhi apna password kisi aur ko mat batao<br>"
            "• Logout karna mat bhoolo — shared computer pe<br>"
            "• Phone number sahi rakho — recovery ke liye zaroori hai"
            "</div></div>",
            unsafe_allow_html=True
        )

    conn.close()

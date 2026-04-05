import streamlit as st
from modules.database import get_conn

EDUCATION_LEVELS = ["No education", "Primary (1-5)", "Middle (6-8)", "8th Pass", "10th Pass", "12th Pass", "ITI/Diploma", "Graduate", "Post Graduate"]
DISTRICTS = ["Mumbai", "Thane", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Kolhapur", "Ahmednagar", "Satara", "Other"]
GENDERS = ["Male", "Female", "Other"]
CASTES = ["General", "OBC", "SC", "ST", "NT", "Minority", "Other"]

def show_login(t):
    st.markdown("""
    <div style="max-width:480px;margin:0 auto;">
    <div class="form-container">
    <div class="form-title">🔐 Login to Your Account</div>
    </div></div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        with st.container():
            st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:16px;padding:2rem;">""", unsafe_allow_html=True)

            phone = st.text_input("📱 Mobile Number", placeholder="Enter 10-digit number", key="login_phone")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_pass")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Login", use_container_width=True, type="primary", key="do_login"):
                if phone and password:
                    conn = get_conn()
                    c = conn.cursor()
                    c.execute("SELECT * FROM users WHERE phone=? AND password=?", (phone.strip(), password.strip()))
                    user = c.fetchone()
                    conn.close()
                    if user:
                        st.session_state.user = dict(user)
                        st.session_state.page = 'jobs'
                        st.success(f"✅ Welcome back, **{user['name']}**!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid mobile number or password.")
                else:
                    st.warning("⚠️ Please enter both fields.")

            st.markdown("<div style='text-align:center;color:#8b949e;font-size:0.85rem;margin-top:1rem;'>Don't have account? Click Register above</div>", unsafe_allow_html=True)
            st.markdown("""<div style='background:#1a2744;border:1px solid #2d4a8a;border-radius:8px;padding:0.75rem;margin-top:0.75rem;font-size:0.82rem;color:#94a3b8;'>
            <b style='color:#60a5fa;'>Demo Admin:</b> 9999999999 / admin123<br>
            <b style='color:#60a5fa;'>Demo User:</b> 9876543210 / pass123
            </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def show_register(t):
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:16px;padding:2rem;">
        <div style="font-family:'Sora',sans-serif;font-size:1.4rem;font-weight:700;color:#e6edf3;margin-bottom:1.5rem;text-align:center;">
        📝 Create Your Free Account</div>""", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("👤 Full Name *", placeholder="Ram Kumar", key="reg_name")
            phone = st.text_input("📱 Mobile Number *", placeholder="9876543210", key="reg_phone")
            age = st.number_input("🎂 Age", min_value=14, max_value=80, value=25, key="reg_age")
            location = st.text_input("📍 Area / Locality", placeholder="Dharavi, Mumbai", key="reg_location")
            district = st.selectbox("🗺️ District", DISTRICTS, key="reg_district")

        with col_b:
            gender = st.selectbox("⚥ Gender", GENDERS, key="reg_gender")
            caste = st.selectbox("🏷️ Category", CASTES, key="reg_caste")
            education = st.selectbox("🎓 Education Level", EDUCATION_LEVELS, key="reg_edu")
            skills = st.text_input("🔧 Skills", placeholder="electrical, driving, stitching", key="reg_skills")
            income = st.number_input("💰 Monthly Income (₹)", min_value=0, max_value=500000, value=0, step=500, key="reg_income")

        password = st.text_input("🔒 Password *", type="password", placeholder="Create a password", key="reg_pass")
        confirm = st.text_input("🔒 Confirm Password *", type="password", placeholder="Repeat password", key="reg_confirm")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Create Account", use_container_width=True, type="primary", key="do_register"):
            if not name or not phone or not password:
                st.error("❌ Name, Mobile Number and Password are required.")
            elif password != confirm:
                st.error("❌ Passwords do not match.")
            elif len(phone) != 10 or not phone.isdigit():
                st.error("❌ Enter a valid 10-digit mobile number.")
            else:
                try:
                    conn = get_conn()
                    c = conn.cursor()
                    c.execute("""INSERT INTO users (name,age,phone,password,location,district,skills,education,income,gender,caste)
                                 VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                              (name.strip(), int(age), phone.strip(), password.strip(),
                               location.strip(), district, skills.strip(), education,
                               int(income), gender, caste))
                    conn.commit()
                    uid = c.lastrowid
                    c.execute("SELECT * FROM users WHERE id=?", (uid,))
                    user = c.fetchone()
                    conn.close()
                    st.session_state.user = dict(user)
                    st.session_state.page = 'jobs'
                    st.success(f"🎉 Welcome, **{name}**! Account created successfully.")
                    st.rerun()
                except Exception as e:
                    if "UNIQUE" in str(e):
                        st.error("❌ This mobile number is already registered.")
                    else:
                        st.error(f"Error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

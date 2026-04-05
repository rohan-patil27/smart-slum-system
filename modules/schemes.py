import streamlit as st
from modules.database import get_conn

CATEGORY_ICONS = {
    "Housing": "🏠", "Energy": "⚡", "Health": "🏥",
    "Skill Development": "🎓", "Finance": "💰", "Sanitation": "🚿",
    "Education": "📚", "Insurance": "🛡️", "Social Welfare": "❤️",
    "Employment": "💼"
}

def check_eligibility(user, scheme):
    """Returns (is_eligible, reasons)"""
    reasons = []
    eligible = True

    age = int(user.get('age', 0))
    income = int(user.get('income', 0))
    gender = user.get('gender', 'Male')
    caste = user.get('caste', 'General')

    if age < int(scheme['min_age'] or 0):
        eligible = False
        reasons.append(f"Age must be at least {scheme['min_age']}")
    if age > int(scheme['max_age'] or 100):
        eligible = False
        reasons.append(f"Age must be at most {scheme['max_age']}")
    if income > int(scheme['max_income'] or 9999999):
        eligible = False
        reasons.append(f"Income must be below ₹{scheme['max_income']:,}")
    if scheme['gender'] != 'All' and scheme['gender'] != gender:
        eligible = False
        reasons.append(f"Only for {scheme['gender']}")
    if scheme['caste'] != 'All':
        eligible_castes = [c.strip() for c in scheme['caste'].split(',')]
        if caste not in eligible_castes:
            eligible = False
            reasons.append(f"Only for: {scheme['caste']}")

    return eligible, reasons

def show_schemes(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">🏛️</div>
        <div>
            <h2>Government Scheme Finder</h2>
            <p>Schemes you are eligible for based on your profile</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # User profile summary
    st.markdown(f"""
    <div class="info-box" style="display:flex;gap:1.5rem;flex-wrap:wrap;">
        <div>👤 <b style="color:#e6edf3;">{user['name']}</b></div>
        <div>🎂 <span style="color:#94a3b8;">Age:</span> <b style="color:#60a5fa;">{user.get('age','?')}</b></div>
        <div>💰 <span style="color:#94a3b8;">Income:</span> <b style="color:#60a5fa;">₹{int(user.get('income',0)):,}/mo</b></div>
        <div>⚥ <span style="color:#94a3b8;">Gender:</span> <b style="color:#60a5fa;">{user.get('gender','?')}</b></div>
        <div>🏷️ <span style="color:#94a3b8;">Category:</span> <b style="color:#60a5fa;">{user.get('caste','?')}</b></div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        show_eligible_only = st.checkbox("✅ Show only eligible schemes", value=True, key="elig_only")
    with col2:
        categories = ["All"] + list(CATEGORY_ICONS.keys())
        sel_cat = st.selectbox("📂 Category", categories, key="scheme_cat")

    conn = get_conn()
    c = conn.cursor()
    query = "SELECT * FROM schemes"
    params = []
    if sel_cat != "All":
        query += " WHERE category=?"
        params.append(sel_cat)
    c.execute(query, params)
    schemes = [dict(r) for r in c.fetchall()]
    conn.close()

    eligible_count = 0
    shown = 0

    for scheme in schemes:
        is_eligible, reasons = check_eligibility(user, scheme)
        if show_eligible_only and not is_eligible:
            continue

        shown += 1
        if is_eligible:
            eligible_count += 1

        icon = CATEGORY_ICONS.get(scheme['category'], "📋")
        status_html = '<span style="color:#34d399;font-weight:600;">✅ You are eligible</span>' if is_eligible else f'<span style="color:#f87171;font-weight:600;">❌ Not eligible: {", ".join(reasons)}</span>'
        card_extra = "" if is_eligible else 'style="opacity:0.65;"'

        st.markdown(f"""
        <div class="scheme-card" {card_extra}>
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.6rem;">
                <span style="font-size:1.5rem;">{icon}</span>
                <div>
                    <div class="scheme-title">{scheme['name']}</div>
                    <span class="badge badge-purple" style="font-size:0.75rem;">{scheme['category']}</span>
                </div>
            </div>
            <div style="color:#94a3b8;font-size:0.88rem;margin-bottom:0.6rem;">{scheme['description']}</div>
            <div class="scheme-benefit">🎁 {scheme['benefits']}</div>
            <div style="color:#8b949e;font-size:0.82rem;margin-bottom:0.4rem;">
                📋 <b>Eligibility:</b> {scheme['eligibility']}
            </div>
            <div style="font-size:0.85rem;margin:0.4rem 0;">{status_html}</div>
            <div style="color:#8b949e;font-size:0.8rem;">
                📄 <b>Documents needed:</b> {scheme.get('document_required','N/A')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_eligible:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button(f"🔗 Apply Online", key=f"scheme_{scheme['id']}", use_container_width=True):
                    st.markdown(f"<script>window.open('{scheme['apply_link']}','_blank')</script>", unsafe_allow_html=True)
                    st.info(f"🔗 Visit: {scheme['apply_link']}")

    st.markdown(f"""
    <div style="margin-top:1.5rem;padding:1rem;background:#161b22;border-radius:10px;border:1px solid #21262d;text-align:center;">
        <span style="color:#34d399;font-weight:700;font-size:1.1rem;">{eligible_count}</span>
        <span style="color:#94a3b8;"> schemes found eligible out of </span>
        <span style="color:#60a5fa;font-weight:700;">{shown}</span>
        <span style="color:#94a3b8;"> shown</span>
    </div>
    """, unsafe_allow_html=True)

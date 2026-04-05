import streamlit as st
from modules.database import get_conn

TYPE_ICONS = {
    "Mental Health NGO": "🧠", "Crisis Helpline": "📞", "Child Welfare NGO": "👶",
    "Youth & Skill NGO": "🎓", "Government Hospital": "🏥", "Child Helpline": "👦",
    "Women Safety": "👩", "National Emergency": "🚨", "Rehabilitation NGO": "❤️",
    "Homeless NGO": "🏠"
}
CRITICAL_PHONES = {"1098", "181", "112"}

def show_emergency(t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">🆘</div>
        <div>
            <h2>Emergency Help & Support</h2>
            <p>Nearby NGOs, hospitals, helplines — available 24/7</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Critical helplines first
    st.markdown("""
    <div style="background:linear-gradient(135deg,#2d0a0a,#1a0505);border:1px solid #7f1d1d;border-radius:14px;padding:1.5rem;margin-bottom:1.5rem;">
        <div style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;color:#f87171;margin-bottom:1rem;">🚨 National Emergency Numbers — Call Free, 24/7</div>
        <div style="display:flex;flex-wrap:wrap;gap:1rem;">
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#f87171;">112</div>
                <div style="color:#fca5a5;font-size:0.82rem;">Police • Fire • Ambulance</div>
            </div>
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#fbbf24;">1098</div>
                <div style="color:#fde68a;font-size:0.82rem;">Childline — Child Help</div>
            </div>
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#a78bfa;">181</div>
                <div style="color:#c4b5fd;font-size:0.82rem;">Women Helpline</div>
            </div>
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#34d399;">108</div>
                <div style="color:#6ee7b7;font-size:0.82rem;">Free Ambulance</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.selectbox("📂 Type", ["All Types", "Government Hospital", "Mental Health NGO",
                                                "Crisis Helpline", "Child Welfare NGO", "Youth & Skill NGO",
                                                "Rehabilitation NGO", "Homeless NGO"], key="em_type")
    with col2:
        districts = ["All Districts", "Mumbai", "Thane", "Pune", "Nagpur", "Nashik", "Aurangabad"]
        dist_filter = st.selectbox("📍 District", districts, key="em_dist")

    conn = get_conn()
    c = conn.cursor()
    query = "SELECT * FROM emergency_contacts WHERE type NOT IN ('Child Helpline','Women Safety','National Emergency')"
    params = []
    if type_filter != "All Types":
        query += " AND type=?"
        params.append(type_filter)
    if dist_filter != "All Districts":
        query += " AND (district=? OR district='All')"
        params.append(dist_filter)
    c.execute(query, params)
    contacts = [dict(r) for r in c.fetchall()]
    conn.close()

    st.markdown(f"<div style='color:#8b949e;font-size:0.85rem;margin-bottom:1rem;'>Showing <b style='color:#60a5fa;'>{len(contacts)}</b> contacts</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, contact in enumerate(contacts):
        icon = TYPE_ICONS.get(contact['type'], "📋")
        is_critical = contact.get('phone','') in CRITICAL_PHONES
        card_class = "emergency-card critical" if is_critical else "emergency-card"

        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display:flex;align-items:flex-start;gap:0.75rem;">
                    <span style="font-size:1.8rem;">{icon}</span>
                    <div style="flex:1;">
                        <div style="font-family:'Sora',sans-serif;font-weight:600;color:#e6edf3;font-size:0.95rem;">{contact['name']}</div>
                        <span class="badge badge-purple" style="font-size:0.72rem;margin:0.3rem 0;">{contact['type']}</span>
                        <div><span class="phone-badge">📞 {contact['phone']}</span></div>
                        <div style="color:#8b949e;font-size:0.8rem;margin-top:0.4rem;">📍 {contact['address']}</div>
                        <div style="color:#94a3b8;font-size:0.8rem;margin-top:0.3rem;">🕐 {contact['timing']}</div>
                        <div style="color:#8b949e;font-size:0.8rem;margin-top:0.3rem;padding-top:0.3rem;border-top:1px solid #21262d;">
                            {contact['services']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Safety tips
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("💡 Safety Tips & Rights", expanded=False):
        st.markdown("""
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.8;">
        <b style="color:#60a5fa;">Your Rights:</b><br>
        ✅ Right to free emergency medical treatment at any government hospital<br>
        ✅ Right to file FIR at any police station (cannot be refused)<br>
        ✅ Right to free legal aid (call 15100 for National Legal Services)<br>
        ✅ Childline 1098 is free from any phone, 24/7<br><br>
        <b style="color:#60a5fa;">In Case of Emergency:</b><br>
        🚨 Call 112 first — they will connect police/ambulance/fire<br>
        📸 Document everything (photos, videos) if safe to do so<br>
        🏥 No hospital can refuse emergency treatment citing payment<br>
        </div>
        """, unsafe_allow_html=True)

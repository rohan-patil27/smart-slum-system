import streamlit as st
from modules.database import get_conn
from datetime import datetime

STATUS_STEPS = ["Applied", "Under Review", "Interview Scheduled", "Selected", "Rejected"]
STATUS_COLORS = {
    "Applied":             ("#1e3a5f", "#60a5fa", "#2d4a8a"),
    "Under Review":        ("#2d1f00", "#f59e0b", "#78350f"),
    "Interview Scheduled": ("#1a1a3e", "#a78bfa", "#4c1d95"),
    "Selected":            ("#0d2d1a", "#34d399", "#065f46"),
    "Rejected":            ("#2d1515", "#f87171", "#7f1d1d"),
}

def show_tracker(user, t):
    st.markdown(
        "<div class='section-header'>"
        "<div class='section-header-icon'>📊</div>"
        "<div><h2>Application Status Tracker</h2>"
        "<p>Apni saari job applications ka status ek jagah dekho</p></div>"
        "</div>",
        unsafe_allow_html=True
    )

    conn = get_conn()
    c    = conn.cursor()

    c.execute("""
        SELECT a.id, j.title, j.company, j.location, j.salary_min, j.salary_max,
               a.status, a.applied_at, a.notes, j.contact, j.id as job_id
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        WHERE a.user_id = ?
        ORDER BY a.applied_at DESC
    """, (user['id'],))
    apps = [dict(r) for r in c.fetchall()]

    if not apps:
        st.markdown(
            "<div style='text-align:center;padding:3rem;'>"
            "<div style='font-size:3rem;margin-bottom:1rem;'>📋</div>"
            "<div style='color:#8b949e;'>Abhi tak kisi job mein apply nahi kiya.</div>"
            "<div style='color:#60a5fa;font-size:0.88rem;margin-top:0.5rem;'>Jobs page pe jao aur apply karo!</div>"
            "</div>",
            unsafe_allow_html=True
        )
        conn.close()
        return

    # Summary cards
    status_counts = {}
    for a in apps:
        status_counts[a['status']] = status_counts.get(a['status'], 0) + 1

    cols = st.columns(5)
    for col, status in zip(cols, STATUS_STEPS):
        cnt = status_counts.get(status, 0)
        bg, fg, border = STATUS_COLORS[status]
        with col:
            st.markdown(
                "<div style='background:" + bg + ";border:1px solid " + border + ";"
                "border-radius:10px;padding:0.8rem;text-align:center;'>"
                "<div style='color:" + fg + ";font-size:1.4rem;font-weight:700;'>" + str(cnt) + "</div>"
                "<div style='color:" + fg + ";font-size:0.72rem;margin-top:2px;opacity:0.85;'>" + status + "</div>"
                "</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.selectbox("Filter by Status", ["All"] + STATUS_STEPS, key="tracker_filter")
    with col2:
        search_term = st.text_input("Search company/job", placeholder="Search...", key="tracker_search")

    filtered = apps
    if filter_status != "All":
        filtered = [a for a in filtered if a['status'] == filter_status]
    if search_term:
        filtered = [a for a in filtered if search_term.lower() in a['title'].lower()
                    or search_term.lower() in a['company'].lower()]

    st.markdown(
        "<div style='color:#8b949e;font-size:0.82rem;margin-bottom:1rem;'>"
        "Showing <b style='color:#60a5fa;'>" + str(len(filtered)) + "</b> applications</div>",
        unsafe_allow_html=True
    )

    for app in filtered:
        bg, fg, border = STATUS_COLORS.get(app['status'], ("#161b22","#e6edf3","#21262d"))
        applied_date = app['applied_at'][:10] if app['applied_at'] else "N/A"

        # Progress bar
        step_idx = STATUS_STEPS.index(app['status']) if app['status'] in STATUS_STEPS else 0
        progress_pct = int(((step_idx + 1) / len(STATUS_STEPS)) * 100)

        st.markdown(
            "<div style='background:#161b22;border:1px solid #21262d;border-radius:14px;"
            "padding:1.2rem;margin-bottom:1rem;border-left:3px solid " + border + ";'>"

            # Header row
            "<div style='display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;'>"
            "<div>"
            "<div style='font-weight:600;color:#e6edf3;font-size:1rem;'>" + app['title'] + "</div>"
            "<div style='color:#60a5fa;font-size:0.88rem;'>🏢 " + app['company'] + "</div>"
            "</div>"
            "<div style='background:" + bg + ";border:1px solid " + border + ";border-radius:20px;"
            "padding:0.3rem 0.9rem;font-size:0.82rem;font-weight:600;color:" + fg + ";'>"
            + app['status'] + "</div>"
            "</div>"

            # Meta
            "<div style='display:flex;flex-wrap:wrap;gap:0.5rem;margin:0.6rem 0;'>"
            "<span style='background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;"
            "border-radius:5px;padding:2px 8px;font-size:0.78rem;'>📍 " + str(app['location']) + "</span>"
            "<span style='background:#0d2d1a;color:#34d399;border:1px solid #065f46;"
            "border-radius:5px;padding:2px 8px;font-size:0.78rem;'>💰 ₹" + str(app['salary_min']) + "–₹" + str(app['salary_max']) + "/mo</span>"
            "<span style='background:#21262d;color:#8b949e;border:1px solid #30363d;"
            "border-radius:5px;padding:2px 8px;font-size:0.78rem;'>📅 Applied: " + applied_date + "</span>"
            "</div>"

            # Progress track
            "<div style='margin:0.6rem 0 0.3rem;'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:4px;'>"
            + "".join([
                "<span style='font-size:0.68rem;color:" +
                (fg if STATUS_STEPS.index(s) <= step_idx else "#484f58") + ";'>" + s + "</span>"
                for s in STATUS_STEPS
            ]) +
            "</div>"
            "<div style='background:#21262d;border-radius:4px;height:6px;'>"
            "<div style='width:" + str(progress_pct) + "%;height:100%;border-radius:4px;"
            "background:" + fg + ";transition:width 0.5s;'></div>"
            "</div>"
            "</div>"

            # Contact
            "<div style='color:#8b949e;font-size:0.8rem;margin-top:0.5rem;'>📞 " + str(app['contact']) + "</div>"
            "</div>",
            unsafe_allow_html=True
        )

        # Update status + notes
        with st.expander("✏️ Status Update / Notes", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                cur_idx = STATUS_STEPS.index(app['status']) if app['status'] in STATUS_STEPS else 0
                new_status = st.selectbox(
                    "Update Status",
                    STATUS_STEPS,
                    index=cur_idx,
                    key="status_sel_" + str(app['id'])
                )
            with col2:
                notes = st.text_input(
                    "Notes (interview date, contact person...)",
                    value=app.get('notes','') or '',
                    key="notes_" + str(app['id'])
                )
            if st.button("💾 Save", key="save_status_" + str(app['id'])):
                conn.execute(
                    "UPDATE applications SET status=?, notes=? WHERE id=?",
                    (new_status, notes, app['id'])
                )
                conn.commit()
                st.success("✅ Updated!")
                st.rerun()

    conn.close()

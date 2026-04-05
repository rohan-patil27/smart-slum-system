import streamlit as st
from modules.database import get_conn
import io
from datetime import datetime

def show_resume_generator(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">📄</div>
        <div>
            <h2>Resume Generator</h2>
            <p>Create a professional resume PDF in seconds</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_preview = st.columns([1, 1])

    with col_form:
        st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:14px;padding:1.5rem;">
        <div style="font-weight:600;color:#e6edf3;margin-bottom:1rem;">✏️ Fill Your Details</div>""", unsafe_allow_html=True)

        name = st.text_input("Full Name", value=user.get('name',''), key="res_name")
        phone = st.text_input("Mobile Number", value=user.get('phone',''), key="res_phone")
        location = st.text_input("Address / Location", value=user.get('location',''), key="res_loc")
        email = st.text_input("Email (optional)", placeholder="example@gmail.com", key="res_email")
        objective = st.text_area("Career Objective", value="Seeking a suitable opportunity to utilize my skills and contribute to organizational growth.", height=80, key="res_obj")
        skills = st.text_input("Skills", value=user.get('skills',''), key="res_skills")
        education = st.text_input("Education", value=user.get('education',''), key="res_edu")
        experience = st.text_area("Work Experience (if any)", placeholder="e.g. Electrician at ABC company for 2 years", height=80, key="res_exp")
        languages = st.text_input("Languages Known", value="Hindi, Marathi, English", key="res_lang")
        references = st.text_input("Reference (optional)", placeholder="Name - Phone number", key="res_ref")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:14px;padding:1.5rem;">
        <div style="font-weight:600;color:#e6edf3;margin-bottom:1rem;">👁️ Resume Preview</div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#ffffff;color:#1a1a1a;padding:2rem;border-radius:10px;font-family:Georgia,serif;">
            <div style="text-align:center;border-bottom:3px solid #1e40af;padding-bottom:1rem;margin-bottom:1rem;">
                <div style="font-size:1.4rem;font-weight:700;color:#1e40af;">{name or 'Your Name'}</div>
                <div style="font-size:0.85rem;color:#4b5563;margin-top:0.3rem;">
                    📱 {phone or 'Phone'} &nbsp;|&nbsp; 📍 {location or 'Location'}
                    {f'&nbsp;|&nbsp; ✉️ {email}' if email else ''}
                </div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="font-weight:700;color:#1e40af;font-size:0.9rem;border-bottom:1px solid #dbeafe;padding-bottom:0.3rem;margin-bottom:0.4rem;">CAREER OBJECTIVE</div>
                <div style="font-size:0.85rem;color:#374151;">{objective or '—'}</div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="font-weight:700;color:#1e40af;font-size:0.9rem;border-bottom:1px solid #dbeafe;padding-bottom:0.3rem;margin-bottom:0.4rem;">SKILLS</div>
                <div style="font-size:0.85rem;color:#374151;">{skills or '—'}</div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="font-weight:700;color:#1e40af;font-size:0.9rem;border-bottom:1px solid #dbeafe;padding-bottom:0.3rem;margin-bottom:0.4rem;">EDUCATION</div>
                <div style="font-size:0.85rem;color:#374151;">{education or '—'}</div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="font-weight:700;color:#1e40af;font-size:0.9rem;border-bottom:1px solid #dbeafe;padding-bottom:0.3rem;margin-bottom:0.4rem;">WORK EXPERIENCE</div>
                <div style="font-size:0.85rem;color:#374151;">{experience or 'Fresher – Ready to work and learn'}</div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="font-weight:700;color:#1e40af;font-size:0.9rem;border-bottom:1px solid #dbeafe;padding-bottom:0.3rem;margin-bottom:0.4rem;">LANGUAGES</div>
                <div style="font-size:0.85rem;color:#374151;">{languages or '—'}</div>
            </div>
            {'<div><div style="font-weight:700;color:#1e40af;font-size:0.9rem;border-bottom:1px solid #dbeafe;padding-bottom:0.3rem;margin-bottom:0.4rem;">REFERENCE</div><div style="font-size:0.85rem;color:#374151;">'+references+'</div></div>' if references else ''}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬇️ Download Resume as HTML", use_container_width=True, type="primary", key="download_resume"):
            html_content = _generate_html_resume(name, phone, location, email, objective, skills, education, experience, languages, references)
            st.download_button(
                label="📥 Click to Download resume.html",
                data=html_content,
                file_name=f"Resume_{name.replace(' ','_')}.html",
                mime="text/html",
                use_container_width=True,
                key="dl_html"
            )
            st.info("💡 Tip: Open the downloaded file in Chrome and press Ctrl+P to save/print as PDF!")

def _generate_html_resume(name, phone, location, email, objective, skills, education, experience, languages, references):
    date_now = datetime.now().strftime("%B %Y")
    ref_html = f"""<div class='section'><div class='section-title'>REFERENCE</div><p>{references}</p></div>""" if references else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Resume - {name}</title>
<style>
  body {{ font-family: 'Georgia', serif; max-width: 800px; margin: 40px auto; padding: 2rem; color: #1a1a1a; }}
  .header {{ text-align: center; border-bottom: 3px solid #1e40af; padding-bottom: 1rem; margin-bottom: 1.5rem; }}
  .header h1 {{ color: #1e40af; font-size: 2rem; margin: 0; }}
  .contact {{ color: #4b5563; font-size: 0.95rem; margin-top: 0.5rem; }}
  .section {{ margin-bottom: 1.5rem; }}
  .section-title {{ font-weight: bold; color: #1e40af; font-size: 1rem; border-bottom: 1px solid #bfdbfe; padding-bottom: 4px; margin-bottom: 8px; letter-spacing: 1px; }}
  p {{ font-size: 0.95rem; color: #374151; line-height: 1.6; margin: 0; }}
  @media print {{ body {{ margin: 0; padding: 1rem; }} }}
</style>
</head>
<body>
  <div class="header">
    <h1>{name}</h1>
    <div class="contact">📱 {phone} &nbsp;|&nbsp; 📍 {location}{f' &nbsp;|&nbsp; ✉️ {email}' if email else ''}</div>
    <div style="color:#6b7280;font-size:0.85rem;margin-top:0.3rem;">Generated on {date_now}</div>
  </div>
  <div class="section"><div class="section-title">CAREER OBJECTIVE</div><p>{objective}</p></div>
  <div class="section"><div class="section-title">SKILLS</div><p>{skills}</p></div>
  <div class="section"><div class="section-title">EDUCATION</div><p>{education}</p></div>
  <div class="section"><div class="section-title">WORK EXPERIENCE</div><p>{experience or 'Fresher – Ready to work and learn'}</p></div>
  <div class="section"><div class="section-title">LANGUAGES</div><p>{languages}</p></div>
  {ref_html}
</body>
</html>"""

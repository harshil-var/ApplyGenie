
import os
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ApplyGenie",
    page_icon="🧞",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🧞 ApplyGenie</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered job application assistant. '
    'Generate personalized application emails, cover letters, '
    'and job summaries from your resume and a job posting.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BACKEND CONFIGURATION
# ============================================================

# Default backend URL
API_URL = os.getenv(
    "API_URL",
    "https://applygenie.onrender.com"
).rstrip("/")

# Override using Streamlit secrets if available
try:
    if "API_URL" in st.secrets:
        API_URL = st.secrets["API_URL"].rstrip("/")
except Exception:
    pass


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None


# ============================================================
# JOB INFORMATION
# ============================================================

st.header("🔗 Job Information")

job_url = st.text_input(
    "Job Posting URL",
    placeholder="https://company.com/jobs/ai-engineer",
    help="Paste the URL of the job posting you want to apply for."
)


# ============================================================
# RESUME UPLOAD
# ============================================================

st.header("📄 Resume")

resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    help="Upload your resume as a PDF file."
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate = st.button(
    "🚀 Generate Application",
    use_container_width=True
)


# ============================================================
# GENERATE APPLICATION
# ============================================================

if generate:

    # --------------------------------------------------------
    # Validate Job URL
    # --------------------------------------------------------

    if not job_url.strip():
        st.warning("⚠️ Please enter the job posting URL.")
        st.stop()

    job_url = job_url.strip()

    if not job_url.startswith(("http://", "https://")):
        st.warning(
            "⚠️ Please enter a valid URL starting with "
            "`http://` or `https://`."
        )
        st.stop()

    # --------------------------------------------------------
    # Validate Resume
    # --------------------------------------------------------

    if resume is None:
        st.warning("⚠️ Please upload your resume PDF.")
        st.stop()

    # --------------------------------------------------------
    # Validate Resume Size
    # --------------------------------------------------------

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    if resume.size > MAX_FILE_SIZE:
        st.error("❌ Resume file is too large. Maximum size is 10 MB.")
        st.stop()

    # --------------------------------------------------------
    # Send Request to FastAPI Backend
    # --------------------------------------------------------

    with st.spinner(
        "🔍 Scraping the job posting, analyzing your resume, "
        "and generating your application... "
        "This may take up to 2 minutes."
    ):

        try:

            files = {
                "resume": (
                    resume.name,
                    resume.getvalue(),
                    "application/pdf"
                )
            }

            data = {
                "link": job_url
            }

            response = requests.post(
                f"{API_URL}/generate_application",
                data=data,
                files=files,
                timeout=180
            )

            # ------------------------------------------------
            # Successful Response
            # ------------------------------------------------

            if response.status_code == 200:

                try:
                    result = response.json()

                except ValueError:
                    st.error(
                        "❌ Backend returned an invalid JSON response."
                    )
                    st.stop()

                st.session_state.result = result

                st.success(
                    "✅ Application materials generated successfully!"
                )

            # ------------------------------------------------
            # Backend Error
            # ------------------------------------------------

            else:

                try:
                    error_data = response.json()

                    error = error_data.get(
                        "detail",
                        "Unknown backend error."
                    )

                except ValueError:
                    error = response.text

                st.error(
                    f"❌ Backend Error ({response.status_code}): {error}"
                )

        # ----------------------------------------------------
        # Connection Error
        # ----------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                f"❌ Could not connect to the FastAPI server.\n\n"
                f"Backend: `{API_URL}`\n\n"
                "If your backend is hosted on Render's free tier, "
                "it may be sleeping. Please wait a little and try again."
            )

        # ----------------------------------------------------
        # Timeout Error
        # ----------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "⏳ The request took too long to complete. "
                "Please try again."
            )

        # ----------------------------------------------------
        # Request Error
        # ----------------------------------------------------

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Request failed: {str(e)}"
            )

        # ----------------------------------------------------
        # Unexpected Error
        # ----------------------------------------------------

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {str(e)}"
            )


# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.result:

    res = st.session_state.result

    # --------------------------------------------------------
    # Job Title
    # --------------------------------------------------------

    st.header("🎯 Job")

    job_title = res.get(
        "job_title",
        "Job Application"
    )

    st.info(f"**{job_title}**")


    # --------------------------------------------------------
    # Job Summary
    # --------------------------------------------------------

    st.header("📋 Job Summary")

    job_summary = res.get(
        "job_summary",
        ""
    )

    st.text_area(
        "Job Summary Output",
        value=job_summary,
        height=350,
        key="summary_area"
    )

    st.download_button(
        "⬇️ Download Job Summary",
        data=job_summary,
        file_name="job_summary.txt",
        mime="text/plain",
        key="summary_download"
    )


    # --------------------------------------------------------
    # Application Email
    # --------------------------------------------------------

    st.header("📧 Application Email")

    email = res.get(
        "email",
        ""
    )

    st.text_area(
        "Generated Email Output",
        value=email,
        height=350,
        key="email_area"
    )

    st.download_button(
        "⬇️ Download Email",
        data=email,
        file_name="application_email.txt",
        mime="text/plain",
        key="email_download"
    )


    # --------------------------------------------------------
    # Cover Letter
    # --------------------------------------------------------

    st.header("📝 Cover Letter")

    cover_letter = res.get(
        "cover_letter",
        ""
    )

    st.text_area(
        "Generated Cover Letter Output",
        value=cover_letter,
        height=450,
        key="cover_area"
    )

    st.download_button(
        "⬇️ Download Cover Letter",
        data=cover_letter,
        file_name="cover_letter.txt",
        mime="text/plain",
        key="cover_download"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🧞 ApplyGenie • Built with Python • FastAPI • Streamlit • "
    "Playwright • PyPDF • Mistral"
)


import requests
import streamlit as st

st.set_page_config(
    page_title="ApplyGenie",
    page_icon="🧞",
    layout="wide"
)

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


# Header

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


# Backend Configuration

API_URL = " https://applygenie.onrender.com/generate_application || http://127.0.0.1:8000/generate_application "


# Input Section


st.header("🔗 Job Information")

job_url = st.text_input(
    "Job Posting URL",
    placeholder="https://company.com/jobs/ai-engineer"
)


st.header("📄 Resume")

resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    help="Upload your resume as a PDF file."
)


generate = st.button(
    "🚀 Generate Application",
    use_container_width=True
)

# Generate Application

if generate:

    if not job_url:

        st.warning(
            "Please enter the job posting URL."
        )

        st.stop()

    if not job_url.startswith(
        ("http://", "https://")
    ):

        st.warning(
            "Please enter a valid URL starting with "
            "http:// or https://"
        )

        st.stop()

    if resume is None:

        st.warning(
            "Please upload your resume PDF."
        )

        st.stop()

   
    # Send Request

    with st.spinner(
        "🔍 Analyzing job posting and resume..."
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

            # Successful Response
            

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "✅ Application materials generated successfully!"
                )

              # JOB title
                st.header("🎯 Job")

                job_title = result.get(
                    "job_title",
                    "Job Application"
                )

                st.info(
                    f"**{job_title}**"
                )

                # Job Summary
                
                st.header("📋 Job Summary")

                job_summary = result.get(
                    "job_summary",
                    ""
                )

                st.text_area(
                    "Job Summary",
                    value=job_summary,
                    height=400
                )

                st.download_button(
                    "⬇️ Download Job Summary",
                    data=job_summary,
                    file_name="job_summary.txt",
                    mime="text/plain"
                )

                # Application EMAIL
                

                st.header("📧 Application Email")

                email = result.get(
                    "email",
                    ""
                )

                st.text_area(
                    "Generated Email",
                    value=email,
                    height=350
                )

                st.download_button(
                    "⬇️ Download Email",
                    data=email,
                    file_name="application_email.txt",
                    mime="text/plain"
                )

                # Cover Letter

                st.header("📝 Cover Letter")

                cover_letter = result.get(
                    "cover_letter",
                    ""
                )

                st.text_area(
                    "Generated Cover Letter",
                    value=cover_letter,
                    height=500
                )

                st.download_button(
                    "⬇️ Download Cover Letter",
                    data=cover_letter,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )

            # Backend Error
            

            else:

                try:

                    error = response.json().get(
                        "detail",
                        "Unknown backend error."
                    )

                except Exception:

                    error = response.text

                st.error(
                    f"❌ Backend Error: {error}"
                )

        # Connection Error

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the FastAPI server.\n\n"
                "Make sure the backend is running."
            )

        # Timeout

        except requests.exceptions.Timeout:

            st.error(
                "⏳ The request took too long. "
                "Please try again."
            )

        # Other Errors
        

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {str(e)}"
            )
 
# Footer

st.markdown("---")

st.caption(
    "🧞 ApplyGenie • Built with Python • FastAPI • Streamlit • "
    "Playwright • PyPDF • Mistral"
)

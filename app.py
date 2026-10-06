import streamlit as st
from auditor import audit_website, get_ai_analysis


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Security Auditor",
    page_icon="🔐",
    layout="wide"
)


# ---------------- CSS ----------------

st.markdown("""
<style>

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1f4e79;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------

st.markdown(
    '<div class="title">🔐 AI Security Auditor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze basic security configurations of websites you own '
    'or have permission to test.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- SIDEBAR ----------------

st.sidebar.title("Security Auditor")

st.sidebar.info(
    "Use this tool only on websites or systems you own "
    "or have explicit permission to audit."
)


# ---------------- URL INPUT ----------------

url = st.text_input(
    "🌐 Enter Website URL",
    placeholder="https://example.com"
)


audit_button = st.button(
    "🔍 Start Security Audit",
    use_container_width=True
)


# ---------------- AUDIT ----------------

if audit_button:

    if not url:

        st.warning("Please enter a website URL.")

    else:

        with st.spinner("Running security audit..."):

            result = audit_website(url)


        # ---------------- ERROR ----------------

        if not result["success"]:

            st.error(result["error"])


        # ---------------- SUCCESS ----------------

        else:

            st.success("Website successfully checked!")


            # ---------------- WEBSITE INFORMATION ----------------

            st.subheader("📊 Website Information")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Status Code",
                    result["status_code"]
                )

            with col2:

                st.metric(
                    "HTTPS",
                    "Enabled"
                    if result["https"]
                    else "Not Enabled"
                )

            with col3:

                st.metric(
                    "Response Time",
                    f"{result['response_time']:.2f}s"
                )


            # ---------------- SECURITY SCORE ----------------

            st.subheader("📈 Security Score")

            score = result["score"]

            st.progress(score / 100)

            score_col1, score_col2 = st.columns(2)


            with score_col1:

                st.metric(
                    "Security Score",
                    f"{score}/100"
                )


            with score_col2:

                risk = result["risk_level"]

                if risk == "Low":

                    st.success(
                        f"🟢 Risk Level: {risk}"
                    )

                elif risk == "Medium":

                    st.warning(
                        f"🟠 Risk Level: {risk}"
                    )

                else:

                    st.error(
                        f"🔴 Risk Level: {risk}"
                    )


            # ---------------- SECURITY HEADERS ----------------

            st.subheader("🛡️ Security Headers")


            st.write("### Present")

            if result["headers_found"]:

                for header in result["headers_found"]:

                    st.success(
                        f"✅ {header}"
                    )

            else:

                st.info(
                    "No recommended security headers were found."
                )


            st.write("### Missing")

            if result["headers_missing"]:

                for header in result["headers_missing"]:

                    st.warning(
                        f"⚠️ {header}"
                    )

            else:

                st.success(
                    "All checked security headers are present!"
                )


            # ---------------- AUDIT SUMMARY ----------------

            st.subheader("📋 Audit Summary")


            summary_col1, summary_col2 = st.columns(2)


            with summary_col1:

                st.write(
                    f"**Security headers found:** "
                    f"{len(result['headers_found'])}"
                )

                st.write(
                    f"**Security headers missing:** "
                    f"{len(result['headers_missing'])}"
                )


            with summary_col2:

                st.write(
                    f"**Security Score:** "
                    f"{score}/100"
                )

                st.write(
                    f"**Risk Level:** "
                    f"{result['risk_level']}"
                )


            st.info(
                "This tool performs a basic security configuration "
                "audit. A missing security header does not automatically "
                "mean that a website is vulnerable."
            )


            # ---------------- AI ANALYSIS ----------------

            st.subheader("🤖 AI Security Analysis")

            with st.spinner(
                "Gemini AI is analyzing the security findings..."
            ):

                ai_result = get_ai_analysis(result)


            st.write(ai_result)


            # ---------------- DOWNLOAD REPORT ----------------

            st.subheader("📥 Security Report")


            report = f"""
AI SECURITY AUDITOR
===================

Website:
{result["url"]}

HTTP Status Code:
{result["status_code"]}

HTTPS:
{"Enabled" if result["https"] else "Not Enabled"}

Response Time:
{result["response_time"]:.2f} seconds


SECURITY SCORE
==============

Score: {score}/100

Risk Level: {result["risk_level"]}


SECURITY HEADERS
================

Present:
{chr(10).join("- " + item for item in result["headers_found"]) if result["headers_found"] else "None"}


Missing:
{chr(10).join("- " + item for item in result["headers_missing"]) if result["headers_missing"] else "None"}


AI SECURITY ANALYSIS
====================

{ai_result}


DISCLAIMER
==========

This tool performs a basic security configuration audit.
It is not a replacement for a complete penetration test
or professional security assessment.
"""


            st.download_button(

                label="📥 Download Security Report",

                data=report,

                file_name="security_audit_report.txt",

                mime="text/plain",

                use_container_width=True
            )
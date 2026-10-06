import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
from google import genai


# ---------------- SECURITY CHECKS ----------------

SECURITY_CHECKS = {
    "Strict-Transport-Security": {
        "name": "HSTS",
        "weight": 15
    },
    "Content-Security-Policy": {
        "name": "Content Security Policy",
        "weight": 20
    },
    "X-Content-Type-Options": {
        "name": "X-Content-Type-Options",
        "weight": 10
    },
    "X-Frame-Options": {
        "name": "Clickjacking Protection",
        "weight": 15
    },
    "Referrer-Policy": {
        "name": "Referrer Policy",
        "weight": 10
    },
    "Permissions-Policy": {
        "name": "Permissions Policy",
        "weight": 10
    }
}


# ---------------- WEBSITE AUDIT ----------------

def audit_website(url):

    # Add HTTPS if user doesn't enter protocol
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed_url = urlparse(url)

    if not parsed_url.hostname:
        return {
            "success": False,
            "error": "Invalid URL"
        }

    try:

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        headers_found = []
        headers_missing = []

        earned_score = 0
        maximum_header_score = sum(
            item["weight"] for item in SECURITY_CHECKS.values()
        )

        # ---------------- HEADER CHECK ----------------

        for header, details in SECURITY_CHECKS.items():

            if header in response.headers:

                headers_found.append(details["name"])
                earned_score += details["weight"]

            else:

                headers_missing.append(details["name"])


        # ---------------- HTTPS SCORE ----------------

        https_enabled = response.url.startswith("https://")

        # HTTPS gets 20 points
        https_score = 20 if https_enabled else 0

        # Total possible = 100
        score = int(
            ((earned_score + https_score) /
             (maximum_header_score + 20)) * 100
        )


        # ---------------- RISK LEVEL ----------------

        if score >= 85:
            risk_level = "Low"

        elif score >= 60:
            risk_level = "Medium"

        else:
            risk_level = "High"


        # ---------------- RETURN RESULT ----------------

        return {

            "success": True,

            "url": response.url,

            "status_code": response.status_code,

            "https": https_enabled,

            "response_time": response.elapsed.total_seconds(),

            "headers_found": headers_found,

            "headers_missing": headers_missing,

            "score": score,

            "risk_level": risk_level

        }


    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "The website took too long to respond."
        }


    except requests.exceptions.SSLError:

        return {
            "success": False,
            "error": "SSL certificate verification failed."
        }


    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "error": "Could not connect to the website."
        }


    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


# ---------------- GEMINI AI ----------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:

    client = genai.Client(api_key=api_key)

else:

    client = None


def get_ai_analysis(result):

    if client is None:

        return (
            "Gemini API key not found. "
            "Please check your .env file."
        )


    findings = "\n".join(
        f"- {item}"
        for item in result["headers_missing"]
    )


    if not findings:

        findings = "No checked security headers are missing."


    prompt = f"""

You are a cybersecurity assistant.

Analyze the following website security audit.

Website: {result["url"]}

HTTP Status Code: {result["status_code"]}

HTTPS: {result["https"]}

Security Score: {result["score"]}/100

Risk Level: {result["risk_level"]}

Missing Security Headers:
{findings}


Provide the analysis in the following structure:

1. Risk Level
2. Security Findings
3. Why These Findings Matter
4. Recommended Fixes
5. Overall Security Assessment

Explain the findings clearly for a student/project user.

Do not claim that the website is hacked or compromised
only because a security header is missing.

This is a basic security configuration audit,
not a full penetration test.
"""


    try:

        response = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=prompt

        )

        return response.text


    except Exception as error:

        return f"AI analysis failed: {error}"
"""
AI Workplace Productivity Assistant
Built with Streamlit + Google Gemini
Capaciti AI Skill Accelerator Programme
Single-file complete application.
"""

import os
import re
import json

import streamlit as st
import pandas as pd
import google.generativeai as genai

# ==================================================================
# PAGE CONFIG
# ==================================================================
st.set_page_config(
    page_title="AI Workplace Productivity Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================================
# RESPONSIBLE AI TEXT
# ==================================================================
DISCLAIMER = """
> ⚠️ **Responsible AI Notice**
> This assistant uses Google Gemini. Outputs may contain inaccuracies,
> bias, or outdated information. **Always review, validate and edit
> AI-generated content before professional use.** Do not paste
> confidential client data into public AI tools.
"""

BIAS_WARNING = """
> 🧭 **Bias & Fairness Check:** AI can reflect historical bias in
> language. Review for gendered, cultural or ableist phrasing.
> Verify all factual claims independently.
"""

# ==================================================================
# GEMINI HELPERS
# ==================================================================
def get_api_key() -> str:
    """Read API key from Streamlit secrets, env, or sidebar."""
    if st.session_state.get("api_key"):
        return st.session_state["api_key"]
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


def call_gemini(system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
    """Send a prompt to Gemini and return text."""
    api_key = get_api_key()
    if not api_key:
        return "⚠️ No Gemini API key configured. Add it in the sidebar or Streamlit secrets."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=st.session_state.get("model", "gemini-1.5-flash"),
            system_instruction=system_prompt,
        )
        response = model.generate_content(
            user_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 4096,
            },
        )
        return (response.text or "").strip()
    except Exception as e:
        return f"❌ Gemini error: {e}"


def extract_json(raw: str):
    """Robustly pull JSON out of an LLM reply."""
    if not raw:
        return None
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except Exception:
        try:
            cleaned = match.group().replace("'", '"')
            return json.loads(cleaned)
        except Exception:
            return None


# ==================================================================
# SIDEBAR
# ==================================================================
with st.sidebar:
    st.title("🤖 AI Productivity Assistant")
    st.caption("Powered by Google Gemini")

    st.session_state["api_key"] = st.text_input(
        "Gemini API Key",
        value=st.session_state.get("api_key", ""),
        type="password",
        help="Get one free at https://aistudio.google.com/app/apikey",
    )

    st.session_state["model"] = st.selectbox(
        "Model",
        ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro"],
        index=0,
    )

    st.divider()

    module = st.radio(
        "Choose a module",
        [
            "🏠 Home",
            "📄 AI Resume Builder",
            "✉️ Smart Email Generator",
            "📝 Meeting Notes Summarizer",
            "📅 AI Task Planner",
            "🔎 AI Research Assistant",
            "💬 AI Workplace Chatbot",
        ],
    )

    st.divider()
    st.markdown(DISCLAIMER)

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat cleared.")


# ==================================================================
# HOME
# ==================================================================
if module == "🏠 Home":
    st.title("🤖 AI Workplace Productivity Assistant")
    st.markdown(
        """
        Welcome to your **AI-powered workplace assistant**, built with
        **Streamlit + Google Gemini** for the Capaciti AI Skill Accelerator Programme.

        ### Modules
        1. **📄 AI Resume Builder** — ATS-optimised resumes with Markdown/HTML export
        2. **✉️ Smart Email Generator** — Tone & audience-aware emails
        3. **📝 Meeting Notes Summarizer** — Decisions, actions, owners, risks
        4. **📅 AI Task Planner** — Priorities, timelines, definitions of done
        5. **🔎 AI Research Assistant** — Executive summaries & insights
        6. **💬 AI Workplace Chatbot** — Multi-turn conversational assistant

        ### Responsible AI
        Every module includes disclaimers, bias warnings, and validation steps.
        """
    )
    st.info("👉 Add your Gemini API key in the sidebar, then choose a module.")


# ==================================================================
# 1. AI RESUME BUILDER
# ==================================================================
elif module == "📄 AI Resume Builder":
    st.title("📄 AI Resume Builder")
    st.markdown(DISCLAIMER)

    with st.form("resume_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name", "Jane Doe")
            email = st.text_input("Email", "jane@example.com")
            phone = st.text_input("Phone", "+27 00 000 0000")
            location = st.text_input("Location", "Gqeberha, South Africa")

        with col2:
            target_job = st.text_input("Target Job Title", "Junior Data Analyst")
            years_exp = st.number_input("Years of Experience", 0, 40, 3)
            education = st.text_input("Education", "BSc Computer Science")

        st.markdown("### Job Description")
        job_description = st.text_area(
            "Paste the full job description",
            height=150,
            placeholder="Paste the target job description here...",
        )

        st.markdown("### Your Experience")
        experience = st.text_area(
            "Experience (one bullet per line)",
            height=150,
            placeholder="- Built dashboards in Power BI\n- Automated weekly reports with Python",
        )

        st.markdown("### Your Skills")
        skills = st.text_area(
            "Skills (comma-separated)",
            value="Python, SQL, Excel, Power BI, Communication",
        )

        submitted = st.form_submit_button("🚀 Generate Resume")

    if submitted:
        if not job_description.strip():
            st.warning("Please paste the job description.")
        else:
            with st.spinner("Generating professional summary..."):
                summary = call_gemini(
                    "You are an expert ATS-friendly resume writer.",
                    f"""Write a 3-4 sentence professional summary for {name},
targeting the role "{target_job}".
Years of experience: {years_exp}. Education: {education}.
Job description: {job_description}
Experience: {experience}
Skills: {skills}""",
                )

            with st.spinner("Improving experience bullets..."):
                improved_exp = call_gemini(
                    "You are a senior resume coach specialising in ATS optimisation.",
                    f"""Rewrite the following experience bullets to be achievement-oriented,
quantified where possible, aligned to the target role "{target_job}".
Return each bullet on a new line starting with "- ".
Original:
{experience}""",
                )

            with st.spinner("Running ATS keyword analysis..."):
                ats_raw = call_gemini(
                    "You are an ATS optimisation specialist. Return valid JSON only.",
                    f"""Compare the resume below with the job description.
Return a JSON object with keys:
"matched_keywords": list,
"missing_keywords": list,
"ats_score": integer 0-100,
"suggestions": list of 3 strings.

Job Description:
{job_description}

Resume Summary:
{summary}

Experience:
{improved_exp}

Skills: {skills}""",
                )

            ats_data = extract_json(ats_raw) or {
                "matched_keywords": [],
                "missing_keywords": [],
                "ats_score": 0,
                "suggestions": ["Could not parse ATS output."],
            }

            resume_md = f"""# {name}
📍 {location} | ✉️ {email} | ☎️ {phone}

## Target Role
**{target_job}**

## Professional Summary
{summary}

## Experience
{improved_exp}

## Skills
{skills}

## Education
{education}
"""

            html_resume = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{name} - Resume</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; color:#222; }}
h1 {{ color:#0d3b66; }} h2 {{ color:#1d3557; border-bottom:1px solid #ccc; padding-bottom:4px; }}
ul {{ line-height:1.6; }}
</style></head><body>
<h1>{name}</h1>
<p>{location} | {email} | {phone}</p>
<h2>Target Role</h2><p><strong>{target_job}</strong></p>
<h2>Professional Summary</h2><p>{summary}</p>
<h2>Experience</h2><ul>
{''.join(f'<li>{line.lstrip("- ")}</li>' for line in improved_exp.splitlines() if line.strip())}
</ul>
<h2>Skills</h2><p>{skills}</p>
<h2>Education</h2><p>{education}</p>
</body></html>"""

            st.success("✅ Resume generated!")

            tab1, tab2, tab3 = st.tabs(["👁️ Preview", "📊 ATS Analysis", "⬇️ Export"])

            with tab1:
                st.markdown(resume_md)

            with tab2:
                score = int(ats_data.get("ats_score", 0))
                st.metric("ATS Score", f"{score}/100")
                st.progress(min(max(score, 0), 100) / 100)

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**✅ Matched Keywords**")
                    for k in ats_data.get("matched_keywords", []):
                        st.markdown(f"- {k}")
                with c2:
                    st.markdown("**❌ Missing Keywords**")
                    for k in ats_data.get("missing_keywords", []):
                        st.markdown(f"- {k}")

                st.markdown("**💡 Suggestions**")
                for s in ats_data.get("suggestions", []):
                    st.markdown(f"- {s}")

                st.markdown(BIAS_WARNING)

            with tab3:
                st.download_button(
                    "⬇️ Download Markdown",
                    data=resume_md,
                    file_name=f"{name.replace(' ', '_')}_resume.md",
                    mime="text/markdown",
                )
                st.download_button(
                    "⬇️ Download HTML",
                    data=html_resume,
                    file_name=f"{name.replace(' ', '_')}_resume.html",
                    mime="text/html",
                )


# ==================================================================
# 2. SMART EMAIL GENERATOR
# ==================================================================
elif module == "✉️ Smart Email Generator":
    st.title("✉️ Smart Email Generator")
    st.markdown(DISCLAIMER)

    col1, col2, col3 = st.columns(3)
    with col1:
        audience = st.selectbox("Audience", ["Client", "Manager", "Team"])
    with col2:
        tone = st.selectbox("Tone", ["Formal", "Professional", "Friendly", "Persuasive"])
    with col3:
        length = st.selectbox("Length", ["Short", "Medium", "Detailed"])

    subject = st.text_input("Email Subject / Purpose", "Follow-up on project proposal")
    context = st.text_area(
        "Context / Key Points",
        height=150,
        placeholder="Mention the deadline, attach the proposal, ask for feedback by Friday...",
    )

    if st.button("✉️ Generate Email"):
        with st.spinner("Drafting email..."):
            email = call_gemini(
                "You are a professional business communication assistant.",
                f"""Write a {tone.lower()} email to a {audience.lower()}.
Length: {length}.
Subject / Purpose: {subject}
Context / Key points: {context}

Rules:
- Include a clear subject line.
- Use a professional sign-off.
- Do not invent facts not provided.""",
            )
        st.markdown(email)
        st.download_button(
            "⬇️ Download Email",
            data=email,
            file_name="email.txt",
            mime="text/plain",
        )
        st.markdown(BIAS_WARNING)


# ==================================================================
# 3. MEETING NOTES SUMMARIZER
# ==================================================================
elif module == "📝 Meeting Notes Summarizer":
    st.title("📝 Meeting Notes Summarizer")
    st.markdown(DISCLAIMER)

    notes = st.text_area(
        "Paste raw meeting notes",
        height=250,
        placeholder="Paste transcript or rough notes here...",
    )

    if st.button("📝 Summarize"):
        if not notes.strip():
            st.warning("Please paste meeting notes.")
        else:
            with st.spinner("Summarising..."):
                raw = call_gemini(
                    "You are an expert meeting analyst. Return valid JSON only.",
                    f"""Analyse the meeting notes below and return a JSON object with:
"key_points": list of strings,
"decisions": list of strings,
"action_items": list of objects with "task" and "owner",
"deadlines": list of strings,
"risks": list of strings,
"open_questions": list of strings.

Notes:
{notes}""",
                )

            data = extract_json(raw)
            if not data:
                st.error("Could not parse model output. Raw response:")
                st.code(raw)
            else:
                st.subheader("🔑 Key Points")
                for x in data.get("key_points", []):
                    st.markdown(f"- {x}")

                st.subheader("✅ Decisions")
                for x in data.get("decisions", []):
                    st.markdown(f"- {x}")

                st.subheader("📌 Action Items")
                df = pd.DataFrame(data.get("action_items", []))
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No action items identified.")

                st.subheader("⏰ Deadlines")
                for x in data.get("deadlines", []):
                    st.markdown(f"- {x}")

                st.subheader("⚠️ Risks")
                for x in data.get("risks", []):
                    st.markdown(f"- {x}")

                st.subheader("❓ Open Questions")
                for x in data.get("open_questions", []):
                    st.markdown(f"- {x}")

                st.download_button(
                    "⬇️ Download Summary (JSON)",
                    data=json.dumps(data, indent=2),
                    file_name="meeting_summary.json",
                    mime="application/json",
                )


# ==================================================================
# 4. AI TASK PLANNER
# ==================================================================
elif module == "📅 AI Task Planner":
    st.title("📅 AI Task Planner")
    st.markdown(DISCLAIMER)

    tasks = st.text_area(
        "List your tasks (one per line)",
        height=150,
        placeholder="- Finish quarterly report\n- Reply to client emails\n- Prepare team standup",
    )
    horizon = st.selectbox("Planning Horizon", ["Day", "Week"])
    hours = st.slider("Available hours", 1, 60, 8)

    if st.button("📅 Build Plan"):
        if not tasks.strip():
            st.warning("Please add some tasks.")
        else:
            with st.spinner("Planning..."):
                raw = call_gemini(
                    "You are an expert productivity coach. Return valid JSON only.",
                    f"""Build a {horizon.lower()} plan for the following tasks.
Available hours: {hours}
Tasks:
{tasks}

Return a JSON object with:
"prioritised_tasks": list of objects with keys
    "task", "priority" (High/Medium/Low), "time_estimate", "action_plan",
"timeline": list of strings,
"time_optimisation": list of strings,
"definition_of_done": list of strings,
"risks_and_mitigations": list of objects with "risk" and "mitigation".""",
                )
            data = extract_json(raw)
            if not data:
                st.error("Parse error. Raw output:")
                st.code(raw)
            else:
                st.subheader("🎯 Prioritised Tasks")
                df = pd.DataFrame(data.get("prioritised_tasks", []))
                if not df.empty:
                    st.dataframe(df, use_container_width=True)

                st.subheader("🗓️ Timeline")
                for x in data.get("timeline", []):
                    st.markdown(f"- {x}")

                st.subheader("⚡ Time Optimisation")
                for x in data.get("time_optimisation", []):
                    st.markdown(f"- {x}")

                st.subheader("🏁 Definition of Done")
                for x in data.get("definition_of_done", []):
                    st.markdown(f"- {x}")

                st.subheader("⚠️ Risks & Mitigations")
                for r in data.get("risks_and_mitigations", []):
                    st.markdown(f"- **{r.get('risk')}** → {r.get('mitigation')}")


# ==================================================================
# 5. AI RESEARCH ASSISTANT
# ==================================================================
elif module == "🔎 AI Research Assistant":
    st.title("🔎 AI Research Assistant")
    st.markdown(DISCLAIMER)

    topic = st.text_input(
        "Research topic / question",
        "Impact of AI on entry-level jobs in South Africa",
    )
    text = st.text_area(
        "Paste article / report (optional)",
        height=200,
        placeholder="Paste source material, or leave blank to use the model's knowledge.",
    )

    if st.button("🔎 Research"):
        with st.spinner("Researching..."):
            raw = call_gemini(
                "You are a senior research analyst. Return valid JSON only. "
                "Always note uncertainty and never fabricate statistics.",
                f"""Research the topic: "{topic}"
Source material (may be empty): {text}

Return a JSON object with:
"executive_summary": string,
"key_findings": list,
"insights": list,
"recommendations": list,
"limitations": list,
"research_directions": list.""",
            )
        data = extract_json(raw)
        if not data:
            st.error("Parse error. Raw output:")
            st.code(raw)
        else:
            st.subheader("📋 Executive Summary")
            st.write(data.get("executive_summary", ""))

            for section, icon in [
                ("key_findings", "🔑"),
                ("insights", "💡"),
                ("recommendations", "✅"),
                ("limitations", "⚠️"),
                ("research_directions", "🧭"),
            ]:
                st.subheader(f"{icon} {section.replace('_', ' ').title()}")
                for x in data.get(section, []):
                    st.markdown(f"- {x}")

            st.markdown(BIAS_WARNING)


# ==================================================================
# 6. AI WORKPLACE CHATBOT
# ==================================================================
elif module == "💬 AI Workplace Chatbot":
    st.title("💬 AI Workplace Chatbot")
    st.markdown(DISCLAIMER)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your workplace assistant...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        api_key = get_api_key()
        if not api_key:
            reply = "⚠️ No Gemini API key configured."
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name=st.session_state.get("model", "gemini-1.5-flash"),
                    system_instruction=(
                        "You are a professional workplace AI assistant. "
                        "Be concise, accurate and helpful. If unsure, say so. "
                        "Never fabricate facts. Encourage the user to validate "
                        "critical information."
                    ),
                )

                history_text = ""
                for m in st.session_state.chat_history[-10:]:
                    role = "User" if m["role"] == "user" else "Assistant"
                    history_text += f"{role}: {m['content']}\n"

                response = model.generate_content(
                    history_text,
                    generation_config={"temperature": 0.4, "max_output_tokens": 2048},
                )
                reply = (response.text or "").strip()
            except Exception as e:
                reply = f"❌ Error: {e}"

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

    if st.session_state.chat_history:
        st.download_button(
            "⬇️ Export Conversation",
            data="\n\n".join(
                f"**{m['role'].upper()}:** {m['content']}"
                for m in st.session_state.chat_history
            ),
            file_name="chat_history.md",
            mime="text/markdown",
        )

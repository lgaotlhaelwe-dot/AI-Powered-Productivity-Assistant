"""
AI Productivity Assistant
--------------------------
A multi-tool workplace assistant powered by Google Gemini.
Features:
  1. Smart Email Generator
  2. Meeting Notes Summarizer
  3. AI Task Planner / Scheduler
  4. AI Research Assistant
  5. AI Chatbot Interface

Author: Your Name
Date: 2026
"""

import os
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Productivity Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar — API Key & Model
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuration")

# Try to read from environment (useful for deployment)
default_key = os.getenv("GEMINI_API_KEY", "")

api_key = st.sidebar.text_input(
    "Gemini API Key",
    value=default_key,
    type="password",
    help="Get your free key at https://aistudio.google.com/apikey",
)

model_name = st.sidebar.selectbox(
    "Model",
    ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.1-pro-preview"],
    index=0,
)

temperature = st.sidebar.slider(
    "Creativity (temperature)",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Responsible AI Notice**\n\n"
    "AI outputs may contain inaccuracies or biases. "
    "Always review and validate before sending, sharing, or acting on them."
)

# ---------------------------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------------------------
def get_client(api_key: str):
    """Return a Gemini client or None if no key is provided."""
    if not api_key or not api_key.strip():
        return None
    try:
        return genai.Client(api_key=api_key.strip())
    except Exception as e:
        st.error(f"Failed to create Gemini client: {e}")
        return None


def call_gemini(client, prompt: str, system_instruction: str | None = None):
    """Send a prompt to Gemini and return the text response."""
    try:
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=2048,
        )
        if system_instruction:
            config.system_instruction = system_instruction

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config,
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"


# ---------------------------------------------------------------------------
# Page Header
# ---------------------------------------------------------------------------
st.title("🤖 AI Productivity Assistant")
st.caption(
    "Automate emails, summaries, planning, research, and chat — "
    "all in one place. Built with Google Gemini."
)

client = get_client(api_key)

if client is None:
    st.warning("🔑 Please enter your Gemini API key in the sidebar to get started.")
    st.stop()

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_email, tab_notes, tab_planner, tab_research, tab_chat = st.tabs(
    [
        "📧 Smart Email",
        "📝 Meeting Notes",
        "📅 Task Planner",
        "🔍 Research Assistant",
        "💬 Chatbot",
    ]
)

# ===========================================================================
# 1. SMART EMAIL GENERATOR
# ===========================================================================
with tab_email:
    st.subheader("Smart Email Generator")
    st.write("Generate context-aware professional emails with tone and audience control.")

    col1, col2, col3 = st.columns(3)
    with col1:
        audience = st.selectbox(
            "Audience",
            ["Client", "Manager", "Team", "Colleague", "Vendor", "Other"],
        )
    with col2:
        tone = st.selectbox(
            "Tone",
            ["Formal", "Informal", "Persuasive", "Friendly", "Assertive", "Apologetic"],
        )
    with col3:
        length = st.selectbox("Length", ["Short", "Medium", "Detailed"])

    email_context = st.text_area(
        "What is the email about?",
        placeholder=(
            "e.g., Follow up on the project proposal sent last week. "
            "Ask for feedback and suggest a call on Thursday."
        ),
        height=120,
    )

    if st.button("✉️ Generate Email", key="email_btn"):
        if not email_context.strip():
            st.warning("Please describe the email context.")
        else:
            system = (
                "You are an expert business communication assistant. "
                "Write clear, professional emails that match the requested tone, "
                "audience, and length. Include a subject line. "
                "Do not invent facts that were not provided."
            )
            prompt = f"""
Write a professional email.

Audience: {audience}
Tone: {tone}
Length: {length}
Context: {email_context}

Format:
Subject: <subject line>
Body:
<email body>
"""
            with st.spinner("Drafting your email..."):
                result = call_gemini(client, prompt, system)
            st.markdown("### ✉️ Generated Email")
            st.markdown(result)
            st.download_button(
                "📥 Download as .txt",
                data=result,
                file_name="email_draft.txt",
                mime="text/plain",
            )

# ===========================================================================
# 2. MEETING NOTES SUMMARIZER
# ===========================================================================
with tab_notes:
    st.subheader("Meeting Notes Summarizer")
    st.write("Convert lengthy notes into concise summaries with key points and action items.")

    notes = st.text_area(
        "Paste your meeting notes here",
        placeholder=(
            "e.g., Discussed Q3 marketing budget. Sarah will send the revised "
            "spreadsheet by Friday. Tom raised concerns about vendor delays. "
            "Decision: move launch to October 15th."
        ),
        height=250,
    )

    if st.button("📝 Summarize Notes", key="notes_btn"):
        if not notes.strip():
            st.warning("Please paste some meeting notes.")
        else:
            system = (
                "You are a meticulous meeting-notes summarizer. "
                "Extract only information present in the notes. "
                "If something is unclear, say so instead of guessing."
            )
            prompt = f"""
Summarize the following meeting notes.

Provide:
1. **Concise Summary** (3–5 sentences)
2. **Key Points** (bullet list)
3. **Decisions Made** (bullet list)
4. **Action Items** (table with columns: Task | Owner | Deadline)
5. **Deadlines & Responsibilities** (bullet list)

If any category has no items, write "None mentioned."

Meeting Notes:
\"\"\"
{notes}
\"\"\"
"""
            with st.spinner("Summarizing..."):
                result = call_gemini(client, prompt, system)
            st.markdown("### 📝 Summary")
            st.markdown(result)

# ===========================================================================
# 3. AI TASK PLANNER / SCHEDULER
# ===========================================================================
with tab_planner:
    st.subheader("AI Task Planner / Scheduler")
    st.write("Generate a prioritized daily or weekly plan based on your tasks.")

    col1, col2 = st.columns(2)
    with col1:
        plan_type = st.radio("Plan type", ["Daily", "Weekly"], horizontal=True)
    with col2:
        working_hours = st.text_input("Working hours", value="09:00 – 17:00")

    tasks_raw = st.text_area(
        "List your tasks (one per line)",
        placeholder=(
            "Finish quarterly report – due Friday\n"
            "Reply to client emails\n"
            "Prepare slides for Monday stand-up\n"
            "Review pull requests"
        ),
        height=180,
    )

    if st.button("📅 Generate Plan", key="planner_btn"):
        if not tasks_raw.strip():
            st.warning("Please enter at least one task.")
        else:
            system = (
                "You are a productivity coach who uses prioritization frameworks "
                "such as Eisenhower Matrix (urgent/important). "
                "Create realistic, actionable schedules. "
                "Do not assume tasks that were not listed."
            )
            prompt = f"""
Create a {plan_type.lower()} plan.

Working hours: {working_hours}

Tasks:
{tasks_raw}

Provide:
1. **Priority Ranking** (High / Medium / Low) with brief justification
2. **{plan_type} Schedule** (time-blocked)
3. **Time-Optimization Tips** (3–5 tips)
4. **Potential Conflicts or Risks**
"""
            with st.spinner("Building your plan..."):
                result = call_gemini(client, prompt, system)
            st.markdown(f"### 📅 Your {plan_type} Plan")
            st.markdown(result)

# ===========================================================================
# 4. AI RESEARCH ASSISTANT
# ===========================================================================
with tab_research:
    st.subheader("AI Research Assistant")
    st.write("Summarize articles, reports, or topics and extract key insights.")

    research_input = st.text_area(
        "Paste text, article, or topic description",
        placeholder=(
            "Paste an article excerpt or describe a topic you want researched. "
            "e.g., 'Impact of remote work on team productivity in software teams.'"
        ),
        height=250,
    )

    if st.button("🔍 Analyze", key="research_btn"):
        if not research_input.strip():
            st.warning("Please provide some text or a topic.")
        else:
            system = (
                "You are a research analyst. Summarize accurately, "
                "distinguish facts from opinions, and never fabricate sources. "
                "If the input is a topic (not a pasted article), provide a balanced overview "
                "and note that external verification is recommended."
            )
            prompt = f"""
Analyze the following input.

Provide:
1. **Executive Summary** (3–4 sentences)
2. **Key Insights** (bullet list)
3. **Recommendations** (bullet list)
4. **Complex Concepts Simplified** (plain-language explanations)
5. **Limitations / What to Verify** (important caveats)

Input:
\"\"\"
{research_input}
\"\"\"
"""
            with st.spinner("Researching..."):
                result = call_gemini(client, prompt, system)
            st.markdown("### 🔍 Research Summary")
            st.markdown(result)

# ===========================================================================
# 5. AI CHATBOT INTERFACE
# ===========================================================================
with tab_chat:
    st.subheader("AI Chatbot Interface")
    st.write("Ask anything — your workplace assistant is ready.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I'm your AI workplace assistant. "
                    "Ask me to draft something, explain a concept, "
                    "brainstorm ideas, or help with planning."
                ),
            }
        ]

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Build conversation context
        history_text = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages[-10:]  # last 10 turns
        )

        system = (
            "You are a helpful, professional AI workplace assistant. "
            "Be concise, accurate, and practical. "
            "If you are unsure, say so. "
            "Never invent facts, policies, or sources."
        )
        prompt = f"""
Conversation so far:
{history_text}

Respond to the latest user message.
"""

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = call_gemini(client, prompt, system)
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Clear chat button
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared. How can I help you?",
            }
        ]
        st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Built for the AI Skill Accelerator Programme · "
    "Powered by Google Gemini · "
    "Always validate AI outputs before professional use."
)

import re
import streamlit as st 
import streamlit.components.v1 as components
from crewai import Agent, Task, Crew, Process, LLM

# ────────────────────────────────────────────────────────
# STREAMLIT UI CONFIGURATION & SESSION STATE
# ────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Agent Storefront", page_icon="🚀", layout="centered")

# Initialize API Key in Session State to empty string if it doesn't exist yet
if "saved_api_key" not in st.session_state:
    st.session_state["saved_api_key"] = ""

# Visual Title & Branding
st.title("🤖 Multi-Agent Content Engine")
st.write("Stop wasting hours writing social copy. Let a specialized agent crew instantly transform any topic into high-performing content for X, LinkedIn, and Instagram.")

st.markdown("---")

# ────────────────────────────────────────────────────────
# SIDEBAR AUTHENTICATION SETUP (PURE USER ENTRY)
# ────────────────────────────────────────────────────────
st.sidebar.header("🔑 Authentication Setup")

# Input field binds directly to st.session_state["saved_api_key"] via the 'key' argument
api_key_input = st.sidebar.text_input(
    label="Enter Your Gemini API Key:",
    placeholder="AIzaSy...",
    type="password",
    key="saved_api_key",
    help="Get a free key from Google AI Studio. It will be securely stored for this session."
)

# Visual status indicator for the user
if st.session_state["saved_api_key"].strip():
    st.sidebar.success("🔒 API Key Loaded & Active")
else:
    st.sidebar.warning("⚠️ API Key Required to Launch")


# ────────────────────────────────────────────────────────
# USER INPUT CONFIGURATION
# ────────────────────────────────────────────────────────
st.subheader("🔮 Campaign Configuration")
user_topic = st.text_area(
    label="What topic or link do you want your agent crew to generate copy for?",
    placeholder="e.g., Why building open-source software is the best way to land a tech job in 2026...",
    height=100
)

st.caption("💡 Tier Feature: Standard access uses optimized cloud routing (Gemini 3.1 Flash Lite).")


# ────────────────────────────────────────────────────────
# CREWAI BACKEND ORCHESTRATION PIPELINE
# ────────────────────────────────────────────────────────
def run_marketing_agent(topic_input, user_key):
    # Instantiate the LLM engine dynamically using the user's provided key
    llm = LLM(
        model="gemini/gemini-3.1-flash-lite",  
        temperature=0.7,
        api_key=user_key
    )

    # Define Agents
    researcher = Agent(
        role='Lead Content Researcher',
        goal='Accurately extract key facts, statistics, and core insights from raw text or topics.',
        backstory="""You are an elite research analyst. Your job is to deliver structured summaries. 
        CRITICAL: Focus ONLY on the current topic provided. Do not assume or inject artificial intelligence, 
        software engineering, or tech industry concepts unless the topic explicitly asks for it.""",
        llm=llm
    )

    writer = Agent(
        role='Social Media Copywriter',
        goal='Transform research summaries into highly engaging, viral platform-specific posts.',
        backstory="""You are a master digital marketer who knows exactly how to capture attention on X, LinkedIn, and Instagram.
        CRITICAL: Match the tone and domain of the topic perfectly. If the topic is about food, hospitality, or local retail, 
        do not write about AI, coding, or tech optimization. Keep it grounded in the actual industry of the prompt.""",
        llm=llm
    )

    editor = Agent(
        role='Chief Brand Editor',
        goal='Ensure all generated copy is polished, typo-free, and aligned with professional standards.',
        backstory="""You are a meticulous editor with an eagle eye for detail, sentence flow, and formatting.
        CRITICAL: Check for context bleeding. Strip out any repetitive tech jargon or AI patterns if the topic 
        is a non-technical business (like an ice cream shop). Ensure the copy sounds natural for its target industry.""",
        llm=llm
    )

    task_research = Task(
        description=f"Analyze the following input or topic: '{topic_input}'. Extract the top 3 key takeaways and target audience.",
        expected_output="A clean, bulleted summary of key facts.",
        agent=researcher
    )

    task_write = Task(
        description="Take the researcher's summary and generate: 1) A thread for X, 2) A high-value post for LinkedIn, and 3) A caption for Instagram.",
        expected_output="Draft copy for X, LinkedIn, and Instagram separated clearly by headers.",
        agent=writer
    )

    task_edit = Task(
        description="Review the generated platform drafts. Improve sentence flow and ensure clean readability with appropriate line breaks.",
        expected_output="The final output must be partitioned cleanly with explicit markers like this:\n"
                    "[TWITTER]\n(Twitter thread content here)\n\n"
                    "[LINKEDIN]\n(LinkedIn post content here)\n\n"
                    "[INSTAGRAM]\nIMAGE SUGGESTION: (Describe the visual/graphic idea here)\nCAPTION: (Instagram caption text here)",
        agent=editor
    )

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[task_research, task_write, task_edit],
        process=Process.sequential,
        max_rpm=12,
        verbose=False
    )
    
    return crew.kickoff()


# ────────────────────────────────────────────────────────
# ACTION BUTTON EXECUTION TRIGGER
# ────────────────────────────────────────────────────────
if st.button("Launch Agent Crew 🚀", type="primary"):
    # Reference the session state key directly for safety checks
    active_key = st.session_state["saved_api_key"].strip()
    
    if not active_key:
        st.sidebar.error("❌ Missing API Key! Provide an API Key to execute campaigns.")
    elif not user_topic.strip():
        st.warning("Please provide a topic or text input first!")
    else:
        with st.spinner("Agents are collaborating... (Step 1: Researching 🔍 -> Step 2: Drafting ✍️ -> Step 3: Editing 🧼)"):
            try:
                # Run the backend agent script with the session-saved key
                final_output = run_marketing_agent(user_topic, active_key)
                result_string = str(final_output)
                
                # --- CASE-INSENSITIVE ROBUST REGEX PARSING LOGIC ---
                x_content = result_string
                linkedin_content = result_string
                instagram_content = result_string
                
                has_twitter = re.search(r'\[TWITTER\]', result_string, re.IGNORECASE)
                has_linkedin = re.search(r'\[LINKEDIN\]', result_string, re.IGNORECASE)
                has_instagram = re.search(r'\[INSTAGRAM\]', result_string, re.IGNORECASE)
                
                if has_twitter and has_linkedin and has_instagram:
                    try:
                        parts_x = re.split(r'\[TWITTER\]', result_string, flags=re.IGNORECASE)[1]
                        parts_x_split = re.split(r'\[LINKEDIN\]', parts_x, flags=re.IGNORECASE)
                        x_content = parts_x_split[0].strip()
                        
                        parts_li_split = re.split(r'\[INSTAGRAM\]', parts_x_split[1], flags=re.IGNORECASE)
                        linkedin_content = parts_li_split[0].strip()
                        instagram_content = parts_li_split[1].strip()
                    except Exception:
                        pass
                # ----------------───────────────────────────────────

                st.success("✨ Campaign Generated Successfully!")
                st.balloons()
                
                st.markdown("## 📢 Your Polished Marketing Campaign")
                st.caption("Your multi-agent crew has segmented your content. Select a tab below to copy platform-optimized copy:")

                # Create interactive tabs for clean categorization
                tab_x, tab_linkedin, tab_instagram = st.tabs(["𝕏 Twitter Thread", "💼 LinkedIn Post", "📸 Instagram Copy"])

                with tab_x:
                    st.markdown(
                        """
                        <div style="background-color: #1a1a1a; padding: 15px; border-radius: 8px; border-left: 5px solid #ffffff; color: #ffffff; margin-bottom: 15px;">
                            <h4 style="color: #ffffff; margin-top: 0; margin-bottom: 5px;">𝕏 Twitter Thread</h4>
                            <p style="color: #aaaaaa; font-size: 0.85rem; margin: 0;">Isolated thread updates optimized with engagement hooks.</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    st.code(x_content, language="text", wrap_lines=True)
                    st.info("💡 Pro-Tip: Space out your thread updates by 2 minutes for optimal algorithmic reach.")

                with tab_linkedin:
                    st.markdown(
                        """
                        <div style="background-color: #f3f6f8; padding: 15px; border-radius: 8px; border-left: 5px solid #0077b5; color: #1d2226; margin-bottom: 15px;">
                            <h4 style="color: #0077b5; margin-top: 0; margin-bottom: 5px;">💼 LinkedIn Professional Post</h4>
                            <p style="color: #5e5e5e; font-size: 0.85rem; margin: 0;">Structured with white-space scannability and authority building metrics.</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    st.code(linkedin_content, language="text", wrap_lines=True)
                    
                with tab_instagram:
                    st.markdown(
                        """
                        <div style="background-color: #fff5f6; padding: 15px; border-radius: 8px; border-left: 5px solid #e1306c; color: #262626; margin-bottom: 15px;">
                            <h4 style="color: #e1306c; margin-top: 0; margin-bottom: 5px;">📸 Instagram Asset Suite</h4>
                            <p style="color: #737373; font-size: 0.85rem; margin: 0;">Isolated visual spacing copy packaged with high-traffic tag arrays.</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    insta_image = f"A creative, high-converting social graphic highlighting the core concepts of: '{user_topic}'"
                    insta_caption = instagram_content
                    
                    if re.search(r'IMAGE', instagram_content, re.IGNORECASE) and re.search(r'CAPTION:', instagram_content, re.IGNORECASE):
                        try:
                            if re.search(r'IMAGE SUGGESTION:', instagram_content, re.IGNORECASE):
                                parts_insta = re.split(r'IMAGE SUGGESTION:', instagram_content, flags=re.IGNORECASE)[1]
                            else:
                                parts_insta = re.split(r'IMAGE:', instagram_content, flags=re.IGNORECASE)[1]
                                
                            parts_insta_split = re.split(r'CAPTION:', parts_insta, flags=re.IGNORECASE)
                            insta_image = parts_insta_split[0].strip()
                            insta_caption = parts_insta_split[1].strip()
                        except Exception:
                            pass
                    
                    # 1. Image Suggestion Component Box
                    st.markdown("##### 🎨 Creative Design Direction")
                    st.code(insta_image, language="text", wrap_lines=True)
                    
                    st.write("") 
                    
                    # 2. Caption Component Box
                    st.markdown("##### 📝 Optimized Caption & Tags")
                    st.code(insta_caption, language="text", wrap_lines=True)
                
            except Exception as e:
                st.error(f"An unexpected server exception occurred: {e}")
                
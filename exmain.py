import os
import streamlit as st 
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load variables
load_dotenv()

# Configure the Gemini Flash Engine
llm = LLM(
    model="gemini/gemini-3.1-flash-lite",  
    temperature=0.7,
    api_key=os.environ.get("GEMINI_API_KEY")
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

def run_marketing_agent(topic_input):
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
# STREAMLIT UI CODE (Your Storefront Layout)
# ────────────────────────────────────────────────────────

# Set webpage properties
st.set_page_config(page_title="AI Agent Storefront", page_icon="🚀", layout="centered")

# Visual Title & Branding
st.title("🤖 Multi-Agent Content Engine")
st.write("Stop wasting hours writing social copy. Let an specialized agent crew instantly transform any topic into high-performing content for X, LinkedIn, and Instagram.")

st.markdown("---")

# User Inputs Section
st.subheader("🔮 Campaign Configuration")
user_topic = st.text_area(
    label="What topic or link do you want your agent crew to generate copy for?",
    placeholder="e.g., Why building open-source software is the best way to land a tech job in 2026...",
    height=100
)

# Pricing/Value Tier simulation for your customers
st.caption("💡 Tier Feature: Standard access uses optimized cloud routing (Gemini 3.1 Flash Lite).")

# Center Action Button
if st.button("Launch Agent Crew 🚀", type="primary"):
    if not user_topic.strip():
        st.warning("Please provide a topic or text input first!")
    else:
        with st.spinner("Agents are collaborating... (Step 1: Researching 🔍 -> Step 2: Drafting ✍️ -> Step 3: Editing 🧼)"):
            try:
                # Run the backend agent script
                final_output = run_marketing_agent(user_topic)
                result_string = str(final_output)
                
                # --- SMART PARSING LOGIC ---
                # Default fallbacks if parsing fails
                x_content = result_string
                linkedin_content = result_string
                instagram_content = result_string
                
                # Split text by markers if they exist
                if "[TWITTER]" in result_string and "[LINKEDIN]" in result_string and "[INSTAGRAM]" in result_string:
                    try:
                        parts_x = result_string.split("[TWITTER]")[1].split("[LINKEDIN]")
                        x_content = parts_x[0].strip()
                        
                        parts_li = parts_x[1].split("[INSTAGRAM]")
                        linkedin_content = parts_li[0].strip()
                        instagram_content = parts_li[1].strip()
                    except Exception:
                        # Fallback to full string if index splitting encounters a formatting anomaly
                        pass
                # ----------------------------

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
                            <p style="color: #5e5e5e; font-size: 0.85rem; margin: 0;">Isolated authority copy built for high scannability links.</p>
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
                    
                    # 💡 DYNAMIC FIX: Fallbacks now adapt to the user's specific input topic!
                    insta_image = f"A creative, high-converting social graphic highlighting the core concepts of: '{user_topic}'"
                    insta_caption = instagram_content
                    
                    # More robust parsing that handles case-insensitive generation
                    upper_content = instagram_content.upper()
                    if "IMAGE" in upper_content and "CAPTION:" in instagram_content:
                        try:
                            # Split dynamically based on whatever the agent returned
                            if "IMAGE SUGGESTION:" in instagram_content:
                                parts_insta = instagram_content.split("IMAGE SUGGESTION:")[1].split("CAPTION:")
                            else:
                                parts_insta = instagram_content.split("IMAGE:")[1].split("CAPTION:")
                                
                            insta_image = parts_insta[0].strip()
                            insta_caption = parts_insta[1].strip()
                        except Exception:
                            pass
                    
                    # 1. Image Suggestion Component Box
                    st.markdown("##### 🎨 Creative Design Direction")
                    st.code(insta_image, language="text", wrap_lines=True)
                    
                    st.write("") # Layout spacer
                    
                    # 2. Caption Component Box
                    st.markdown("##### 📝 Optimized Caption & Tags")
                    st.code(insta_caption, language="text", wrap_lines=True)
                
            except Exception as e:
                st.error(f"An unexpected server exception occurred: {e}")
                
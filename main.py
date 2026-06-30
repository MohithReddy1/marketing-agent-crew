import os
import streamlit as st 
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load variables
load_dotenv()

# Configure the Gemini Flash Engine
llm = LLM(
    model="gemini/gemini-2.5-flash",  
    temperature=0.7,
    api_key=os.environ.get("GEMINI_API_KEY")
)

# Define Agents
researcher = Agent(
    role='Lead Content Researcher',
    goal='Accurately extract key facts, statistics, and core insights from raw text or topics.',
    backstory="You are an elite research analyst. Your job is to deliver structured summaries.",
    llm=llm
)

writer = Agent(
    role='Social Media Copywriter',
    goal='Transform research summaries into highly engaging, viral platform-specific posts.',
    backstory="You are a master digital marketer who knows exactly how to capture attention on X, LinkedIn, and Instagram.",
    llm=llm
)

editor = Agent(
    role='Chief Brand Editor',
    goal='Ensure all generated copy is polished, typo-free, and aligned with professional standards.',
    backstory="You are a meticulous editor with an eagle eye for detail, sentence flow, and formatting.",
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
        expected_output="The finalized, production-ready marketing copy for all three social channels.",
        agent=editor
    )

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[task_research, task_write, task_edit],
        process=Process.sequential,
        verbose=True
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
st.caption("💡 Tier Feature: Standard access uses optimized cloud routing (Gemini 2.5 Flash).")

# Center Action Button
if st.button("Launch Agent Crew 🚀", type="primary"):
    if not user_topic.strip():
        st.warning("Please provide a topic or text input first!")
    else:
        # Show a clean loading state to your customer while agents work in background
        with st.spinner("Agents are collaborating... (Step 1: Researching 🔍 -> Step 2: Drafting ✍️ -> Step 3: Editing 🧼)"):
            try:
                # Run the backend agent script
                final_output = run_marketing_agent(user_topic)
                
                # Success display layout
                st.success("✨ Campaign Generated Successfully!")
                st.balloons()
                
                st.markdown("### 📢 Your Polished Marketing Campaign")
                # Render the final output inside a structured text container safely using str()
                st.text_area(label="Copy-paste ready results:", value=str(final_output), height=450)
                
            except Exception as e:
                st.error(f"An unexpected server exception occurred: {e}")
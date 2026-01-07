import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="The Ruthless_Advocate", page_icon="💀")

# 2. The Title and Description
st.title("💀 The Ruthless_Advocate")
st.write("""
**Optimism bias is the enemy.** Paste your business idea, travel plan, or decision below. 
I will assume it has already failed and tell you exactly why.
""")

# 3. Securely access the API Key
# Note: We will name the secret "GROQ_API_KEY" in the next step
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except FileNotFoundError:
    st.error("API Key not found. Please set your secrets in Streamlit.")
    st.stop()

# 4. Input Area
user_plan = st.text_area("Describe your plan:", height=150, placeholder="Example: I'm quitting my job to sell coffee on the beach...")

# 5. The "Destroy" Button
if st.button("Destroy My Plan"):
    if not user_plan:
        st.warning("Please enter a plan first. I can't destroy nothingness.")
    else:
        with st.spinner("Analyzing failure points..."):
            try:
                # 6. The API Call (Sending the prompt to Groq)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": """You are the 'Chief Pessimist' and a Senior Risk Analyst. 
                            You are skeptical, strictly logical, and immune to hype. 
                            
                            ### THE TASK ###
                            1. Assume we are 1 year in the future.
                            2. Assume the plan has ALREADY failed catastrophically.
                            3. Perform a "Pre-Mortem" analysis to explain the failure.

                            ### CONSTRAINTS ###
                            - Do not use phrases like "You might want to consider" or "There is a risk of."
                            - Use definitive language: "This failed because..."
                            - Focus on "Silent Killers"—boring details (logistics, regulations, fatigue).

                            ### OUTPUT FORMAT ###
                            Provide the analysis in this specific structure:
                            💀 The Cause of Death: [The single biggest reason the plan failed]
                            1. The Logic Gap: [Where the user's reasoning was flawed]
                            2. The Resource Trap: [Where time/money was underestimated]
                            3. The Blind Spot: [An external factor the user ignored]
                            🩹 The Pivot: [1 harsh but constructive suggestion to prevent this]
                            """
                        },
                        {
                            "role": "user",
                            "content": user_plan,
                        }
                    ],
                    # We use Llama-3 70B because it is smart and free on Groq
                    model="llama3-70b-8192", 
                    temperature=0.6,
                )

                # 7. Display the Result
                analysis = chat_completion.choices[0].message.content
                st.success("Analysis Complete.")
                st.markdown(analysis)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

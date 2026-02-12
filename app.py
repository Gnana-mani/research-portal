import streamlit as st
import os
from openai import OpenAI
import json
from datetime import datetime

# Page configuration
st.set_page_config(page_title="AI Research Portal", layout="wide")
st.title("🔬 AI Research Portal")
st.write("Upload an Earnings Call Transcript for AI-powered research analysis")

# Sidebar for API key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password", key="api_key")

if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to proceed")
    st.info("""
    Don't have an API key? Get one free:
    1. Go to https://platform.openai.com/api-keys
    2. Sign up (free account)
    3. Create an API key
    4. Paste it in the sidebar
    """)
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# File uploader
uploaded_file = st.file_uploader("Upload an Earnings Call Transcript", type=["pdf", "txt"])

if uploaded_file is not None:
    # Read file content
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    else:
        st.error("Please upload a .txt file (PDF support coming soon)")
        st.stop()
    
    st.success(f"✓ File uploaded: {uploaded_file.name}")
    
    # Show file preview
    with st.expander("📄 View transcript preview"):
        st.text(content[:500] + "..." if len(content) > 500 else content)
    
    # Analyze button
    if st.button("🚀 Analyze Earnings Call", type="primary"):
        with st.spinner("Analyzing transcript with AI..."):
            try:
                # AI analysis prompt
                analysis_prompt = f"""Analyze the following earnings call transcript and provide a structured research summary.

TRANSCRIPT:
{content}

Please provide your analysis in the following JSON format:
{{
    "management_tone": "optimistic/cautious/neutral/pessimistic",
    "confidence_level": "high/medium/low",
    "tone_reasoning": "Brief explanation of the tone assessment",
    "key_positives": [
        "Key positive point 1",
        "Key positive point 2",
        "Key positive point 3"
    ],
    "key_concerns": [
        "Key concern 1",
        "Key concern 2",
        "Key concern 3"
    ],
    "forward_guidance": {{
        "revenue_outlook": "Description or percentage guidance if available",
        "margin_outlook": "Description or percentage guidance if available",
        "capex_outlook": "Description or amount if available"
    }},
    "capacity_utilization": "Description of any capacity/utilization trends mentioned",
    "growth_initiatives": [
        "New growth initiative 1",
        "New growth initiative 2",
        "New growth initiative 3"
    ],
    "data_completeness": "Note any sections that were missing or unclear",
    "key_quotes": [
        {{"quote": "Important management quote", "context": "What this relates to"}},
        {{"quote": "Another important quote", "context": "Context"}}
    ]
}}

Be concise, accurate, and only include information explicitly stated in the transcript. Do not hallucinate information."""

                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert financial analyst. Provide structured, accurate analysis without hallucination."},
                        {"role": "user", "content": analysis_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                
                # Parse response
                analysis_text = response.choices[0].message.content
                
                # Try to extract JSON
                try:
                    # Find JSON in response
                    start_idx = analysis_text.find('{')
                    end_idx = analysis_text.rfind('}') + 1
                    json_str = analysis_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                except:
                    st.error("Could not parse AI response. Try again.")
                    st.text(analysis_text)
                    st.stop()
                
                # Display results
                st.markdown("---")
                st.header("📊 Research Analysis Results")
                
                # Tone section
                col1, col2 = st.columns(2)
                with col1:
                    tone_emoji = {"optimistic": "📈", "cautious": "⚠️", "neutral": "➡️", "pessimistic": "📉"}
                    tone = analysis.get("management_tone", "N/A").lower()
                    st.metric("Management Tone", f"{tone_emoji.get(tone, '•')} {analysis.get('management_tone', 'N/A')}")
                
                with col2:
                    confidence = analysis.get("confidence_level", "N/A")
                    st.metric("Confidence Level", confidence.upper())
                
                st.info(analysis.get("tone_reasoning", "No reasoning provided"))
                
                # Key Positives
                st.subheader("✅ Key Positives")
                for i, positive in enumerate(analysis.get("key_positives", []), 1):
                    st.write(f"{i}. {positive}")
                
                # Key Concerns
                st.subheader("⚠️ Key Concerns")
                for i, concern in enumerate(analysis.get("key_concerns", []), 1):
                    st.write(f"{i}. {concern}")
                
                # Forward Guidance
                st.subheader("🎯 Forward Guidance")
                guidance = analysis.get("forward_guidance", {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Revenue Outlook:**")
                    st.write(guidance.get("revenue_outlook", "Not specified"))
                with col2:
                    st.write("**Margin Outlook:**")
                    st.write(guidance.get("margin_outlook", "Not specified"))
                with col3:
                    st.write("**Capex Outlook:**")
                    st.write(guidance.get("capex_outlook", "Not specified"))
                
                # Capacity Utilization
                if analysis.get("capacity_utilization"):
                    st.subheader("📦 Capacity Utilization Trends")
                    st.write(analysis.get("capacity_utilization"))
                
                # Growth Initiatives
                st.subheader("🚀 Growth Initiatives")
                for i, initiative in enumerate(analysis.get("growth_initiatives", []), 1):
                    st.write(f"{i}. {initiative}")
                
                # Key Quotes
                if analysis.get("key_quotes"):
                    st.subheader("💬 Key Management Quotes")
                    for item in analysis.get("key_quotes", []):
                        st.quote(f'"{item.get("quote", "")}"')
                        st.caption(f"➜ {item.get('context', '')}")
                
                # Data Completeness Note
                if analysis.get("data_completeness"):
                    st.warning(f"📌 Note: {analysis.get('data_completeness')}")
                
                # Download results as JSON
                st.markdown("---")
                json_str = json.dumps(analysis, indent=2)
                st.download_button(
                    label="📥 Download Analysis as JSON",
                    data=json_str,
                    file_name=f"earnings_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                if "API key" in str(e):
                    st.warning("Please check your OpenAI API key is valid")

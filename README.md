# 🔬 AI Research Portal

An internal research tool that uses AI to analyze earnings call transcripts and produce structured research outputs.

## Features

- **Earnings Call Analysis**: Upload earnings call transcripts and get AI-powered analysis including:
  - Management tone (optimistic/cautious/neutral/pessimistic)
  - Confidence level assessment
  - Key positives and concerns
  - Forward guidance (revenue, margin, capex outlook)
  - Capacity utilization trends
  - Growth initiatives
  - Key management quotes
  - JSON export for further analysis

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5-turbo
- **Language**: Python 3.8+

## Local Setup

### 1. Prerequisites
- Python 3.8 or higher
- OpenAI API key (get one free at https://platform.openai.com/api-keys)

### 2. Install Dependencies

```bash
cd research_portal
pip install -r requirements.txt
```

### 3. Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### 4. Using the Portal

1. Paste your OpenAI API key in the sidebar
2. Upload a .txt file containing an earnings call transcript
3. Click "Analyze Earnings Call"
4. Review the structured analysis
5. Download results as JSON if needed

## Deployment (Free Options)

### Option 1: Deploy to Render (Recommended)

1. Push your code to GitHub
2. Create account at https://render.com
3. Connect GitHub repository
4. Create new "Web Service"
5. Set environment variables:
   - `STREAMLIT_SERVER_PORT=10000`
   - `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
   - `STREAMLIT_SERVER_HEADLESS=true`
6. Deploy!

### Option 2: Deploy to Heroku

1. Create account at https://www.heroku.com
2. Install Heroku CLI
3. Create `Procfile`:
   ```
   web: streamlit run app.py --logger.level=error
   ```
4. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```
5. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set STREAMLIT_SERVER_PORT=10000
   git push heroku main
   ```

### Option 3: Deploy to Vercel/Netlify (with backend)

For Vercel, you'll need a backend API. Create a simple FastAPI endpoint:

```python
# Deploy as serverless function
from fastapi import FastAPI

app = FastAPI()

@app.post("/analyze")
async def analyze(transcript: str, api_key: str):
    # Your analysis logic here
    pass
```

## Sample Earnings Call Transcript

Create a test file `sample_transcript.txt`:

```
EARNINGS CALL TRANSCRIPT

Q3 2024 Earnings Call

Operator: Good day, and thank you for standing by and welcome to the Q3 2024 Earnings Call...

CEO: Thank you for the introduction. We're pleased to report strong Q3 results with revenue of $5.2B, 
up 12% year-over-year. Our margins improved to 28%, reflecting operational efficiency gains...

Key Points:
- Revenue guidance for Q4: $5.5-5.7B (growth of 10-15%)
- Margin expansion expected (30-31%)
- CapEx investment of $800M planned
- New product launches driving growth
- Market conditions remain challenging but outlook is cautiously optimistic
```

## Limitations

- **Free OpenAI API**: Limited to ~3-5 analyses per minute with free tier
- **File Size**: Max 100MB per file (Streamlit limitation)
- **Supported Formats**: Currently .txt files only (PDF support coming)
- **Accuracy**: Depends on transcript quality and LLM capabilities

## Key Implementation Decisions

1. **No Hallucination**: Prompt explicitly tells LLM to only extract information present in transcript
2. **Structured JSON Output**: Makes results machine-readable and analyzable
3. **Confidence Levels**: Human judgment about tone is probabilistic, not deterministic
4. **Missing Data Handling**: Explicitly notes when sections are incomplete
5. **Temperature=0.3**: Low temperature ensures consistent, factual responses

## Troubleshooting

### "API key invalid"
- Verify your OpenAI API key is correct
- Check that your account has available credits

### "Could not parse AI response"
- The LLM response format was unexpected
- Try a different transcript or verify the API is working

### "File upload failed"
- Ensure file is in .txt format
- Check file is <100MB

## Future Enhancements

1. PDF support with better text extraction
2. Multiple file uploads in one session
3. Comparative analysis across multiple transcripts
4. Export to Excel/CSV formats
5. Support for other LLMs (Claude, Llama)
6. Real-time metrics dashboard

## Support

For issues or questions, check:
1. OpenAI API status: https://status.openai.com
2. Streamlit documentation: https://docs.streamlit.io
3. Review transcript format (ensure it's plain text)

---

**Note**: This is a research tool prototype. Always validate AI-generated insights with human analysis before making financial decisions.

# Multi-Agent Travel Planner System

A sophisticated AI-powered travel planning system built with LangChain, LangGraph, and multiple LLM providers (Gemini, OpenAI, OpenRouter).

## 🌟 Features

- **4 Specialized AI Agents** working collaboratively:
  - 🗺️ **DestinationResearchAgent**: Researches destinations, weather, visa requirements, and local tips
  - 🗓️ **ItineraryPlannerAgent**: Creates detailed day-by-day itineraries
  - 💰 **BudgetEstimatorAgent**: Provides realistic cost estimates across budget tiers
  - 📋 **TravelSummaryAgent**: Compiles everything into a polished travel guide

- **Multi-LLM Support**: 
  - Google Gemini (gemini-2.0-flash)
  - OpenAI (gpt-4o-mini)
  - OpenRouter (openai/gpt-4o-mini)

- **Smart Rate Limiting**: Automatic retry logic with exponential backoff for API rate limits

- **Interactive CLI**: User-friendly command-line interface for input

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- API key for one of: Gemini, OpenAI, or OpenRouter

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your API keys:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# GEMINI_API_KEY=your-gemini-api-key-here
# OPENROUTER_API_KEY=your-openrouter-api-key-here
# OPENAI_API_KEY=your-openai-api-key-here
```

5. Choose your LLM provider in `multi_agent_system.py`:
```python
# For OpenRouter (default)
USE_OPENROUTER = True
USE_OPENAI = False

# For OpenAI
USE_OPENROUTER = False
USE_OPENAI = True

# For Gemini
USE_OPENROUTER = False
USE_OPENAI = False
```

### Usage

Run the travel planner:
```bash
python multi_agent_system.py
```

You'll be prompted to enter:
- Destination (e.g., "Tokyo, Japan")
- Duration (e.g., "7")
- Number of travelers (e.g., "2")
- Interests (e.g., "culture, food, adventure")
- Budget preference (budget / mid-range / luxury)

The system will generate a comprehensive travel plan and optionally save it to `travel_plan.txt`.

## 📋 Example Output

The system generates:
- **Trip Overview**: Summary of your travel preferences
- **Destination Insights**: Key attractions, weather, visa requirements, safety tips
- **Day-by-Day Itinerary**: Detailed activities for each day with timing and recommendations
- **Budget Breakdown**: Itemized costs for flights, accommodation, food, activities, transport
- **Pro Tips**: Practical advice for your trip

## 🏗️ Architecture

```
START
  ↓
DestinationResearchAgent (researches destination)
  ↓
ItineraryPlannerAgent (creates itinerary)
  ↓
BudgetEstimatorAgent (estimates costs)
  ↓
TravelSummaryAgent (compiles final plan)
  ↓
END
```

Built with **LangGraph** for orchestrating the multi-agent workflow with shared state management.

## 🛠️ Technical Details

- **Framework**: LangChain + LangGraph
- **State Management**: TypedDict with message history
- **Error Handling**: Exponential backoff retry logic for rate limits
- **Rate Limiting**: 20-second delays between agent calls
- **Max Retries**: 5 attempts with smart delay extraction from error messages

## 📝 Configuration

### API Keys

All API keys are stored securely in the `.env` file (which is git-ignored). Never commit your `.env` file!

1. Copy `.env.example` to `.env`
2. Add your API keys to `.env`
3. The application will automatically load them

### Switching LLM Providers

Edit the flags in `multi_agent_system.py`:

```python
USE_OPENROUTER = True   # For OpenRouter
USE_OPENAI = False      # For OpenAI
# Leave both False for Gemini
```

### Adjusting Rate Limits

Modify the delays in agent functions:
```python
time.sleep(20)  # Adjust delay between agents (in seconds)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Rate Limit Errors
- The system automatically retries with exponential backoff
- If Gemini quota is exhausted, switch to OpenRouter or OpenAI
- Free tier quotas reset daily

### API Key Issues
- Ensure API keys are correctly set in `.env` file
- Never commit the `.env` file to version control
- Use `.env.example` as a template
- Verify the correct provider flag is set in `multi_agent_system.py`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment before running

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Happy Travels! ✈️🌍**

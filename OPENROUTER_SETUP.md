# 🔑 OpenRouter API Setup Guide

This project uses **OpenRouter** to access Claude AI and other language models. OpenRouter provides a unified API for multiple AI providers.

---

## 🌟 Why OpenRouter?

- ✅ **Access Multiple Models**: Claude, GPT-4, Llama, and more
- ✅ **Competitive Pricing**: Often cheaper than direct API access
- ✅ **Unified API**: One API key for all models
- ✅ **Fallback Support**: Automatic fallback to alternative models
- ✅ **No Vendor Lock-in**: Easy to switch between models

---

## 📝 Getting Your API Key

### Step 1: Create Account
1. Go to https://openrouter.ai/
2. Click **"Sign In"** or **"Get Started"**
3. Sign up with Google, GitHub, or email

### Step 2: Add Credits
1. Go to https://openrouter.ai/credits
2. Add credits to your account (minimum $5)
3. OpenRouter uses pay-as-you-go pricing

### Step 3: Get API Key
1. Go to https://openrouter.ai/keys
2. Click **"Create Key"**
3. Give it a name (e.g., "Voice AI Assistant")
4. Copy the API key (starts with `sk-or-v1-...`)

---

## 🔧 Configuration

### Option 1: Environment Variable (Recommended)

**Windows PowerShell:**
```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

**Windows CMD:**
```cmd
set OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### Option 2: .env File (Persistent)

Create or edit `backend/.env`:
```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
PORT=5000
FLASK_ENV=development
```

---

## 🤖 Available Models

The project is configured to use **Claude 3.5 Sonnet** by default, but you can easily switch to other models.

### Current Model
```python
# In backend/agent.py
self.model = "anthropic/claude-3.5-sonnet"
```

### Other Available Models

**Claude Models:**
- `anthropic/claude-3.5-sonnet` - Best balance (default)
- `anthropic/claude-3-opus` - Most capable
- `anthropic/claude-3-haiku` - Fastest and cheapest

**OpenAI Models:**
- `openai/gpt-4-turbo` - Very capable
- `openai/gpt-4` - Reliable
- `openai/gpt-3.5-turbo` - Fast and cheap

**Other Models:**
- `meta-llama/llama-3-70b-instruct` - Open source
- `google/gemini-pro` - Google's model
- `mistralai/mistral-large` - European alternative

### Changing the Model

Edit `backend/agent.py`:
```python
class ToDoAgent:
    def __init__(self, memory_store: MemoryStore, todo_manager: ToDoManager):
        # ... other code ...
        self.model = "openai/gpt-4-turbo"  # Change this line
```

---

## 💰 Pricing

OpenRouter pricing varies by model. Check current prices at:
https://openrouter.ai/models

**Example Pricing (as of 2024):**
- Claude 3.5 Sonnet: ~$3 per million input tokens
- GPT-4 Turbo: ~$10 per million input tokens
- GPT-3.5 Turbo: ~$0.50 per million input tokens

**Typical Usage:**
- Average conversation: 1,000-5,000 tokens
- Cost per conversation: $0.003-$0.015 (Claude 3.5)
- $5 credit = ~300-1,500 conversations

---

## 🔒 Security Best Practices

### ✅ DO:
- Store API key in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables
- Rotate keys periodically
- Monitor usage on OpenRouter dashboard

### ❌ DON'T:
- Commit API keys to git
- Share API keys publicly
- Hardcode keys in source code
- Use same key for multiple projects
- Leave unused keys active

---

## 🧪 Testing Your Setup

### Test 1: Check Environment Variable
```bash
# PowerShell
echo $env:OPENROUTER_API_KEY

# Linux/Mac
echo $OPENROUTER_API_KEY
```

Should output your API key (starting with `sk-or-v1-`)

### Test 2: Test API Connection
```bash
cd backend
python -c "
from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')
print(f'API Key loaded: {api_key[:20]}...')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'anthropic/claude-3.5-sonnet',
    'messages': [{'role': 'user', 'content': 'Say hello'}],
    'max_tokens': 50
}

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers=headers,
    json=payload
)

print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
"
```

### Test 3: Start Backend
```bash
cd backend
python api.py
```

Should see:
```
INFO:root:OpenRouter API key loaded successfully
* Running on http://0.0.0.0:5000
```

---

## 🐛 Troubleshooting

### Issue: "OPENROUTER_API_KEY not set"

**Solution:**
1. Check `.env` file exists in `backend/` folder
2. Verify key is correct format: `OPENROUTER_API_KEY=sk-or-v1-...`
3. Restart backend server after setting key

### Issue: "401 Unauthorized"

**Causes:**
- Invalid API key
- Expired API key
- Insufficient credits

**Solution:**
1. Verify API key at https://openrouter.ai/keys
2. Check credits at https://openrouter.ai/credits
3. Generate new key if needed

### Issue: "429 Rate Limit"

**Solution:**
- Wait a few seconds between requests
- Upgrade to higher tier if needed
- Check usage at https://openrouter.ai/activity

### Issue: "Model not found"

**Solution:**
- Check model name is correct
- Verify model is available at https://openrouter.ai/models
- Some models require special access

---

## 📊 Monitoring Usage

### OpenRouter Dashboard
1. Go to https://openrouter.ai/activity
2. View:
   - Request count
   - Token usage
   - Cost breakdown
   - Model usage

### Set Spending Limits
1. Go to https://openrouter.ai/settings
2. Set monthly spending limit
3. Get alerts when approaching limit

---

## 🔄 Migrating from Anthropic Direct API

If you were using Anthropic's direct API before:

### What Changed:
- ✅ API endpoint: Now using OpenRouter
- ✅ API key: Now using OpenRouter key
- ✅ Request format: Slightly different
- ✅ Model names: Prefixed with provider

### What Stayed the Same:
- ✅ Model capabilities (still Claude)
- ✅ Response format
- ✅ Tool calling support
- ✅ Application functionality

### Migration Steps:
1. Get OpenRouter API key
2. Update `.env` file
3. Install dependencies: `pip install requests python-dotenv`
4. Restart backend server
5. Test functionality

---

## 💡 Tips for Cost Optimization

### 1. Choose Right Model
- Use Claude 3 Haiku for simple tasks
- Use Claude 3.5 Sonnet for complex tasks
- Reserve Opus for critical tasks

### 2. Optimize Prompts
- Keep system prompts concise
- Limit conversation history
- Use clear, specific instructions

### 3. Implement Caching
- Cache common responses
- Store frequently used data
- Reduce redundant API calls

### 4. Monitor Usage
- Check dashboard regularly
- Set spending alerts
- Review cost per feature

---

## 🆘 Getting Help

### OpenRouter Support
- Documentation: https://openrouter.ai/docs
- Discord: https://discord.gg/openrouter
- Email: support@openrouter.ai

### Project Issues
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review backend logs
- Test API connection

---

## ✅ Setup Checklist

- [ ] Created OpenRouter account
- [ ] Added credits to account
- [ ] Generated API key
- [ ] Set environment variable or `.env` file
- [ ] Installed dependencies (`requests`, `python-dotenv`)
- [ ] Tested API connection
- [ ] Started backend successfully
- [ ] Verified AI responses work

---

## 🎉 You're All Set!

Your Voice AI Assistant is now powered by OpenRouter!

**Benefits:**
- ✅ Access to Claude AI
- ✅ Competitive pricing
- ✅ Flexible model selection
- ✅ Reliable service

**Next Steps:**
1. Start using the assistant
2. Monitor your usage
3. Optimize for your needs
4. Explore other models

---

*For more information, visit https://openrouter.ai/docs*

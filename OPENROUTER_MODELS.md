# 🤖 OpenRouter Model Names

## Current Model Configuration

Your app is now configured to use:
```
anthropic/claude-3.5-sonnet:beta
```

---

## Available Claude Models on OpenRouter

### Claude 3.5 (Recommended)
```python
"anthropic/claude-3.5-sonnet:beta"     # Latest Claude 3.5 Sonnet (CURRENT)
"anthropic/claude-3.5-sonnet"          # Stable Claude 3.5 Sonnet
```

### Claude 3 (Older versions)
```python
"anthropic/claude-3-opus"              # Most capable Claude 3
"anthropic/claude-3-sonnet"            # Balanced Claude 3
"anthropic/claude-3-haiku"             # Fastest Claude 3
```

### Claude 3 with specific dates
```python
"anthropic/claude-3-opus:beta"
"anthropic/claude-3-sonnet:beta"
"anthropic/claude-3-haiku:beta"
```

---

## Other Popular Models on OpenRouter

### OpenAI Models
```python
"openai/gpt-4-turbo"                   # GPT-4 Turbo
"openai/gpt-4"                         # GPT-4
"openai/gpt-3.5-turbo"                 # GPT-3.5 (cheapest)
"openai/gpt-4o"                        # GPT-4 Optimized
```

### Google Models
```python
"google/gemini-pro"                    # Gemini Pro
"google/gemini-pro-vision"             # Gemini with vision
"google/palm-2-chat-bison"             # PaLM 2
```

### Meta Models
```python
"meta-llama/llama-3-70b-instruct"      # Llama 3 70B
"meta-llama/llama-3-8b-instruct"       # Llama 3 8B
```

### Mistral Models
```python
"mistralai/mistral-large"              # Mistral Large
"mistralai/mistral-medium"             # Mistral Medium
"mistralai/mistral-small"              # Mistral Small
```

---

## How to Change Model

Edit `backend/agent.py`:

```python
class ToDoAgent:
    def __init__(self, memory_store: MemoryStore, todo_manager: ToDoManager):
        # ... other code ...
        
        # Change this line:
        self.model = "anthropic/claude-3.5-sonnet:beta"  # Current
        
        # To one of these:
        # self.model = "anthropic/claude-3-opus"           # More capable
        # self.model = "anthropic/claude-3-haiku"          # Faster, cheaper
        # self.model = "openai/gpt-4-turbo"                # Alternative AI
        # self.model = "openai/gpt-3.5-turbo"              # Cheapest option
```

Then restart the backend:
```bash
# Stop backend (Ctrl+C)
# Start again
start-backend.bat
```

---

## Model Comparison

### Claude 3.5 Sonnet (Current)
- **Speed:** Fast
- **Quality:** Excellent
- **Cost:** ~$3 per million tokens
- **Best for:** General use, complex tasks
- **Recommended:** ✅ Yes

### Claude 3 Opus
- **Speed:** Slower
- **Quality:** Best
- **Cost:** ~$15 per million tokens
- **Best for:** Most complex tasks
- **Recommended:** For critical tasks only

### Claude 3 Haiku
- **Speed:** Fastest
- **Quality:** Good
- **Cost:** ~$0.25 per million tokens
- **Best for:** Simple tasks, high volume
- **Recommended:** For cost savings

### GPT-4 Turbo
- **Speed:** Fast
- **Quality:** Excellent
- **Cost:** ~$10 per million tokens
- **Best for:** Alternative to Claude
- **Recommended:** If Claude unavailable

### GPT-3.5 Turbo
- **Speed:** Very fast
- **Quality:** Good
- **Cost:** ~$0.50 per million tokens
- **Best for:** Simple tasks, testing
- **Recommended:** For development/testing

---

## Pricing Estimates

Based on typical usage:

### Average Conversation (1,000-5,000 tokens)

| Model | Cost per Conversation | $5 Gets You |
|-------|----------------------|-------------|
| Claude 3.5 Sonnet | $0.003 - $0.015 | 300-1,500 |
| Claude 3 Opus | $0.015 - $0.075 | 65-330 |
| Claude 3 Haiku | $0.0003 - $0.0013 | 3,800-16,600 |
| GPT-4 Turbo | $0.010 - $0.050 | 100-500 |
| GPT-3.5 Turbo | $0.0005 - $0.0025 | 2,000-10,000 |

---

## Testing Different Models

### Quick Test Script

Create `backend/test_model.py`:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_model(model_name):
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one sentence."}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ {model_name}")
        print(f"   Response: {data['choices'][0]['message']['content']}")
        return True
    except Exception as e:
        print(f"❌ {model_name}")
        print(f"   Error: {e}")
        return False

# Test models
models = [
    "anthropic/claude-3.5-sonnet:beta",
    "anthropic/claude-3-opus",
    "anthropic/claude-3-haiku",
    "openai/gpt-4-turbo",
    "openai/gpt-3.5-turbo",
]

print("Testing OpenRouter Models...\n")
for model in models:
    test_model(model)
    print()
```

Run it:
```bash
cd backend
python test_model.py
```

---

## Checking Available Models

Visit OpenRouter's model list:
https://openrouter.ai/models

Or use their API:
```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

---

## Model Selection Guide

### For Your Voice Assistant:

**Best Overall:** `anthropic/claude-3.5-sonnet:beta`
- ✅ Great quality
- ✅ Good speed
- ✅ Reasonable cost
- ✅ Excellent for conversations

**Budget Option:** `anthropic/claude-3-haiku`
- ✅ Very cheap
- ✅ Very fast
- ⚠️ Slightly lower quality
- ✅ Good for simple tasks

**Premium Option:** `anthropic/claude-3-opus`
- ✅ Best quality
- ⚠️ Slower
- ⚠️ More expensive
- ✅ Best for complex reasoning

**Alternative:** `openai/gpt-4-turbo`
- ✅ Excellent quality
- ✅ Good speed
- ⚠️ More expensive than Claude 3.5
- ✅ Good if Claude unavailable

---

## Current Configuration

Your app is configured with:
```python
model = "anthropic/claude-3.5-sonnet:beta"
```

This is the **recommended model** for:
- ✅ Voice conversations
- ✅ Task management
- ✅ Memory storage
- ✅ Natural language understanding
- ✅ Tool calling

---

## Troubleshooting Model Errors

### Error: "No endpoints found for [model]"

**Cause:** Model name is incorrect or not available

**Solution:**
1. Check model name spelling
2. Visit https://openrouter.ai/models
3. Use exact model name from the list
4. Try alternative model

### Error: "Model requires higher tier"

**Cause:** Some models require paid plans

**Solution:**
1. Add credits to OpenRouter account
2. Use a different model
3. Check model requirements

### Error: "Rate limit exceeded"

**Cause:** Too many requests

**Solution:**
1. Wait a few seconds
2. Reduce request frequency
3. Upgrade OpenRouter plan

---

## Summary

✅ **Current Model:** `anthropic/claude-3.5-sonnet:beta`  
✅ **Status:** Working  
✅ **Quality:** Excellent  
✅ **Cost:** Reasonable  
✅ **Speed:** Fast  

**Your Voice AI Assistant is now using the correct model! 🎉**

---

*For latest model list, visit: https://openrouter.ai/models*

# Security Guidelines

## 🔒 API Key Security

This project uses environment variables to securely manage API keys. Follow these guidelines:

### ✅ DO:
- Store all API keys in the `.env` file
- Use `.env.example` as a template
- Keep `.env` in `.gitignore` (already configured)
- Rotate API keys regularly
- Use different API keys for development and production

### ❌ DON'T:
- Never commit `.env` to version control
- Never hardcode API keys in source code
- Never share your `.env` file
- Never commit files containing API keys

## 🛡️ Protected Files

The following files are automatically ignored by git:

- `.env` - Contains your actual API keys
- `__pycache__/` - Python cache files
- `.venv/` - Virtual environment
- `*.log` - Log files
- `travel_plan.txt` - Output files that may contain personal data
- `test_travel_plan.txt` - Test output files

## 🔍 Before Committing

Always run these checks before committing:

```bash
# 1. Verify .env is ignored
git check-ignore -v .env

# 2. Check what will be committed
git status

# 3. Search for potential API keys in tracked files
git grep -i "api.key\|secret\|token" -- ':!SECURITY.md' ':!README.md'
```

## 🚨 If You Accidentally Commit API Keys

1. **Immediately revoke/rotate the exposed API keys**
2. Remove the keys from git history:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. Force push (if already pushed to remote):
   ```bash
   git push origin --force --all
   ```
4. Update `.env` with new API keys

## 📋 Setup Checklist for New Users

- [ ] Clone the repository
- [ ] Copy `.env.example` to `.env`
- [ ] Add your API keys to `.env`
- [ ] Verify `.env` is in `.gitignore`
- [ ] Never commit `.env`

## 🔗 API Key Resources

- **Google Gemini**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **OpenRouter**: https://openrouter.ai/keys

## 📞 Reporting Security Issues

If you discover a security vulnerability, please email the maintainer directly instead of opening a public issue.

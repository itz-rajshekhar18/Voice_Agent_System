# 🔄 Change Repository Guide

## Current Repository
- **Current:** https://github.com/itz-rajshekhar18/multi_agent_system.git
- **Project:** Voice-Enabled AI Assistant (formerly multi_agent_system)

---

## 📋 Steps to Change Repository

### Option 1: Push to New Repository (Recommended)

This keeps your git history and pushes to a new repo.

#### Step 1: Create New Repository on GitHub
1. Go to https://github.com/new
2. Create a new repository (e.g., `voice-ai-assistant`)
3. **Do NOT** initialize with README, .gitignore, or license
4. Copy the new repository URL

#### Step 2: Commit Current Changes
```bash
# Stage all changes
git add .

# Commit with a descriptive message
git commit -m "Complete voice-enabled AI assistant with React frontend and Flask backend"
```

#### Step 3: Change Remote URL
```bash
# Remove old remote
git remote remove origin

# Add new remote (replace with your new repo URL)
git remote add origin https://github.com/YOUR-USERNAME/voice-ai-assistant.git

# Verify
git remote -v
```

#### Step 4: Push to New Repository
```bash
# Push to new repo
git push -u origin main

# If main branch doesn't exist, try:
git push -u origin master
```

---

### Option 2: Keep Same Repository, Rename It

If you want to keep the same repository but rename it:

#### Step 1: Rename on GitHub
1. Go to https://github.com/itz-rajshekhar18/multi_agent_system
2. Click **Settings**
3. Change repository name to `voice-ai-assistant`
4. Click **Rename**

#### Step 2: Update Local Remote
```bash
# Commit current changes first
git add .
git commit -m "Complete voice-enabled AI assistant"

# Update remote URL (GitHub will redirect, but it's good practice)
git remote set-url origin https://github.com/itz-rajshekhar18/voice-ai-assistant.git

# Push changes
git push origin main
```

---

### Option 3: Fresh Start (Clean History)

If you want to start fresh without old history:

#### Step 1: Create New Repository on GitHub
1. Go to https://github.com/new
2. Create repository: `voice-ai-assistant`
3. Copy the repository URL

#### Step 2: Remove Old Git History
```bash
# Remove .git folder
rm -rf .git

# Initialize new repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Voice-enabled AI assistant"
```

#### Step 3: Push to New Repository
```bash
# Add remote
git remote add origin https://github.com/YOUR-USERNAME/voice-ai-assistant.git

# Create main branch and push
git branch -M main
git push -u origin main
```

---

## 🎯 Recommended Approach

**I recommend Option 1** because:
- ✅ Keeps your commit history
- ✅ Easy to revert if needed
- ✅ Professional approach
- ✅ Can reference old commits

---

## 📝 Before You Push

### 1. Create .gitignore
```bash
# Create .gitignore file
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
dist/
.vite/
.vite-temp/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
backend/todos.json
backend/memory.json
backend/__pycache__/
voice_agent_system/dist/
voice_agent_system/.vite/
EOF
```

### 2. Review Files to Commit
```bash
# Check what will be committed
git status

# Review changes
git diff
```

### 3. Update README with New Repo URL
Update any references to the old repository in documentation.

---

## ✅ Post-Change Checklist

After changing repository:

- [ ] New repository created on GitHub
- [ ] All changes committed
- [ ] Remote URL updated
- [ ] Successfully pushed to new repo
- [ ] .gitignore file added
- [ ] README updated with new repo URL
- [ ] Documentation references updated
- [ ] Old repository archived (optional)

---

## 🔒 Security Notes

### Before Pushing, Check for Secrets:
```bash
# Search for potential API keys
grep -r "sk-ant-" .
grep -r "ANTHROPIC_API_KEY" .

# Make sure .env files are in .gitignore
cat .gitignore | grep .env
```

### Files That Should NOT Be Committed:
- ❌ `.env` files with real API keys
- ❌ `todos.json` with personal data
- ❌ `memory.json` with personal data
- ❌ `node_modules/` folder
- ❌ `__pycache__/` folders
- ❌ `.vite/` cache folders

### Files That SHOULD Be Committed:
- ✅ `.env.example` (template without real keys)
- ✅ All source code files
- ✅ Documentation files
- ✅ Configuration files
- ✅ `requirements.txt` and `package.json`

---

## 🚀 Quick Commands

### Complete Flow (Option 1):
```bash
# 1. Commit changes
git add .
git commit -m "Complete voice-enabled AI assistant"

# 2. Change remote
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/NEW-REPO.git

# 3. Push
git push -u origin main
```

### Verify Everything:
```bash
# Check remote
git remote -v

# Check branch
git branch

# Check status
git status

# View commit history
git log --oneline
```

---

## 📞 Need Help?

### Common Issues:

**"Permission denied"**
- Check GitHub authentication
- Use personal access token if needed
- Verify repository permissions

**"Repository not found"**
- Check repository URL is correct
- Verify repository exists on GitHub
- Check you have access to the repository

**"Failed to push"**
- Try: `git pull origin main --rebase`
- Then: `git push origin main`

**"Divergent branches"**
- If new repo has README: `git pull origin main --allow-unrelated-histories`
- Then: `git push origin main`

---

## 🎉 Done!

Your project is now in a new repository!

### Next Steps:
1. Update any CI/CD pipelines
2. Update deployment configurations
3. Notify team members of new URL
4. Archive old repository (optional)
5. Update bookmarks and links

---

*Good luck with your new repository!* 🚀

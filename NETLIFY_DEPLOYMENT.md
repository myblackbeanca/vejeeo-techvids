# 🚀 Netlify Deployment Guide for Vejeeo TechVids

## Quick Deploy Options

### Option 1: Deploy via Netlify UI (Recommended) ⭐

1. **Go to Netlify**: Visit https://app.netlify.com/
2. **Click "Add new site"** → **"Import an existing project"**
3. **Connect to GitHub**:
   - Select your GitHub account
   - Choose repository: `myblackbeanca/vejeeo-techvids`
   - Click "Authorize"

4. **Configure Build Settings**:
   ```
   Branch to deploy: main
   Build command: (leave empty)
   Publish directory: .
   ```

5. **Click "Deploy site"**

That's it! Netlify will:
- Auto-detect the `netlify.toml` configuration
- Deploy all HTML files and JSON data
- Set up redirects and headers
- Provide a live URL

---

### Option 2: Deploy Button

Click this button to deploy in one click:

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/myblackbeanca/vejeeo-techvids)

---

### Option 3: Manual Drag & Drop

1. Create a ZIP file of the required files:
   ```bash
   zip -r vejeeo-techvids-deploy.zip \
     index.html \
     playbookai.html \
     channels-index.html \
     video_feed.json \
     channels_index.json \
     ai_videos.json \
     docs/ \
     netlify.toml
   ```

2. Go to https://app.netlify.com/drop
3. Drag and drop the ZIP file
4. Your site will be deployed instantly!

---

## 🎯 What's Configured

### Build Settings (netlify.toml)
- **Publish directory**: Current directory (.)
- **No build command**: Static HTML site
- **Redirects**:
  - `/` → `index.html`
  - `/playbook` → `playbookai.html`
  - `/channels` → `channels-index.html`

### Security Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection enabled
- Referrer-Policy: strict-origin-when-cross-origin

### Caching
- JSON files: 1 hour cache
- HTML files: No cache (always fresh)

---

## 📊 Expected Result

After deployment, you'll get:

**Live URLs:**
- Main Dashboard: `https://your-site-name.netlify.app/`
- AI Playbook: `https://your-site-name.netlify.app/playbookai.html`
- Channels: `https://your-site-name.netlify.app/channels-index.html`

**Custom Domain (Optional):**
- You can add a custom domain in Netlify dashboard
- SSL certificate is automatic and free

---

## 🔧 Troubleshooting

### If deployment fails:
1. Check that all JSON files are valid
2. Verify netlify.toml syntax
3. Check Netlify build logs in dashboard

### If pages don't load:
1. Clear browser cache
2. Check browser console for errors
3. Verify JSON files are accessible

### To update the site:
- Just push to GitHub main branch
- Netlify auto-deploys on every push
- Or use the Netlify UI to trigger manual deploy

---

## 📈 Post-Deployment

### Monitor your site:
- **Analytics**: Enable in Netlify dashboard
- **Build logs**: Check deployment status
- **Forms**: Can add forms for user feedback
- **Functions**: Can add serverless functions later

### Continuous Deployment:
- ✅ Auto-deploys from GitHub
- ✅ Preview deploys for PRs
- ✅ Rollback to previous versions
- ✅ Branch deploys for testing

---

## 💡 Pro Tips

1. **Custom domain**: Add in "Domain settings"
2. **Environment variables**: Add in "Site settings" → "Build & deploy"
3. **Split testing**: Test different versions
4. **Analytics**: Enable to track visitors
5. **Forms**: Add forms without backend code

---

## 🎨 Current Site Structure

```
vejeeo-techvids/
├── index.html              (Main Dashboard - 3,066 videos)
├── playbookai.html         (AI Playbook - 114 AI videos)
├── channels-index.html     (627 channels)
├── video_feed.json         (2.5MB - all videos)
├── channels_index.json     (536KB - channel data)
├── ai_videos.json          (59KB - AI videos)
├── netlify.toml            (Configuration)
└── docs/                   (Documentation)
```

---

## 🚀 Next Steps

1. Deploy using Option 1 above
2. Get your live URL
3. Share with @collectivewinca
4. Optional: Add custom domain
5. Optional: Enable analytics

**Estimated deployment time**: 1-2 minutes

---

Last updated: January 9, 2026

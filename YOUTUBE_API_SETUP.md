# YouTube Data API v3 Setup Guide

This guide will help you set up the YouTube Data API v3 to use with the Vejeeo TechVids pipeline.

## Prerequisites

- Google Cloud SDK (`gcloud` CLI)
- Google Account
- 10-15 minutes

## Step-by-Step Setup

### Step 1: Authenticate with Google Cloud

```bash
gcloud auth login
```

This will:
- Open your browser for Google authentication
- Ask you to sign in with your Google account
- Request permissions
- Return an authentication token

**Verify authentication:**
```bash
gcloud auth list
```

You should see your account marked as `ACTIVE`.

### Step 2: Create or Select a Google Cloud Project

**Check current project:**
```bash
gcloud config list --filter=core.project
```

**Create a new project (if needed):**
```bash
gcloud projects create vejeeo-techvids --name="Vejeeo Tech Videos"
```

**Set as active project:**
```bash
gcloud config set project vejeeo-techvids
```

**Verify:**
```bash
gcloud config list
```

### Step 3: Enable YouTube Data API v3

**Option A: Using gcloud CLI (recommended)**

```bash
gcloud services enable youtube.googleapis.com
```

**Option B: Manual via Console**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to "APIs & Services" > "Library"
4. Search for "YouTube Data API v3"
5. Click "Enable"

### Step 4: Create API Credentials

**Using gcloud CLI:**

```bash
gcloud services enable serviceusage.googleapis.com
gcloud compute project-info describe --project=vejeeo-techvids \
  --format='value(commonInstanceMetadata.items[google-compute-default-region].value)'
```

**Manual via Console (recommended for API Key):**

1. Go to [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" dropdown
3. Select "API Key"
4. Copy the generated API key
5. (Optional) Restrict the key:
   - Click the key to edit
   - Set "Application restrictions" to "HTTP referrers"
   - Set "API restrictions" to "YouTube Data API v3"

### Step 5: Set Environment Variable

**Add to your shell profile** (`.bashrc`, `.zshrc`, etc.):

```bash
export YOUTUBE_API_KEY='YOUR_API_KEY_HERE'
```

**Or set temporarily for current session:**

```bash
export YOUTUBE_API_KEY='YOUR_API_KEY_HERE'
```

**Verify it's set:**

```bash
echo $YOUTUBE_API_KEY
```

Should output your API key.

### Step 6: Test the API

```bash
python3 fetch_test_channels.py
```

This will:
- Use the 10 test channels from `test_channels.json`
- Fetch data from YouTube API
- Display results summary
- Save results to `test_results.json`

## API Quota

### Default Quota
- **10,000 units per day**
- Each API call uses 1-4 units
- Typical usage: ~2,500 channels per day

### For Full Dataset
- 652 channels = ~2,000-2,600 units
- Sufficient for ~3-4 full runs per day

### Monitor Quota

**In Google Cloud Console:**
1. Go to "APIs & Services" > "YouTube Data API v3"
2. Click "Quotas" tab
3. View current usage

**Command line:**
```bash
gcloud compute project-info describe --project=vejeeo-techvids
```

## Usage Examples

### Test with 10 Channels
```bash
python3 fetch_test_channels.py
```

### Fetch All 652 Channels
```bash
python3 fetch_youtube_data.py
```

### Display Results
```bash
python3 display_test_results.py
```

## Troubleshooting

### Issue: "YOUTUBE_API_KEY not set"

**Solution:**
```bash
# Check if variable is set
echo $YOUTUBE_API_KEY

# If empty, set it
export YOUTUBE_API_KEY='your-key-here'

# Verify
python3 -c "import os; print(os.getenv('YOUTUBE_API_KEY'))"
```

### Issue: "API quota exceeded"

**Solution:**
- Wait 24 hours for quota reset
- Upgrade to a paid plan if needed
- Optimize requests to use fewer units

### Issue: "403 Forbidden"

**Possible causes:**
1. API not enabled in Google Cloud Console
2. API key restrictions too strict
3. API key expired or invalid

**Solution:**
```bash
# Verify API is enabled
gcloud services list --enabled | grep youtube

# Create new API key if needed
```

### Issue: "404 Channel not found"

**Possible causes:**
1. Channel has been deleted
2. Channel ID is incorrect
3. Channel is private/restricted

**Solution:**
- Verify the channel URL is correct
- Check channel exists on YouTube
- Try different URL formats (custom URL, handle, etc.)

## Security Best Practices

### 🔒 API Key Security

1. **Never commit API keys to git**
   - Add to `.gitignore`:
   ```
   YOUTUBE_API_KEY
   .env
   *.key
   ```

2. **Use environment variables**
   ```bash
   export YOUTUBE_API_KEY='your-key'
   ```

3. **Restrict API Key**
   - Limit to YouTube Data API v3 only
   - Restrict HTTP referrers if possible
   - Set IP restrictions if using from server

4. **Rotate keys periodically**
   - Create new keys monthly
   - Delete old unused keys

### 🔐 Service Account (Alternative)

For production deployments, use a service account instead:

```bash
# Create service account
gcloud iam service-accounts create youtube-api-user

# Create key
gcloud iam service-accounts keys create youtube-key.json \
  --iam-account=youtube-api-user@vejeeo-techvids.iam.gserviceaccount.com

# Use in code
export GOOGLE_APPLICATION_CREDENTIALS='youtube-key.json'
```

## Next Steps

1. ✅ Authenticate with `gcloud auth login`
2. ✅ Create/select project
3. ✅ Enable YouTube Data API
4. ✅ Create API credentials
5. ✅ Set `YOUTUBE_API_KEY` environment variable
6. ✅ Test with `python3 fetch_test_channels.py`
7. ✅ Run on all 652 channels with `python3 fetch_youtube_data.py`
8. ✅ Generate documentation with `python3 generate_markdown.py`

## Resources

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [API Quota Information](https://developers.google.com/youtube/v3/determine_quota_cost)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Authentication Guide](https://cloud.google.com/docs/authentication)
- [API Key Best Practices](https://cloud.google.com/docs/authentication/api-keys)

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [YouTube API Documentation](https://developers.google.com/youtube/v3)
3. Check [Google Cloud Status](https://status.cloud.google.com/)
4. Open an issue on [GitHub](https://github.com/myblackbeanca/vejeeo-techvids/issues)

---

**Last Updated:** January 8, 2024
**YouTube API Version:** v3
**Required Quota:** 10,000 units/day (default)

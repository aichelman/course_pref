# Render Setup Guide - Persistent Storage & Keep-Alive

This guide fixes two issues with Render's free tier:
1. **Database persistence** - User accounts disappearing when service restarts
2. **Keep-alive** - Preventing the service from sleeping after 15 minutes

---

## Issue 1: Fix Database Persistence (IMPORTANT!)

### The Problem
Render's free tier uses ephemeral storage. When your service sleeps or restarts, the SQLite database gets wiped and all user accounts disappear.

### The Solution: Add Persistent Disk

#### Option A: Using render.yaml (Recommended)

The repo already includes a `render.yaml` file that configures persistent storage. Render will automatically detect and use it.

**Steps:**
1. Push the updated code to GitHub (includes render.yaml)
2. When creating/updating your service on Render, it will automatically:
   - Mount a 1GB persistent disk at `/data`
   - Store the database at `/data/courses.db`
   - Keep data even when service restarts

**Verify:** After deployment, check Render dashboard → Your Service → Disks tab to confirm the disk is mounted.

#### Option B: Manual Configuration (If render.yaml doesn't work)

1. Go to your Render dashboard
2. Select your web service
3. Go to "Disks" in the left sidebar
4. Click "Add Disk"
5. Configure:
   - **Name**: `course-data`
   - **Mount Path**: `/data`
   - **Size**: 1 GB (free tier includes up to 1GB)
6. Save and wait for service to redeploy

---

## Issue 2: Keep Server Alive (Optional)

### The Problem
Render's free tier sleeps after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

### Solutions

#### Option 1: UptimeRobot (Free & Easy)

**Best for:** Keeping your app awake during specific hours (e.g., when you and friends are most active)

1. Sign up at [uptimerobot.com](https://uptimerobot.com) (free)
2. Click "Add New Monitor"
3. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Golf Course Ranker
   - **URL**: `https://your-app-name.onrender.com/login`
   - **Monitoring Interval**: 5 minutes (free tier minimum)
4. Save

**Result:** UptimeRobot pings your app every 5 minutes, keeping it awake.

**Note:** This uses extra bandwidth. Render's free tier includes 100 GB/month, which should be plenty for this use case.

#### Option 2: Cron-job.org

1. Sign up at [cron-job.org](https://cron-job.org) (free)
2. Create new cron job
3. Configure:
   - **URL**: `https://your-app-name.onrender.com/login`
   - **Schedule**: Every 10 minutes (or 5 if available)
4. Enable and save

#### Option 3: BetterStack (formerly BetterUptime)

1. Sign up at [betterstack.com](https://betterstack.com)
2. Create uptime monitor
3. Point it to your Render URL
4. Set check interval to 5 minutes

#### Option 4: Simple Python Script (Run Locally)

Create a file called `keep_alive.py`:

```python
import requests
import time

APP_URL = "https://your-app-name.onrender.com/login"

while True:
    try:
        response = requests.get(APP_URL)
        print(f"Pinged {APP_URL} - Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    # Wait 10 minutes
    time.sleep(600)
```

Run it on your computer:
```bash
pip install requests
python keep_alive.py
```

**Downside:** Only works when your computer is on and running the script.

---

## Comparison Table

| Solution | Cost | Setup Time | Effectiveness | Notes |
|----------|------|------------|---------------|-------|
| **Persistent Disk** | FREE | 2 min | Essential | Fixes database issue |
| **UptimeRobot** | FREE | 5 min | High | Recommended keep-alive |
| **Cron-job.org** | FREE | 5 min | High | Alternative to UptimeRobot |
| **BetterStack** | FREE tier | 5 min | High | Enterprise features available |
| **Python Script** | FREE | 2 min | Medium | Requires computer to run |
| **Render Paid** | $7/mo | 1 min | Perfect | Best solution if budget allows |

---

## Recommended Setup

### For Most Users (Free):
1. ✅ **Enable persistent disk** (fixes database issue)
2. ✅ **Set up UptimeRobot** (keeps app awake)
3. Total cost: $0/month

### If Budget Allows:
1. ✅ **Enable persistent disk** (included)
2. ✅ **Upgrade to Render paid tier** ($7/month)
   - No sleep time
   - Faster performance
   - Better for multiple users

---

## Testing After Setup

### Test Persistent Storage:
1. Create a user account on your deployed app
2. Wait 20 minutes (let service sleep)
3. Visit the app again (wait for wake-up)
4. Try logging in with same credentials
5. ✅ If login works, persistence is working!

### Test Keep-Alive:
1. Check UptimeRobot dashboard
2. Look for "Up" status
3. Monitor "Response Time" - should stay consistent
4. ✅ If response time is always <500ms, keep-alive is working!

---

## Troubleshooting

### Database Still Resetting?
- Check Render dashboard → Disks → Ensure disk is mounted at `/data`
- Check logs for database path errors
- Verify environment variable `RENDER=true` is set (Render sets this automatically)

### Keep-Alive Not Working?
- Verify UptimeRobot shows "Up" status
- Check that ping URL is correct (include https://)
- Ensure monitoring interval is 5-10 minutes
- Check Render logs to see incoming ping requests

### Users Still Can't Login?
- Ensure persistent disk is configured first
- Redeploy the service after adding disk
- Have users create fresh accounts after persistence is enabled

---

## Important Notes

⚠️ **Ethical Consideration**: Using keep-alive services on free tiers may violate terms of service for some platforms. UptimeRobot and similar services are designed for monitoring (which is legitimate), but using them solely to avoid sleep time is a gray area.

💡 **Best Practice**: If you and your friends use this app regularly and want it always available, consider upgrading to Render's paid tier ($7/month) to support the platform.

🎯 **Alternative**: Use the free tier with persistent storage and accept the 30-second wake-up time. Most users won't mind the occasional wait.

---

## Next Steps

1. **Push updated code to GitHub** (includes render.yaml and database fix)
2. **Render will auto-redeploy** with persistent storage
3. **Set up UptimeRobot** (optional, for keep-alive)
4. **Test user accounts** to confirm persistence works
5. **Share with friends!**

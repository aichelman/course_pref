# Fix: Database Error on Render

If you're seeing this error:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
```

This means the persistent disk needs to be manually added to your Render service.

## Quick Fix Steps

### 1. Go to Render Dashboard
- Visit [dashboard.render.com](https://dashboard.render.com)
- Click on your `golf-course-ranker` service

### 2. Add Persistent Disk
- In the left sidebar, click **"Disks"**
- Click the **"Add Disk"** button
- Configure:
  - **Name**: `course-data`
  - **Mount Path**: `/data`
  - **Size**: 1 GB (free tier includes 1GB)
- Click **"Save"**

### 3. Wait for Redeploy
- Render will automatically redeploy your service (takes 2-3 minutes)
- The error should be fixed!

### 4. Verify It Worked
- Try visiting your app URL
- Register a new account
- The login should work now!

---

## Why This Happened

The `render.yaml` file should have automatically created the disk, but sometimes Render requires manual disk creation for free tier services.

## Alternative: Remove Disk Requirement (Quick Fix)

If you want to skip the disk setup for now (data will reset on restart):

1. Go to Render Dashboard → Your Service → Environment
2. Remove or set `RENDER` environment variable to empty
3. This will use ephemeral storage (like before the persistence update)
4. Redeploy

**Note**: With this option, user accounts will still disappear on service restart.

---

## Need Help?

If you're still having issues:
1. Check Render logs for more detailed error messages
2. Ensure the disk mount path is exactly `/data`
3. Make sure the disk is in "Active" status in the Disks tab

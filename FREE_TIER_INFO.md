# Render Free Tier Information

## Important Limitation

**Render's free tier does NOT include persistent storage.** This means:

### What Happens:
- ✅ Your app works perfectly while it's running
- ✅ Users can register, add courses, and rank them
- ❌ **When the service restarts or sleeps, all data (user accounts, courses, rankings) is LOST**
- ❌ This includes the 15-minute sleep after inactivity

### Why This Happens:
- Free tier uses "ephemeral storage" - temporary storage that resets
- Persistent disks are only available on paid plans ($7/month)

---

## Your Options

### Option 1: Accept the Free Tier Limitations (Current Setup)
**Cost**: Free
**Pros**:
- No cost
- Works great while running
- Good for testing or casual use

**Cons**:
- Data resets after sleep (15 min inactivity)
- Users need to re-register after restart
- Rankings are lost

**Best for**: Testing, demo purposes, or if you don't mind re-entering data

---

### Option 2: Upgrade to Render Paid Plan
**Cost**: $7/month
**Pros**:
- ✅ Persistent storage - data never resets!
- ✅ No sleep time - always instant
- ✅ Better performance
- ✅ Professional setup for you and friends

**Cons**:
- Costs $7/month

**How to Upgrade**:
1. Go to Render dashboard
2. Click your service
3. Click "Upgrade Plan"
4. Select "Starter" plan ($7/month)
5. Add persistent disk (included in paid plan)

**Best for**: Regular use with friends, want data to persist

---

### Option 3: Use Different Free Hosting
Some alternatives with better free tiers:

**Railway**:
- $5 credit/month (free)
- Persistent storage included
- Might last longer depending on usage

**Fly.io**:
- More generous free tier
- Persistent volumes included
- Good for small apps

---

## Recommendation

### For Now (Free):
- Use the current Render free tier setup
- Set up **UptimeRobot** to keep it awake (prevents 15-min sleep)
- Accept that data resets if service restarts (rare, but happens)
- Good enough for casual use with friends

### If You Love It:
- After a week or two of use, if you and friends are using it regularly
- Upgrade to Render paid ($7/month) for persistence
- Worth it if you're ranking 50+ courses and don't want to re-do it

---

## Current Status

Your app is configured to work on Render's **free tier**:
- ✅ No persistent storage (data may reset)
- ✅ 15-minute sleep after inactivity (use UptimeRobot to prevent)
- ✅ Works perfectly while running

To get persistent storage, upgrade to paid plan and follow instructions in `RENDER_DISK_FIX.md`.

---

## Questions?

**Q: How often does data reset?**
A: Only when Render restarts your service (during deployments, maintenance, or if manually restarted). With UptimeRobot keeping it awake, this is rare.

**Q: Will my friends lose their data?**
A: Only if the service restarts. If everyone uses it within the same session, data persists fine.

**Q: Is $7/month worth it?**
A: If you and friends use it regularly and have ranked many courses, yes! If just testing, stay on free tier.

**Q: Can I export my data?**
A: Not currently, but we could add a feature to download your rankings as CSV if needed.

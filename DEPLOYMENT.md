# Deployment Guide

This guide will help you deploy your Golf Course Ranking app so your friends can access it online.

## Option 1: Deploy to Render (Recommended - Easiest & Free)

### Prerequisites
- GitHub account
- Render account (free at [render.com](https://render.com))

### Steps

1. **Push your code to GitHub**
   ```bash
   cd /Users/jaichelman/dev/course_pref
   git init
   git add .
   git commit -m "Initial commit - Golf Course Ranking App"
   # Create a new repo on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com) and sign in
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: golf-course-ranker (or your choice)
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

3. **Set Environment Variables**
   - In Render dashboard, go to "Environment"
   - Add these variables:
     - `SECRET_KEY`: Generate a random string (e.g., use `python -c "import secrets; print(secrets.token_hex(32))"`)
     - `FLASK_ENV`: production

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app (takes 2-3 minutes)
   - You'll get a URL like: `https://golf-course-ranker.onrender.com`

5. **Share with Friends**
   - Send them the URL
   - Each friend creates their own account
   - Everyone has their own private course list and rankings!

### Important Notes for Render
- Free tier sleeps after 15 minutes of inactivity (takes ~30 seconds to wake up)
- Database persists between restarts
- Upgrade to paid tier ($7/month) for always-on service

---

## Option 2: Deploy to Railway

### Steps

1. **Push code to GitHub** (same as above)

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Flask apps
   - Add environment variable:
     - `SECRET_KEY`: (generate with command above)
     - `FLASK_ENV`: production

4. **Deploy**
   - Railway automatically deploys
   - Get your URL from the dashboard

---

## Option 3: Deploy to Fly.io

### Steps

1. **Install Fly CLI**
   ```bash
   brew install flyctl  # macOS
   ```

2. **Login and Launch**
   ```bash
   fly auth login
   cd /Users/jaichelman/dev/course_pref
   fly launch
   ```

3. **Configure**
   - Follow the prompts
   - Set secrets:
   ```bash
   fly secrets set SECRET_KEY="your-generated-secret-key"
   fly secrets set FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

---

## Option 4: PythonAnywhere (Good for Beginners)

### Steps

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com) (free tier available)

2. **Upload your code**
   - Use their file browser or Git
   - Upload all files to `/home/yourusername/golf-course-ranker/`

3. **Create a Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask"
   - Python version: 3.11

4. **Configure WSGI**
   - Edit the WSGI configuration file
   - Point it to your app.py

5. **Install Dependencies**
   - Open a Bash console
   ```bash
   cd ~/golf-course-ranker
   pip install -r requirements.txt
   ```

6. **Reload** and your app will be live!

---

## Security Checklist Before Going Live

- [ ] Set a strong `SECRET_KEY` environment variable (not the default)
- [ ] Ensure `FLASK_ENV=production` is set
- [ ] Test login/register functionality
- [ ] Test that users can't see each other's courses
- [ ] Database file is in `.gitignore` if using SQLite in production

---

## Database Considerations

**SQLite (Current Setup)**
- Works fine for small groups (you + a few friends)
- Simple, no configuration needed
- Limitations: Not ideal for high traffic or concurrent writes

**If You Grow Larger**
Consider switching to PostgreSQL:
- Most platforms offer free PostgreSQL databases
- Change `SQLALCHEMY_DATABASE_URI` to use Postgres
- Install `psycopg2-binary` package

---

## Troubleshooting

**App won't start?**
- Check logs in your hosting platform
- Verify all dependencies are in requirements.txt
- Ensure SECRET_KEY is set

**Database not persisting?**
- Check that instance/ directory exists
- On some platforms, you need to use persistent storage volumes

**Friends can't register?**
- Check that the /register route is accessible
- Verify no firewall issues

---

## Cost Breakdown

| Platform | Free Tier | Limitations | Paid (Monthly) |
|----------|-----------|-------------|----------------|
| Render | Yes | Sleeps after 15min inactivity | $7 (always-on) |
| Railway | $5 credit/month | Limited hours | $5+ usage-based |
| Fly.io | Yes | 3 apps, limited resources | $5+ usage-based |
| PythonAnywhere | Yes | Custom domain not available | $5 (custom domain) |

**Recommendation**: Start with Render's free tier. If your friends use it regularly and the sleep delay bothers you, upgrade to $7/month.

---

## Sharing with Friends

Once deployed, send your friends:
1. The URL (e.g., `https://your-app.onrender.com`)
2. Instructions: "Create an account and start adding your courses!"
3. Each person will have their own private course list

---

## Need Help?

- Check your platform's logs for errors
- Ensure all environment variables are set correctly
- Test locally first with `python app.py`

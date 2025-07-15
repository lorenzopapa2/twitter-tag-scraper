## Deployment Instructions for Vercel

### Your GitHub Repository:
https://github.com/lorenzopapa2/twitter-tag-scraper

### Steps to Deploy on Vercel:

1. **Visit Vercel**: Go to https://vercel.com and sign in with your GitHub account

2. **Import Project**:
   - Click 'New Project'
   - Select 'Import Git Repository'
   - Choose 'twitter-tag-scraper' from your repositories

3. **Configure Project**:
   - Framework Preset: Select 'Other'
   - Root Directory: Leave as './'
   - Build Command: Leave empty
   - Output Directory: Leave as './'

4. **Deploy**:
   - Click 'Deploy'
   - Wait for deployment to complete (usually takes 1-2 minutes)

5. **Access Your Site**:
   - Once deployed, you'll get a URL like: https://twitter-tag-scraper.vercel.app
   - Your site will be live immediately\!

### Important Notes:
- The main page (index.html) will be served automatically
- All static files are included in the deployment
- The ChatGPT API key is embedded in the HTML (consider using environment variables for production)

### Custom Domain (Optional):
- In Vercel dashboard, go to Settings > Domains
- Add your custom domain if you have one

Your application is now ready to be deployed\!

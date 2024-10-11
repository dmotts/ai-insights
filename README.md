<h1 align="center">
AI Insights <br> Report Generator</span>
</h1>

<div align="center">
<p align="center">
<a href="https://github.com/dmotts/ai-insights/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.yml&title=%5BFeature+Request%5D+">Request Feature</a>
     ·
    <a href="https://ai-insights-production.up.railway.app/" target="blank">View Demo</a>
    ·
    <a href="https://github.com/dmotts/ai-insights/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml&title=%5BBug%5D+">Report Bug</a>
 
</p>

   <img src="https://res.cloudinary.com/dzpafdvkm/image/upload/v1727899164/Portfolio/ai-insights-screenshot.png" alt="AI Insights Screenshot" />
</div>

## Project Overview 🧐
AI Insights is a web-based application designed to provide valuable insights for your business using AI-driven analytics. The application leverages multiple data sources to deliver comprehensive reports and visualizations, helping users make data-driven decisions with ease.

## Setup Instructions 📄

### Prerequisites 
- Python 3.x
- Poetry package manager
- Google Sheets API credentials (either through environment variables or a `credentials.json` file)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dmotts/ai-insights.git
   cd ai-insights
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Configure the necessary environment variables. You can set them in your environment or create a `.env` file in the root directory. Required variables include:

   - `GOOGLE_SHEETS_TYPE`
   - `GOOGLE_SHEETS_PROJECT_ID`
   - `GOOGLE_SHEETS_PRIVATE_KEY_ID`
   - `GOOGLE_SHEETS_PRIVATE_KEY`
   - `GOOGLE_SHEETS_CLIENT_EMAIL`
   - `GOOGLE_SHEETS_CLIENT_ID`
   - `GOOGLE_SHEETS_AUTH_URI`
   - `GOOGLE_SHEETS_TOKEN_URI`
   - `GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL`
   - `GOOGLE_SHEETS_CLIENT_X509_CERT_URL`
   - `OPENAI_API_KEY`
   - `PROTONMAIL_ADDRESS`
   - `PROTONMAIL_PASSWORD`
   - `MONGODB_URI`

   Alternatively, you can store Google Sheets credentials in a `credentials.json` file in the root directory.

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://localhost:5000` to view the application.

## Contributions 🧑‍🔧👷‍♀️🏗️🏢
We welcome and appreciate all contributions to the **Customer Support Bot** project! 

Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started! 🚀

<p align="center"><em>Thank you for your support!</em></p>

<hr>
<h2 align="center"> 🌎 Let's Stay Connected 🤜🤛 </h2>

<p align="center"> If you like this project and would like to see more features or show your support.</p>
<p align="center"> Feel free to reach out to the developer(s) and give this project a ⭐!</p>



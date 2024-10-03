<h1 align="center">
AI Insights Report Generator</span>
</h1>

<div align="center">
<p align="center">
<a href="https://github.com/dmotts/ai-insights/issues/new/choose">Request Feature</a>
     ·
    <a href="https://ai-insights-production.up.railway.app/" target="blank">View Demo</a>
    ·
    <a href="https://github.com/dmotts/ai-insights/issues/new/choose">Report Bug</a>
 
</p>

   <img src="https://res.cloudinary.com/dzpafdvkm/image/upload/v1727899164/Portfolio/ai-insights-screenshot.png" alt="AI Insights Screenshot" />
</div>

## Project Overview
AI Insights is a web-based application designed to provide valuable insights for your business using AI-driven analytics. The application leverages multiple data sources to deliver comprehensive reports and visualizations, helping users make data-driven decisions with ease.

## Setup Instructions

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

## Contributions

Contributions are welcome! It only takes five (5) steps!

To contribute:

1) Fork the repository.

2) Create a new branch: `git checkout -b my-feature-branch`.

3) Make your changes and commit them: `git commit -m 'Add some feature'`.

4) Push to the branch: `git push origin my-feature-branch`.

5) Open a pull request.


***Please ensure your code follows the project's coding standards and includes tests where appropriate.***

## Contributors 

[Daley Mottley (dmotts)](https://github.com/dmotts)

## Let's Connect 🤝

<p> If you liked this project and would like see more features or show your support.</p>
Feel free to reach out to the developer(s) and give this project a ⭐!


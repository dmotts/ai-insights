<h1 align="center">
AI Insights <br> Report Generator <br> 🥸</span>
</h1>

<div align="center">
<p align="center">
<a href="https://github.com/daley-mottley/ai-insights/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.yml&title=%5BFeature+Request%5D+">Request Feature</a>
     ·
    <a href="https://ai-insights-production.up.railway.app/" target="blank">View Demo</a>
    ·
    <a href="https://github.com/daley-mottley/ai-insights/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml&title=%5BBug%5D+">Report Bug</a>
 
</p>

   <img src="https://res.cloudinary.com/dzpafdvkm/image/upload/v1727899164/Portfolio/ai-insights-screenshot.png" alt="AI Insights Screenshot" />
</div>

## Project Overview 🧐
AI Insights is a web-based application designed to provide valuable insights for your business using AI-driven analytics. The application leverages multiple data sources to deliver comprehensive reports and visualizations, helping users make data-driven decisions with ease. By default, it uses Google’s Gemini model (`gemini-1.5-pro`) for AI capabilities, with OpenAI as an optional alternative.

## Setup Instructions 📄

### Prerequisites 
- Python 3.x
- Poetry package manager (recommended) or pip
- Google Sheets API credentials (either through environment variables or a `credentials.json` file - see instructions below)
- Google Gemini API Key (required for default functionality)
- OpenAI API Key (optional, if using OpenAI instead of Gemini)

### Installation

1.  **Clone the repository:**
    ```bash
    # Clones the ai-insights repository from GitHub to your local machine
    git clone https://github.com/daley-mottley/ai-insights.git
    # Changes the current directory to the cloned repository
    cd ai-insights
    ```

2.  **Install dependencies:**
    ```bash
    # Installs the project dependencies listed in requirements.txt using pip
    # Note: Poetry is preferred (run `poetry install` instead) as it aligns with pyproject.toml
    pip install -r requirements.txt
    # Or using Poetry:
    # poetry install
    ```

3.  **Set up Environment Variables or `credentials.json`:**

    You need to provide credentials for the Google Sheets API. You have two options:

    **Option A: Using Environment Variables (Recommended for deployment)**

    Set the following environment variables in your system or in a `.env` file in the root directory:

    -   `GOOGLE_SHEETS_TYPE`
    -   `GOOGLE_SHEETS_PROJECT_ID`
    -   `GOOGLE_SHEETS_PRIVATE_KEY_ID`
    -   `GOOGLE_SHEETS_PRIVATE_KEY` (Make sure to handle multi-line keys correctly, often by replacing newlines with `\n`)
    -   `GOOGLE_SHEETS_CLIENT_EMAIL`
    -   `GOOGLE_SHEETS_CLIENT_ID`
    -   `GOOGLE_SHEETS_AUTH_URI`
    -   `GOOGLE_SHEETS_TOKEN_URI`
    -   `GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL`
    -   `GOOGLE_SHEETS_CLIENT_X509_CERT_URL`

    *(If you choose this option, you don't need the `credentials.json` file)*

    **Option B: Using `credentials.json` File (Easier for local development)**

    Store Google Sheets credentials in a file named `credentials.json` in the root directory of the project. Follow the steps below to obtain this file.

    *(If you choose this option, you don't need the `GOOGLE_SHEETS_*` environment variables listed above)*

    **Other Required Environment Variables:**

    Regardless of the Google Sheets credential method chosen, you must also set these (in your environment or `.env` file):

    -   `GEMINI_API_KEY` (required for default Gemini model)
    -   `OPENAI_API_KEY` (optional, required if using OpenAI)
    -   `LLM_MODEL` (optional, set to `'openai'` to use OpenAI; defaults to `'gemini'`)
    -   `PROTONMAIL_ADDRESS`
    -   `PROTONMAIL_PASSWORD`
    -   `MONGODB_URI`

### Obtaining Google Sheets `credentials.json` (Option B)

Follow these steps to create a service account and download the `credentials.json` file:

1.  **Go to the Google Cloud Console:**
    Navigate to [https://console.cloud.google.com/](https://console.cloud.google.com/) and log in with your Google account.

2.  **Create or Select a Project:**
    -   If you don't have a project, click the project dropdown menu at the top, then click "New Project". Give it a name (e.g., "AI Insights Access") and create it.
    -   If you have an existing project you want to use, select it from the dropdown menu.

3.  **Enable the Google Sheets API:**
    -   In the navigation menu (☰), go to "APIs & Services" > "Library".
    -   Search for "Google Sheets API".
    -   Click on "Google Sheets API" in the search results.
    -   Click the "Enable" button. Wait for the API to be enabled.

4.  **Create Service Account Credentials:**
    -   In the navigation menu (☰), go to "APIs & Services" > "Credentials".
    -   Click "+ CREATE CREDENTIALS" at the top and select "Service account".
    -   **Service account details:**
        -   Enter a "Service account name" (e.g., "ai-insights-sheet-access"). The "Service account ID" will be generated automatically.
        -   Add an optional "Description" (e.g., "Service account for AI Insights app to access Google Sheets").
        -   Click "CREATE AND CONTINUE".
    -   **Grant this service account access to project (Optional):** You can skip this step for accessing Google Sheets; roles here apply to GCP resources. Click "CONTINUE".
    -   **Grant users access to this service account (Optional):** You can skip this step. Click "DONE".

5.  **Generate a Key (JSON file):**
    -   You should now see your newly created service account listed under the "Service Accounts" section on the Credentials page.
    -   Click on the email address of the service account you just created.
    -   Go to the "KEYS" tab.
    -   Click "ADD KEY" and select "Create new key".
    -   Choose "JSON" as the key type.
    -   Click "CREATE".
    -   A JSON file containing your credentials will be automatically downloaded to your computer.

6.  **Rename and Place the File:**
    -   Rename the downloaded JSON file to `credentials.json`.
    -   Place this `credentials.json` file in the **root directory** of your cloned `ai-insights` project.
    -   **IMPORTANT:** Add `credentials.json` to your `.gitignore` file to prevent accidentally committing sensitive credentials to version control!
      ```bash
      echo "credentials.json" >> .gitignore
      ```

7.  **Share your Google Sheet(s) with the Service Account:**
    -   Open the `credentials.json` file and find the `client_email` value (it looks like an email address, e.g., `...@...gserviceaccount.com`). Copy this email address.
    -   Go to the Google Sheet(s) that this application needs to access.
    -   Click the "Share" button (usually in the top-right corner).
    -   Paste the copied service account email address into the "Add people and groups" field.
    -   Grant the service account the necessary permissions (e.g., "Editor" if the app needs to read and write data, or "Viewer" if it only needs to read).
    -   Ensure the "Notify people" checkbox is **unchecked** (optional, but usually desired for service accounts).
    -   Click "Share" or "Send".

Now you have the `credentials.json` file set up correctly in your project's root directory.

---

4.  **Run the application:**
    ```bash
    # Launches the Flask application using Python, defaulting to port 5000
    python app.py
    ```

5.  **Access the application:**
    Open your web browser and go to `http://localhost:5000` to view the application.

**Note:** The application uses Google’s Gemini model (`gemini-1.5-pro`) by default for AI-driven report generation. To switch to OpenAI (e.g., `gpt-3.5-turbo`), set `LLM_MODEL=openai` and provide an `OPENAI_API_KEY` in your environment variables.

## Contributions 🧑‍🔧👷‍♀️🏗️🏢

Contributions are welcome! It only takes five (5) steps!

To contribute:

1) Fork the repository.

2) Create a new branch: `git checkout -b my-feature-branch`.

3) Make your changes and commit them: `git commit -m 'Add some feature'`.

4) Push to the branch: `git push origin my-feature-branch`.

5) Open a pull request.

<p align="center" ><strong><em>Please read our <a href="https://github.com/daley-mottley/ai-insights/blob/main/CONTRIBUTION.md" >Contributing Guidelines</a> to get started!</em></strong> 🚀</p>


<a name="contributors"></a>
<h2 align="center">Say 'Hi' To Our Contributors!</h2>

<p align="center">
  <a href="https://github.com/daley-mottley">
    <img src="https://github.com/daley-mottley.png" width="100" height="100" style="border-radius: 50%;" alt="daley-mottley"/>
  </a>
  <a href="https://github.com/Devansh422">
    <img src="https://github.com/Devansh422.png" width="100" height="100" style="border-radius: 50%;" alt="Devansh422"/>
  </a>

</p>


<p align="center">🫶 <em>Thank you for your support! </em>🙌 </p>
<hr>
<h2 align="center"> 🌎 Let's Stay Connected 🫸🫷 </h2>

<p align="center"> If you like this project and would like to see more features or show your support.</p>
<p align="center"> Feel free to reach out to the developer(s) and give this project a ⭐!</p>

# AI Insights: Contributing Guidelines 📄

## Table of Contents
1. [Introduction](#introduction-)
2. [Tech Stack](#tech-stack-)
3. [Installation](#installation-)
4. [Contributing](#contributing-)
   - [Development Workflow](#development-workflow)
   - [Issue Report Process](#issue-report-process-)
   - [Pull Request Process](#pull-request-process-)
   - [Contributing Using GitHub Desktop](#contributing-using-github-desktop)
5. [Resources for Beginners](#resources-for-beginners-)
6. [Documentation](#documentation-)
7. [Code Reviews](#code-reviews-)
8. [Feature Requests](#feature-requests-)
9. [Spreading the Word](#spreading-the-word-)
10. [Code of Conduct](#code-of-conduct-)
11. [Thank You](#thank-you-)

## Introduction 🖥️

Welcome to **AI Insights**, a web-based application designed to provide valuable insights for your business using AI-driven analytics. The application leverages multiple data sources to deliver comprehensive reports and visualizations, helping users make data-driven decisions with ease. We are excited to have you contribute to our project! No contribution is too small, and we appreciate your help in improving this application.

## Tech Stack 🗃️

The project is built using the following technologies:

- [Python](https://www.python.org/) – The main programming language used for backend development.
- [Flask](https://flask.palletsprojects.com/) – A lightweight web framework used to build the web application.
- [OpenAI API](https://beta.openai.com/docs/) – Provides AI capabilities for natural language processing and generation features.
- [Google Sheets API](https://developers.google.com/sheets/api) – Used to interact with Google Sheets for data retrieval and manipulation.
- [MongoDB](https://www.mongodb.com/) – A NoSQL database for storing application data.
- [HTML/CSS/JavaScript](https://developer.mozilla.org/en-US/docs/Web/HTML) – Frontend technologies for building the user interface.
- [Bootstrap](https://getbootstrap.com/) – A CSS framework for responsive design and styling.
- [ProtonMail SMTP](https://protonmail.com/support/knowledge-base/protonmail-smtp-configuration/) – Used for sending emails securely from the application.

## Installation ⚙️

You can set up the **AI Insights** application by following these steps:

### Prerequisites

- **Python 3.x**
- **Poetry** package manager (or use `pip` if you prefer)
- **Google Sheets API credentials** (either through environment variables or a `credentials.json` file)
- **OpenAI API Key**
- **ProtonMail credentials**
- **MongoDB URI**

### Installation Steps

1. **Clone the repository:**

   ```
   git clone https://github.com/dmotts/ai-insights.git
   cd ai-insights
   ```

2. **Install dependencies:**

   ```
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

   ```
   python app.py
   ```

5. **Access the application:**

   Open your web browser and go to `http://localhost:5000` to view the application.

## Contributing 📝

We welcome contributions to **AI Insights**! Please follow these guidelines to ensure a smooth contribution process.

### Development Workflow

- **Work on a New Branch:** Always create a new branch for each issue or feature you are working on.
- **Keep Your Branch Up to Date:** Regularly pull changes from the main branch to keep your branch up to date.
- **Write Clear Commit Messages:** Use descriptive commit messages to explain what your changes do.
- **Test Thoroughly:** Ensure your changes work correctly and do not break existing functionality.
- **Self-Review:** Review your code before submitting to catch any errors or areas for improvement.

### Issue Report Process 📌

1. **Check Existing Issues:** Before creating a new issue, check if it has already been reported.
2. **Create a New Issue:** Go to the project's [issues section](https://github.com/dmotts/ai-insights/issues) and select the appropriate template.
3. **Provide Details:** Give a clear and detailed description of the issue.
4. **Wait for Assignment:** Wait for the issue to be assigned to you before starting work.

### Pull Request Process 🚀

1. **Ensure Self-Review:** Make sure you have thoroughly reviewed your code.
2. **Provide Descriptions:** Add a clear description of the functionality and changes in your pull request.
3. **Comment Your Code:** Comment on complex or hard-to-understand areas of your code.
4. **Add Screenshots:** Include screenshots or logs if they help explain your changes.
5. **Submit PR:** Submit your pull request using the provided template, and wait for the maintainers to review it.

### Contributing Using GitHub Desktop

If you prefer using GitHub Desktop, follow these steps:

1. **Open GitHub Desktop:** Launch GitHub Desktop and log in to your GitHub account.
2. **Clone the Repository:** Click on "File" > "Clone Repository" and select the repository to clone.
3. **Create a Branch:** Click on "Current Branch" and select "New Branch" to create a new branch for your work.
4. **Make Changes:** Edit the code using your preferred code editor.
5. **Commit Changes:**
   - In GitHub Desktop, select the files you changed.
   - Enter a summary and description for your commit.
   - Click "Commit to [branch-name]".
6. **Push Changes:** Click "Push origin" to push your changes to GitHub.
7. **Create a Pull Request:**
   - On GitHub, navigate to your forked repository.
   - Click on "Compare & pull request".
   - Review your changes and submit the pull request.
8. **Wait for Review:** Wait for the maintainers to review your pull request.

## Resources for Beginners 📚

If you're new to Git and GitHub, here are some resources to help you get started:

- [Forking a Repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
- [Cloning a Repo](https://help.github.com/en/desktop/contributing-to-projects/creating-an-issue-or-pull-request)
- [Creating a Pull Request](https://opensource.com/article/19/7/create-pull-request-github)
- [Getting Started with Git and GitHub](https://towardsdatascience.com/getting-started-with-git-and-github-6fcd0f2d4ac6)
- [Learn GitHub from Scratch](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)

## Documentation 📍

- **Update Documentation:** Document any significant changes or additions to the codebase.
- **Provide Clear Explanations:** Explain the functionality, usage, and any relevant considerations.
- **Use Comments:** Comment your code, especially in complex areas.

## Code Reviews 🔎

- **Be Open to Feedback:** Welcome feedback and constructive criticism from other contributors.
- **Participate in Reviews:** Help review others' code when possible.
- **Follow Guidelines:** Ensure your code meets the project's coding standards and guidelines.

## Feature Requests 🔥

- **Suggest Improvements:** Propose new features or enhancements that could benefit the project.
- **Provide Details:** Explain the rationale and potential impact of your suggestion.

## Spreading the Word 👐

- **Share Your Experience:** Share the project with others who might be interested.
- **Engage on Social Media:** Talk about the project on social media, developer forums, or relevant platforms.

## Code of Conduct 📜

Please note that we have a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Thank You 💗

Thank you for contributing to **AI Insights**! Together, we can make a significant impact. Happy coding! 🚀

Don't forget to ⭐ the repository!

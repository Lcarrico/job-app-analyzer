# Resume & Cover Letter Analyzer

This application analyzes resumes and cover letters against job descriptions using GPT-4o and provides visual scoring and suggestions for improvement.

## Requirements

- Python 3.12
- OpenAI API Key ([Get your API key here](https://platform.openai.com/signup/))

## Setup Instructions

1. **Clone the Repository**  
   Clone the repository from GitHub:
   ```bash
   git clone https://github.com/Lcarrico/job-app-analyzer.git
   cd job-app-analyzer
   ```

2. **Open the Project in VS Code**  
   Open the cloned folder in Visual Studio Code.

3. **Create a Virtual Environment in VS Code**  
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS).
   - Search for and select `Python: Create Environment`.
   - Choose `venv` as the environment type.
   - Select the Python 3.12 interpreter.

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage Instructions

1. **Open the Application**  
   After running the application, open the provided URL in your browser (e.g., `http://localhost:8501`).

2. **Enter Your OpenAI API Key**  
   Paste your OpenAI API key in the "🔑 OpenAI API Key" field. You can obtain your API key from [OpenAI](https://platform.openai.com/signup/).

3. **Input Data**  
   - **Resume**: Paste your resume in the "📄 Paste Resume" field.
   - **Cover Letter**: Paste your cover letter in the "✉️ Paste Cover Letter" field.
   - **Job Description**: Paste the job description in the "💼 Paste Job Description" field.

4. **Analyze**  
   Click the "Analyze" button to start the analysis.

## Application Sections

### Resume Match Breakdown
- **Overall Resume Score**: Displays the total score for your resume.
- **Category-by-Category Table**: Shows the required, matched, and missing items for each category, along with the percentage match.

### Visual Analysis
- **Match Progress by Category**: Displays progress bars for each category, showing how well your resume matches the job description.
- **Radar Chart**: Visualizes the category-wise match percentage.

### Skill Match Checklist
- Lists missing skills for each category, helping you identify areas for improvement.

### Cover Letter Rubric Breakdown
- **Overall Cover Letter Score**: Displays the total score for your cover letter.
- **Detailed Rubric Breakdown**: Provides an easy-to-read layout of each rubric category, its score, and the reason for the score.
- **Charts**: Includes a bar chart and radar chart for visualizing rubric scores.

### Suggestions
- Provides the top 3 actionable suggestions to improve your resume and cover letter.

## Notes
- Ensure all fields are filled before clicking "Analyze."
- The application uses GPT-4o for analysis, so an active OpenAI API key is required.
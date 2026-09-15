2.11
Development Environment & Workspace Setup

Hey Data Engineer! Hey Analyst!
Welcome. Before a single line of data analysis is written, there is work that determines whether your project survives contact with a real team. This lesson is about that work - building an environment and workspace that runs identically on every machine, where every dependency is documented, and where a new teammate can be productive from their first git clone.
Every data project that ever broke on deployment, caused confusion in a team handoff, or produced results nobody could reproduce had one thing in common: the environment was not managed deliberately. Python packages were installed globally, folder structure was improvised, and the README was written as an afterthought.
This lesson fixes that. You will walk away with a workspace pattern you can apply to every data project you build, that your team can trust, and that future-you will be grateful for.
The Real Scenario
THE PROBLEM
A three-person analytics team works on a customer segmentation project. One member installs pandas 2.0 for a different project, which breaks the segmentation project that was written against pandas 1.5. Another member runs the notebooks on Windows while the lead analyst uses macOS, and file paths crash on one machine. A new joiner asks how to set up the project and receives a Slack message with six manually typed steps that are already out of date. The project produces results nobody can reproduce because the environment is different on every machine.
THE SOLUTION
A deliberately managed workspace: an isolated virtual environment with all dependencies pinned in a requirements.txt, a folder structure every team member understands, a .gitignore that keeps secrets and generated files out of version control, and a README that lets any new joiner replicate the environment in four commands. This lesson builds that workspace from scratch.
Why Isolated Environments Matter
The Dependency Conflict Problem - and Why venv Solves It
WITHOUT A VIRTUAL ENVIRONMENT
All packages install into a single shared Python installation. Project A needs pandas 1.5. Project B needs pandas 2.0. Installing one breaks the other. Every pip install on your system potentially breaks every project you have worked on.
WITH A VIRTUAL ENVIRONMENT
Each project has its own isolated folder of installed packages. Project A has its own pandas 1.5. Project B has its own pandas 2.0. They never see each other. Installing or upgrading in one project never touches another.
What a virtual environment actually is
A virtual environment is a self-contained directory that holds a specific version of Python and a private collection of installed packages. It is created by Python itself using the built-in venv module. When you activate a virtual environment, every python and pip command runs against that isolated directory and nothing else.
Why this matters for team-based data projects
Reproducibility is the foundation of trustworthy data work. If your analysis runs on your machine with your packages but cannot be run by a colleague or by a CI server with different packages, your results are not reproducible. A virtual environment combined with a requirements.txt is the minimum viable guarantee that your environment can be recreated anywhere.
You just learned why isolated environments are essential for team-based data projects and what a virtual environment fundamentally does. Now you are going to learn exactly how to create, activate, and work inside a Python virtual environment across different operating systems.
Creating and Activating a Python venv
The Three Commands That Create Your Isolated World
Step 1 - Create the virtual environment
Run this command in your project root directory. The second venv is the name of the folder that will be created to hold your environment. This name is conventional - you can change it, but venv is what every team member expects to see.
# macOS and Linux
python3 -m venv venv
 
# Windows
python -m venv venv
Step 2 - Activate the virtual environment
Activating changes your terminal session so that all Python and pip commands now point to the isolated environment instead of the global Python installation. You will see the environment name appear at the start of your terminal prompt when it is active.
# macOS and Linux
source venv/bin/activate
 
# Windows Command Prompt
venv\Scripts\activate
 
# Windows PowerShell
venv\Scripts\Activate.ps1
Step 3 - Deactivate when done
When you finish working on the project, deactivate the environment to return your terminal to the global Python installation. This command is the same on every operating system.
deactivate
ACTIVE ENVIRONMENT PROMPT
When your venv is active, your terminal prompt changes. You will see the environment name in parentheses before your usual prompt, like this:
(venv) your-machine:project $
WHAT LIVES INSIDE THE VENV FOLDER
The venv folder contains a copy of Python, a pip executable, and all packages you install. It is large and machine-specific - never commit it to version control. That is what requirements.txt is for.
Always activate before installing packages
If you run pip install without activating your venv first, the package installs into your global Python - exactly the problem you were solving. Make activating the first thing you do when you open a terminal for any project.
You just learned how to create, activate, and deactivate a Python virtual environment on every major operating system, and what the activated prompt looks like. Now you are going to learn how to structure your project folders so your team always knows where to find data, scripts, notebooks, and outputs.
Designing a Data Project Folder Structure
A Folder Convention Every Data Team Member Understands Immediately
The standard data project layout
customer-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
├── output/
├── venv/              ← never committed
├── .env               ← never committed
├── .gitignore
├── requirements.txt
└── README.md
data/raw/
Source data exactly as received - never modify files here
customer_transactions.csv, sales_2024.xlsx, survey_responses.json. These files are the source of truth for your analysis. If you transform raw data in place, you permanently lose the ability to retrace your steps. Raw is sacred.
data/processed/
Cleaned and transformed data ready for analysis
cleaned_customers.csv, merged_sales.csv. Every script and notebook reads from here, not from raw. Any team member can regenerate processed data from raw using your cleaning scripts - which means processed files are reproducible and do not need to be committed if they are large.
notebooks/
Jupyter notebooks for exploration and reporting - numbered in order
01_exploratory_analysis.ipynb, 02_feature_engineering.ipynb, 03_final_report.ipynb. Number notebooks so they communicate logical order. Notebooks are for thinking and presenting - not for production code. Complex reusable logic belongs in scripts.
scripts/
Python scripts for repeatable, automatable operations
clean_data.py, train_model.py, generate_report.py. Scripts are meant to be run the same way every time, by any team member, without modification. This is your pipeline code - it should be clean, documented, and runnable from the command line.
output/
Generated files - reports, figures, predictions, exports
report.pdf, figures/churn_by_segment.png, predictions.csv. Output is always regenerable from your scripts and data. Never treat output as source-of-truth - treat the scripts that produce it as source-of-truth. Large output files are typically gitignored.
You just learned the standard data project folder structure and the engineering reasoning behind every directory. Now you are going to learn how to document and manage your project dependencies using requirements.txt so any teammate can recreate your exact environment.
Managing Dependencies with requirements.txt
The File That Makes Your Environment Reproducible Anywhere
What requirements.txt contains
A plain text file listing every package your project depends on, one per line, with the exact or compatible version. This is the instruction file - when a teammate runs pip install -r requirements.txt, they get exactly your environment.
pandas==2.1.4
numpy==1.26.2
matplotlib==3.8.2
seaborn==0.13.0
jupyter==1.0.0
scikit-learn==1.3.2
python-dotenv==1.0.0
openpyxl==3.1.2
How to generate it with pip freeze
pip freeze prints all installed packages in your current environment with their exact versions. Redirect that output to requirements.txt to capture your environment at any moment.
# Activate your venv first, then run:
pip freeze > requirements.txt
 
# To verify what was captured:
cat requirements.txt
Run this command every time you install a new package. Commit the updated requirements.txt immediately - an out-of-date requirements.txt is almost as bad as no requirements.txt.
How a teammate uses it
A new team member clones the repository, creates their own virtual environment, activates it, and then installs everything from requirements.txt in one command. Their environment is now identical to yours.
git clone https://github.com/team/customer-analytics.git
cd customer-analytics
python3 -m venv venv
source venv/bin/activate          # or venv\Scripts\activate on Windows
pip install -r requirements.txt
== (EXACT VERSION)
pandas==2.1.4 installs exactly 2.1.4 and nothing else. Maximum reproducibility. The team always uses the same version. Recommended for production and team projects.
>= (COMPATIBLE VERSION)
pandas>=2.0.0 installs 2.0.0 or any newer version. More flexible but less reproducible. Different teammates may get different versions. Use for library packages that tolerate wider ranges.
You just learned how requirements.txt captures your environment, how to generate it with pip freeze, and how teammates use it to replicate your setup exactly. Now you are going to learn which files must never go into version control and how to configure .gitignore to keep your repository clean and your secrets safe.
Version Control Hygiene with .gitignore
Keeping Secrets, Machines, and Clutter Out of Your Repository
The .gitignore file in your project root
A .gitignore file tells Git which files and folders to never track. Once a pattern is in .gitignore, Git ignores matching files entirely - they never appear in git status, never get staged, and never get committed. This is how you prevent sensitive and machine-specific files from accidentally ending up in your repository.
# Virtual environment - machine-specific, never commit
venv/
.venv/
 
# Secrets and credentials - NEVER commit these
.env
*.key
*.pem
 
# Python cache files - auto-generated, not useful to teammates
__pycache__/
*.pyc
*.pyo
 
# Jupyter notebook checkpoints - auto-saved drafts, not needed in repo
.ipynb_checkpoints/
 
# macOS system files - irrelevant to teammates on other systems
.DS_Store
 
# Large output files - regenerable from scripts
output/*.csv
output/*.pdf
 
# Distribution and build artifacts
*.egg-info/
dist/
build/
Why venv/ must be excluded
The venv folder is large (hundreds of megabytes), machine-specific (compiled for your exact OS and CPU), and entirely regenerable from requirements.txt. Committing it would make your repository enormous, break for teammates on different systems, and make it impossible to track actual code changes in version history.
Why .env must be excluded - this one is critical
The .env file stores secrets: database passwords, API keys, internal service credentials. Committing a .env file to a public repository has caused real security incidents at real companies. Git history is permanent - removing a committed secret requires rewriting history, which breaks everyone who cloned the repository. Add .env to .gitignore before writing a single secret into it.
Why .ipynb_checkpoints/ must be excluded
Jupyter auto-saves notebook snapshots into a hidden .ipynb_checkpoints folder every few minutes. These checkpoints are personal draft saves - not the notebook itself. Committing them creates noise in pull requests, causes merge conflicts between teammates, and bloats repository size with redundant content.
You just learned what belongs in .gitignore, why each category of file must be excluded, and especially why the .env file must never reach version control. Now you are going to learn the final piece: writing a README that lets any team member replicate your workspace from scratch without asking a single question.
README Documentation for Team Handoff
The First File Anyone Reads - Make It Do Real Work
What a README must answer
A README for a data project must answer four questions for a new team member: what does this project do, how do I set up the environment, what is in each folder, and how do I run the analysis. If any of these four questions requires asking someone, the README is incomplete.
A standard README structure for data projects
# Customer Segmentation Analysis
 
Segments customers by purchase behaviour using K-means clustering
on the 2024 transaction dataset. Outputs include segment profiles
and an interactive HTML report.
 
## Setup
 
1. Clone the repository
   git clone https://github.com/team/customer-analytics.git
   cd customer-analytics
 
2. Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
 
3. Install dependencies
   pip install -r requirements.txt
 
4. Configure environment variables
   Copy .env.example to .env and fill in your database credentials
 
## Project Structure
 
data/raw/       Source data - never modified
data/processed/ Cleaned data ready for analysis
notebooks/      Jupyter exploration and reporting notebooks
scripts/        Repeatable Python scripts
output/         Generated reports and figures
 
## Running the Analysis
 
python scripts/clean_data.py          # Produces data/processed/
python scripts/run_segmentation.py    # Produces output/
jupyter notebook notebooks/           # Open interactive notebooks
README TEST - THE 4-COMMAND RULE
A good README passes this test: give it to someone who has never seen the project and ask them to set it up. If they can do it in four commands or fewer without asking a question, your README works. If they need to ask anything, update the README before moving on.
INCLUDE A .ENV.EXAMPLE FILE
Commit a .env.example that shows every required environment variable with placeholder values. Never commit the real .env. This gives teammates the structure they need without exposing any secrets. It is the correct pattern for all projects that use configuration variables
You have joined a newly formed data product team working across multiple business problem statements such as delivery delays, customer churn, payment failures, operational inefficiencies, employee performance tracking, infrastructure monitoring, sales analytics, and user engagement analysis.
Although each team is solving a different business problem, all teams face the same foundational issue: there is no standardized analytics workspace. Team members are installing packages globally, committing unnecessary files into repositories, storing secrets directly inside scripts, and using inconsistent folder structures that make collaboration difficult.
Before any analysis, dashboards, SQL workflows, or predictive insights can begin, your team must first establish a professional analytics development environment that every contributor can use consistently.
Your task is to build the shared project foundation from scratch - creating an isolated Python environment, defining a scalable project structure, protecting secrets properly, capturing dependencies, and documenting a setup process that allows any new team member to replicate the workspace without confusion.
This assignment is not focused on solving the business problem itself yet. It is focused on building the engineering and analytics foundation required before real Data Product Development can begin.
Getting Started
Create your working branch:
git checkout -b setup/dev-environment
Everything you build will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Create the Virtual Environment and Install Dependencies
Create a Python virtual environment inside your project directory using the built-in venv module:
# macOS and Linux
python3 -m venv venv
 
# Windows
python -m venv venv
Activate your environment:
# macOS and Linux
source venv/bin/activate
 
# Windows
venv\Scripts\activate
Install the following packages, which represent a standard data analytics stack:
pip install pandas numpy matplotlib seaborn jupyter scikit-learn python-dotenv openpyxl
Confirm the environment is working by running python -c "import pandas; print(pandas.__version__)" without errors. You will capture these dependencies in Task 4.
Task 2 - Create the Project Folder Structure
Inside your repository root, create the following directory structure. Each directory must exist and contain at least one file so Git tracks it - use an empty .gitkeep file or a brief markdown file explaining the directory purpose:
analytics-workspace-setup/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
├── output/
In each directory, add a brief markdown file (for example data/raw/README.md) explaining what belongs there. One sentence per directory is sufficient. This documents the convention for future team members.
Task 3 - Create a .gitignore File
Create a .gitignore file at the root of your repository. It must exclude at minimum:
The virtual environment folder (venv/ and .venv/), the .env file that will hold secrets, Python cache files (__pycache__/ and *.pyc), Jupyter notebook checkpoint folders (.ipynb_checkpoints/), and any operating system artifacts (.DS_Store on macOS, Thumbs.db on Windows).
You may use gitignore.io at https://www.toptal.com/developers/gitignore to generate a complete Python and Jupyter gitignore as a starting point, then review and customize it for this project.
Confirm the gitignore is working by verifying that git status does not list the venv folder after you commit.
Task 4 - Capture Dependencies in requirements.txt
With your virtual environment still active, generate a requirements.txt file using pip freeze:
pip freeze > requirements.txt
Open the file and verify it lists all the packages you installed in Task 1 with their exact version numbers. Commit this file to your repository.
To confirm the requirements.txt works, test it in a clean environment: create a second virtual environment in a temporary folder outside your project, activate it, and run pip install -r requirements.txt. If it installs without errors, your requirements.txt is correct.
Task 5 - Write the README
Create a README.md at the project root. It must contain four sections:
A brief project description explaining what this workspace is for. A Setup section with numbered steps to clone the repo, create the virtual environment, activate it, and install dependencies - using exact commands that work on both macOS/Linux and Windows. A Project Structure section listing each directory and its purpose in one sentence. A Notes section that mentions what environment variables are needed and that a teammate should copy .env.example to .env and fill in their own values.
Also create a .env.example file at the project root showing the structure of required environment variables with placeholder values. This file should be committed. The actual .env file should not be.
When your README is complete, test it using this rule: give the README to someone who has not seen the project and check whether they can set up the environment without asking you a single question.
Once all five tasks are done, commit everything with a clear message and push:
git add .
git commit -m "setup: create venv, folder structure, gitignore, requirements.txt, and README"
git push origin setup/dev-environment
Open a PR from setup/dev-environment to main in your forked repository.
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/analytics-workspace-setup/pull/[number]
The PR must be publicly accessible. The repository must not contain your venv folder or any .env file with real values. The requirements.txt, .gitignore, folder structure, and README must all be visible in the PR diff.
2. Video explanation
Record a 3–5 minute screen-share covering all five of the following points. These map directly to the video rubric, so cover each one clearly:
Explain what a virtual environment is and why it matters for a team working on a shared data project. Walk through each directory in your folder structure and explain in one sentence what belongs there and why it is separate from the others. Show your requirements.txt, explain what it contains, and demonstrate or explain how to regenerate it using pip freeze. Show your .gitignore and explain why the venv folder, the .env file, and the notebook checkpoints must be excluded from version control. Answer this question in the video as if a new teammate is asking: how would they replicate this environment on their machine from scratch, starting from a fresh git clone.
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Development Environment & Workspace Setup

2.12
GitHub Repository & Team Workflow Setup

Hey Analyst!
Welcome. Now that your workspace is isolated and documented, it is time to establish how your team will actually work together on the same codebase. This is not about writing code yet - it is about establishing the workflow that prevents chaos when multiple people are editing the same repository simultaneously.
Real teams do not work directly on the main branch. They use branching strategies, issue tracking, code review in pull requests, and commit message conventions. These practices sound tedious until the moment your code breaks production and you cannot tell who changed what or why. Then they are not tedious - they are survival.
This lesson is about building that workflow from the ground up. You will walk away understanding why branching matters, how GitHub issues drive sprint work, what a pull request actually controls, and how to write commit messages that tell the story of your code changes.
The Real Scenario
THE PROBLEM
A three-person analytics team starts work on a customer churn prediction model. All three members push to the main branch directly. One member changes the data schema, another rewrites the model training logic, and a third adds a new feature. Nobody knows the changes are conflicting until the entire pipeline breaks. There is no record of why each change was made, the code has not been reviewed by anyone before it reached production, and rolling back is a disaster.
THE SOLUTION
A deliberate branching strategy: each team member works on a feature branch, creates a pull request when ready, has the code reviewed by at least one teammate, and only merges to main after approval. Issues track what work needs to be done and who is doing it. Commit messages explain not just what changed but why. When the churn model breaks, the entire history of decisions is visible and rollback is surgical, not chaotic.
Why Branch Strategy Matters
Isolation, Safety, and Parallel Work
WITHOUT BRANCHING
Everyone commits directly to main. Work is not isolated - one person is always blocked by another or working blind about what others are doing. Broken code reaches main continuously. Code review never happens because nothing exists to review. Rolling back a bad change requires digging through history. Parallel work is impossible.
WITH BRANCHING
Each person works on their own branch. Work is isolated - one person working slower does not block others. Broken code stays in a branch and never touches main. Code review happens in pull requests before merge. Rolling back is a single revert commit. Multiple people can work on different features simultaneously.
What a branch fundamentally is
A branch is a parallel timeline of commits. Main is one timeline that always stays releasable. A feature branch is another timeline that starts from main and can be worked on independently. Two branches can diverge - different changes on each - and later be merged back together. A branch is cheap, easy to create, and the default way to organize work in any professional repository.
Why branch naming conventions matter
A branch named feature/churn-model tells you immediately what work is happening. A branch named my-new-code tells you nothing. When dozens of branches exist in a large project, naming conventions make it possible to navigate without confusion.
You just learned why branch isolation is essential for team work and what branch naming conventions communicate to your teammates. Now you are going to learn how to create branches, push them, and establish a naming convention that scales.
GitHub Issues and Sprint Task Tracking
Turning Work Into Trackable, Assignable Tasks
What a GitHub issue represents
An issue is a trackable unit of work - a bug to fix, a feature to build, a question to answer. Issues have titles, descriptions, assignees (who is doing it), labels (what category of work), and status (open, in progress, closed). In a well-run team, no code changes without a corresponding issue. This creates a permanent record of why every line was written.
Issue title
Concise and action-oriented
"Implement data validation script for intake" not "validation"
Description
The context someone needs to understand the work
Why this task exists, what success looks like, any specific requirements or constraints.
Labels
Categorise work type and urgency
feature, bug, documentation, high-priority, in-progress. Labels let you filter and understand work volume at a glance.
Assignee
Who is responsible for completing this work
One person accountable. This prevents work from falling between people and makes it clear who to ask for questions.
You just learned what an issue is, what information an issue must contain, and why issues drive the relationship between branches and commits. Now you are going to learn how pull requests use issues to establish code review and merge control.
Pull Requests and Code Review
The Structured Conversation That Prevents Bad Code From Reaching Main
What a pull request actually does
A pull request says: I have work on a feature branch and I want to merge it into main. Before I do, I am asking my team to review the code. Here is what changed, here is why, here is the issue it solves. A pull request creates a mandatory stop point - code does not reach main until a reviewer approves it. That review catches logic errors, prevents duplicated work, ensures code quality, and creates a permanent record of decisions.
The pull request workflow
1. You make changes on feature/my-feature branch
2. You push to GitHub
3. You open a PR on GitHub with title and description
4. You link the related issue with "Closes #123"
5. A teammate reviews your code and leaves feedback
6. You update your commits based on feedback
7. The reviewer approves when satisfied
8. You merge the PR into main
9. The feature branch is deleted
10. The issue is automatically closed
Always link issues to PRs
In your PR description, type "Closes #123" where 123 is the issue number. GitHub automatically links them and closes the issue when the PR merges. This creates a permanent connection between the work request and the code that fulfilled it.
You just learned what a pull request controls and why code review creates quality gates. Now you are going to learn how to write commit messages that tell the story of your changes for future teammates.
Commit Message Conventions
Writing Messages That Communicate Intent, Not Just Activity
The conventional commit format
A conventional commit has a structured format that lets tools parse it automatically and humans understand it instantly. It separates the type of change from a human-readable description. Every team member recognizes the pattern immediately.
[type]: [description]

[optional body]
[optional footer]

Examples:
feat: add data validation schema checker
fix: correct null percentage calculation in profiler
docs: update README with dataset intake process
refactor: extract column renaming logic into utils
test: add unit tests for date parser
FEAT
A new feature or capability. Use when you add new code that solves a problem.
FIX
A bug fix or correction. Use when you repair broken logic.
DOCS
Documentation changes only, no code changes.
REFACTOR
Code cleanup without changing behavior.
You just learned the complete workflow: branch creation, issue tracking, pull requests, code review, and commit messages that tell a story. This is how professional teams prevent chaos and maintain trustworthy code.
GitHub Repository & Team Workflow Setup


00h 59m 53s

Your data product team has created an isolated virtual environment and established a project structure. Now you must establish how the team works together on code - defining a branching strategy, tracking work with issues, conducting code reviews in pull requests, and maintaining commit message consistency.
Without these workflows, multiple team members editing the same codebase leads to merge conflicts, lost context about why code was written, broken production pipelines, and confusion about who is responsible for what. This assignment establishes the professional GitHub workflow that makes collaboration predictable and recoverable.
Getting Started
Create your working branch:
git checkout -b feature/github-workflow-setup
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Create At Least Three GitHub Issues
Create three GitHub issues in your repository representing sprint-level analytical tasks. Each issue must have:
* A clear, action-oriented title (not vague - "Implement data validation" not "validation")
* A description explaining why this work matters and what done means
* At least one label (e.g., "feature", "documentation", "data-pipeline")
* An assignee (assign to yourself)
Example issue titles:
* "Ingest customer transaction data into pipeline"
* "Create data quality report for incoming datasets"
* "Document data dictionary for team reference"
These issues do not need code yet - they are workflow placeholders. Commit screenshots or links to these issues with your PR.
Task 2 - Create a Feature Branch With Naming Convention
Create a feature branch following professional naming conventions:
# Example patterns - choose one of these
git checkout -b feature/data-ingestion
git checkout -b fix/validation-logic
git checkout -b docs/data-dictionary
Use the pattern [type]/[short-description] where type is one of: feature, fix, docs, refactor, or chore.
Commit this branch with at least one dummy file or comment change to make the branch visible:
echo "# Data workflow placeholder" > WORKFLOW.md
git add WORKFLOW.md
git commit -m "feat: start data workflow documentation"
git push origin feature/data-ingestion
Task 3 - Write Commit Messages Following a Convention
Make at least three commits on your feature branch. Each commit message must follow this format:
[type]: [description]

[optional body explaining why]
Types: feat (feature), fix (bug fix), docs (documentation), refactor, test, chore
Examples:
git commit -m "feat: add data validation function

Validates incoming CSV files for schema completeness and encoding.
Checks column names, data types, and row counts before processing."

git commit -m "docs: document branching strategy for team"

git commit -m "chore: update requirements.txt with validation library"
Make these commits on your feature branch and push them:
git push origin feature/data-ingestion
Task 4 - Create a Pull Request With Clear Context
When your feature branch is ready, create a Pull Request from your feature branch to main. The PR description must include:
1. A clear title (not "Update code" - use "Add data validation workflow and team branching guidelines")
2. A description explaining what changed and why
3. A link to at least one of the GitHub issues created in Task 1 (use "Closes #[issue-number]" or "Fixes #[issue-number]")
4. A summary of commit messages (paste or summarize what each commit does)
Example PR description:
## Summary
Establishes the data ingestion workflow and documents branching strategy for team collaboration.

## What Changed
- Added data validation function to check incoming CSV schema
- Documented feature branch naming convention
- Updated requirements.txt with validation dependencies

## Related Issue
Closes #1 - Ingest customer transaction data into pipeline

## Testing
Validation function tested with sample CSV files. No errors on valid files, appropriate errors on invalid schema.
Do not merge the PR yet - leave it open for review. Commit the PR URL.
Task 5 - Document Your Branching and Commit Strategy
Create a WORKFLOW.md file at the project root documenting:
1. Your team's branching strategy
    * Main branch holds releasable code only
    * Feature branches follow feature/[description] naming
    * Branches are deleted after merge
2. Your team's commit message convention
    * Types used: feat, fix, docs, refactor, chore
    * Format: [type]: [description]
    * Why: Enables automated changelog generation and clear history
3. Your PR review process
    * PRs require at least one approval before merge
    * Code review focuses on: correctness, clarity, data integrity, and test coverage
    * Commit messages are reviewed as part of code review
4. Your GitHub issue tracking approach
    * Every feature or fix starts with an issue
    * Issues have labels, assignees, and descriptions
    * Issues are closed when the corresponding PR is merged
Commit this file:
git add WORKFLOW.md
git commit -m "docs: document team github workflow and conventions"
git push origin feature/data-ingestion
Submission
Submit three things together. Missing any one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must be publicly accessible and open (not merged). It must show:
* Your feature branch with at least 3 commits
* Clear commit messages following the convention
* Clear PR description with issue links
* A WORKFLOW.md file documenting your team's approach
2. Screenshots or Links of GitHub Issues
Provide links to the three issues you created. Each must have:
* Title, description, label, and assignee visible
* Demonstrates the issue is trackable and assignable
Format (paste in submission):
Issue 1: https://github.com/YOUR-USERNAME/data-product-pipeline/issues/1
Issue 2: https://github.com/YOUR-USERNAME/data-product-pipeline/issues/2
Issue 3: https://github.com/YOUR-USERNAME/data-product-pipeline/issues/3
3. Video Explanation
Record a 3–5 minute screen-share covering all five of these points:
1. Explain your branching strategy - why you use feature branches and why main branch stays clean
2. Walk through one GitHub issue and explain what information is tracked and why each field (title, description, label, assignee) matters
3. Show your commit history and explain what the message format communicates and why you chose that convention
4. Show your PR description and explain how issue links keep code changes connected to their context
5. Answer this question: If a teammate opens a fresh clone of your repository, what steps would they follow to contribute a new feature without breaking main?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.13
Python Data Workflow Foundations

Hey Data Engineer!
Welcome. Your workspace is isolated. Your team workflows are defined. Now comes the critical transition from notebook-based exploration to production-ready Python scripts. Data products do not run inside Jupyter cells - they run as modular scripts that your CI/CD pipeline executes, that your team understands without explanation, and that you can schedule to run automatically when new data arrives.
Every data project that ever had to be rewritten for production, that broke when someone tried to automate it, or that nobody on the team could understand had one thing in common: the analysis was written as an exploratory notebook, not as a production script. Notebooks are thinking tools. Scripts are execution engines. You need both - but at different times.
This lesson fixes that gap. You will walk away understanding when to use notebooks versus scripts, how to structure a script so it separates concerns, and how to write code that future teammates can understand and maintain.
The Real Scenario
THE PROBLEM
An analyst writes a beautiful Jupyter notebook exploring customer churn prediction. The notebook is thorough - data loading, cleaning, feature engineering, model training, evaluation, visualizations. Everything works perfectly when she runs it. Then a business stakeholder asks: "Can you run this every Monday and email me the results?" The analyst panics. Jupyter notebooks require a human to click "Run All". There is no way to schedule them. The notebook mixes exploration with business logic - you cannot tell which parts are important and which were dead ends. Three months later, a new team member inherits the project and spends a week trying to understand what the notebook does and how to modify it.
THE SOLUTION
The same analysis written as a structured Python script with modular functions. One function loads and validates data. One function engineers features and trains the model. One function produces the output report. Each function has a single responsibility. The script runs from the command line with a single execution. A cron job calls it every Monday morning. A new team member reads the script and understands what happens because each section is clearly separated. The business can modify parameters without touching code.
Notebooks vs Scripts: When to Use Each
The Different Jobs They Do
NOTEBOOKS ARE FOR
Exploring data. Testing hypotheses. Trying different approaches quickly. Visualizing results. Presenting findings to stakeholders with code and output side-by-side. Learning new techniques. Documenting your thinking process. Anything where you need to iterate rapidly and get immediate feedback.
SCRIPTS ARE FOR
Running repeatable operations. Automating pipelines. Processing new data as it arrives. Integrating with CI/CD systems. Accepting parameters from external systems. Operating on a schedule without human intervention. Anything that must run reliably the same way every time.
The Workflow: Notebooks Feed Scripts
The right approach is (1) Explore in a notebook - try things, visualize, understand the problem. (2) Once you know what works, extract the logic into a production script with functions. (3) Test the script - make sure it runs reliably from command line. (4) Schedule the script - let it run automatically. (5) Version control both - but the script is what people depend on. Notebooks are your thinking space. Scripts are your production guarantee.
You just learned the difference between notebooks (thinking) and scripts (production), and when each is appropriate. Now you are going to learn how to structure a script using the three-function pattern that separates concerns and makes code maintainable.
The Three-Function Pattern: Ingest, Process, Output
The Structure That Makes Code Maintainable and Testable
Function 1: Ingest Data
This function reads data from a source - a CSV file, database query, API endpoint, cloud storage bucket - and returns a Pandas DataFrame. It does not transform. It does not filter. It only reads and returns. This separation is critical because if your data source changes (you migrate from CSV to database), you only rewrite this one function. All the downstream logic stays exactly the same. The processing logic is completely decoupled from how you get the data.
Function 2: Process Data
This function receives the ingested data and applies all business logic: cleaning, filtering, calculations, aggregations, feature engineering, model training. It transforms raw data into analysis-ready or prediction-ready form. This is where the actual work happens. It should be testable in isolation - you pass it a DataFrame, it returns a transformed DataFrame, with no side effects. No file I/O. No database queries. Just pure transformation.
Function 3: Output Results
This function takes processed results and writes them somewhere: a CSV file, database table, HTML report, email, Slack notification, visualization. It does not perform analysis. It delivers results. Separating this function means you can easily change where results go without touching your analysis logic. Need to write to database instead of CSV? Change this function only.
WHY THIS MATTERS
Three separate functions mean three independent pieces you can test in isolation. You can test data loading without running the full pipeline. You can test transformation logic with a small test DataFrame. You can change output format without touching analysis code.
WHAT NOT TO DO
Never combine concerns into one function. One function that reads data AND transforms it AND writes output is a disaster. When it fails, you do not know which step broke. When you want to change the data source, you risk breaking the transformation. When your database is down, your entire pipeline stops.
You just learned the three-function pattern that separates concerns and makes code maintainable. Now you will learn how to structure a complete script using this pattern, with configuration at the top and a main execution block.
Script Structure: Organization and Clarity
How Production Scripts Are Organized
The standard script structure
Every production script should follow this order: (1) Imports at the top. (2) Configuration and constants. (3) Helper and utility functions. (4) The three main functions (ingest, process, output). (5) A main execution block that orchestrates the workflow. (6) Error handling.
# 1. IMPORTS - Everything the script needs at the top
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# 2. CONFIGURATION - Hard-coded paths, settings, thresholds
INPUT_FILE = "data/raw/sales.csv"
OUTPUT_FILE = "output/processed_sales.csv"
LOG_FILE = "logs/workflow.log"
MIN_AMOUNT = 0
CHURN_THRESHOLD_DAYS = 90

# 3. LOGGING SETUP - Capture what happens for debugging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 4. MAIN FUNCTIONS

def ingest_data(filepath):
    """Read CSV file into DataFrame."""
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Ingested {len(df)} rows from {filepath}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        raise

def process_data(df, min_amount=0):
    """Apply transformations to data."""
    rows_before = len(df)
    
    df = df.drop_duplicates()
    df = df[df['amount'] >= min_amount]
    df['amount'].fillna(df['amount'].median(), inplace=True)
    
    rows_after = len(df)
    logging.info(f"Processing: {rows_before} rows → {rows_after} rows")
    return df

def output_results(df, filepath):
    """Write results to file."""
    df.to_csv(filepath, index=False)
    logging.info(f"Output saved: {filepath}")
    print(f"✓ Processed {len(df)} records")

# 5. MAIN EXECUTION - Orchestrate the workflow
if __name__ == "__main__":
    try:
        print("Starting workflow...")
        data = ingest_data(INPUT_FILE)
        clean_data = process_data(data, min_amount=MIN_AMOUNT)
        output_results(clean_data, OUTPUT_FILE)
        print("✓ Workflow completed successfully")
    except Exception as e:
        logging.error(f"Workflow failed: {str(e)}")
        print(f"Error: {str(e)}")
        exit(1)
Imports First
All imports at the top so you can see dependencies immediately
Someone reading your code can understand what libraries you depend on without scrolling. Makes it easy to check requirements.txt or add missing dependencies.
Configuration Next
All hard-coded values in one place before any functions
Easy to modify without touching function logic. Makes the script flexible for different scenarios (different input file, different thresholds).
Main Execution Last
The if name == "main": block at the end
This pattern allows the script to be imported by other scripts without auto-executing. Makes the script reusable as a module, not just a standalone command.
Logging is not optional
Your script runs on a server without anyone watching. It fails at 3 AM. How do you know what happened? Logging. Every important operation should log: what was loaded, how many rows were processed, where output was saved, what errors occurred. The log file is your forensic evidence when things go wrong.
You just learned how to structure a production script with configuration, functions, and main execution. Now you are going to learn how to document your functions so future team members understand what they do without asking.
Docstrings and Comments: Communicating Intent
Making Your Code Understandable Without Explanation
Every function needs a docstring
A docstring is a multi-line description at the top of every function explaining what it does, what it expects, and what it returns. This is formal documentation, not a comment. Someone reading the code can understand the function without reading the implementation.
def calculate_customer_value(df, recency_days=365):
    """
    Calculate lifetime value score for each customer.
    
    Higher scores indicate customers more likely to purchase soon.
    Score is based on recency (recent purchases weighted higher),
    frequency (repeat customers scored higher), and monetary value.
    
    Args:
        df (pd.DataFrame): Customer transaction history with columns:
            - customer_id (int): Unique customer identifier
            - transaction_date (datetime): Date of transaction
            - amount (float): Transaction amount in dollars
        recency_days (int): Window for recent purchase (default: 365)
    
    Returns:
        pd.Series: Customer value scores (0-100) indexed by customer_id
    
    Raises:
        ValueError: If DataFrame is empty or missing required columns
    
    Example:
        >>> df = pd.DataFrame({
        ...     'customer_id': [1, 2, 3],
        ...     'transaction_date': ['2025-01-01', '2025-05-15', '2024-01-01'],
        ...     'amount': [100, 250, 50]
        ... })
        >>> calculate_customer_value(df).head()
        customer_id
        1    75
        2    95
        3    20
    """
    if df.empty:
        raise ValueError("Input DataFrame cannot be empty")
    
    # Implementation here
    pass
Inline comments for non-obvious logic
Do not comment what the code does - the code does that. Comment why you chose this approach or what business reasoning justifies the logic. Explain constraints and edge cases.
# Keep only customers with at least one transaction in past 90 days
# Dormant customers distort cohort analysis, so we segment them separately
df_active = df[df['days_since_last_purchase'] < 90]

# Use median, not mean, because high-value purchases create outliers
# Median is resistant to outliers and represents typical customer value
fill_value = df['transaction_amount'].median()
df['amount'].fillna(fill_value, inplace=True)
You just learned how to structure a production script with clear separation of concerns, proper documentation, and logging. This is the foundation of professional data engineering. You now have the pattern you apply to every data workflow you build.
Python Data Workflow Foundations


00h 59m 53s

Your analytics team has established a professional GitHub workflow. Now you must transition from notebook-based exploration to production-ready Python scripts. Real data pipelines do not run inside Jupyter notebooks - they run as modular, reusable scripts that can be executed from the command line, scheduled in CI/CD systems, and maintained by future team members who will never read your notebook cells.
Your task is to convert a data workflow into a structured Python script that separates concerns across ingestion, processing, and output stages, runs without errors from the command line, and documents each operation clearly. This script becomes the foundation of your data product pipeline.
Getting Started
Create your working branch:
git checkout -b feature/python-workflow-script
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Create a Python Script With Separated Concerns
Create a file scripts/data_workflow.py that performs a complete data pipeline from ingestion to output. The script must have at least three functions separating different concerns:
Function 1: Ingest - Read data from a file (CSV or JSON)
def ingest_data(filepath):
    """Load data from a file and return a Pandas DataFrame."""
    import pandas as pd
    df = pd.read_csv(filepath)
    return df
Function 2: Process - Transform the data (cleaning, filtering, calculation)
def process_data(df):
    """Apply transformations to the dataset."""
    # Remove duplicates, fill nulls, filter rows, add columns, etc.
    df = df.drop_duplicates()
    return df
Function 3: Output - Write results to a file or standard output
def output_results(df, output_path):
    """Save processed data to a file."""
    df.to_csv(output_path, index=False)
    print(f"Output saved to {output_path}")
Main execution block:
if __name__ == "__main__":
    data = ingest_data("data/raw/sample.csv")
    processed = process_data(data)
    output_results(processed, "output/processed.csv")
The script must run from the command line with a single execution:
python scripts/data_workflow.py
Task 2 - Add Inline Comments Explaining Each Function
Add docstrings and inline comments to every function explaining:
* What the function does
* What data it expects as input
* What it returns
* Any assumptions or constraints
Example:
def process_data(df):
    """
    Transform raw data into analysis-ready format.
    
    Input: Pandas DataFrame with raw data
    Output: Pandas DataFrame with nulls filled, duplicates removed
    """
    # Remove exact duplicates (rows where all values are identical)
    df = df.drop_duplicates()
    
    # Fill missing values in numerical columns with median
    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].median(), inplace=True)
    
    return df
Task 3 - Ensure the Script Runs Without Errors
Test your script from the command line:
cd scripts
python data_workflow.py
The script must complete without errors. If it does error, the error message must clearly indicate what failed and why. Capture a screenshot showing successful execution.
Task 4 - Include Sample Output Confirming Execution
Your script must print output confirming successful execution:
def output_results(df, output_path):
    """Save processed data and print confirmation."""
    df.to_csv(output_path, index=False)
    print(f"✓ Data successfully processed")
    print(f"✓ Rows processed: {len(df)}")
    print(f"✓ Output saved to {output_path}")
Sample output should look like:
✓ Data successfully processed
✓ Rows processed: 1200
✓ Output saved to output/processed.csv
Commit this output to the repository as output/sample_run.txt:
python scripts/data_workflow.py > output/sample_run.txt
git add output/sample_run.txt
git commit -m "feat: add sample output from workflow execution"
Task 5 - Commit and Document the Workflow
Commit your script with clear messages:
git add scripts/data_workflow.py
git commit -m "feat: create modular data workflow script

Implements ingestion, processing, and output functions.
Script is executable from command line and documents each operation.
Processes sample data and generates analysis-ready output."

git push origin feature/python-workflow-script
Create a WORKFLOW.md section documenting:
* How to execute the script
* What each function does
* How to modify it for new datasets
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* Your scripts/data_workflow.py with separated functions (ingest, process, output)
* Clear docstrings and inline comments
* Sample output file in output/ confirming execution
* Clean commit messages
2. Video Explanation
Record a 3–5 minute screen-share covering all five points:
1. Explain the difference between a notebook-based workflow and a script-based workflow - when each is appropriate
2. Explain why separating ingestion, processing, and output into functions matters for maintainability and team collaboration
3. Walk through your script line-by-line and explain what each function does and what it returns
4. Show your script running from the command line and explain what happens at each step
5. Answer this follow-up: How would you convert a Jupyter notebook into a production-ready Python script that a non-technical stakeholder could run?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public
2.14
Dataset Intake & Source Validation

Hey Folks!
Welcome. Your scripts are modular and maintainable. Now comes the quality gate that protects your entire pipeline: data validation. Before a single transformation happens, you must verify that incoming data is what you expected. A file arrives malformed, with missing columns, or in wrong encoding - your pipeline crashes. Solution: build a validation firewall that checks everything before analysis begins.
Every data project that failed unexpectedly, wasted hours debugging corrupted data, or produced wrong conclusions had one thing in common: data validation happened too late or not at all. Bad data entered the pipeline, broke assumptions downstream, and nobody knew until analysis was half complete. This lesson fixes that. You will build a validation script that catches problems before they become disasters.
The Real Scenario
THE PROBLEM
A file arrives from the upstream data team. Your analysis script tries to load it and crashes with an encoding error. You check: file exists, but was saved in latin-1, not utf-8. You expected columns customer_id, amount, date. The file has customer_code, transaction_amount, transaction_ts. Different naming convention from last week. A different team sent a JSON file instead of CSV. Your pipeline fails. Your analysis stalls. Nobody knows what went wrong or how to fix it. Hours are wasted troubleshooting when the problem was obvious if checked upfront.
THE SOLUTION
A validation script runs before any analysis. It checks: file exists and has content, format is supported, columns match schema, encoding is readable, dimensions are captured. If any check fails, script stops and produces a report. Only when validation passes does data enter the pipeline. This quality firewall prevents broken data from breaking downstream code.
Why Validation Matters
Catching Problems Before They Propagate
WITHOUT VALIDATION
Bad data enters pipeline. Transformation code crashes with cryptic error. You debug for hours. Eventually realize problem is in the data itself, not your code. Analysis never completes. Trust is broken.
WITH VALIDATION
Validation runs first. Problem caught immediately with clear message: "Missing column: revenue". You contact upstream team. They fix the file. Pipeline runs successfully. Time to resolution: minutes not hours.
What validation actually does
Validation answers five questions about incoming data before any transformation: (1) Does the file exist? (2) Is it in an expected format? (3) Does it have required columns? (4) Can we read it (encoding)? (5) What are dimensions? Each question is independent. Each has a yes/no answer. If any fails, stop and report the problem clearly.
You just learned why validation catches problems early and what five questions validation must answer. Now you are going to learn how to implement each validation check and combine them into a report.
The Five Validation Checks
Each Check is Independent and Returns Clear Status
Check 1: File Existence
Does the file actually exist on disk and does it have content? A missing file means no data to process. An empty file indicates incomplete upload or data source failure. Both should stop the pipeline immediately with a clear error.
def validate_file_exists(filepath):
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    if os.path.getsize(filepath) == 0:
        return False, f"File is empty"
    return True, "File exists and has content"
Check 2: Format Validation
Is the file in an expected format? Check file extension matches what your pipeline expects (CSV, JSON, Excel, Parquet). Format mismatch stops processing - you cannot parse a JSON file as CSV without special handling.
def validate_file_format(filepath, allowed=['csv', 'json', 'xlsx']):
    ext = filepath.split('.')[-1].lower()
    if ext not in allowed:
        return False, f"Unsupported: {ext}"
    return True, f"Format valid: {ext}"
Check 3: Schema Validation
Does it have all required columns? Load file and check column names against your expected schema. Missing required columns = incomplete data. Extra columns might indicate accidental file mix-up or upstream schema change. Document exactly what was expected and what was found.
def validate_schema(df, expected_cols):
    missing = set(expected_cols) - set(df.columns)
    extra = set(df.columns) - set(expected_cols)
    if missing or extra:
        msg = []
        if missing: msg.append(f"Missing: {missing}")
        if extra: msg.append(f"Extra: {extra}")
        return False, " | ".join(msg)
    return True, "Schema valid"
Check 4: Encoding Detection
Can you actually read this file with expected encoding? Many files arrive in latin-1 or cp1252 when your pipeline expects utf-8. Encoding errors are silent and dangerous - data loads but characters are corrupted. Detect encoding explicitly and report confidence level.
import chardet

def detect_encoding(filepath):
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read(10000))
    enc = result.get('encoding', 'unknown')
    conf = result.get('confidence', 0)
    return enc, f"Detected: {enc} ({conf:.0%})"
Check 5: Dimensions
What are actual row and file sizes? Log row count, column count, file size in MB. These become baseline metrics. "This dataset has 1.2M rows instead of 500K" tells you something changed upstream. Helps catch errors and anomalies early.
def capture_stats(filepath, df):
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'file_size_mb': os.path.getsize(filepath) / (1024*1024)
    }
You just learned the five validation checks and how to implement each one independently. Now you will learn how to combine them into a single report that stops the pipeline if anything fails.
Building a Validation Report
Documenting What Was Checked and What Passed
A validation report combines all checks
The report answers: "Is this data safe to process?" It documents every check result and explains what to do next. Save it as JSON so downstream systems can parse it if needed. Make it human-readable so analysts can understand what failed.
import json

def generate_report(filepath, expected_cols):
    report = {
        'timestamp': datetime.now().isoformat(),
        'filepath': filepath,
        'checks': {}
    }
    
    # Run each check
    file_ok, msg = validate_file_exists(filepath)
    report['checks']['file_exists'] = msg
    if not file_ok: return report  # Stop if file missing
    
    format_ok, msg = validate_file_format(filepath)
    report['checks']['format'] = msg
    if not format_ok: return report
    
    df = pd.read_csv(filepath)
    
    schema_ok, msg = validate_schema(df, expected_cols)
    report['checks']['schema'] = msg
    
    enc, msg = detect_encoding(filepath)
    report['checks']['encoding'] = msg
    
    report['statistics'] = capture_stats(filepath, df)
    
    # Save report
    with open('output/intake_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    return report
Fail Fast
Stop on first failure
Do not run schema check on missing file. Do not run encoding check on unsupported format. Each check is a gate. If it fails, report immediately and stop the pipeline.
Be Specific
Error messages must be actionable

"Missing column: revenue" not "Schema invalid". "Detected latin-1 but expected utf-8" not "Encoding error". Specific messages let people fix problems immediately.

You just learned how to build a validation report that documents what was checked and what passed. You now have the quality firewall that protects your entire data pipeline from bad data entering downstream.
Dataset Intake & Source Validation


00h 59m 53s

Before transforming any dataset, your team must evaluate incoming data for quality and readiness. Datasets arrive in inconsistent formats, with encoding errors, missing columns, or unexpected structures. If you begin analysis on unvalidated data, your entire pipeline fails downstream. You cannot fix corrupted assumptions - they compound through every step.
Your task is to build a validation script that checks for format consistency, schema completeness, file encoding, and ingestion readiness - producing a structured validation report that gatekeeps all further analysis. This script becomes the quality firewall between raw data and your pipeline.
Getting Started
Create your working branch:
git checkout -b feature/dataset-intake-validation
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Check File Existence, Non-Emptiness, and Format
Create scripts/validate_intake.py that checks the foundational file properties:
import os

def validate_file_exists(filepath):
    """Check if file exists and is non-empty."""
    if not os.path.exists(filepath):
        return False, f"File does not exist: {filepath}"
    
    if os.path.getsize(filepath) == 0:
        return False, f"File is empty: {filepath}"
    
    return True, "File exists and has content"

def validate_file_format(filepath, allowed_formats=['csv', 'json', 'xlsx']):
    """Check if file extension is supported."""
    extension = filepath.split('.')[-1].lower()
    
    if extension not in allowed_formats:
        return False, f"Unsupported format: {extension}. Allowed: {allowed_formats}"
    
    return True, f"Format valid: {extension}"
Test with a sample CSV file that exists and has content.
Task 2 - Validate Column Schema
Create a function that compares incoming columns against an expected schema:
def validate_schema(df, expected_columns):
    """Validate that DataFrame has all expected columns."""
    missing = set(expected_columns) - set(df.columns)
    extra = set(df.columns) - set(expected_columns)
    
    issues = []
    if missing:
        issues.append(f"Missing columns: {missing}")
    if extra:
        issues.append(f"Unexpected columns: {extra}")
    
    if not issues:
        return True, f"Schema valid: {len(df.columns)} columns present"
    return False, " | ".join(issues)
Define expected columns for your sample data. Flag both missing and extra columns.
Task 3 - Detect and Report File Encoding
Create a function that detects encoding and handles non-standard cases:
import chardet

def detect_encoding(filepath):
    """Detect file encoding with confidence."""
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read(10000))
    
    encoding = result.get('encoding', 'utf-8')
    confidence = result.get('confidence', 0)
    
    return encoding, f"Detected: {encoding} (confidence: {confidence:.1%})"
Test with UTF-8 encoded file. Document the detected encoding in your report.
Task 4 - Capture Row Count and File Size
Create a function that logs dataset dimensions:
def capture_dataset_stats(filepath, df):
    """Log row count and file size."""
    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
    row_count = len(df)
    col_count = len(df.columns)
    
    return {
        'rows': row_count,
        'columns': col_count,
        'file_size_mb': round(file_size_mb, 2),
        'bytes': os.path.getsize(filepath)
    }
Include these in your validation report so you have baseline metrics.
Task 5 - Generate and Save Intake Validation Report
Create a function that combines all validations into a structured JSON report:
import json
from datetime import datetime

def generate_intake_report(filepath, expected_columns):
    """Generate complete intake validation report."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'filepath': filepath,
        'validations': {}
    }
    
    # Check existence
    file_exists, msg = validate_file_exists(filepath)
    report['validations']['file_exists'] = msg
    if not file_exists:
        return report
    
    # Check format
    format_valid, msg = validate_file_format(filepath)
    report['validations']['format'] = msg
    
    # Load data for remaining checks
    df = pd.read_csv(filepath)
    
    # Check schema
    schema_valid, msg = validate_schema(df, expected_columns)
    report['validations']['schema'] = msg
    
    # Check encoding
    encoding, msg = detect_encoding(filepath)
    report['validations']['encoding'] = msg
    
    # Capture statistics
    stats = capture_dataset_stats(filepath, df)
    report['statistics'] = stats
    
    # Save report to file
    with open('output/intake_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    return report
The report should document every validation result with clear pass/fail status.
Task 6 - Execute and Commit Report
Run the validation on a sample dataset. Create a sample CSV in data/raw/sample.csv with known structure:
customer_id,customer_name,transaction_amount,transaction_date
1,Alice Smith,150.50,2025-01-15
2,Bob Johnson,200.00,2025-01-20
3,Carol White,75.25,2025-02-01
Execute your validation script:
python scripts/validate_intake.py
Verify that output/intake_report.json is created with all validation results. It should look like:
{
  "timestamp": "2025-05-21T10:30:00",
  "filepath": "data/raw/sample.csv",
  "validations": {
    "file_exists": "File exists and has content",
    "format": "Format valid: csv",
    "schema": "Schema valid: 4 columns present",
    "encoding": "Detected: utf-8 (confidence: 99.9%)"
  },
  "statistics": {
    "rows": 3,
    "columns": 4,
    "file_size_mb": 0.00234,
    "bytes": 2456
  }
}
Commit all files:
git add scripts/validate_intake.py data/raw/sample.csv output/intake_report.json
git commit -m "feat: implement dataset intake validation

Checks file existence, format, schema, encoding, and dimensions.
Generates structured intake report gating downstream analysis.
Prevents broken data from entering processing pipeline."

git push origin feature/dataset-intake-validation
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* scripts/validate_intake.py with all validation functions
* Sample CSV data in data/raw/
* output/intake_report.json demonstrating successful validation
* Clear, descriptive commit messages
* Documentation of validation approach
2. Video Explanation
Record a 3–5 minute screen-share covering all five of the following points. These map directly to the video rubric, so cover each one clearly:
1. Explain what dataset intake validation is and why it must happen before any transformation begins. Why is validation a gatekeeper rather than optional?
2. Explain how column schema validation works and what happens when unexpected columns are found. How would you handle a file that arrives with columns in different order?
3. Explain what file encoding is, what encoding errors look like when data is loaded, and how you detect the correct encoding. Why is this a silent problem?
4. Walk through your intake report generated and explain what each field in the report means and why it matters. Show how the report documents validation results.
5. Answer this follow-up: How would you handle a file that arrives with a different column order each time, or with column name variations? What changes to your validation would you make?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.15
CSV & JSON Data Ingestion

Hey Data Engineer!
Welcome. Your data is validated. Now comes ingestion: loading business data from multiple formats into analysis-ready Pandas DataFrames. Datasets arrive as CSVs with varying delimiters, JSON with nested structures, Excel sheets with multiple tabs. Each format requires different handling. The key principle: be explicit with parameters, never rely on defaults. Defaults hide problems until data format changes unexpectedly.
Every data project that broke unexpectedly on new data, that loaded silently wrong data, or that crashed with cryptic errors had one thing in common: ingestion made assumptions about format and trusted defaults. This lesson fixes that. You will learn to ingest data precisely from multiple formats with explicit parameters and clear documentation of what was loaded.
The Real Scenario
THE PROBLEM
A CSV from European partner has semicolon delimiters. Script uses default comma. You get one giant column instead of separated fields. A JSON file has nested customer objects. You try to access a column that does not exist because it is buried in a nested structure. An Excel file has data on sheet "Sales", script reads default "Sheet1" and finds empty cells. Hours wasted debugging when all these problems were obvious if formats were specified explicitly.
THE SOLUTION
Write ingestion functions that accept parameters for delimiter, encoding, sheet name. Specify explicitly even when using defaults. Load, validate shape and columns, print sample output. Document everything so people know what was loaded. Turn ingestion from magic into predictable operations.
Be Explicit With Every Parameter
Why Defaults Are Dangerous
USING DEFAULTS
Assume file is comma-delimited → semicolon-delimited file loads wrong. Assume utf-8 → latin-1 file loads corrupted. Assume file exists → moved file crashes cryptically. Silent failures worst of all.
BEING EXPLICIT
Specify every parameter. Data format changes → immediate error with clear message. Encoding wrong → caught at load time. Explicit = safer because failures are loud and clear.
CSV Ingestion Pattern
def ingest_csv(filepath, delimiter=',', encoding='utf-8'):
    """Load CSV with explicit parameters."""
    try:
        df = pd.read_csv(filepath, delimiter=delimiter, encoding=encoding)
        return df
    except UnicodeDecodeError:
        print(f"Cannot decode with {encoding}. Try: latin-1, iso-8859-1, cp1252")
        raise
Specify delimiter (even if comma). Specify encoding (even if utf-8). Comment why you chose those values.
You just learned why explicit parameters prevent silent failures. Now you will learn how to handle JSON with nested structures and implement encoding fallback.
Multi-Format Ingestion
Handling CSV, JSON, and Encoding Variants
JSON Ingestion & Nested Flattening
JSON is hierarchical. Pandas is tabular. Nested structures cannot be columns directly. Solution: flatten with pd.json_normalize() to expand nested objects into separate columns.
def ingest_json(filepath, is_nested=False):
    df = pd.read_json(filepath)
    if is_nested:
        df = pd.json_normalize(df)
        print("✓ Flattened nested JSON")
    return df

# Nested: {'customer': {'name': 'Alice'}} → customer.name
# Becomes column 'customer.name' accessible as df['customer.name']
Encoding Fallback Strategy
Try multiple encodings if primary fails. Prevents pipeline from crashing on encoding mismatch.
def ingest_csv_with_fallback(filepath):
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    for enc in encodings:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not load file with any encoding")
You just learned how to ingest CSV, JSON, and handle encoding variants. Now you will learn how to document what was loaded so future analysts understand the data.
Documenting Ingestion Output
Creating Audit Trail of What Was Loaded
Always document ingestion
def document_ingestion(df, source):
    print(f"\nINGESTION REPORT: {source}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"\nColumn Types:")
    print(df.dtypes)
    print(f"\nFirst 3 rows:")
    print(df.head(3))
This creates permanent record of what was loaded. Future analysis can reference it.
SHAPE
Rows and columns tell you if data is expected size. 1M rows instead of 1K = something changed upstream.
DTYPES
Data types show if columns loaded as expected. String when should be numeric = encoding issue.
You just learned to ingest multiple formats precisely and document what was loaded. Your ingestion is now robust and auditable.
CSV & JSON Data Ingestion


00h 59m 54s

Your team must ingest business data from multiple sources in different formats. Datasets arrive as CSVs with varying delimiters, JSON files with nested structures, and Excel spreadsheets with multiple sheets. Each format requires different handling - encoding parameters, delimiter specifications, type conversions. Your task is to write a comprehensive ingestion script that loads diverse data formats into analysis-ready Pandas DataFrames, handles encoding variations, flattens nested JSON, and documents what was loaded for the entire team.
Getting Started
Create your working branch:
git checkout -b feature/multi-format-data-ingestion
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Load CSV Files With Explicit Parameters
Create scripts/ingest_data.py with a CSV ingestion function that specifies all parameters explicitly:
import pandas as pd

def ingest_csv(filepath, delimiter=',', encoding='utf-8', dtype_dict=None):
    """
    Load CSV file with explicit parameters documented.
    
    Args:
        filepath: Path to CSV file
        delimiter: Field delimiter (comma by default, but could be semicolon or tab)
        encoding: File encoding (UTF-8 standard, but may be latin-1 or cp1252)
        dtype_dict: Dictionary mapping column names to data types
    
    Returns:
        Pandas DataFrame with shape and column names confirmed
    """
    try:
        df = pd.read_csv(
            filepath,
            delimiter=delimiter,
            encoding=encoding,
            dtype=dtype_dict
        )
        print(f"✓ CSV loaded: {filepath}")
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"  Columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        raise
    except UnicodeDecodeError as e:
        print(f"Encoding error: Could not decode with {encoding}")
        print("Try: latin-1, iso-8859-1, or cp1252")
        raise
Test with a comma-delimited CSV. Note why you chose each parameter.
Task 2 - Load JSON Files Including Nested Structures
Create a JSON ingestion function that handles nested data:
def ingest_json(filepath, is_nested=False):
    """
    Load JSON file, handling nested structures by flattening them.
    
    Args:
        filepath: Path to JSON file
        is_nested: If True, flatten nested JSON structures into columns
    
    Returns:
        Pandas DataFrame with nested structures expanded
    """
    try:
        df = pd.read_json(filepath)
        
        if is_nested:
            # Flatten nested JSON: {'customer': {'name': 'Alice'}} → 'customer.name': 'Alice'
            df = pd.json_normalize(df)
            print("✓ Nested JSON flattened to tabular format")
        
        print(f"✓ JSON loaded: {filepath}")
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        raise
Test with a JSON file. Show both flat and nested examples.
Task 3 - Implement Encoding Fallback Strategy
Create function that tries multiple encodings when default fails:
def ingest_csv_with_fallback(filepath, delimiters=[','], fallback_encodings=None):
    """
    Load CSV with fallback encodings if initial attempt fails.
    
    Tries multiple encodings and delimiters in sequence.
    """
    if fallback_encodings is None:
        fallback_encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for delimiter in delimiters:
        for encoding in fallback_encodings:
            try:
                df = pd.read_csv(filepath, delimiter=delimiter, encoding=encoding)
                print(f"✓ Successfully loaded with delimiter='{delimiter}', encoding='{encoding}'")
                return df
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
    
    raise ValueError(f"Could not load {filepath} with any encoding/delimiter combination")
Task 4 - Document Ingestion Output With Shape and Types
Create function that prints comprehensive ingestion summary:
def document_ingestion(df, source_file):
    """
    Print detailed ingestion report for audit trail.
    """
    print(f"\n{'='*60}")
    print(f"INGESTION REPORT: {source_file}")
    print(f"{'='*60}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"\nColumn Names & Data Types:")
    print(df.dtypes)
    print(f"\nNull Values Per Column:")
    print(df.isnull().sum())
    print(f"\nFirst 3 Rows:")
    print(df.head(3).to_string())
    print(f"{'='*60}\n")
    return df
This creates a clear record of what was loaded.
Task 5 - Main Ingestion Script Combining Multiple Formats
Create main execution that ingests various formats:
if __name__ == "__main__":
    print("Starting multi-format ingestion...\n")
    
    # Load CSV with explicit parameters
    csv_df = ingest_csv(
        "data/raw/customers.csv",
        delimiter=',',
        encoding='utf-8'
    )
    document_ingestion(csv_df, "customers.csv")
    
    # Load JSON with flattening
    json_df = ingest_json(
        "data/raw/transactions.json",
        is_nested=True
    )
    document_ingestion(json_df, "transactions.json")
    
    # Save ingested data
    csv_df.to_csv("data/processed/customers_ingested.csv", index=False)
    json_df.to_csv("data/processed/transactions_ingested.csv", index=False)
    
    print("\n✓ All data ingested and saved to processed/")
Task 6 - Test With Sample Data and Commit
Create sample CSV in data/raw/customers.csv:
customer_id,name,email,signup_date
1,Alice,alice@example.com,2025-01-15
2,Bob,bob@example.com,2025-02-20
3,Carol,carol@example.com,2025-03-10
Create sample JSON in data/raw/transactions.json:
[
  {"id": 1, "customer_id": 1, "amount": 100, "status": "completed"},
  {"id": 2, "customer_id": 2, "amount": 250, "status": "pending"},
  {"id": 3, "customer_id": 1, "amount": 150, "status": "completed"}
]
Run ingestion:
python scripts/ingest_data.py
Commit:
git add scripts/ingest_data.py data/raw/ data/processed/
git commit -m "feat: implement multi-format data ingestion

Loads CSV with explicit delimiter/encoding parameters.
Loads JSON with nested structure flattening.
Documents all ingestion with shape, dtypes, and sample rows.
Handles encoding fallback for non-standard files."

git push origin feature/multi-format-data-ingestion
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* scripts/ingest_data.py with CSV and JSON loading functions
* Sample CSV and JSON files in data/raw/
* Processed data files in data/processed/
* Clear documentation of all parameters
* Ingestion output documentation
2. Video Explanation
Record a 3–5 minute screen-share covering all five points:
1. Explain the difference between pd.read_csv() and pd.read_json() and the key parameters each accepts. Why must you be explicit?
2. Explain what happens when encoding is not specified and how encoding errors manifest when data is loaded. Show an example of encoding corruption.
3. Explain what nested JSON looks like and how it is flattened into columns using pd.json_normalize(). Why can't you work with nested structures directly?
4. Walk through your ingestion output and explain what .shape, .dtypes, and .head() reveal about the data. Why document this?
5. Answer this follow-up: How would you handle a CSV file that is too large to load into memory all at once? What approaches exist?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.16
Dataset Profiling & Quality Assessment

Hey Analyst!
Welcome. Your data is validated and ingested. Now comes profiling: understanding actual data quality before analysis begins. What percent null? Unexpected duplicates? Reasonable values? Before you can decide how to fix problems, you must see them. Profiling reveals every quality issue - it does not fix them, but you make conscious cleaning decisions once problems are visible.
Every analyst who wasted hours on analysis later discovering data problems, who found wrong conclusions because they did not understand the data, or who had analysis break on data anomalies had one thing in common: they did not profile before analyzing. This lesson fixes that. You will build profiling scripts that compute null percentages, duplicate counts, value distributions, and statistical summaries - producing reports that guide all downstream decisions.
The Real Scenario
THE PROBLEM
Analyst loads dataset and immediately begins analysis. Three hours in, they notice metrics do not match business expectations. Investigation: 40% of email column is null. Revenue has negative values. Customer names entered in a dozen different ways. The dataset is full of problems, but nobody knew until analysis was half complete. Wasted effort. Wrong conclusions.
THE SOLUTION
Run profiling before analysis. Takes minutes. Null percentages show unusable columns. Duplicate counts reveal import errors. Value distributions show spelling inconsistencies and outliers. You see problems upfront and make conscious decisions.
What Profiling Reveals
Five Dimensions of Quality
COMPLETENESS
Null % per column. High nulls = unusable columns.
UNIQUENESS
Duplicate rows. High duplicates = import errors.
DISTRIBUTION
What values appear? Reasonable or corrupted?
VALIDITY
Do values make business sense? (negative revenue = error)
Consistency
Names spelled different ways, dates different formats = data entry variation needing standardization.
You just learned five dimensions of quality revealed by profiling. Now you will implement profiling functions that compute these metrics.
Building a Profiling Script
Computing and Documenting Quality Metrics
Null and Duplicate Metrics
def profile_nulls_and_duplicates(df):
    profile = {}
    for col in df.columns:
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        profile[col] = {'nulls': df[col].isnull().sum(), 'null_%': round(null_pct, 2)}
    profile['exact_duplicates'] = df.duplicated().sum()
    return profile
Numerical Profiles
def profile_numerical(df):
    stats = {}
    for col in df.select_dtypes(include=['number']).columns:
        stats[col] = {
            'min': df[col].min(),
            'max': df[col].max(),
            'mean': round(df[col].mean(), 2),
            'median': df[col].median()
        }
    return stats
Identify Quality Issues
def identify_issues(df, null_threshold=30, dup_threshold=5):
    issues = []
    for col in df.columns:
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        if null_pct > null_threshold:
            issues.append({
                'column': col,
                'type': 'High nulls',
                'value': f"{null_pct:.1f}%"
            })
    dup_pct = (df.duplicated().sum() / len(df)) * 100
    if dup_pct > dup_threshold:
        issues.append({'type': 'High duplicates', 'value': f"{dup_pct:.1f}%"})
    return issues
You just learned how to compute nulls, duplicates, distributions and identify issues. Now you will save these as a structured report
Dataset Profiling & Quality Assessment


00h 59m 55s

Ingested data is raw and unvetted. Before cleaning, you must understand its actual quality. What percentage of values are missing? Are there suspicious duplicates hiding in the data? What do numerical distributions look like? Are categorical values reasonable or corrupted? Your task is to write a profiling script that computes null percentages, duplicate counts, value distributions, and statistical summaries - producing a data quality report that guides all downstream cleaning decisions.
Getting Started
Create your working branch:
git checkout -b feature/data-profiling-quality
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Compute Null and Duplicate Metrics
Create scripts/profile_data.py with profiling functions:
import pandas as pd
import numpy as np

def profile_nulls_and_duplicates(df):
    """
    Compute null percentage and duplicate counts per column.
    
    Returns: Dictionary with null analysis by column
    """
    profile = {
        'null_counts': {},
        'null_percentages': {},
        'exact_duplicate_count': 0
    }
    
    for col in df.columns:
        null_count = df[col].isna().sum()
        null_pct = (null_count / len(df)) * 100
        profile['null_counts'][col] = null_count
        profile['null_percentages'][col] = round(null_pct, 2)
    
    profile['exact_duplicate_count'] = df.duplicated().sum()
    profile['duplicate_percentage'] = round((df.duplicated().sum() / len(df)) * 100, 2)
    
    return profile
Task 2 - Profile Numerical Columns
Create numerical column profiling:
def profile_numerical_columns(df):
    """
    Summarise numerical columns with statistical measures.
    
    Returns: DataFrame with min, max, mean, median, std
    """
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    stats = {}
    for col in numerical_cols:
        stats[col] = {
            'min': round(df[col].min(), 2),
            'max': round(df[col].max(), 2),
            'mean': round(df[col].mean(), 2),
            'median': round(df[col].median(), 2),
            'std': round(df[col].std(), 2),
            'null_count': df[col].isnull().sum()
        }
    
    return pd.DataFrame(stats).T
Task 3 - Profile Categorical Columns
Create categorical column profiling:
def profile_categorical_columns(df, top_n=5):
    """
    Summarise categorical columns with value distributions.
    
    Returns: Dictionary with unique counts and top values
    """
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    profile = {}
    for col in categorical_cols:
        profile[col] = {
            'unique_count': df[col].nunique(),
            'top_values': df[col].value_counts().head(top_n).to_dict(),
            'null_count': df[col].isnull().sum()
        }
    
    return profile
Task 4 - Identify Data Quality Issues
Create function that flags common quality problems:
def identify_quality_issues(df, null_threshold=30, duplicate_threshold=5):
    """
    Identify data quality problems based on thresholds.
    
    Returns: List of issues found with severity and recommendations
    """
    issues = []
    
    # Check nulls
    null_pcts = (df.isnull().sum() / len(df)) * 100
    for col, pct in null_pcts.items():
        if pct > null_threshold:
            issues.append({
                'type': 'High nulls',
                'column': col,
                'severity': 'HIGH',
                'value': f"{pct:.1f}% missing",
                'recommendation': 'Consider imputation or column exclusion'
            })
    
    # Check duplicates
    dup_count = df.duplicated().sum()
    dup_pct = (dup_count / len(df)) * 100
    if dup_pct > duplicate_threshold:
        issues.append({
            'type': 'High duplicates',
            'column': 'Full row',
            'severity': 'HIGH',
            'value': f"{dup_pct:.1f}% duplicated",
            'recommendation': 'Deduplication required before analysis'
        })
    
    # Check for invalid ranges
    for col in df.select_dtypes(include=[np.number]).columns:
        if (df[col] < 0).any() and 'amount' in col.lower():
            issues.append({
                'type': 'Invalid range',
                'column': col,
                'severity': 'MEDIUM',
                'value': f"Contains negative values",
                'recommendation': 'Investigate negative entries'
            })
    
    return issues
Task 5 - Generate Structured Quality Report
Create comprehensive profiling report:
import json

def generate_profile_report(df, filepath):
    """
    Generate complete data quality report and save to JSON.
    
    Returns: Complete profile report dictionary
    """
    report = {
        'dataset': filepath,
        'record_count': len(df),
        'column_count': len(df.columns),
        'nulls_and_duplicates': profile_nulls_and_duplicates(df),
        'numerical_stats': profile_numerical_columns(df).to_dict(),
        'categorical_stats': profile_categorical_columns(df),
        'quality_issues': identify_quality_issues(df)
    }
    
    # Save report
    with open('output/profile_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"DATA QUALITY PROFILE: {filepath}")
    print(f"{'='*60}")
    print(f"Records: {report['record_count']}")
    print(f"Columns: {report['column_count']}")
    print(f"\nQuality Issues Found: {len(report['quality_issues'])}")
    for issue in report['quality_issues']:
        print(f"  [{issue['severity']}] {issue['type']} in {issue['column']}")
        print(f"    Value: {issue['value']} → {issue['recommendation']}")
    print(f"{'='*60}\n")
    
    return report
Task 6 - Test and Commit
Create sample data with quality issues in data/raw/quality_test.csv:
customer_id,name,email,amount,status
1,Alice,alice@example.com,100,active
2,Bob,,250,active
3,Alice,alice@example.com,100,active
4,,charlie@example.com,500,inactive
5,Diana,,,-50
Run profiling:
python scripts/profile_data.py
Verify output/profile_report.json contains all metrics. Commit:
git add scripts/profile_data.py output/profile_report.json data/raw/quality_test.csv
git commit -m "feat: add data profiling and quality assessment

Computes null%, duplicates, distribution stats for numerical/categorical columns.
Identifies quality issues (high nulls, duplicates, invalid ranges).
Generates structured quality report guiding cleaning decisions."

git push origin feature/data-profiling-quality
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* scripts/profile_data.py with profiling functions
* output/profile_report.json with structured profiling results
* Sample data with intentional quality issues
* All quality issues properly identified
2. Video Explanation
Record a 3–5 minute screen-share covering all five points:
1. Explain what data profiling is and why it must happen before any cleaning begins. What would happen if you skipped it?
2. Explain what null percentage and duplicate rate reveal about a dataset's reliability. When are they warning signs?
3. Walk through your profiling output and identify the most critical quality issue found. What would you do about it?
4. Explain what a value frequency distribution shows and how it helps detect data errors like spelling variations or invalid values.
5. Answer this follow-up: How would you automate profiling for a new dataset that arrives every week? What would you automate and what would still require manual review?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.17
Data Dictionary & Business Context Mapping

Hey Data Engineer!
Welcome. Your data is validated, ingested, profiled, documented, and nulls are handled. Now comes type enforcement: ensuring every column carries the correct data type. A date stored as string "2025-01-15" cannot be sorted chronologically. Currency as text "$150.50" cannot be summed for revenue calculations. Boolean as integer 0/1 confuses models expecting actual boolean type. Type mismatches break analysis silently. You must enforce correct types proactively before analysis begins.
Every analysis that crashed on type errors, that produced wrong results from silent type coercion, or that failed on calculations had one thing in common: types were not enforced explicitly at the beginning. This lesson teaches you to enforce types deliberately and validate the conversions. You will convert string dates to datetime with explicit format, strip currency symbols and convert to float, convert 0/1 to boolean, and log all conversions so the impact is visible.
The Real Scenario
THE PROBLEM
A date column is stored as string "2025-01-15". Analyst tries to group transactions by month using df['date'].dt.to_period('M') and crashes - strings have no dt accessor. A payment column contains values like "$150.50" and analyst tries to sum revenue and gets a type error. Boolean columns arrive as 0 and 1 (integers) but the logistic regression model expects actual boolean type and rejects them. Each of these is a type mismatch that could have been caught upfront with explicit type enforcement. Instead, analysts spend hours debugging what should have been a validation step.
THE SOLUTION
A type enforcement function that converts every column to its correct type. String dates are converted to datetime with explicit format - never relying on pandas to infer. Currency is cleaned by stripping symbols then converting to float. 0/1 is converted to proper boolean. If a conversion fails, you get a clear error message telling exactly which value could not be converted. Type enforcement catches errors immediately instead of later when analysis breaks.
Why Type Enforcement Matters
Catching Type Mismatches Upfront
SILENT FAILURES
Dates stay strings. Calculations fail cryptically. Currency text cannot be summed. Models reject integer booleans. Hours spent debugging what should have been a validation step.
CAUGHT UPFRONT
Type enforcement converts immediately. Invalid value caught with clear message. Pipeline fails fast before analysis breaks. Problem solved in minutes, not hours.
Format Strings Are Critical for Dates
The string "01-02-2025" is ambiguous: January 2nd (MM-DD-YYYY US format) or February 1st (DD-MM-YYYY European format)? If you call pd.to_datetime() without specifying format, pandas guesses. On some machines it guesses right. On others it silently converts wrong, producing corrupted date data. Always specify format explicitly: pd.to_datetime(df['date'], format='%m-%d-%Y'). Explicit format prevents silent data corruption.
You just learned why type enforcement catches errors early and why format strings are critical. Now you will implement type conversion functions for the three most common cases.
Implementing Type Enforcement
Converting Common Type Mismatches
String → Datetime (Always Specify Format)
# CORRECT: Explicit format prevents silent corruption
df['transaction_date'] = pd.to_datetime(
    df['transaction_date'], 
    format='%Y-%m-%d'  # YYYY-MM-DD format
)

# WRONG: Never do this - pandas guesses and corrupts silently
# df['transaction_date'] = pd.to_datetime(df['transaction_date'])
Explicit format = no guessing = no corruption.
Currency → Float (Strip Then Convert)
# Strip symbols first
df['amount'] = df['amount'].str.replace('[$,]', '', regex=True)

# Then convert to numeric
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
# errors='coerce' turns invalid values to NaN (visible for debugging)
Cannot sum currency text. Must be numeric for all calculations.
Integer → Boolean (Map or Cast)
# Option 1: Direct cast (0→False, 1→True)
df['is_active'] = df['is_active'].astype(bool)

# Option 2: Map for clarity
mapping = {0: False, 1: True, 'yes': True, 'no': False}
df['is_premium'] = df['is_premium'].map(mapping)
Models need actual boolean, not integer 0/1.
You just learned how to enforce types correctly for dates, currency, and booleans. Now you will compare before/after dtypes to validate all conversions succeeded.
Data Dictionary & Business Context Mapping


00h 59m 54s

A dataset arrives with column names like trnx_amt, cust_segment, flag_churn. These are technical labels, not business meanings. A new analyst sees cust_segment and has no idea what it represents. Does it matter? Yes - misinterpreting a column leads to incorrect conclusions and wasted analysis. Your task is to create a data dictionary that maps every column to its business meaning, identifies the KPIs each column represents, resolves ambiguous names, and documents relationships between columns. This becomes the single source of truth for your team.
Getting Started
Create your working branch:
git checkout -b feature/data-dictionary-mapping
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Map Every Column to Business Context
Create a data dictionary CSV at docs/data_dictionary.csv:
column_name,data_type,description,business_meaning,example_value,related_kpi,notes
customer_id,integer,Unique identifier for customer,Customer ID in CRM system,12456,Customer tracking,Primary key - never null
trnx_amt,float,Transaction amount in USD,Revenue per transaction,150.99,Monthly revenue,Amount paid by customer in dollars
purchase_date,datetime,Date transaction occurred,When sale was completed,2025-01-15,Sales velocity,UTC timezone - never null
cust_segment,string,Customer classification,Business segment (B2B/B2C/SMB),B2B,Segment profitability,Updated monthly from CRM
flag_churn,integer,Churn indicator (0/1),Whether customer left within 90 days,0,Churn rate prediction,Target variable for retention models
For each column document:
* Column name (as it appears in data)
* Data type (int, float, string, datetime, etc.)
* Technical description
* Business meaning (what stakeholders care about)
* Example value (real sample)
* Related KPI (what metric this feeds)
* Notes (frequency of updates, special meanings, constraints)
Task 2 - Map Columns to Business KPIs
Create a mapping document showing which columns relate to which KPIs:
## Column to KPI Mapping

### Monthly Revenue
- **Formula**: SUM(trnx_amt)
- **Related Columns**: trnx_amt, purchase_date
- **Why It Matters**: Tracks total company revenue
- **Update Frequency**: Daily

### Sales Velocity  
- **Formula**: COUNT(transactions) / days
- **Related Columns**: purchase_date
- **Why It Matters**: Measures sales activity rate and momentum
- **Update Frequency**: Weekly

### Segment Revenue
- **Formula**: SUM(trnx_amt) grouped by cust_segment
- **Related Columns**: trnx_amt, cust_segment
- **Why It Matters**: Identifies most profitable market segments
- **Update Frequency**: Monthly

### Churn Rate
- **Formula**: SUM(flag_churn) / total_customers
- **Related Columns**: flag_churn, customer_id
- **Why It Matters**: Critical retention metric
- **Update Frequency**: Quarterly
Document at least 5 columns and their KPI relationships.
Task 3 - Flag Ambiguous Columns
Identify poorly named or unclear columns and propose business interpretations:
## Ambiguous Columns & Resolutions

### Column: flag_churn
- **Original Ambiguity**: Does it mean "currently churned" or "will churn in future"?
- **Resolved Meaning**: Binary indicator of whether customer churned in 90 days following this transaction
- **Business Interpretation**: Historical churn flag used for training predictive retention models
- **Proposed Rename**: has_churned_90d
- **Risk If Misunderstood**: Models trained on wrong definition produce unreliable predictions

### Column: segment
- **Original Ambiguity**: Is this market segment, customer segment, product segment, or geographic region?
- **Resolved Meaning**: Customer market segment (B2B, B2C, SMB) - determines go-to-market strategy
- **Business Interpretation**: Informs pricing strategy and sales approach
- **Proposed Rename**: market_segment
- **Risk If Misunderstood**: Revenue analysis by wrong dimension produces misleading segment performance
Flag at least 2 ambiguous columns with resolutions.
Task 4 - Document Column Relationships
Explain how columns interact:
## Column Relationships

### Revenue per Customer
- **Definition**: SUM(trnx_amt) grouped by customer_id
- **How It Matters**: Identifies high-value customers for retention focus and upsell opportunities
- **Example**: "Top 10% of customers generate 50% of revenue"
- **Related Columns**: customer_id, trnx_amt, customer_segment

### Churn by Segment  
- **Definition**: SUM(flag_churn) / SUM(all customers) grouped by cust_segment
- **How It Matters**: Identifies which segments have highest churn risk requiring intervention
- **Example**: "SMB segment has 25% churn vs 10% for B2B"
- **Related Columns**: flag_churn, cust_segment, customer_id

### Revenue Velocity
- **Definition**: Rolling sum of trnx_amt over 30-day windows
- **How It Matters**: Tracks sales momentum and growth rate trends
- **Example**: "Monthly revenue velocity trending up 15% quarter-over-quarter"
- **Related Columns**: trnx_amt, purchase_date
Document at least 2 column relationships with business impact.
Task 5 - Create Structured Dictionary File
Create comprehensive Markdown data dictionary at docs/DATA_DICTIONARY.md:
# Data Dictionary

## Dataset Overview
This dataset contains customer transaction records updated daily from the CRM system.
Last Updated: 2025-05-21
Maintained By: Data Engineering Team

## Columns

### customer_id
- **Type**: Integer
- **Business Meaning**: Unique customer identifier from CRM system
- **Example**: 12456
- **Null Handling**: Never null (primary key)
- **Related KPI**: Customer tracking, lifetime value calculation
- **Updates**: Assigned when customer created in CRM

### trnx_amt  
- **Type**: Float
- **Business Meaning**: Revenue from single transaction
- **Example**: 150.99
- **Unit**: USD
- **Null Handling**: Very rare - investigate if found
- **Related KPI**: Monthly revenue, average transaction value, customer lifetime value
- **Updates**: Set when transaction completes

### cust_segment
- **Type**: String
- **Business Meaning**: Customer market segment (B2B/B2C/SMB)
- **Valid Values**: B2B, B2C, SMB
- **Example**: B2B
- **Null Handling**: If null, classify as UNKNOWN
- **Related KPI**: Segment revenue, segment churn rate
- **Updates**: Monthly from CRM classification
Task 6 - Commit and Document
Create both CSV and Markdown versions:
git add docs/data_dictionary.csv docs/DATA_DICTIONARY.md
git commit -m "feat: create comprehensive data dictionary

Maps every column to business meaning and KPIs.
Resolves ambiguous column names with proposed renames.
Documents relationships between columns for team understanding.
Enables consistent interpretation across analytics team."

git push origin feature/data-dictionary-mapping
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* docs/data_dictionary.csv covering all columns
* docs/DATA_DICTIONARY.md with comprehensive documentation
* At least 5 columns explicitly mapped to business KPIs
* At least 2 ambiguous columns flagged with resolutions
* At least 2 documented column relationships
2. Video Explanation
Record a 3–5 minute screen-share covering all five points:
1. Explain what a data dictionary is and why it is essential for team-based analytical work. What problems does it prevent?
2. Explain how a raw column name is translated into business meaning - give a specific example from your dictionary.
3. Walk through five columns from your data dictionary and explain the business context of each. Why does each matter to the business?
4. Explain what an ambiguous column is and how you resolved its meaning through data exploration and team conversation.
5. Answer this follow-up: How would you maintain your data dictionary when new columns are added in future dataset updates? What processes would you put in place?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.18
Missing Value Detection & Imputation

Hey Data Engineer!
Welcome. Your data is validated, ingested, profiled, and documented. Now comes the delicate work of handling incomplete records. Real datasets have missing values - a customer email is empty, a transaction amount is null, an update timestamp is blank. These gaps break aggregations and distort analysis. You cannot analyze what is not there. You must decide what to do with nulls intentionally: fill, drop, or leave documented. Every decision must be recorded and justified.
Every analyst who made bad decisions about nulls - filling too much and inventing false data, imputing blindly without understanding context, or dropping rows without tracking - created corrupted analysis that downstream teams depended on. This lesson teaches you to handle nulls defensibly. You will implement multiple imputation strategies based on column type and business context, document every decision with reasoning, and log before/after metrics so the impact is visible and auditable.
The Real Scenario
THE PROBLEM
A dataset has 45 missing values in the revenue column out of 5000 rows. An analyst, impatient to begin analysis, simply deletes those 45 rows without documenting why. Months later, a stakeholder asks: "Why is your customer count 45 lower than what we have in the database?" The analyst has no answer. No documentation exists. Trust erodes. Another analyst sees null email addresses and fills them with the string "UNKNOWN". Later the marketing team accidentally sends campaign emails to UNKNOWN@company.com and the email bounces 45 times. Bad null handling creates cascading problems throughout the organization.
THE SOLUTION
For each column with missing values, you define a strategy: median for numerical columns, mode for categorical, forward fill for time-series, or row dropping only for critical identifiers. You document the business reasoning for every choice - why median makes sense for revenue, why mode preserves categorical meaning, why deleting customer records is justified only when the identifier itself is missing. You log before-and-after null counts and document the impact. Nulls become intentional, never hidden.
Why Null Handling Matters
Choosing Strategy Based on Type and Context
NUMERICAL - MEDIAN
50th percentile, resistant to outliers. Use for revenue, quantities, ages. Preserves distribution shape better than mean. Typical transaction was $250, use that as fill value for the 0.5% missing entries.
CATEGORICAL - MODE
Most common value. Use for category, region, segment. Does not distort categorical distribution. 85% of customers in B2B, so missing segment likely B2B. Fill with mode preserves percentage.
TIME-SERIES - FORWARD FILL
Fill with previous value. For time-ordered data only. Assumes status did not change between observations. Valid for prices, inventory levels. Risky for volatile metrics.
CRITICAL IDS - DROP ROWS
No customer_id = incomplete record that cannot be traced. Cannot impute identifiers. Only strategy for critical columns. Dropping 45 records from 5000 (0.9%) is reasonable. Losing identifier column is not.
The Over-Imputation Risk
Filling nulls artificially inflates confidence in your data. If 20% of a column is missing and you fill it with median, you have invented data for one-fifth of your dataset. Your statistics become unreliable. Your correlations become artificial. The risk: downstream users believe the imputed data is real. Always document imputation rates so analysts know what is original and what is synthetic.
You just learned why null handling matters and what strategies work for different column types. Now you will implement multiple strategies and document every decision with business reasoning.
Implementing Imputation Strategies
Functions for Each Strategy
Analyzing Nulls Before Treatment
Always examine missing values before doing anything. Understand patterns and context. Some nulls are random. Some indicate systematic issues - all values missing on certain dates means data collection failed that day.
def analyze_missing_before(df):
    """Show what we have before treatment."""
    print("BEFORE IMPUTATION:")
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        if null_count > 0:
            print(f"  {col}: {null_count} nulls ({null_pct:.1f}%)")
Applying Multiple Strategies
# Drop rows with nulls in critical columns
df = df.dropna(subset=['customer_id'])

# Fill numerical with median
df['amount'].fillna(df['amount'].median(), inplace=True)

# Fill categorical with mode
df['segment'].fillna(df['segment'].mode()[0], inplace=True)

# Forward fill for time series
df['price'].fillna(method='ffill', inplace=True)
Documenting Decisions
Create a log documenting every imputation choice and business reasoning. This becomes your team's audit trail for null handling decisions.
You just learned how to implement multiple imputation strategies and document your decisions. Your null handling is now intentional and auditable instead of hidden.
Missing Value Detection & Imputation


00h 59m 55s

Real datasets have missing values. A customer's email is empty. A transaction amount is null. An update timestamp is blank. These gaps break analysis - you cannot aggregate nulls, you cannot train models on incomplete records, you cannot trust conclusions based on partial data. Your task is to identify incomplete records across all columns, choose imputation strategies based on column type and business context (mean/median fill, forward fill, mode fill, or row dropping), document every decision, and log before/after metrics. This ensures your cleaned dataset is complete and defensible.
Getting Started
Create your working branch:
git checkout -b feature/missing-value-handling
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Analyze Missing Values Before Any Treatment
Create scripts/handle_missing.py:
import pandas as pd
import numpy as np

def analyze_missing_values(df):
    """
    Compute null counts and percentages before treatment.
    
    Returns: DataFrame with analysis of missing data by column
    """
    missing_analysis = pd.DataFrame({
        'column': df.columns,
        'null_count': df.isnull().sum().values,
        'null_percentage': (df.isnull().sum() / len(df) * 100).round(2).values,
        'data_type': df.dtypes.values,
        'null_meaning': ''  # To be filled based on column context
    })
    
    print("="*70)
    print("BEFORE IMPUTATION - Missing Value Analysis")
    print("="*70)
    print(missing_analysis.to_string(index=False))
    print(f"\nTotal rows: {len(df)}")
    print(f"Total cells: {len(df) * len(df.columns)}")
    print(f"Missing cells: {df.isnull().sum().sum()}")
    print("="*70)
    
    return missing_analysis
Task 2 - Implement Multiple Imputation Strategies
Create separate imputation functions for each strategy:
def impute_mean_median(df, numerical_cols, strategy='median'):
    """Fill numerical nulls with mean or median."""
    df_imputed = df.copy()
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            fill_value = df[col].median() if strategy == 'median' else df[col].mean()
            df_imputed[col].fillna(fill_value, inplace=True)
            null_count = df[col].isnull().sum()
            print(f"  ✓ {col}: filled {null_count} nulls with {strategy} ({fill_value:.2f})")
    return df_imputed

def impute_mode(df, categorical_cols):
    """Fill categorical nulls with mode (most common value)."""
    df_imputed = df.copy()
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            null_count = df[col].isnull().sum()
            df_imputed[col].fillna(mode_val, inplace=True)
            print(f"  ✓ {col}: filled {null_count} nulls with mode '{mode_val}'")
    return df_imputed

def impute_forward_fill(df, time_series_cols):
    """Fill with previous value (for time-series data)."""
    df_imputed = df.copy()
    for col in time_series_cols:
        if df[col].isnull().sum() > 0:
            null_count = df[col].isnull().sum()
            df_imputed[col].fillna(method='ffill', inplace=True)
            print(f"  ✓ {col}: forward-filled {null_count} nulls")
    return df_imputed

def drop_rows_with_nulls(df, critical_cols):
    """Drop rows where critical columns are null."""
    rows_before = len(df)
    df_imputed = df.dropna(subset=critical_cols)
    rows_dropped = rows_before - len(df_imputed)
    print(f"  ✓ Dropped {rows_dropped} rows with null in: {critical_cols}")
    return df_imputed
Task 3 - Document Imputation Decisions With Business Reasoning
Create decision log:
def document_imputation_decisions(df_original, df_imputed):
    """Document all imputation decisions with business justification."""
    
    decisions = {
        'amount': {
            'column_type': 'numerical',
            'null_count_before': (df_original['amount'].isnull().sum() if 'amount' in df_original else 0),
            'strategy': 'median_imputation',
            'value_used': df_original['amount'].median() if 'amount' in df_original else None,
            'business_reasoning': 'Median purchase amount is representative of typical transaction. Mean would be skewed by high-value outliers. Maintains distribution integrity.',
            'risk_assessment': 'Low - median is stable metric resistant to outliers'
        },
        'email': {
            'column_type': 'categorical_identifier',
            'null_count_before': (df_original['email'].isnull().sum() if 'email' in df_original else 0),
            'strategy': 'drop_rows',
            'rows_affected': (df_original['email'].isnull().sum() if 'email' in df_original else 0),
            'business_reasoning': 'Email is critical for customer contact and marketing campaigns. Rows without email cannot be used for outreach. Data is incomplete.',
            'risk_assessment': 'Low - only affects small percentage of data'
        },
        'status_date': {
            'column_type': 'datetime_series',
            'null_count_before': (df_original['status_date'].isnull().sum() if 'status_date' in df_original else 0),
            'strategy': 'forward_fill',
            'interpretation': 'Assumes last known status date is still valid until changed',
            'business_reasoning': 'For time-series analysis, forward fill preserves temporal continuity. Status typically does not change frequently.',
            'risk_assessment': 'Medium - assumes no change between observations'
        }
    }
    
    import json
    with open('output/imputation_decisions.json', 'w') as f:
        json.dump(decisions, f, indent=2, default=str)
    
    return decisions
Task 4 - Compare Before and After Metrics
Create validation function:
def validate_imputation(df_original, df_imputed):
    """Compare metrics before and after imputation."""
    
    print("\n" + "="*70)
    print("AFTER IMPUTATION - Validation Report")
    print("="*70)
    print(f"Total rows before: {len(df_original)}")
    print(f"Total rows after:  {len(df_imputed)}")
    print(f"Rows removed: {len(df_original) - len(df_imputed)}")
    print(f"\nTotal nulls before: {df_original.isnull().sum().sum()}")
    print(f"Total nulls after:  {df_imputed.isnull().sum().sum()}")
    
    missing_after = pd.DataFrame({
        'column': df_imputed.columns,
        'null_count_after': df_imputed.isnull().sum().values,
        'null_percentage_after': (df_imputed.isnull().sum() / len(df_imputed) * 100).round(2).values
    })
    
    print("\nNull values by column after imputation:")
    print(missing_after.to_string(index=False))
    print("="*70)
    
    return missing_after
Task 5 - Main Imputation Workflow
Create end-to-end imputation:
if __name__ == "__main__":
    # Load data
    df = pd.read_csv('data/raw/raw_data.csv')
    
    # Analyze missing before treatment
    print("Step 1: Analyzing missing values...")
    analyze_missing_values(df)
    
    # Apply strategy-specific imputation
    print("\nStep 2: Applying imputation strategies...")
    
    # Drop rows with nulls in critical columns
    df = drop_rows_with_nulls(df, ['customer_id', 'email'])
    
    # Impute numerical columns
    df = impute_mean_median(df, ['amount', 'quantity'], strategy='median')
    
    # Impute categorical columns
    df = impute_mode(df, ['category', 'region'])
    
    # Impute time-series columns
    df = impute_forward_fill(df, ['last_updated'])
    
    # Document decisions
    print("\nStep 3: Documenting imputation decisions...")
    document_imputation_decisions(df, df)
    
    # Validate results
    print("\nStep 4: Validating imputation...")
    validate_imputation(df, df)
    
    # Save cleaned data
    df.to_csv('data/processed/cleaned_data.csv', index=False)
    print("\n✓ Cleaned data saved to data/processed/cleaned_data.csv")
Task 6 - Test and Commit
Create sample data with missing values in data/raw/missing_data.csv:
customer_id,name,email,amount,category
1,Alice,alice@example.com,100,A
2,Bob,,250,B
3,Alice,alice@example.com,100,A
4,,charlie@example.com,500,C
5,Diana,,200,B
Run imputation:
python scripts/handle_missing.py
Verify output/imputation_decisions.json documents all choices. Commit:
git add scripts/handle_missing.py output/imputation_decisions.json data/processed/cleaned_data.csv
git commit -m "feat: implement missing value detection and imputation

Analyzes null counts before treatment.
Applies multiple strategies: median/mode fill, forward fill, row dropping.
Documents business reasoning for each imputation decision.
Compares before/after metrics to validate treatment."

git push origin feature/missing-value-handling
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* scripts/handle_missing.py with multiple imputation strategies
* output/imputation_decisions.json documenting business reasoning
* Before/after null counts demonstrating effectiveness
* Cleaned data file in data/processed/
2. Video Explanation
Record a 3–5 minute screen-share covering all five points:
1. Explain the difference between mean, median, and mode imputation and when each is appropriate. What are the risks of each?
2. Explain what forward fill is and in what type of column (time-series) it makes business sense to apply. What assumption does it make?
3. Explain the risk of over-imputing and how it can distort downstream analysis. When should you drop rows instead?
4. Walk through one imputation decision from your code and explain your business reasoning behind the choice.
5. Answer this follow-up: How would you handle missing values in a key identifier column like customer_id? What would you never do?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public
2.19
Data Type Enforcement & Standardisation

Hey Analyst!
Welcome. Nulls are handled. Now enforce correct types across columns. Type mismatches break analysis: dates as strings cannot be sorted chronologically, currency as text cannot be summed, 0/1 as integers confuse models expecting boolean. You must enforce correct types proactively before analysis begins.
Every analysis that failed on type errors, that produced wrong results from silent type coercion, or that crashed on calculations had one thing in common: types were not enforced explicitly. This lesson teaches you to enforce types deliberately. You will convert string dates to datetime with explicit format, strip currency symbols, convert 0/1 to boolean, and log all conversions.
The Real Scenario
THE PROBLEM
Date column is string "2025-01-15". Call dt.to_period() for grouping - crashes, strings lack dt accessor. Payment is "$150.50". Sum for revenue - type error. Boolean is 0/1, model rejects integers. Hours debugging when all were type mismatches.
THE SOLUTION
Type enforcement function converts every column: string dates to datetime with explicit format, currency to float after stripping symbols, 0/1 to boolean. Conversion failures produce clear error messages immediately.
Type Enforcement Patterns
Converting Common Type Mismatches
String → Datetime
# ALWAYS specify format - never rely on inference
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# NOT: pd.to_datetime(df['date'])  ← dangerous, guesses wrong
"01-02-2025" is ambiguous (MM-DD or DD-MM) without format. Explicit format prevents silent corruption.
Currency → Float
# Strip symbols first, then convert
df['amount'] = df['amount'].str.replace('[$,]', '', regex=True)
df['amount'] = pd.to_numeric(df['amount'])
Cannot sum currency text. Must be numeric for calculations.
Integer → Boolean
df['is_active'] = df['is_active'].astype(bool)  # 0→False, 1→True
You just learned type enforcement patterns for common mismatches. Now you will compare before/after dtypes to validate success
Data Type Enforcement & Standardisation


00h 59m 45s

A dataset arrives with dates stored as strings ("2025-01-15"). Boolean flags stored as integers (0 and 1). Currency amounts with symbols ("" symbols. Your task is to enforce correct data types across every column - converting string dates to datetime, boolean integers to proper boolean types, currency symbols to floats - and log all conversions so future analysts understand what was standardized.
Getting Started
Create your working branch:
git checkout -b feature/data-type-enforcement
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Create Explicit Type Casting Function
Create scripts/enforce_types.py:
import pandas as pd
import numpy as np

def cast_columns_to_types(df, type_mapping):
    """
    Explicitly cast columns to correct dtypes.
    
    Args:
        df: Input DataFrame
        type_mapping: Dict of {column: target_dtype}
    
    Returns:
        DataFrame with corrected types and conversion log
    """
    df_typed = df.copy()
    conversion_log = {}
    
    for col, target_dtype in type_mapping.items():
        if col not in df.columns:
            print(f"Warning: Column {col} not found in DataFrame")
            continue
        
        original_dtype = df[col].dtype
        
        try:
            df_typed[col] = df_typed[col].astype(target_dtype)
            conversion_log[col] = {
                'from': str(original_dtype),
                'to': str(target_dtype),
                'status': 'success'
            }
            print(f"✓ {col}: {original_dtype} → {target_dtype}")
        except Exception as e:
            conversion_log[col] = {
                'from': str(original_dtype),
                'to': str(target_dtype),
                'status': 'failed',
                'error': str(e)
            }
            print(f"✗ {col}: Conversion failed - {e}")
            raise
    
    return df_typed, conversion_log
Task 2 - Convert String Dates to Datetime
Create date conversion function with explicit format:
def convert_string_dates_to_datetime(df, date_columns, date_format=None):
    """
    Convert string columns to datetime with explicit format.
    
    Args:
        df: Input DataFrame
        date_columns: List of column names containing dates
        date_format: Datetime format string (e.g., '%Y-%m-%d')
    
    Returns:
        DataFrame with datetime columns converted
    
    Note: ALWAYS specify format. "01-02-2025" is ambiguous without it.
    """
    df_typed = df.copy()
    
    for col in date_columns:
        if col not in df.columns:
            print(f"Warning: Column {col} not found")
            continue
        
        try:
            # Pandas infers format if not specified - risky!
            if date_format:
                df_typed[col] = pd.to_datetime(df_typed[col], format=date_format)
            else:
                # Only use inference if absolutely necessary
                df_typed[col] = pd.to_datetime(df_typed[col])
            
            print(f"✓ {col}: Converted to datetime")
            
        except Exception as e:
            print(f"✗ {col}: Conversion failed - {e}")
            print(f"  Sample values: {df[col].head(3).tolist()}")
            print(f"  Expected format: {date_format}")
            raise
    
    return df_typed
Task 3 - Convert Currency to Float
Create currency conversion function:
def convert_currency_to_float(df, currency_columns):
    """
    Strip currency symbols and convert to float.
    
    Example: '$150.50' → 150.50
    
    Args:
        df: Input DataFrame
        currency_columns: List of column names with currency
    
    Returns:
        DataFrame with clean numeric columns
    """
    df_typed = df.copy()
    
    for col in currency_columns:
        if col not in df.columns:
            print(f"Warning: Column {col} not found")
            continue
        
        try:
            # Remove common currency symbols and whitespace
            df_typed[col] = (df_typed[col]
                            .astype(str)
                            .str.replace('[$,]', '', regex=True)
                            .str.strip())
            
            # Convert to float - coerce errors to NaN
            df_typed[col] = pd.to_numeric(df_typed[col], errors='coerce')
            
            # Check for failed conversions
            failed_conversions = df_typed[col].isnull().sum() - df[col].isnull().sum()
            if failed_conversions > 0:
                print(f"⚠ {col}: {failed_conversions} values could not be converted to numeric")
            
            print(f"✓ {col}: Stripped symbols, converted to float")
            
        except Exception as e:
            print(f"✗ {col}: Conversion failed - {e}")
            raise
    
    return df_typed
Task 4 - Convert Boolean-like Integers
Create boolean conversion function:
def convert_integers_to_boolean(df, boolean_columns):
    """
    Convert 0/1 or yes/no columns to proper boolean type.
    
    Args:
        df: Input DataFrame
        boolean_columns: List of column names with binary values
    
    Returns:
        DataFrame with bool columns
    """
    df_typed = df.copy()
    
    for col in boolean_columns:
        if col not in df.columns:
            print(f"Warning: Column {col} not found")
            continue
        
        try:
            # First check what values exist
            unique_vals = df[col].unique()
            print(f"  {col} unique values: {unique_vals}")
            
            # Map different boolean representations
            if df[col].dtype == 'object':
                mapping = {
                    'yes': True, 'no': False,
                    'y': True, 'n': False,
                    'true': True, 'false': False,
                    '1': True, '0': False,
                    1: True, 0: False,
                    True: True, False: False
                }
                df_typed[col] = df_typed[col].map(mapping)
            else:
                df_typed[col] = df_typed[col].astype(bool)
            
            print(f"✓ {col}: Converted to boolean")
            
        except Exception as e:
            print(f"✗ {col}: Conversion failed - {e}")
            raise
    
    return df_typed
Task 5 - Compare Before and After Types
Create validation function:
def compare_dtypes(df_original, df_typed):
    """
    Compare dtypes before and after conversion.
    
    Returns: Summary of all changes
    """
    comparison = pd.DataFrame({
        'column': df_original.columns,
        'dtype_before': df_original.dtypes.values,
        'dtype_after': df_typed.dtypes.values,
        'changed': (df_original.dtypes != df_typed.dtypes).values
    })
    
    print("\n" + "="*70)
    print("DTYPE CONVERSION SUMMARY")
    print("="*70)
    print(comparison.to_string(index=False))
    
    # Save report
    comparison.to_csv('output/dtype_conversion_report.csv', index=False)
    print("\nReport saved to output/dtype_conversion_report.csv")
    print("="*70)
    
    return comparison
Task 6 - Main Execution
Create end-to-end type enforcement:
if __name__ == "__main__":
    # Load data
    df = pd.read_csv('data/raw/untyped_data.csv')
    
    print("="*70)
    print("BEFORE TYPE CONVERSION")
    print("="*70)
    print(df.dtypes)
    print(f"\nSample data:")
    print(df.head(3))
    
    # Define conversions
    df_typed = df.copy()
    
    # Convert dates with explicit format
    print("\n1. Converting date columns...")
    df_typed = convert_string_dates_to_datetime(
        df_typed,
        ['transaction_date', 'signup_date'],
        date_format='%Y-%m-%d'
    )
    
    # Convert currency
    print("\n2. Converting currency columns...")
    df_typed = convert_currency_to_float(
        df_typed,
        ['amount', 'revenue']
    )
    
    # Convert booleans
    print("\n3. Converting boolean columns...")
    df_typed = convert_integers_to_boolean(
        df_typed,
        ['is_active', 'is_premium']
    )
    
    # Compare
    print("\n4. Comparing before/after types...")
    print("="*70)
    print("AFTER TYPE CONVERSION")
    print("="*70)
    print(df_typed.dtypes)
    print(f"\nSample data:")
    print(df_typed.head(3))
    
    # Validation report
    compare_dtypes(df, df_typed)
    
    # Save typed data
    df_typed.to_csv('data/processed/typed_data.csv', index=False)
    print("\n✓ Typed data saved to data/processed/typed_data.csv")
Task 7 - Test and Commit
Create sample data with mixed types in data/raw/untyped_data.csv:
transaction_date,amount,is_active,signup_date
2025-01-15,$150.50,1,2024-01-01
2025-02-20,$200.00,0,2024-02-15
2025-03-10,$75.25,1,2024-03-01
Run type enforcement:
python scripts/enforce_types.py
Commit:
git add scripts/enforce_types.py output/dtype_conversion_report.csv data/processed/typed_data.csv
git commit -m "feat: enforce data type standardization

Converts string dates to datetime with explicit format.
Strips currency symbols and converts to float.
Converts 0/1 to proper boolean type.
Compares before/after dtypes and generates conversion report."

git push origin feature/data-type-enforcement
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* scripts/enforce_types.py with conversion functions for dates, currency, booleans
* output/dtype_conversion_report.csv showing before/after dtypes
* Typed data file in data/processed/
* Clear documentation of format specifications
2. Video Explanation
Record a 3–5 minute screen-share covering all five points:
1. Explain why storing dates as strings causes problems in analysis and time-based aggregation. Give a concrete example.
2. Explain how pd.to_datetime() works and what the format parameter controls. Why is it critical to specify it?
3. Explain the risk of leaving currency columns as strings when performing calculations. What happens if you sum them?
4. Walk through at least one non-obvious type conversion and explain your approach taken. Why not just use astype()?
5. Answer this follow-up: How would you handle columns that contain mixed types in the same field (some valid dates, some invalid text)?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.20
Duplicate Detection & Record Deduplication

Hey Data Engineer!
Welcome. Your data is validated, ingested, profiled, documented, nulls handled, and types enforced. One final problem blocks analysis: duplicates. A customer appears twice in the database. A transaction is imported twice from different sources. A row is accidentally duplicated during a merge. These exact and near-duplicates distort every metric - customer count inflates, revenue doubles, analysis conclusions become unreliable. You must detect them, decide which version to keep, and log all removals for audit and compliance.
Every analysis broken by duplicate records, every count that did not match reality, every KPI that stakeholders questioned had one thing in common: duplicates entered the pipeline and were never caught before analysis began. This lesson teaches you to detect and remove duplicates defensibly. You will identify exact duplicates using .duplicated(), find near-duplicates by key columns, implement deduplication logic preserving the best record, log all removals for audit purposes, and compare before/after metrics.
The Real Scenario
THE PROBLEM
A customer database contains 10,000 records. An analyst runs analysis and gets 10,500 unique customers. Where did the 500 extra come from? Investigation reveals: 250 exact duplicates where every field matches (data imported twice by mistake). Another 250 near-duplicates where the same customer is recorded under slightly different names (JOHN vs JOHN SMITH). Nobody tracked which duplicates were removed. Analysis completed before duplicates were noticed. Now conclusions about customer count, revenue per customer, and churn rates are all wrong. Trust erodes. The fix requires redoing analysis, but nobody documented what was removed.
THE SOLUTION
A deduplication workflow that detects exact duplicates using .duplicated(), identifies near-duplicates by matching on key columns (customer_id + date), removes duplicates keeping the most complete or most recent record, logs all removals to an audit file for compliance, and documents the impact with before/after row counts. Everything is traceable. When someone asks "Where did that record go?" you can answer with certainty: "It was a duplicate of record X, removed on date Y."
Exact vs Near Duplicates
Identifying What to Remove and How
EXACT DUPLICATES
Every field identical. Same customer_id, same transaction amount, same date. Accidental import from source system that sends data twice. Remove all but first (or most recent, or most complete depending on strategy).
NEAR DUPLICATES
Same key columns (customer_id, transaction_date) but different other values. Same transaction recorded with slightly different amounts or descriptions. Merge into single record or keep most complete version. Requires business logic to decide.
Detection and Removal Pattern
# Exact duplicates
exact_dup_count = df.duplicated().sum()
df = df.drop_duplicates(keep='first')  # Keep first/last/False to remove all

# Near-duplicates on key
dup_keys = df[df.duplicated(subset=['customer_id'], keep=False)]
df = df.drop_duplicates(subset=['customer_id'], keep='first')
You just learned the difference between exact and near-duplicates and how to detect each. Now you will implement deduplication strategies and create audit trails.
Deduplication Strategy and Audit Trail
Keeping the Best Record and Documenting Removals
Deduplication Strategies
Keep First - Preserve original record. Use when first entry is most reliable.
Keep Last - Preserve most recent. Use when later updates are corrections.
Keep Most Complete - Preserve record with fewest nulls. Use for merging incomplete data from multiple sources.
Choose based on business logic. Document your choice. Later analysts need to know what you kept and why.
Audit Trail Logging
# Save every removed record
removed = df_original[~df_original.index.isin(df_dedup.index)]
removed.to_csv('output/removed_duplicates_audit.csv')

# Document impact
print(f"Before: {len(df_original):,} rows")
print(f"After:  {len(df_dedup):,} rows")
print(f"Removed: {len(removed):,} ({pct:.1f}%)")
Audit trail answers: "Where is that record?" → "Duplicate of X, removed date Y."
Before/After Comparison
Log metrics showing deduplication impact so results are traceable:
comparison = {
    'rows_before': len(df_original),
    'rows_after': len(df_dedup),
    'rows_removed': len(df_original) - len(df_dedup),
    'removal_pct': round(removed / len(df_original) * 100, 2)
}
You just learned how to deduplicate data, keep the best records, and create audit trails. Your data cleaning foundation is now complete - from validation through deduplication
Duplicate Detection & Record Deduplication


00h 59m 55s

A customer's record appears twice in your dataset. A transaction is imported twice from different sources. A row is duplicated when data was loaded into Pandas. These duplicates distort every metric - customer count inflates, revenue doubles, analysis conclusions are wrong. Your task is to identify exact and near-duplicate records using key-column matching and hash-based comparison, implement deduplication logic that chooses which record to keep (first, last, or most complete), log all removed entries for audit purposes, and document row counts before and after. This ensures your final dataset contains only unique, valid records.
Getting Started
Create your working branch:
git checkout -b feature/duplicate-detection-dedup
All work will be committed on this branch. Open a PR to main when all tasks are complete.
Tasks
Task 1 - Detect Exact Duplicates
Create scripts/deduplicate_data.py:
import pandas as pd
import numpy as np

def detect_exact_duplicates(df):
    """
    Find rows where all values are identical.
    
    Returns: Tuple of (count, duplicate_rows_dataframe)
    """
    # Count exact duplicates
    exact_dups = df.duplicated().sum()
    
    # Get actual duplicate rows including the original
    dup_rows = df[df.duplicated(keep=False)].sort_values(by=df.columns.tolist())
    
    print("\nEXACT DUPLICATE DETECTION")
    print("="*60)
    print(f"Exact duplicates found: {exact_dups}")
    print(f"Total duplicate rows (including originals): {len(dup_rows)}")
    
    if len(dup_rows) > 0:
        print(f"\nSample duplicate rows:")
        print(dup_rows.head(10).to_string())
    
    return exact_dups, dup_rows
Task 2 - Detect Near-Duplicates Using Key Columns
Create near-duplicate detection:
def detect_near_duplicates(df, key_columns):
    """
    Find rows with same key values but different other fields.
    
    Args:
        df: Input DataFrame
        key_columns: Columns defining uniqueness (e.g., ['customer_id', 'date'])
    
    Returns:
        DataFrame showing near-duplicates grouped by key
    """
    # Find records with duplicate key values
    duplicate_keys = df[df.duplicated(subset=key_columns, keep=False)]
    
    print("\nNEAR-DUPLICATE DETECTION")
    print("="*60)
    print(f"Records with duplicate keys: {len(duplicate_keys)}")
    print(f"Unique key combinations with duplicates: {len(duplicate_keys.groupby(key_columns))}")
    
    # Show sample groups
    if len(duplicate_keys) > 0:
        print(f"\nSample groups with duplicate keys:")
        for keys, group in list(duplicate_keys.groupby(key_columns))[:3]:
            print(f"\n  Key: {keys}")
            print(f"  Records in group: {len(group)}")
            print(group.to_string())
    
    return duplicate_keys
Task 3 - Remove Exact Duplicates With Keep Strategy
Create removal function:
def remove_exact_duplicates(df, keep='first'):
    """
    Remove exact duplicates, choosing which record to keep.
    
    Args:
        df: Input DataFrame
        keep: 'first' (keep oldest), 'last' (keep newest), or False (remove all)
    
    Returns:
        Deduplicated DataFrame with row counts documented
    """
    rows_before = len(df)
    
    df_dedup = df.drop_duplicates(keep=keep)
    
    rows_after = len(df_dedup)
    rows_removed = rows_before - rows_after
    removal_pct = (rows_removed / rows_before) * 100
    
    print("\nEXACT DUPLICATE REMOVAL")
    print("="*60)
    print(f"Keep strategy: {keep}")
    print(f"Rows before: {rows_before:,}")
    print(f"Rows after:  {rows_after:,}")
    print(f"Rows removed: {rows_removed:,} ({removal_pct:.2f}%)")
    
    return df_dedup
Task 4 - Remove Near-Duplicates With Custom Logic
Create near-duplicate removal:
def remove_near_duplicates(df, key_columns, keep_strategy='most_complete'):
    """
    Remove near-duplicates by choosing best record.
    
    Args:
        df: Input DataFrame
        key_columns: Columns defining uniqueness
        keep_strategy: 'most_complete' (fewest nulls), 'first', 'last'
    
    Returns:
        Deduplicated DataFrame
    """
    rows_before = len(df)
    
    if keep_strategy == 'most_complete':
        # Keep row with fewest nulls per group
        def keep_most_complete(group):
            null_counts = group.isnull().sum(axis=1)
            best_idx = null_counts.idxmin()
            return group.loc[[best_idx]]
        
        df_dedup = df.groupby(key_columns, as_index=False).apply(keep_most_complete).reset_index(drop=True)
    
    elif keep_strategy == 'last':
        # Keep most recent record (last by index)
        df_dedup = df.drop_duplicates(subset=key_columns, keep='last')
    
    else:
        # Keep first record
        df_dedup = df.drop_duplicates(subset=key_columns, keep='first')
    
    rows_after = len(df_dedup)
    rows_removed = rows_before - rows_after
    removal_pct = (rows_removed / rows_before) * 100
    
    print("\nNEAR-DUPLICATE REMOVAL")
    print("="*60)
    print(f"Keep strategy: {keep_strategy}")
    print(f"Key columns: {key_columns}")
    print(f"Rows before: {rows_before:,}")
    print(f"Rows after:  {rows_after:,}")
    print(f"Rows removed: {rows_removed:,} ({removal_pct:.2f}%)")
    
    return df_dedup
Task 5 - Log Removed Records for Audit
Create audit logging:
import json
from datetime import datetime

def log_removed_duplicates(df_original, df_dedup):
    """
    Save all removed duplicate rows to audit file for compliance.
    
    Returns: Audit summary
    """
    # Find rows in original but not in deduplicated
    removed_mask = ~df_original.index.isin(df_dedup.index)
    removed_records = df_original[removed_mask]
    
    print("\nAUDIT LOGGING")
    print("="*60)
    print(f"Total records removed: {len(removed_records)}")
    
    # Save removed records for audit trail
    removed_records.to_csv('output/removed_duplicates_audit.csv', index=False)
    print(f"✓ Removed records saved to audit file")
    
    # Create summary
    audit_summary = {
        'removal_timestamp': datetime.now().isoformat(),
        'total_removed': int(len(removed_records)),
        'reason': 'Duplicate detection and deduplication',
        'audit_file': 'output/removed_duplicates_audit.csv',
        'audit_note': 'All removed records logged for compliance and recovery if needed'
    }
    
    with open('output/dedup_audit_summary.json', 'w') as f:
        json.dump(audit_summary, f, indent=2, default=str)
    
    print(f"✓ Audit summary saved")
    print("="*60)
    
    return removed_records, audit_summary
Task 6 - Compare Before and After
Create validation function:
def compare_before_after(df_original, df_dedup):
    """
    Log before/after metrics confirming deduplication worked.
    
    Returns: Comparison dictionary
    """
    comparison = {
        'rows_before': len(df_original),
        'rows_after': len(df_dedup),
        'rows_removed': len(df_original) - len(df_dedup),
        'removal_percentage': round(((len(df_original) - len(df_dedup)) / len(df_original)) * 100, 2),
        'columns': len(df_original.columns),
        'nulls_before': int(df_original.isnull().sum().sum()),
        'nulls_after': int(df_dedup.isnull().sum().sum()),
        'timestamp': datetime.now().isoformat()
    }
    
    print("\n" + "="*70)
    print("DEDUPLICATION FINAL SUMMARY")
    print("="*70)
    print(f"Rows before: {comparison['rows_before']:,}")
    print(f"Rows after:  {comparison['rows_after']:,}")
    print(f"Removed:     {comparison['rows_removed']:,} ({comparison['removal_percentage']}%)")
    print(f"\nNulls before: {comparison['nulls_before']:,}")
    print(f"Nulls after:  {comparison['nulls_after']:,}")
    print(f"Null change:  {comparison['nulls_before'] - comparison['nulls_after']:,}")
    print("="*70)
    
    import json
    with open('output/dedup_summary.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    
    return comparison
Task 7 - Main Deduplication Workflow
Create end-to-end script:
if __name__ == "__main__":
    # Load data
    df = pd.read_csv('data/raw/data_with_dupes.csv')
    
    print("\n" + "="*70)
    print("STARTING DEDUPLICATION WORKFLOW")
    print("="*70)
    print(f"Initial record count: {len(df):,}")
    
    # Step 1: Detect exact duplicates
    print("\n[Step 1/4] Detecting exact duplicates...")
    exact_count, exact_rows = detect_exact_duplicates(df)
    
    # Step 2: Detect near-duplicates
    print("\n[Step 2/4] Detecting near-duplicates by key...")
    near_dups = detect_near_duplicates(df, key_columns=['customer_id', 'transaction_date'])
    
    # Step 3: Remove exact duplicates
    print("\n[Step 3/4] Removing exact duplicates (keeping first)...")
    df = remove_exact_duplicates(df, keep='first')
    
    # Step 4: Remove near-duplicates
    print("\n[Step 4/4] Removing near-duplicates (keeping most complete)...")
    df = remove_near_duplicates(
        df,
        key_columns=['customer_id', 'transaction_date'],
        keep_strategy='most_complete'
    )
    
    # Log removals
    print("\n[Audit] Logging removed records for compliance...")
    log_removed_duplicates(df, df)
    
    # Compare metrics
    compare_before_after(df, df)
    
    # Save deduplicated data
    df.to_csv('data/processed/deduplicated_data.csv', index=False)
    print("\n✓ Deduplicated data saved to data/processed/deduplicated_data.csv")
Task 8 - Test and Commit
Create sample data with duplicates in data/raw/data_with_dupes.csv:
customer_id,transaction_date,amount,status
1,2025-01-15,100,completed
1,2025-01-15,100,completed
2,2025-01-20,250,pending
2,2025-01-20,250,pending
3,2025-02-01,150,completed
Run deduplication:
python scripts/deduplicate_data.py
Commit:
git add scripts/deduplicate_data.py output/removed_duplicates_audit.csv output/dedup_summary.json data/processed/deduplicated_data.csv
git commit -m "feat: implement duplicate detection and deduplication

Detects exact duplicates using .duplicated() method.
Finds near-duplicates using key column combinations.
Removes duplicates with configurable keep strategy (first/last/most_complete).
Logs removed records to audit file for compliance.
Compares before/after metrics documenting all changes."

git push origin feature/duplicate-detection-dedup
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
Format: https://github.com/YOUR-USERNAME/data-product-pipeline/pull/[number]
The PR must show:
* scripts/deduplicate_data.py with exact and near-duplicate detection
* output/removed_duplicates_audit.csv logging all removed records
* output/dedup_summary.json with before/after metrics
* Deduplicated data in data/processed/
* Clear documentation of deduplication strategy
2. Video Explanation
Record a 3–5 minute screen-share covering all five points:
1. Explain the difference between exact duplicates and near-duplicates with a concrete example from your data.
2. Explain what the keep parameter in .duplicated() controls and what options are available ('first', 'last', False).
3. Explain why logging removed records matters in a professional data workflow. What questions does the audit trail answer?
4. Walk through the key columns chosen for near-duplicate detection and explain why they were selected. Why not use all columns?
5. Answer this follow-up: How would you detect duplicates when the same record has slight spelling variations (e.g., "John" vs "Jon" in the name field)? What approaches exist?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public

2.21
String Cleaning & Text Normalisation

Hey Data Cleaner!
Welcome. Your data is validated and types enforced. Now comes the meticulous work of string cleaning: the spaces before names that break groupby, the inconsistent casing ("JOHN", "john", "John") that creates three categories instead of one, the special characters hiding in text fields. Real-world text is messy. You must clean it deliberately.
Every analyst who skipped string cleaning, who thought "close enough" was good enough, who ran groupby aggregations on uncleaned text and got wrong segment counts had the same problem: text diversity masqueraded as data volume. This lesson teaches you to build transformation pipelines. You will strip whitespace, normalize casing, remove special characters with regex, standardize categorical labels using mapping dictionaries, and build reusable functions that clean any text column consistently.
The Real Scenario
THE PROBLEM
A dataset has a product_category column with values like " Electronics ", "electronics", "ELECTRONICS", "electro nics". An analyst runs .value_counts() and expects three categories. Instead they get seven. The inconsistency inflates category counts. A customer_name column has trailing spaces (" John ") that break exact matching. A city field contains special characters ("São Paulo", "Montréal") that disappear in some export formats. Marketing team uses "B2B", "b2b", "B 2 B" interchangeably. Groupby aggregations produce wrong results. Analysis falls apart.
THE SOLUTION
A string cleaning pipeline that applies transformations consistently: .str.strip() removes leading/trailing whitespace, .str.lower() normalizes casing, regex removes special characters, mapping dictionaries standardize spelling variations. All wrapped in reusable functions. Once written, the pipeline cleans not just this dataset but any future dataset with the same column names. Groupby now produces correct counts. Analysis is reliable.
Why String Cleaning Matters
Text Consistency as Data Quality Foundation
DIRTY TEXT
Whitespace variation. Mixed casing. Special characters. Spelling inconsistencies. Groupby treats each variation as unique. Segment counts inflated. Aggregations unreliable. Business metrics wrong.
CLEAN TEXT
Whitespace stripped. Casing normalized. Special characters handled. Spelling standardized. Groupby produces correct counts. Metrics reliable. Analysis trustworthy.
Four String Cleaning Fundamentals
Strip removes whitespace noise. Casing normalization makes matching possible. Special character removal prevents encoding issues. Mapping dictionaries handle spelling variants. Together they transform inconsistent raw text into analysis-ready data.
You just learned why string cleaning is critical for groupby accuracy and reliable aggregations. Now you will implement the four core transformation techniques.
Building the String Cleaning Pipeline
Transformation Step by Step
Strip Whitespace
Leading and trailing spaces are invisible but break exact matching. Remove them always.
df['category'] = df['category'].str.strip()
# " Electronics " → "Electronics"
Normalize Casing
Make case consistent. Lowercase is standard for categorical data. Models treat "John" and "JOHN" as different unless normalized.
df['name'] = df['name'].str.lower()
# "John", "JOHN", "john" → all become "john"
Remove Special Characters with Regex
Regex pattern [^a-zA-Z0-9 ] removes everything except letters, numbers, and spaces. Carrot ^ inside brackets means "NOT".
df['city'] = df['city'].str.replace('[^a-zA-Z0-9 ]', '', regex=True)
# "São Paulo" → "So Paulo"
# "Montréal" → "Montreal"
Map Spelling Variations to Canonical Form
segment_map = {
    'b2b': 'B2B',
    'b 2 b': 'B2B',
    'b2 b': 'B2B',
    'business-to-business': 'B2B'
}
df['segment'] = df['segment'].map(segment_map)
Build Reusable Functions
Wrap transformations in functions. This pipeline becomes reusable across projects. Don't hardcode transformations inline - they become unmaintainable.
You just learned all four string cleaning techniques and why reusable functions matter. Now you will apply them to a complete pipeline.
Creating a Reusable Pipeline
Function-Based String Cleaning
Template Pipeline
def clean_text_column(series, 
                     lowercase=True, 
                     strip=True, 
                     remove_special=False,
                     mapping=None):
    """Reusable text cleaning function."""
    result = series.copy()
    
    if strip:
        result = result.str.strip()
    
    if lowercase:
        result = result.str.lower()
    
    if remove_special:
        result = result.str.replace('[^a-zA-Z0-9 ]', '', regex=True)
    
    if mapping:
        result = result.map(mapping)
    
    return result
Apply to multiple columns:
df['name'] = clean_text_column(df['name'], lowercase=True, strip=True)
df['category'] = clean_text_column(df['category'], mapping=category_map)
You just learned to build reusable string cleaning functions. Your pipeline now cleans consistently, scales to new datasets, and becomes part of your permanent toolkit.
String Cleaning & Text Normalisation


00h 59m 56s

You are building a customer database integration project. Data is arriving from three different sources with inconsistent text formatting: product names have extra spaces (" Electronics ", "electronics", "ELECTRONICS"), customer segments have special characters ("B2B", "b2b", "B 2 B"), and locations contain international characters ("São Paulo", "Montréal") that cause encoding issues downstream. Your task is to build a reusable string cleaning pipeline that standardizes all text fields and makes them analysis-ready.
Getting Started
1. Create a new branch: git checkout -b assignment-11-string-cleaning
2. Create a Python script: scripts/string_cleaning_pipeline.py
3. Load a sample dataset with messy text columns (create synthetic data if needed)
4. Build the cleaning pipeline following the requirements below
Task 1: Strip Whitespace Consistently (1 mark)
Objective: Remove leading and trailing spaces from all text columns
Requirements:
* Apply .str.strip() to every string column in your dataset
* Document which columns were cleaned and how many values had whitespace
* Show before/after comparison with .value_counts() to prove duplicates were consolidated
Code Template:
def strip_all_strings(df):
    """Strip whitespace from all string columns."""
    string_cols = df.select_dtypes(include=['object']).columns
    
    for col in string_cols:
        if df[col].dtype == 'object':
            # Count before
            before = df[col].nunique()
            
            # Apply strip
            df[col] = df[col].str.strip()
            
            # Count after
            after = df[col].nunique()
            
            print(f"{col}: {before} → {after} unique values")
    
    return df
What to submit:
* Script with .str.strip() applied
* Before/after value counts for at least 2 columns showing consolidation
* Summary showing total whitespace issues fixed
Task 2: Normalize Casing to Consistent Standard (1 mark)
Objective: Convert all categorical text to single consistent case (typically lowercase)
Requirements:
* Apply .str.lower() (or .str.upper()) to categorical columns
* Document business decision about which case standard to use
* Show that "JOHN", "john", and "John" all map to "john"
Code Template:
def normalize_casing(df, columns_to_lower):
    """Normalize casing for specified columns."""
    for col in columns_to_lower:
        df[col] = df[col].str.lower()
        print(f"Normalized {col} to lowercase")
    
    return df
What to submit:
* Identify at least 3 columns where casing was inconsistent
* Apply normalization consistently
* Show sample rows before and after with .head()
Task 3: Remove Special Characters Using Regex (1 mark)
Objective: Clean international characters and special symbols that break systems
Requirements:
* Use regex pattern [^a-zA-Z0-9 ] to remove non-alphanumeric characters
* Apply .str.replace(pattern, '', regex=True) with proper escaping
* Handle at least one column with international characters ("São Paulo" → "So Paulo")
Code Template:
def remove_special_characters(df, columns):
    """Remove special characters from specified columns."""
    for col in columns:
        df[col] = df[col].str.replace('[^a-zA-Z0-9 ]', '', regex=True)
        print(f"Removed special characters from {col}")
    
    return df
What to submit:
* Regex pattern used and explanation of what it matches
* Before/after samples showing special character removal
* Verification that international characters are handled correctly
Task 4: Standardize Categorical Labels Using Mapping Dictionary (1 mark)
Objective: Consolidate spelling variations and abbreviations into canonical forms
Requirements:
* Create a mapping dictionary for at least 3 variations of the same category
* Example: {'b2b': 'B2B', 'b 2 b': 'B2B', 'business-to-business': 'B2B'}
* Apply mapping with .map() or .replace()
* Document business decision for each canonical form chosen
Code Template:
segment_map = {
    'b2b': 'B2B',
    'b 2 b': 'B2B',
    'b2 b': 'B2B',
    'sme': 'SMB',
    'small medium enterprise': 'SMB',
    'enterprise': 'Enterprise'
}

df['segment'] = df['segment'].map(segment_map)
What to submit:
* Mapping dictionary with at least 3 categories × 3 variations
* Justification for each canonical form (e.g., "Using B2B not b2b for consistency with CRM system")
* Value counts before and after mapping showing consolidation
Task 5: Build Reusable String Cleaning Function (1 mark)
Objective: Wrap all transformations in a single reusable function
Requirements:
* Function accepts column and optional parameters (lowercase, strip, remove_special, mapping)
* Can be applied to any dataset with string columns
* Includes error handling for null values
* Returns cleaned column
Code Template:
def clean_text_column(series, lowercase=True, strip=True, 
                     remove_special=False, mapping=None):
    """Reusable text cleaning function for any string column."""
    result = series.copy()
    
    if result.isna().any():
        print(f"Warning: {result.isna().sum()} null values in column")
    
    if strip:
        result = result.str.strip()
    
    if lowercase:
        result = result.str.lower()
    
    if remove_special:
        result = result.str.replace('[^a-zA-Z0-9 ]', '', regex=True)
    
    if mapping:
        result = result.map(mapping)
    
    return result

# Apply to multiple columns
df['name'] = clean_text_column(df['name'], lowercase=True, strip=True)
df['segment'] = clean_text_column(df['segment'], mapping=segment_map)
What to submit:
* Function definition with clear parameters
* Applied to at least 3 different columns with different parameter combinations
* Documentation of parameter choices for each column
Testing Instructions
Test your pipeline with edge cases:
test_cases = [
    '  Product A  ',      # Leading/trailing spaces
    'PRODUCT B',         # All caps
    'Product_C',         # Special char
    None,                # Null value
    ''                   # Empty string
]

test_series = pd.Series(test_cases)
result = clean_text_column(test_series, lowercase=True, strip=True, remove_special=True)
print(result)
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
Record a 3-5 minute video explaining your pipeline. Address these points:
1. Why inconsistent casing causes groupby to fail (1 mark) - Explain how "JOHN", "john", "John" become 3 separate groups instead of 1, breaking aggregations
2. How .str.strip() differs from .str.replace() (1 mark) - Strip removes only leading/trailing spaces; replace can remove any substring pattern
3. Regex power for bulk character removal (1 mark) - Show how [^a-zA-Z0-9 ] removes any non-alphanumeric in one operation vs looping
4. Walkthrough of one category standardization (1 mark) - Pick one mapping (e.g., B2B variants) and explain the business decision behind the canonical form
5. Handle columns with mixed languages or special sets (1 mark) - Discuss how to preserve needed characters (e.g., apostrophes in names, accented vowels) while removing noise
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.22
Date & Time Transformation Pipeline

Hey Timestamp Parser!
Welcome. Text is clean. Now comes temporal data: timestamps stored as strings that cannot be grouped by week, hours as integers that cannot measure elapsed time, dates across timezones that confuse aggregations. Parsing dates unlocks time-based analysis. You must extract features: day-of-week, hour-of-day, week number, compute elapsed time, enable time-series aggregation.
Every analyst who tried to group by week on string dates and failed, who computed hour-of-day manually in loops instead of using .dt.hour, who lost data to timezone confusion had the same problem: they did not parse timestamps immediately. This lesson teaches you to parse dates first, extract features, compute metrics. You will convert strings to datetime, extract day-of-week and hour-of-day, compute days-since-event, perform resample operations on time-indexed data, and build features that support meaningful time-series analysis.
The Real Scenario
THE PROBLEM
A transaction dataset has a transaction_date column stored as strings "2025-01-15 14:30:45". Analyst tries to group by week using .resample('W') and gets an error - resample requires datetime index. Another analyst needs to analyze peak transaction hours. Without parsed datetime, they manually split strings and extract hour numbers in a loop across 100k rows - slow and error-prone. Marketing needs to know "days since last purchase" for each customer but dates are strings. Recency calculation requires datetime arithmetic which strings cannot support. Analysis stalls.
THE SOLUTION
Parse all timestamps immediately to datetime type. Use .dt accessor to extract features instantly: .dt.day_name() for day-of-week, .dt.hour for hour-of-day, .dt.isocalendar().week for week number. Compute elapsed time using datetime arithmetic: (today - purchase_date).dt.days. Set datetime as index for .resample() to work. Now groupby hour, week, day work instantly without loops. Time-series aggregation becomes fast and natural.
Why Datetime Parsing Matters
From String to Temporal Analysis
STRING DATES
Cannot group by week. Cannot extract hour. Cannot compute elapsed time. Manual string parsing required. Slow. Error-prone. Time-series analysis impossible.
PARSED DATETIME
Resample works instantly. Extract hour with .dt.hour. Compute days with arithmetic. Groupby by time works naturally. Fast. Reliable. Time-series analysis enabled.
The .dt Accessor
Once you have datetime type, the .dt accessor unlocks dozens of attributes. Day name, month, year, week, day of year, hour, minute, second. All available instantly. This is why parsing first is critical - without it, these attributes don't exist.
You just learned why datetime parsing unlocks time-series capabilities. Now you will implement feature extraction and time-based aggregations.
Extracting Time-Based Features
Features from Parsed Datetime
Parse First - Always
df['transaction_date'] = pd.to_datetime(
    df['transaction_date'], 
    format='%Y-%m-%d %H:%M:%S'
)
# Now .dt accessor is available
Extract Day of Week
df['day_of_week'] = df['transaction_date'].dt.day_name()
# Monday, Tuesday, Wednesday, etc.

# Or numeric version (0=Monday, 6=Sunday)
df['dow_numeric'] = df['transaction_date'].dt.dayofweek
Extract Hour of Day
df['hour'] = df['transaction_date'].dt.hour
# 0-23 representing midnight to 11pm
Compute Time Since Event
today = pd.Timestamp.now()
df['days_since_purchase'] = (today - df['transaction_date']).dt.days
# Datetime arithmetic produces timedelta, .dt.days extracts days
Time-Series Aggregation with Resample
# Set datetime as index
df_ts = df.set_index('transaction_date')

# Resample to weekly and sum transaction amounts
weekly_revenue = df_ts['amount'].resample('W').sum()
# W = week, D = day, M = month, H = hour
You just learned to extract time-based features and aggregate by time periods. Time-series analysis is now accessible to your workflows.
Advanced Time Features
Week Number, Month, and Fiscal Features
Week Number and Quarter
df['week_num'] = df['transaction_date'].dt.isocalendar().week
df['month'] = df['transaction_date'].dt.month
df['quarter'] = df['transaction_date'].dt.quarter
You just learned all essential time-based features and how to enable time-series analysis. Your dataset now supports temporal grouping and trend analysis.


2.22 Date & Time Transformation Pipeline
2.22
Date & Time Transformation Pipeline

Hey Timestamp Parser!
Welcome. Text is clean. Now comes temporal data: timestamps stored as strings that cannot be grouped by week, hours as integers that cannot measure elapsed time, dates across timezones that confuse aggregations. Parsing dates unlocks time-based analysis. You must extract features: day-of-week, hour-of-day, week number, compute elapsed time, enable time-series aggregation.
Every analyst who tried to group by week on string dates and failed, who computed hour-of-day manually in loops instead of using .dt.hour, who lost data to timezone confusion had the same problem: they did not parse timestamps immediately. This lesson teaches you to parse dates first, extract features, compute metrics. You will convert strings to datetime, extract day-of-week and hour-of-day, compute days-since-event, perform resample operations on time-indexed data, and build features that support meaningful time-series analysis.
The Real Scenario
THE PROBLEM
A transaction dataset has a transaction_date column stored as strings "2025-01-15 14:30:45". Analyst tries to group by week using .resample('W') and gets an error - resample requires datetime index. Another analyst needs to analyze peak transaction hours. Without parsed datetime, they manually split strings and extract hour numbers in a loop across 100k rows - slow and error-prone. Marketing needs to know "days since last purchase" for each customer but dates are strings. Recency calculation requires datetime arithmetic which strings cannot support. Analysis stalls.
THE SOLUTION
Parse all timestamps immediately to datetime type. Use .dt accessor to extract features instantly: .dt.day_name() for day-of-week, .dt.hour for hour-of-day, .dt.isocalendar().week for week number. Compute elapsed time using datetime arithmetic: (today - purchase_date).dt.days. Set datetime as index for .resample() to work. Now groupby hour, week, day work instantly without loops. Time-series aggregation becomes fast and natural.
Why Datetime Parsing Matters
From String to Temporal Analysis
STRING DATES
Cannot group by week. Cannot extract hour. Cannot compute elapsed time. Manual string parsing required. Slow. Error-prone. Time-series analysis impossible.
PARSED DATETIME
Resample works instantly. Extract hour with .dt.hour. Compute days with arithmetic. Groupby by time works naturally. Fast. Reliable. Time-series analysis enabled.
The .dt Accessor
Once you have datetime type, the .dt accessor unlocks dozens of attributes. Day name, month, year, week, day of year, hour, minute, second. All available instantly. This is why parsing first is critical - without it, these attributes don't exist.
You just learned why datetime parsing unlocks time-series capabilities. Now you will implement feature extraction and time-based aggregations.
Extracting Time-Based Features
Features from Parsed Datetime
Parse First - Always
df['transaction_date'] = pd.to_datetime(
    df['transaction_date'], 
    format='%Y-%m-%d %H:%M:%S'
)
# Now .dt accessor is available
Extract Day of Week
df['day_of_week'] = df['transaction_date'].dt.day_name()
# Monday, Tuesday, Wednesday, etc.

# Or numeric version (0=Monday, 6=Sunday)
df['dow_numeric'] = df['transaction_date'].dt.dayofweek
Extract Hour of Day
df['hour'] = df['transaction_date'].dt.hour
# 0-23 representing midnight to 11pm
Compute Time Since Event
today = pd.Timestamp.now()
df['days_since_purchase'] = (today - df['transaction_date']).dt.days
# Datetime arithmetic produces timedelta, .dt.days extracts days
Time-Series Aggregation with Resample
# Set datetime as index
df_ts = df.set_index('transaction_date')

# Resample to weekly and sum transaction amounts
weekly_revenue = df_ts['amount'].resample('W').sum()
# W = week, D = day, M = month, H = hour
You just learned to extract time-based features and aggregate by time periods. Time-series analysis is now accessible to your workflows.
Advanced Time Features
Week Number, Month, and Fiscal Features
Week Number and Quarter
df['week_num'] = df['transaction_date'].dt.isocalendar().week
df['month'] = df['transaction_date'].dt.month
df['quarter'] = df['transaction_date'].dt.quarter
You just learned all essential time-based features and how to enable time-series analysis. Your dataset now supports temporal grouping and trend analysis.
Bonus Resources
* Pandas Datetime API Documentation - comprehensive reference for .dt accessor with all 50+ available attributes
* Time-Series Resampling Guide - detailed examples of using .resample() for different time frequencies and aggregation functions
* Timezone Handling in Pandas - best practices for working with multi-timezone timestamps and avoiding common pitfalls


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Date & Time Transformation Pipeline


00h 59m 54s

Your transaction dataset contains raw timestamp strings like "2025-01-15 14:30:45" that cannot be grouped by week, cannot extract hour-of-day, cannot compute recency. You need to parse these strings to datetime type and extract time-based features for meaningful temporal analysis. Build a pipeline that converts strings to datetime, extracts 4+ features (day-of-week, hour, week number), and computes time-since-event metrics for churn analysis.
Getting Started
1. Create branch: git checkout -b assignment-12-datetime-features
2. Create script: scripts/datetime_feature_engineering.py
3. Load sample transaction data with datetime strings
4. Build the transformation pipeline
Task 1: Parse Timestamp Strings with Explicit Format (1 mark)
Objective: Convert string dates to datetime type with explicit format
Requirements:
* Use pd.to_datetime(format='%Y-%m-%d %H:%M:%S') with format specification
* Never use pd.to_datetime() without format (causes silent corruption)
* Document the exact format string used
* Verify by checking .dtype shows 'datetime64'
Code:
df['transaction_date'] = pd.to_datetime(
    df['transaction_date'],
    format='%Y-%m-%d %H:%M:%S'
)

# Verify
print(df['transaction_date'].dtype)  # Should be datetime64[ns]
Task 2: Extract Day-of-Week and Hour-of-Day (1 mark)
Objective: Create time-of-day features for traffic/engagement analysis
Requirements:
* Extract .dt.day_name() for readable day names
* Extract .dt.hour for numeric hour (0-23)
* Create distribution showing which days/hours are busiest
* Plot histogram showing hour distribution
Code:
df['day_of_week'] = df['transaction_date'].dt.day_name()
df['hour'] = df['transaction_date'].dt.hour

# Distribution
hourly_volume = df.groupby('hour').size()
print(hourly_volume)
Task 3: Compute Week Number and Resample Data (1 mark)
Objective: Enable weekly aggregations and trend analysis
Requirements:
* Extract week number with .dt.isocalendar().week
* Set datetime as index for .resample() operations
* Resample to weekly buckets and compute sum/count/mean
* Show weekly trend (e.g., revenue per week)
Code:
df['week_num'] = df['transaction_date'].dt.isocalendar().week

# Resample for weekly metrics
df_ts = df.set_index('transaction_date')
weekly_revenue = df_ts['amount'].resample('W').sum()
print(weekly_revenue)
Task 4: Compute Days-Since-Event Metric (1 mark)
Objective: Build recency metrics for customer churn prediction
Requirements:
* Compute days since last purchase per customer
* Use datetime arithmetic: (today - purchase_date).dt.days
* Show distribution of recency (how many days since last purchase)
* Identify customers with no recent activity
Code:
today = pd.Timestamp.now()

# By customer
customer_last_purchase = df.groupby('customer_id')['transaction_date'].max()
df['days_since_last_purchase'] = (today - customer_last_purchase).dt.days

# Distribution
print(df['days_since_last_purchase'].describe())
Task 5: Build Time-Indexed Aggregation (1 mark)
Objective: Enable time-series analysis with multiple temporal dimensions
Requirements:
* Group by day AND hour to see patterns
* Compute at least 3 aggregation functions (sum, count, mean)
* Create pivot showing hour × day-of-week heatmap
* Identify peak activity windows
Code:
# Multi-level groupby
hourly_daily = df.groupby(['day_of_week', 'hour']).agg({
    'amount': ['sum', 'count', 'mean']
})

# Pivot for visualization
pivot_table = pd.pivot_table(
    df,
    values='amount',
    index='hour',
    columns='day_of_week',
    aggfunc='sum'
)

print(pivot_table)
Testing Instructions
# Test datetime parsing
print(f"Min date: {df['transaction_date'].min()}")
print(f"Max date: {df['transaction_date'].max()}")

# Test feature extraction
print(f"Days in dataset: {(df['transaction_date'].max() - df['transaction_date'].min()).days}")
print(f"Hours with data: {df['hour'].unique()}")
print(f"Weeks in dataset: {df['week_num'].nunique()}")

# Test recency
print(f"Min days since purchase: {df['days_since_last_purchase'].min()}")
print(f"Max days since purchase: {df['days_since_last_purchase'].max()}")
Submission Checklist
*  Timestamp strings parsed with explicit format specification
*  Day-of-week and hour-of-day extracted and distributed
*  Week number computed and resampling functional
*  Days-since-event metrics computed with datetime arithmetic
*  Multi-dimensional aggregations working (day × hour × metrics)
*  Peak activity windows identified and documented
*  Plots showing temporal distributions created
*  PR link submitted
*  Video (3-5 min) covers 5 required points
Video Rubric (5 marks)
1. Why parsing first is required - Explain why string dates cannot use .dt accessor or .resample()
2. What .dt accessor provides - Name 4+ attributes available (day_name, hour, week, month, etc.)
3. How time-since-event is computed - Walk through datetime arithmetic step-by-step
4. Time-based aggregation insight - Explain what pattern/insight the pivot table reveals
5. Handling multi-timezone timestamps - Discuss converting UTC to local timezone before feature extraction
Advanced Temporal Analysis
ONCE BASICS ARE COMPLETE, extend with:
# Seasonal decomposition
from statsmodels.tsa.seasonal import seasonal_decompose

ts = df.set_index('transaction_date')['amount']
decomposition = seasonal_decompose(ts, model='additive', period=52)  # 52 weeks

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
decomposition.observed.plot(ax=axes[0], title='Observed')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
decomposition.resid.plot(ax=axes[3], title='Residual')
plt.tight_layout()
Identify repeating patterns: Do Saturdays always have lower traffic? Does December spike?
Edge Cases and Timezone Handling
Test with:
# Multiple timezone formats
test_dates = [
    '2025-01-15 14:30:45',        # Standard
    '2025-1-15 14:30:45',         # Single-digit month
    '15/01/2025 14:30:45',        # European format
    '2025-01-15T14:30:45Z',       # ISO format with Z
]

for date_str in test_dates:
    try:
        parsed = pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S')
        print(f"✓ {date_str}")
    except:
        print(f"✗ {date_str} - format mismatch")
Always test your format string against real data samples.
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. explains why parsing timestamps before extracting features is a required first step
2. explains what .dt accessor methods provide and names at least four attributes available
3. explains how a time-since-event feature is computed and what business value it adds
4. walks through a time-based aggregation and explains what insight it produces
5. answers a follow-up on how to handle timestamps stored across multiple timezones in one column
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

String Cleaning & Text Normalisation
Outlier Detection with Statistical Methods



Student App | Kalvium

2.23
Outlier Detection with Statistical Methods

Hey Statistical Analyst!
Welcome. Time features are extracted. Now comes outlier detection: the50, the 99-hour work week when normal is 40, the product return rate of 95% when others are 5%. These anomalies distort averages and break assumptions. You must detect them statistically, decide whether to cap, remove, or flag, and log every decision for audit.
Every analyst who ignored outliers and got wrong statistics, who silently removed anomalies without documentation, or who capped values incorrectly had the same problem: they treated outlier detection as optional cleanup instead of intentional decision-making. This lesson teaches you statistical detection. You will implement Z-score and IQR methods, apply different handling strategies per column, flag anomalies with binary columns, document decisions, and trace all transformations.
The Real Scenario
THE PROBLEM
A salary dataset has one executive earning65k. One employee has 150 vacation days when the company max is 30. A customer spent500. An analyst computes average salary and gets skewed results. Median vacation days is misleading. Mean customer spend does not represent typical behavior. The outliers either need removal, capping at reasonable bounds, or flagging so downstream analysis can handle them separately. But the analyst made no documented decision - did they cap or drop the executive salary? Months later, another analyst cannot reproduce the analysis because the decision was invisible.
THE SOLUTION
Detect outliers using Z-score (how many standard deviations from mean) or IQR (1.5 times interquartile range). For each column, decide intentionally: cap at boundary, remove the row, or flag with a boolean column. Cap preserves row but bounds extreme values. Remove eliminates data. Flag keeps all data but marks anomalies for separate treatment. Document every decision with reasoning. Create a cleaning log showing column, method, action, count. All traceable. Auditable.
Outlier Detection Methods
Z-Score vs Interquartile Range
Z-SCORE
Count of standard deviations from mean. Z > 3 usually outlier. Assumes normal distribution. Works on scaled data. Sensitive to extreme outliers that shift the mean.
IQR
1.5 × (Q3 − Q1). Values beyond boundary are outliers. Robust to distribution shape. Resistant to extreme values. Better for skewed data.
Detection & Decision Making
# Z-score detection
from scipy import stats
z_scores = np.abs(stats.zscore(df['salary']))
df['outlier_zscore'] = z_scores > 3

# IQR detection
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df['outlier_iqr'] = (df['salary'] < lower_bound) | (df['salary'] > upper_bound)
You just learned the two most important outlier detection methods. Now you will decide what to do with detected outliers.
Handling Outliers: Three Strategies
Cap, Remove, or Flag
Strategy 1: Cap at Boundaries
Extreme value gets replaced with boundary value. Preserves all rows. Bounds the influence of outliers on statistics.
df['salary_capped'] = df['salary'].clip(lower=lower_bound, upper=upper_bound)
# Values below lower_bound become lower_bound
# Values above upper_bound become upper_bound
Strategy 2: Remove Rows
Delete entire row if outlier detected. Loses data but removes influence completely. Use only if row is invalid or represents data collection error.
df_clean = df[~df['outlier_iqr']]
# Keep only rows where outlier_iqr is False
Strategy 3: Flag with Binary Column
# Keep all data, mark anomalies separately
df['is_salary_outlier'] = df['outlier_iqr'].astype(int)
# Downstream analysis can filter or weight these separately
Document Every Decision
Create a cleaning log with column name, method used, action taken (cap/remove/flag), count of affected rows, and business reasoning. This log becomes part of your repository and explains all transformations.
You just learned three ways to handle outliers and why documenting decisions is essential. Outlier handling is now intentional, not hidden.
Bonus Resources
* Outlier Detection Methods - comprehensive overview of Z-score, IQR, isolation forests, and when each is appropriate
* SciPy Stats Library - statistical outlier detection functions with detailed examples and parameter guidance
* Robust Statistics for Skewed Data - techniques for detecting outliers in non-normal distributions where assumptions break down


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Date & Time Transformation Pipeline
Data Consistency & Validation Rules



Student App | Kalvium


2.23 Outlier Detection with Statistical Methods
2.23
Outlier Detection with Statistical Methods

Hey Statistical Analyst!
Welcome. Time features are extracted. Now comes outlier detection: the50, the 99-hour work week when normal is 40, the product return rate of 95% when others are 5%. These anomalies distort averages and break assumptions. You must detect them statistically, decide whether to cap, remove, or flag, and log every decision for audit.
Every analyst who ignored outliers and got wrong statistics, who silently removed anomalies without documentation, or who capped values incorrectly had the same problem: they treated outlier detection as optional cleanup instead of intentional decision-making. This lesson teaches you statistical detection. You will implement Z-score and IQR methods, apply different handling strategies per column, flag anomalies with binary columns, document decisions, and trace all transformations.
The Real Scenario
THE PROBLEM
A salary dataset has one executive earning65k. One employee has 150 vacation days when the company max is 30. A customer spent500. An analyst computes average salary and gets skewed results. Median vacation days is misleading. Mean customer spend does not represent typical behavior. The outliers either need removal, capping at reasonable bounds, or flagging so downstream analysis can handle them separately. But the analyst made no documented decision - did they cap or drop the executive salary? Months later, another analyst cannot reproduce the analysis because the decision was invisible.
THE SOLUTION
Detect outliers using Z-score (how many standard deviations from mean) or IQR (1.5 times interquartile range). For each column, decide intentionally: cap at boundary, remove the row, or flag with a boolean column. Cap preserves row but bounds extreme values. Remove eliminates data. Flag keeps all data but marks anomalies for separate treatment. Document every decision with reasoning. Create a cleaning log showing column, method, action, count. All traceable. Auditable.
Outlier Detection Methods
Z-Score vs Interquartile Range
Z-SCORE
Count of standard deviations from mean. Z > 3 usually outlier. Assumes normal distribution. Works on scaled data. Sensitive to extreme outliers that shift the mean.
IQR
1.5 × (Q3 − Q1). Values beyond boundary are outliers. Robust to distribution shape. Resistant to extreme values. Better for skewed data.
Detection & Decision Making
# Z-score detection
from scipy import stats
z_scores = np.abs(stats.zscore(df['salary']))
df['outlier_zscore'] = z_scores > 3

# IQR detection
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df['outlier_iqr'] = (df['salary'] < lower_bound) | (df['salary'] > upper_bound)
You just learned the two most important outlier detection methods. Now you will decide what to do with detected outliers.
Handling Outliers: Three Strategies
Cap, Remove, or Flag
Strategy 1: Cap at Boundaries
Extreme value gets replaced with boundary value. Preserves all rows. Bounds the influence of outliers on statistics.
df['salary_capped'] = df['salary'].clip(lower=lower_bound, upper=upper_bound)
# Values below lower_bound become lower_bound
# Values above upper_bound become upper_bound
Strategy 2: Remove Rows
Delete entire row if outlier detected. Loses data but removes influence completely. Use only if row is invalid or represents data collection error.
df_clean = df[~df['outlier_iqr']]
# Keep only rows where outlier_iqr is False
Strategy 3: Flag with Binary Column
# Keep all data, mark anomalies separately
df['is_salary_outlier'] = df['outlier_iqr'].astype(int)
# Downstream analysis can filter or weight these separately
Document Every Decision
Create a cleaning log with column name, method used, action taken (cap/remove/flag), count of affected rows, and business reasoning. This log becomes part of your repository and explains all transformations.
You just learned three ways to handle outliers and why documenting decisions is essential. Outlier handling is now intentional, not hidden.
Bonus Resources
* Outlier Detection Methods - comprehensive overview of Z-score, IQR, isolation forests, and when each is appropriate
* SciPy Stats Library - statistical outlier detection functions with detailed examples and parameter guidance
* Robust Statistics for Skewed Data - techniques for detecting outliers in non-normal distributions where assumptions break down


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Outlier Detection with Statistical Methods


00h 59m 58s

Your customer revenue dataset has extreme outliers: one customer spent500. Your age column has impossible values (150+ years). These outliers distort averages and break assumptions. Implement Z-score and IQR outlier detection, decide handling strategy (cap/remove/flag) per column, and document all decisions in a cleaning log.
Task 1: Z-Score Outlier Detection (1 mark)
Detect outliers as values beyond ±3 standard deviations from mean.
from scipy import stats

df['revenue_zscore'] = np.abs(stats.zscore(df['revenue']))
z_outliers = df[df['revenue_zscore'] > 3]

print(f"Z-score outliers: {len(z_outliers)}")
Task 2: IQR Outlier Detection (1 mark)
Detect outliers beyond 1.5 × IQR from quartiles.
Q1 = df['revenue'].quantile(0.25)
Q3 = df['revenue'].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df['is_outlier_iqr'] = (df['revenue'] < lower) | (df['revenue'] > upper)
Task 3: Cap Outliers at Boundaries (1 mark)
Apply capping strategy: replace extreme values with boundary values.
df['revenue_capped'] = df['revenue'].clip(lower=lower, upper=upper)

# Verify capping worked
print(f"Before: min={df['revenue'].min()}, max={df['revenue'].max()}")
print(f"After: min={df['revenue_capped'].min()}, max={df['revenue_capped'].max()}")
Task 4: Flag Outliers with Binary Column (1 mark)
Mark anomalies without removing data.
# Use both methods and combine
df['is_outlier'] = (df['is_outlier_iqr']) | (df['revenue_zscore'] > 3)

# Downstream analysis can filter or weight separately
normal = df[~df['is_outlier']]
anomalies = df[df['is_outlier']]

print(f"Normal records: {len(normal)}")
print(f"Anomalies: {len(anomalies)}")
Task 5: Create Cleaning Log (1 mark)
Document all outlier-related transformations.
cleaning_log = [{
    'column': 'revenue',
    'method': 'IQR',
    'action': 'cap',
    'threshold_lower': lower,
    'threshold_upper': upper,
    'affected_rows': df['is_outlier_iqr'].sum(),
    'date': pd.Timestamp.now()
}]

log_df = pd.DataFrame(cleaning_log)
log_df.to_csv('output/cleaning_log.csv')
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Z-score vs IQR comparison - When is each appropriate?
2. IQR formula explanation - What does 1.5× multiplier represent?
3. Why flagging beats removal - When is marking better than deleting?
4. One outlier decision walkthrough - Show business reasoning for your chosen action
5. Skewed distributions - How do Z-score assumptions break down in skewed data?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

Date & Time Transformation Pipeline
Data Consistency & Validation Rules

Student App | Kalvium

2.24
Data Consistency & Validation Rules

Hey Controller!
Welcome. Outliers are handled. Now comes systematic validation: building rules that catch broken records before they reach analysis. A customer birth date is in the future. A price is negative. An end date is before start date. A product category is empty when required. These violations distort analysis silently. You must write validation rules, check every record, isolate failures, and produce a structured report.
Every analysis corrupted by bad data that should have been caught, every business decision made on records that violated obvious rules, every trust-breaking moment when downstream users found corrupt data had the same root: validation rules were never written or never enforced. This lesson teaches you systematic validation. You will implement range checks, null constraints, format patterns, referential integrity, business rule validation, isolate failures, and produce validation reports.
The Real Scenario
THE PROBLEM
A customer dataset has birth_date values in the year 2050 - future dates that should never exist. Price column has negative values. Customer_id is sometimes missing when it should never be null. Campaign_start_date is after campaign_end_date. Email addresses are missing the @ symbol. An analyst builds a customer lifetime value model on this data without validating. Model trains on corrupted inputs. Results are meaningless. Business makes decisions on invalid analysis. Later the data issues are discovered but nobody has a record of which records were bad. No validation report exists. Audit trail is gone.
THE SOLUTION
Before any analysis, write validation rules. Range checks ensure birth_date is between 1920 and today. Null checks ensure customer_id is never missing. Format patterns check email contains @. Business rules check end_date >= start_date. Run all rules before analysis. Isolate failing records into a separate file. Produce a structured validation report with pass/fail counts per rule. Only data that passes all rules proceeds to analysis. Failed records are documented and traceable.
Building Validation Rules
Five Categories of Validation
Range Check
Ensure values fall within expected bounds
Age 0-150, price >= 0, date between reasonable range. Catches impossible values that indicate data entry errors or corruption.
Null Constraint
Ensure critical columns never have nulls
customer_id, email, primary_key should never be empty. Null in critical field means record is incomplete and unusable.
Format Pattern
Validate structure with regex patterns
Email contains @, phone is digits only, postal code matches expected pattern. Catches malformed entries that will break downstream systems.
Referential Integrity
Ensure relationships between columns
If order has customer_id, that ID must exist in customer table. Foreign key constraint prevents orphaned references.
Business Rules
Domain-specific logic checks
End date must be after start date, order total must equal sum of items, discount cannot exceed 50%. Catches logical inconsistencies.
You just learned five types of validation checks that catch real data issues. Now you will implement them and isolate failures.
Implementing Validation Rules
Checking and Reporting
Range and Null Checks
# Range check
df['valid_age'] = (df['age'] >= 0) & (df['age'] <= 120)

# Null checks on critical columns
df['valid_customer_id'] = df['customer_id'].notna()
df['valid_email'] = df['email'].notna()
Format Pattern with Regex
# Email must contain @
df['valid_email_format'] = df['email'].str.contains('@', na=False)

# Phone must be digits only
df['valid_phone'] = df['phone'].str.match(r'^\d{10}$', na=False)
Business Rule Check
# End date must be after start date
df['valid_date_order'] = df['end_date'] >= df['start_date']
Isolation and Reporting
# Combine all checks
validation_cols = ['valid_age', 'valid_customer_id', 'valid_email', 'valid_date_order']
df['passes_all_checks'] = df[validation_cols].all(axis=1)

# Isolate failures
failures = df[~df['passes_all_checks']]
failures.to_csv('output/validation_failures.csv')

# Report
print(f"Records: {len(df)}")
print(f"Passed: {df['passes_all_checks'].sum()}")
print(f"Failed: {(~df['passes_all_checks']).sum()}")

# Proceed with clean data
df_clean = df[df['passes_all_checks']]
You just learned to implement systematic validation and isolate bad records. Your data is now validated before analysis begins.
Bonus Resources
* Great Expectations Framework - open-source library for automated data validation at scale with rich reporting
* Data Quality Metrics - guidance on defining and measuring validation success rates and tracking improvements over time
* Pandas Validation Patterns - best practices for combining multiple validation checks and producing audit logs


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Outlier Detection with Statistical Methods
Multi-Source Merging & Join Validation

Student App | Kalvium


2.24 Data Consistency & Validation Rules
2.24
Data Consistency & Validation Rules

Hey Controller!
Welcome. Outliers are handled. Now comes systematic validation: building rules that catch broken records before they reach analysis. A customer birth date is in the future. A price is negative. An end date is before start date. A product category is empty when required. These violations distort analysis silently. You must write validation rules, check every record, isolate failures, and produce a structured report.
Every analysis corrupted by bad data that should have been caught, every business decision made on records that violated obvious rules, every trust-breaking moment when downstream users found corrupt data had the same root: validation rules were never written or never enforced. This lesson teaches you systematic validation. You will implement range checks, null constraints, format patterns, referential integrity, business rule validation, isolate failures, and produce validation reports.
The Real Scenario
THE PROBLEM
A customer dataset has birth_date values in the year 2050 - future dates that should never exist. Price column has negative values. Customer_id is sometimes missing when it should never be null. Campaign_start_date is after campaign_end_date. Email addresses are missing the @ symbol. An analyst builds a customer lifetime value model on this data without validating. Model trains on corrupted inputs. Results are meaningless. Business makes decisions on invalid analysis. Later the data issues are discovered but nobody has a record of which records were bad. No validation report exists. Audit trail is gone.
THE SOLUTION
Before any analysis, write validation rules. Range checks ensure birth_date is between 1920 and today. Null checks ensure customer_id is never missing. Format patterns check email contains @. Business rules check end_date >= start_date. Run all rules before analysis. Isolate failing records into a separate file. Produce a structured validation report with pass/fail counts per rule. Only data that passes all rules proceeds to analysis. Failed records are documented and traceable.
Building Validation Rules
Five Categories of Validation
Range Check
Ensure values fall within expected bounds
Age 0-150, price >= 0, date between reasonable range. Catches impossible values that indicate data entry errors or corruption.
Null Constraint
Ensure critical columns never have nulls
customer_id, email, primary_key should never be empty. Null in critical field means record is incomplete and unusable.
Format Pattern
Validate structure with regex patterns
Email contains @, phone is digits only, postal code matches expected pattern. Catches malformed entries that will break downstream systems.
Referential Integrity
Ensure relationships between columns
If order has customer_id, that ID must exist in customer table. Foreign key constraint prevents orphaned references.
Business Rules
Domain-specific logic checks
End date must be after start date, order total must equal sum of items, discount cannot exceed 50%. Catches logical inconsistencies.
You just learned five types of validation checks that catch real data issues. Now you will implement them and isolate failures.
Implementing Validation Rules
Checking and Reporting
Range and Null Checks
# Range check
df['valid_age'] = (df['age'] >= 0) & (df['age'] <= 120)

# Null checks on critical columns
df['valid_customer_id'] = df['customer_id'].notna()
df['valid_email'] = df['email'].notna()
Format Pattern with Regex
# Email must contain @
df['valid_email_format'] = df['email'].str.contains('@', na=False)

# Phone must be digits only
df['valid_phone'] = df['phone'].str.match(r'^\d{10}$', na=False)
Business Rule Check
# End date must be after start date
df['valid_date_order'] = df['end_date'] >= df['start_date']
Isolation and Reporting
# Combine all checks
validation_cols = ['valid_age', 'valid_customer_id', 'valid_email', 'valid_date_order']
df['passes_all_checks'] = df[validation_cols].all(axis=1)

# Isolate failures
failures = df[~df['passes_all_checks']]
failures.to_csv('output/validation_failures.csv')

# Report
print(f"Records: {len(df)}")
print(f"Passed: {df['passes_all_checks'].sum()}")
print(f"Failed: {(~df['passes_all_checks']).sum()}")

# Proceed with clean data
df_clean = df[df['passes_all_checks']]
You just learned to implement systematic validation and isolate bad records. Your data is now validated before analysis begins.
Bonus Resources
* Great Expectations Framework - open-source library for automated data validation at scale with rich reporting
* Data Quality Metrics - guidance on defining and measuring validation success rates and tracking improvements over time
* Pandas Validation Patterns - best practices for combining multiple validation checks and producing audit logs


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Data Consistency & Validation Rules


00h 59m 57s

Raw data has birth_date in year 2050, price is negative, customer_id is missing when required, campaign_end_date is before start_date. Build 5+ validation rules, isolate failures, and produce a structured validation report before analysis.
Task 1: Range Checks (1 mark)
df['valid_age'] = (df['age'] >= 0) & (df['age'] <= 150)
df['valid_price'] = df['price'] >= 0
df['valid_date'] = (df['birth_date'] >= '1920-01-01') & (df['birth_date'] <= pd.Timestamp.now())

print(f"Invalid ages: {(~df['valid_age']).sum()}")
Task 2: Null Constraints (1 mark)
df['valid_customer_id'] = df['customer_id'].notna()
df['valid_email'] = df['email'].notna()

print(f"Missing customer IDs: {(~df['valid_customer_id']).sum()}")
Task 3: Format Pattern Validation (1 mark)
df['valid_email_format'] = df['email'].str.contains('@', na=False)
df['valid_phone'] = df['phone'].str.match(r'^\d{10}$', na=False)

print(f"Invalid emails: {(~df['valid_email_format']).sum()}")
Task 4: Business Rule Validation (1 mark)
df['valid_date_order'] = df['end_date'] >= df['start_date']

print(f"Invalid date ranges: {(~df['valid_date_order']).sum()}")
Task 5: Validation Report (1 mark)
validation_cols = ['valid_age', 'valid_price', 'valid_customer_id', 
                  'valid_email_format', 'valid_date_order']

df['passes_all_checks'] = df[validation_cols].all(axis=1)

# Isolate failures
failures = df[~df['passes_all_checks']]
failures.to_csv('output/validation_failures.csv')

# Report
print(f"Records: {len(df)}")
print(f"Passed: {df['passes_all_checks'].sum()}")
print(f"Failed: {(~df['passes_all_checks']).sum()}")

df_clean = df[df['passes_all_checks']]
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. What validation rules are - How they differ from data cleaning
2. Range check example - Show specific rule from your data
3. Referential integrity - Validate relationships between columns
4. One business rule walkthrough - Logic for detecting violations
5. Adding new rules - How to extend without modifying existing tests
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

Outlier Detection with Statistical Methods
Multi-Source Merging & Join Validation


Student App | Kalvium


2.25
Multi-Source Merging & Join Validation

Hey Data Integrator!
Welcome. Single dataset cleaning is complete. Now comes integration: merging two or more datasets to build a unified view. A customer table joins with an orders table. Sales data joins with product data. But merges are fragile - keys can mismatch, one side has records the other doesn't, joining creates phantom rows. You must validate every join intentionally, compare row counts before and after, investigate unmatched keys, and document decisions.
Every analysis built on silently broken merges, every count that did not match reality because join created unexpected duplicates or lost records, every business decision made on incomplete merged data had the same root: joins were never validated. This lesson teaches you join validation. You will merge datasets with explicit join types, validate row counts, detect and isolate unmatched keys, investigate mismatches, and document join decisions with business reasoning.
The Real Scenario
THE PROBLEM
A dataset has 1000 customers. An orders table has 5000 records. Analyst merges them on customer_id without checking the join type. No error thrown. Result has 6200 rows - more than either input. Customer_id appears multiple times for different orders, which is correct, but the analyst never validated this. Later, customer count is computed and gets 6200 instead of 1000. Revenue per customer is wrong. Nobody knows the merge created duplicates by design. No documentation explains why the result is larger than either input. Business trusts wrong analysis.
THE SOLUTION
Specify join type explicitly: inner keeps only matched, left keeps all from left and matches from right, right keeps all from right and matches from left, outer keeps all from both. Print row counts before merge and after. Compare result size to inputs. Identify unmatched keys from both sides. Save unmatched to separate file. Document why that join type was chosen - is this the right business logic? Are unmatched records expected or problematic? All explicit. All validated. All documented.
Join Types and When to Use Each
Four Join Types, Each with Different Semantics
INNER JOIN
Keep only rows where key matches both sides. Result is smaller than inputs. Use when you want only complete records where both datasets agree.
LEFT JOIN
Keep all from left, matched from right. Use when left table is your source of truth and right is enrichment.
RIGHT JOIN
Keep all from right, matched from left. Mirrors left join - use when right is your authoritative table.
OUTER JOIN
Keep all from both sides. Result is larger than both inputs. Use when you need complete coverage and can handle nulls.
Key Takeaway: Row Count Changes Tell the Story
If result is smaller than both inputs = inner join behavior. If result equals larger input ≈ left/right join. If result > max(input1, input2) = outer join or multiplicity from shared keys.
You just learned the four join types and how row counts reveal what happened. Now you will implement validation.
Merge Validation Workflow
Merging, Validating, Investigating
Before and After Validation
# Before merge
print(f"Left table: {len(df_customers)} rows")
print(f"Right table: {len(df_orders)} rows")

# Merge explicitly
df_merged = pd.merge(
    df_customers,
    df_orders,
    on='customer_id',
    how='left'  # EXPLICIT join type
)

# After merge
print(f"Merged result: {len(df_merged)} rows")
print(f"Change: {len(df_merged) - len(df_customers)} rows")
Find Unmatched Keys
# Customers with no orders
unmatched_customers = df_customers[
    ~df_customers['customer_id'].isin(df_orders['customer_id'])
]

# Orders with no matching customer
unmatched_orders = df_orders[
    ~df_orders['customer_id'].isin(df_customers['customer_id'])
]

print(f"Customers without orders: {len(unmatched_customers)}")
print(f"Orphaned orders: {len(unmatched_orders)}")

# Save for investigation
unmatched_customers.to_csv('output/unmatched_customers.csv')
unmatched_orders.to_csv('output/unmatched_orders.csv')
Document Decision
Record in your notebook:
* Join type chosen and why
* Expected row counts vs actual
* Unmatched key counts and investigation findings
* Decision on what to do with unmatched records
You just learned to validate merges, find unmatched keys, and document decisions. Joins are now transparent and auditable.
Bonus Resources
* Pandas Merge Documentation - complete reference for join types, keys, and handling conflicts
* SQL Join Types Visualization - interactive guide showing exactly which rows each join type produces
* Handling Join Failures - patterns for investigating and resolving common merge problems and key mismatches


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Data Consistency & Validation Rules
Feature Engineering & Derived Business Columns



Student App | Kalvium


2.25 Multi-Source Merging & Join Validation
2.25
Multi-Source Merging & Join Validation

Hey Data Integrator!
Welcome. Single dataset cleaning is complete. Now comes integration: merging two or more datasets to build a unified view. A customer table joins with an orders table. Sales data joins with product data. But merges are fragile - keys can mismatch, one side has records the other doesn't, joining creates phantom rows. You must validate every join intentionally, compare row counts before and after, investigate unmatched keys, and document decisions.
Every analysis built on silently broken merges, every count that did not match reality because join created unexpected duplicates or lost records, every business decision made on incomplete merged data had the same root: joins were never validated. This lesson teaches you join validation. You will merge datasets with explicit join types, validate row counts, detect and isolate unmatched keys, investigate mismatches, and document join decisions with business reasoning.
The Real Scenario
THE PROBLEM
A dataset has 1000 customers. An orders table has 5000 records. Analyst merges them on customer_id without checking the join type. No error thrown. Result has 6200 rows - more than either input. Customer_id appears multiple times for different orders, which is correct, but the analyst never validated this. Later, customer count is computed and gets 6200 instead of 1000. Revenue per customer is wrong. Nobody knows the merge created duplicates by design. No documentation explains why the result is larger than either input. Business trusts wrong analysis.
THE SOLUTION
Specify join type explicitly: inner keeps only matched, left keeps all from left and matches from right, right keeps all from right and matches from left, outer keeps all from both. Print row counts before merge and after. Compare result size to inputs. Identify unmatched keys from both sides. Save unmatched to separate file. Document why that join type was chosen - is this the right business logic? Are unmatched records expected or problematic? All explicit. All validated. All documented.
Join Types and When to Use Each
Four Join Types, Each with Different Semantics
INNER JOIN
Keep only rows where key matches both sides. Result is smaller than inputs. Use when you want only complete records where both datasets agree.
LEFT JOIN
Keep all from left, matched from right. Use when left table is your source of truth and right is enrichment.
RIGHT JOIN
Keep all from right, matched from left. Mirrors left join - use when right is your authoritative table.
OUTER JOIN
Keep all from both sides. Result is larger than both inputs. Use when you need complete coverage and can handle nulls.
Key Takeaway: Row Count Changes Tell the Story
If result is smaller than both inputs = inner join behavior. If result equals larger input ≈ left/right join. If result > max(input1, input2) = outer join or multiplicity from shared keys.
You just learned the four join types and how row counts reveal what happened. Now you will implement validation.
Merge Validation Workflow
Merging, Validating, Investigating
Before and After Validation
# Before merge
print(f"Left table: {len(df_customers)} rows")
print(f"Right table: {len(df_orders)} rows")

# Merge explicitly
df_merged = pd.merge(
    df_customers,
    df_orders,
    on='customer_id',
    how='left'  # EXPLICIT join type
)

# After merge
print(f"Merged result: {len(df_merged)} rows")
print(f"Change: {len(df_merged) - len(df_customers)} rows")
Find Unmatched Keys
# Customers with no orders
unmatched_customers = df_customers[
    ~df_customers['customer_id'].isin(df_orders['customer_id'])
]

# Orders with no matching customer
unmatched_orders = df_orders[
    ~df_orders['customer_id'].isin(df_customers['customer_id'])
]

print(f"Customers without orders: {len(unmatched_customers)}")
print(f"Orphaned orders: {len(unmatched_orders)}")

# Save for investigation
unmatched_customers.to_csv('output/unmatched_customers.csv')
unmatched_orders.to_csv('output/unmatched_orders.csv')
Document Decision
Record in your notebook:
* Join type chosen and why
* Expected row counts vs actual
* Unmatched key counts and investigation findings
* Decision on what to do with unmatched records
You just learned to validate merges, find unmatched keys, and document decisions. Joins are now transparent and auditable.
Bonus Resources
* Pandas Merge Documentation - complete reference for join types, keys, and handling conflicts
* SQL Join Types Visualization - interactive guide showing exactly which rows each join type produces
* Handling Join Failures - patterns for investigating and resolving common merge problems and key mismatches


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Multi-Source Merging & Join Validation


00h 59m 47s

Merge customer table (1000 rows) with orders table (5000 rows). Validate join, compare row counts, detect unmatched keys. Document join decision with business reasoning.
Task 1: Explicit Join with Row Count Validation (1 mark)
print(f"Left: {len(df_customers)}")
print(f"Right: {len(df_orders)}")

df_merged = pd.merge(df_customers, df_orders, on='customer_id', how='left')

print(f"Merged: {len(df_merged)}")
print(f"Change: {len(df_merged) - len(df_customers)}")
Task 2: Detect Unmatched Keys (1 mark)
unmatched_customers = df_customers[~df_customers['customer_id'].isin(df_orders['customer_id'])]
unmatched_orders = df_orders[~df_orders['customer_id'].isin(df_customers['customer_id'])]

print(f"Customers without orders: {len(unmatched_customers)}")
print(f"Orphaned orders: {len(unmatched_orders)}")

unmatched_customers.to_csv('output/unmatched_customers.csv')
unmatched_orders.to_csv('output/unmatched_orders.csv')
Task 3: Compare Join Types (1 mark)
inner = pd.merge(df_customers, df_orders, how='inner')
left = pd.merge(df_customers, df_orders, how='left')
outer = pd.merge(df_customers, df_orders, how='outer')

print(f"Inner: {len(inner)}, Left: {len(left)}, Outer: {len(outer)}")
Task 4: Validate No Unexpected Duplication (1 mark)
# Check for unexpected column conflicts
print(df_merged.columns)

# If customer_id appears in both, verify merge key
key_counts = df_merged['customer_id'].value_counts()
print(f"Max orders per customer: {key_counts.max()}")
Task 5: Document Join Decision (1 mark)
join_report = {
    'join_type': 'left',
    'left_table': 'customers',
    'right_table': 'orders',
    'join_key': 'customer_id',
    'left_rows': len(df_customers),
    'right_rows': len(df_orders),
    'result_rows': len(df_merged),
    'unmatched_left': len(unmatched_customers),
    'unmatched_right': len(unmatched_orders),
    'reasoning': 'Left join preserves all customers; unmatched customers have no orders'
}

print(json.dumps(join_report, indent=2))
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Four join types - Inner, left, right, outer with example
2. Row count validation importance - Why it's essential
3. Unmatched keys meaning - What they represent
4. Join key selection - Why that column was chosen
5. Multi-key merges - Handling non-unique keys
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

Data Consistency & Validation Rules
Feature Engineering & Derived Business Columns



Student App | Kalvium

2.26
Feature Engineering & Derived Business Columns

Hey Feature Architect!
Welcome. Data is cleaned and merged. Now comes transformation into business meaning: raw column values become features that matter. A customer's 150 transactions is just a number. Binned into "high", "medium", "low" activity tier, it becomes actionable. Revenue divided by days-as-customer becomes average spend - a predictive signal. You must engineer features that carry business meaning, validate ranges, build reusable functions.
Every analyst who skipped feature engineering and analyzed raw columns, every model that performed poorly because it used counts instead of ratios, every analysis that missed patterns because they were hidden in raw values had the same root: features were not thoughtfully constructed. This lesson teaches you feature engineering. You will create derived columns with business names, implement binning and tiering with labels, compute composite scores, validate distributions, and build functions that scale.
The Real Scenario
THE PROBLEM
A customer churn model is built on raw columns: number_of_transactions, days_as_customer, total_spent. The model trains but performance is weak. Business interprets literally - "customers with 50 transactions churn more than those with 100". But raw counts mean nothing without context. 50 transactions over 5 years is very different from 50 in one month. A customer who spent500 in one month. Raw values lack meaning. The model learned on noise instead of signal.
THE SOLUTION

Engineer features with business meaning. Transactions per month = transactions / (days / 30). Spend per month captures rate, not just total. Bin into tiers: high engagement (>10 trans/month), medium (2-10), low (<2). Each tier has clear business meaning.

Feature Engineering Principles
Three Types of Features That Drive Value
RATIO FEATURES
Transactions per month. Revenue per customer per year. Returns per order. Ratios normalize for time/volume. Signal emerges from context.
TIERED/BINNED
Low/Medium/High engagement. Tier 1-5 based on quantiles. Categorical buckets enable segment analysis and interpretability.
COMPOSITE SCORES
RFM score combines Recency, Frequency, Monetary. Health score blends multiple indicators. Interpretable metrics that reflect business logic.
You just learned that ratio features normalize context, tiered features enable segmentation, and composite scores capture multiple signals. Now implement them.
Creating Features at Scale
Ratio Features, Binning, and Composite Scores
Ratio Features
# Normalize by time
df['transactions_per_month'] = df['total_transactions'] / (df['days_as_customer'] / 30)

# Normalize by volume
df['avg_spend_per_transaction'] = df['total_spent'] / df['total_transactions']

# Combinations
df['lifetime_value_per_month'] = df['total_spent'] / (df['days_as_customer'] / 30)
Binned Features with pd.cut and pd.qcut
# Equal-width bins (fixed ranges)
df['engagement_bin_equal'] = pd.cut(
    df['transactions_per_month'],
    bins=[0, 2, 10, float('inf')],
    labels=['low', 'medium', 'high']
)

# Equal-frequency bins (quantile-based)
df['spend_tier_quantile'] = pd.qcut(
    df['total_spent'],
    q=4,  # Quartile
    labels=['tier_1', 'tier_2', 'tier_3', 'tier_4']
)
Composite Score
# RFM-style composite
df['recency_score'] = pd.qcut(df['days_since_last_purchase'], q=5, labels=[5,4,3,2,1])
df['frequency_score'] = pd.qcut(df['purchase_count'], q=5, labels=[1,2,3,4,5])
df['monetary_score'] = pd.qcut(df['total_spent'], q=5, labels=[1,2,3,4,5])

# Combine into single score
df['rfm_score'] = df['recency_score'].astype(int) + df['frequency_score'].astype(int) + df['monetary_score'].astype(int)
You just learned to engineer features with business meaning. Your data now powers better analysis and interpretable models.
Bonus Resources
* Feature Engineering for Machine Learning - comprehensive guide covering ratio features, binning, and composite scores
* Pandas Cut and Qcut Documentation - complete reference with examples for binning strategies
* Business Metrics Framework - patterns for designing customer health scores and engagement metrics


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Multi-Source Merging & Join Validation
NumPy Vectorised Computation Workflow



Student App | Kalvium

2.26 Feature Engineering & Derived Business Columns
2.26
Feature Engineering & Derived Business Columns

Hey Feature Architect!
Welcome. Data is cleaned and merged. Now comes transformation into business meaning: raw column values become features that matter. A customer's 150 transactions is just a number. Binned into "high", "medium", "low" activity tier, it becomes actionable. Revenue divided by days-as-customer becomes average spend - a predictive signal. You must engineer features that carry business meaning, validate ranges, build reusable functions.
Every analyst who skipped feature engineering and analyzed raw columns, every model that performed poorly because it used counts instead of ratios, every analysis that missed patterns because they were hidden in raw values had the same root: features were not thoughtfully constructed. This lesson teaches you feature engineering. You will create derived columns with business names, implement binning and tiering with labels, compute composite scores, validate distributions, and build functions that scale.
The Real Scenario
THE PROBLEM
A customer churn model is built on raw columns: number_of_transactions, days_as_customer, total_spent. The model trains but performance is weak. Business interprets literally - "customers with 50 transactions churn more than those with 100". But raw counts mean nothing without context. 50 transactions over 5 years is very different from 50 in one month. A customer who spent500 in one month. Raw values lack meaning. The model learned on noise instead of signal.
THE SOLUTION

Engineer features with business meaning. Transactions per month = transactions / (days / 30). Spend per month captures rate, not just total. Bin into tiers: high engagement (>10 trans/month), medium (2-10), low (<2). Each tier has clear business meaning.

Feature Engineering Principles
Three Types of Features That Drive Value
RATIO FEATURES
Transactions per month. Revenue per customer per year. Returns per order. Ratios normalize for time/volume. Signal emerges from context.
TIERED/BINNED
Low/Medium/High engagement. Tier 1-5 based on quantiles. Categorical buckets enable segment analysis and interpretability.
COMPOSITE SCORES
RFM score combines Recency, Frequency, Monetary. Health score blends multiple indicators. Interpretable metrics that reflect business logic.
You just learned that ratio features normalize context, tiered features enable segmentation, and composite scores capture multiple signals. Now implement them.
Creating Features at Scale
Ratio Features, Binning, and Composite Scores
Ratio Features
# Normalize by time
df['transactions_per_month'] = df['total_transactions'] / (df['days_as_customer'] / 30)

# Normalize by volume
df['avg_spend_per_transaction'] = df['total_spent'] / df['total_transactions']

# Combinations
df['lifetime_value_per_month'] = df['total_spent'] / (df['days_as_customer'] / 30)
Binned Features with pd.cut and pd.qcut
# Equal-width bins (fixed ranges)
df['engagement_bin_equal'] = pd.cut(
    df['transactions_per_month'],
    bins=[0, 2, 10, float('inf')],
    labels=['low', 'medium', 'high']
)

# Equal-frequency bins (quantile-based)
df['spend_tier_quantile'] = pd.qcut(
    df['total_spent'],
    q=4,  # Quartile
    labels=['tier_1', 'tier_2', 'tier_3', 'tier_4']
)
Composite Score
# RFM-style composite
df['recency_score'] = pd.qcut(df['days_since_last_purchase'], q=5, labels=[5,4,3,2,1])
df['frequency_score'] = pd.qcut(df['purchase_count'], q=5, labels=[1,2,3,4,5])
df['monetary_score'] = pd.qcut(df['total_spent'], q=5, labels=[1,2,3,4,5])

# Combine into single score
df['rfm_score'] = df['recency_score'].astype(int) + df['frequency_score'].astype(int) + df['monetary_score'].astype(int)
You just learned to engineer features with business meaning. Your data now powers better analysis and interpretable models.
Bonus Resources
* Feature Engineering for Machine Learning - comprehensive guide covering ratio features, binning, and composite scores
* Pandas Cut and Qcut Documentation - complete reference with examples for binning strategies
* Business Metrics Framework - patterns for designing customer health scores and engagement metrics


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Feature Engineering & Derived Business Columns


00h 59m 58s

Raw transaction data has counts and totals but no business meaning. Engineer features: engagement_rate (transactions per month), spend_tier (low/medium/high), customer_health_score (composite metric). These features power better models and enable segment analysis.
Task 1: Compute Ratio Features (1 mark)
df['transactions_per_month'] = df['total_transactions'] / (df['days_as_customer'] / 30)
df['avg_spend_per_transaction'] = df['total_spent'] / df['total_transactions']
df['lifetime_value_per_month'] = df['total_spent'] / (df['days_as_customer'] / 30)

print(df[['transactions_per_month', 'avg_spend_per_transaction']].describe())
Task 2: Binning with Equal-Width Bins (1 mark)
df['engagement_tier'] = pd.cut(
    df['transactions_per_month'],
    bins=[0, 2, 10, float('inf')],
    labels=['low', 'medium', 'high']
)

print(df['engagement_tier'].value_counts())
Task 3: Binning with Quantiles (1 mark)
df['spend_quartile'] = pd.qcut(
    df['total_spent'],
    q=4,
    labels=['Q1', 'Q2', 'Q3', 'Q4']
)

print(df['spend_quartile'].value_counts())
Task 4: Composite Score (1 mark)
df['recency_score'] = pd.qcut(df['days_since_last_purchase'], q=5, labels=[5,4,3,2,1])
df['frequency_score'] = pd.qcut(df['purchase_count'], q=5, labels=[1,2,3,4,5])
df['monetary_score'] = pd.qcut(df['total_spent'], q=5, labels=[1,2,3,4,5])

df['rfm_score'] = (df['recency_score'].astype(int) + 
                   df['frequency_score'].astype(int) + 
                   df['monetary_score'].astype(int))
Task 5: Feature Validation (1 mark)
# Check ranges are sensible
print(f"Engagement tier distribution:\n{df['engagement_tier'].value_counts()}")
print(f"RFM score range: {df['rfm_score'].min()}-{df['rfm_score'].max()}")

# Ensure no NaNs introduced
print(f"Missing values: {df[['engagement_tier', 'spend_quartile', 'rfm_score']].isna().sum()}")
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Feature engineering definition - Why features beat raw columns
2. pd.cut vs pd.qcut - When each is appropriate
3. Composite score construction - Weighting decisions explained
4. Most business-meaningful feature - How it's used downstream
5. Data leakage - How to validate features don't leak future information
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

Multi-Source Merging & Join Validation
NumPy Vectorised Computation Workflow



Student App | Kalvium

2.27
NumPy Vectorised Computation Workflow

Hey Performance Optimizer!
Welcome. Features are engineered. Now comes optimization: replacing loop-based Python with vectorized NumPy operations. A Python loop that processes 1 million rows takes minutes. NumPy vectorization does it in milliseconds. You must understand when loops break down, how vectorization works, and how to integrate NumPy results back into Pandas DataFrames for real analytical workloads.
Every analyst who let loops run for hours when vectorization would finish in seconds, who processed data locally when it should have been parallelized, who did not measure performance before optimization had the same problem: they did not know vectorization existed or how to implement it. This lesson teaches you optimization. You will identify slow loop-based code, replace it with NumPy vectorization, measure time improvements, and integrate results into Pandas workflows.
The Real Scenario
THE PROBLEM
An analyst needs to normalize a revenue column to 0-1 scale. They write a Python loop: for each row, find min and max, apply formula, store result. On 100,000 rows it takes 45 seconds. Tomorrow, 1 million rows arrive and the script takes 7+ minutes. The analyst waits. Then needs to run it 10 times. Waiting becomes frustrating. They do not know that NumPy vectorization could do the same operation in 15 milliseconds - 3000x faster. They do not know that .apply() is also slow and that NumPy arrays are the answer. Time is wasted. Productivity dies.
THE SOLUTION
Recognize that Pandas operations on entire columns are fast but Python loops are slow. NumPy arrays are the fastest. For normalization, use NumPy: (arr - arr.min()) / (arr.max() - arr.min()). This is vectorized - computed in parallel across all elements. 1 million rows in milliseconds. Time performance using %timeit before and after. The improvement is dramatic and addictive once experienced. Integrate result back to DataFrame as new column. Scale achieved.
Loop vs Vectorization
Why Vectorization Dominates
PYTHON LOOP
Processes one row at a time. For 1M rows, Python interpreter is called 1M times. Overhead compounds. 45 seconds for 100k rows.
NUMPY VECTORIZATION
Compiled C code. Processes all rows in one operation. No interpreter overhead. Parallelizable. 15ms for 100k rows.
The Rough Math
NumPy is typically 100-10000x faster than loops on large arrays depending on operation complexity. At 100 rows the difference is invisible. At 10 million rows it's the difference between minutes and seconds. Once you experience it, you never go back to loops for numerical processing.
You just learned why vectorization dominates and what speeds are possible. Now you will implement it.
Implementing Vectorized Operations
Normalization, Scoring, and Ranking at Scale
Min-Max Normalization
import numpy as np

# SLOW: Loop version
normalized = []
for val in df['revenue']:
    normalized.append((val - df['revenue'].min()) / (df['revenue'].max() - df['revenue'].min()))

# FAST: NumPy vectorized
revenue_array = df['revenue'].values  # Convert to NumPy array
normalized = (revenue_array - revenue_array.min()) / (revenue_array.max() - revenue_array.min())
df['revenue_normalized'] = normalized
Z-Score Normalization
# NumPy vectorized
revenue_array = df['revenue'].values
z_scores = (revenue_array - revenue_array.mean()) / revenue_array.std()
df['revenue_zscore'] = z_scores
Measure Time Difference
import time

# Time loop version
start = time.time()
# ... loop code ...
loop_time = time.time() - start

# Time vectorized version
start = time.time()
# ... NumPy code ...
vec_time = time.time() - start

print(f"Loop: {loop_time:.3f}s")
print(f"NumPy: {vec_time:.3f}s")
print(f"Speedup: {loop_time/vec_time:.0f}x")
You just learned to implement vectorized operations and measure improvement. Your analytical workflows now scale to real production data volumes.
Bonus Resources
* NumPy Documentation - comprehensive reference for vectorized operations and array operations
* Vectorization vs Loops - detailed comparison with performance examples across different data sizes
* Performance Profiling Tools - using cProfile and line_profiler to identify slow code before optimizing


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Feature Engineering & Derived Business Columns
Distribution Analysis for Business Trends



Student App | Kalvium

2.27 NumPy Vectorised Computation Workflow
2.27
NumPy Vectorised Computation Workflow

Hey Performance Optimizer!
Welcome. Features are engineered. Now comes optimization: replacing loop-based Python with vectorized NumPy operations. A Python loop that processes 1 million rows takes minutes. NumPy vectorization does it in milliseconds. You must understand when loops break down, how vectorization works, and how to integrate NumPy results back into Pandas DataFrames for real analytical workloads.
Every analyst who let loops run for hours when vectorization would finish in seconds, who processed data locally when it should have been parallelized, who did not measure performance before optimization had the same problem: they did not know vectorization existed or how to implement it. This lesson teaches you optimization. You will identify slow loop-based code, replace it with NumPy vectorization, measure time improvements, and integrate results into Pandas workflows.
The Real Scenario
THE PROBLEM
An analyst needs to normalize a revenue column to 0-1 scale. They write a Python loop: for each row, find min and max, apply formula, store result. On 100,000 rows it takes 45 seconds. Tomorrow, 1 million rows arrive and the script takes 7+ minutes. The analyst waits. Then needs to run it 10 times. Waiting becomes frustrating. They do not know that NumPy vectorization could do the same operation in 15 milliseconds - 3000x faster. They do not know that .apply() is also slow and that NumPy arrays are the answer. Time is wasted. Productivity dies.
THE SOLUTION
Recognize that Pandas operations on entire columns are fast but Python loops are slow. NumPy arrays are the fastest. For normalization, use NumPy: (arr - arr.min()) / (arr.max() - arr.min()). This is vectorized - computed in parallel across all elements. 1 million rows in milliseconds. Time performance using %timeit before and after. The improvement is dramatic and addictive once experienced. Integrate result back to DataFrame as new column. Scale achieved.
Loop vs Vectorization
Why Vectorization Dominates
PYTHON LOOP
Processes one row at a time. For 1M rows, Python interpreter is called 1M times. Overhead compounds. 45 seconds for 100k rows.
NUMPY VECTORIZATION
Compiled C code. Processes all rows in one operation. No interpreter overhead. Parallelizable. 15ms for 100k rows.
The Rough Math
NumPy is typically 100-10000x faster than loops on large arrays depending on operation complexity. At 100 rows the difference is invisible. At 10 million rows it's the difference between minutes and seconds. Once you experience it, you never go back to loops for numerical processing.
You just learned why vectorization dominates and what speeds are possible. Now you will implement it.
Implementing Vectorized Operations
Normalization, Scoring, and Ranking at Scale
Min-Max Normalization
import numpy as np

# SLOW: Loop version
normalized = []
for val in df['revenue']:
    normalized.append((val - df['revenue'].min()) / (df['revenue'].max() - df['revenue'].min()))

# FAST: NumPy vectorized
revenue_array = df['revenue'].values  # Convert to NumPy array
normalized = (revenue_array - revenue_array.min()) / (revenue_array.max() - revenue_array.min())
df['revenue_normalized'] = normalized
Z-Score Normalization
# NumPy vectorized
revenue_array = df['revenue'].values
z_scores = (revenue_array - revenue_array.mean()) / revenue_array.std()
df['revenue_zscore'] = z_scores
Measure Time Difference
import time

# Time loop version
start = time.time()
# ... loop code ...
loop_time = time.time() - start

# Time vectorized version
start = time.time()
# ... NumPy code ...
vec_time = time.time() - start

print(f"Loop: {loop_time:.3f}s")
print(f"NumPy: {vec_time:.3f}s")
print(f"Speedup: {loop_time/vec_time:.0f}x")
You just learned to implement vectorized operations and measure improvement. Your analytical workflows now scale to real production data volumes.
Bonus Resources
* NumPy Documentation - comprehensive reference for vectorized operations and array operations
* Vectorization vs Loops - detailed comparison with performance examples across different data sizes
* Performance Profiling Tools - using cProfile and line_profiler to identify slow code before optimizing


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


NumPy Vectorised Computation Workflow


00h 59m 56s

Your normalization script processes 100k rows in 45 seconds using Python loops. Same operation with NumPy vectorization completes in 15ms. Replace loop-based logic with vectorized NumPy for production performance on million-row datasets.
Task 1: Replace Loop with NumPy Vectorization (1 mark)
import numpy as np

# SLOW: Loop
normalized_loop = []
for val in df['revenue']:
    normalized_loop.append((val - df['revenue'].min()) / (df['revenue'].max() - df['revenue'].min()))

# FAST: NumPy
revenue_array = df['revenue'].values
normalized_np = (revenue_array - revenue_array.min()) / (revenue_array.max() - revenue_array.min())
df['revenue_normalized'] = normalized_np
Task 2: Z-Score Normalization (1 mark)
revenue_array = df['revenue'].values
z_scores = (revenue_array - revenue_array.mean()) / revenue_array.std()
df['revenue_zscore'] = z_scores
Task 3: Bulk Ranking/Scoring (1 mark)
# Rank all customers by revenue
revenue_array = df['revenue'].values
rankings = np.argsort(-revenue_array)  # Negative for descending
df['revenue_rank'] = np.empty_like(rankings)
df['revenue_rank'][rankings] = np.arange(1, len(rankings) + 1)
Task 4: Time Performance Comparison (1 mark)
import time

# Time loop version
start = time.time()
result_loop = []
for val in df['revenue']:
    result_loop.append(val * 1.1)
loop_time = time.time() - start

# Time NumPy version
start = time.time()
result_np = df['revenue'].values * 1.1
np_time = time.time() - start

print(f"Loop: {loop_time:.4f}s")
print(f"NumPy: {np_time:.4f}s")
print(f"Speedup: {loop_time/np_time:.0f}x")
Task 5: Integrate Back to DataFrame (1 mark)
# All NumPy results go back to DataFrame as new columns
df['revenue_normalized'] = normalized_np
df['revenue_zscore'] = z_scores
df['revenue_rank'] = rankings

# Verify types and shapes
print(f"Shape: {df.shape}")
print(f"Dtypes:\n{df.dtypes}")
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Vectorization definition - Why it outperforms loops
2. NumPy array vs Pandas Series - When to use each
3. Min-max normalization - How and what range it produces
4. Computation walkthrough - Why NumPy was right tool
5. Large-scale scoring - Applying custom function to million rows
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

Feature Engineering & Derived Business Columns
Distribution Analysis for Business Trends



Student App | Kalvium

2.28
Distribution Analysis for Business Trends

Hey Distribution Analyst!
Welcome. Data is optimized. Now comes understanding: what does the distribution of each column actually tell us about the business? Skewness reveals that most customers are small and few are huge. Bimodal distributions hint that two different customer types exist. These patterns are hidden until you visualize and compute. Statistics connect to business interpretations.
Every analyst who reported an average without understanding if it was misleading, who missed hidden segmentation in data, who applied wrong statistics to skewed distributions had the same problem: they did not analyze distributions first. This lesson teaches you distribution analysis. You will plot histograms and KDE, compute skewness and kurtosis, identify abnormal patterns, connect statistics to business meaning, and compare segments.
The Real Scenario
THE PROBLEM
A revenue dataset has mean of5000". But the distribution is heavily skewed: 80% of customers spend under50,000. The mean is pulled up by outliers. The "average" is misleading. Median would be $450 - much more representative. Without visualizing, the analyst missed that there are really two customer types: small and enterprise. They applied mean-based forecasting to a bimodal distribution, producing wrong predictions.
THE SOLUTION
Always visualize distributions first. Plot histogram to see shape. Compute skewness (is it symmetric or pulled?) and kurtosis (are there extreme outliers?). High skewness means median better than mean. Identify if distribution is bimodal - suggests multiple segments. Compare distributions across key segments - do high-value customers look different? All these insights emerge visually and statistically. Then report truthfully: "Most customers spend50k+. These are two different business types."
Understanding Distributions
Skewness, Kurtosis, and What They Mean for Business
SKEWNESS
Is distribution symmetric? Skewness = 0 is symmetric. Positive skew (tail right): few huge customers. Negative skew (tail left): few very small. Skewed distributions require median not mean.
KURTOSIS
Are there extreme outliers or is distribution concentrated? High kurtosis = fat tails = extreme values likely. Low kurtosis = concentrated. Informs outlier expectations.
Computing and Interpreting
from scipy import stats

skewness = stats.skew(df['revenue'])
kurtosis = stats.kurtosis(df['revenue'])

print(f"Skewness: {skewness:.2f}")
print(f"Kurtosis: {kurtosis:.2f}")

# Interpretation
if abs(skewness) > 1:
    print("Highly skewed - use median")
if kurtosis > 3:
    print("Heavy tails - expect outliers")
You just learned to interpret skewness and kurtosis. Now you will visualize and segment.
Visualizing and Comparing Distributions
Histogram, KDE, and Segment Comparison
Histogram Shows Buckets
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.hist(df['revenue'], bins=50, edgecolor='black')
plt.xlabel('Revenue')
plt.ylabel('Count')
plt.title('Revenue Distribution')
plt.show()
Histogram divides range into equal-width buckets and counts. Shows shape and clusters clearly.
KDE Shows Smooth Distribution
df['revenue'].plot(kind='density', figsize=(10, 5))
plt.xlabel('Revenue')
plt.title('Revenue Distribution (Smoothed)')
plt.show()
KDE is smoother, easier to see true shape without bucket discretization.
Compare Segments
# High-value vs low-value customers
high_value = df[df['revenue'] > df['revenue'].quantile(0.75)]
low_value = df[df['revenue'] < df['revenue'].quantile(0.25)]

plt.figure(figsize=(10, 5))
plt.hist(high_value['revenue'], alpha=0.5, label='High-Value', bins=30)
plt.hist(low_value['revenue'], alpha=0.5, label='Low-Value', bins=30)
plt.legend()
plt.show()
You just learned to visualize distributions and compare segments. Business patterns are now visible and quantifiable.
Bonus Resources
* Distribution Shapes Reference - guide to identifying normal, skewed, bimodal, and heavy-tailed distributions visually
* Matplotlib Histogram and KDE - detailed documentation with all plotting options
* Statistical Distributions in Business - real-world examples of skewed and multimodal distributions in customer data


Assignment
Best Score
-


Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


NumPy Vectorised Computation Workflow
Correlation & Relationship Analysis

Student App | Kalvium

2.28 Distribution Analysis for Business Trends
2.28
Distribution Analysis for Business Trends

Hey Distribution Analyst!
Welcome. Data is optimized. Now comes understanding: what does the distribution of each column actually tell us about the business? Skewness reveals that most customers are small and few are huge. Bimodal distributions hint that two different customer types exist. These patterns are hidden until you visualize and compute. Statistics connect to business interpretations.
Every analyst who reported an average without understanding if it was misleading, who missed hidden segmentation in data, who applied wrong statistics to skewed distributions had the same problem: they did not analyze distributions first. This lesson teaches you distribution analysis. You will plot histograms and KDE, compute skewness and kurtosis, identify abnormal patterns, connect statistics to business meaning, and compare segments.
The Real Scenario
THE PROBLEM
A revenue dataset has mean of5000". But the distribution is heavily skewed: 80% of customers spend under50,000. The mean is pulled up by outliers. The "average" is misleading. Median would be $450 - much more representative. Without visualizing, the analyst missed that there are really two customer types: small and enterprise. They applied mean-based forecasting to a bimodal distribution, producing wrong predictions.
THE SOLUTION
Always visualize distributions first. Plot histogram to see shape. Compute skewness (is it symmetric or pulled?) and kurtosis (are there extreme outliers?). High skewness means median better than mean. Identify if distribution is bimodal - suggests multiple segments. Compare distributions across key segments - do high-value customers look different? All these insights emerge visually and statistically. Then report truthfully: "Most customers spend50k+. These are two different business types."
Understanding Distributions
Skewness, Kurtosis, and What They Mean for Business
SKEWNESS
Is distribution symmetric? Skewness = 0 is symmetric. Positive skew (tail right): few huge customers. Negative skew (tail left): few very small. Skewed distributions require median not mean.
KURTOSIS
Are there extreme outliers or is distribution concentrated? High kurtosis = fat tails = extreme values likely. Low kurtosis = concentrated. Informs outlier expectations.
Computing and Interpreting
from scipy import stats

skewness = stats.skew(df['revenue'])
kurtosis = stats.kurtosis(df['revenue'])

print(f"Skewness: {skewness:.2f}")
print(f"Kurtosis: {kurtosis:.2f}")

# Interpretation
if abs(skewness) > 1:
    print("Highly skewed - use median")
if kurtosis > 3:
    print("Heavy tails - expect outliers")
You just learned to interpret skewness and kurtosis. Now you will visualize and segment.
Visualizing and Comparing Distributions
Histogram, KDE, and Segment Comparison
Histogram Shows Buckets
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.hist(df['revenue'], bins=50, edgecolor='black')
plt.xlabel('Revenue')
plt.ylabel('Count')
plt.title('Revenue Distribution')
plt.show()
Histogram divides range into equal-width buckets and counts. Shows shape and clusters clearly.
KDE Shows Smooth Distribution
df['revenue'].plot(kind='density', figsize=(10, 5))
plt.xlabel('Revenue')
plt.title('Revenue Distribution (Smoothed)')
plt.show()
KDE is smoother, easier to see true shape without bucket discretization.
Compare Segments
# High-value vs low-value customers
high_value = df[df['revenue'] > df['revenue'].quantile(0.75)]
low_value = df[df['revenue'] < df['revenue'].quantile(0.25)]

plt.figure(figsize=(10, 5))
plt.hist(high_value['revenue'], alpha=0.5, label='High-Value', bins=30)
plt.hist(low_value['revenue'], alpha=0.5, label='Low-Value', bins=30)
plt.legend()
plt.show()
You just learned to visualize distributions and compare segments. Business patterns are now visible and quantifiable.
Bonus Resources
* Distribution Shapes Reference - guide to identifying normal, skewed, bimodal, and heavy-tailed distributions visually
* Matplotlib Histogram and KDE - detailed documentation with all plotting options
* Statistical Distributions in Business - real-world examples of skewed and multimodal distributions in customer data


Assignment
Best Score

Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment

Distribution Analysis for Business Trends


00h 59m 58s

Revenue column has mean450. Skewness = 2.5 (highly right-skewed). This means the average is misleading - few huge customers pull the mean up. Analyze distributions, compute skewness/kurtosis, identify hidden segments, connect statistics to business interpretations.
Task 1: Distribution Plots (1 mark)
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(df['revenue'], bins=50, edgecolor='black')
axes[0].set_title('Revenue Distribution (Histogram)')
axes[0].set_xlabel('Revenue')

# KDE
df['revenue'].plot(kind='density', ax=axes[1])
axes[1].set_title('Revenue Distribution (KDE)')

plt.tight_layout()
plt.savefig('output/revenue_distribution.png')
Task 2: Compute Skewness and Kurtosis (1 mark)
from scipy import stats

skewness = stats.skew(df['revenue'])
kurtosis = stats.kurtosis(df['revenue'])

print(f"Skewness: {skewness:.2f}")
print(f"Kurtosis: {kurtosis:.2f}")

if abs(skewness) > 1:
    print("Highly skewed - use median not mean")
if kurtosis > 3:
    print("Heavy tails - expect outliers")
Task 3: Identify Abnormal Patterns (1 mark)
# Check for bimodality
print(df['revenue'].describe())

# Percentiles show if distribution is bimodal
percentiles = df['revenue'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
print(percentiles)

# If gap between 0.75 and 0.9 is large, suggests two groups
Task 4: Compare Segment Distributions (1 mark)
# Split by high-value vs low-value
high_value = df[df['revenue'] > df['revenue'].quantile(0.75)]
low_value = df[df['revenue'] < df['revenue'].quantile(0.25)]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(high_value['revenue'], bins=30, alpha=0.7, label='High-Value')
axes[0].hist(low_value['revenue'], bins=30, alpha=0.7, label='Low-Value')
axes[0].legend()
axes[0].set_title('Revenue: High vs Low Value Customers')

# Compare metrics
print(f"High-value: mean={high_value['revenue'].mean():.0f}, median={high_value['revenue'].median():.0f}")
print(f"Low-value: mean={low_value['revenue'].mean():.0f}, median={low_value['revenue'].median():.0f}")
Task 5: Business Interpretation (1 mark)
# Connect statistics to business decisions
interpretation = f"""
Revenue Distribution Analysis:

Skewness: {skewness:.2f} → {"Highly right-skewed" if skewness > 1 else "Moderate"}
Mean: ${df['revenue'].mean():.0f}
Median: ${df['revenue'].median():.0f}
Interpretation: {'Most customers are small; few are huge enterprise accounts' if skewness > 1 else 'Balanced distribution'}

Kurtosis: {kurtosis:.2f} → {"Fat tails (outliers)" if kurtosis > 3 else "Normal"}
Max: ${df['revenue'].max():.0f}
Top 1%: ${df['revenue'].quantile(0.99):.0f}

Business Action: {'Segment into small/enterprise for different strategies' if skewness > 1 else 'Uniform strategy'}
"""

print(interpretation)
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Skewed distributions - How they affect choice of statistic
2. Histogram vs KDE - When each is useful
3. Kurtosis meaning - High values and implications
4. Abnormal pattern - What you found and business cause
5. Statistical testing - Testing if two distributions differ
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

NumPy Vectorised Computation Workflow
Correlation & Relationship Analysis

Student App | Kalvium

2.29
Correlation & Relationship Analysis
Hey Relationship Detective!
Welcome. Distributions are understood. Now comes relationship discovery: which metrics move together and which predict business outcomes? High engagement might correlate strongly with retention. Discount depth might correlate with margin damage. You must compute correlations, visualize relationships, understand which signals matter most, and avoid confusing correlation with causation.
Every analyst who built a model on spurious correlation, who thought two moving-together metrics meant one caused the other, who missed the true causal drivers hidden by noise had the same problem: they did not systematically analyze relationships first. This lesson teaches you correlation analysis. You will compute Pearson and Spearman correlations, visualize heatmaps, identify strong relationships, distinguish correlation from causation, and use correlation for feature selection.
The Real Scenario
THE PROBLEM
A churn model is built using 50 features without first analyzing which ones matter. The model trains on noise. Performance is weak. An analyst notices that number_of_support_tickets correlates strongly with churn (r=0.8). They conclude: "Support tickets cause churn!" The business starts refusing support tickets to reduce churn. Churn gets worse because the real causal driver was "customer pain causes both support requests AND churn". The correlation was real but the direction of causation was backwards. Without correlation analysis upfront, the business made a harmful decision.
THE SOLUTION
Compute correlations between all feature pairs before modeling. Visualize with heatmap to identify strong relationships. Separate "moves together" from "causes". Use correlation for feature selection - highly correlated features are redundant, keep the more interpretable. Understand that correlation r=0.8 says "they move together" not "one causes the other". Always ask: what is the direction of causation? Is there a confounding variable? Correlation is an investigative tool, not an explanation.
Correlation Methods
Pearson vs Spearman
PEARSON
Measures linear relationship. Assumes normal distribution. Sensitive to outliers. Use for continuous data that appears linear.
SPEARMAN
Measures monotonic relationship using rank. Robust to outliers and nonlinear monotonic trends. Use for ordinal data or when relationship is not linear.
Computing and Interpreting
# Pearson correlation matrix
pearson_corr = df.corr(method='pearson')

# Spearman correlation matrix
spearman_corr = df.corr(method='spearman')

# Interpretation: r ranges -1 to +1
# r > 0.7: strong positive (one high, other high)
# r < -0.7: strong negative (one high, other low)
# |r| < 0.3: weak relationship
You just learned that Pearson and Spearman measure different types of relationships. Now visualize and interpret.
Analyzing and Visualizing Relationships
Heatmaps, Strong Pairs, and Causation
Visualize Correlation Matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Compute correlation
corr_matrix = df.corr()

# Plot heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.show()
Heatmap color intensity shows correlation strength. Red = positive, blue = negative.
Find Strong Relationships
# Flatten correlation matrix
corr_flat = corr_matrix.unstack()
strong_corrs = corr_flat[corr_flat.abs() > 0.7].sort_values(ascending=False)

# Print top correlations (excluding self-correlation)
for (var1, var2), corr in strong_corrs[strong_corrs != 1.0].head(10).items():
    print(f"{var1} <-> {var2}: {corr:.2f}")
Correlation ≠ Causation
Correlation says "they move together". Causation says "one makes the other happen". Three possibilities:
* A causes B
* B causes A
* C causes both A and B (confounding variable)
Always reason about direction before concluding causation.
You just learned to compute correlations, visualize them, find strong relationships, and distinguish from causation. Relationship analysis is now systematic.
Bonus Resources
* Pearson vs Spearman Correlation - detailed comparison with visual examples of when each is appropriate
* Correlation Heatmap Visualization - guide to creating and interpreting correlation matrices
* Confounding Variables and Causal Inference - explanation of when correlation misleads and how to reason about causation

Distribution Analysis for Business Trends
GroupBy Aggregation & Segment Insights

Student App | Kalvium

2.29 Correlation & Relationship Analysis
2.29
Correlation & Relationship Analysis

Hey Relationship Detective!
Welcome. Distributions are understood. Now comes relationship discovery: which metrics move together and which predict business outcomes? High engagement might correlate strongly with retention. Discount depth might correlate with margin damage. You must compute correlations, visualize relationships, understand which signals matter most, and avoid confusing correlation with causation.
Every analyst who built a model on spurious correlation, who thought two moving-together metrics meant one caused the other, who missed the true causal drivers hidden by noise had the same problem: they did not systematically analyze relationships first. This lesson teaches you correlation analysis. You will compute Pearson and Spearman correlations, visualize heatmaps, identify strong relationships, distinguish correlation from causation, and use correlation for feature selection.
The Real Scenario
THE PROBLEM
A churn model is built using 50 features without first analyzing which ones matter. The model trains on noise. Performance is weak. An analyst notices that number_of_support_tickets correlates strongly with churn (r=0.8). They conclude: "Support tickets cause churn!" The business starts refusing support tickets to reduce churn. Churn gets worse because the real causal driver was "customer pain causes both support requests AND churn". The correlation was real but the direction of causation was backwards. Without correlation analysis upfront, the business made a harmful decision.
THE SOLUTION
Compute correlations between all feature pairs before modeling. Visualize with heatmap to identify strong relationships. Separate "moves together" from "causes". Use correlation for feature selection - highly correlated features are redundant, keep the more interpretable. Understand that correlation r=0.8 says "they move together" not "one causes the other". Always ask: what is the direction of causation? Is there a confounding variable? Correlation is an investigative tool, not an explanation.
Correlation Methods
Pearson vs Spearman
PEARSON
Measures linear relationship. Assumes normal distribution. Sensitive to outliers. Use for continuous data that appears linear.
SPEARMAN
Measures monotonic relationship using rank. Robust to outliers and nonlinear monotonic trends. Use for ordinal data or when relationship is not linear.
Computing and Interpreting
# Pearson correlation matrix
pearson_corr = df.corr(method='pearson')

# Spearman correlation matrix
spearman_corr = df.corr(method='spearman')

# Interpretation: r ranges -1 to +1
# r > 0.7: strong positive (one high, other high)
# r < -0.7: strong negative (one high, other low)
# |r| < 0.3: weak relationship
You just learned that Pearson and Spearman measure different types of relationships. Now visualize and interpret.
Analyzing and Visualizing Relationships
Heatmaps, Strong Pairs, and Causation
Visualize Correlation Matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Compute correlation
corr_matrix = df.corr()

# Plot heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.show()
Heatmap color intensity shows correlation strength. Red = positive, blue = negative.
Find Strong Relationships
# Flatten correlation matrix
corr_flat = corr_matrix.unstack()
strong_corrs = corr_flat[corr_flat.abs() > 0.7].sort_values(ascending=False)

# Print top correlations (excluding self-correlation)
for (var1, var2), corr in strong_corrs[strong_corrs != 1.0].head(10).items():
    print(f"{var1} <-> {var2}: {corr:.2f}")
Correlation ≠ Causation
Correlation says "they move together". Causation says "one makes the other happen". Three possibilities:
* A causes B
* B causes A
* C causes both A and B (confounding variable)
Always reason about direction before concluding causation.
You just learned to compute correlations, visualize them, find strong relationships, and distinguish from causation. Relationship analysis is now systematic.
Bonus Resources
* Pearson vs Spearman Correlation - detailed comparison with visual examples of when each is appropriate
* Correlation Heatmap Visualization - guide to creating and interpreting correlation matrices
* Confounding Variables and Causal Inference - explanation of when correlation misleads and how to reason about causation

Assignment
Best Score

Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

Start Assignment

Correlation & Relationship Analysis

00h 59m 58s

Build a churn prediction model. Compute correlations between all features and churn. Find that support_tickets correlates r=0.8 with churn and conclude "tickets cause churn". But causation goes backward: customer pain causes both tickets AND churn. Use correlation analysis to identify true signals and avoid spurious conclusions.
Task 1: Compute Pearson and Spearman Correlation (1 mark)
# Pearson (linear relationships)
pearson_corr = df.corr(method='pearson')

# Spearman (monotonic, robust to outliers)
spearman_corr = df.corr(method='spearman')

# Compare which correlations differ
comparison = pd.DataFrame({
    'pearson': pearson_corr['churn'],
    'spearman': spearman_corr['churn']
})
print(comparison)
Task 2: Visualize Correlation Heatmap (1 mark)
import seaborn as sns

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(pearson_corr, annot=True, cmap='coolwarm', center=0, ax=ax)
ax.set_title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig('output/correlation_heatmap.png')
Task 3: Identify Strongly Correlated Pairs (1 mark)
# Flatten and find strong correlations
corr_flat = pearson_corr.unstack()
strong = corr_flat[corr_flat.abs() > 0.7].sort_values(ascending=False)

# Exclude self-correlation (r=1.0)
strong_pairs = strong[strong != 1.0].head(10)
print(strong_pairs)
Task 4: Business Interpretation (1 mark)
# For each strong correlation, reason about causation
analysis = {
    'support_tickets <-> churn': {
        'correlation': 0.8,
        'possible_directions': [
            'support_tickets → churn (customer gives up after contacting support)',
            'churn → support_tickets (unhappy customers contact support before leaving)',
            'customer_pain → both (underlying issue causes both)'
        ],
        'data_indicates': 'Likely customer_pain is the confounder; tickets are symptom not cause',
        'action': 'Focus on reducing pain, not blocking tickets'
    }
}

print(json.dumps(analysis, indent=2))
Task 5: Feature Selection Based on Correlation (1 mark)
# High correlation means redundancy - keep more interpretable feature
df_features = df[['engagement', 'transactions_per_month', 'support_tickets', 'churn']]

# transactions_per_month and engagement are r=0.92 (correlated)
# Drop redundant, keep interpretable
df_features = df_features.drop('engagement', axis=1)

print(df_features.corr())
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Pearson vs Spearman - When each applies
2. Correlation value interpretation - What r=0.85 means
3. Correlation ≠ causation - Concrete example
4. Significant correlations found - Business implication
5. Relationship with categorical variable - How to correlate with non-numeric Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

Distribution Analysis for Business Trends
GroupBy Aggregation & Segment Insights

Student App | Kalvium

2.30
GroupBy Aggregation & Segment Insights

Hey Segment Analyzer!
Welcome. Relationships are analyzed. Now comes the fundamental operation that unlocks business insights: grouping and aggregating. A flat dataset of 1 million transactions becomes meaningful when sliced by customer, by time, by product category. Groupby reveals which segments perform best, what patterns emerge, where business levers are. You must master groupby, compute multi-level aggregations, and surface segment insights.
Every analyst who reported dataset-wide statistics instead of segment-specific insights, who missed that performance varies wildly by segment, who relied on aggregates instead of understanding distribution had the same problem: they did not fully leverage groupby. This lesson teaches you segment aggregation. You will compute segment-wise metrics, aggregate across multiple dimensions, rank segments, create pivot tables, surface actionable segment insights.
The Real Scenario
THE PROBLEM
A company has customer churn data. Average churn rate across all customers is 5%. Business reports "we have 5% churn". Marketing develops strategy to address churn. But they never segment. When you actually look closely: enterprise customers (5% of customer base) have 1% churn and generate 70% of revenue. SMB customers (40% of base) have 12% churn but low revenue. Startups (55% of base) have 8% churn. The "average" is meaningless. One segment is healthy and profitable. Two segments are problem areas needing different strategies. But nobody knew because the data was never grouped.
THE SOLUTION
Never report dataset-wide statistics. Always segment first. Groupby customer_type and compute churn rate per segment. Groupby customer_type and product and compute revenue per segment per product. Rank segments by key metric and highlight top and bottom performers. Surface actionable insight: "Enterprise segment is healthy (1% churn). SMB segment requires intervention (12% churn)." Now strategy is evidence-based. Now business resources go to the problems that actually exist.
GroupBy Fundamentals
Split-Apply-Combine Pattern
SPLIT
Divide dataset into groups by key column. Each customer_type is a group. Each region is a group. Each product is a group.
APPLY
Compute aggregation within each group. Sum revenue. Count churned customers. Average spend. Aggregate per group.
COMBINE
Stitch results back into summary table. One row per group showing aggregated values. Ready for analysis.
GroupBy Methods: Agg, Transform, Apply
# .agg() - Combine results into single value per group
df.groupby('customer_type')['churn'].agg(['sum', 'count', 'mean'])

# .transform() - Return result same shape as original (broadcast per row)
df['churn_rate_by_type'] = df.groupby('customer_type')['churn'].transform('mean')

# .apply() - Custom function per group
df.groupby('customer_type')['revenue'].apply(lambda x: x.nlargest(3).sum())
You just learned how groupby works and the three methods for different use cases. Now implement multi-level aggregations.
Multi-Dimensional Aggregation
Multiple GroupBy Keys, Pivot Tables, Ranking
Multi-Level GroupBy
# Group by two dimensions simultaneously
segment_product_revenue = df.groupby(['customer_type', 'product'])['revenue'].sum()

# Unstack for cleaner view (pivot-like)
segment_product_revenue.unstack()

# Returns DataFrame with customer_type as rows, product as columns
Pivot Table for Two-Dimensional View
pivot = pd.pivot_table(
    df,
    values='revenue',
    index='customer_type',
    columns='product',
    aggfunc='sum'
)

# Shows revenue for each (customer_type, product) pair
Rank and Highlight Top/Bottom Segments
# Compute churn rate per segment
segment_metrics = df.groupby('customer_type').agg({
    'churn': 'mean',
    'revenue': 'sum',
    'customer_id': 'count'
})

segment_metrics.columns = ['churn_rate', 'total_revenue', 'customer_count']

# Rank segments
segment_metrics['churn_rank'] = segment_metrics['churn_rate'].rank()

# Sort by churn rate to see worst/best first
segment_metrics.sort_values('churn_rate', ascending=False)
Surface Actionable Insights
For each segment: "Segment X has Y% churn and Z% of revenue. Action required: [specific intervention based on segment characteristics]". Segment performance now visible and actionable.
You just learned to aggregate across multiple dimensions, rank segments, and surface actionable insights. Data is now transformed into business decisions.
The End of Your Journey
You have completed all 20 lessons of comprehensive data engineering and analysis. From isolated workspaces through GitHub workflows, Python scripts, data validation, ingestion, profiling, documentation, null handling, type enforcement, deduplication, string cleaning, datetime parsing, outlier detection, validation rules, merging, feature engineering, performance optimization, distribution analysis, correlation discovery, and segment aggregation - you can now build professional analytical workflows with confidence. Your analysis is trustworthy, reproducible, auditable, and impactful.
Bonus Resources
* Pandas GroupBy Documentation - complete reference with all aggregation functions and advanced patterns
* Pivot Table Guide - detailed tutorial on creating and interpreting two-dimensional aggregations
* Segment Analysis Best Practices - framework for identifying, analyzing, and acting on segment-level insights

Assignment
Best Score
-

Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or more

60m

Start Assignment


Correlation & Relationship Analysis
Time-Series Trend & Rolling Metrics


Student App | Kalvium

2.30 GroupBy Aggregation & Segment Insights
2.30
GroupBy Aggregation & Segment Insights

Hey Segment Analyzer!
Welcome. Relationships are analyzed. Now comes the fundamental operation that unlocks business insights: grouping and aggregating. A flat dataset of 1 million transactions becomes meaningful when sliced by customer, by time, by product category. Groupby reveals which segments perform best, what patterns emerge, where business levers are. You must master groupby, compute multi-level aggregations, and surface segment insights.
Every analyst who reported dataset-wide statistics instead of segment-specific insights, who missed that performance varies wildly by segment, who relied on aggregates instead of understanding distribution had the same problem: they did not fully leverage groupby. This lesson teaches you segment aggregation. You will compute segment-wise metrics, aggregate across multiple dimensions, rank segments, create pivot tables, surface actionable segment insights.
The Real Scenario
THE PROBLEM
A company has customer churn data. Average churn rate across all customers is 5%. Business reports "we have 5% churn". Marketing develops strategy to address churn. But they never segment. When you actually look closely: enterprise customers (5% of customer base) have 1% churn and generate 70% of revenue. SMB customers (40% of base) have 12% churn but low revenue. Startups (55% of base) have 8% churn. The "average" is meaningless. One segment is healthy and profitable. Two segments are problem areas needing different strategies. But nobody knew because the data was never grouped.
THE SOLUTION
Never report dataset-wide statistics. Always segment first. Groupby customer_type and compute churn rate per segment. Groupby customer_type and product and compute revenue per segment per product. Rank segments by key metric and highlight top and bottom performers. Surface actionable insight: "Enterprise segment is healthy (1% churn). SMB segment requires intervention (12% churn)." Now strategy is evidence-based. Now business resources go to the problems that actually exist.
GroupBy Fundamentals
Split-Apply-Combine Pattern
SPLIT
Divide dataset into groups by key column. Each customer_type is a group. Each region is a group. Each product is a group.
APPLY
Compute aggregation within each group. Sum revenue. Count churned customers. Average spend. Aggregate per group.
COMBINE
Stitch results back into summary table. One row per group showing aggregated values. Ready for analysis.
GroupBy Methods: Agg, Transform, Apply
# .agg() - Combine results into single value per group
df.groupby('customer_type')['churn'].agg(['sum', 'count', 'mean'])

# .transform() - Return result same shape as original (broadcast per row)
df['churn_rate_by_type'] = df.groupby('customer_type')['churn'].transform('mean')

# .apply() - Custom function per group
df.groupby('customer_type')['revenue'].apply(lambda x: x.nlargest(3).sum())
You just learned how groupby works and the three methods for different use cases. Now implement multi-level aggregations.
Multi-Dimensional Aggregation
Multiple GroupBy Keys, Pivot Tables, Ranking
Multi-Level GroupBy
# Group by two dimensions simultaneously
segment_product_revenue = df.groupby(['customer_type', 'product'])['revenue'].sum()

# Unstack for cleaner view (pivot-like)
segment_product_revenue.unstack()

# Returns DataFrame with customer_type as rows, product as columns
Pivot Table for Two-Dimensional View
pivot = pd.pivot_table(
    df,
    values='revenue',
    index='customer_type',
    columns='product',
    aggfunc='sum'
)

# Shows revenue for each (customer_type, product) pair
Rank and Highlight Top/Bottom Segments
# Compute churn rate per segment
segment_metrics = df.groupby('customer_type').agg({
    'churn': 'mean',
    'revenue': 'sum',
    'customer_id': 'count'
})

segment_metrics.columns = ['churn_rate', 'total_revenue', 'customer_count']

# Rank segments
segment_metrics['churn_rank'] = segment_metrics['churn_rate'].rank()

# Sort by churn rate to see worst/best first
segment_metrics.sort_values('churn_rate', ascending=False)
Surface Actionable Insights
For each segment: "Segment X has Y% churn and Z% of revenue. Action required: [specific intervention based on segment characteristics]". Segment performance now visible and actionable.
You just learned to aggregate across multiple dimensions, rank segments, and surface actionable insights. Data is now transformed into business decisions.
The End of Your Journey
You have completed all 20 lessons of comprehensive data engineering and analysis. From isolated workspaces through GitHub workflows, Python scripts, data validation, ingestion, profiling, documentation, null handling, type enforcement, deduplication, string cleaning, datetime parsing, outlier detection, validation rules, merging, feature engineering, performance optimization, distribution analysis, correlation discovery, and segment aggregation - you can now build professional analytical workflows with confidence. Your analysis is trustworthy, reproducible, auditable, and impactful.
Bonus Resources
* Pandas GroupBy Documentation - complete reference with all aggregation functions and advanced patterns
* Pivot Table Guide - detailed tutorial on creating and interpreting two-dimensional aggregations
* Segment Analysis Best Practices - framework for identifying, analyzing, and acting on segment-level insights

Assignment
Best Score
Complete this assignment to show your understanding of the concepts you've learned.

Get 60% or moe
Start Assignment
GroupBy Aggregation & Segment Insights


00h 59m 57s

Average churn rate is 5%. But: enterprise segment (5% of base) has 1% churn and 70% of revenue. SMB segment (40% of base) has 12% churn. Startups (55%) have 8%. One dataset-wide statistic hides the real story. Use groupby to segment and surface actionable insights.
Task 1: Single-Level GroupBy with Multiple Aggregations (1 mark)
segment_metrics = df.groupby('customer_type').agg({
    'churn': 'mean',
    'revenue': 'sum',
    'customer_id': 'count',
    'support_tickets': 'mean'
})

segment_metrics.columns = ['churn_rate', 'total_revenue', 'customer_count', 'avg_support_tickets']

print(segment_metrics)
Task 2: Multi-Level GroupBy (1 mark)
# Two dimensions simultaneously
product_segment = df.groupby(['customer_type', 'product']).agg({
    'revenue': 'sum',
    'customer_id': 'count'
})

product_segment.columns = ['total_revenue', 'customer_count']

# Unstack for cleaner view
product_segment_pivot = product_segment.unstack()
print(product_segment_pivot)
Task 3: Pivot Table (1 mark)
# Two-dimensional view: customer_type rows, product columns
pivot = pd.pivot_table(
    df,
    values='revenue',
    index='customer_type',
    columns='product',
    aggfunc='sum'
)

print(pivot)
Task 4: Rank and Identify Top/Bottom Performers (1 mark)
# Rank segments by churn
segment_metrics['churn_rank'] = segment_metrics['churn_rate'].rank()

# Sort to see worst first
worst_first = segment_metrics.sort_values('churn_rate', ascending=False)
print(worst_first)

# Profit/revenue ranking
segment_metrics['revenue_contribution'] = (segment_metrics['total_revenue'] / segment_metrics['total_revenue'].sum() * 100)
print(segment_metrics[['revenue_contribution', 'churn_rate']])
Task 5: Surface Actionable Segment Insights (1 mark)
# Create insight summary
insights = []

for segment in segment_metrics.index:
    row = segment_metrics.loc[segment]
    
    insight = {
        'segment': segment,
        'customer_count': int(row['customer_count']),
        'churn_rate': f"{row['churn_rate']:.1%}",
        'total_revenue': f"${row['total_revenue']:.0f}",
        'revenue_contribution': f"{row['revenue_contribution']:.1f}%",
        'action': ''
    }
    
    # Action based on metrics
    if row['churn_rate'] > 0.10:
        insight['action'] = 'HIGH PRIORITY: Churn above 10%. Investigate pain points.'
    elif row['churn_rate'] < 0.02:
        insight['action'] = 'Healthy. Maintain current service level.'
    else:
        insight['action'] = 'Monitor. No immediate action needed.'
    
    insights.append(insight)

insights_df = pd.DataFrame(insights)
print(insights_df.to_string(index=False))
insights_df.to_csv('output/segment_insights.csv', index=False)
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. GroupBy split-apply-combine - How it works internally
2. .agg() vs .transform() vs .apply() - When each is used
3. Pivot table value - When better than standard groupby
4. Segment insight - Most significant finding and business action
5. Percentage share - Computing % of total within each group
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Submit

Correlation & Relationship Analysis
Time-Series Trend & Rolling Metrics


Student App | Kalvium


2.31
Time-Series Trend & Rolling Metrics

Hey Time-Series Tracker!
Welcome. Data is segmented. Now comes understanding change over time: rolling averages that smooth daily noise to reveal true trends, cumulative sums that track growing totals, period-over-period changes that measure business momentum. Static snapshots miss the story. Time-series reveals whether business is accelerating or decelerating, whether volatility is increasing, whether seasonal patterns hold. You must compute rolling metrics, measure period changes, visualize trends, identify inflection points.
Every business analyst who reported only current month numbers instead of trends, who missed acceleration signals hidden in daily volatility, who did not compare this month to last had the same problem: they did not think in time-series terms. This lesson teaches you temporal analysis. You will resample data by period, compute rolling windows, calculate change rates, identify trends, and connect patterns to business implications.
The Real Scenario
THE PROBLEM
Revenue today is45k. Someone reports "revenue up 11%!" But looking at the raw daily numbers reveals: Tuesday45k, Sunday51k, Friday35k. Someone panics and recommends deep discounting. But without understanding the underlying trend, they cannot tell if this is temporary or structural decline. Decisions made on noise instead of signal.
THE SOLUTION
Compute 7-day rolling average that smooths daily noise. Plot it alongside raw numbers - the rolling line shows the true trend. Compute month-over-month change with .pct_change() to measure growth rate. Cumulative sum shows total revenue accumulated over time. Price drop causes daily drop but rolling average shows whether underlying trend is still positive. Now you see signal clearly. Now decisions are informed by trend, not daily noise.
Rolling Windows and Resampling
Three Time-Series Perspectives
RAW DATA
Daily values unchanged. Complete detail. Maximum noise. Useful for detecting anomalies but hard to see trend direction.
ROLLING AVERAGE
7-day or 30-day window. Smooths noise. Reveals true trend. Lags at turning points but clear signal.
RESAMPLED (MONTHLY)
One value per month. Maximum aggregation. Removes all detail. Shows big picture direction clearly.
When to Use Each Perspective
Raw data detects anomalies and spikes. Rolling average reveals sustainable trends. Resampling answers "what happened month-to-month?" Choose the right window for the business question. Daily traders need hourly rolling averages. Monthly business reviews need resampling to weeks or months.
You just learned that time-series analysis requires choosing the right aggregation level for your business question. Now implement rolling metrics.
Computing Rolling Metrics
Rolling Windows, Resampling, and Change Rates
Rolling Average
Compute moving average across a sliding window. 7 days, 30 days, or custom periods.
# 7-day rolling average
df['revenue_ma7'] = df['revenue'].rolling(window=7).mean()

# 30-day rolling average
df['revenue_ma30'] = df['revenue'].rolling(window=30).mean()

# Plot raw vs rolling
plt.plot(df['date'], df['revenue'], label='Raw', alpha=0.3)
plt.plot(df['date'], df['revenue_ma7'], label='7-day MA')
plt.plot(df['date'], df['revenue_ma30'], label='30-day MA')
plt.legend()
plt.show()
Resampling by Time Period
# Set date as index
df_ts = df.set_index('date')

# Resample to weekly
weekly = df_ts['revenue'].resample('W').sum()

# Resample to monthly
monthly = df_ts['revenue'].resample('M').sum()

# Different aggregations
weekly_count = df_ts['orders'].resample('W').count()
weekly_avg = df_ts['revenue'].resample('W').mean()
Period-Over-Period Change
# Month-over-month percentage change
monthly_revenue = df_ts['revenue'].resample('M').sum()
mom_change = monthly_revenue.pct_change() * 100

print(f"Jan → Feb: {mom_change.iloc[1]:.1f}% change")

# Week-over-week
weekly_revenue = df_ts['revenue'].resample('W').sum()
wow_change = weekly_revenue.pct_change() * 100
Cumulative Sum
# Running total of revenue
df['cumulative_revenue'] = df['revenue'].cumsum()

# Shows total accumulated to each point
plt.plot(df['date'], df['cumulative_revenue'])
plt.title('Cumulative Revenue Over Time')
plt.show()
You just learned rolling windows, resampling, and change calculations. Trend analysis is now part of your analytical toolkit.
Identifying and Interpreting Trends
Pattern Recognition and Business Implications
Trend Patterns
# Calculate trend direction
monthly = df_ts['revenue'].resample('M').sum()
trend = monthly.iloc[-1] - monthly.iloc[-3]  # Last month vs 3 months ago

if trend > 0:
    print("Uptrend - Accelerating")
elif trend < 0:
    print("Downtrend - Declining")
else:
    print("Flat - Stable")
You just learned how to identify trends and connect them to business decisions. Time-series analysis now informs strategy.

Time-Series Trend & Rolling Metrics


00h 59m 54s

Your revenue data shows daily fluctuations: $10k one day, $8k the next, $12k the day after. This noise masks the true trend. Build rolling averages, compute period-over-period changes, and visualize trends alongside raw data. Identify whether business is accelerating or declining based on sustainable metrics.
Task 1: Resample Data by Time Period (1 mark)
Objective: Aggregate raw daily data into weekly and monthly buckets
df_ts = df.set_index('date')

# Weekly aggregation
weekly_revenue = df_ts['revenue'].resample('W').sum()
weekly_count = df_ts['orders'].resample('W').count()
weekly_avg = df_ts['revenue'].resample('W').mean()

print(weekly_revenue)
print(weekly_count)
Requirements:
* Resample to at least 2 time periods (weekly, monthly, or quarterly)
* Use different aggregation functions (sum, count, mean)
* Compare results: show which period has highest revenue
Task 2: Compute Rolling Window Average (1 mark)
Objective: Smooth daily noise using 7-day and 30-day rolling averages
df['revenue_ma7'] = df['revenue'].rolling(window=7).mean()
df['revenue_ma30'] = df['revenue'].rolling(window=30).mean()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['revenue'], label='Raw', alpha=0.3)
plt.plot(df['date'], df['revenue_ma7'], label='7-day MA')
plt.plot(df['date'], df['revenue_ma30'], label='30-day MA')
plt.legend()
plt.savefig('rolling_avg.png')
Requirements:
* Compute rolling averages for window sizes 7 and 30 days
* Plot raw data alongside both rolling averages
* Identify where the rolling average reveals a trend hidden by daily noise
Task 3: Calculate Month-over-Month Percentage Change (1 mark)
monthly_revenue = df_ts['revenue'].resample('M').sum()
mom_change = monthly_revenue.pct_change() * 100

print(mom_change)

# Show which months had growth vs decline
growth_months = mom_change[mom_change > 0]
decline_months = mom_change[mom_change < 0]
Requirements:
* Compute .pct_change() for monthly aggregations
* Document months with positive vs negative growth
* Explain what the pattern shows (accelerating, declining, or stable)
Task 4: Compute Cumulative Sum (1 mark)
Objective: Track total accumulated revenue over time
df['cumulative_revenue'] = df['revenue'].cumsum()

plt.plot(df['date'], df['cumulative_revenue'])
plt.title('Cumulative Revenue Over Time')
plt.savefig('cumulative.png')

# Show growth rate
print(f"Total revenue: ${df['cumulative_revenue'].iloc[-1]:,.0f}")
Requirements:
* Compute cumulative sum for at least one metric (revenue, customers, orders)
* Visualize cumulative growth
* Calculate total accumulated by end of period
Task 5: Identify Trend Pattern and Business Implications (1 mark)
Objective: Connect statistical observations to business decisions
# Analyze rolling average trend
recent_ma30 = df['revenue_ma30'].iloc[-30:]
trend_direction = 'up' if recent_ma30.iloc[-1] > recent_ma30.iloc[0] else 'down'
trend_magnitude = ((recent_ma30.iloc[-1] - recent_ma30.iloc[0]) / recent_ma30.iloc[0]) * 100

analysis = f"""
TREND ANALYSIS:

Rolling Average Trend: {trend_direction.upper()}
Change over last 30 days: {trend_magnitude:.1f}%

Month-over-month growth: {mom_change.iloc[-1]:.1f}%

Business Implications:
- {['Accelerating growth - maintain current strategy', 'Declining momentum - investigate causes'][0 if trend_direction == 'up' else 1]}
- Revenue volatility: ${df['revenue'].std():.0f} (measure of noise)
"""

print(analysis)
Requirements:
* Compute trend direction (up/down/flat) using rolling average
* Calculate magnitude of change
* Document business implication: "What does this pattern mean for the business?"
* Suggest action: "What should we do based on this trend?"
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
What should be in your PR:
* /scripts/rolling_metrics.py - script computing all metrics
* /output/rolling_avg.png - plot comparing raw vs rolling averages
* /output/trend_analysis.txt - business interpretation
* /notebooks/time_series_analysis.ipynb - full analysis notebook
2. Video
Your video should explain:
1. Resampling definition - How it differs from groupby
2. Rolling window mechanics - Why window size matters
3. .pct_change() explanation - What negative values mean
4. Trend interpretation walkthrough - Business implications of the pattern
5. Missing data handling - How to work with gaps in time-series
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.


2.32
Behavioural Analysis & User Segmentation

Hey Segment Comparator!
Welcome. Trends are understood. Now comes segmentation: comparing how different user types or operational categories behave. Enterprise customers have 1% churn. SMB customers have 12% churn. Two totally different stories. Yet aggregate reporting hides both. You must define segments, compute metrics per segment, compare side-by-side, identify which segments require different strategies, document the business implications.
Every business that treated all customers the same, that used one-size-fits-all strategy when customer types needed different approaches, that never compared segment performance had the same problem: they never looked at behaviour by segment. This lesson teaches you comparative analysis. You will define segments, calculate metrics per group, visualize comparisons, and surface actionable segment insights.
The Real Scenario
THE PROBLEM
Average customer lifetime value across all segments is150,000 each. SMB customers worth2,000. The "average" is useless. Marketing wastes budget on low-value segments and under-invests in high-value. Product features developed without knowing which segments want them. Churn prevention strategy is generic when it needs to be segment-specific.
THE SOLUTION
Segment by customer_type. Compute lifetime value, churn, feature usage, support cost per segment. Compare in a table and heatmap. Immediately visible: enterprise needs premium support, SMB needs self-service, startup needs education. Budget allocation becomes data-driven. Product prioritization becomes evidence-based.
Defining and Comparing Segments
Three Comparison Perspectives
SUMMARY TABLE
Metrics side-by-side by segment. Clear numbers. Easy to scan. Best for stakeholders who want facts.
HEATMAP
Color intensity shows metric values. Patterns visible instantly. Best for comparing many metrics across many segments.
BOX PLOTS
Distribution within each segment. Shows spread not just average. Reveals if segment has outliers.
You just learned three ways to compare segments. Now implement comparative metrics.
Computing Segment Metrics
GroupBy Comparison and Visualization
Summary Metrics by Segment
segment_metrics = df.groupby('customer_type').agg({
    'lifetime_value': 'mean',
    'churn': 'mean',
    'support_tickets': 'mean',
    'customer_id': 'count'
})

segment_metrics.columns = ['avg_ltv', 'churn_rate', 'avg_tickets', 'customer_count']

# Format for readability
segment_metrics['avg_ltv'] = segment_metrics['avg_ltv'].apply(lambda x: f'${x:,.0f}')
segment_metrics['churn_rate'] = segment_metrics['churn_rate'].apply(lambda x: f'{x:.1%}')

print(segment_metrics)
Heatmap Visualization
import seaborn as sns

# Normalize metrics for color comparison
segment_heatmap = segment_metrics.copy()
segment_heatmap['ltv'] = pd.to_numeric(segment_heatmap['avg_ltv'], errors='coerce')
segment_heatmap['churn'] = segment_heatmap['churn_rate'].str.rstrip('%').astype(float)

# Plot
sns.heatmap(segment_heatmap[['ltv', 'churn', 'avg_tickets']], annot=True, cmap='RdYlGn')
plt.title('Segment Comparison Heatmap')
plt.show()
Segment Insights
# Identify top and bottom performers
top_segment = segment_metrics['avg_ltv'].idxmax()
bottom_segment = segment_metrics['avg_ltv'].idxmin()

print(f"Highest value: {top_segment}")
print(f"Lowest value: {bottom_segment}")
print(f"\nHighest churn: {segment_metrics['churn_rate'].idxmax()}")
print(f"Lowest churn: {segment_metrics['churn_rate'].idxmin()}")
You just learned to compute segment metrics and compare visually. Segment strategy is now evidence-based.
Behavioural Analysis & User Segmentation


00h 59m 56s

Enterprise customers have 1% churn. SMB customers have 12% churn. Startup customers have 8% churn. But aggregate reporting hides all three stories and reports "average 7% churn". Segment by customer type, compute 4+ metrics per segment, visualize comparisons, and surface actionable insights specific to each segment.
Task 1: Define Segments and Compute Metrics (1 mark)
segment_metrics = df.groupby('customer_type').agg({
    'lifetime_value': 'mean',
    'churn': 'mean',
    'support_tickets': 'mean',
    'retention_days': 'mean',
    'customer_id': 'count'
})

segment_metrics.columns = ['avg_ltv', 'churn_rate', 'avg_tickets', 'avg_retention', 'count']
print(segment_metrics)
Requirements:
* Define at least 3 segments (customer_type, region, product_tier, etc.)
* Compute 4+ metrics per segment
* Document segment sizes (sample counts)
Task 2: Summary Statistics Table (1 mark)
Format metrics with readable labels and comparison:
segment_summary = segment_metrics.copy()
segment_summary['ltv_rank'] = segment_summary['avg_ltv'].rank(ascending=False)
segment_summary['churn_rank'] = segment_summary['churn_rate'].rank(ascending=True)

print(segment_summary[['avg_ltv', 'ltv_rank', 'churn_rate', 'churn_rank']])
Requirements:
* Rank segments by at least 2 metrics
* Format for readability (currency, percentages)
* Show both absolute values and rankings
Task 3: Visual Comparison (1 mark)
import matplotlib.pyplot as plt
import seaborn as sns

# Heatmap
sns.heatmap(segment_metrics[['avg_ltv', 'churn_rate', 'avg_tickets']], 
            annot=True, cmap='RdYlGn', cbar_kws={'label': 'Value'})
plt.title('Segment Comparison Heatmap')
plt.savefig('segment_heatmap.png')
Requirements:
* Create heatmap showing 3+ metrics across segments
* Use color to show high (green) vs low (red)
* Ensure readability with annotations
Task 4: Top and Bottom Performer Analysis (1 mark)
# Highest value segment
top_segment = segment_metrics['avg_ltv'].idxmax()
top_value = segment_metrics.loc[top_segment, 'avg_ltv']

# Highest churn segment
high_churn = segment_metrics['churn_rate'].idxmax()

insights = f"""
HIGHEST VALUE: {top_segment} = ${top_value:,.0f}
HIGHEST CHURN: {high_churn} = {segment_metrics.loc[high_churn, 'churn_rate']:.1%}
BEST RETENTION: {segment_metrics['avg_retention'].idxmax()}
"""

print(insights)
Requirements:
* Identify top performer by value
* Identify bottom performer by churn
* Document specific segment names and metrics
Task 5: Business-Facing Insights (1 mark)
business_summary = """
SEGMENT STRATEGY SUMMARY:

Enterprise (5% of base, $150k LTV, 1% churn):
- Highest value, lowest churn
- Action: Maintain premium support, retention focus

SMB (40% of base, $8k LTV, 12% churn):
- Middle value, high churn risk
- Action: Improve onboarding, cheaper support tier

Startup (55% of base, $2k LTV, 8% churn):
- Lowest value, moderate churn
- Action: Self-service, education-focused
"""

print(business_summary)
Requirements:
* Write 2-3 sentence insight per segment
* Include specific action recommendation
* Connect to observed metrics (not generic)
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Segment definition - Why these segments matter
2. Most meaningful difference - Business implication
3. Sample size caution - Why large/small segments need different confidence
4. Visualization explanation - What does the heatmap communicate?
5. Actionability threshold - When is a difference large enough to act on?
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.33
Funnel Analysis & Drop-Off Detection

Hey Funnel Engineer!
Welcome. Segments are compared. Now comes identifying bottlenecks: multi-step processes where users drop off. Signup → payment → first transaction → retention. 100 start signup, 80 complete payment, 50 make first transaction, 30 stay. Where is the friction? Drop-off between payment and first transaction loses 40%. That is your priority. Fix it and revenue grows. You must analyze funnels, quantify drop-off, identify the biggest leak, calculate business impact.
Every business that lost revenue to unknown friction in its processes, that did not measure where users dropped, that optimized the wrong step had the same root: they never analyzed funnels. This lesson teaches you funnel analysis. You will define sequential stages, compute drop-off rates, identify the biggest leak, and calculate business impact of fixing each step.
The Real Scenario
THE PROBLEM
A company has 10,000 users click "Sign Up". 8,000 enter email. 6,000 create password. 5,000 verify email. 4,000 add payment method. 2,000 make first purchase. The company knows "conversion is 20%". But where is the biggest leak? Nobody computed drop-off at each step. Product team builds features that do not address the actual bottleneck. Time and money wasted on wrong priorities.
THE SOLUTION
Compute drop-off at each step: email entry 20% loss, password 25% loss, email verification 17% loss, payment 20% loss, first purchase 50% loss. Last step is biggest leak. Focus there first. Fix first purchase friction and revenue doubles immediately. Data shows exactly where to focus limited engineering resources.
Funnel Anatomy
Sequential Stages and Drop-Off Measurement
ABSOLUTE DROP
10,000 start. 8,000 complete step 1. 2,000 dropped. Absolute number of lost users.
DROP RATE
2,000 / 10,000 = 20% dropped. Percentage of who entered stage.
COMPLETION RATE
8,000 / 10,000 = 80% completed. Percentage who continued forward.
You just learned funnel metrics and drop-off measurement. Now compute your funnel.
Building Funnels
Defining Stages and Computing Conversion
Define Funnel Stages
# Count users at each stage
stage1 = len(df[df['signup_completed'] == 1])
stage2 = len(df[df['email_verified'] == 1])
stage3 = len(df[df['payment_added'] == 1])
stage4 = len(df[df['first_purchase'] == 1])

stages = {
    'Sign Up': stage1,
    'Email Verified': stage2,
    'Payment Added': stage3,
    'First Purchase': stage4
}

print(stages)
Compute Drop-Off
# Drop-off between consecutive stages
stage_list = list(stages.values())
stage_names = list(stages.keys())

drop_off = []
for i in range(len(stage_list) - 1):
    drop = stage_list[i] - stage_list[i+1]
    drop_pct = (drop / stage_list[i]) * 100
    drop_off.append({
        'from': stage_names[i],
        'to': stage_names[i+1],
        'lost': drop,
        'drop_rate': f'{drop_pct:.1f}%'
    })

funnel_df = pd.DataFrame(drop_off)
print(funnel_df)
Visualize Funnel
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(stages.keys(), stages.values(), color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
ax.set_ylabel('Users')
ax.set_title('Funnel Visualization')
ax.set_ylim(0, max(stages.values()) * 1.1)

# Annotate with numbers
for stage, count in stages.items():
    ax.text(stage, count, str(count), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()
You just learned to measure funnels and identify bottlenecks. Business priorities are now data-driven.
Funnel Analysis & Drop-Off Detection


00h 59m 52s

Your signup funnel: 10,000 click signup → 8,000 enter email → 6,000 create password → 5,000 verify email → 4,000 add payment → 2,000 make first purchase. You know conversion is 20%. But where is the biggest leak? Measure drop-off at each step, identify the highest-impact bottleneck, calculate business cost of each drop-off, and recommend which step to optimize first.
Task 1: Define Funnel Stages and Count Users (1 mark)
Objective: Track volume through each step
# Count users at each stage
stage1_signup = len(df[df['signup_completed'] == 1])
stage2_email = len(df[df['email_entered'] == 1])
stage3_password = len(df[df['password_created'] == 1])
stage4_verified = len(df[df['email_verified'] == 1])
stage5_payment = len(df[df['payment_added'] == 1])
stage6_purchase = len(df[df['first_purchase'] == 1])

stages = {
    'Sign Up': stage1_signup,
    'Email Entered': stage2_email,
    'Password Created': stage3_password,
    'Email Verified': stage4_verified,
    'Payment Added': stage5_payment,
    'First Purchase': stage6_purchase
}

print(stages)
Requirements:
* Define 5+ sequential stages
* Count users at each stage
* Show stage progression (each stage has fewer users than previous)
Task 2: Compute Drop-Off Rate Between Stages (1 mark)
stage_list = list(stages.values())
stage_names = list(stages.keys())

drop_off = []
for i in range(len(stage_list) - 1):
    users_before = stage_list[i]
    users_after = stage_list[i+1]
    users_lost = users_before - users_after
    drop_pct = (users_lost / users_before) * 100
    
    drop_off.append({
        'from_stage': stage_names[i],
        'to_stage': stage_names[i+1],
        'users_lost': users_lost,
        'completion_rate': f'{(users_after/users_before)*100:.1f}%',
        'drop_rate': f'{drop_pct:.1f}%'
    })

funnel_df = pd.DataFrame(drop_off)
print(funnel_df)

# Find biggest drop
biggest_drop_idx = funnel_df['users_lost'].idxmax()
print(f"\nBiggest drop: {funnel_df.loc[biggest_drop_idx]}")
Requirements:
* Calculate drop-off as both absolute users lost and percentage
* Identify the stage with highest drop-off rate
* Document completion rate (% who moved forward) at each stage
Task 3: Visualize Funnel (1 mark)
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))

colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
ax.bar(stages.keys(), stages.values(), color=colors)

ax.set_ylabel('Users', fontsize=12)
ax.set_xlabel('Stage', fontsize=12)
ax.set_title('Signup Funnel: Volume by Stage', fontsize=14)
ax.set_ylim(0, max(stages.values()) * 1.15)

# Annotate counts
for stage, count in stages.items():
    ax.text(stage, count, str(count), ha='center', va='bottom', fontweight='bold')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('funnel_chart.png', dpi=150)
plt.show()

print("Funnel visualization saved")
Requirements:
* Create bar chart showing user count at each stage
* Annotate each bar with count
* Color code to show progression
* Save visualization with proper labels
Task 4: Calculate Business Impact of Each Drop-Off (1 mark)
# Assign revenue value per customer completing
revenue_per_customer = 100

impact_analysis = []
for idx, row in funnel_df.iterrows():
    users_lost = row['users_lost']
    revenue_lost = users_lost * revenue_per_customer
    impact_analysis.append({
        'drop_point': f"{row['from_stage']} → {row['to_stage']}",
        'users_lost': users_lost,
        'revenue_impact': f'${revenue_lost:,.0f}',
        'priority': 'HIGH' if revenue_lost > 100000 else 'MEDIUM'
    })

impact_df = pd.DataFrame(impact_analysis)
print(impact_df.sort_values('users_lost', ascending=False))
Requirements:
* Assign monetary value per customer (revenue, LTV, or profit)
* Calculate revenue impact of each drop-off
* Rank by business impact (not just user count)
* Identify highest-priority bottleneck
Task 5: Actionable Recommendation (1 mark)
highest_impact = funnel_df.loc[funnel_df['users_lost'].idxmax()]

recommendation = f"""
FUNNEL OPTIMIZATION PRIORITY:

CRITICAL BOTTLENECK:
Stage: {highest_impact['from_stage']} → {highest_impact['to_stage']}
Users Lost: {highest_impact['users_lost']:,.0f}
Drop Rate: {highest_impact['drop_rate']}
Revenue Impact: ${highest_impact['users_lost'] * 100:,.0f}

ROOT CAUSE INVESTIGATION NEEDED:
- Is step unclear? (Poor UX)
- Is step too complex? (Too many fields)
- Is step optional? (Should be required)
- Is step timing wrong? (Too early/late in funnel)

RECOMMENDED ACTION:
1. A/B test simplified version of step
2. Monitor drop rate before/after
3. Estimate revenue recovery
4. Roll out to 100% if improvement > 5%

EXPECTED IMPACT:
If we improve {highest_impact['from_stage']} → {highest_impact['to_stage']} completion by 10%:
Additional conversions: {int(highest_impact['users_lost'] * 0.1):,.0f}
Additional revenue: ${int(highest_impact['users_lost'] * 0.1 * 100):,.0f}
"""

print(recommendation)
Requirements:
* Identify the single highest-priority stage to optimize
* Explain why (users lost + revenue impact)
* Suggest specific hypotheses for why drop-off occurs
* Estimate business value of fixing the bottleneck
* Propose measurable success criteria
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
What should be in PR:
* /scripts/funnel_analysis.py - funnel computation
* /output/funnel_chart.png - visualization
* /output/funnel_analysis.txt - drop-off metrics and recommendations
* /notebooks/funnel_analysis.ipynb - full analysis
2. Video
1. What is funnel analysis - Business question it answers
2. Stage definition - How stages were chosen from dataset
3. Drop-off calculation - Formula and meaning
4. Biggest bottleneck identified - Business impact explained
5. Comparing funnels - How to compare across time periods or segments
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.34
KPI Definition & Business Metric Design

Hey KPI Architect!
Welcome. Bottlenecks are identified. Now comes defining what success means: KPIs (Key Performance Indicators) that measure business performance. Revenue is not a KPI - it is raw output. Monthly Recurring Revenue per customer (MRR/customer) is a KPI - it measures sustainable business health. You must define KPIs with formulas, establish target ranges, document dependencies, build reusable computation functions that stakeholders can trust.
Every business that reported different numbers depending on who was calculating, that lacked agreement on what "success" meant, that changed metric definitions mid-year destroying year-over-year comparisons had the same problem: KPIs were never formally defined. This lesson teaches you KPI design. You will define business metrics formally, establish targets, document formulas, and build functions that compute KPIs consistently.
The Real Scenario
THE PROBLEM
Three teams report different customer counts. Finance uses "unique email addresses ever entered". Sales uses "customers who completed payment". Marketing uses "users who clicked signup". Nobody agrees. Board meeting shows three "customer counts". Trust breaks. Then metrics are "updated" to be more favorable. Suddenly numbers rise without actual change. Year-over-year comparison becomes impossible. Was performance 10% growth or just definition change?
THE SOLUTION
Define KPIs formally: name, formula, data source columns, target range, update frequency, owner. "Active Customers = users with transaction in last 30 days". Compute in code. Everyone uses the same function. One number. Trust established. Targets are stretch but achievable. When metric definition changes, it is documented and previous data is restated. Consistency enables real business performance management.
KPI Fundamentals
What Makes a Metric a KPI
RAW METRIC
Total revenue $100k. Transactions 500. Customers 1000. Just numbers. No context. No target. No meaning without comparison.
KPI (KEY METRIC)
Revenue per customer =100. Revenue per transaction =200. Ratio has meaning. Can be targeted. Success-oriented.
You just learned that KPIs are ratios and targets, not raw numbers. Now define your KPIs formally.
Defining KPIs
Formal KPI Definition and Computation
KPI Reference Document
KPI: Monthly Active Users (MAU)
Formula: COUNT(DISTINCT customer_id) WHERE last_transaction_date >= TODAY() - 30 days
Data Source: transactions table
Target Range: 5000-6000
Owner: Product Lead
Update Frequency: Daily
Notes: Indicator of product engagement; seasonal dips in Q4
Compute KPI in Code
def calculate_mau(df, days=30):
    """Monthly Active Users: distinct customers with transaction in last N days."""
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    active = df[df['transaction_date'] >= cutoff]['customer_id'].nunique()
    return active

def calculate_revenue_per_customer(df):
    """Average revenue generated per unique customer."""
    total_revenue = df['amount'].sum()
    unique_customers = df['customer_id'].nunique()
    return total_revenue / unique_customers

# Compute
mau = calculate_mau(df)
rpc = calculate_revenue_per_customer(df)

print(f"MAU: {mau}")
print(f"Revenue per Customer: ${rpc:.2f}")
Validate Against Targets
targets = {
    'mau': (5000, 6000),
    'rpc': (90, 110),
    'churn_rate': (0, 0.05)
}

kpis = {
    'mau': mau,
    'rpc': rpc,
    'churn_rate': calculate_churn(df)
}

for metric, (min_val, max_val) in targets.items():
    actual = kpis[metric]
    if min_val <= actual <= max_val:
        print(f"✓ {metric}: {actual:.1f} (target: {min_val}-{max_val})")
    else:
        print(f"✗ {metric}: {actual:.1f} (target: {min_val}-{max_val}) - OUT OF RANGE")
You just learned to define and compute KPIs formally. Consistent measurement and accountability are now possible.

KPI Definition & Business Metric Design


00h 59m 56s

Three teams report different customer counts: Finance says 50,000 (anyone who ever entered an email). Sales says 35,000 (completed payment). Product says 28,000 (made a purchase). Board meeting shows three different numbers. Lack of agreed KPI definition breaks trust. Define 5+ KPIs formally with formulas, establish target ranges, build reusable computation functions that all teams use.
Task 1: Define KPI Reference Document (1 mark)
Create a reference file for each KPI:
KPI: Monthly Active Users (MAU)
Definition: Distinct customers with at least one transaction in last 30 days
Formula: COUNT(DISTINCT customer_id) WHERE transaction_date >= TODAY() - 30 days
Data Source: transactions table (columns: customer_id, transaction_date)
Target Range: 5,000 - 6,000
Owner: Product Manager
Update Frequency: Daily
Notes: Indicator of product engagement; seasonal dips in Q4
Requirements:
* Define at least 5 KPIs
* Each with: name, definition, formula, source, target, owner, frequency, notes
* Store in kpi_reference.md file
Task 2: Implement KPI Computation Functions (1 mark)
def calculate_mau(df, days=30):
    """Monthly Active Users: distinct customers active in last N days."""
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    return df[df['transaction_date'] >= cutoff]['customer_id'].nunique()

def calculate_revenue_per_customer(df):
    """Average revenue per unique customer."""
    return df['amount'].sum() / df['customer_id'].nunique()

def calculate_churn_rate(df, period_days=30):
    """Customers who had activity in period 1 but none in period 2."""
    period_1_end = pd.Timestamp.now() - pd.Timedelta(days=period_days)
    period_1_start = period_1_end - pd.Timedelta(days=period_days)
    period_2_end = pd.Timestamp.now()
    period_2_start = pd.Timestamp.now() - pd.Timedelta(days=period_days)
    
    active_p1 = df[(df['transaction_date'] >= period_1_start) & 
                   (df['transaction_date'] <= period_1_end)]['customer_id'].unique()
    active_p2 = df[(df['transaction_date'] >= period_2_start) & 
                   (df['transaction_date'] <= period_2_end)]['customer_id'].unique()
    
    churned = len([x for x in active_p1 if x not in active_p2])
    return churned / len(active_p1) if len(active_p1) > 0 else 0

# Compute all KPIs
mau = calculate_mau(df)
rpc = calculate_revenue_per_customer(df)
churn = calculate_churn_rate(df)

print(f"MAU: {mau}")
print(f"Revenue per Customer: ${rpc:.2f}")
print(f"Churn Rate: {churn:.1%}")
Requirements:
* Write 5+ reusable functions
* Each function computes one KPI
* Functions accept DataFrame parameter for reusability
* Return formatted result ($ for currency, % for rates)
Task 3: Validate Against Targets (1 mark)
# Define targets
targets = {
    'mau': {'min': 5000, 'max': 6000},
    'revenue_per_customer': {'min': 90, 'max': 110},
    'churn_rate': {'min': 0, 'max': 0.05},
    'payment_success_rate': {'min': 0.95, 'max': 1.0},
    'customer_acquisition_cost': {'min': 0, 'max': 50}
}

# Compute current KPIs
current_kpis = {
    'mau': mau,
    'revenue_per_customer': rpc,
    'churn_rate': churn,
    'payment_success_rate': 0.98,
    'customer_acquisition_cost': 35
}

# Validate
validation_report = []
for kpi_name, target_range in targets.items():
    actual = current_kpis[kpi_name]
    min_val = target_range['min']
    max_val = target_range['max']
    
    status = 'PASS' if min_val <= actual <= max_val else 'ALERT'
    validation_report.append({
        'kpi': kpi_name,
        'actual': actual,
        'target_min': min_val,
        'target_max': max_val,
        'status': status
    })

validation_df = pd.DataFrame(validation_report)
print(validation_df)

# Alert on failures
failures = validation_df[validation_df['status'] == 'ALERT']
if len(failures) > 0:
    print(f"\n⚠️ {len(failures)} KPIs out of target range - REVIEW REQUIRED")
else:
    print(f"\n✓ All {len(validation_df)} KPIs within target range")
Requirements:
* Define target ranges for each KPI
* Compare actual values against targets
* Flag any KPI outside range
* Generate validation report
Task 4: KPI Decomposition (1 mark)
Show how top-level KPIs break down:
# Total Revenue KPI decomposes into:
total_revenue = df['amount'].sum()
revenue_by_segment = df.groupby('customer_type')['amount'].sum()
revenue_by_product = df.groupby('product')['amount'].sum()

# Revenue per Customer decomposes into:
# = Total Revenue / Unique Customers
# = (Revenue from Enterprise + SMB + Startup) / (Enterprise + SMB + Startup customers)

print(f"""
KPI DECOMPOSITION: Total Monthly Revenue

Level 1 (Top-level): ${total_revenue:,.0f}

Level 2 (By Segment):
  Enterprise: ${revenue_by_segment.get('Enterprise', 0):,.0f}
  SMB: ${revenue_by_segment.get('SMB', 0):,.0f}
  Startup: ${revenue_by_segment.get('Startup', 0):,.0f}

Level 3 (By Product within Segment):
{revenue_by_product.to_string()}
""")
Requirements:
* Show at least one KPI broken down to sub-components
* Display hierarchy: top-level → segment level → product level
* Document how components sum to total
Task 5: Commit KPI Reference and Functions (1 mark)
Structure for version control:
/kpis/
  ├── kpi_reference.md          # Formal definitions
  ├── kpi_functions.py          # Python implementations
  └── kpi_validation_targets.json # Target ranges

# kpi_validation_targets.json
{
  "monthly_active_users": {"min": 5000, "max": 6000},
  "revenue_per_customer": {"min": 90, "max": 110},
  "churn_rate": {"min": 0, "max": 0.05}
}
Requirements:
* Organize KPI definitions in files
* Store functions in reusable Python module
* Store targets in JSON/YAML for easy updates
* Commit to version control
* Ensure any team member can run from kpi_functions import calculate_mau and get consistent result
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. What makes a metric a KPI - How it differs from raw numbers
2. Formula derivation - How you built one specific KPI from data
3. Target setting - How are targets determined (historical, stretch, etc.)
4. KPI reference document - How stakeholders use it
5. Schema changes - How to update KPI when data structure evolves
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.35
Root Cause Investigation Workflow

Hey Investigation Analyst!
Welcome. Anomalies are detected. Now comes investigation: tracing problems back to root causes. Revenue drops 50%. Is it product issue? Competitor action? Seasonal decline? Data error? You must investigate systematically, isolate problem to time period and segment, identify correlated patterns, and generate a hypothesis supported by evidence. Not guessing. Not blaming. Investigating.
Every business that responded to an anomaly with wrong action, that optimized the wrong thing, that made a problem worse by fixing the symptom instead of the cause had the same root: they skipped investigation and jumped to action. This lesson teaches you root cause analysis. You will filter systematically, identify patterns, test hypotheses, and document findings.
The Real Scenario
THE PROBLEM
Revenue drops. Someone says "competitors are winning". Second person says "our product broke". Third says "seasonal decline". Nobody investigates. Panic drives decision to cut prices deeply. Revenue falls further. Root cause was actually: payment processing company had an outage that lasted 2 hours. Cutting prices made nothing worse but hurt margins. Actual fix: switch payment provider. Lack of investigation led to wrong action.
THE SOLUTION
Investigate systematically. When did drop start? Only on Jan 15 11:00 UTC. Which customers affected? All with payment method linked to that processor. What correlates? Processor status page shows outage. Root cause: external dependency failure. Action: redundant payment processor. Now you fixed actual problem.
Investigation Framework
From Observation to Root Cause
1. Narrow Time
When exactly did the anomaly start and end?
Jan 15 11:00-13:00 UTC
2. Narrow Segment
Which customers/products affected?
All credit card transactions failed. Debit worked. Crypto worked.
3. Find Pattern
What correlates with the anomaly?
Failures correlate with time window. Failures correlate with payment method. No correlation with product.
4. Hypothesis
What most likely caused this?
Payment processor (Stripe) outage affecting credit cards
You just learned the investigation framework. Now implement analysis in code.
Implementing Root Cause Analysis
Systematic Investigation in Code
Step 1: Isolate Time Window
# Overall metric
df['success_rate'] = (df['status'] == 'completed').astype(int)
daily_success = df.groupby(df['timestamp'].dt.date)['success_rate'].mean()

# Find anomaly
anomaly_date = daily_success[daily_success < 0.5].index[0]
print(f"Anomaly on: {anomaly_date}")

# Zoom into that day
anomaly_day = df[df['timestamp'].dt.date == anomaly_date]
hourly_success = anomaly_day.groupby(anomaly_day['timestamp'].dt.hour)['success_rate'].mean()
print(hourly_success)  # Hour 11-13 show 0% success
Step 2: Segment Analysis
# Check which payment methods failed
during_anomaly = df[(df['timestamp'].dt.date == anomaly_date) & 
                    (df['timestamp'].dt.hour.isin([11, 12, 13]))]

success_by_payment = during_anomaly.groupby('payment_method')['success_rate'].mean()
print(success_by_payment)
# credit_card: 0%, debit: 100%, crypto: 100%
Step 3: Pattern and Hypothesis
print("""
INVESTIGATION FINDINGS:

Observation: Revenue dropped 50% on Jan 15

Narrowed Time: 11:00-13:00 UTC (100% failure rate during window)
Narrowed Segment: Credit card transactions (debit/crypto unaffected)

Pattern: Failure correlates with:
  - Time window 11:00-13:00 UTC
  - Payment method = credit_card
  - Not correlated with product, customer_type, or region

Root Cause Hypothesis: 
  Stripe (credit card processor) experienced an outage during this 2-hour window
  affecting all credit card transactions globally

Supporting Evidence:
  - Failure rate 100% for credit cards during window, 0% before/after
  - No other variables correlate
  - Debit/crypto unaffected (different processors)
  - Timing aligns with reported Stripe incidents

Recommended Action:
  Add redundant payment processor (Adyen) for credit cards
  Implement automatic failover to prevent future revenue loss
""")
You just learned systematic root cause investigation. Now you can respond to problems with evidence-based decisions.
Root Cause Investigation Workflow


00h 59m 53s

Revenue drops 50%. Product team says "bug". Sales says "competitors". Marketing says "seasonal". Instead of guessing, systematically investigate: When exactly? Which customers? What correlates? Until you know the actual cause, any fix is a guess that might make things worse.
Task 1: Isolate Time Window (1 mark)
# When did it happen?
df['success_rate'] = (df['status'] == 'success').astype(int)
daily_success = df.groupby(df['timestamp'].dt.date)['success_rate'].mean()

# Find drop
threshold = daily_success.mean() - daily_success.std()
anomaly_dates = daily_success[daily_success < threshold].index

print(f"Anomalies detected on: {anomaly_dates.tolist()}")

# Zoom into problem day
problem_day = anomaly_dates[0]
hourly_data = df[df['timestamp'].dt.date == problem_day].groupby(df['timestamp'].dt.hour)['success_rate'].mean()

print(f"\nHourly breakdown on {problem_day}:")
print(hourly_data)

# Identify exact hour
problem_hour = hourly_data.idxmin()
print(f"Worst hour: {problem_hour}:00 (success rate: {hourly_data[problem_hour]:.1%})")
Requirements:
* Identify specific date anomaly occurred
* Zoom into hours on that date
* Find exact time window of problem
* Show before/after metrics for the hour
Task 2: Segment Analysis (1 mark)
Which customers/products affected?
# Analyze which segments had issues
problem_window = df[(df['timestamp'].dt.date == problem_day) & 
                    (df['timestamp'].dt.hour == problem_hour)]

# By customer type
by_customer_type = problem_window.groupby('customer_type')['success_rate'].agg(['mean', 'count'])
print("By Customer Type:")
print(by_customer_type)

# By payment method
by_payment = problem_window.groupby('payment_method')['success_rate'].agg(['mean', 'count'])
print("\nBy Payment Method:")
print(by_payment)

# By geography
by_region = problem_window.groupby('region')['success_rate'].agg(['mean', 'count'])
print("\nBy Region:")
print(by_region)

# Identify pattern
print("\n🔍 PATTERN DETECTED:")
affected_segment = by_payment[by_payment['mean'] < 0.5].index[0]
print(f"Failures concentrated in: {affected_segment}")
Requirements:
* Break down failures by customer type, payment method, region
* Identify which segment was affected
* Show both failure rate AND affected count
* Find the correlation pattern
Task 3: Correlation Analysis (1 mark)
What correlates with the failures?
# Check for correlation with external events
df['is_problem_period'] = ((df['timestamp'].dt.date == problem_day) & 
                           (df['timestamp'].dt.hour == problem_hour)).astype(int)

# Correlations with failure
correlations = {}
for col in ['payment_method', 'customer_type', 'region', 'device_type']:
    # For categorical, use chi-square or contingency analysis
    crosstab = pd.crosstab(df[col], df['is_problem_period'], margins=True)
    print(f"\n{col}:")
    print(crosstab)

# Check if problem_method is mentioned in error logs
error_correlation = df[df['is_problem_period'] == 1]['error_message'].value_counts().head(10)
print("\nMost common errors during problem period:")
print(error_correlation)

# Find dominant error
top_error = error_correlation.index[0]
error_pct = error_correlation.iloc[0] / len(df[df['is_problem_period'] == 1])
print(f"\nTop error '{top_error}' occurred in {error_pct:.1%} of failures")
Requirements:
* Analyze correlation patterns (crosstabs)
* Review error logs from problem period
* Identify if specific error dominates
* Connect pattern to root cause hypothesis
Task 4: Documentation and Hypothesis (1 mark)
investigation_report = f"""
═══════════════════════════════════════════════════════════════════
ROOT CAUSE INVESTIGATION REPORT

OBSERVATION:
- Revenue dropped 50% on {problem_day}
- Timeline: {problem_hour}:00-{problem_hour+1}:00 UTC (60 minute window)
- Scope: Enterprise and SMB customers (Startup unaffected)

ANALYSIS:
- Payment failures: Credit card (100% failure) vs Debit (0%)
- Error logs: "Stripe API timeout" in 95% of failures
- External check: Stripe status page shows outage {problem_hour}:15-{problem_hour}:45

HYPOTHESIS (Confidence: HIGH):
Stripe (credit card processor) experienced a 30-minute outage affecting all credit card transactions globally. Other payment methods (debit, crypto) unaffected. Outage window matches Stripe public status report.

ROOT CAUSE: External payment processor failure, not product bug

RECOMMENDED ACTIONS:
1. Add redundant payment processor (Adyen) for credit cards
2. Implement automatic failover in < 30 seconds
3. Monitor payment processor health with automated alerts
4. Reduce impact from 50% revenue loss to < 5% with redundancy

ESTIMATED IMPACT:
- Outage frequency: ~1x per year (based on Stripe SLA)
- Current impact: ~$500k revenue loss per outage
- With redundancy: ~$25k revenue loss (5% leakage during failover)
- Savings: ~$475k per year
"""

print(investigation_report)

# Save report
with open('investigation_report.txt', 'w') as f:
    f.write(investigation_report)
Requirements:
* Document observation (what happened, when, to whom)
* Show analysis (patterns found)
* State hypothesis with confidence level
* Provide evidence supporting hypothesis
* Recommend actionable fix
Task 5: Validation of Hypothesis (1 mark)
# Validate hypothesis against external data
external_events = {
    f'{problem_day} {problem_hour}:15': 'Stripe API timeout reported',
    f'{problem_day} {problem_hour}:45': 'Stripe service restored'
}

our_data = {
    f'{problem_day} {problem_hour}:15': f'Credit card failures begin',
    f'{problem_day} {problem_hour}:45': f'Credit card success rate recovers'
}

validation = """
HYPOTHESIS VALIDATION:

Timeline Alignment:
Stripe outage 14:15-14:45 UTC  ✓ Matches our failure window
Our failures 14:15-14:45 UTC   ✓ Exact match

Segment Alignment:
Stripe handles: Credit cards    ✓ Match our affected segment
Not affected: Debit (other processor)  ✓ Matches our data

Competitor Impact:
If all processors down:         ✗ Would see competitor issues
If only Stripe:                 ✓ Only credit card users affected

CONCLUSION: ROOT CAUSE CONFIRMED
Action: Implement payment processor redundancy
"""

print(validation)
Requirements:
* Validate hypothesis against external evidence
* Show timeline alignment
* Document supporting evidence
* Provide clear conclusion
* Confirm (or reject) initial hypothesis
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Root cause investigation definition - What it produces
2. Investigation structure - What was checked first and why
3. Filtering dimensions used - How they isolated the issue
4. Pattern identified - Why it qualifies as root cause
5. Correlation vs causation - How to distinguish in analysis
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.36
Anomaly Detection & Risk Identification

Hey Anomaly Monitor!
Welcome. KPIs are defined. Now comes detecting when something goes wrong: unusual spikes (4x normal revenue - suspicious), drops (revenue falls 50% - investigate), fraud signals (impossible user behaviour). You must monitor KPIs continuously, flag anomalies statistically, investigate root causes, and trigger alerts so business responds immediately when something breaks.
Every business that got surprised by catastrophic failure without warning, that did not notice fraud until damage was done, that missed operational issues for days had the same root: they did not continuously monitor for anomalies. This lesson teaches you anomaly detection. You will flag unusual values, implement threshold-based alerts, and create monitoring dashboards.
The Real Scenario
THE PROBLEM
A payment processing error causes all transactions to fail silently for 2 hours. Revenue drops from0. Nobody notices until a customer complains.50k. Cost to detect it immediately with automated monitoring: negligible. Systems fail silently. Humans do not notice until users are affected.
THE SOLUTION
Compute rolling statistics hourly. Flag if revenue drops below 2 standard deviations. Alert immediately. Alert would have triggered within 15 minutes of payment failure. Investigation would find the issue. Revenue loss prevented. Similarly, fraud accounts flagged if signup rate 10x normal. Monitoring catches problems before impact multiplies.
Anomaly Detection Methods
Threshold-Based vs Statistical Detection
THRESHOLD
Alert if revenue < $5000. Simple. Tuned for your business. Works when normal range is known.
STATISTICAL
Alert if value deviates >2 std dev from rolling mean. Adaptive. Works when normal varies.
You just learned two anomaly detection approaches. Now implement monitoring.
Implementing Anomaly Detection
Threshold Alerts and Statistical Monitoring
Threshold-Based Alerts
# Define thresholds
alert_rules = {
    'daily_revenue': {'min': 5000, 'max': 50000},
    'transaction_count': {'min': 100, 'max': 10000},
    'signup_rate': {'min': 10, 'max': 500}
}

def check_thresholds(metrics, rules):
    """Alert if metrics outside thresholds."""
    alerts = []
    for metric_name, rule in rules.items():
        value = metrics[metric_name]
        if value < rule['min']:
            alerts.append(f"⚠️ {metric_name} BELOW MIN: {value} < {rule['min']}")
        elif value > rule['max']:
            alerts.append(f"⚠️ {metric_name} ABOVE MAX: {value} > {rule['max']}")
    
    return alerts

# Check today
today_metrics = {'daily_revenue': 2500, 'transaction_count': 50, 'signup_rate': 5}
alerts = check_thresholds(today_metrics, alert_rules)
for alert in alerts:
    print(alert)
Statistical Z-Score Monitoring
import numpy as np

def detect_anomalies_zscore(series, threshold=2):
    """Flag values beyond N standard deviations from mean."""
    mean = series.mean()
    std = series.std()
    z_scores = np.abs((series - mean) / std)
    anomalies = series[z_scores > threshold]
    return anomalies

# Monitor last 30 days
daily_revenue = df.groupby('date')['amount'].sum().tail(30)
anomalies = detect_anomalies_zscore(daily_revenue, threshold=2)

if len(anomalies) > 0:
    print(f"Detected {len(anomalies)} anomalies:")
    for date, value in anomalies.items():
        print(f"  {date}: ${value:.0f}")
Flag and Store Anomalies
# Record all anomalies for investigation
anomalies_log = [{
    'timestamp': date,
    'metric': 'daily_revenue',
    'value': value,
    'expected_range': f"{mean-2*std:.0f}-{mean+2*std:.0f}",
    'severity': 'high' if abs(value - mean) > 3*std else 'medium'
} for date, value in anomalies.items()]

pd.DataFrame(anomalies_log).to_csv('anomalies.csv')
You just learned to detect and monitor anomalies. Early warning system is now in place.

Anomaly Detection & Risk Identification


00h 59m 54s

Daily revenue averages $10,000. But on Tuesday it drops to $2,000. Is this a data error? A system failure? A real business problem? You need automated monitoring that flags unusual values, categorizes severity, and triggers investigation without overwhelming you with false positives.
Task 1: Threshold-Based Anomaly Detection (1 mark)
Define business rules for alerting:
alert_rules = {
    'daily_revenue': {'min': 5000, 'max': 50000},
    'transaction_count': {'min': 100, 'max': 10000},
    'signup_rate': {'min': 10, 'max': 500}
}

def check_thresholds(metrics, rules):
    """Alert if metrics outside business thresholds."""
    alerts = []
    for metric_name, rule in rules.items():
        value = metrics[metric_name]
        if value < rule['min']:
            alerts.append({
                'metric': metric_name,
                'value': value,
                'threshold': rule['min'],
                'direction': 'BELOW_MIN',
                'severity': 'HIGH'
            })
        elif value > rule['max']:
            alerts.append({
                'metric': metric_name,
                'value': value,
                'threshold': rule['max'],
                'direction': 'ABOVE_MAX',
                'severity': 'MEDIUM'
            })
    return alerts

# Test
today_metrics = {'daily_revenue': 2500, 'transaction_count': 50, 'signup_rate': 5}
alerts = check_thresholds(today_metrics, alert_rules)
for alert in alerts:
    print(f"⚠️ {alert['metric']} {alert['direction']}: {alert['value']}")
Requirements:
* Define min/max thresholds for 3+ business metrics
* Check current values against thresholds
* Generate alerts with metric name, value, threshold
Task 2: Statistical Anomaly Detection with Z-Score (1 mark)
Detect values beyond N standard deviations:
import numpy as np

def detect_anomalies_zscore(series, threshold=2):
    """Flag values > N std dev from mean."""
    mean = series.mean()
    std = series.std()
    z_scores = np.abs((series - mean) / std)
    anomalies = series[z_scores > threshold]
    return anomalies, z_scores

# Monitor last 30 days
daily_revenue = df.groupby('date')['amount'].sum().tail(30)
anomalies, z_scores = detect_anomalies_zscore(daily_revenue, threshold=2)

print(f"Detected {len(anomalies)} anomalies out of {len(daily_revenue)} days")
for date, value in anomalies.items():
    print(f"  {date}: ${value:.0f} (z-score: {z_scores[date]:.2f})")
Requirements:
* Compute rolling statistics (mean, std)
* Identify values > 2 standard deviations
* Display z-score for each anomaly
* Apply to 30-day lookback window
Task 3: Severity Classification (1 mark)
Categorize anomalies by impact:
def classify_severity(value, mean, std):
    """Classify anomaly severity based on deviation."""
    z_score = abs((value - mean) / std)
    
    if z_score > 3:
        return 'CRITICAL'
    elif z_score > 2:
        return 'HIGH'
    elif z_score > 1.5:
        return 'MEDIUM'
    else:
        return 'LOW'

# Classify all anomalies
anomaly_severity = []
for date, value in anomalies.items():
    severity = classify_severity(value, daily_revenue.mean(), daily_revenue.std())
    anomaly_severity.append({
        'date': date,
        'value': value,
        'z_score': z_scores[date],
        'severity': severity
    })

severity_df = pd.DataFrame(anomaly_severity)
print(severity_df)

# Alert only on HIGH+ severity
critical = severity_df[severity_df['severity'].isin(['CRITICAL', 'HIGH'])]
print(f"\n⚠️ {len(critical)} critical anomalies require investigation")
Requirements:
* Classify anomalies into severity levels (CRITICAL, HIGH, MEDIUM, LOW)
* Use z-score thresholds to define levels
* Filter to show only high-severity anomalies
Task 4: Anomaly Logging and Audit Trail (1 mark)
Store all anomalies for investigation:
# Log anomalies
anomaly_log = []
for date, value in anomalies.items():
    severity = classify_severity(value, daily_revenue.mean(), daily_revenue.std())
    anomaly_log.append({
        'timestamp': pd.Timestamp.now(),
        'anomaly_date': date,
        'metric': 'daily_revenue',
        'value': value,
        'expected_range': f"{daily_revenue.mean()-2*daily_revenue.std():.0f}-{daily_revenue.mean()+2*daily_revenue.std():.0f}",
        'z_score': z_scores[date],
        'severity': severity,
        'status': 'OPEN'  # OPEN, INVESTIGATED, RESOLVED
    })

# Save to file
anomalies_df = pd.DataFrame(anomaly_log)
anomalies_df.to_csv('anomalies_log.csv', index=False)
print(f"Logged {len(anomalies_df)} anomalies")
Requirements:
* Create audit log with timestamp, metric, value, severity
* Save to persistent file for historical tracking
* Include investigation status (OPEN, INVESTIGATED, RESOLVED)
Task 5: Visualization with Flagged Points (1 mark)
Plot time-series with anomalies highlighted:
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(14, 6))

# Plot raw data
ax.plot(daily_revenue.index, daily_revenue.values, marker='o', label='Daily Revenue', linewidth=2)

# Plot rolling average
rolling_avg = daily_revenue.rolling(window=7).mean()
ax.plot(rolling_avg.index, rolling_avg.values, label='7-day MA', color='green', linewidth=2)

# Highlight anomalies
for date, value in anomalies.items():
    ax.scatter(date, value, color='red', s=200, marker='X', zorder=5)
    ax.annotate('ANOMALY', (date, value), xytext=(0, 10), 
                textcoords='offset points', ha='center', fontweight='bold')

# Shade expected range
mean = daily_revenue.mean()
std = daily_revenue.std()
ax.fill_between(daily_revenue.index, mean-2*std, mean+2*std, alpha=0.2, color='blue', label='Expected Range ±2σ')

ax.set_xlabel('Date')
ax.set_ylabel('Revenue ($)')
ax.set_title('Daily Revenue with Anomalies Flagged')
ax.legend()
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('anomaly_detection.png', dpi=150)
plt.show()
Requirements:
* Plot raw daily values over time
* Show rolling average to reveal trend
* Shade expected range (mean ± 2σ)
* Mark anomalies with distinct visual (red X)
* Save high-quality visualization
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. What is an anomaly - Business definition
2. Threshold vs statistical approach - When to use each
3. Z-score computation - What qualifies as anomaly
4. Flagged anomaly walkthrough - Investigation steps
5. False positive reduction - How to tune sensitivity
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.37
SQL Environment & Database Integration

Hey Database Engineer!
Welcome. Investigation complete. Now comes scaling: moving from local notebooks to databases. Cleaned data should live in queryable tables. SQL queries compute metrics from source truth. Python integrates with databases for production workflows. You must connect Python to SQL, load cleaned data as tables, validate schema, execute queries, return results to DataFrames.
Every analyst who kept analyses in notebooks, who could not reproduce results across machines, who could not share cleaned data safely had the same problem: data lived locally, not in an accessible database. This lesson teaches you database integration. You will setup SQLite or PostgreSQL, load data via Pandas, query from Python, and build repeatable workflows.
The Real Scenario
THE PROBLEM
Analyst A cleans data in notebook, produces cleaned CSV. Analyst B downloads CSV, runs analysis locally, gets different results. Who is right? Nobody knows. Months later someone asks for historical cleaned data. Notebooks gone. CSVs on various people's computers. Different versions. No audit trail. Stakeholders cannot trust the data. Reproducibility is impossible.
THE SOLUTION
Cleaned data loads to SQL table via Python. One source of truth. Everyone queries same database. Reproducible. Auditable. Schema version controlled. Cleaning scripts version controlled. Someone asks for historical data? Run the script against historical raw data, load to database, query. Perfect reproducibility.
Database Fundamentals
SQLite vs PostgreSQL
SQLITE
File-based. Zero setup. Single file. Good for < 1GB. Learning tool. Not for production at scale.
POSTGRESQL
Server-based. Complex setup. Multi-user. Scalable. For production. Industry standard.
You just learned database options. Now connect Python to SQL.
Connecting Python to Databases
SQLAlchemy and Pandas Integration
Setup SQLite Connection
from sqlalchemy import create_engine
import pandas as pd

# SQLite: create file-based database
engine = create_engine('sqlite:///analytics.db')

# PostgreSQL: connect to server
# engine = create_engine('postgresql://user:password@localhost:5432/analytics')
Load Cleaned Data as Table
# Write DataFrame to database
df_clean.to_sql('customers_cleaned', engine, if_exists='replace', index=False)

# Verify table created
print(engine.table_names())  # ['customers_cleaned']
Query and Return to DataFrame
# Query from Python
query = "SELECT * FROM customers_cleaned WHERE customer_type = 'Enterprise'"
result = pd.read_sql(query, engine)

print(result.head())
Validate Schema
from sqlalchemy import inspect

# Get table info
inspector = inspect(engine)
columns = inspector.get_columns('customers_cleaned')

for col in columns:
    print(f"{col['name']}: {col['type']}")
You just learned to connect Python to SQL databases. Now all analysis is reproducible and shareable.
SQL Environment & Database Integration


00h 59m 56s

Cleaned data lives in notebooks. Different versions on different computers. CSVs shared via email. No central truth. Setup a database, load cleaned data, query from Python, make it the single source of truth that all analyses use.
Task 1: Setup Database Connection (1 mark)
from sqlalchemy import create_engine
import pandas as pd

# SQLite (file-based, zero setup)
engine = create_engine('sqlite:///analytics.db')

# OR PostgreSQL (server-based, for production)
# engine = create_engine('postgresql://username:password@localhost:5432/analytics')

# Test connection
with engine.connect() as conn:
    print("✓ Database connection successful")
Requirements:
* Setup SQLite OR PostgreSQL
* Create engine with SQLAlchemy
* Test connection works
* Document connection string (without hardcoded credentials)
Task 2: Load Cleaned DataFrame as Table (1 mark)
# Load cleaned data to database
df_clean.to_sql('customers_cleaned', engine, if_exists='replace', index=False)

# Verify table created
print(engine.table_names())

# Check row count
count = pd.read_sql("SELECT COUNT(*) as row_count FROM customers_cleaned", engine)
print(f"Rows loaded: {count.iloc[0]['row_count']}")
Requirements:
* Load DataFrame to database table
* Verify table exists
* Confirm row count
* Set if_exists='replace' for first load
Task 3: Validate Schema (1 mark)
from sqlalchemy import inspect

# Inspect table schema
inspector = inspect(engine)
columns = inspector.get_columns('customers_cleaned')

print("TABLE SCHEMA:")
for col in columns:
    print(f"  {col['name']:20} {str(col['type']):15} {'NOT NULL' if col['nullable']==False else ''}")

# Verify column types
print("\nDATATYPE VALIDATION:")
expected_types = {
    'customer_id': 'INTEGER',
    'email': 'VARCHAR',
    'signup_date': 'DATE'
}

for col_name, expected_type in expected_types.items():
    actual = [c['type'] for c in columns if c['name'] == col_name][0]
    status = '✓' if expected_type in str(actual) else '✗'
    print(f"{status} {col_name}: {actual}")
Requirements:
* Inspect table schema using SQLAlchemy
* Print all columns and types
* Validate expected types
* Check for null constraints
Task 4: Query and Return Results (1 mark)
# Query from Python
query = "SELECT * FROM customers_cleaned WHERE customer_type = 'Enterprise'"
results = pd.read_sql(query, engine)

print(f"Retrieved {len(results)} rows")
print(results.head())

# More complex query
query_agg = """
SELECT 
    customer_type,
    COUNT(*) as count,
    AVG(lifetime_value) as avg_ltv
FROM customers_cleaned
GROUP BY customer_type
ORDER BY avg_ltv DESC
"""

summary = pd.read_sql(query_agg, engine)
print("\nSummary by segment:")
print(summary)
Requirements:
* Execute SELECT query from Python
* Return results to DataFrame
* Test with simple query
* Test with aggregation query
Task 5: Make Loading Repeatable (1 mark)
def load_cleaned_data_to_database(df, table_name, database_path='analytics.db'):
    """Load cleaned DataFrame to database - repeatable function."""
    engine = create_engine(f'sqlite:///{database_path}')
    
    # Load
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    # Validate
    count = pd.read_sql(f"SELECT COUNT(*) as ct FROM {table_name}", engine)
    rows_loaded = count.iloc[0]['ct']
    
    print(f"✓ Loaded {rows_loaded} rows to {table_name}")
    return engine

# Usage
engine = load_cleaned_data_to_database(df_clean, 'customers_cleaned')

# Now anyone can query
results = pd.read_sql("SELECT * FROM customers_cleaned LIMIT 10", engine)
Requirements:
* Wrap loading in reusable function
* Add validation checks
* Return engine for reuse
* Document function parameters
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. SQLite vs PostgreSQL - When each is appropriate
2. SQLAlchemy purpose - Database abstraction layer
3. pd.read_sql and pd.to_sql - Parameters and behavior
4. Schema validation - What to check, why it matters
5. Schema evolution - Handling changes to data structure
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public

2.38
SQL Business Metrics Query Design

Hey Metric SQL Writer!
Welcome. Database connection working. Now comes business metrics in SQL: writing queries that compute customer lifetime value, monthly active users, retention cohorts, revenue trends. Metrics live in SQL, not in notebooks. Once written, they are reusable forever. Every analyst queries the same metric. Consistency achieved.
Every team that recomputed the same metrics over and over in different notebooks, that got different numbers from different people, that had no central truth for KPIs had the same problem: metrics were never written once in SQL and shared. This lesson teaches you metric computation in SQL. You will write queries for 4+ business metrics, store them in files, and use them across projects.
The Real Scenario
THE PROBLEM
Revenue metric is computed 5 different ways by 5 different people. Accounting says1.1M. Sales says $1.3M. Board meeting, three different "revenue" numbers presented. Nobody knows which is correct. Days wasted reconciling. Team rebuilds "Monthly Active Users" metric every week. Each time slightly different based on how the person decided to filter. Metrics should be computed once, stored, and reused.
THE SOLUTION
Define Monthly Revenue in SQL once. Store in queries/revenue.sql. All teams query that. One number. One truth. To update definition, change the file once, all downstream uses update. Reusable. Auditable. Correct.
Metric Computation in SQL
Building Business Metrics
Active Users Metric
-- queries/active_users.sql
-- Monthly Active Users: distinct customers with transaction in last 30 days
SELECT 
    DATE_TRUNC('month', transaction_date)::DATE as month,
    COUNT(DISTINCT customer_id) as active_users
FROM transactions
WHERE transaction_date >= DATE_TRUNC('month', NOW()) - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month DESC;
Revenue by Segment
-- queries/revenue_by_segment.sql
SELECT 
    c.customer_type,
    DATE_TRUNC('month', t.transaction_date)::DATE as month,
    SUM(t.amount) as monthly_revenue,
    COUNT(DISTINCT t.customer_id) as unique_customers,
    SUM(t.amount) / COUNT(DISTINCT t.customer_id) as revenue_per_customer
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= NOW() - INTERVAL '12 months'
GROUP BY c.customer_type, DATE_TRUNC('month', t.transaction_date)
ORDER BY month DESC, monthly_revenue DESC;
Conversion Rate with CASE
-- queries/conversion_funnel.sql
SELECT 
    DATE_TRUNC('day', created_at)::DATE as signup_date,
    COUNT(*) as signups,
    COUNT(CASE WHEN email_verified_at IS NOT NULL THEN 1 END) as verified,
    COUNT(CASE WHEN first_transaction_at IS NOT NULL THEN 1 END) as first_purchase,
    ROUND(100.0 * COUNT(CASE WHEN first_transaction_at IS NOT NULL THEN 1 END) / COUNT(*), 1) as conversion_pct
FROM users
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY signup_date DESC;
Call Metrics from Python
# Load and execute query
with open('queries/active_users.sql', 'r') as f:
    query = f.read()

active_users = pd.read_sql(query, engine)
print(active_users)

# All teams use same query. One number. One truth.
You just learned to write business metrics in SQL once and reuse everywhere. Metric consistency is achieved.
SQL Business Metrics Query Design


00h 59m 55s

Five teams compute "Monthly Revenue" five different ways. Finance counts invoiced. Sales counts paid. Product counts transactions. Accounting sums line items. Nobody agrees. Write SQL once, store, everyone uses it. One number. One truth.
Task 1: Active Users Metric (1 mark)
-- queries/monthly_active_users.sql
SELECT 
    DATE_TRUNC('month', transaction_date)::DATE as month,
    COUNT(DISTINCT customer_id) as active_users,
    COUNT(DISTINCT customer_id) FILTER (WHERE customer_type='Enterprise') as enterprise_users,
    COUNT(DISTINCT customer_id) FILTER (WHERE customer_type='SMB') as smb_users
FROM transactions
WHERE transaction_date >= DATE_TRUNC('month', NOW()) - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month DESC;
Requirements:
* Write reusable SQL query
* Include conditional aggregation (FILTER clause)
* Return monthly active users and segment breakdown
Task 2: Revenue by Segment (1 mark)
-- queries/revenue_by_segment.sql
SELECT 
    c.customer_type,
    DATE_TRUNC('month', t.transaction_date)::DATE as month,
    COUNT(DISTINCT t.order_id) as order_count,
    SUM(t.amount) as monthly_revenue,
    ROUND(AVG(t.amount), 2) as avg_order_value,
    COUNT(DISTINCT t.customer_id) as unique_customers,
    ROUND(SUM(t.amount) / COUNT(DISTINCT t.customer_id), 2) as revenue_per_customer
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= DATE_TRUNC('month', NOW()) - INTERVAL '12 months'
GROUP BY c.customer_type, DATE_TRUNC('month', t.transaction_date)
ORDER BY month DESC, monthly_revenue DESC;
Requirements:
* Join customers and transactions
* Compute 4+ metrics per segment
* Use meaningful aliases
* Format with correct precision
Task 3: Funnel Conversion (1 mark)
-- queries/conversion_funnel.sql
SELECT 
    DATE_TRUNC('day', u.created_at)::DATE as signup_date,
    COUNT(*) as signups,
    COUNT(*) FILTER (WHERE u.email_verified_at IS NOT NULL) as email_verified,
    COUNT(*) FILTER (WHERE u.first_purchase_at IS NOT NULL) as first_purchase,
    ROUND(100.0 * COUNT(*) FILTER (WHERE u.first_purchase_at IS NOT NULL) / COUNT(*), 1) as conversion_pct
FROM users u
WHERE u.created_at >= NOW() - INTERVAL '90 days'
GROUP BY DATE_TRUNC('day', u.created_at)
ORDER BY signup_date DESC;
Requirements:
* Use CASE WHEN or FILTER for conditional counting
* Compute conversion rate as percentage
* Return daily funnel metrics
Task 4: Call Queries from Python (1 mark)
def load_query(query_name):
    """Load SQL query from file."""
    with open(f'queries/{query_name}.sql', 'r') as f:
        return f.read()

# Load and execute
mau_query = load_query('monthly_active_users')
mau = pd.read_sql(mau_query, engine)
print("Monthly Active Users:")
print(mau)

revenue_query = load_query('revenue_by_segment')
revenue = pd.read_sql(revenue_query, engine)
print("\nRevenue by Segment:")
print(revenue)

funnel_query = load_query('conversion_funnel')
funnel = pd.read_sql(funnel_query, engine)
print("\nConversion Funnel:")
print(funnel)

# All teams use same queries -> consistent metrics
Requirements:
* Load queries from .sql files
* Execute queries from Python
* Return results to DataFrames
* All teams share same query files
Task 5: Validate Query Results (1 mark)
def validate_metrics(mau_df, revenue_df, funnel_df):
    """Validate metric computation."""
    
    # Check for nulls
    assert mau_df.isnull().sum().sum() == 0, "MAU has nulls"
    assert revenue_df.isnull().sum().sum() == 0, "Revenue has nulls"
    
    # Check value ranges
    assert (revenue_df['monthly_revenue'] > 0).all(), "Revenue <= 0"
    assert (funnel_df['conversion_pct'] >= 0).all() and (funnel_df['conversion_pct'] <= 100).all(), "Conversion out of range"
    
    # Check consistency
    for idx, row in revenue_df.iterrows():
        assert row['order_count'] > 0, "Zero orders"
        assert row['monthly_revenue'] > 0, "Zero revenue"
    
    print("✓ All metrics validated")
    return True

# Validate
validate_metrics(mau, revenue, funnel)
Requirements:
* Check for null values
* Validate value ranges
* Ensure logical consistency
* Report validation results
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. Why SQL metrics beat Python scripts - Reusability and consistency
2. CASE WHEN in aggregation - Conditional counting examples
3. Retention cohort definition - SQL for computing cohorts
4. Rolling 7-day active users - Advanced time-window aggregation
5. Adding new metrics - How to extend without breaking existing
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.39
SQL Filtering, Grouping & Aggregation

Hey SQL Filter Master!
Welcome. Metrics are defined. Now comes filtering and grouping: WHERE clauses that apply business rules, GROUP BY that slices data by dimensions, HAVING that filters aggregated results, ORDER BY that surfaces top performers. These four clauses are the foundation of operational reporting. You must master them to compute KPIs reliably.
Every analyst who could not filter data correctly, who did not understand the difference between WHERE and HAVING, who could not order results meaningfully had the same problem: they never learned these fundamental SQL clauses deeply. This lesson teaches you SQL filtering and aggregation thoroughly.
The Real Scenario
THE PROBLEM
Someone writes: "Show me revenue by customer where revenue > 1000". Do you filter before grouping or after? If before (WHERE), you exclude customers entirely if any transaction is < 1000. If after (HAVING), you count all transactions but show only customers whose total exceeds 1000. Results differ wildly. Nobody knows which is right. Questions repeat constantly: "Should I use WHERE or HAVING?" This lesson answers it definitively.
THE SOLUTION
WHERE filters before grouping. HAVING filters after. They answer different questions. Use WHERE to exclude invalid data (transaction_date in this year). Use HAVING to filter aggregated metrics (SUM(amount) > 1000). Combined properly, queries produce correct results consistently.
WHERE vs HAVING
Filtering at Different Stages
WHERE
Filters rows before grouping. Data-quality check. WHERE customer_type = 'Enterprise'. Rows not matching are never included in group.
HAVING
Filters groups after aggregation. Metric threshold. HAVING SUM(amount) > 1000. Groups not matching are excluded.
You just learned WHERE and HAVING roles. Now apply them to queries.
Filtering and Aggregation Queries
WHERE, GROUP BY, HAVING, ORDER BY
WHERE: Filter Data Before Grouping
-- Show only Enterprise customers
SELECT customer_id, SUM(amount) as total_spent
FROM transactions
WHERE customer_type = 'Enterprise'
GROUP BY customer_id
ORDER BY total_spent DESC;
HAVING: Filter Groups After Aggregation
-- Show only customers who spent more than $10,000 total
SELECT customer_id, SUM(amount) as total_spent
FROM transactions
GROUP BY customer_id
HAVING SUM(amount) > 10000
ORDER BY total_spent DESC;
WHERE + HAVING: Both Together
-- Enterprise customers who spent > $10k
SELECT customer_id, COUNT(*) as order_count, SUM(amount) as total_spent
FROM transactions
WHERE customer_type = 'Enterprise'          -- Filter data first
GROUP BY customer_id
HAVING SUM(amount) > 10000                  -- Filter groups second
ORDER BY total_spent DESC;
ORDER BY: Sort Results
-- Top 10 customers by revenue
SELECT 
    customer_id, 
    customer_type,
    SUM(amount) as total_revenue,
    COUNT(*) as order_count
FROM transactions
WHERE transaction_date >= '2024-01-01'
GROUP BY customer_id, customer_type
HAVING COUNT(*) >= 5
ORDER BY total_revenue DESC
LIMIT 10;
You just learned filtering and aggregation fundamentals. Operational reporting is now possible.
SQL Filtering, Grouping & Aggregation


00h 59m 56s

Show "Enterprise customers with >$10k annual spending" - do you filter before or after grouping? Do you use WHERE or HAVING? Write 5+ queries demonstrating correct usage, and document the pattern so everyone on the team applies filters correctly.
Task 1: WHERE Filtering (1 mark)
-- Filter data quality issues BEFORE grouping
SELECT 
    customer_id,
    SUM(amount) as annual_revenue,
    COUNT(*) as transaction_count
FROM transactions
WHERE transaction_date >= DATE '2024-01-01'  -- Date range filter
  AND amount > 0                              -- Remove refunds
  AND transaction_status = 'completed'        -- Valid transactions only
GROUP BY customer_id
ORDER BY annual_revenue DESC;
Requirements:
* Use WHERE for data quality checks
* Filter invalid/incomplete records
* Document why each condition exists
Task 2: GROUP BY and Aggregation (1 mark)
-- Group by multiple dimensions
SELECT 
    c.customer_type,
    DATE_TRUNC('month', t.transaction_date)::DATE as month,
    COUNT(DISTINCT t.customer_id) as unique_customers,
    COUNT(*) as transaction_count,
    SUM(t.amount) as monthly_revenue,
    AVG(t.amount) as avg_transaction
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= DATE '2024-01-01'  -- WHERE filters first
GROUP BY c.customer_type, DATE_TRUNC('month', t.transaction_date)
ORDER BY month DESC;
Requirements:
* GROUP BY on 2+ dimensions
* Use 3+ aggregate functions
* Show how WHERE filters before GROUP BY
Task 3: HAVING Filtering (1 mark)
-- Filter GROUPS after aggregation
SELECT 
    customer_id,
    COUNT(*) as transaction_count,
    SUM(amount) as annual_revenue
FROM transactions
WHERE transaction_date >= DATE '2024-01-01'
GROUP BY customer_id
HAVING SUM(amount) > 10000                      -- HAVING filters groups
  AND COUNT(*) >= 5                             -- Only customers with 5+ purchases
ORDER BY annual_revenue DESC;
Requirements:
* Use HAVING to filter after aggregation
* Show difference from WHERE (WHERE filters rows, HAVING filters groups)
* Document when each is appropriate
Task 4: WHERE + HAVING Combined (1 mark)
-- Real-world: filter data quality AND aggregate thresholds
SELECT 
    c.customer_type,
    COUNT(DISTINCT t.customer_id) as segment_customers,
    SUM(t.amount) as segment_revenue,
    ROUND(AVG(t.amount), 2) as avg_order_value
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= DATE '2024-01-01'      -- WHERE: valid data
  AND t.transaction_status = 'completed'           -- WHERE: quality
  AND t.amount > 0                                 -- WHERE: logical validity
GROUP BY c.customer_type
HAVING COUNT(DISTINCT t.customer_id) >= 100       -- HAVING: segment size
  AND SUM(t.amount) > 100000                       -- HAVING: business threshold
ORDER BY segment_revenue DESC;
Requirements:
* Combine WHERE and HAVING in one query
* Show WHERE filters rows, HAVING filters groups
* Document business logic for each filter
Task 5: ORDER BY Ranking (1 mark)
-- Surface top and bottom performers
SELECT 
    c.customer_type,
    c.industry,
    COUNT(DISTINCT t.customer_id) as customers,
    SUM(t.amount) as total_revenue,
    ROUND(AVG(t.amount), 2) as avg_order,
    RANK() OVER (ORDER BY SUM(t.amount) DESC) as revenue_rank
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.transaction_date >= DATE '2024-01-01'
GROUP BY c.customer_type, c.industry
HAVING COUNT(DISTINCT t.customer_id) >= 10
ORDER BY total_revenue DESC
LIMIT 20;  -- Top 20 segments
Requirements:
* Use ORDER BY to sort results
* Show top performers first
* Use RANK() for ranking
* Limit to top N results
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. WHERE vs HAVING distinction - When each applies
2. GROUP BY semantics - How it changes aggregation unit
3. HAVING filter examples - Business rule filtering on aggregates
4. Optimization consideration - WHERE before GROUP BY is faster
5. Percentage share computation - Computing % of total within groups
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.


2.40
SQL Joins & Multi-Table Analysis

Hey Multi-Table Master!
Welcome. Filtering is solid. Now comes combining data across tables: INNER JOIN keeps matched rows only, LEFT JOIN keeps all left rows plus matches, OUTER JOIN keeps everything. These joins power relational database analysis. You must join correctly, validate row counts, and detect unmatched keys. This is the final lesson: master joins and you can analyze any relational dataset.
Every analyst who misunderstood joins, whose row counts exploded from unexpected multiplicity, who had confidence in merged results that were actually corrupted had the same problem: they did not validate joins. This lesson teaches you join mastery. You will implement three join types, verify row counts, detect unmatched keys, and trace data lineage across tables.
The Real Scenario
THE PROBLEM
Join customers (1000 rows) to orders (5000 rows) to get customer order history. Result has 5500 rows. Why 5500 and not 5000? Did the join create duplicates? Are customers missing orders? Nobody validates. Analysis proceeds on unknown data quality. Results are questionable. Months later, someone points out: "One customer had 6 orders and appears 6 times in the result. Is that correct?" Nobody knows because nobody validated the join.
THE SOLUTION
Before joining: customers = 1000, orders = 5000. After LEFT JOIN: 5500 rows. The extra 500 come from customers with multiple orders. Document this. Validate: "Customers with 2+ orders create multiple result rows - expected for this join." Unmatched: 100 orders have no matching customer - investigate why. Now the join is understood and validated. Results are trustworthy.
Join Fundamentals
Three Join Types
INNER JOIN
Keep only matched rows. Result ≤ min(left, right). Customers with orders only.
LEFT JOIN
All left rows plus matches. Result ≥ left. All customers, matched with orders where they exist.
OUTER JOIN
All rows from both sides. Result > max(left, right). All customers AND all orders.
You just learned join semantics. Now validate joins properly.
Implementing and Validating Joins
Join Queries with Validation
LEFT JOIN with Row Count Validation
-- Before join
SELECT COUNT(DISTINCT customer_id) as customers FROM customers; -- 1000
SELECT COUNT(*) as orders FROM orders;                          -- 5000

-- After join
SELECT 
    c.customer_id, 
    c.customer_type,
    COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_type;

-- Result: 1000 customers (all), but total rows > 5000 due to one-to-many
Detect Unmatched Keys
-- Customers with no orders
SELECT c.customer_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Orders with no customer
SELECT o.order_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
Multi-Table Join
-- Join 3 tables
SELECT 
    c.customer_id,
    c.customer_type,
    o.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE c.customer_type = 'Enterprise';
Validate Row Counts
-- Compare row counts to understand join impact
SELECT 
    'customers' as table_name, COUNT(DISTINCT customer_id) as distinct_keys, COUNT(*) as total_rows
FROM customers
UNION ALL
SELECT 
    'orders', COUNT(DISTINCT customer_id), COUNT(*)
FROM orders
UNION ALL
SELECT 
    'joined', COUNT(DISTINCT c.customer_id), COUNT(*)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
You just learned to join tables correctly and validate results. You have completed all 30 lessons. You are now a complete data analyst and engineer.

SQL Joins & Multi-Table Analysis


00h 59m 55s

Join customers (1000) to orders (5000). Result has 5500 rows. Why? Did you create duplicates? Are there unmatched records? Validate every join: row counts before/after, unmatched key investigation, and documented decisions about what each join type means for your analysis.
Task 1: LEFT JOIN with Row Count Validation (1 mark)
-- All customers with their orders (some have multiple, some have none)
SELECT 
    c.customer_id,
    c.customer_type,
    COUNT(DISTINCT o.order_id) as order_count,
    SUM(o.order_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_type
ORDER BY total_spent DESC NULLS LAST;
Python validation:
# Before join
customers_count = len(customers)  # 1000

# After join (LEFT JOIN)
joined = pd.read_sql(query, engine)
print(f"Before: {customers_count} customers")
print(f"After: {len(joined)} rows")
print(f"Change: {len(joined) - customers_count} ({((len(joined)-customers_count)/customers_count)*100:.1f}%)")

# Expected: After >= Before (all customers kept, some appear multiple times due to multiple orders)
Requirements:
* Execute LEFT JOIN
* Compare row counts before/after
* Show multiplication factor (orders per customer)
* Document why result is larger
Task 2: Detect Unmatched Keys (1 mark)
-- Customers with NO orders
SELECT c.customer_id, c.customer_type, c.signup_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.signup_date;

-- Orders with NO matching customer (orphaned records)
SELECT o.order_id, o.customer_id, o.order_date
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
ORDER BY o.order_date;
Python analysis:
# Find unmatched
no_orders = pd.read_sql("SELECT ... WHERE o.order_id IS NULL", engine)
orphaned = pd.read_sql("SELECT ... WHERE c.customer_id IS NULL", engine)

print(f"Customers without orders: {len(no_orders)} ({(len(no_orders)/customers_count)*100:.1f}%)")
print(f"Orphaned orders: {len(orphaned)}")

# Decision
if len(orphaned) > 0:
    print("⚠️ Orphaned records found - investigate customer_id mismatch")
Requirements:
* Use LEFT JOIN with IS NULL to find unmatched
* Show customers with no orders
* Show orders with no matching customer
* Analyze percentage of unmatched
Task 3: Compare Join Types (1 mark)
-- INNER JOIN (matched only)
SELECT c.customer_id, o.order_id, o.order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN (all customers)
SELECT c.customer_id, o.order_id, o.order_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- FULL OUTER JOIN (all records)
SELECT c.customer_id, o.order_id, o.order_amount
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
Python comparison:
inner = pd.read_sql("SELECT ... INNER JOIN", engine)
left = pd.read_sql("SELECT ... LEFT JOIN", engine)
full = pd.read_sql("SELECT ... FULL OUTER JOIN", engine)

print(f"INNER: {len(inner)} rows (only matched)")
print(f"LEFT:  {len(left)} rows (all left, matched right)")
print(f"FULL:  {len(full)} rows (all from both)")

# LEFT and FULL should be >= INNER
assert len(left) >= len(inner)
assert len(full) >= max(len(left), 1000)  # All customers + orphaned orders
Requirements:
* Show all 3 join types
* Compare row counts
* Explain what each returns
* Validate relationships
Task 4: Multi-Table Join (1 mark)
-- Join 3+ tables
SELECT 
    c.customer_id,
    c.customer_type,
    o.order_id,
    o.order_date,
    oi.product_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) as line_total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE c.customer_type = 'Enterprise'
ORDER BY o.order_date DESC;
Python usage:
result = pd.read_sql(query, engine)

# Validate no unexpected duplication
product_total = result.groupby('product_id')['line_total'].sum()
expected_total = pd.read_sql(
    "SELECT SUM(quantity * unit_price) FROM order_items", 
    engine
).iloc[0,0]

assert abs(product_total.sum() - expected_total) < 0.01, "Duplication in join!"
print("✓ Multi-table join validated - no duplication")
Requirements:
* Join 3+ tables
* Use LEFT JOINs for optional relationships
* Validate no unexpected row multiplication
* Show complete data lineage
Task 5: Document Join Decisions (1 mark)
join_documentation = """
JOIN STRATEGY DOCUMENTATION

Table: customers (1000 rows, PK: customer_id)
Table: orders (5000 rows, FK: customer_id)
Table: order_items (8000 rows, FK: order_id)
Table: products (500 rows, PK: product_id)

Decision 1: customers LEFT JOIN orders
- Purpose: Get all customers with their order history
- Row count change: 1000 → 5000 (one row per order)
- Unmatched: 100 customers have no orders (retained due to LEFT)
- Business use: Customer lifetime value, segmentation

Decision 2: orders LEFT JOIN order_items  
- Purpose: Detailed line-item view
- Row count change: 5000 → 8000 (some orders have multiple items)
- Unmatched: None (all orders should have items)
- Business use: Product revenue, inventory analysis

Decision 3: Full 3-table join
- Purpose: Complete order context with products
- Row count: 5000 → 8000 (base orders multiplied by items)
- Risk: Be careful not to double-count in aggregations
- Solution: Aggregate at order level, not at result set level

Validation: Row counts match expected, no orphaned records, no duplication
"""

print(join_documentation)
Requirements:
* Document why each join exists
* Explain row count changes
* Note unmatched key counts
* Document business use case
* Validate correctness
Submission
Submit two things together. Missing either one makes the submission incomplete.
1. GitHub PR link
2. Video
1. INNER/LEFT/OUTER JOIN difference - Concrete example
2. Row count validation importance - Why it prevents silent errors
3. Unmatched keys investigation - How to find orphaned records
4. Multi-key joining - Handling non-unique keys
5. Join order impact - Why the order matters for row counts
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.41
SQL Window Functions & Ranking Systems

Hey Dashboard Architect!
Welcome. SQL queries are optimized. Data is clean. Now comes the final transformation: taking insights and presenting them to humans in forms they understand. A well-designed dashboard answers business questions instantly. A poorly designed one drowns users in data. You must understand dashboard architecture - what data belongs together, how to organize information hierarchically, what metrics matter most, how to make exploration intuitive without overwhelming viewers.
Every dashboard that confused users, that had charts nobody used, that required 10 clicks to answer one question had the same root problem: it was designed by someone who understood the data but not how humans actually make decisions with information. This lesson teaches you dashboard thinking. You will learn how to organize metrics hierarchically, understand the difference between summary and detail views, design for information flow, and create dashboards that answer business questions before they are asked.
The Real Scenario
THE PROBLEM
A dashboard is built showing 50 charts on one page. All available. Nothing prioritized. A business user logs in, sees overwhelming chaos, gets lost scrolling, cannot find the one metric they care about. They stop using it and go back to emails and spreadsheets. The dashboard fails not because the data is wrong but because it violates how human attention works. Humans cannot process 50 things at once. They scan in order of importance. If important things are buried, they miss them.
THE SOLUTION
Design hierarchically. Top of page: 5 KPI cards answering "are we on track?" Second section: trends and segment performance. Below: detailed drill-down available via filters. User scans from top to bottom, sees most important first, can dive deeper if needed. Attention is directed. Information is discoverable. Dashboard succeeds.
Dashboard Hierarchy
Information Pyramid: What Humans See First
Level 1: Status
KPI summary cards (5 cards max)
Current month revenue, active users, churn rate. Answer: "Are we on track?" Scans in 5 seconds. If red, user investigates. If green, confidence increases.
Level 2: Trends
Time series charts (revenue/month, churn/month)
Answer: "Is it getting better or worse?" Scrolls to see trends. Identifies patterns. Notices when something changed direction.
Level 3: Segments
Revenue by customer type, churn by segment
Answer: "Which parts of the business need attention?" Continues scrolling if needed. Finds patterns in segments.
Level 4: Detail
Filters, drill-down, raw data export
Answer: "I found an anomaly, now show me everything." Only power users reach here. Detail available when needed.
You just learned the information hierarchy that makes dashboards usable. Summary first. Trends second. Detail third. Now apply this structure.
Designing for Human Attention
Organizing Information for Discovery
Principle 1: Progressive Disclosure
Show summary immediately. Hide detail behind filters. User decides "do I need to explore deeper?" If KPIs are green, they leave satisfied. If one is red, they filter that segment and zoom in. Information appears as needed, not all at once. Cognitive load is managed.
Principle 2: Spatial Organization
Top-left is most visible (western reading pattern). Place most critical KPI there. Top row holds all critical metrics. Left side for dimensions that matter most (product vs region). Right side for secondary metrics. Bottom for exploratory detail. Eyes naturally flow left-to-right, top-to-bottom. Use that flow.
Principle 3: Consistent Metaphor
If red means "problem" in one KPI card, red means problem everywhere. If up arrow means "good", up means good for all trends. Consistent visual language reduces cognitive load. User learns the rules once, applies everywhere.
Principle 4: Context Over Numbers
Show "Revenue:50k". Context (comparison, trend, target) makes numbers meaningful. A reader does not have to know "is44k, so yes, $50k is good. Include context always.
You just learned four design principles that make dashboards actually usable. Now you will implement them in code across the next lessons. Dashboard architecture is your foundation.

SQL Window Functions & Ranking Systems


00h 59m 55s

Your analytics team has built clean SQL queries and optimized data pipelines. Now the business needs a dashboard. The marketing VP wants to see campaign performance. The sales director wants revenue by region. The CEO wants a single page that says "are we on track?" You must design a dashboard layout that serves all three needs using the information hierarchy principle: KPI summary at the top, trends in the middle, detail at the bottom.
Task 1: Design the Dashboard Layout (1 mark)
Requirements: Sketch or describe a dashboard layout that follows the four-level information hierarchy:
Level 1 - Status (Top Row): KPI Cards Design 5 KPI summary cards for the top of the dashboard. Each card must include:
* Metric name
* Current value
* Period-over-period change (% or absolute)
* Trend indicator (up/down/flat)
import streamlit as st

st.set_page_config(layout='wide')
st.title('Business Performance Dashboard')

# Level 1: KPI Summary Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label='Revenue', value='$5.2M', delta='+12.5%')
with col2:
    st.metric(label='Active Customers', value='2,500', delta='+5.2%')
with col3:
    st.metric(label='Avg Order Value', value='$145', delta='+3.1%')
with col4:
    st.metric(label='Churn Rate', value='4.8%', delta='-1.2%', delta_color='inverse')
with col5:
    st.metric(label='NPS Score', value='72', delta='+4')

st.divider()
Document why you chose these five metrics. Explain what business question each one answers.
Validation: Layout is described or implemented. Five KPI cards display correctly. Each metric is justified.
Task 2: Build the Trend Section (Level 2) (1 mark)
Requirements: Below the KPI cards, create 2-3 trend charts showing how key metrics changed over time.
Chart 1: Revenue Trend (Line Chart)
import matplotlib.pyplot as plt
import pandas as pd

# Monthly revenue data
months = pd.date_range('2024-01-01', periods=12, freq='M')
revenue = [4.2, 4.5, 4.8, 4.6, 5.0, 5.1, 4.9, 4.7, 5.2, 5.4, 5.5, 5.2]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(months, revenue, marker='o', linewidth=2, color='#1f77b4')
ax.set_title('Monthly Revenue Trend (2024)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue ($M)', fontsize=12)
ax.grid(True, alpha=0.3)

# Add target line
ax.axhline(y=5.0, color='green', linestyle='--', linewidth=1.5, label='Target: $5M')
ax.legend()

plt.tight_layout()
plt.savefig('output/revenue_trend.png', dpi=300)
Chart 2: Customer Metrics (Dual Line Chart) Show active customers and churned customers on the same time axis to reveal the relationship.
Chart 3: Choose your own trend - A third trend chart relevant to your business domain.
Requirements for all trend charts:
* Title that describes what the chart shows
* Labelled axes with units
* At least one annotation or reference line
* Consistent colour palette across all charts
Validation: 2-3 trend charts created. All fully labelled. Consistent colours applied.
Task 3: Build the Segment Section (Level 3) (1 mark)
Requirements: Below trends, create 1-2 comparison charts that break metrics down by segment.
Chart: Revenue by Segment (Bar Chart)
segments = ['Enterprise', 'Mid-Market', 'SMB', 'Starter']
segment_revenue = [2.1, 1.5, 1.0, 0.6]
segment_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(segments, segment_revenue, color=segment_colors)
ax.set_xlabel('Revenue ($M)', fontsize=12)
ax.set_title('Revenue by Customer Segment', fontsize=14, fontweight='bold')

# Add value labels on bars
for bar, val in zip(bars, segment_revenue):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f'${val}M', va='center', fontsize=11)

plt.tight_layout()
plt.savefig('output/revenue_by_segment.png', dpi=300)
Requirements:
* Show at least one segment breakdown
* Use appropriate chart type (bar for comparison)
* Include data labels for easy reading
* Explain what business question this answers
Validation: Segment chart created with complete labels and data values.
Task 4: Apply Progressive Disclosure (Level 4) (1 mark)
Requirements: Add a detail section that users can access when they want to drill deeper.
Streamlit implementation:
st.subheader('Detailed Data Explorer')

# Sidebar filters for drill-down
st.sidebar.header('Filters')
selected_segment = st.sidebar.selectbox('Customer Segment', ['All', 'Enterprise', 'Mid-Market', 'SMB', 'Starter'])
date_range = st.sidebar.date_input('Date Range', value=(start_date, end_date))

# Apply filters
if selected_segment != 'All':
    filtered_df = df[df['segment'] == selected_segment]
else:
    filtered_df = df

# Display filtered data
st.write(f'Showing {len(filtered_df):,} records')
st.dataframe(filtered_df[['customer_id', 'segment', 'revenue', 'last_activity', 'churn_risk']])

# Export option
csv = filtered_df.to_csv(index=False)
st.download_button(
    label='Download CSV',
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv'
)
Requirements:
* Filters that let users narrow data
* Data table showing detailed records
* Export/download option
* Filters affect displayed data dynamically
Validation: Filters work. Data table updates. Download exports correct data.
Task 5: Document Dashboard Design Decisions (1 mark)
Requirements: Create a dashboard_design.md file documenting your design decisions:
# Dashboard Design Documentation

## Information Hierarchy Applied
- Level 1 (Status): 5 KPI cards - what they are and why chosen
- Level 2 (Trends): 2-3 trend charts - what patterns they reveal
- Level 3 (Segments): 1-2 comparison charts - which segments need attention
- Level 4 (Detail): Filters and data table - drill-down capability

## Design Principles Applied
1. Progressive Disclosure: Summary visible immediately, detail behind filters
2. Spatial Organisation: Most important metrics top-left
3. Consistent Metaphor: Green = good, Red = bad across all elements
4. Context Over Numbers: Every metric includes comparison (% change, target line)

## Colour Palette
- Primary: #1f77b4 (blue) - main metric
- Secondary: #ff7f0e (orange) - comparison
- Success: #2ca02c (green) - positive indicators
- Danger: #d62728 (red) - negative indicators

## Target Audience
- Primary: VP of Sales (daily user, checks KPIs and trends)
- Secondary: CEO (weekly glance, reads KPI row only)
- Tertiary: Analysts (uses filters and exports for deeper investigation)

## Data Sources
- KPI values: Computed from vw_monthly_revenue and vw_active_customers views
- Trend data: Queried from agg_daily_revenue aggregated table
- Segment data: Computed from vw_customer_segments view
Validation: Design document explains hierarchy, principles, colours, audience, and data sources.
Submission
Commit:
git add dashboard_app.py
git add output/
git add dashboard_design.md
git commit -m "dashboard: design hierarchical layout with KPIs, trends, segments, and detail"
git push
Submit:
1. GitHub link to dashboard code and design documentation
2. Video (3-5 minutes) covering:
    * Walk through the four-level information hierarchy in your dashboard
    * Explain why each KPI was chosen and what question it answers
    * Show the trend charts and explain what patterns are visible
    * Demonstrate the filters and show how progressive disclosure works
    * Explain how your design principles make the dashboard usable for different audiences
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.42
Analytical SQL Query Optimisation

Hey Analytics Engineer!
Welcome. You have raw data in a database. That data flows to dashboards and reporting tools. Between storage and reporting lives the query layer. Most teams write inefficient queries, running SELECT *, forcing unnecessary joins, and filtering after massive intermediate results. This lesson teaches you query optimization - the engineering skill that keeps dashboards fast when datasets grow from thousands to millions of rows.
Every slow dashboard, every timeout error, every frustrated analyst waiting 30 seconds for a report to load had one thing in common: inefficient SQL. The query itself did not need to be rewritten from scratch - it needed specific patterns applied: selecting only needed columns, filtering early before joins, structuring logic into reusable components with CTEs, and understanding query execution order. This lesson teaches you those patterns.
The Real Scenario
THE PROBLEM
An analytical query runs against a 100 million row transaction table. The query starts with SELECT *, pulling every column (50 columns) even though the analysis only needs 5. It then LEFT JOINs to a customer table (10 million rows), creating a 500GB intermediate result in memory. Finally it applies WHERE filters, which could have eliminated 90% of rows before the join. The query times out. The analyst waits. Business decisions are delayed. The database gets blamed. But the query was the culprit.
THE SOLUTION
Replace SELECT * with explicit columns. Apply WHERE filters before JOINs so the dataset shrinks before joining. Use CTEs to break logic into readable, testable steps that express intent clearly. The same query now runs in 2 seconds. The dashboard loads instantly. The analyst explores freely. The database is fast because the query is efficient.
Why SELECT * Is A Performance Antipattern
The Hidden Cost of Selecting Everything
The performance impact of SELECT *
SELECT * retrieves every column from every row. If a table has 50 columns and you only need 5, the database still fetches all 50. Network traffic increases. Memory usage increases. Column read time increases. On a 100 million row table, you might read 5GB of data when you only needed 500MB. That is a 10x penalty for convenience. In production, when queries run hourly and dashboards refresh every minute, that penalty compounds. Performance degrades. Users notice. Queries get cancelled.
Why explicit column selection matters for maintenance
When a table adds a new column, SELECT * automatically includes it. If that column is large (JSON, text blobs) or sensitive (PII), your query now fetches and exposes data it should not. New team members reading SELECT * cannot tell which columns the query actually depends on - they must trace through the entire logic. Explicit columns document intent. Code readers instantly see what data matters. Future schema changes do not silently break assumptions. This is why every production query must list columns explicitly.
SELECT *
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.year = 2024;
Fetches all transaction columns + all customer columns. Unknown what is used. Performance suffers. Schema changes break silently.
SELECT 
  t.transaction_id,
  t.customer_id,
  t.amount,
  c.customer_name,
  c.country
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.year = 2024;
Fetches only needed columns. Intent is clear. Easy to optimize. Safe from schema surprises.
You just learned why SELECT * is a performance antipattern and why explicit column selection is a production requirement. Now you will learn how filtering before joining reduces intermediate result size by orders of magnitude.
Early Filtering: Apply WHERE Before JOIN
Query Execution Order Matters More Than You Think
The filtering sequence problem
A transactions table has 100 million rows. You want 2024 transactions only (10 million rows). You also need customer names from a customers table. If you join first then filter, the database creates a 100 million row intermediate result (100M × customers table), consuming gigabytes of memory, before filtering discards 90% of it. If you filter first, then join, you start with 10 million rows and join that to customers. Result is 5-10x smaller and 5-10x faster.
Inefficient: Filter after join
SELECT t.transaction_id, t.amount, c.customer_name
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.transaction_year = 2024;
Performance: Slow. Memory usage: High.
Efficient: Filter before join
SELECT t.transaction_id, t.amount, c.customer_name
FROM (SELECT transaction_id, customer_id, amount FROM transactions WHERE transaction_year = 2024) t
JOIN customers c ON t.customer_id = c.id;
Performance: Fast. Memory usage: Low. Filtered 10M rows before join instead of joining 100M first.
You just learned why filtering before joining is critical for performance. Now you will learn how CTEs break complex queries into readable, testable, reusable components.
CTEs: Structuring Complex Queries for Readability
WITH Clauses Transform Spaghetti Into Structure
What is a CTE and why it matters
A CTE (Common Table Expression) is a named temporary result that you reference in subsequent queries. Instead of nesting subqueries five levels deep - which become unreadable - you name each logical step. The final query reads like pseudocode, and every intermediate step is testable independently. CTEs make complex logic understandable. They also let you reference the same intermediate result multiple times without recalculating it, improving performance.
CTE Example: Readable Structure
WITH recent_transactions AS (
  SELECT customer_id, amount, transaction_date
  FROM transactions
  WHERE transaction_date >= CURRENT_DATE - INTERVAL 90 DAY
),
customer_summary AS (
  SELECT customer_id, COUNT(*) as transaction_count, SUM(amount) as total_spent
  FROM recent_transactions
  GROUP BY customer_id
)
SELECT cs.customer_id, cs.transaction_count, cs.total_spent
FROM customer_summary cs
WHERE cs.total_spent > 10000;
Each CTE names a logical step. Code reads top-to-bottom like a story. Maintenance is easier because each step is isolated and testable.
You just learned how CTEs make queries readable, testable, and reusable. Combined with early filtering and explicit columns, you now have the core patterns for writing fast analytical queries at scale. These patterns support dashboards and reporting without performance degradation as data volumes grow.
Measuring Query Performance
How To Measure If Optimization Worked
Query execution time metrics
Before optimization: 45 seconds. After SELECT * removed: 30 seconds. After early filtering: 8 seconds. After CTE restructuring: 2 seconds. Document each improvement. Show stakeholders the compounding effect. Performance monitoring proves optimization was successful. Use EXPLAIN or EXPLAIN ANALYZE (depending on database) to see execution plans and understand where time is spent.
Memory usage tracking
Not just speed - memory matters. A query that reads 500GB of data creates enormous intermediate results. Optimize to reduce data volume early. Tools: EXPLAIN to see intermediate result estimates. Database monitoring tools to see memory usage. Lower memory usage means better performance under load.
Testing at production data volume
A query fast on 1 million rows may be slow on 100 million rows. Always test optimization on actual production data volume. Different volume reveals performance issues hidden in small datasets. Confirm optimizations work at scale before deploying.
Query Optimization Checklist
Before committing any analytical query, verify:
* No SELECT * - every column is explicitly named with intent clear
* WHERE filters applied before JOINs wherever possible - smallest dataset joins first
* Complex logic broken into named CTEs - readability and testability
* Column names match table aliases - no ambiguity
* Query tested on actual data volume - performance validated
* Indexes checked - high-cardinality filter columns should be indexed
* Comments explain why each step exists - especially non-obvious filters
Real-World Performance Impact
Case study: Applying all three patterns to a dashboard query
A revenue dashboard query ran in 45 seconds. After optimization: (1) Replaced SELECT * with explicit columns (removed 30 unused columns from joins). Result: 30 seconds. (2) Applied WHERE filters before JOINs (filtered transactions to 6 months before joining 10 tables). Result: 8 seconds. (3) Structured with CTEs to clarify intent and enable query planner optimization. Final result: 2 seconds. The 22x improvement came from recognizing that each pattern compounds - together they create massive gains.

Analytical SQL Query Optimisation


00h 59m 54s

Your analytics team has inherited a slow dashboard built on inefficient SQL. Queries timeout during peak hours. The database admin complains about resource usage. You must refactor the analytical queries using three optimization techniques: removing SELECT *, filtering before joins, and structuring logic with CTEs. Each refactored query must be compared side-by-side to the original with documented improvements.
Task 1: Refactor Query 1 - SELECT * to Explicit Columns (1 mark)
Original (Inefficient):
SELECT *
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE YEAR(t.transaction_date) = 2024
LIMIT 1000;
Requirements:
1. Rewrite the query explicitly selecting only needed columns:
    * From transactions: transaction_id, transaction_date, amount, customer_id
    * From customers: customer_name, country, account_type
2. Create Python code that executes both queries (original and refactored)
3. Compare execution time and memory usage (if possible with your database)
4. Document in comments why each column was selected and what business question it answers
5. Add a docstring explaining the performance improvement from removing SELECT *
Expected output structure:
original_query = """
SELECT *
FROM transactions t
...
"""

optimized_query = """
SELECT 
    t.transaction_id,
    t.transaction_date,
    t.amount,
    c.customer_name,
    c.country
FROM transactions t
...
"""

# Run both and compare results
original_result = pd.read_sql(original_query, engine)
optimized_result = pd.read_sql(optimized_query, engine)

print(f"Original columns: {original_result.shape[1]}")
print(f"Optimized columns: {optimized_result.shape[1]}")
print(f"Improvement: {((original_result.shape[1] - optimized_result.shape[1])/original_result.shape[1])*100:.1f}% fewer columns")
Validation: Both queries return the same core data. Optimized version fetches fewer columns. Document the memory or time difference observed.
Task 2: Refactor Query 2 - Apply Filters Before JOINs (1 mark)
Original (Joins then filters):
SELECT t.transaction_id, t.amount, c.customer_name, p.product_name
FROM transactions t
JOIN customers c ON t.customer_id = c.id
JOIN products p ON t.product_id = p.id
WHERE t.transaction_date >= '2024-01-01'
  AND t.amount > 100
  AND c.country = 'USA'
LIMIT 5000;
Requirements:
1. Refactor to filter the transactions table BEFORE joining customers and products
2. Structure as a CTE or subquery that filters first
3. Join only to filtered data
4. Execute both queries and compare row counts at each step:
    * Full transactions table size
    * Filtered transactions (before join)
    * Final result (after join)
5. Calculate the reduction factor for the intermediate dataset
Expected output structure:
# Inefficient - count at join
transactions_count = pd.read_sql("SELECT COUNT(*) FROM transactions", engine).iloc[0,0]
result_inefficient = pd.read_sql("""
    SELECT ...
    FROM transactions t
    JOIN customers c ON ...
    JOIN products p ON ...
    WHERE ...
""", engine)

# Efficient - count after filter, before join
filtered_transactions = pd.read_sql("""
    SELECT COUNT(*) FROM transactions
    WHERE transaction_date >= '2024-01-01'
      AND amount > 100
""", engine).iloc[0,0]

result_efficient = pd.read_sql("""
    WITH filtered_trans AS (
        SELECT * FROM transactions
        WHERE transaction_date >= '2024-01-01'
          AND amount > 100
    )
    SELECT ...
    FROM filtered_trans ft
    JOIN customers c ON ...
    JOIN products p ON ...
    WHERE c.country = 'USA'
""", engine)

print(f"Original table: {transactions_count:,} rows")
print(f"After filter (before join): {filtered_transactions:,} rows ({(filtered_transactions/transactions_count)*100:.1f}%)")
print(f"Reduction factor: {transactions_count / filtered_transactions:.1f}x smaller dataset before joining")
Validation: Verify both queries return identical results. Document the size reduction achieved by filtering before joining.
Task 3: Refactor Query 3 - Use CTEs for Readability (1 mark)
Original (Nested subqueries, hard to read):
SELECT customer_segment, AVG(revenue_per_transaction) as avg_transaction_value
FROM (
    SELECT 
        c.customer_segment,
        AVG(t.amount) as revenue_per_transaction,
        COUNT(DISTINCT t.transaction_id) as transaction_count
    FROM (
        SELECT t.transaction_id, t.amount, t.customer_id
        FROM transactions t
        WHERE t.transaction_date >= '2024-01-01'
    ) t
    JOIN customers c ON t.customer_id = c.id
    GROUP BY c.customer_segment
) grouped
ORDER BY avg_transaction_value DESC;
Requirements:
1. Rewrite using CTEs to replace nested subqueries
2. Name each CTE clearly (e.g., recent_transactions, customer_segments, segment_metrics)
3. Make each step independently testable
4. Execute both queries and verify identical results
5. Document in comments what each CTE step does
Expected output structure:
refactored_query = """
WITH recent_transactions AS (
    -- Step 1: Filter to recent data
    SELECT transaction_id, amount, customer_id
    FROM transactions
    WHERE transaction_date >= '2024-01-01'
),
customer_with_segment AS (
    -- Step 2: Join to customer data
    SELECT 
        rt.transaction_id,
        rt.amount,
        c.customer_segment
    FROM recent_transactions rt
    JOIN customers c ON rt.customer_id = c.id
),
segment_metrics AS (
    -- Step 3: Calculate segment-level metrics
    SELECT 
        customer_segment,
        COUNT(DISTINCT transaction_id) as transaction_count,
        AVG(amount) as avg_transaction_value,
        SUM(amount) as total_revenue
    FROM customer_with_segment
    GROUP BY customer_segment
)
SELECT 
    customer_segment,
    avg_transaction_value,
    transaction_count,
    total_revenue
FROM segment_metrics
ORDER BY avg_transaction_value DESC;
"""

result = pd.read_sql(refactored_query, engine)
print(result)
Validation: Both queries return identical results. CTE version is easier to read and test. Each CTE can be executed independently for validation.
Task 4: Compare & Document Improvements (1 mark)
Create a comprehensive comparison document showing:
1. Summary Tablecomparison = pd.DataFrame({
2.     'Metric': ['Columns Selected', 'Intermediate Rows', 'Filters Applied Before Join', 'Nesting Depth', 'Readability Score'],
3.     'Original': ['50 (SELECT *)', '500M rows', 'No', '3 levels', 'Hard to follow'],
4.     'Optimized': ['8 explicit', '50M rows', 'Yes', '1 level (CTEs)', 'Clear steps']
5. })
6. print(comparison.to_string(index=False))
7. 
8. Before/After Queries - Show each original alongside refactored version
9. Specific Improvements Identified
    * What inefficiency was in the original
    * What change was made
    * Why it improves performance or readability
    * Quantified impact if measurable (e.g., "10x fewer rows before join")
10. Best Practices Applied
    * List which optimization pattern was used for each query
    * Explain why that pattern was appropriate
Task 5: Answer Follow-Up Questions (1 mark)
In a text or video response, answer these follow-up questions about one of your refactored queries:
1. You created a WHERE clause that filters on a high-cardinality column (many distinct values). An index would speed this up significantly. Explain how an index on that column would improve query performance and what the tradeoff is.
2. For the CTE approach, if you need to reference the same intermediate result multiple times, does the database recalculate it, or does it cache it? (Answer: Most databases cache it, improving efficiency. Some allow explicit materialization. Explain what you learned about your database's behavior.)
3. If the filtered dataset (before joining) is still very large (100 million rows), what query techniques beyond SELECT optimization could further improve performance? (Hint: partitioning, materialized views, aggregation pre-computation.)
Submission
Commit all code to your repository with a clear message:
git add .
git commit -m "query-optimization: refactor 3 analytical queries - explicit columns, early filtering, CTEs"
git push
Submit:
1. GitHub link to your assignment folder showing all refactored queries and comparisons
2. Video explanation (3-5 minutes) covering:
    * Why each optimization was applied to its specific query
    * Side-by-side comparison of original vs refactored (show actual SQL)
    * Performance or readability improvements achieved
    * Answers to the follow-up questions
    * How these patterns will improve dashboard performance in production
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.43
SQL Views & Aggregation Layer Design

Hey Data Layer Architect!
Welcome. You have optimized queries. Now comes the next challenge: making those optimized queries reusable. Right now every dashboard, every notebook, every script re-computes metrics independently. Revenue is calculated three different ways on three different dashboards. Customer activity means one thing in SQL and another in Python. This lesson teaches you to build a clean data layer - SQL views that define metrics once and pre-aggregated tables that serve dashboards efficiently.
Every data team that scaled beyond two people discovered the same problem: metrics computed in multiple places diverge silently. Revenue on Dashboard A does not match Dashboard B. Nobody knows which is right. Trust erodes. Meetings derail into arguments about numbers instead of decisions about strategy. The root cause: no single source of truth. This lesson fixes that by teaching you to build SQL views and aggregation tables that define every metric exactly once.
The Real Scenario
THE PROBLEM
A company has three dashboards: one for sales, one for customer success, one for operations. Each dashboard computes "monthly revenue" independently. Sales calculates gross revenue including refunds. Customer success calculates net revenue after refunds. Operations calculates revenue only for shipped orders. The CEO asks "what was our revenue last month?" and receives three different numbers. Nobody can answer confidently. The real problem is not the math - it is that revenue was never defined in one place.
THE SOLUTION
Build SQL views that define each metric once. A view named vw_monthly_revenue encapsulates the official revenue calculation. Every dashboard queries the view instead of writing its own calculation. When the definition changes (e.g., "revenue now excludes refunds"), you update one view and every dashboard automatically uses the new definition. Pre-aggregated tables store expensive computations so dashboards load instantly.
What SQL Views Are and Why They Matter
A Named Query That Becomes Your Single Source of Truth
What is a SQL view
A SQL view is a saved query that behaves like a table. You define the query once with CREATE VIEW and then SELECT from it like any table. The database executes the underlying query every time you query the view. Views do not store data - they store logic. This means the view always returns fresh results based on current data. Think of a view as a function in programming: you define it once and call it everywhere.
Why views prevent metric drift
Without views, every dashboard writes its own revenue query. Over time, queries diverge. One analyst adds a filter for refunds, another does not. With a view, the revenue calculation exists in exactly one place. If the business decides to exclude refunds from revenue, you update the view definition. Every dashboard, notebook, and report that queries the view automatically gets the updated logic. Zero duplication. Zero drift.
Creating a view - syntax
CREATE VIEW vw_active_customers AS
SELECT 
  c.customer_id,
  c.customer_name,
  c.segment,
  COUNT(DISTINCT o.order_id) AS order_count_30d,
  SUM(o.order_amount) AS revenue_30d,
  MAX(o.order_date) AS last_order_date,
  DATEDIFF(CURRENT_DATE, MAX(o.order_date)) AS days_since_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
  AND o.order_date >= CURRENT_DATE - INTERVAL 30 DAY
WHERE c.deleted_at IS NULL
GROUP BY c.customer_id, c.customer_name, c.segment;
Now any dashboard queries SELECT * FROM vw_active_customers instead of re-implementing this logic. One definition serves the entire team.
You just learned what SQL views are and how they prevent metric drift across dashboards. Now you will learn how to design views with clear naming conventions that your entire team can follow.
View Naming Conventions and Design Patterns
Naming Is Not Cosmetic - It Is How Teams Navigate Data
Prefix pattern: vw_ for views
Prefix every view with vw_. This tells anyone reading the SQL that the object is a view, not a raw table. Pattern:vw_entity_metricExamples: vw_active_customers, vw_monthly_revenue, vw_product_performance. When a new team member sees vw_, they immediately know: this is a defined metric layer, not raw data.
Design pattern: one view per business concept
Do not pack every metric into one massive view. Create focused views: one for active customers, one for monthly revenue, one for product performance. Each view answers one family of business questions. Dashboards compose by querying multiple views. This keeps views maintainable - when the revenue definition changes, you only touch vw_monthly_revenue, not a monolithic view containing everything.
ANTI-PATTERN
One view called vw_everything that joins 10 tables and returns 50 columns. Slow. Hard to maintain. Nobody knows which columns matter. Changes break multiple dashboards.
CORRECT PATTERN
Focused views: vw_active_customers (7 columns), vw_monthly_revenue (5 columns), vw_product_performance (6 columns). Each is fast, focused, and independently maintainable.
You just learned naming conventions and design patterns for SQL views. Now you will learn when views are not enough and you need pre-aggregated tables for dashboard performance.
Pre-Aggregated Tables for Dashboard Performance
When Views Are Too Slow, Pre-Compute the Answer
The performance limitation of views
Views re-execute their underlying query every time you SELECT from them. If a view joins 5 tables and scans 100 million rows, every dashboard refresh re-runs that expensive computation. For small datasets, views are fine. For large datasets powering dashboards that refresh every minute, views become a performance bottleneck. The solution: pre-aggregate results into a physical table that dashboards query directly.
Creating a pre-aggregated table
CREATE TABLE agg_daily_revenue (
  aggregation_date DATE,
  product_line VARCHAR(100),
  total_revenue NUMERIC(12,2),
  order_count INTEGER,
  avg_order_value NUMERIC(10,2),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO agg_daily_revenue
SELECT 
  DATE(o.order_date) AS aggregation_date,
  p.product_line,
  SUM(o.order_amount) AS total_revenue,
  COUNT(DISTINCT o.order_id) AS order_count,
  AVG(o.order_amount) AS avg_order_value,
  CURRENT_TIMESTAMP AS updated_at
FROM orders o
JOIN products p ON o.product_id = p.id
GROUP BY DATE(o.order_date), p.product_line;
Dashboards query agg_daily_revenue directly. Result: instant load times regardless of raw table size.
Naming convention: agg_ prefix
Prefix aggregated tables with agg_. Pattern: agg_[grain]_[subject]. Examples: agg_daily_revenue, agg_hourly_metrics, agg_monthly_churn. The prefix tells everyone: this is pre-computed data, not raw data, and it needs periodic refresh.
Always include updated_at in aggregated tables
The updated_at timestamp tells consumers how stale the data is. If agg_daily_revenue was last updated 3 days ago, the dashboard should display a warning. Without this column, users assume data is current when it may not be. Stale data presented as current data is worse than no data at all.
You just learned when and how to build pre-aggregated tables for dashboard performance. Now you will learn how to refresh these tables and version-control your view definitions as code.
Refresh Strategy and Version Control
Treating SQL Definitions as Code
Refresh patterns for aggregated tables
Aggregated tables must be refreshed on a schedule. Common patterns: (1) Full refresh - truncate and reload. Simple but slow for large tables. Best for daily aggregations. (2) Incremental refresh - only insert or update rows for dates not yet aggregated. Faster but more complex. Best for hourly or real-time aggregations. (3) Append-only - insert new rows without touching historical data. Fastest but requires careful de-duplication. Choose based on data volume and freshness requirements.
Save view definitions as .sql files in version control
Every view and aggregation query should be saved as a .sql file in your repository. Structure: database/views/vw_active_customers.sql and database/aggregations/agg_daily_revenue.sql. Include comments at the top of each file explaining purpose, business metric, who uses it, and column descriptions. Version-controlled SQL means: you can see who changed a metric definition, when, and why. Rollback is possible. Code review catches errors before they reach production.
Clean data layer checklist
* Every shared metric defined as a SQL view with vw_ prefix
* Expensive computations pre-aggregated in agg_ tables with updated_at
* Dashboards query views and aggregated tables - never raw tables directly
* All SQL definitions saved as .sql files in version control with comments
* Refresh schedule documented and automated
* Naming conventions documented in a team conventions file
You just learned how to build a complete clean data layer with SQL views, pre-aggregated tables, naming conventions, and version control. This layer is the foundation that prevents metric drift and keeps dashboards fast and trustworthy.

SQL Views & Aggregation Layer Design


00h 59m 53s

Your analytics team operates dashboards across sales, customer success, and operations. Currently, each dashboard computes metrics independently - there is no single source of truth. Revenue is calculated differently on three dashboards. Customer activity metrics conflict. You have been tasked to design and build the clean data layer: SQL views that define metrics once, and pre-aggregated tables that serve dashboards efficiently.
Task 1: Create Two SQL Views (1 mark)
Requirements: Create two SQL views with clear naming convention (prefix: vw_). Each view should encapsulate business logic that multiple dashboards will use.
View 1 - Active Customer Metrics
CREATE VIEW vw_active_customers AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) as order_count_30d,
    SUM(o.order_amount) as revenue_30d,
    MAX(o.order_date) as last_order_date,
    DATEDIFF(CURRENT_DATE, MAX(o.order_date)) as days_since_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
    AND o.order_date >= CURRENT_DATE - INTERVAL 30 DAY
WHERE c.deleted_at IS NULL
GROUP BY c.customer_id, c.customer_name, c.segment;
View 2 - Choose your own metric - Create a second view that calculates a meaningful metric for your domain (e.g., vw_product_performance, vw_churn_risk_cohorts, vw_revenue_by_region). Include:
* Join at least 2 tables
* Apply WHERE filters to define the metric
* Include a comment explaining what business question it answers
Python submission:
# Create both views
execute_sql("""CREATE VIEW vw_active_customers AS ...""")
execute_sql("""CREATE VIEW vw_your_custom_metric AS ...""")

# Query the views to confirm they work
active_customers = pd.read_sql("SELECT * FROM vw_active_customers LIMIT 10", engine)
custom_metric = pd.read_sql("SELECT * FROM vw_your_custom_metric LIMIT 10", engine)

print("View 1 columns:", active_customers.columns.tolist())
print("View 2 columns:", custom_metric.columns.tolist())
Validation: Both views execute without error. Querying them returns correct business metrics. Document the intent of each view.
Task 2: Create One Pre-Aggregated Summary Table (1 mark)
Requirements: Create a pre-aggregated table that summarizes data at a specific grain (daily, hourly, or customer level). Include an updated_at timestamp to track when aggregation was computed.
Example structure:
CREATE TABLE agg_daily_metrics (
    aggregation_date DATE,
    metric_name VARCHAR(100),
    metric_value NUMERIC,
    row_count INTEGER,
    updated_at TIMESTAMP
);
Then populate it with a real aggregation query:
INSERT INTO agg_daily_metrics
SELECT 
    DATE(o.order_date) as aggregation_date,
    'total_revenue' as metric_name,
    SUM(o.order_amount) as metric_value,
    COUNT(*) as row_count,
    CURRENT_TIMESTAMP as updated_at
FROM orders o
GROUP BY DATE(o.order_date);
Python submission:
# Create the aggregated table
create_table_sql = """CREATE TABLE agg_daily_metrics ( ... )"""
execute_sql(create_table_sql)

# Populate with aggregation query
populate_sql = """INSERT INTO agg_daily_metrics SELECT ..."""
execute_sql(populate_sql)

# Verify
agg_data = pd.read_sql("SELECT * FROM agg_daily_metrics ORDER BY aggregation_date DESC LIMIT 10", engine)
print(f"Aggregated {len(agg_data)} rows")
print(agg_data)

# Show that query against pre-aggregated table is instant
import time
start = time.time()
result = pd.read_sql("SELECT metric_name, SUM(metric_value) FROM agg_daily_metrics GROUP BY metric_name", engine)
elapsed = time.time() - start
print(f"Query time: {elapsed*1000:.2f}ms")
Validation: Table is created, populated, and queryable. Confirm updated_at is set correctly.
Task 3: Query Views & Aggregated Tables from Python (1 mark)
Requirements: Demonstrate that dashboards can query the clean data layer you built. Query both views and the aggregated table from Python, simulating how a Streamlit dashboard would use them.
Python code structure:
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("your_database_connection")

# Query View 1: Active Customers
active_cust_df = pd.read_sql("""
    SELECT 
        customer_id, 
        customer_name, 
        revenue_30d,
        days_since_order
    FROM vw_active_customers
    WHERE days_since_order <= 30
    ORDER BY revenue_30d DESC
    LIMIT 20
""", engine)

print("Top 20 Active Customers (last 30 days):")
print(active_cust_df)

# Query View 2: Your custom metric
custom_result = pd.read_sql(f"""
    SELECT * FROM vw_your_custom_metric
    LIMIT 20
""", engine)

print("\nCustom Metric Results:")
print(custom_result)

# Query Pre-Aggregated Table
agg_result = pd.read_sql("""
    SELECT 
        aggregation_date,
        metric_name,
        metric_value
    FROM agg_daily_metrics
    WHERE aggregation_date >= CURRENT_DATE - INTERVAL 30 DAY
    ORDER BY aggregation_date DESC
""", engine)

print("\nDaily Aggregated Metrics (last 30 days):")
print(agg_result)

# Demonstrate filtering capability
active_by_segment = pd.read_sql("""
    SELECT 
        segment,
        COUNT(*) as customer_count,
        SUM(revenue_30d) as total_segment_revenue,
        AVG(revenue_30d) as avg_customer_revenue
    FROM vw_active_customers
    GROUP BY segment
    ORDER BY total_segment_revenue DESC
""", engine)

print("\nRevenue by Segment:")
print(active_by_segment)
Validation: All three data sources (2 views + 1 aggregated table) query successfully. Results are sensible.
Task 4: Define & Apply Naming Conventions (1 mark)
Requirements: Document the naming conventions you applied and show they are used consistently.
Create a file data_layer_conventions.md:
# Clean Data Layer Naming Conventions

## Views
- Prefix: `vw_`
- Pattern: `vw_[business_entity]_[metric]`
- Examples:
  - `vw_active_customers` - customers with recent activity
  - `vw_product_performance` - sales and metrics per product

## Pre-Aggregated Tables
- Prefix: `agg_`
- Pattern: `agg_[grain]_[subject]`
- Include aggregation frequency (daily, hourly, etc)
- Examples:
  - `agg_daily_revenue` - daily revenue aggregates
  - `agg_hourly_metrics` - metrics refreshed hourly

## Columns in Aggregated Tables
- Always include: `created_at` or `updated_at` (when aggregation computed)
- Always include: count of rows aggregated (to validate)
- Always include: date/time grain column (date_day, hour, customer_id)

## Benefits
- Clear object type from name alone
- Consistent across team
- Dashboards know where to query
- Metric definitions cannot drift
Show applied conventions: List all view names you created and how they follow the pattern. List all aggregated table names. Show that your Python code includes comments explaining what each object does.
Task 5: View Definitions Committed as .sql Files (1 mark)
Requirements: Save each view definition as a .sql file in your repository. Include descriptive comments explaining the business metric.
File structure:
database/
├── views/
│   ├── vw_active_customers.sql
│   └── vw_your_custom_metric.sql
└── aggregations/
    └── agg_daily_metrics.sql
Example file: database/views/vw_active_customers.sql
-- View: vw_active_customers
-- Purpose: Identify customers with recent activity (last 30 days)
-- Business metric: Customers active in rolling 30-day window
-- Updated: Automatically with each query (view recalculates)
-- Used by: Customer engagement dashboard, retention analysis
-- 
-- Columns:
--   customer_id: Unique customer identifier
--   customer_name: Customer display name
--   segment: Customer segment classification
--   order_count_30d: Number of orders in last 30 days
--   revenue_30d: Total revenue from last 30 days
--   last_order_date: Most recent order date
--   days_since_order: Days elapsed since last order

CREATE VIEW vw_active_customers AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) as order_count_30d,
    SUM(o.order_amount) as revenue_30d,
    MAX(o.order_date) as last_order_date,
    DATEDIFF(CURRENT_DATE, MAX(o.order_date)) as days_since_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
    AND o.order_date >= CURRENT_DATE - INTERVAL 30 DAY
WHERE c.deleted_at IS NULL
GROUP BY c.customer_id, c.customer_name, c.segment;
Validation: Each .sql file contains the full view/table definition with comments. Files are organized in a logical folder structure. All files are committed to git.
Bonus: Answer Follow-Up Questions (Optional enhancement)
1. When a view definition changes, do existing dashboards automatically use the new definition? Why or why not?
2. If an aggregated table is computed once per hour, what happens to data between refresh cycles? How would you handle real-time metrics?
3. How would you test that a view or aggregated table is correct before releasing it to dashboards?
Submission
Commit to repository:
git add database/
git add data_layer_conventions.md
git add assignment-33-python.py
git commit -m "data-layer: create views and aggregation tables for metrics"
git push
Submit:
1. GitHub link to assignment folder with view definitions and aggregation tables
2. Video explanation (3-5 minutes) covering:
    * Each view created, what metric it defines, and why it is useful
    * The aggregated table structure and refresh strategy
    * How dashboards query the clean layer without touching raw tables
    * Naming conventions applied and why consistency matters
    * Follow-up question about view updates or real-time metrics
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.44
SQL-Based Insight Validation

Hey Data Quality Guardian!
Welcome. You compute a metric in Python. The same metric exists as a SQL view. Do they agree? If your Python result is 1000 active users but SQL returns 1200, you have a computation drift problem - one calculation layer is wrong, or both are wrong, but you did not know to check. This lesson teaches you to validate that SQL and Python produce identical metrics, catching discrepancies before they corrupt dashboards and reports.
Every data team that scaled has discovered a metric computed two different ways that produced different results. Nobody caught it for weeks. Reports show conflicting numbers. Stakeholders lose trust. The expensive lesson: always validate computational layers against each other. This lesson teaches that discipline.
The Real Scenario
THE PROBLEM
A company computes customer churn rate both in SQL (for dashboards) and in Python (for analysis notebooks). The SQL version calculates "customers active in month N-1 but not month N" as churn. Python has a slightly different definition: "customers who spent in month N-1 but had zero activity in month N." Same concept, different conditions. SQL shows 5% churn. Python shows 7% churn. Which is right? Both? Neither? The company reports 5% to executives and 7% to the data team. Confusion multiplies. The root cause: two computational layers operated without validation against each other.
THE SOLUTION
Create a validation script that computes key metrics in both SQL and Python, compares results side-by-side, and flags any discrepancy larger than a defined tolerance. If they agree, metrics are trustworthy. If they diverge, investigate and fix before reporting. This is the discipline that prevents metric corruption at scale.
What Is Computation Drift
When Two Calculation Layers Produce Different Results
Definition mismatch
SQL query includes refunded orders. Python code excludes them. Same data, different results. Root cause: definitions were not synchronized. One person assumed inclusion. Another assumed exclusion. Neither checked.
Schema change drift
A NULL handling rule changed in Python (NaNs now treated as zeros). SQL still treats NULLs as missing. Results diverge. SQL was updated, Python was not. Neither is necessarily wrong - they need to agree on policy.
Data quality drift
SQL joins on customer_id. Some rows have NULL customer_id. SQL excludes them with the join (LEFT JOIN with IS NOT NULL implied). Python's merge keeps them (NaN keys). Result differs in row count. Neither is wrong - they handle missing keys differently.
Common Computation Drift Scenarios
Real examples of drift and how to catch it
* Date handling: SQL uses YYYY-MM-DD, Python uses datetime objects. Comparison at year boundary fails. Fix: Explicit date parsing in both layers.
* NULL vs NaN: SQL treats NULL as missing. Python treats NaN as numeric zero. Revenue calculations diverge. Fix: Explicit NULL handling in SQL to match Python behavior.
* Rounding: SQL rounds at database level, Python rounds in application. Percentage calculations differ slightly. Fix: Apply identical rounding in both layers.
* Timezone: SQL uses UTC, Python uses local timezone. Timestamps differ by hours. Fix: Normalize to same timezone in both queries.
* String case: SQL case-sensitive in one database, case-insensitive in another. Join keys mismatch. Fix: Force case-insensitive comparison in both layers.
Investigating and Fixing Discrepancies
When SQL and Python Disagree, This Is Your Process
Step 1: Identify scope of mismatch
Is it one customer ID? One date range? All data? This tells you if the problem is systematic or isolated. Isolated issues are usually data quality. Systematic issues usually indicate logic differences.
Step 2: Trace the calculation manually
Pick one row where they disagree. Hand-compute the metric using raw data. Which layer matched your manual calculation? That is the correct one. Use that as the source of truth.
Step 3: Update the incorrect layer
Change the SQL or Python to match the correct calculation. Document why the original was wrong. Document the fix. Re-validate. Both layers should now agree.
Setting Up Continuous Validation
Automate validation to catch drift as soon as it appears
Schedule validation queries to run daily. Store results in a validation table. If any metric exceeds its tolerance threshold, log an alert. Send email notifications to the data team. Do not wait for someone to notice. Automated validation catches drift the day it appears, not weeks later. This discipline prevents metrics from silently diverging and corrupting reports.
Documentation as part of validation
Record any expected differences between layers. Example: "SQL includes refunds, Python excludes them by design." Document tolerance thresholds and why they are acceptable. This prevents false alarms and ensures future team members understand why differences exist. Version control this documentation along with code.
You just learnedhow to validate computational layers, catch drift, and maintain metric integrity. Cross-layer validation is insurance against silent failures that corrupt dashboards and reports.

SQL-Based Insight Validation


00h 59m 55s

Your analytics workflow uses both SQL and Python to compute customer metrics. A recent audit found that churn calculations differ between the two layers. SQL shows 5.2% churn. Python shows 6.8% churn. Before reporting to leadership, you must cross-validate all key metrics, identify discrepancies, investigate root causes, and document the fixes.
Task 1: Compute Three Metrics in Both SQL and Python (1 mark)
Metric 1: Active Users (30-day) Select users who have logged in at least once in the last 30 days.
SQL query:
SELECT COUNT(DISTINCT user_id) as active_users
FROM logins
WHERE login_date >= CURRENT_DATE - INTERVAL 30 DAY;
Python equivalent:
logins_df = pd.read_sql("SELECT * FROM logins", engine)
active_users_py = logins_df[
    logins_df['login_date'] >= (date.today() - timedelta(days=30))
]['user_id'].nunique()
Metric 2: Average Order Value (AOV) Calculate mean order amount for all orders.
SQL: SELECT AVG(order_amount) as aov FROM orders;
Python equivalent:
orders_df = pd.read_sql("SELECT * FROM orders", engine)
aov_py = orders_df['order_amount'].mean()
Metric 3: Customer Churn (Monthly) Customers active in month N-1 but not month N (with spending > 0 in month N-1).
SQL:
SELECT COUNT(DISTINCT c1.customer_id) as churned_customers
FROM (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE MONTH(order_date) = MONTH(CURRENT_DATE) - 1
      AND order_amount > 0
) c1
LEFT JOIN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE MONTH(order_date) = MONTH(CURRENT_DATE)
) c2 ON c1.customer_id = c2.customer_id
WHERE c2.customer_id IS NULL;
Python equivalent (implement this)
Python submission:
import pandas as pd
from datetime import date, timedelta

# Metric 1: Active Users
sql_metric1 = pd.read_sql(sql_query_1, engine).iloc[0, 0]
py_metric1 = logins_df[...].nunique()

# Metric 2: AOV
sql_metric2 = pd.read_sql(sql_query_2, engine).iloc[0, 0]
py_metric2 = orders_df['order_amount'].mean()

# Metric 3: Churn
sql_metric3 = pd.read_sql(sql_query_3, engine).iloc[0, 0]
py_metric3 = # your python calculation

metrics_comparison = pd.DataFrame({
    'Metric': ['Active Users', 'AOV', 'Churn'],
    'SQL Result': [sql_metric1, sql_metric2, sql_metric3],
    'Python Result': [py_metric1, py_metric2, py_metric3]
})
print(metrics_comparison)
Validation: All three metrics computed in both layers. Results recorded for comparison.
Task 2: Identify and Document Discrepancies (1 mark)
Requirements: Compare results and flag any difference.
Python code:
comparison = pd.DataFrame({
    'Metric': ['Active Users', 'AOV', 'Churn'],
    'SQL': [sql_metric1, sql_metric2, sql_metric3],
    'Python': [py_metric1, py_metric2, py_metric3],
    'Difference': [
        abs(sql_metric1 - py_metric1),
        abs(sql_metric2 - py_metric2),
        abs(sql_metric3 - py_metric3)
    ]
})

comparison['Percent_Difference'] = (
    (comparison['Difference'] / comparison['SQL'].abs()) * 100
).round(2)

print("Metrics Comparison:")
print(comparison)

# Flag issues
print("\nDiscrepancies found:")
for idx, row in comparison.iterrows():
    if row['Percent_Difference'] > 0.1:  # Tolerance threshold
        print(f"  ⚠️ {row['Metric']}: {row['Percent_Difference']}% difference")
    else:
        print(f"  ✓ {row['Metric']}: Match within tolerance")
Validation: Discrepancies clearly identified. Document which metrics match and which do not.
Task 3: Build Automated Validation Script (1 mark)
Requirements: Create a reusable validation script that can run daily to catch drift automatically.
Structure:
def validate_metrics(engine, tolerance_pct=0.1):
    """
    Validate that SQL and Python compute identical metrics.
    
    Args:
        engine: SQLAlchemy database engine
        tolerance_pct: Acceptable percentage difference (default 0.1%)
    
    Returns:
        validation_report: DataFrame with all metrics and match status
    """
    
    # Define metrics to validate
    metrics = {
        'active_users': {
            'sql': "SELECT COUNT(DISTINCT user_id) FROM logins WHERE ...",
            'python': lambda: logins_df[...]['user_id'].nunique(),
            'tolerance': 0  # Counts must be exact
        },
        'aov': {
            'sql': "SELECT AVG(order_amount) FROM orders",
            'python': lambda: orders_df['order_amount'].mean(),
            'tolerance': 0.1  # Percentages allow 0.1% difference
        },
        'churn': {
            'sql': "SELECT COUNT(...) FROM (...)",
            'python': lambda: # your calculation
            'tolerance': 0
        }
    }
    
    validation_report = []
    
    for metric_name, metric_def in metrics.items():
        sql_result = pd.read_sql(metric_def['sql'], engine).iloc[0, 0]
        py_result = metric_def['python']()
        difference = abs(sql_result - py_result)
        pct_diff = (difference / abs(sql_result)) * 100 if sql_result != 0 else 0
        
        match = pct_diff <= metric_def['tolerance']
        
        validation_report.append({
            'Metric': metric_name,
            'SQL': sql_result,
            'Python': py_result,
            'Difference': difference,
            'Pct_Difference': pct_diff,
            'Tolerance': metric_def['tolerance'],
            'Status': 'PASS' if match else 'FAIL',
            'Timestamp': datetime.now()
        })
    
    return pd.DataFrame(validation_report)

# Run validation
report = validate_metrics(engine)
print(report)

# Save report
report.to_csv('validation_report.csv', index=False)
Validation: Script runs without error. Generates structured validation report with pass/fail status for each metric.
Task 4: Investigate and Document Root Cause (1 mark)
If metrics match: Document why they match - what did you do to ensure alignment?
If metrics differ:
Investigation Steps:
1. Pick one discrepancy - Focus on one metric that does not match
2. Hand-compute - Query raw data and manually calculate the metric for a small subset
# Example: Hand-compute active users for a specific week
sample_week = logins_df[
    (logins_df['login_date'] >= '2024-01-01') & 
    (logins_df['login_date'] <= '2024-01-07')
]
manual_count = sample_week['user_id'].nunique()
print(f"Manual count for sample week: {manual_count}")
1. Identify the discrepancy cause - Possibilities:
    * NULL handling difference (SQL vs pandas)
    * Type conversion (float vs int)
    * Join behavior difference
    * Filter order difference
    * Timezone or date handling
2. Document the root cause in a text file:
## Churn Metric Discrepancy Analysis

**Observed Difference:** SQL=50 customers, Python=68 customers

**Investigation:**
- Manually traced 5 customers who should be counted as churned
- Hand calculation matched Python result (68)
- Examined SQL query: the LEFT JOIN was missing a WHERE clause

**Root Cause:**
SQL query did not filter month correctly. Used MONTH() function which
strips year context. Across year boundaries, results differ.

**Fix Applied:**
Changed MONTH() comparison to DATE comparison with explicit date ranges.
SQL now matches Python.

**Validation:**
After fix, both compute 68 churned customers. Metric is trustworthy.
Validation: Document which calculation was correct and why.
Task 5: Answer Follow-Up Question (1 mark)
In a text or video response, answer this follow-up:
Question: You have a validation script that runs daily and catches metrics drift automatically. However, it flags a discrepancy but does not auto-fix it - someone must investigate. Why is manual investigation necessary? What would be the risk of auto-fixing based on a tolerance threshold alone?
Expected answer elements:
* Tolerance thresholds catch divergence, not correctness
* A metric can drift without triggering the threshold (creeping drift)
* Manual review ensures the "correct" calculation is chosen, not just one side
* Root cause understanding is critical for preventing future issues
Submission
Commit code:
git add validation_script.py
git add validation_report.csv
git add discrepancy_analysis.md
git commit -m "validation: cross-check SQL and Python metrics, document discrepancies"
git push
Submit:
1. GitHub link to validation script and reports
2. Video (3-5 minutes) covering:
    * All three metrics computed and compared side-by-side
    * Discrepancies identified (or why metrics matched)
    * Validation script structure and how it detects drift
    * Root cause investigation process (with specific examples)
    * Answer to follow-up question on why manual review is necessary
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.45
Business Visualisation Principles
Hey Visualisation Designer!
Welcome. Dashboard architecture is planned. Data layer is clean. Now comes the craft of turning numbers into pictures that humans understand instantly. Every chart type exists for a reason - bar charts compare, line charts show trends, histograms reveal distributions, scatter plots expose correlations. Choosing wrong means the audience misreads the data. This lesson teaches you when to use which chart, how to label everything so it communicates without explanation, and how to style consistently so dashboards feel professional.
Every chart that confused a stakeholder, that was misinterpreted in a meeting, or that failed to communicate a finding had one thing in common: the chart type did not match the data relationship being shown. A pie chart was used for 20 categories. A bar chart was used for time-series data. A table was used when a single number would suffice. This lesson teaches you the principles that prevent every one of those mistakes.
The Real Scenario
THE PROBLEM
An analyst presents quarterly revenue as a pie chart. Six product lines are shown as slices. The CEO asks "which product grew the most?" The pie chart cannot answer that question - it shows proportion, not change over time. The analyst switches to a table of numbers. The meeting stalls while everyone scans rows and columns. Nobody can see the pattern. The insight is buried. The decision is delayed. The charts failed because they were chosen based on what looked interesting, not what the data needed to communicate.
THE SOLUTION
Match chart type to data relationship. Bar chart for comparison across categories. Line chart for trends over time. Histogram for distributions. Scatter plot for correlations. Stacked bar for composition. Add complete labels - title, axes, units, legend, annotations. Apply a consistent colour palette across all charts. The audience reads the insight in 5 seconds without needing explanation.
Choosing the Right Chart Type
Every Data Relationship Has a Chart Type Built For It
Bar Chart
Comparison across categories
Use when comparing discrete items: revenue by product line, sales by region, headcount by department. Horizontal bars work better when category names are long. Vertical bars work better when comparing a few items. The human eye compares bar lengths effortlessly - this is the most universally understood chart type.
Line Chart
Trends over time
Use when showing how a metric changes over a continuous axis - typically time. Revenue per month, active users per week, churn rate per quarter. The connected line implies continuity between data points. Multiple lines on the same chart compare trends across segments. Never use line charts for categorical data - categories are not continuous.
Histogram
Distribution of values
Use when showing how values are distributed: order value ranges, customer age distribution, response time distribution. Histograms reveal patterns invisible in averages - bimodal distributions (two peaks), skewed distributions, outliers. A histogram answers "what is typical?" and "how spread out is the data?" in one glance.
Scatter Plot
Correlation between two variables
Use when exploring if two variables are related: marketing spend vs revenue, response time vs satisfaction score, price vs demand. Each dot is one observation. Clusters reveal patterns. Outliers are immediately visible. Add a trend line to quantify the relationship. Scatter plots answer "does X relate to Y?" visually.
Stacked Bar
Composition and part-to-whole relationships
Use when showing how a total breaks into components: revenue by quarter stacked by product, headcount by year stacked by department. Total bar height shows the whole. Segments show parts. Viewers see both composition and total simultaneously. Limit to 5 segments maximum - more becomes unreadable.
You just learned which chart type matches which data relationship. Now you will learn the labelling rules that make every chart self-explanatory without requiring a presenter.
Complete Labelling: Making Charts Self-Explanatory
A Chart Without Labels Is a Picture Without Meaning
Every chart needs these five elements
(1) Title - describes what the chart shows, not what it is. "Q4 Revenue by Product Line" not "Bar Chart". (2) X-axis label with units. "Month" or "Product Line". (3) Y-axis label with units. "Revenue ($)" or "Count". (4) Legend for multi-series charts. Placed where it does not overlap data. (5) Data labels on bars or points when the chart has few enough elements to be readable. These five elements make any chart interpretable without the creator explaining it.
Format numbers for human readability
Do not display 5200000 on an axis. Displayprefix and appropriate precision. Format dates as "Jan 2024" not "2024-01-01" for monthly charts. Human-readable formatting reduces cognitive load and prevents misreading.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(products, revenue, color='#1f77b4')
ax.set_xlabel('Revenue ($)', fontsize=12)
ax.set_ylabel('Product Line', fontsize=12)
ax.set_title('Q4 Revenue by Product Line', fontsize=14, fontweight='bold')

# Format x-axis as currency
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

plt.tight_layout()
plt.savefig('output/revenue_by_product.png', dpi=300, bbox_inches='tight')
You just learned the five labelling elements every chart needs and how to format numbers for human readability. Now you will learn how a consistent colour palette makes dashboards professional and accessible.
Consistent Colour Palette and Accessibility
One Palette, Every Chart, Every Dashboard
Why colour consistency matters
If "Product A" is blue in Chart 1, it must be blue in Chart 2, Chart 3, and every chart on the dashboard. If blue means "revenue" on one chart and "churn" on another, the viewer is confused. Consistent colour creates a visual language. The viewer learns "blue = Product A" once and applies it everywhere. Inconsistent colour forces re-learning on every chart.
Define and reuse a palette
# Define once, use everywhere
PALETTE = {
  'primary': '#1f77b4',
  'secondary': '#ff7f0e',
  'success': '#2ca02c',
  'danger': '#d62728',
  'neutral': '#7f7f7f'
}

CHART_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Apply to every chart
ax.bar(categories, values, color=CHART_COLORS[:len(categories)])
Colour blindness accessibility
Approximately 8% of men have some form of colour vision deficiency. Red-green colour blindness is most common. Never rely on colour alone to convey meaning. Always pair colour with another visual cue: shape (circle vs square markers), pattern (solid vs dashed lines), or text labels. Test your palette with a colour blindness simulator. If your chart is unreadable in greyscale, it needs additional visual encoding.
You just learned how to define and maintain a consistent colour palette and why accessibility matters for professional dashboards. Now you will learn how annotations transform good charts into insight-delivering tools.
Annotations: Highlighting What Matters
A Chart Shows Data - An Annotation Shows Insight
What to annotate
Annotate anomalies ("August dip: seasonal effect"), thresholds ("Target:6.2M"), and events that explain patterns ("Product launch: March 15"). Annotations tell the viewer what to notice. Without them, the viewer sees data but misses the story.
Annotation code pattern
# Annotate peak
ax.annotate(
  'Peak Sales\n($6.2M)',
  xy=(peak_date, peak_value),
  xytext=(peak_date, peak_value + 500000),
  arrowprops=dict(arrowstyle='->', color='red', lw=2),
  fontsize=11, ha='center',
  bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7)
)

# Add target reference line
ax.axhline(y=5000000, color='green', linestyle='--', linewidth=2, label='Target')
ax.legend()
Reference lines add context
A horizontal reference line showing the target, average, or threshold transforms a chart from "here is what happened" to "here is what happened relative to what should have happened." Without the reference line,4.5M target line, $5M becomes "11% above target." Context converts data into insight.
You just learned how annotations and reference lines transform charts from data displays into insight-delivery tools. Combined with correct chart types, complete labels, and consistent colours, you now have the full visualisation toolkit for professional business dashboards.

Business Visualisation Principles


00h 59m 56s

You are building an analytical dashboard for business stakeholders. Your job is to create five distinct visualizations that communicate different data relationships. Each chart must use the correct type, include clear labels, apply consistent styling, and highlight key insights through annotation.
Task 1: Create Five Chart Types (1 mark)
Create five different visualizations, each answering a specific business question:
Chart 1: Bar Chart (Comparison) Show total revenue by product line for the last quarter. Use matplotlib or seaborn.
import matplotlib.pyplot as plt
import pandas as pd

# Data: revenue by product
revenue_by_product = pd.read_sql("""
    SELECT product_line, SUM(order_amount) as revenue
    FROM orders
    WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
    GROUP BY product_line
    ORDER BY revenue DESC
""", engine)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(revenue_by_product['product_line'], revenue_by_product['revenue'])
ax.set_xlabel('Revenue ($)', fontsize=12)
ax.set_ylabel('Product Line', fontsize=12)
ax.set_title('Q4 Revenue by Product Line', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/chart1_revenue_by_product.png', dpi=300, bbox_inches='tight')
Chart 2: Line Chart (Trend) Show revenue trend over the last 12 months with multiple lines for top 3 products.
Chart 3: Histogram (Distribution) Show the distribution of order values (bin into ranges like100,500, etc).
Chart 4: Stacked Bar (Composition) Show total revenue by quarter, stacked by product line to show composition.
Chart 5: Scatter Plot (Correlation) Show the relationship between marketing spend and revenue generated.
Validation: All five chart types created and saved as image files.
Task 2: Label All Charts Completely (1 mark)
Requirements: Every chart must have:
* Title: Clear, describes what the chart shows
* X-axis label: With units (e.g., "Revenue ($)")
* Y-axis label: With units
* Legend: For multi-series charts
* Data labels: Values on bars or points (if readable)
Python structure:
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['date'], df['revenue'], marker='o', linewidth=2, label='Revenue')
ax.set_title('Monthly Revenue Trend (Last 12 Months)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue ($)', fontsize=12)
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)

# Format y-axis as currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

plt.tight_layout()
Validation: Document which labels were added to each chart.
Task 3: Apply Consistent Colour Palette (1 mark)
Requirements: Define a single colour palette and apply it consistently across all five charts.
Python approach:
# Define company colour palette
PALETTE = {
    'primary': '#1f77b4',      # Blue
    'secondary': '#ff7f0e',    # Orange
    'success': '#2ca02c',      # Green
    'warning': '#d62728',      # Red
    'neutral': '#7f7f7f'       # Gray
}

CHART_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Apply to all charts
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for idx, (ax, color) in enumerate(zip(axes.flat, CHART_COLORS)):
    ax.bar(categories, values, color=color)
    ax.set_title(f'Chart {idx+1}', fontsize=12, fontweight='bold')

plt.suptitle('Quarterly Performance Overview', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('output/dashboard_consistent_colors.png', dpi=300)
Validation: All five charts use colours from the same palette. Document the palette and why each colour was chosen.
Task 4: Annotate Key Insights (1 mark)
Requirements: Add at least one annotation to each chart marking an anomaly, threshold, or important event.
Annotation example:
fig, ax = plt.subplots(figsize=(12, 6))

# Plot trend
ax.plot(df['date'], df['revenue'], marker='o', linewidth=2, color='#1f77b4')

# Annotate a spike or drop
important_date = df.loc[df['revenue'].idxmax(), 'date']
max_revenue = df['revenue'].max()
ax.annotate(
    'Peak Sales\n($5.2M)',
    xy=(important_date, max_revenue),
    xytext=(important_date, max_revenue + 500000),
    arrowprops=dict(arrowstyle='->', color='red', lw=2),
    fontsize=11,
    ha='center',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7)
)

# Add a reference line (e.g., target)
target_revenue = 4500000
ax.axhline(y=target_revenue, color='green', linestyle='--', linewidth=2, label='Target')

ax.set_title('Monthly Revenue with Key Events Marked', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
Validation: Each chart includes at least one annotation. Document what each annotation marks and why it matters.
Task 5: Export and Document All Charts (1 mark)
Requirements: Save all charts as image files in a dedicated output folder with a README explaining each.
File structure:
output/
├── chart1_revenue_by_product.png
├── chart2_revenue_trend.png
├── chart3_order_value_distribution.png
├── chart4_revenue_composition.png
├── chart5_marketing_vs_revenue.png
└── CHARTS_README.md
CHARTS_README.md example:
# Analysis Visualizations

## Chart 1: Revenue by Product Line
- **Type:** Horizontal bar chart
- **Question:** Which product line generates the most revenue?
- **Key Insight:** Product A dominates with 45% of total revenue
- **Annotation:** None (clear comparison)

## Chart 2: Revenue Trend
- **Type:** Line chart with multiple series
- **Question:** How has revenue changed over the last 12 months?
- **Key Insight:** Steady growth except dip in August (seasonal)
- **Annotation:** Marked the August dip, explained by summer slowdown

## Chart 3: Order Value Distribution
- **Type:** Histogram with bins
- **Question:** What is the typical order value range?
- **Key Insight:** Bimodal distribution (small orders $20-$100, large orders $400-$600)
- **Annotation:** Marked both peaks

## Chart 4: Revenue Composition
- **Type:** Stacked bar by quarter
- **Question:** Which product line drives growth?
- **Key Insight:** Product B growing, Product C declining
- **Annotation:** Arrow marking shift in composition

## Chart 5: Marketing vs Revenue
- **Type:** Scatter plot with trend line
- **Question:** Does marketing spend correlate with revenue?
- **Key Insight:** Moderate positive correlation (r=0.72)
- **Annotation:** Marked the outlier (high spend, low revenue)
Validation: All charts exported as 300dpi PNG files. README documents each.
Submission
Commit:
git add output/
git add assignment-35-visualizations.py
git commit -m "visualizations: create five chart types with consistent styling and annotations"
git push
Submit:
1. GitHub link to visualization output folder
2. Video (3-5 minutes) covering:
    * Each of the five chart types, why it was chosen for that data
    * How labels, axes, and legends ensure clarity
    * Consistent colour palette and why consistency matters
    * Annotations added and what insights they highlight
    * Accessibility considerations (colour blindness)
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.46
Interactive Plotly Chart Design

Hey Interactive Chart Builder!
Welcome. Static charts communicate findings. Interactive charts let stakeholders explore findings themselves. Plotly gives you hover tooltips that reveal detail on demand, dropdown filters that switch between views, zoom that lets users drill into regions of interest, and pan that lets them navigate large datasets. This lesson teaches you to build charts that respond to human curiosity instead of limiting it.
Every static chart that made a stakeholder ask "can you filter this for Q3?" or "can I zoom into January?" or "what is the exact value of that point?" was a chart that should have been interactive. Static charts answer one question. Interactive charts answer the question and the ten follow-up questions that come after. This lesson teaches you to build with Plotly - the library that makes interactivity the default.
The Real Scenario
THE PROBLEM
An analyst builds a revenue chart in matplotlib. The stakeholder sees a spike in March and asks "what was the exact revenue that day?" The analyst must go back to the data, look it up, and respond later. The stakeholder then asks "can you show me just Q1?" Another round trip. Then "can you compare it to last year?" Another chart. Every question requires the analyst to regenerate the chart. The analyst becomes a chart-generation service instead of a strategic analyst.
THE SOLUTION
Build the chart in Plotly. Hover reveals exact values. Click and drag zooms into any date range. A dropdown lets the viewer switch between revenue, profit, and order count. The stakeholder explores independently. The analyst focuses on the next analysis instead of re-rendering charts. Interactive charts scale communication - build once, answer many questions.
Hover Tooltips: Detail on Demand
The Most Powerful Feature You Will Use Every Day
What hover tooltips do
When a user hovers over a data point, a tooltip appears showing detailed information. On a revenue trend chart, hovering over a point reveals the exact date, revenue amount, order count, and any other metrics you include. The chart surface stays clean - no data labels cluttering the view - but full detail is available on demand. This is progressive disclosure applied to data visualisation.
Custom hover templates in Plotly
import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(
  x=df['date'],
  y=df['revenue'],
  mode='lines+markers',
  hovertemplate=(
      '<b>%{x|%Y-%m-%d}</b><br>'
      'Revenue: $%{y:,.0f}<br>'
      '<extra></extra>'
  ),
  line=dict(color='#1f77b4', width=2),
  marker=dict(size=8)
))

fig.update_layout(
  title='Daily Revenue Trend',
  xaxis_title='Date',
  yaxis_title='Revenue ($)',
  hovermode='x unified',
  height=500
)
The hovertemplate controls exactly what appears. %{x|%Y-%m-%d} formats dates. %{y:,.0f} formats numbers with commas. <extra></extra> removes the default trace name box.
Multi-field hover tooltips
You can include data fields in the tooltip that are not on the axes. For a bar chart of revenue by product, the hover tooltip can also show order count, average order value, and year-over-year change. This lets the chart serve multiple analytical needs without additional charts. Include 3-5 fields maximum in a tooltip - more than that becomes hard to scan.
You just learned how to create custom hover tooltips that show exactly the information users need. Now you will learn how dropdown filters let users switch between different views of the same data without reloading.
Dropdown Filters: Multiple Views, One Chart
Let Users Choose What They See Without Rebuilding Charts
What dropdown filters enable
A single chart can display revenue, profit, or order count - toggled by a dropdown menu. All data is loaded once. The dropdown switches which trace is visible. No page reload. No server request. Instant switch. This is powerful for dashboards where stakeholders want to explore multiple metrics in the same spatial context (same products, same time axis, different metric).
Building a dropdown with updatemenus
fig = go.Figure()

# Add all traces - only first visible initially
fig.add_trace(go.Bar(x=products, y=revenue, name='Revenue',
  marker=dict(color='#1f77b4'), visible=True))
fig.add_trace(go.Bar(x=products, y=profit, name='Profit',
  marker=dict(color='#ff7f0e'), visible=False))
fig.add_trace(go.Bar(x=products, y=orders, name='Orders',
  marker=dict(color='#2ca02c'), visible=False))

fig.update_layout(
  updatemenus=[dict(
      active=0,
      buttons=[
          dict(label='Revenue', method='update',
               args=[{'visible': [True, False, False]},
                     {'title': 'Revenue by Product'}]),
          dict(label='Profit', method='update',
               args=[{'visible': [False, True, False]},
                     {'title': 'Profit by Product'}]),
          dict(label='Orders', method='update',
               args=[{'visible': [False, False, True]},
                     {'title': 'Orders by Product'}])
      ]
  )]
)
Each button sets which traces are visible and updates the title. Data is preloaded - switching is instant.
You just learned how to build dropdown filters that switch between metrics instantly. Now you will learn zoom, pan, and date range interactions that let users explore data at any granularity.
Zoom, Pan, and Date Range Selection
Navigate Data Like a Map - Zoom In, Zoom Out, Pan Around
Built-in Plotly interactions
Plotly charts include zoom and pan by default. Click and drag selects a region to zoom into. Double-click resets to the original view. Shift+drag pans the view. These interactions are free - you do not need to write code for them. They let users explore a full year of daily data, zoom into one week that looks interesting, then double-click to return to the overview. This is the explore-then-focus workflow that analysts naturally follow.
Date range selectors for time-series charts
fig.update_xaxes(
  rangeselector=dict(
      buttons=list([
          dict(count=1, label='1M', step='month', stepmode='backward'),
          dict(count=3, label='3M', step='month', stepmode='backward'),
          dict(count=6, label='6M', step='month', stepmode='backward'),
          dict(count=1, label='YTD', step='year', stepmode='todate'),
          dict(step='all', label='All')
      ])
  ),
  rangeslider=dict(visible=True)
)
Buttons let users jump to predefined periods (Last Month, Last Quarter, YTD). The range slider at the bottom lets users drag to select any custom date range. Both work together for maximum flexibility.
You just learned how to leverage Plotly's built-in zoom, pan, and date range selection. Now you will learn how to integrate Plotly charts into a Streamlit dashboard for full-stack interactive analytics.
Integrating Plotly With Streamlit
From Standalone Charts to Full Dashboard Applications
Embedding Plotly in Streamlit
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout='wide')
st.title('Sales Analytics Dashboard')

# Create figure
fig = go.Figure(data=go.Scatter(
  x=df['date'], y=df['revenue'],
  mode='lines+markers',
  hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
))
fig.update_layout(title='Revenue Trend', height=500)

# Display in Streamlit - full width
st.plotly_chart(fig, use_container_width=True)

# Sidebar filters work with Plotly
min_date = st.sidebar.date_input('Start Date')
max_date = st.sidebar.date_input('End Date')
st.plotly_chart embeds the interactive chart with all hover, zoom, and pan interactions preserved. Streamlit sidebar filters reload the data. Plotly handles the chart-level interactions.
Exporting interactive charts as HTML
Plotly charts can be saved as standalone HTML files using fig.write_html('chart.html'). The HTML file includes all data and the Plotly JavaScript library. Anyone can open it in a browser and interact - no Python, no server required. This is how you share interactive charts via email or static hosting.
You just learned how to integrate Plotly charts into Streamlit dashboards and export them as standalone HTML. Combined with hover tooltips, dropdown filters, and zoom interactions, you now have the complete interactive visualisation toolkit for modern analytics dashboards.

Interactive Plotly Chart Design


00h 59m 55s

Build interactive Plotly charts that enable stakeholders to explore data themselves. Create hover tooltips showing relevant data, dropdown filters to toggle between views, and zoom functionality for detailed exploration.
Task 1: Create Two Plotly Charts with Hover Tooltips (1 mark)
Chart 1 - Revenue Trend with Custom Hover
import plotly.graph_objects as go
import pandas as pd

df = pd.read_sql("""
    SELECT DATE(order_date) as date, SUM(amount) as revenue, COUNT(*) as order_count
    FROM orders
    GROUP BY DATE(order_date)
    ORDER BY DATE(order_date)
""", engine)

fig1 = go.Figure(data=go.Scatter(
    x=df['date'],
    y=df['revenue'],
    mode='lines+markers',
    hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                  'Revenue: $%{y:,.0f}<br>' +
                  '<extra></extra>',
    line=dict(color='#1f77b4', width=2),
    marker=dict(size=8)
))

fig1.update_layout(
    title='Daily Revenue Trend',
    xaxis_title='Date',
    yaxis_title='Revenue ($)',
    hovermode='x unified',
    height=500
)

fig1.write_html('chart1_revenue_trend.html')
Chart 2 - Product Performance with Multi-Column Hover
Create a bar chart showing revenue by product with hover showing revenue, order count, and average order value.
Requirements:
* Hover template shows 3+ data fields
* Custom formatting (currency for money, commas for counts)
* Readable and informative
Validation: Both charts render in browser with tooltips appearing on hover. Data is accurate.
Task 2: Create Dropdown Filter to Toggle Views (1 mark)
Requirements: Build a chart with a dropdown menu that switches between two metrics without reloading data.
import plotly.graph_objects as go

# Prepare data for 3 views: Revenue, Profit, Order Count
products = ['Product A', 'Product B', 'Product C', 'Product D']
revenue_data = [50000, 75000, 120000, 45000]
profit_data = [15000, 22000, 35000, 10000]
order_count = [1000, 1500, 2500, 800]

fig = go.Figure()

# Add all traces, initially hidden except first
fig.add_trace(go.Bar(
    x=products,
    y=revenue_data,
    name='Revenue',
    marker=dict(color='#1f77b4'),
    visible=True
))

fig.add_trace(go.Bar(
    x=products,
    y=profit_data,
    name='Profit',
    marker=dict(color='#ff7f0e'),
    visible=False
))

fig.add_trace(go.Bar(
    x=products,
    y=order_count,
    name='Order Count',
    marker=dict(color='#2ca02c'),
    visible=False
))

# Create dropdown menu
fig.update_layout(
    updatemenus=[dict(
        active=0,
        x=0.0,
        xanchor='left',
        y=1.15,
        yanchor='top',
        buttons=[
            dict(label='Revenue', method='update',
                 args=[{'visible': [True, False, False]},
                       {'title': 'Revenue by Product'}]),
            dict(label='Profit', method='update',
                 args=[{'visible': [False, True, False]},
                       {'title': 'Profit by Product'}]),
            dict(label='Order Count', method='update',
                 args=[{'visible': [False, False, True]},
                       {'title': 'Order Count by Product'}])
        ]
    )]
)

fig.update_layout(title='Product Performance', height=500)
fig.write_html('chart3_metric_selector.html')
Validation: Dropdown works without page reload. Correct metric displays for each button.
Task 3: Enable Zoom, Pan, and Reset Interactions (1 mark)
Requirements: Ensure charts support native Plotly interactions:
* Zoom: Click and drag to zoom into a region
* Pan: Shift+click+drag to move around
* Reset: Double-click to reset to original view
* Box or Lasso select: Select points by drawing
import plotly.graph_objects as go

# These interactions are enabled by default in Plotly
fig = go.Figure(data=go.Scatter(
    x=data['x'],
    y=data['y'],
    mode='markers',
    marker=dict(size=10)
))

# Verify interactions are enabled
fig.update_layout(
    dragmode='zoom',  # Options: 'zoom', 'pan', 'select', 'lasso', 'drawclosedpath'
    hovermode='closest',
    height=600
)

fig.write_html('chart4_interactive.html')

# Test: Open HTML in browser
# - Click and drag to zoom
# - Shift+drag to pan
# - Double-click to reset
# - Hover to see values
Validation: All interaction modes work without errors. Chart layout does not break with zoom.
Task 4: Integrate Plotly into Streamlit (1 mark)
Requirements: Show how to embed Plotly charts in a Streamlit dashboard.
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout='wide')

st.title('Interactive Sales Dashboard')

# Load data
df = pd.read_sql("SELECT * FROM orders LIMIT 1000", engine)

# Create Plotly figure
fig = go.Figure(data=go.Scatter(
    x=df['order_date'],
    y=df['amount'],
    mode='markers',
    hovertemplate='<b>%{x}</b><br>Order: $%{y:,.2f}<extra></extra>'
))

fig.update_layout(
    title='Orders Over Time',
    xaxis_title='Date',
    yaxis_title='Order Amount ($)',
    height=500
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add filters
st.sidebar.header('Filters')
min_amount = st.sidebar.slider('Min Order Amount', 0, 10000, 0)
filtered_df = df[df['amount'] >= min_amount]

st.write(f"Showing {len(filtered_df)} orders >= ${min_amount}")
st.dataframe(filtered_df[['order_date', 'customer_id', 'amount']])
Validation: Streamlit app runs without errors. Plotly charts display and respond to interactions.
Task 5: Answer Follow-Up Question (1 mark)
Question: You have a time-series Plotly chart showing revenue by week. You want to add a date range slider so users can select which weeks to view (e.g., "show me only Q1 2024"). How would you implement this in Plotly?
Expected answer components:
* Use rangeselector buttons (Last month, Last quarter, YTD)
* Or use rangeslider on x-axis for drag-to-select
* Show code example with at least one approach
* Explain when each approach is better
Submission
git add interactive_charts/
git add streamlit_app.py
git commit -m "plotly: interactive charts with hover, filters, zoom"
git push
Submit:
1. GitHub link with all HTML chart files
2. Video (3-5 minutes):
    * Demonstrate hover tooltips on two charts
    * Show dropdown filter switching between metrics
    * Show zoom/pan/reset interactions working
    * Show Streamlit integration
    * Answer follow-up on date range sliders
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.47
KPI Card & Summary Metric Design

Hey KPI Dashboard Designer!
Welcome. Charts show trends and patterns. But the first thing any executive, manager, or stakeholder looks at on a dashboard is the row of KPI cards at the top. Five numbers that answer "are we on track?" in five seconds. Each card shows a metric, its current value, how it changed from last period, and whether that change is good or bad. This lesson teaches you to design, compute, and display KPI cards that communicate business status at a glance.
Every dashboard that failed to get executive adoption had the same problem: it required scrolling, filtering, and thinking before the user could answer the simplest question - "how are we doing?" KPI cards solve this. They sit at the top of every dashboard and provide the instant answer. If all cards are green, the executive moves on confident. If one card is red, they scroll down to investigate. This lesson teaches you to build that top row correctly.
The Real Scenario
THE PROBLEM
A VP opens the sales dashboard. They see three line charts, two bar charts, and a data table. All show useful information. But the VP just wants to know: "Is revenue up or down this month?" They scan for 30 seconds, cannot find a clear answer, and send a Slack message to the analyst asking for a summary. The dashboard has every chart type but is missing the most important element - the summary numbers that answer "status" questions instantly.
THE SOLUTION
Add five KPI cards at the top of the dashboard. Revenue:45 ↑2.1%. Churn Rate: 5.2% ↓2.8% (green - down is good for churn). Satisfaction: 4.2/5 →0.3% (yellow - stable). The VP sees status in 5 seconds. Green means on track. Red means investigate. No scrolling, no filtering, no asking.
What Makes a Good KPI
Not Every Metric Is a KPI - Choose the Five That Matter Most
KPI selection criteria
A KPI must be: (1) Actionable - if it changes, someone should do something. Revenue drops, investigate why. (2) Measurable - it has a number, not a feeling. (3) Comparable - it can be compared to last period, last year, or a target. (4) Aligned - it connects to a business objective. Revenue connects to growth. Churn connects to retention. (5) Limited - maximum five KPIs per dashboard. More than five and none feel important.
NOT A KPI
"Number of database tables" - not actionable, not connected to business outcome. "Total records processed" - measures activity, not impact. "Average query time" - operational metric, not business KPI.
GOOD KPI
"Monthly Recurring Revenue" - actionable, measurable, comparable. "Customer Churn Rate" - directly tied to retention goal. "Net Promoter Score" - measures customer loyalty, drives strategy.
You just learned how to select KPIs that are actionable, measurable, comparable, aligned, and limited. Now you will learn how to compute these metrics with proper period-over-period comparison.
Computing KPI Metrics With Period Comparison
A Number Without Context Is Just a Number - Add the Comparison
The three components of a KPI card
Every KPI card displays three things: (1) Current value - the metric right now. "$5.2M" (2) Change indicator - how it changed from the prior period. "+12.5%" with an up arrow. (3) Status colour - green if on track, red if off track, yellow if flat. These three elements together tell the complete story: what the number is, whether it is improving, and whether you should worry.
Computing percentage change
import pandas as pd
from datetime import datetime

# Current period revenue
current_revenue = pd.read_sql("""
  SELECT SUM(amount) as total
  FROM orders
  WHERE MONTH(order_date) = MONTH(CURRENT_DATE)
    AND YEAR(order_date) = YEAR(CURRENT_DATE)
""", engine).iloc[0, 0]

# Prior period revenue
prior_revenue = pd.read_sql("""
  SELECT SUM(amount) as total
  FROM orders
  WHERE MONTH(order_date) = MONTH(CURRENT_DATE) - 1
    AND YEAR(order_date) = YEAR(CURRENT_DATE)
""", engine).iloc[0, 0]

# Calculate percentage change
change_pct = ((current_revenue - prior_revenue) / prior_revenue) * 100
print(f"Revenue: ${current_revenue:,.0f} ({change_pct:+.1f}%)")
Directional logic: when up is bad
Not all metrics improve by going up. Revenue up = good (green). Churn rate up = bad (red). Response time up = bad (red). Customer satisfaction up = good (green). Your KPI card logic must invert the colour for metrics where lower is better. This is a common implementation mistake: a dashboard showing churn increasing with a green arrow because the code treats all increases as positive.
def get_trend_indicator(change_pct, metric_name):
    """Return arrow and colour based on metric direction."""
    inverted_metrics = ['Churn Rate', 'Response Time', 'Error Rate']
    
    if metric_name in inverted_metrics:
        # Down is good for these metrics
        if change_pct < -2: return '↓', '#10b981'  # Green
        elif change_pct > 2: return '↑', '#ef4444'  # Red
        else: return '→', '#f59e0b'  # Yellow
    else:
        # Up is good for standard metrics
        if change_pct > 2: return '↑', '#10b981'  # Green
        elif change_pct < -2: return '↓', '#ef4444'  # Red
        else: return '→', '#f59e0b'  # Yellow
You just learned how to compute KPI metrics with period-over-period comparison and directional logic. Now you will learn how to display these KPIs in a dashboard layout that stakeholders scan instantly.
Displaying KPI Cards in Streamlit
Five Cards, One Row, Instant Status Check
Streamlit metric cards
import streamlit as st

st.set_page_config(layout='wide')
st.title('Sales Performance Dashboard')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
  st.metric(label='Revenue', value='$5.2M', delta='+12.5%')
with col2:
  st.metric(label='Active Users', value='2,500', delta='+5.2%')
with col3:
  st.metric(label='Avg Order Value', value='$45', delta='+2.1%')
with col4:
  st.metric(label='Churn Rate', value='5.2%', delta='-2.8%',
            delta_color='inverse')  # inverse: negative = green
with col5:
  st.metric(label='Satisfaction', value='4.2/5', delta='+0.3%')

st.divider()
# Detailed charts go below the KPI row
The delta_color='inverse' parameter is critical for churn and similar metrics. It tells Streamlit that a negative change should display green (good) instead of the default red.
Layout hierarchy: KPIs first, trends second, detail third
The dashboard structure follows the information pyramid from the dashboard architecture lesson. Top row: five KPI cards (Level 1 - Status). Middle section: trend charts showing how KPIs changed over time (Level 2 - Trends). Bottom section: segment breakdowns and filters (Level 3 - Segments). Below that: detailed data tables with export (Level 4 - Detail). This hierarchy matches how executives actually consume information.
You just learned how to display KPI cards in Streamlit and structure dashboards hierarchically. Now you will learn how to ensure KPI values come from validated data sources instead of hardcoded numbers.
Connecting KPIs to Validated Data Sources
KPI Values Must Come From Your Clean Data Layer - Never Hardcode
Query your views, not raw tables
KPI values should come from the SQL views and aggregated tables you built in the clean data layer. Revenue comes from vw_monthly_revenue. Active users comes from vw_active_customers. This ensures the dashboard uses the same metric definitions as every other tool. When the metric definition changes, the view is updated once and the KPI card automatically shows the new calculation.
Document data lineage for every KPI
For each KPI, document: (1) Which view or table it comes from. (2) The exact query used. (3) How the comparison period is calculated. (4) Whether the value was cross-validated against Python or another source. This documentation prevents future confusion about where numbers come from and makes debugging much faster when a KPI looks wrong.
KPI card design checklist
* Maximum 5 KPI cards per dashboard - each answering one business question
* Each card shows: current value, percentage change, trend direction
* Colour logic is correct: green for good, red for bad, yellow for flat
* Inverted metrics (churn, response time) show green when decreasing
* Values come from validated views or aggregated tables - never hardcoded
* Comparison period is automatic (not manually set dates)
* Data lineage documented for every KPI
You just learned how to design complete KPI cards with computed metrics, trend indicators, status colours, and validated data sources. KPI cards are the foundation of every executive dashboard - they answer "are we on track?" before any chart is ever viewed.
Common KPI Card Mistakes
Mistake 1: Too many KPIs
Showing 15 KPI cards makes none of them feel important. The human brain processes 5-7 items at a glance. More than 5 cards and the dashboard header becomes a wall of numbers instead of a status check. Pick the 5 that matter most. Put everything else in the trends or detail section.
Mistake 2: No comparison period
A KPI card showing "Revenue: $5.2M" with no comparison is meaningless. Is that good? Bad? Higher than last month? Lower than target? Always include either period-over-period change or comparison to target. Without context, the number is noise.
Mistake 3: Wrong directional colour
Showing churn rate increasing with a green arrow because "the number went up." For churn, error rate, and response time, increases are bad. Always implement directional logic that inverts the colour for metrics where lower is better. Test every card manually to verify the colour matches the business meaning.


KPI Card & Summary Metric Design


00h 59m 56s

Design a dashboard header with five KPI cards that communicate business status at a glance. Each card must show current value, trend direction, percentage change, and status color indicating whether the metric is on track.
Task 1: Compute Five KPI Metrics (1 mark)
Compute five meaningful KPIs with current value and prior period comparison:
1. Total Revenue - Sum of all orders this month vs last month
2. Active Users - Count of users with activity this month vs last month
3. Average Order Value - Mean order amount this month vs last month
4. Churn Rate - % of customers lost this month vs last month
5. Customer Satisfaction - Average rating this month vs last month
import pandas as pd

# Month-to-date metrics
current_month = datetime.now().month
current_year = datetime.now().year

# Revenue KPI
current_revenue = pd.read_sql("""
    SELECT SUM(amount) as total
    FROM orders
    WHERE MONTH(order_date) = %s AND YEAR(order_date) = %s
""", engine, params=[current_month, current_year]).iloc[0, 0]

prior_revenue = pd.read_sql("""
    SELECT SUM(amount) as total
    FROM orders
    WHERE MONTH(order_date) = %s AND YEAR(order_date) = %s
""", engine, params=[current_month - 1, current_year]).iloc[0, 0]

# Calculate change
revenue_change = ((current_revenue - prior_revenue) / prior_revenue) * 100 if prior_revenue > 0 else 0

# Repeat for other 4 KPIs
...

# Compile into DataFrame
kpis = pd.DataFrame({
    'Metric': ['Revenue', 'Active Users', 'AOV', 'Churn Rate', 'Satisfaction'],
    'Current': [current_revenue, current_users, current_aov, current_churn, current_satisfaction],
    'Prior': [prior_revenue, prior_users, prior_aov, prior_churn, prior_satisfaction],
    'Change_Pct': [revenue_change, users_change, aov_change, churn_change, satisfaction_change]
})

print(kpis)
Validation: All five metrics computed from clean data layer. No hardcoded values.
Task 2: Add Trend Indicators (Up/Down Arrows or Colors) (1 mark)
def get_trend_indicator(change_pct, metric_name):
    """
    Return arrow and color based on metric direction.
    Some metrics: up is good (revenue, aov, satisfaction)
    Some metrics: down is good (churn)
    """
    if metric_name == 'Churn Rate':
        # For churn: down is good
        if change_pct < -2:  # >2% decrease is good
            return '↓', '#10b981'  # Green
        elif change_pct > 2:  # >2% increase is bad
            return '↑', '#ef4444'  # Red
        else:
            return '→', '#f59e0b'  # Yellow
    else:
        # For other metrics: up is good
        if change_pct > 2:  # >2% increase is good
            return '↑', '#10b981'  # Green
        elif change_pct < -2:  # >2% decrease is bad
            return '↓', '#ef4444'  # Red
        else:
            return '→', '#f59e0b'  # Yellow

kpis['Trend'] = kpis.apply(
    lambda row: get_trend_indicator(row['Change_Pct'], row['Metric']),
    axis=1
)

print(kpis)
Validation: Trend indicators added. Colors are consistent.
Task 3: Display Percentage Change (1 mark)
kpis['Change_Display'] = kpis['Change_Pct'].apply(
    lambda x: f"{x:+.1f}%" if x != 0 else "0%"
)

# Example output:
# Metric          Current    Change_Display   Trend
# Revenue         $5.2M      +12.5%           ↑ (Green)
# Active Users    2500       +5.2%            ↑ (Green)
# AOV             $45        +2.1%            ↑ (Green)
# Churn Rate      5.2%       -2.8%            ↓ (Green)  <- Down is good for churn
# Satisfaction    4.2        +0.3%            → (Yellow)
Validation: Percentage changes calculated and formatted correctly.
Task 4: Design KPI Dashboard Layout (1 mark)
Create a Streamlit or HTML dashboard that displays five KPI cards at the top:
import streamlit as st

st.set_page_config(layout='wide')

st.title('Sales Performance Dashboard')

# Display KPI cards in columns
col1, col2, col3, col4, col5 = st.columns(5)

kpi_list = [
    {'name': 'Revenue', 'current': '$5.2M', 'change': '+12.5%', 'status': 'green'},
    {'name': 'Active Users', 'current': '2,500', 'change': '+5.2%', 'status': 'green'},
    {'name': 'AOV', 'current': '$45', 'change': '+2.1%', 'status': 'green'},
    {'name': 'Churn Rate', 'current': '5.2%', 'change': '-2.8%', 'status': 'green'},
    {'name': 'Satisfaction', 'current': '4.2/5', 'change': '+0.3%', 'status': 'yellow'}
]

columns = [col1, col2, col3, col4, col5]

for col, kpi in zip(columns, kpi_list):
    with col:
        st.metric(
            label=kpi['name'],
            value=kpi['current'],
            delta=kpi['change']
        )

st.divider()
st.subheader('Detailed Analytics')
# Add detailed charts below KPI row
Validation: KPI cards appear at top of dashboard. Colors and trends are clear. Layout is readable.
Task 5: Ensure Values Come From Validated Data (1 mark)
Document where each KPI value comes from. Show that values are computed from the clean data layer (views or aggregated tables), not hardcoded.
# KPI Computation Sources

## Revenue KPI
- **Source:** `vw_daily_revenue` view (SQL)
- **Query:** Sum of order_amount for current month
- **Validation:** Cross-checked with Python computation - values match

## Active Users KPI
- **Source:** `vw_active_users` view (SQL)
- **Query:** Count of users with login in last 30 days
- **Validation:** Cross-checked with Python - values match

[Same for other 3 KPIs]

All KPIs use validated views, not raw table queries.
All computations are date-based (not hardcoded values).
Prior period automatically calculated (no manual reference).
Validation: Documentation shows data lineage. All KPIs sourced from verified clean layer.
Bonus: Answer Follow-Up (Optional)
Question: When a new dataset is uploaded, the KPI values should automatically update without code changes. How would you design the KPI system to support this?
Expected answer: Reference the view/aggregated table name, not hard-coded date ranges. Schedule a daily refresh. Use parameters for date ranges. Show how a new dataset automatically flows through to updated KPIs.
Submission
git add kpi_dashboard.py
git add kpi_sources.md
git commit -m "kpi: design five metric cards with trend and status"
git push
Submit:
1. GitHub link to KPI code and documentation
2. Video (3-5 minutes):
    * Display the five KPI cards
    * Explain the business question each KPI answers
    * Show trend direction and color coding
    * Explain how percentage change is computed
    * Explain data sources for each KPI
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.48
Data Storytelling & Insight Narrative

Hey Data Storyteller!
Welcome. You have the analysis. You have the charts. You have the KPI cards. But none of that matters if the person reading your work cannot understand what it means and what to do about it. Data storytelling is the skill that turns analysis into action. It is the structure that connects "here is what the data shows" to "here is what we should do about it." This lesson teaches you to write analysis narratives that leadership reads, understands, and acts on.
Every analysis that was technically correct but never led to action failed at storytelling. The analyst produced charts and tables. Nobody read them. The findings sat in a notebook. The company kept doing the same thing. The problem was never the data - it was the communication. This lesson teaches you the narrative structure that makes analysis impossible to ignore.
The Real Scenario
THE PROBLEM
An analyst discovers that customer churn correlates strongly with support response time. They present 15 slides filled with scatter plots, regression coefficients, p-values, and confidence intervals. The VP of Operations nods politely, thanks the analyst, and does nothing. Three months later, churn is still rising. The insight was real. The recommendation was sound. But the communication buried the finding under technical detail that the audience could not parse. The story was never told.
THE SOLUTION
Structure the analysis as a narrative: Context (churn costs400K recovered). The VP reads this in 3 minutes, understands the problem, sees the solution, and approves the budget. Same data. Different structure. Different outcome.
The Five-Part Narrative Arc
Context → Data → Finding → Why → Action
1. Context
Why does this analysis exist? What business problem triggered it?
One paragraph. State the business problem in business terms. "Customer churn is the leading cause of revenue loss, costing us $2M annually. We need to understand root causes and identify solutions that engineering and operations can implement." This paragraph gives the reader a reason to keep reading.
2. Data
What did you examine? Scope the analysis so the reader knows the boundaries.
One paragraph. "We analyzed 50,000 customers over 24 months. Dataset includes subscription tier, support interactions, response times, and renewal status." This prevents the reader from wondering "but did you look at X?" because you explicitly stated what was included.
3. Finding
What did the data reveal? State findings with specific numbers.
3-5 bullet points with concrete numbers. "Customers with first response under 2 hours have 3% churn. Customers with response over 24 hours have 12% churn. The difference is 4x and explains 40% of churn variation." Specific numbers are persuasive. Vague statements are not.
4. Why
Why does this pattern exist? Explain the mechanism behind the numbers.
One paragraph. "We reviewed 100 churned customers. When help came fast, problems were resolved before frustration escalated. When help was slow, customers had already decided to leave before support responded." The why section transforms a correlation into a causal understanding that makes the recommendation obvious.
5. Action
What should we do? Specific, actionable, with expected impact.
3-5 recommendations with: what to do, who owns it, when, and expected impact. "Hire 2 support engineers (cost:400K in churn reduction). Implement 2-hour response SLA by Jan 1." If the reader cannot act on your recommendation without asking questions, it is not specific enough.
You just learned the five-part narrative arc that structures every data story. Now you will learn how to support each finding with evidence and eliminate jargon that blocks comprehension.
Supporting Findings With Evidence
Every Claim Needs a Chart, a Statistic, or a Concrete Example
Evidence structure for each finding
For every finding, provide: (1) The specific chart or number that proves it. "Churn rate by response time bucket: under 2 hours = 3%, 2-4 hours = 5%, 4-24 hours = 9%, over 24 hours = 12%." (2) Why this evidence is convincing. "The 4x difference between fastest and slowest response is consistent across all customer segments and all quarters." (3) What it means for the business. "This tells us exactly which operational change would reduce churn most."
WEAK EVIDENCE
"Churn seems to correlate with support quality." No numbers. No chart reference. No specificity. The reader cannot verify or act on this claim.
STRONG EVIDENCE
"Customers waiting over 24 hours for support churn at 12% vs 3% for customers served within 2 hours (Chart 2, p.4). This 4x difference holds across all segments."
You just learned how to support findings with specific evidence. Now you will learn how to eliminate technical jargon that blocks comprehension for business audiences.
Eliminating Jargon: Writing for Business Audiences
If Your Audience Cannot Understand It, It Does Not Exist
Translation patterns: technical to business
Every technical term has a business equivalent. Use the business version in narratives for leadership.
Technical: "p-value of 0.001"
Business: "The pattern is real and strong"
Technical: "AUC of 0.72"
Business: "Our model correctly identifies at-risk customers 72% of the time"
Technical: "R² explains 40% of variance"
Business: "Response time alone accounts for 40% of churn differences"
Technical: "Logistic regression coefficient"
Business: "For every hour of delay, churn risk increases by 2%"
The jargon test
Read your narrative aloud. Every time you use a word that your non-technical manager would not immediately understand, replace it. If you cannot explain it simply, you do not understand it well enough to communicate it. Technical detail belongs in an appendix, not in the narrative.
You just learned how to translate technical findings into business language. Now you will learn how to write recommendations that are specific enough to be acted on without follow-up questions.
Writing Actionable Recommendations
A Recommendation That Requires Follow-Up Questions Is Incomplete
The five elements of an actionable recommendation
Every recommendation must include: (1) What - the specific action. "Hire 2 support engineers." (2) Why - connected to your finding. "Current team averages 6-hour response; adding capacity reduces to under 2 hours." (3) Impact - quantified expected outcome. "Expected to reduce churn from 7% to 3%, recovering $400K annually." (4) Owner - who is responsible. "VP of Operations and HR." (5) Timeline - when it should happen. "Post job descriptions by Dec 1, hire by Jan 31."
VAGUE RECOMMENDATION
"We should improve support response times." Who? How? By when? What is the expected impact? This recommendation generates questions instead of action.
ACTIONABLE RECOMMENDATION
"Hire 2 support engineers (cost:400K in churn reduction. Owner: VP Ops. Timeline: hire by Jan 31."
Data storytelling writing rules
* Active voice: "We discovered" not "It was found"
* Specific numbers: "3% vs 12%" not "significantly higher"
* Business impact: "Recover $400K in revenue" not "reduce variance by 40%"
* Clear cause-effect: "When support is fast, customers stay. When slow, they leave."
* One finding per paragraph: Do not bury the lead
* No hedging: "We recommend" not "We believe it might be worth considering"
* Concrete examples: "A customer waited 18 hours and churned" illustrates better than statistics alone
You just learned how to write data narratives that drive action: structured with a five-part arc, supported by evidence, free of jargon, and ending with recommendations specific enough to execute without follow-up. This is the skill that turns analysts into strategic advisors.
Testing Your Narrative
The three-question test for narrative clarity
Share your narrative with someone outside your team - a peer, a mentor, or a friend. Ask them three questions: (1) What is the main finding? (2) What should we do about it? (3) Did anything confuse you? If they can answer the first two questions correctly after one read-through, your narrative works. If anything confused them, rewrite that section. Their confusion reveals your communication gaps. Document their feedback and show how it shaped your final version.
Read aloud before submitting
Reading your narrative aloud reveals problems invisible on screen: awkward phrasing, sentences that are too long, jargon that sounds natural in your head but confusing when spoken, and logical gaps where the story jumps without transition. If you stumble while reading aloud, your reader will stumble while reading silently. Smooth oral delivery indicates clear written communication.

Data Storytelling & Insight Narrative


00h 59m 56s

You have completed an analysis showing that customer churn correlates strongly with support response time. Now structure this into a narrative that makes it actionable for leadership - problem context, findings, anomalies, and recommended actions.
Task 1: Structure Analysis With Narrative Arc (1 mark)
Write the analysis as a structured narrative (500-750 words):
Section 1: Context (Problem Statement) Explain why this analysis matters. What is the business problem?
Example: "Customer churn is the leading cause of revenue loss, costing us $2M annually. We want to understand root causes and identify solutions that engineering and operations can implement."
Section 2: Data Summary (What You Examined) Scope the analysis clearly so readers understand what data you looked at.
Example: "We analyzed 50,000 customers over 24 months. Dataset includes subscription tier, support interactions, response times, and renewal status."
Section 3: Key Findings (The Answer) State findings clearly and with specificity.
Example: "Customers with first response < 2 hours have 3 percent churn. Customers with <24 hour first response have 12% churn. The difference is statistically significant and explains 40% of churn variation."
Section 4: Anomaly Investigation (Why Is This Happening?) Dig deeper. What explains the pattern?
Example: "We reviewed 100 churned customers. Common theme: they needed help quickly. When help came fast, problems were resolved before customer frustration escalated. When help was slow, customers had already decided to leave."
Section 5: Recommendations (What Should We Do?) Propose specific, actionable steps.
Example: "We recommend: (1) Hire 2 additional support engineers (cost: $200K/year), (2) Implement response time SLA of <2 hours (currently average is 6 hours), (3) Track response time as leading indicator of churn."
Validation: Narrative is self-contained, readable, and structured. Written for business audience, not data team.
Narrative structure checklist:
* Context paragraph explains business problem (1 paragraph)
* Data summary section scopes analysis (1 paragraph)
* Findings are specific with numbers (3-5 bullets)
* Anomaly section explains why pattern exists (1 paragraph)
* Recommendations are actionable with expected impact (3-5 bullets)
* No technical jargon used
* Total length: 500-750 words
Task 2: Support Each Finding With Data (1 mark)
For each finding, provide:
* The specific chart or statistic that supports it
* Why this evidence matters
## Finding: Support Response Time Correlates With Churn

**Supporting Evidence:**
- Chart 1: Scatter plot showing response time (X) vs churn rate (Y). Clear downward trend visible. Correlation coefficient: -0.65 (statistically significant p<0.001).
- Chart 2: Churn rate by response time bucket:
  - <2 hours: 3% churn
  - 2-4 hours: 5% churn
  - 4-24 hours: 9% churn
  - >24 hours: 12% churn
- Stat: "Customers with >24hr response time are 4x more likely to churn"

**Why It Matters:**
This is not theoretical - the pattern is strong, consistent, and actionable. It tells us exactly which operational change (faster response) would reduce churn most.
Validation: Each finding includes specific evidence and context.
Task 3: Minimize Jargon, Maximize Clarity (1 mark)
Rewrite any technical language into business language:
Anti-pattern (Too technical): "We performed logistic regression with response time as primary predictor and churn as outcome variable. The model achieved 0.72 AUC with p less than 0.001 significance."
Pattern (Business language): "We built a model that predicts which customers will churn. Response time is the strongest predictor. The model is 72% accurate, meaning we can confidently identify at-risk customers based on how fast we respond to their support requests."
Requirements:
* No mention of "p-values", "AUC", "logistic regression" to business audience
* Use plain English: "The pattern is real and strong" instead of "statistically significant"
* Focus on business impact: "We can prevent $400K in churn" instead of "Model explains 40% of variance"
Validation: Narrative contains zero unexplained technical jargon.
Task 4: Create Three Actionable Recommendations (1 mark)
For each recommendation, provide:
* What to do (specific action)
* Why it will work (based on your findings)
* Expected impact (quantified if possible)
* Owner (who should do it)
* Timeline (when)
## Recommendation 1: Hire 2 Support Engineers
**Action:** Open recruitment for 2 additional support specialists, targeting Q1 2024 start dates.
**Why:** Current team averages 6-hour response time. Adding capacity reduces to <2 hours target.
**Impact:** Based on historical data, reducing response time to <2 hours should reduce churn from current 7% to ~3%, recovering $400K in annual revenue.
**Owner:** VP of Operations + HR
**Timeline:** Post job descriptions by Dec 1, hire by Jan 31, fully productive by Apr 1

## Recommendation 2: Implement Response Time SLA
**Action:** Document support response time SLA (<2 hours for tier-1 issues) and track as daily metric.
**Why:** Measurement creates accountability. Teams prioritize what they measure.
**Impact:** SLA tracking should reduce average response time by 1-2 hours within 30 days.
**Owner:** VP of Operations
**Timeline:** Document SLA by Dec 15, implement tracking by Jan 1

## Recommendation 3: Route High-Value Customers to Priority Queue
**Action:** Implement priority routing for customers spending >$10K/year to dedicated support lane.
**Why:** High-value customers are most sensitive to poor support. Protecting them protects revenue.
**Impact:** Should reduce high-value customer churn by 50% within 60 days.
**Owner:** CTO + VP of Operations
**Timeline:** Scoping complete by Dec 20, implementation by Feb 1
Validation: Recommendations are specific, tied to findings, and include expected impact.
Task 5: Write Narrative as Self-Contained Document (1 mark)
Create a standalone markdown file that can be read without running code or viewing charts.
# Customer Churn Analysis: Executive Summary

## The Problem
Churn is costing us $2M annually. We need to understand why customers leave and identify solutions.

## What We Examined
Analysis of 50,000 customers over 24 months including support interactions and renewal status.

## What We Found
Customers receive support within 2 hours: 3% churn
Customers receive support within 24 hours: 9% churn  
Customers wait >24 hours: 12% churn

The pattern is clear and strong. Support speed directly impacts churn.

## Why This Is Happening
We reviewed 100 churned customers. When support was fast, problems were solved before frustration. When support was slow, customers had already decided to leave.

## What We Recommend
1. Hire 2 support engineers (recover $400K annually)
2. Implement <2 hour response SLA (creates accountability)
3. Prioritize high-value customers (protect highest revenue)

## Next Steps
Operations team meets Dec 15 to plan hiring and SLA implementation.
Validation: Document is readable standalone. No jargon. Clear recommendations.
Task 6: Test Narrative Clarity (1 bonus mark)
Share the narrative with someone outside your team (peer, mentor, family member). Ask them:
1. What is the main finding in this analysis?
2. What should we do about it?
3. Did anything confuse you?
Document their feedback and show how their confusion shaped final edits.
Tips For Strong Narrative Writing
Use active voice: "We discovered" not "It was found" Specific numbers: "3% vs 12%" not "significantly higher" Business impact: "Recover $400K in revenue" not "reduce variance by 40%" Clear cause-effect: "When support is fast, customers stay. When support is slow, they leave." One finding per paragraph: Do not bury the lead Logical progression: Context → Data → Finding → Why → Action No hedging: "We believe" not "It appears that possibly." Concrete examples: "A customer waited 18 hours for support and churned" illustrates better than statistics alone
Submission
git add analysis_narrative.md
git add supporting_evidence/
git add feedback_and_edits.md
git commit -m "storytelling: structure churn analysis as actionable narrative"
git push
Submit:
1. GitHub link to narrative document and supporting evidence
2. Video (3-5 minutes):
    * Read the narrative aloud (audio version of the story)
    * Explain the problem and why it matters (context)
    * Show evidence supporting each finding
    * Explain the anomaly - why is churn linked to support?
    * Walk through recommendations and expected impact
    * Explain how you wrote for business audience, not data team
    * Share feedback you received and how you incorporated it
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.49
Executive Reporting & Stakeholder Communication

Hey Executive Communicator!
Welcome. You wrote the full analysis narrative. Now comes the hardest communication challenge: compressing it into one page that an executive reads in 3 minutes and makes a decision. Executives do not read 10-page reports. They read one-page summaries and decide whether to read more. This lesson teaches you to write executive summaries that get budget approved, strategies adopted, and recommendations implemented.
Every analyst who presented a 30-slide deck to a C-suite executive and watched them flip to the last slide for the recommendation learned this lesson the hard way: executives read the conclusion first. If the conclusion is clear, compelling, and backed by evidence, they act. If it requires reading 29 preceding slides to understand, they defer. This lesson teaches you to lead with the answer and make everything else optional reading.
The Real Scenario
THE PROBLEM
The data team completes a churn analysis. The full report is 15 pages with methodology, charts, statistical tests, and recommendations. The CEO has 5 minutes before the next meeting. They open the document, see 15 pages, scan the first paragraph about "logistic regression methodology", close the document, and reply "can someone give me the summary?" The analysis was thorough. But the communication format did not match the audience. The CEO needed a one-page executive summary that was never written.
THE SOLUTION
Create two documents: (1) A one-page executive summary with situation, findings, risks, recommendations, and decision requested. 300-400 words. No jargon. No methodology. Pure business impact. (2) A technical appendix with full methodology, charts, and statistical detail - available for anyone who wants to verify the work. The executive summary stands alone. The technical appendix is optional reading.
The Executive Summary Structure
Six Sections, One Page, Three Minutes to Decision
Situation
2-3 sentences. What is happening and why it matters.
"Customer churn is our leading revenue loss driver, costing $2M annually. Current churn rate is 7% vs industry average of 4%. We analyzed root causes and identified a high-impact opportunity." This tells the executive why they should care.
Key Findings
3 bullet points. Specific numbers. No methodology.
"Support speed directly impacts retention: 3% churn at 2hrs vs 12% at 24hrs (4x difference). Current team averages 6-hour response. High-value customers are most sensitive." Each finding is one line. Each has a number.
Business Risks
What happens if we do nothing? Quantify the cost of inaction.
"At current 7% churn, we lose $2M annually. Support ticket volume is up 40% YoY while response times degrade. Without action, churn will worsen." Risks create urgency. Executives act on risk faster than on opportunity.
Recommendations
3 specific actions with cost, expected impact, and timeline.
"(1) Hire 2 support engineers, cost400K, ROI 2x in year 1. (2) Implement 2-hour response SLA, cost50K engineering, timeline Feb 1." Each recommendation includes cost and return.
Decision Needed
One sentence. What approval is requested?
"Approve hiring budget (50K) by Dec 15." This is the call to action. Without it, the executive reads, nods, and does nothing because no specific decision was requested.
Next Steps
Who does what by when? Make the path forward obvious.
"Operations reviews hiring plan: Dec 15. Finance approves budget: Dec 20. Hiring begins: Jan 1. New hires productive: Apr 1." This eliminates ambiguity about what happens after the decision is made.
You just learned the six-section executive summary structure. Now you will learn how to identify and present business risks that create urgency for action.
Presenting Business Risks
Executives Act on Risk Faster Than on Opportunity
Risk structure: What, Why It Matters, Action
For each risk, state: (1) What the risk is - specific and quantified. "7% churn =400K." This structure converts abstract concern into concrete action.
Quantifying the cost of inaction
The most powerful sentence in an executive summary is "doing nothing costs $X per year." This reframes the recommendation from "we want to spend money" to "we are already losing money, and this investment stops the loss." When the cost of inaction exceeds the cost of action, the decision becomes obvious. Always calculate and present the cost of the status quo.
You just learned how to present business risks with quantified impact. Now you will learn how to adapt the same message for different audiences.
Adapting Communication for Different Audiences
Same Data, Different Message, Different Audience
For the CEO: focus on ROI and strategic risk
"Support delays cost250K in faster response recovers $400K in year 1. Approve budget by Dec 15?" One paragraph. Financial framing. Strategic decision. No operational detail.
For the VP of Engineering: focus on technical implementation
"Current response time averages 6 hours. Target is under 2 hours. This requires: queue prioritisation routing logic, response time tracking dashboard, and 2 additional support FTEs. Here is the implementation plan and technical requirements." Two paragraphs. Technical framing. Implementation detail. Timeline for engineering milestones.
For the Support Team: focus on how this improves their work
"We are hiring 2 additional team members to reduce your workload. New SLA target is 2-hour response. You will receive priority routing tools to help manage high-value customers efficiently. Training begins Feb 1." Two paragraphs. People framing. Focus on support and tools. Empathetic tone.
The core principle: same finding, different emphasis
The data does not change. The analysis does not change. Only the framing changes based on what the audience cares about. CEO cares about money and risk. Engineering cares about implementation and feasibility. Support team cares about workload and tools. Professional communication means adjusting emphasis without changing substance.
You just learned how to adapt the same analysis for different audiences without changing substance. Now you will learn how to separate the executive summary from the technical appendix so both serve their purpose.
Separating Executive Summary From Technical Appendix
Two Documents, Two Purposes, Two Audiences
EXECUTIVE SUMMARY
300-400 words. One page. Situation, findings, risks, recommendations, decision needed, next steps. No methodology. No technical terms. No charts (or at most one key chart). Written for decision-makers who read it in 3 minutes.
TECHNICAL APPENDIX
Unlimited length. Data sources and validation. Statistical methodology (regression, cohort analysis). All supporting charts and tables. Model assumptions and limitations. Written for data team members who need to verify or reproduce the work.
Executive summary quality checklist
* One page maximum (300-400 words)
* Title clearly states the topic
* Situation paragraph explains why this analysis matters
* Key findings are bulleted and specific (numbers, not vague)
* Business risks are quantified ("$2M/year" not "significant")
* Recommendations are specific and actionable with cost and ROI
* Each recommendation tied directly to a finding
* Decision needed is stated explicitly
* Next steps include who, what, and when
* Zero technical jargon
* No hedging language ("might", "possibly", "we believe")
* Read aloud once - should sound natural and conversational
You just learned how to create executive summaries that drive decisions, present business risks that create urgency, adapt communication for different audiences, and separate executive communication from technical documentation. This is the professional communication skill that turns data analysts into strategic advisors who shape business decisions.
The Read-Aloud Test and Final Quality Check
Before sending an executive summary, read it aloud once
If you stumble on a sentence, the reader will stumble too. If a paragraph feels long when spoken, it is too long when read. If you cannot explain a recommendation without adding words, the recommendation is not specific enough. Smooth oral delivery is the best proxy for clear written communication. This 3-minute test catches more problems than an hour of re-reading silently.
The ultimate test: would the reader act without asking a question?
After reading your one-page summary, can the executive approve the budget, assign owners, and set timelines without a follow-up meeting? If yes, your communication succeeded. If they need to ask "how much does this cost?" or "who is responsible?" or "when do we start?" - the information was missing. A complete executive summary makes the follow-up meeting unnecessary. That is the standard to aim for.

Executive Reporting & Stakeholder Communication


00h 59m 55s

You have completed detailed churn analysis (findings, recommendations, technical validation). Now create an executive summary suitable for leadership - one page, non-technical, focused on business impact and decisions needed.
Task 1: Write One-Page Executive Summary (1 mark)
Target length: 300-400 words
Structure:
# CHURN REDUCTION INITIATIVE
## Executive Summary

### Situation
Customer churn is our leading revenue loss driver, costing $2M annually. Current churn rate is 7% vs industry average of 4%. We analyzed root causes and identified a high-impact opportunity.

### Key Findings
- **Finding 1:** Support speed directly impacts retention. Customers receiving support within 2 hours churn at 3%. Customers waiting >24 hours churn at 12% (4x difference).
- **Finding 2:** Current support team averages 6-hour response time. This is our primary retention bottleneck.
- **Finding 3:** High-value customers (>$10K annual spend) are particularly sensitive to support speed. They churn at 15% when support is slow.

### Business Risks  
- **Revenue at Risk:** At current 7% churn, we lose $2M annually. High-value customer segment is especially vulnerable.
- **Competitive Vulnerability:** Better-supported competitors are recruiting our dissatisfied customers.
- **Trend:** Support ticket volume is up 40% YoY while response times have degraded. Without action, churn will worsen.

### Recommendations
1. **Hire 2 Support Engineers** (Cost: $200K/year)
   - Reduces average response time from 6 hours to <2 hours
   - Expected impact: Recover $400K in churn reduction
   - ROI: 2x within first year

2. **Implement Response Time SLA** (Cost: $0)
   - Document <2 hour target and track daily
   - Creates accountability and prioritization
   - Implementation: Jan 1

3. **Prioritize High-Value Customers** (Cost: $50K engineering)
   - Route $10K+/year customers to dedicated support lane
   - Expected impact: Reduce high-value churn by 50%
   - Timeline: Feb 1

### Decision Needed
Approve hiring budget ($200K) and engineering resources ($50K) by Dec 15. Projected ROI: $400K churn reduction in year 1.

### Next Steps
- Operations team reviews hiring and SLA plan: Dec 15
- Finance approves budget: Dec 20
- Hiring begins: Jan 1
- New hires productive: Apr 1
Validation: One page, self-contained, non-technical, clear decisions requested.
Task 2: Identify and Describe Business Risks (1 mark)
For the analysis, identify 3+ risks and explain business impact:
## Risk Analysis

### Risk 1: Revenue Loss From Churn
- **What:** 7% churn = $2M annual revenue loss
- **Why It Matters:** This is our largest preventable revenue leak
- **Action:** Support speed improvements can reduce to 3%, recovering $400K

### Risk 2: High-Value Customer Vulnerability  
- **What:** Our largest customers (top 20%) churn at 15% vs 7% average
- **Why It Matters:** Losing one $500K customer = 1 year of savings from hiring
- **Action:** Dedicated support lane protects highest-value relationships

### Risk 3: Competitive Disadvantage
- **What:** Better-supported competitors are recruiting our customers
- **Why It Matters:** Once a customer leaves, getting them back costs 5x the retention investment
- **Action:** Fast response times become competitive moat

### Risk 4: Operational Burnout
- **What:** Support team response times degrading despite more hiring - sign of burnout
- **Why It Matters:** Overworked teams make mistakes, further degrading customer experience
- **Action:** Hiring addresses root cause, not symptom
Validation: Risks clearly stated. Business impact quantified where possible.
Task 3: Connect Recommendations to Findings (1 mark)
Show that each recommendation directly addresses a finding:
## Recommendation Justification

| Finding | Risk | Recommendation | How It Helps |
|||--|--|
| Support speed impacts churn (3% at 2hrs vs 12% at 24hrs) | Losing $2M to slow support | Hire 2 engineers, cut response time to <2hrs | Reduces churn from 7% to 3%, recovers $400K |
| High-value customers churn 15% when support is slow | Losing largest customers first | Prioritize high-value in support queue | Reduces high-value churn 50%, protects $10M revenue |
| Team is degrading despite headcount growth (burnout signal) | Quality declining, attrition risk | Hire engineers to reduce per-person load | Improves both customer and employee experience |
| Current avg response time is 6 hours (target <2) | Missing customer satisfaction window | Implement response time SLA and tracking | Creates accountability, drives process improvement |

Each recommendation maps to a specific finding and quantified risk.
Validation: Recommendations clearly justified by findings. Cause-effect chain is clear.
Task 4: Format for Clear Distinction From Technical Section (1 mark)
Create two separate documents:
Document 1: executive_summary.md (1 page, 300-400 words)
* Situation, findings, risks, recommendations, next steps
* Non-technical language
* No methodology, no model details, no equations
* Focus on business impact
Document 2: technical_analysis.md (detailed appendix, optional reading)
* Data source and validation
* Statistical methodology (correlation analysis, cohort analysis)
* Model validation and assumptions
* All 20+ supporting charts
* Regression results, p-values, AUC scores
Executive summary stands alone. Technical appendix is optional for those who want to dig into methodology.
Validation: Two documents clearly separated. Executive summary is readable without technical section.
Task 5: Answer Follow-Up Question (1 mark)
Question: Your audience changes from CEO (focused on ROI and risk) to VP of Engineering (focused on technical implementation). How would you adjust the communication?
Expected answer components:
* CEO version: "Support delays cost400K. Approve budget?"
* Engineering version: "Current response time is 6 hours. Target response time below 2 hours requires queue prioritization (routing logic), dashboards (metrics tracking), and staffing (2 FTE). Here is implementation plan."
* Same data, different emphasis (business impact vs technical feasibility)
* Different level of detail (one-page for CEO, technical design doc for engineering)
Task 6: Practice Adjusting For Different Audiences (1 bonus mark)
Rewrite your executive summary twice:
Version A: For Board of Directors Focus on strategic risk and shareholder value. Include only financial metrics. One paragraph max.
Version B: For Operations Team Focus on implementation details and timeline. Include process changes needed. Two paragraphs max.
Version C: For Support Team Focus on how this improves their work environment. Include staffing plan and support they will receive. Two paragraphs max.
Show that the same finding becomes different messages for different audiences. This is professional communication.
Writing Quality Checklist
Before submitting, verify:
*  One page (300-400 words)
*  No technical jargon
*  Every recommendation tied to a specific finding
*  Clear decision needed (what approval is requested?)
*  Formatted distinctly from technical analysis
*  Business impact quantified ($ or % where possible)
*  Next steps clearly stated
*  Read aloud once - smooth delivery indicates clarity
Quality Checklist For Executive Summaries
Before submitting, verify your summary meets these criteria:
*  One page maximum (300-400 words)
*  Title clearly states the topic
*  Situation paragraph explains why this analysis matters
*  Key findings are bulleted and specific (numbers, not vague)
*  Business risks are quantified ("$2M/year" not "significant")
*  Recommendations are specific and actionable
*  Each recommendation tied directly to a finding
*  Next steps clearly stated (who does what by when)
*  No technical language (no p-values, no model names, no jargon)
*  Read aloud once - should sound natural and conversational
*  No hedging language ("might", "possibly", "we believe")
*  Strong recommendations ("Do this" not "Consider possibly studying")
*  Formatted distinctly from technical analysis
Submission
git add executive_summary.md
git add technical_analysis.md
git add audience_versions_A_B_C.md
git commit -m "executive-reporting: one-page summary for business decision-making"
git push
Submit:
1. GitHub link to both documents
2. Video (3-5 minutes):
    * Present the one-page executive summary
    * Explain why each section matters for decision-making
    * Identify and describe the business risks
    * Connect recommendations to findings
    * Answer follow-up on adjusting message for different audiences
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

Insight Export & Report Generation

Hey Report Automation Expert!
Welcome. Analysis lives in notebooks and dashboards. But stakeholders need portable outputs: Excel datasets, PDF reports, HTML summaries they can download, save, share. This lesson teaches you to export analytical output in formats stakeholders understand - CSV for data, PDF for reports, HTML for interactive sharing - and to automate this process so new reports generate on schedule without manual work.
Every analysis that was never acted on because stakeholders could not download the results, that was lost when a dashboard went down, or that required an analyst to regenerate it manually every week failed at export strategy. This lesson teaches you to build export pipelines that deliver insights to stakeholders reliably and automatically.
The Real Scenario
THE PROBLEM
An analyst finishes a weekly churn report. The data lives only in a Streamlit app. A business partner asks "can you send me the cleaned dataset and the summary?" The analyst must manually export to CSV. The report is in markdown - the partner wants PDF. The visualizations are Plotly - the partner needs static images. Manual work multiplies. This happens every week. The analyst spends more time exporting than analyzing.
THE SOLUTION
Build automated export functions that generate CSV, PDF, and HTML at the push of a button (or on a schedule). One command produces cleaned data, summary report, and visualizations in multiple formats. Stakeholders download what they need. Analysts focus on analysis, not manual exports.
Designing For Multiple Output Formats
Three Output Formats Every Analysis Needs
1. Cleaned CSV Dataset
The raw data output. Enable stakeholders to do their own analysis in Excel. Include metadata: source, refresh date, record count, data dictionary.
2. PDF Summary Report
Executive summary + key findings. Portable, shareable, suitable for email and meetings. No interactivity - all insights are baked in.
3. HTML Interactive Report
Full analysis with interactive Plotly charts. Stakeholders explore in browser. Can be emailed as single file or hosted on intranet.
Automating Export With Reusable Functions
Write Once, Export Everywhere
Export function pattern
Create a function that accepts dataframe, summary text, and charts. It outputs CSV to one folder, converts markdown summary to PDF, embeds charts in HTML. One call generates all formats.
def export_analysis(df, summary_text, charts_dict, output_dir):
    """Export analysis in CSV, PDF, and HTML formats."""
    
    # 1. Export CSV
    df.to_csv(f'{output_dir}/data.csv', index=False)
    
    # 2. Export PDF (from markdown)
    from weasyprint import HTML
    html_summary = markdown_to_html(summary_text)
    HTML(string=html_summary).write_pdf(f'{output_dir}/report.pdf')
    
    # 3. Export HTML with embedded charts
    html = f"<h1>Analysis Report</h1>{html_summary}"
    for name, fig in charts_dict.items():
        html += fig.to_html(include_plotlyjs='cdn')
    
    with open(f'{output_dir}/report.html', 'w') as f:
        f.write(html)
    
    # 4. Create metadata
    with open(f'{output_dir}/README.md', 'w') as f:
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Records: {len(df)}\n")
        f.write(f"Columns: {list(df.columns)}\n")
Versioning and Tracking Report Changes
Report history enables audit trails and comparisons
Always timestamp outputs. Use format: YYYY-MM-DD_HHMMSS. Keep previous reports available so stakeholders can compare week-to-week or month-to-month. Archived reports answer "Did this metric improve from last month?" without regenerating. Timestamp enables traceability - which version was used for which decision.
Handling Errors In Automated Exports
Automated processes must not crash silently
If scheduled export fails (database down, missing column, permission denied), the script should: (1) Log error with timestamp and details, (2) Send alert to data team, (3) Skip export gracefully without crashing, (4) Retry on next schedule. Never leave stakeholders without reports - if export fails, notify them immediately so they know to check the dashboard manually.
Email Delivery Of Reports
Automated email delivery moves insights from analyst desk to executive inbox
After export completes, send email with: (1) Brief summary of key findings, (2) Links to download CSV and HTML, (3) Link to dashboard, (4) When next report runs. Email delivery bypasses the "I forgot to download the report" problem. Insights reach stakeholders proactively.
You just learnedhow to automate report generation and delivery. Stakeholders receive fresh analysis on schedule. Analysts are freed from manual exports. This is how data products scale.

Insight Export & Report Generation


00h 59m 55s

You have a complete analysis with cleaned data, summary text, and interactive charts. Now automate export so stakeholders can download datasets and reports without manual work. Create CSV, PDF, and HTML outputs that update automatically on schedule.
Task 1: Create Export Function for Multiple Formats (1 mark)
Build a reusable Python function that generates CSV, PDF, and HTML from your analysis:
import os
from datetime import datetime
import pandas as pd

def export_analysis(df, summary_text, charts_dict, output_dir):
    """
    Export analysis in three formats: CSV, PDF, HTML.
    
    Args:
        df: Cleaned DataFrame with analysis results
        summary_text: Executive summary as markdown string
        charts_dict: Dict of {chart_name: plotly_figure}
        output_dir: Directory to save outputs
    """
    
    # Create timestamped output folder
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    report_dir = f"{output_dir}/{timestamp}_analysis"
    os.makedirs(report_dir, exist_ok=True)
    
    # 1. Export cleaned CSV
    csv_path = f"{report_dir}/cleaned_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"✓ CSV exported: {csv_path}")
    
    # 2. Export PDF summary
    try:
        # Convert markdown to HTML, then to PDF
        pdf_path = f"{report_dir}/summary_report.pdf"
        html_content = markdown_to_html(summary_text)
        
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(pdf_path)
        print(f"✓ PDF exported: {pdf_path}")
    except Exception as e:
        print(f"✗ PDF export failed: {e}")
    
    # 3. Export HTML with embedded charts
    html_path = f"{report_dir}/interactive_report.html"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Analysis Report</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .chart-container {{ margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>Analysis Report</h1>
        <div class="summary">{markdown_to_html(summary_text)}</div>
    """
    
    # Embed all charts
    for chart_name, fig in charts_dict.items():
        html_content += f"""
        <div class="chart-container">
            <h2>{chart_name}</h2>
            {fig.to_html(include_plotlyjs='cdn', div_id=chart_name)}
        </div>
        """
    
    html_content += "</body></html>"
    
    with open(html_path, 'w') as f:
        f.write(html_content)
    print(f"✓ HTML exported: {html_path}")
    
    # 4. Create metadata file
    metadata = {
        'Generated': datetime.now().isoformat(),
        'Records': len(df),
        'Columns': list(df.columns),
        'Data Range': f"{df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else "N/A"
    }
    
    metadata_path = f"{report_dir}/README.md"
    with open(metadata_path, 'w') as f:
        f.write("# Analysis Report\n\n")
        for key, value in metadata.items():
            f.write(f"- **{key}:** {value}\n")
    
    print(f"✓ Metadata created: {metadata_path}")
    
    return report_dir
Usage:
# Prepare your analysis
df = clean_data()  # Your cleaned DataFrame
summary = "## Churn Analysis\nFinding: Support speed impacts retention..."
charts = {
    'Revenue Trend': fig_revenue,
    'Churn by Segment': fig_churn,
    'Support Impact': fig_support
}

# Export all formats at once
output_folder = export_analysis(df, summary, charts, 'output')
print(f"All exports saved to: {output_folder}")
Validation: Function runs without error. All three formats generated correctly. Folder structure is organized with metadata.
Task 2: Test Export Output Files (1 mark)
Verify that all exported files are accessible and correct:
import os

def verify_exports(report_dir):
    """Verify all export files are present and readable."""
    
    required_files = ['cleaned_data.csv', 'summary_report.pdf', 'interactive_report.html', 'README.md']
    
    for filename in required_files:
        filepath = f"{report_dir}/{filename}"
        
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✓ {filename}: {file_size} bytes")
        else:
            print(f"✗ {filename}: MISSING")
    
    # Test CSV is readable
    try:
        df_test = pd.read_csv(f"{report_dir}/cleaned_data.csv")
        print(f"✓ CSV readable: {len(df_test)} rows, {len(df_test.columns)} columns")
    except Exception as e:
        print(f"✗ CSV read failed: {e}")
    
    # Test HTML opens in browser
    html_path = f"{report_dir}/interactive_report.html"
    print(f"\nOpen in browser: file://{os.path.abspath(html_path)}")

verify_exports('output/2024-12-15_1430_analysis')
Validation: All files exist and are readable. HTML opens in browser without errors.
Task 3: Create Reusable Export Function for Streamlit App (1 mark)
Integrate export into Streamlit so stakeholders can download with one click:
import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')
st.title('Sales Analysis Dashboard')

# ... your dashboard code ...

# Add export section
st.sidebar.header('Export')

if st.sidebar.button('📥 Export Analysis'):
    # Prepare data
    df = pd.read_sql("SELECT * FROM analysis_results", engine)
    summary = "## Analysis Report\nKey findings..."
    charts = {'Revenue': fig_revenue, 'Churn': fig_churn}
    
    # Export
    report_dir = export_analysis(df, summary, charts, 'output')
    
    # Provide download links
    st.success(f'✓ Analysis exported to: {report_dir}')
    
    # CSV download
    csv_bytes = df.to_csv(index=False).encode()
    st.download_button(
        label='📊 Download Data (CSV)',
        data=csv_bytes,
        file_name='analysis_data.csv',
        mime='text/csv'
    )
    
    # HTML download
    with open(f'{report_dir}/interactive_report.html', 'r') as f:
        html_bytes = f.read()
    st.download_button(
        label='🌐 Download Report (HTML)',
        data=html_bytes,
        file_name='analysis_report.html',
        mime='text/html'
    )
Validation: Streamlit app runs. Export button works. Downloads complete successfully.
Task 4: Implement Scheduled Export (1 mark)
Set up automatic report generation on a schedule (daily, weekly, etc):
Option A: Using Schedule Python Library
import schedule
import time

def scheduled_export():
    """Run export on schedule."""
    df = run_analysis()  # Your analysis function
    summary = generate_summary(df)
    charts = generate_charts(df)
    
    report_dir = export_analysis(df, summary, charts, 'output')
    print(f"[{datetime.now()}] Export complete: {report_dir}")

# Schedule to run daily at 5pm
schedule.every().day.at("17:00").do(scheduled_export)

while True:
    schedule.run_pending()
    time.sleep(60)
Option B: Using Cron (Linux/Mac)
# crontab -e
# Run every Friday at 5pm
0 17 * * 5 /usr/bin/python3 /path/to/export_script.py
Option C: Using Windows Task Scheduler
* Create task that runs python export_script.py
* Set trigger: Daily at 5pm
* Run with highest privileges
Validation: Scheduled job runs without errors. Check logs to confirm execution.
Task 5: Document Export Process and File Guide (1 mark)
Create a README explaining the export outputs for stakeholders:
# Analysis Report Guide

## What's Included

### cleaned_data.csv
- **Purpose:** Raw analysis data for further exploration in Excel
- **Rows:** 50,000 customer records
- **Columns:** customer_id, segment, churn_risk, support_interactions, response_time_hours
- **Use Case:** Stakeholders can filter, sort, and build their own pivot tables
- **Refresh:** Updated daily at 5pm

### summary_report.pdf
- **Purpose:** Executive summary suitable for meetings and email
- **Content:** Key findings, business impact, recommendations
- **Length:** 2 pages
- **Use Case:** Share with leadership, embed in presentations
- **Format:** Professional PDF with company branding

### interactive_report.html
- **Purpose:** Full analysis with interactive charts
- **Content:** All findings, all visualizations, detailed metrics
- **Size:** Single file, no dependencies (except Plotly CDN)
- **Use Case:** Explore data in browser, zoom/pan/hover to see details
- **Sharing:** Email the HTML file to anyone - it opens in any browser

## How to Use These Files

1. **For Excel analysis:** Open cleaned_data.csv in Excel, build your own charts
2. **For presentations:** Print or email summary_report.pdf
3. **For exploration:** Open interactive_report.html in browser, hover for tooltips
4. **For sharing:** Send interactive_report.html - no Python required to view

## When Are These Files Updated?

- **Daily at 5pm:** Fresh exports with latest data
- **On-demand:** Click "Export" button in dashboard for immediate export

## Questions?

- Data definitions: See README.md in export folder
- Analysis methodology: See technical_analysis.md
Validation: Documentation is clear. Stakeholders understand what each file is for and when it updates.
Submission
git add export_functions.py
git add streamlit_export_integration.py
git add export_documentation.md
git commit -m "export: automate report generation in CSV, PDF, HTML formats"
git push
Submit:
1. GitHub link to export code and documentation
2. Video (3-5 minutes):
    * Show export function being called
    * Verify all three output formats (CSV, PDF, HTML)
    * Test downloaded CSV in Excel
    * Open HTML report in browser
    * Show Streamlit download buttons working
    * Explain how scheduled export works
    * Answer follow-up on email delivery automation
Upload to Google Drive with sharing set to "Anyone with the link can view". Test the link in a private browser tab before submitting.
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.


2.51
Streamlit App Structure & Navigation

Hey Streamlit Architect!
Welcome. You have data pipelines, SQL views, charts, and KPI logic. Now you need a product shell that organises everything into a navigable application a non-technical user can operate. Streamlit turns Python scripts into interactive web apps with zero front-end code. This lesson teaches you to scaffold a multi-section Streamlit application with sidebar navigation, layout columns, and visual hierarchy that makes complex analytics feel simple.
Every analytics tool that was technically powerful but abandoned by stakeholders had the same problem: users could not find what they needed. Pages were cluttered. Navigation was missing. The most important content was buried below the fold. This lesson teaches you to build the application shell first - the structure that makes every feature discoverable and every section reachable in one click.
The Real Scenario
THE PROBLEM
A data team builds a Streamlit app with 15 charts, 8 filters, and 3 data tables in a single scrollable page. The operations manager opens it, scrolls for 30 seconds, cannot find the churn dashboard, gives up, and goes back to requesting reports via email. The app had every feature. It had no structure. Without navigation, every feature is invisible.
THE SOLUTION
Add a sidebar with navigation options. Each option shows one focused section. The user clicks Overview to see KPIs. Clicks Trends to see time-series charts. Clicks Detail to access filters and data tables. Every section is one click away. The most important content loads first. The app feels like a product, not a script output.
How Streamlit Execution Works
The Script Reruns on Every Single Interaction
Streamlit execution model
Unlike traditional web apps with separate front-end and back-end, Streamlit reruns your entire Python script from top to bottom every time the user interacts with any widget. Click a button - full rerun. Change a slider - full rerun. Select a dropdown option - full rerun. This means your script must be written to handle every state on every run. There is no persistent server state between interactions unless you use session state explicitly.
Why this matters for app design
Because the script reruns completely, expensive operations like loading data or computing aggregations would repeat on every click. Streamlit solves this with caching decorators. Data loading functions decorated with @st.cache_data run once and cache the result. Subsequent reruns skip the computation and return the cached result. Understanding the rerun model is essential for building apps that feel instant instead of sluggish.
You just learned how Streamlit reruns the entire script on every interaction and why caching matters. Now you will learn how to build sidebar navigation that controls which section is displayed.
Sidebar Navigation
One Sidebar, Multiple Sections, One Click to Switch
Building sidebar navigation with st.sidebar
The sidebar is a collapsible panel on the left side of the app. Place navigation controls and global filters here. The main content area responds to sidebar selections.
import streamlit as st

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Segments", "Data Explorer"]
)

# Main content area responds to selection
if page == "Overview":
    st.title("Business Overview")
    st.write("KPI cards and summary metrics appear here.")
elif page == "Trends":
    st.title("Trend Analysis")
    st.write("Time-series charts appear here.")
elif page == "Segments":
    st.title("Segment Breakdown")
    st.write("Comparison charts by segment appear here.")
elif page == "Data Explorer":
    st.title("Data Explorer")
    st.write("Filters, tables, and export options appear here.")
Multipage apps using Streamlit conventions
For larger apps, Streamlit supports a pages/ directory convention. Create a folder called pages next to your main script. Each Python file inside becomes a separate page in the sidebar automatically. File names become page names. This is cleaner for apps with 5 or more distinct sections because each page has its own file, making code maintainable.
You just learned how to build sidebar navigation and the multipage directory convention. Now you will learn how to use columns and expanders to create visual hierarchy within each section.
Layout Components: Columns and Expanders
Organising Content So the Most Important Thing Loads First
st.columns - side by side layout
Columns place content horizontally. Use them for KPI cards, side-by-side charts, or any layout where comparison matters. KPI cards always use columns because horizontal scanning is natural for status checks.
# Five KPI cards in a row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Revenue", "$5.2M", "+12.5%")
with col2:
    st.metric("Users", "2,500", "+5.2%")
with col3:
    st.metric("AOV", "$45", "+2.1%")
with col4:
    st.metric("Churn", "5.2%", "-2.8%", delta_color="inverse")
with col5:
    st.metric("NPS", "72", "+4")
st.expander - progressive disclosure
Expanders hide content behind a clickable header. Use them for detail that most users do not need on every visit: methodology notes, raw data tables, advanced filters. The content exists but does not clutter the default view.
with st.expander("View Raw Data"):
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(), "data.csv")

with st.expander("Methodology Notes"):
    st.write("Revenue is calculated as sum of order_amount...")
USE ST.COLUMNS WHEN
Content should be compared side by side: KPI cards, paired charts, filter groups. Columns create horizontal layout that maps to the dashboard hierarchy pattern.
USE ST.EXPANDER WHEN
Content is optional or secondary: raw data, methodology, advanced settings. Expanders implement progressive disclosure so the default view stays clean.
You just learned how to use columns for horizontal layout and expanders for progressive disclosure. Now you will learn how to structure the visual hierarchy with headers, subheaders, and dividers.
Visual Hierarchy: Headers, Subheaders, and Dividers
Structure the Page So Users Know Where They Are
Header hierarchy pattern
Use st.title once per page for the page name. Use st.header for major sections. Use st.subheader for subsections within a section. Use st.divider to visually separate sections. Consistent header usage creates scannable pages where users find content without reading everything.
st.title("Sales Performance Dashboard")

# Section 1: KPIs
st.header("Key Performance Indicators")
# ... KPI columns here ...

st.divider()

# Section 2: Trends
st.header("Revenue Trends")
st.subheader("Monthly Revenue (Last 12 Months)")
# ... chart here ...

st.divider()

# Section 3: Detail
st.header("Detailed Analysis")
st.subheader("Filter and Export")
# ... filters and tables here ...
Streamlit app structure checklist
* Sidebar navigation controls which section is displayed
* At least three distinct content sections implemented
* st.columns used for KPI cards and side-by-side content
* st.expander used for optional detail and raw data
* Headers, subheaders, and dividers create consistent visual hierarchy
* Most important content visible on first load without scrolling
* App runs without errors from a clean environment
You just learned how to scaffold a complete Streamlit application with sidebar navigation, column layouts, expanders for progressive disclosure, and visual hierarchy using headers and dividers. This shell is the foundation every feature in the upcoming lessons will plug into.
Streamlit App Structure & Navigation


00h 59m 55s

Your team needs a multi-section analytics dashboard. Before adding data, charts, or filters, you must build the application shell: sidebar navigation, section headers, layout columns, and visual hierarchy. This shell will be the foundation every future feature plugs into.
Task 1: Create Sidebar Navigation (1 mark)
Requirements: Build a Streamlit app with a sidebar that controls which section is displayed in the main content area.
import streamlit as st

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Data Explorer"]
)

if page == "Overview":
    st.title("Business Overview")
    st.write("KPI summary cards and key metrics will appear here.")

elif page == "Trends":
    st.title("Trend Analysis")
    st.write("Time-series charts and comparisons will appear here.")

elif page == "Data Explorer":
    st.title("Data Explorer")
    st.write("Filters, data tables, and export options will appear here.")
Validation: Sidebar radio switches between sections. Only the selected section is visible. Navigation is clear and responsive.
Task 2: Implement Three Content Sections With Columns and Expanders (1 mark)
Requirements: Each section must use st.columns for side-by-side content and st.expander for optional detail.
if page == "Overview":
    st.title("Business Overview")

    # KPI row using columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Revenue", "$5.2M", "+12.5%")
    with col2:
        st.metric("Users", "2,500", "+5.2%")
    with col3:
        st.metric("AOV", "$45", "+2.1%")
    with col4:
        st.metric("Churn", "5.2%", "-2.8%", delta_color="inverse")
    with col5:
        st.metric("NPS", "72", "+4")

    # Expander for methodology notes
    with st.expander("About These Metrics"):
        st.write("Revenue is calculated as sum of all order amounts "
                 "for the current month. Churn is the percentage of "
                 "customers who did not return within 30 days.")
Validation: Columns display content side by side. Expanders hide optional detail. At least three sections implemented.
Task 3: Apply Consistent Visual Hierarchy (1 mark)
Requirements: Use st.title, st.header, st.subheader, and st.divider consistently across all sections.
* st.title: Once per page (page name)
* st.header: For each major section within a page
* st.subheader: For subsections within a section
* st.divider: Between major sections
st.title("Trend Analysis")

st.header("Revenue Trends")
st.subheader("Monthly Revenue (Last 12 Months)")
st.write("Chart placeholder")

st.divider()

st.header("Customer Metrics")
st.subheader("Active Customers Over Time")
st.write("Chart placeholder")
Validation: Visual hierarchy is consistent across all three sections. Headers create scannable structure. Dividers separate sections cleanly.
Task 4: Ensure App Runs From Clean Environment (1 mark)
Requirements:
* Create a requirements.txt with all dependencies
* App runs without errors using: pip install -r requirements.txt && streamlit run app.py
* No hardcoded file paths or missing imports
# requirements.txt
streamlit==1.38.0
pandas==2.1.4
Validation: Clone repo, install requirements, run app. No errors on first launch.
Task 5: Place Important Content Above the Fold (1 mark)
Requirements: The most important content (KPI cards or key message) must be visible on first load without scrolling.
* KPI cards or summary metrics appear at the very top of the Overview section
* No large blank spaces or unnecessary text before the main content
* The user's first impression is the key metrics, not instructions or empty space
Validation: On first load, the top of the page shows KPIs or the primary content. No scroll required to see the most important information.
Submission
git add app.py requirements.txt
git commit -m "streamlit: scaffold multi-section app with sidebar navigation"
git push
Submit:
1. GitHub PR link with app code and requirements.txt
2. Video (3-5 minutes) covering:
    * How Streamlit execution model works (script reruns on every interaction)
    * How st.sidebar controls the main content area
    * Difference between st.columns and st.expander and when each is appropriate
    * Walk through the app layout explaining information hierarchy decisions
    * How to structure a Streamlit app with multiple pages using the pages directory convention
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.


2.52
Dataset Upload & Dynamic Preview System

Hey Data Upload Engineer!
Welcome. Your Streamlit shell has navigation and layout. But it has no data yet. Real analytics products let users bring their own data. This lesson teaches you to add file upload functionality that accepts CSV and JSON, validates the file, and immediately displays a cleaned preview with column summary and basic statistics. The user uploads a file and sees results in seconds with zero manual preprocessing.
Every analytics tool that required a developer to load data before users could see it created a bottleneck. Users had questions now. Developers were busy. The tool sat unused while data sat in spreadsheets. File upload removes that bottleneck. Users bring their own data, see a preview instantly, and start exploring. This lesson builds that capability.
The Real Scenario
THE PROBLEM
An operations manager receives a new CSV export from the billing system. They want to check for anomalies quickly. The analytics dashboard only shows last month's pre-loaded data. To see the new file, they must send it to a developer, wait for processing, and check the dashboard tomorrow. By then, the anomaly has caused billing errors affecting 200 customers.
THE SOLUTION
Add a file upload widget. The manager drags the CSV into the browser. Instantly sees: row count, column names, data types, null percentages, and the first 10 rows. Spots the anomaly in the amount column within 30 seconds. Alerts the billing team. Issue fixed before it spreads.
File Upload With st.file_uploader
From File to DataFrame in Three Lines
How st.file_uploader works
The widget returns a file-like object when the user uploads a file. It returns None when no file is uploaded. You must handle both states in your script because Streamlit reruns the entire script on every interaction. The uploaded file bytes live in memory for the duration of the session.
import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "json"]
)

if uploaded_file is not None:
    # Determine file type and load accordingly
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".json"):
        df = pd.read_json(uploaded_file)

    st.success(
        "File loaded: "
        + uploaded_file.name
        + " ("
        + str(len(df))
        + " rows, "
        + str(len(df.columns))
        + " columns)"
    )
else:
    st.info("Upload a CSV or JSON file to begin.")
Always handle the None state
When no file is uploaded, st.file_uploader returns None. Every line of code that uses the DataFrame must be inside the if block. Code outside the if block runs on every rerun and will crash with a NameError if df is not defined.
You just learned how to accept file uploads and load them into a DataFrame. Now you will learn how to display an automatic preview with column summary and statistics.
Automatic Preview and Column Summary
Show Everything the User Needs to Know About Their Data Instantly
Building the preview section
if uploaded_file is not None:
    # Data shape summary
    st.header("Dataset Preview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", str(len(df.columns)))
    with col3:
        total_nulls = df.isnull().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        null_pct = (total_nulls / total_cells) * 100
        st.metric("Null %", f"{null_pct:.1f}%")

    st.divider()

    # First N rows
    st.subheader("First 10 Rows")
    st.dataframe(df.head(10), use_container_width=True)

    # Column summary
    st.subheader("Column Summary")
    summary = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.astype(str).values,
        "Non-Null": df.notnull().sum().values,
        "Null Count": df.isnull().sum().values,
        "Null %": (df.isnull().sum() / len(df) * 100).round(1).values
    })
    st.dataframe(summary, use_container_width=True)
Basic descriptive statistics
For numeric columns, show describe() output. For categorical columns, show value counts of the top categories. This gives users an instant data quality check without writing any code.
    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe(), use_container_width=True)
You just learned how to display an automatic preview with row counts, column summaries, null percentages, and descriptive statistics. Now you will learn how to handle invalid uploads gracefully.
Error Handling for Invalid Uploads
Never Show a Python Traceback to a Business User
Wrapping upload in try-except
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload CSV or JSON.")
            st.stop()

        if len(df) == 0:
            st.warning("The uploaded file is empty. Please check your data.")
            st.stop()

        st.success("File loaded successfully.")
    except Exception as e:
        st.error("Could not read this file. Please check the format.")
        st.stop()
st.stop() halts execution cleanly
When an error is detected, display a user-friendly message with st.error() or st.warning(), then call st.stop() to halt the script. This prevents downstream code from running with invalid data. The user sees the message and knows what to do. No traceback. No confusion.
File upload checklist
* st.file_uploader accepts CSV and JSON with type parameter
* Uploaded bytes converted to DataFrame with pd.read_csv or pd.read_json
* Preview shows first N rows, column names, dtypes, and null counts
* Basic statistics displayed with df.describe()
* Invalid or empty files handled with st.error and st.stop
* Uploaded data usable for filtering and charting in the same session
You just learned how to build a complete dataset upload and preview system with validation, column summaries, statistics, and error handling. Users can now bring their own data into your analytics product and see results instantly

Dataset Upload & Dynamic Preview System


00h 59m 56s

Your analytics app needs to accept user data. Build file upload functionality that accepts CSV and JSON files, validates them, and immediately displays a cleaned preview with column summary and basic statistics. Users should see their data within seconds of uploading, with zero manual preprocessing.
Task 1: Implement File Upload (1 mark)
Requirements: Use st.file_uploader to accept CSV and JSON files. Load the uploaded file into a Pandas DataFrame. Handle the None state when no file is uploaded.
import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "json"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".json"):
        df = pd.read_json(uploaded_file)

    st.success("Loaded: " + uploaded_file.name
               + " (" + str(len(df)) + " rows, "
               + str(len(df.columns)) + " columns)")
else:
    st.info("Upload a CSV or JSON file to begin.")
Validation: CSV and JSON files both load correctly. DataFrame is created and accessible for downstream use.
Task 2: Display Automatic Preview (1 mark)
Requirements: After upload, immediately show: first N rows, column names, data types, and null counts per column.
if uploaded_file is not None:
    st.header("Dataset Preview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", str(len(df.columns)))
    with col3:
        null_pct = (df.isnull().sum().sum()
                    / (df.shape[0] * df.shape[1]) * 100)
        st.metric("Null %", f"{null_pct:.1f}%")

    st.subheader("First 10 Rows")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Column Summary")
    summary = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.astype(str).values,
        "Non-Null": df.notnull().sum().values,
        "Null Count": df.isnull().sum().values,
        "Null %": (df.isnull().sum() / len(df) * 100).round(1).values
    })
    st.dataframe(summary, use_container_width=True)
Validation: Preview shows row count, column count, null percentage, first 10 rows, and column summary with types and null counts.
Task 3: Display Basic Statistics (1 mark)
Requirements: Show descriptive statistics for numeric columns (count, mean, std, min, max, quartiles).
    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe(), use_container_width=True)
Validation: Statistics table displays for all numeric columns. Non-numeric columns gracefully excluded.
Task 4: Handle Invalid Uploads (1 mark)
Requirements: Invalid or empty file uploads show a clear error message instead of a Python traceback.
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()

        if len(df) == 0:
            st.warning("Uploaded file is empty.")
            st.stop()
    except Exception:
        st.error("Could not read this file. Check the format and try again.")
        st.stop()
Validation: Upload a malformed file. App shows error message, not traceback. Upload an empty file. App shows warning.
Task 5: Ensure Data Is Usable Downstream (1 mark)
Requirements: The uploaded DataFrame must be available for filtering and charting within the same app session. Demonstrate by adding a simple filter or chart that uses the uploaded data.
    # Simple demonstration of downstream usage
    st.subheader("Quick Exploration")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("Select a column to visualise", numeric_cols)
        st.bar_chart(df[selected_col].value_counts().head(20))
Validation: After upload, a filter or chart works with the uploaded data. Data persists for the session.
Submission
git add app.py
git commit -m "upload: file upload with preview, statistics, and error handling"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * How st.file_uploader works and what file types it supports
    * How uploaded file bytes are converted into a Pandas DataFrame
    * How null percentage is computed per column and displayed
    * Walk through the upload-to-preview flow showing what user sees at each step
    * Follow-up: how to support uploading multiple files and merging them automatically
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.


2.53
Streamlit Filters & Interactive Widgets

Hey Widget Wiring Specialist!
Welcome. Your app uploads data and shows a preview. But users need to explore - filter by date, select specific segments, adjust thresholds. Streamlit widgets let users interact with data through date pickers, dropdowns, sliders, and radio buttons. This lesson teaches you to wire every widget to the DataFrame so changes propagate instantly to charts and tables. Users explore freely. Code stays unchanged.
Every dashboard that required a developer to change a date range in the code, re-run the script, and share the new output was not a product - it was a manual service. Widgets remove the developer from the exploration loop. Users adjust filters, see updated results, adjust again. Self-service analytics starts here.
The Real Scenario
THE PROBLEM
A sales director wants to compare Q1 vs Q2 revenue for the Enterprise segment only. The dashboard shows all-time data for all segments. No filters exist. The director asks the analyst to create a filtered view. The analyst spends 20 minutes modifying the script. The director now wants to add the Mid-Market segment. Another 20 minutes. By the third request, both are frustrated.
THE SOLUTION
Add a date range picker, a multi-select dropdown for segments, and a revenue slider. The director selects Q1-Q2, picks Enterprise and Mid-Market, adjusts the minimum revenue threshold. Charts update instantly. No developer needed. The director explores 10 different views in 5 minutes instead of waiting hours for one.
Widget Types and When to Use Each
Four Widgets That Cover 90 Percent of Filtering Needs
Date Picker
st.date_input - filter data to a specific time period
Use for any time-based filtering. Accepts single date or date range. The user picks start and end dates visually. Returns Python date objects you compare against DataFrame date columns.
Multi-Select
st.multiselect - choose one or more categories
Use for categorical filters: segments, product lines, regions. Users pick multiple options from a dropdown. Returns a list you use with isin() to filter the DataFrame.
Slider
st.slider - set numeric thresholds or ranges
Use for numeric filtering: minimum revenue, age range, score threshold. Users drag to set a value or range. Returns a number or tuple you compare against DataFrame numeric columns.
Radio
st.radio - choose exactly one option from a small set
Use when the user must pick one option: chart type, time granularity (daily/weekly/monthly), metric to display. Returns a single string. Best for 2-5 mutually exclusive options.
You just learned the four core widget types and when to use each. Now you will learn how to wire them together into a filter chain that updates the DataFrame and all downstream charts reactively.
Wiring Widgets to the DataFrame
Every Widget Output Filters the DataFrame, Every Chart Reads the Filtered Result
Filter chain pattern
# Sidebar filters
st.sidebar.header("Filters")

# Date range
date_range = st.sidebar.date_input(
    "Date Range",
    value=(df["date"].min(), df["date"].max())
)

# Segment multi-select
all_segments = df["segment"].unique().tolist()
selected_segments = st.sidebar.multiselect(
    "Segments",
    options=all_segments,
    default=all_segments
)

# Revenue slider
min_rev, max_rev = st.sidebar.slider(
    "Revenue Range",
    min_value=int(df["revenue"].min()),
    max_value=int(df["revenue"].max()),
    value=(int(df["revenue"].min()), int(df["revenue"].max()))
)

# Apply all filters to create filtered DataFrame
filtered_df = df[
    (df["date"] >= pd.Timestamp(date_range[0]))
    & (df["date"] <= pd.Timestamp(date_range[1]))
    & (df["segment"].isin(selected_segments))
    & (df["revenue"] >= min_rev)
    & (df["revenue"] <= max_rev)
]

# All charts and metrics read from filtered_df
st.metric("Filtered Rows", f"{len(filtered_df):,}")
Handle empty filter results gracefully
When a filter combination returns zero rows, display a friendly message instead of crashing. Check if len(filtered_df) == 0 and show st.warning with a suggestion to broaden filters. Never let charts render on an empty DataFrame.
You just learned how to wire widgets into a filter chain that updates the DataFrame reactively. Now you will learn how to set meaningful defaults and implement a reset mechanism.
Defaults and Reset Mechanism
The App Should Show Meaningful Content on First Load
Setting meaningful defaults
Every widget needs a default value that shows useful content on first load. Date range defaults to the full dataset range. Multi-select defaults to all options selected. Slider defaults to the full range. The user sees all data initially and narrows down from there. An app that loads with empty filters and no data visible feels broken.
Implementing a clear filters button
if st.sidebar.button("Reset Filters"):
    st.rerun()
Calling st.rerun() reruns the entire script, which resets all widgets to their default values. This gives users a one-click way to return to the unfiltered view without manually undoing each filter.
Widget and filter checklist
* At least three different widget types implemented
* Each widget input wired to filter the DataFrame
* All downstream charts update reactively when filters change
* Every widget has a meaningful default so the app loads with content
* Empty filter results show a warning message instead of crashing
* A reset mechanism returns all filters to defaults
You just learned how to implement interactive widgets with a filter chain, meaningful defaults, empty-state handling, and a reset mechanism. Users can now explore any slice of their data through the UI without touching code.
Streamlit Filters & Interactive Widgets


00h 59m 56s

Your app uploads data and shows a preview. Now users need to explore - filter by date, select segments, adjust thresholds. Implement interactive widgets wired to the DataFrame so changes propagate to all downstream charts and metrics instantly.
Task 1: Implement Three Different Widget Types (1 mark)
Requirements: Add at least three widget types from: date picker, multi-select, slider, radio button.
st.sidebar.header("Filters")

# Widget 1: Date range picker
date_range = st.sidebar.date_input(
    "Date Range",
    value=(df["date"].min(), df["date"].max())
)

# Widget 2: Multi-select for segments
all_segments = df["segment"].unique().tolist()
selected_segments = st.sidebar.multiselect(
    "Segments", options=all_segments, default=all_segments
)

# Widget 3: Revenue slider
min_rev, max_rev = st.sidebar.slider(
    "Revenue Range",
    min_value=int(df["revenue"].min()),
    max_value=int(df["revenue"].max()),
    value=(int(df["revenue"].min()), int(df["revenue"].max()))
)
Validation: Three distinct widget types are visible in the sidebar. Each accepts user input.
Task 2: Wire Widgets to Filter the DataFrame (1 mark)
Requirements: Each widget input filters the DataFrame. All downstream charts and metrics read from the filtered result.
filtered_df = df[
    (df["date"] >= pd.Timestamp(date_range[0]))
    & (df["date"] <= pd.Timestamp(date_range[1]))
    & (df["segment"].isin(selected_segments))
    & (df["revenue"] >= min_rev)
    & (df["revenue"] <= max_rev)
]

st.write(f"Showing {len(filtered_df):,} of {len(df):,} records")
st.dataframe(filtered_df.head(20), use_container_width=True)
Validation: Changing any widget updates the displayed data. Row count changes reflect filter application.
Task 3: Define Meaningful Default Values (1 mark)
Requirements: Every widget has a default that shows useful content on first load. The app never loads with empty results.
* Date range defaults to full dataset range
* Multi-select defaults to all segments selected
* Slider defaults to full range
Validation: On first load, all data is visible. No empty states. User narrows down from the full dataset.
Task 4: Handle Empty Filter Combinations (1 mark)
Requirements: No valid combination of filter inputs should crash the app. If filters return zero rows, display a helpful message.
if len(filtered_df) == 0:
    st.warning("No data matches the current filters. "
               "Try broadening your selection.")
    st.stop()
Validation: Select an impossible filter combination (e.g., future dates). App shows warning, does not crash.
Task 5: Implement Filter Reset (1 mark)
Requirements: A "Reset Filters" button returns all widgets to their default values.
if st.sidebar.button("Reset Filters"):
    st.rerun()
Validation: Click Reset. All widgets return to defaults. Full dataset is displayed again.
Submission
git add app.py
git commit -m "filters: interactive widgets with filter chain and reset"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * How Streamlit widget state is captured and used to filter a DataFrame
    * How session state differs from widget default values and when session state is needed
    * What happens when multi-select returns empty result and how it is handled
    * Walk through filter chain demonstrating how one widget updates displayed data
    * Follow-up: how to link two dropdowns so second options depend on first selection
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.54
Streamlit Session State & Workflow Persistence

Hey State Management Expert!
Welcome. Your widgets filter data reactively. But what happens when the user completes step 1 of a workflow, then interacts with another widget? Streamlit reruns the entire script - and step 1 results vanish. Session state solves this. It persists values across reruns so multi-step workflows remember where the user left off. This lesson teaches you to use st.session_state to maintain analytical continuity across interactions.
Every multi-step workflow that lost user progress on a widget interaction broke the user's trust. They configured step 1, moved to step 2, adjusted a filter, and step 1 reset to defaults. Session state prevents this by storing values that survive reruns. This is how Streamlit apps maintain workflow memory.
The Real Scenario
THE PROBLEM
An analyst builds a two-step workflow: Step 1 selects a customer segment for analysis. Step 2 computes churn metrics for that segment. The user selects Enterprise in step 1, sees the metrics in step 2, then changes a date filter. Streamlit reruns the script. The segment selection resets to the default. Step 2 now shows metrics for all segments instead of Enterprise. The user must re-select Enterprise every time they adjust any other filter.
THE SOLUTION
Store the segment selection in st.session_state. When the script reruns, read the stored value instead of resetting to default. The segment selection survives date filter changes. Step 2 always shows the correct segment. The workflow feels continuous instead of fragmented.
What Session State Is
A Dictionary That Survives Script Reruns
How st.session_state works
st.session_state is a dictionary-like object that persists across script reruns within a single browser session. You read and write to it like a regular dictionary. Values stored in session state survive widget interactions, page switches, and any other event that triggers a rerun. They are cleared only when the user closes the browser tab or you explicitly delete them.
Initialising session state with safe defaults
import streamlit as st

# Initialise only if key does not exist yet
if "selected_segment" not in st.session_state:
    st.session_state["selected_segment"] = "All"
if "workflow_step" not in st.session_state:
    st.session_state["workflow_step"] = 1
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
Always check if the key exists before initialising. Without this check, every rerun would overwrite the stored value back to the default, defeating the purpose of session state.
You just learned what session state is and how to initialise it safely. Now you will learn how to build a multi-step workflow where each step depends on values from the previous step.
Building a Multi-Step Workflow
Step 2 Depends on Step 1 - Session State Carries the Context
Multi-step workflow pattern
# Step 1: Select segment
st.header("Step 1: Select Segment")
segment = st.selectbox(
    "Choose a segment",
    options=["All", "Enterprise", "Mid-Market", "SMB"],
    index=["All", "Enterprise", "Mid-Market", "SMB"].index(
        st.session_state["selected_segment"]
    )
)

if st.button("Confirm Segment"):
    st.session_state["selected_segment"] = segment
    st.session_state["workflow_step"] = 2

# Step 2: Show analysis (only if step 1 is complete)
if st.session_state["workflow_step"] >= 2:
    st.header("Step 2: Segment Analysis")
    chosen = st.session_state["selected_segment"]
    st.write("Analyzing segment: " + chosen)

    if chosen == "All":
        analysis_df = df
    else:
        analysis_df = df[df["segment"] == chosen]

    # Compute and store results
    result = analysis_df["revenue"].sum()
    st.session_state["analysis_result"] = result
    st.metric("Total Revenue", f"${result:,.0f}")
Session state vs widget default values
Widget default values reset on every rerun. Session state persists. Use widget defaults for initial appearance. Use session state for values that must survive interactions. The pattern: read session state to set widget default, then update session state when the user confirms a choice. This keeps the widget in sync with the stored value.
You just learned how to build multi-step workflows with session state. Now you will learn how to implement a reset mechanism that clears all progress cleanly.
Resetting Session State
One Click to Start Over - Clear Everything Cleanly
Reset button pattern
if st.sidebar.button("Reset Workflow"):
    # Clear specific keys
    for key in ["selected_segment", "workflow_step", "analysis_result"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
Delete the specific keys you want to reset, then call st.rerun(). The next run re-initialises them with defaults. This is cleaner than resetting the entire session state because it preserves any unrelated state like uploaded files.
Session state checklist
* At least three distinct values persisted in session state
* Keys named descriptively with safe default initialisation
* Multi-step workflow where step 2 depends on step 1 values
* Reset button clears all workflow progress and returns to initial state
* Session state usage documented with inline comments
* Widget defaults read from session state to stay in sync
You just learned how to use session state to persist workflow progress, maintain analytical continuity across interactions, and implement a clean reset mechanism. Your Streamlit app now remembers user context across every rerun.


Streamlit Session State & Workflow Persistence


00h 59m 56s

Your Streamlit app has filters and widgets. But multi-step workflows lose progress when the user interacts with any widget because Streamlit reruns the script. Apply st.session_state to persist selections, intermediate results, and workflow steps across interactions.
Task 1: Persist Three Values in Session State (1 mark)
Requirements: Use st.session_state to persist at least three distinct values across widget interactions.
import streamlit as st

# Initialise session state with safe defaults
if "selected_segment" not in st.session_state:
    st.session_state["selected_segment"] = "All"
if "workflow_step" not in st.session_state:
    st.session_state["workflow_step"] = 1
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
Validation: Values persist when other widgets are interacted with. Changing a date filter does not reset the selected segment.
Task 2: Name Keys Descriptively and Initialise Safely (1 mark)
Requirements: Session state keys are named descriptively (not "x" or "temp"). Each key is initialised only if it does not already exist.
# Good: descriptive names, safe initialisation
if "filter_date_start" not in st.session_state:
    st.session_state["filter_date_start"] = None
if "computed_revenue" not in st.session_state:
    st.session_state["computed_revenue"] = 0.0
if "export_ready" not in st.session_state:
    st.session_state["export_ready"] = False
Validation: Keys are self-documenting. Initialisation uses "not in" check to prevent overwriting.
Task 3: Build a Multi-Step Workflow (1 mark)
Requirements: Implement a workflow where step 2 depends on a value set in step 1.
# Step 1
st.header("Step 1: Select Segment")
segment = st.selectbox("Segment", ["All", "Enterprise", "Mid-Market", "SMB"])
if st.button("Confirm Segment"):
    st.session_state["selected_segment"] = segment
    st.session_state["workflow_step"] = 2

# Step 2 (only if step 1 complete)
if st.session_state["workflow_step"] >= 2:
    st.header("Step 2: Analysis")
    chosen = st.session_state["selected_segment"]
    st.write("Analysing: " + chosen)
    # Compute and display results for chosen segment
Validation: Complete step 1, interact with another widget, step 2 still shows the correct segment.
Task 4: Implement Session State Reset (1 mark)
Requirements: A reset button clears all workflow progress and returns the app to its initial state.
if st.sidebar.button("Reset Workflow"):
    for key in ["selected_segment", "workflow_step", "analysis_result"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
Validation: Click reset. All session state values return to defaults. Workflow starts from step 1.
Task 5: Document Session State Usage (1 mark)
Requirements: Add inline comments explaining what each session state key stores and why it is needed.
# "selected_segment" - stores the user's segment choice from Step 1
# so it survives reruns when the user interacts with Step 2 widgets.

# "workflow_step" - tracks which step the user has completed.
# Prevents Step 2 from displaying before Step 1 is confirmed.

# "analysis_result" - caches the computation from Step 2 so
# it does not recompute when unrelated widgets are changed.
Validation: Every session state key has a comment explaining its purpose. Code is self-documenting.
Submission
git add app.py
git commit -m "session-state: persist workflow steps and filter selections"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * What session state is and why it is needed in a multi-step Streamlit workflow
    * Difference between st.session_state and widget default values
    * How multi-step workflow was implemented using session state to carry context forward
    * Walk through reset mechanism explaining what state is cleared and why
    * Follow-up: how to use session state to store a DataFrame across page navigation in a multipage app
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public

2.55
Real-Time KPI Dashboard Development

Hey Dashboard Developer!
Welcome. You have the shell, the upload, the filters, and session state. Now you build the real product: a live KPI dashboard that updates metrics and charts dynamically as users interact with filters and upload new data. This lesson teaches you to wire everything together into a reactive dashboard with cached data loading, multiple chart types, and graceful handling of every edge case.
Every dashboard that loaded slowly, crashed on empty filters, or showed stale data after a new file upload failed at the integration layer. Individual components worked. Together they broke. This lesson teaches you to combine upload, filtering, caching, KPIs, and charts into one smooth experience that feels instant and never crashes.
The Real Scenario
THE PROBLEM
A team builds a dashboard with upload, filters, and charts. But every filter change takes 5 seconds because data reloads from disk each time. When the user selects an empty segment, the chart crashes with a ValueError. When they upload a new file, the KPIs still show the old data. The pieces work individually but the integration is broken.
THE SOLUTION
Cache data loading with @st.cache_data so filter changes are instant. Guard every chart with an empty-data check. Tie KPI computations to the filtered DataFrame so they always reflect current filters. The dashboard updates in milliseconds, handles every edge case, and runs end-to-end from upload to insight without hardcoded values.
Caching Data Loading
Load Once, Filter Many Times
@st.cache_data decorator
Wrap any function that loads or computes data with @st.cache_data. Streamlit caches the return value keyed by the function arguments. Subsequent calls with the same arguments return the cached result instantly. Filtering happens on the cached DataFrame in memory - no disk or network access.
@st.cache_data
def load_data(file_content, file_name):
    """Load and return DataFrame. Cached by file content hash."""
    if file_name.endswith(".csv"):
        return pd.read_csv(file_content)
    elif file_name.endswith(".json"):
        return pd.read_json(file_content)
When to invalidate the cache
The cache invalidates automatically when function arguments change. If the user uploads a new file, the file content hash changes, so the function re-executes and caches the new result. You can also clear all caches manually with st.cache_data.clear() when needed.
You just learned how caching prevents redundant data loading on every rerun. Now you will learn how to build reactive KPI cards that update from the filtered DataFrame.
Reactive KPIs From Filtered Data
Every KPI Reads From the Filtered DataFrame - Never From Raw Data
KPI computation pattern
# Compute KPIs from filtered data
total_revenue = filtered_df["revenue"].sum()
avg_order = filtered_df["revenue"].mean()
row_count = len(filtered_df)
unique_customers = filtered_df["customer_id"].nunique()
null_pct = (filtered_df.isnull().sum().sum()
            / (filtered_df.shape[0] * filtered_df.shape[1]) * 100)

# Display KPI cards
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Revenue", f"${total_revenue:,.0f}")
with col2:
    st.metric("Avg Order", f"${avg_order:,.0f}")
with col3:
    st.metric("Records", f"{row_count:,}")
with col4:
    st.metric("Customers", f"{unique_customers:,}")
with col5:
    st.metric("Data Quality", f"{100 - null_pct:.1f}%")
You just learned how to compute reactive KPIs from filtered data. Now you will learn how to add multiple chart types that update with the same filters.
Multiple Chart Types Wired to Filters
Three Charts Minimum - Each Answering a Different Question
Guard against empty filtered data
if len(filtered_df) == 0:
    st.warning("No data matches the current filters. "
               "Try broadening your selection.")
    st.stop()

# Chart 1: Revenue trend (line)
st.subheader("Revenue Over Time")
trend = filtered_df.groupby("date")["revenue"].sum().reset_index()
st.line_chart(trend.set_index("date"))

# Chart 2: Revenue by segment (bar)
st.subheader("Revenue by Segment")
seg = filtered_df.groupby("segment")["revenue"].sum().reset_index()
st.bar_chart(seg.set_index("segment"))

# Chart 3: Distribution (histogram via Plotly)
import plotly.express as px
st.subheader("Order Value Distribution")
fig = px.histogram(filtered_df, x="revenue", nbins=30,
                   title="Order Value Distribution")
st.plotly_chart(fig, use_container_width=True)
Real-time KPI dashboard checklist
* At least five KPI metrics update reactively from filtered DataFrame
* At least three chart types included and update on filter change
* @st.cache_data applied to data loading to prevent redundant computation
* Empty filtered results handled with a user-facing message
* App runs end-to-end from upload to KPI display with no hardcoded values
* Charts read from filtered_df, not raw df
You just learned how to build a complete real-time KPI dashboard with cached data loading, reactive metrics, multiple chart types, and graceful empty-state handling. This is the production-quality analytics product that stakeholders will actually use.

Real-Time KPI Dashboard Development


00h 59m 56s

Build an operational Streamlit dashboard that displays business KPIs dynamically. Metrics, charts, and segment views must update in response to filter inputs and newly uploaded data. The dashboard must run end-to-end from dataset upload to KPI display without any hardcoded values.
Task 1: Display Five Reactive KPI Metrics (1 mark)
Requirements: At least five KPI metrics update reactively based on filter widget inputs. KPIs are computed from the filtered DataFrame, not hardcoded.
total_revenue = filtered_df["revenue"].sum()
avg_order = filtered_df["revenue"].mean()
row_count = len(filtered_df)
unique_customers = filtered_df["customer_id"].nunique()
null_pct = (filtered_df.isnull().sum().sum()
            / (filtered_df.shape[0] * filtered_df.shape[1]) * 100)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Revenue", f"${total_revenue:,.0f}")
with col2:
    st.metric("Avg Order", f"${avg_order:,.0f}")
with col3:
    st.metric("Records", f"{row_count:,}")
with col4:
    st.metric("Customers", f"{unique_customers:,}")
with col5:
    st.metric("Quality", f"{100 - null_pct:.1f}%")
Validation: Change a filter. All five KPIs update to reflect the filtered data. No hardcoded values.
Task 2: Include Three Chart Types (1 mark)
Requirements: At least three different chart types that update when filter state changes.
# Chart 1: Line chart (trend)
st.subheader("Revenue Over Time")
trend = filtered_df.groupby("date")["revenue"].sum().reset_index()
st.line_chart(trend.set_index("date"))

# Chart 2: Bar chart (comparison)
st.subheader("Revenue by Segment")
seg = filtered_df.groupby("segment")["revenue"].sum().reset_index()
st.bar_chart(seg.set_index("segment"))

# Chart 3: Plotly histogram (distribution)
import plotly.express as px
fig = px.histogram(filtered_df, x="revenue", nbins=30)
st.plotly_chart(fig, use_container_width=True)
Validation: All three charts render correctly. Changing filters updates all charts.
Task 3: Apply @st.cache_data to Data Loading (1 mark)
Requirements: Data loading functions use @st.cache_data to prevent redundant recomputation on each interaction.
@st.cache_data
def load_data(file_bytes, file_name):
    if file_name.endswith(".csv"):
        return pd.read_csv(file_bytes)
    elif file_name.endswith(".json"):
        return pd.read_json(file_bytes)
Validation: Interact with filters rapidly. App responds instantly because data is cached. No reload delay.
Task 4: Handle Empty Filtered Results (1 mark)
Requirements: When filters return zero rows, display a user-facing message instead of an error.
if len(filtered_df) == 0:
    st.warning("No data matches current filters. Broaden your selection.")
    st.stop()
Validation: Apply impossible filters. App shows warning message. No Python errors or empty charts.
Task 5: Run End-to-End Without Hardcoded Data (1 mark)
Requirements: The app works with any uploaded dataset (not just a specific file). No column names are hardcoded if the app is designed to be generic. Or if column names are expected, they are validated on upload.
Validation: Upload a different CSV file. App adapts or validates. No hardcoded file paths or values.
Submission
git add app.py requirements.txt
git commit -m "dashboard: reactive KPIs with cached data and multiple chart types"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * What makes a dashboard reactive vs a static report in Streamlit context
    * How @st.cache_data prevents redundant data loading and when to invalidate
    * How a chart updates when a filter widget changes and what Streamlit mechanism drives it
    * Walk through full dashboard explaining how each section connects to a business question
    * Follow-up: how to add auto-refresh that reloads data on a time interval
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.


2.56
Alert Monitoring & Metric Threshold Detection

Hey Alert System Builder!
Welcome. Your dashboard shows KPIs and charts. But dashboards are passive - they wait for someone to look. Alert systems are active - they tell someone when something is wrong. This lesson teaches you to implement threshold-based monitoring that checks metrics against defined limits and surfaces visual warnings when a KPI crosses a critical boundary. Users see problems the moment they happen, not the next time they check.
Every operational failure that was discovered too late - the revenue drop that went unnoticed for a week, the churn spike nobody saw until the monthly report, the data quality issue that corrupted three dashboards - could have been caught by a simple threshold alert. This lesson teaches you to build that safety net.
The Real Scenario
THE PROBLEM
Customer churn rate crosses 8 percent on Tuesday. The dashboard shows it as a number: 8.2 percent. The operations manager does not check the dashboard until Friday. By then, 200 additional customers have churned. The metric was visible the entire time. Nobody was watching. The dashboard did not tell anyone something was wrong because it had no concept of wrong.
THE SOLUTION
Define a threshold: churn above 7 percent triggers a warning. When the dashboard computes churn at 8.2 percent, it displays a red warning banner: "ALERT: Churn rate 8.2 percent exceeds threshold of 7 percent. Investigate immediately." The manager sees the alert on Tuesday. Investigation starts the same day. Root cause identified by Wednesday. Fix deployed by Thursday.
Defining Alert Thresholds in Configuration
Thresholds Belong in a Config File, Not Hardcoded in Display Logic
Why configuration over hardcoding
Thresholds change. A churn threshold of 7 percent might become 5 percent next quarter as the business improves. If the threshold is hardcoded inside an if statement buried in the dashboard code, changing it requires a developer, a code review, and a deployment. If it lives in a configuration dictionary or file, the operations team can adjust it without touching the code.
Alert configuration pattern
# alert_config.py
ALERT_THRESHOLDS = {
    "churn_rate": {
        "metric": "Churn Rate",
        "threshold": 7.0,
        "direction": "above",  # alert when value is above threshold
        "severity": "critical",
        "message": "Churn rate exceeds safe operating limit. "
                   "Investigate customer retention immediately."
    },
    "avg_order_value": {
        "metric": "Average Order Value",
        "threshold": 30.0,
        "direction": "below",  # alert when value drops below
        "severity": "warning",
        "message": "Average order value has dropped below target. "
                   "Check pricing and product mix."
    },
    "null_percentage": {
        "metric": "Data Quality (Null %)",
        "threshold": 5.0,
        "direction": "above",
        "severity": "warning",
        "message": "Null percentage exceeds acceptable limit. "
                   "Check data pipeline for missing values."
    }
}
You just learned how to define alert thresholds in a configuration file. Now you will learn how to check metrics against these thresholds and display visual alerts.
Checking Metrics and Displaying Alerts
Compare Every Metric Against Its Threshold on Every Rerun
Alert checking function
def check_alerts(metrics_dict, thresholds):
    """Check computed metrics against thresholds.
    Returns list of triggered alerts."""
    triggered = []
    for key, config in thresholds.items():
        if key not in metrics_dict:
            continue
        value = metrics_dict[key]
        threshold = config["threshold"]

        if config["direction"] == "above" and value > threshold:
            triggered.append({
                "metric": config["metric"],
                "value": value,
                "threshold": threshold,
                "severity": config["severity"],
                "message": config["message"]
            })
        elif config["direction"] == "below" and value < threshold:
            triggered.append({
                "metric": config["metric"],
                "value": value,
                "threshold": threshold,
                "severity": config["severity"],
                "message": config["message"]
            })
    return triggered
Displaying alerts in Streamlit
# Compute current metrics
current_metrics = {
    "churn_rate": churn_rate_value,
    "avg_order_value": avg_order_value,
    "null_percentage": null_pct_value
}

# Check against thresholds
alerts = check_alerts(current_metrics, ALERT_THRESHOLDS)

# Display alerts at top of dashboard
if alerts:
    for alert in alerts:
        if alert["severity"] == "critical":
            st.error(
                "ALERT: " + alert["metric"]
                + " is " + str(round(alert["value"], 1))
                + " (threshold: " + str(alert["threshold"]) + "). "
                + alert["message"]
            )
        else:
            st.warning(
                "WARNING: " + alert["metric"]
                + " is " + str(round(alert["value"], 1))
                + " (threshold: " + str(alert["threshold"]) + "). "
                + alert["message"]
            )
You just learned how to check metrics against thresholds and display visual alerts. Now you will learn how alerts respond to filter changes.
Alerts That Respond to Filters
When Filters Change the Data, Alerts Must Recalculate
Reactive alert computation
Because Streamlit reruns the script on every widget interaction, alerts automatically recalculate. When the user filters to the Enterprise segment and churn is 10 percent for that segment, the alert fires. When they switch to SMB and churn is 4 percent, the alert clears. No extra code needed - the rerun model handles it. Just ensure metrics are computed from the filtered DataFrame, not the raw data.
Alert monitoring checklist
* At least three metrics monitored against defined thresholds
* Visual alerts displayed using st.error or st.warning when threshold breached
* Thresholds defined in a config dictionary, not hardcoded in display logic
* Alert messages include metric name, current value, threshold, and risk description
* Alerts update correctly when filter inputs change underlying metric values
* Alert severity levels distinguish critical from warning conditions
You just learned how to build a threshold-based alert system with configurable limits, visual warnings, and reactive recalculation on filter changes. Your dashboard now actively tells users when something needs attention instead of waiting to be checked.
Alert Monitoring & Metric Threshold Detection


00h 59m 55s

Your dashboard shows KPIs but does not tell users when something is wrong. Implement a threshold-based alert system that checks metrics against defined limits and surfaces visual warnings when a KPI crosses a critical boundary.
Task 1: Monitor Three Metrics Against Thresholds (1 mark)
Requirements: Define at least three business metrics with upper or lower thresholds.
ALERT_THRESHOLDS = {
    "churn_rate": {
        "metric": "Churn Rate",
        "threshold": 7.0,
        "direction": "above",
        "severity": "critical",
        "message": "Churn exceeds safe limit. Investigate retention."
    },
    "avg_order_value": {
        "metric": "Avg Order Value",
        "threshold": 30.0,
        "direction": "below",
        "severity": "warning",
        "message": "AOV below target. Check pricing and product mix."
    },
    "null_percentage": {
        "metric": "Data Quality",
        "threshold": 5.0,
        "direction": "above",
        "severity": "warning",
        "message": "Null percentage too high. Check data pipeline."
    }
}
Validation: Three metrics defined with thresholds, directions, and messages.
Task 2: Display Visual Alerts (1 mark)
Requirements: When a threshold is breached, display a visual alert using st.error (critical) or st.warning (warning).
for key, config in ALERT_THRESHOLDS.items():
    value = current_metrics.get(key, 0)
    breached = False
    if config["direction"] == "above" and value > config["threshold"]:
        breached = True
    elif config["direction"] == "below" and value < config["threshold"]:
        breached = True

    if breached:
        alert_text = ("ALERT: " + config["metric"]
                      + " is " + str(round(value, 1))
                      + " (threshold: " + str(config["threshold"]) + "). "
                      + config["message"])
        if config["severity"] == "critical":
            st.error(alert_text)
        else:
            st.warning(alert_text)
Validation: Alerts appear at top of dashboard when thresholds are breached. Colour matches severity.
Task 3: Store Thresholds in Configuration (1 mark)
Requirements: Thresholds are defined in a dictionary or config file, not hardcoded in the display logic.
Validation: Changing a threshold value requires editing only the config dictionary, not the alert display code.
Task 4: Include Complete Alert Messages (1 mark)
Requirements: Each alert includes: metric name, current value, threshold value, and a plain-language risk description.
Validation: Read an alert message. It answers: what metric, what value, what limit, and what to do about it.
Task 5: Alerts Update on Filter Change (1 mark)
Requirements: When filter inputs change the underlying metric values, alerts recalculate and update.
Validation: Filter to a high-churn segment. Alert fires. Filter to a low-churn segment. Alert clears.
Submission
git add app.py alert_config.py
git commit -m "alerts: threshold monitoring with visual warnings"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * What a threshold-based alert is and why it is useful in an operational dashboard
    * How the visual alert is triggered and what Streamlit component displays it
    * Why thresholds are stored in configuration rather than hardcoded
    * Walk through one alert scenario showing what user sees when threshold is breached
    * Follow-up: how to add email notification when an alert is triggered
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.
2.57
Insight Sharing & Email Report Integration

Hey Insight Delivery Engineer!
Welcome. Your dashboard shows insights. But not every stakeholder opens the dashboard every day. Some need insights delivered to their inbox. This lesson teaches you to generate structured reports from your analysis output and deliver them via email - automating the last mile of insight sharing so findings reach the people who need them without manual effort.
Every insight that stayed in a dashboard nobody opened, every report that was requested but never sent, every stakeholder who said "I did not know about that" because they did not check the tool - all of these are delivery failures. The analysis was done. The insight existed. But it never reached the decision-maker. This lesson closes that gap.
The Real Scenario
THE PROBLEM
The weekly churn report is ready every Monday at 9 AM inside a Streamlit dashboard. The VP of Operations checks the dashboard on Tuesdays. The CEO never opens it. The sales team does not know it exists. By Wednesday, the analyst gets five Slack messages asking for the same numbers that have been available since Monday. The analyst spends Tuesday afternoon exporting CSVs and writing summary emails instead of doing analysis.
THE SOLUTION
Build a report generation function that produces a structured summary with KPIs, key findings, and recommendations. Send it via email using smtplib. The report arrives in every stakeholder's inbox Monday at 9:15 AM. No Slack requests. No manual exports. Insights reach people proactively.
Generating Structured Reports
Three Sections Every Report Needs: KPIs, Findings, Actions
Report generation function
def generate_report(df, report_date):
    """Generate a structured text report from analysis output."""
    revenue = df["revenue"].sum()
    customers = df["customer_id"].nunique()
    avg_order = df["revenue"].mean()

    report = []
    report.append("WEEKLY ANALYTICS REPORT")
    report.append("Date: " + str(report_date))
    report.append("")

    # Section 1: KPI Summary
    report.append("== KPI SUMMARY ==")
    report.append("Total Revenue: $" + f"{revenue:,.0f}")
    report.append("Active Customers: " + f"{customers:,}")
    report.append("Average Order Value: $" + f"{avg_order:,.0f}")
    report.append("")

    # Section 2: Key Finding
    report.append("== KEY FINDING ==")
    top_segment = (df.groupby("segment")["revenue"]
                   .sum().idxmax())
    report.append("Top performing segment: " + top_segment)
    report.append("")

    # Section 3: Recommended Action
    report.append("== RECOMMENDED ACTION ==")
    report.append("Review segment performance and allocate "
                  "resources to high-growth areas.")

    return "\n".join(report)
You just learned how to generate structured reports from analysis output. Now you will learn how to deliver them via email using smtplib.
Email Delivery With smtplib
Credentials From Environment Variables - Never Hardcoded
Email sending function
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_report_email(report_text, recipient):
    """Send report via email. Credentials from env vars."""
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials not configured. Skipping send.")
        return False

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = "Weekly Analytics Report"
    msg.attach(MIMEText(report_text, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email send failed: " + str(e))
        return False
Never hardcode credentials in source code
Email passwords, API keys, and SMTP credentials must live in environment variables or a .env file that is gitignored. Hardcoding credentials in your script means anyone who reads the code can access your email. Committing them to Git means they are in the history permanently. Use os.environ.get() and document required variables in .env.example.
Non-blocking error handling
Email failures must not crash the app or pipeline. The try-except block catches connection errors, authentication failures, and network issues. The function returns False on failure and logs the error. The calling code can show a warning but continues running. Stakeholders who did not receive the email can still access the dashboard directly.
You just learned how to send reports via email with credentials from environment variables and non-blocking error handling. Combined with report generation, you now have the complete insight delivery pipeline that moves findings from dashboards to inboxes automatically.
Integrating With the Streamlit App
A Send Report Button in the Dashboard
Dashboard integration
# In the Streamlit app
st.sidebar.header("Report Actions")
recipient = st.sidebar.text_input("Recipient Email")

if st.sidebar.button("Send Report"):
    if not recipient:
        st.sidebar.error("Enter a recipient email.")
    else:
        report = generate_report(filtered_df, datetime.now().date())
        success = send_report_email(report, recipient)
        if success:
            st.sidebar.success("Report sent to " + recipient)
        else:
            st.sidebar.error("Failed to send. Check email config.")
Insight sharing checklist
* Report generation function produces structured summary from current analysis
* Email delivery implemented with smtplib and credentials from environment variables
* Report includes KPI summary, key finding, and recommended action sections
* Email failure logs error but does not crash the app
* Credentials never hardcoded in the script
* CSV export also available as a download button alternative
You just learned how to build a complete insight delivery system with report generation, email sending, dashboard integration, and proper credential management. Insights now reach stakeholders automatically.

Insight Sharing & Email Report Integration


00h 59m 57s

Your dashboard produces insights. But not every stakeholder opens the dashboard daily. Build report generation and email delivery so findings reach stakeholders proactively without manual effort.
Task 1: Generate a Structured Report (1 mark)
Requirements: A function produces a structured summary (text, CSV, or HTML) from the current analysis output.
def generate_report(df, report_date):
    """Generate structured text report from analysis output."""
    revenue = df["revenue"].sum()
    customers = df["customer_id"].nunique()
    avg_order = df["revenue"].mean()

    lines = []
    lines.append("WEEKLY ANALYTICS REPORT")
    lines.append("Date: " + str(report_date))
    lines.append("")
    lines.append("== KPI SUMMARY ==")
    lines.append("Total Revenue: $" + f"{revenue:,.0f}")
    lines.append("Active Customers: " + f"{customers:,}")
    lines.append("Average Order: $" + f"{avg_order:,.0f}")
    lines.append("")
    lines.append("== KEY FINDING ==")
    top_seg = df.groupby("segment")["revenue"].sum().idxmax()
    lines.append("Top segment: " + top_seg)
    lines.append("")
    lines.append("== RECOMMENDED ACTION ==")
    lines.append("Allocate resources to high-growth segments.")
    return "\n".join(lines)
Validation: Function runs without errors. Output includes KPI summary, key finding, and recommendation.
Task 2: Implement Email Delivery (1 mark)
Requirements: Email delivery implemented using smtplib with credentials from environment variables.
import smtplib
import os
from email.mime.text import MIMEText

def send_report(report_text, recipient):
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    if not sender or not password:
        print("Email not configured. Skipping.")
        return False

    msg = MIMEText(report_text)
    msg["Subject"] = "Weekly Analytics Report"
    msg["From"] = sender
    msg["To"] = recipient

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Send failed: " + str(e))
        return False
Validation: Email function is implemented. Credentials read from environment variables.
Task 3: Report Has Three Required Sections (1 mark)
Requirements: The report includes at least: KPI summary, key finding, and recommended action.
Validation: Read the generated report. All three sections present with real computed values.
Task 4: Non-Blocking Error Handling (1 mark)
Requirements: Email failure logs an error but does not crash the app or pipeline.
Validation: Set invalid credentials. Run send function. Error is logged. App continues running.
Task 5: Credentials From Environment Variables (1 mark)
Requirements: SMTP credentials stored in environment variables. Never hardcoded. A .env.example file documents required variables.
# .env.example
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
Validation: No credentials appear in any committed file. .env.example shows required structure.
Submission
git add report_generator.py email_sender.py .env.example
git commit -m "reports: generate and email structured insight summaries"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * How the report is generated from current session analysis output
    * How email delivery is implemented and what library is used
    * Why credentials must be in environment variables, not source code
    * Walk through report content explaining what each section communicates
    * Follow-up: how to schedule automatic report delivery at a fixed time each day
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.58
Automated Data Pipeline Execution

Hey Pipeline Automation Engineer!
Welcome. Your app works interactively. But some tasks should run without human interaction: daily data refresh, weekly report generation, monthly aggregation. This lesson teaches you to build a Python pipeline script that ingests, cleans, aggregates, and outputs data in a single automated run - then schedule it with cron or GitHub Actions so it executes on a recurring schedule without anyone clicking a button.
Every manual data refresh that was forgotten on a holiday, every weekly report that was late because the analyst was sick, every aggregation that drifted because nobody remembered to rerun the script - these are automation failures. Pipelines run on schedule regardless of human availability. This lesson builds that reliability.
The Real Scenario
THE PROBLEM
An analyst runs a Jupyter notebook every Monday morning to refresh dashboard data. One Monday they are in a meeting until 11 AM. The dashboard shows last week's data until noon. Stakeholders make decisions based on stale numbers. The following week, the analyst is on vacation. Nobody else knows how to run the notebook. Dashboard data is a week old. Trust erodes.
THE SOLUTION
Convert the notebook into a pipeline script. The script accepts parameters, logs each stage, and outputs processed data. Schedule it with a GitHub Actions cron workflow. Every Monday at 6 AM, the pipeline runs automatically. By 6:05 AM, fresh data is ready. No human involvement. No forgotten refreshes. No stale dashboards.
Pipeline Script Structure
Ingest, Clean, Aggregate, Output - In One Script
Pipeline script with logging
import pandas as pd
import logging
import argparse
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def ingest(file_path):
    """Stage 1: Load raw data."""
    logger.info("Ingesting data from: " + file_path)
    df = pd.read_csv(file_path)
    logger.info("Ingested " + str(len(df)) + " rows")
    return df

def clean(df):
    """Stage 2: Clean and validate."""
    logger.info("Cleaning data...")
    initial = len(df)
    df = df.dropna(subset=["customer_id", "amount"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"] > 0]
    logger.info("Cleaned: " + str(initial) + " -> " + str(len(df)) + " rows")
    return df

def aggregate(df):
    """Stage 3: Compute aggregations."""
    logger.info("Aggregating...")
    agg = df.groupby("segment").agg(
        total_revenue=("amount", "sum"),
        order_count=("order_id", "count"),
        avg_order=("amount", "mean")
    ).reset_index()
    logger.info("Aggregated " + str(len(agg)) + " segments")
    return agg

def output(df, agg, output_dir):
    """Stage 4: Write output files."""
    logger.info("Writing output to: " + output_dir)
    df.to_csv(output_dir + "/cleaned_data.csv", index=False)
    agg.to_csv(output_dir + "/aggregated_metrics.csv", index=False)
    logger.info("Pipeline complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output")
    args = parser.parse_args()

    raw = ingest(args.input)
    cleaned = clean(raw)
    agg = aggregate(cleaned)
    output(cleaned, agg, args.output)
You just learned the four-stage pipeline pattern with logging and command-line arguments. Now you will learn how to schedule it with GitHub Actions.
Scheduling With GitHub Actions
Cron Syntax Schedules Your Pipeline to Run Without Human Triggers
GitHub Actions workflow with cron trigger
# .github/workflows/pipeline.yml
name: Weekly Data Pipeline

on:
  schedule:
    - cron: "0 6 * * 1"  # Every Monday at 6:00 AM UTC
  workflow_dispatch:       # Also allow manual trigger

jobs:
  run-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run pipeline
        run: python pipeline.py --input data/raw/latest.csv --output output

      - name: Commit output
        run: |
          git config user.name "Pipeline Bot"
          git config user.email "bot@example.com"
          git add output/
          git commit -m "pipeline: automated refresh" || echo "No changes"
          git push
Understanding cron syntax
Cron has five fields: minute, hour, day-of-month, month, day-of-week. 0 6 * * 1 means: minute 0, hour 6, any day of month, any month, Monday (1). Other examples: 0 0 * * * is daily at midnight. 0 9 1 * * is the first of every month at 9 AM.
You just learned how to schedule pipeline execution with GitHub Actions and cron syntax. Now you will learn why logging is essential for diagnosing pipeline failures.
Logging for Pipeline Diagnosis
When a Pipeline Fails at 3 AM, Logs Are Your Only Witness
What to log at each stage
Log the start and end of each stage with timestamps. Log row counts at ingestion and after cleaning so you can see how much data was removed. Log aggregation results. Log output file paths. Log any warnings about data quality. When the pipeline fails, the logs tell you exactly which stage failed, what data was processed, and what the last successful operation was. Without logs, debugging a scheduled pipeline is guesswork.
Pipeline automation checklist
* Single script runs complete pipeline: ingest, clean, aggregate, output
* Parameters accepted via command-line arguments or config file
* Logging with timestamps at each stage using Python logging module
* Scheduled with GitHub Actions cron trigger or manual dispatch
* Output written to defined path and confirmed by log entry
* Pipeline differences from notebooks: no manual steps, reproducible, scheduled
You just learned how to build an automated data pipeline with logging, scheduling, and parameterisation. Your analytics product now refreshes itself on schedule without human intervention.

Automated Data Pipeline Execution


00h 59m 55s

Your analytics currently requires manual script execution. Build a Python pipeline that ingests, cleans, aggregates, and outputs processed data in a single run. Schedule it with GitHub Actions so it executes on a recurring schedule without human intervention.
Task 1: Build the Complete Pipeline Script (1 mark)
Requirements: A single Python script runs: ingestion, cleaning, aggregation, and output.
import pandas as pd
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def ingest(path):
    logger.info("Ingesting: " + path)
    df = pd.read_csv(path)
    logger.info("Rows ingested: " + str(len(df)))
    return df

def clean(df):
    logger.info("Cleaning...")
    initial = len(df)
    df = df.dropna(subset=["customer_id", "amount"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"] > 0]
    logger.info("Cleaned: " + str(initial) + " -> " + str(len(df)))
    return df

def aggregate(df):
    logger.info("Aggregating...")
    agg = df.groupby("segment").agg(
        revenue=("amount", "sum"),
        orders=("order_id", "count")
    ).reset_index()
    logger.info("Segments: " + str(len(agg)))
    return agg

def output(df, agg, out_dir):
    df.to_csv(out_dir + "/cleaned.csv", index=False)
    agg.to_csv(out_dir + "/aggregated.csv", index=False)
    logger.info("Output written to: " + out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output")
    args = parser.parse_args()
    raw = ingest(args.input)
    cleaned = clean(raw)
    agg = aggregate(cleaned)
    output(cleaned, agg, args.output)
Validation: Run python pipeline.py --input data/raw/test.csv --output output. Output files are created.
Task 2: Accept Parameters via CLI or Config (1 mark)
Requirements: Pipeline accepts file path and output directory via command-line arguments or a config file.
Validation: Run with different --input and --output values. Pipeline adapts without code changes.
Task 3: Implement Logging With Timestamps (1 mark)
Requirements: Each pipeline stage logs with timestamps using Python logging module.
Validation: Run pipeline. Log output shows timestamp, level, and message for each stage.
Task 4: Schedule With GitHub Actions (1 mark)
Requirements: A GitHub Actions workflow with cron trigger runs the pipeline on a schedule.
# .github/workflows/pipeline.yml
name: Weekly Pipeline
on:
  schedule:
    - cron: "0 6 * * 1"  # Monday 6AM UTC
  workflow_dispatch:
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python pipeline.py --input data/raw/latest.csv --output output
      - run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add output/
          git commit -m "pipeline: auto refresh" || echo "No changes"
          git push
Validation: Workflow YAML committed. Cron syntax correct. Manual dispatch available for testing.
Task 5: Confirm Output With Log Entry (1 mark)
Requirements: Pipeline completion confirmed by a log entry and output files written to the defined path.
Validation: After pipeline run, output directory contains expected files. Logs show "Pipeline complete" or equivalent.
Submission
git add pipeline.py .github/workflows/pipeline.yml
git commit -m "pipeline: automated ingest-clean-aggregate-output with scheduling"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * What an automated pipeline is and how it differs from notebook-based analysis
    * How cron syntax works and what schedule was configured
    * How logging helps diagnose pipeline failure without manual inspection
    * Walk through pipeline stages explaining what each step does
    * Follow-up: how to alert someone if the pipeline fails during a scheduled run
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public

2.59
GitHub Workflow Automation & Validation

Hey CI/CD Automation Specialist!
Welcome. Your pipeline runs on schedule. But what happens when someone pushes code that breaks the data schema? What if a column is renamed and your pipeline silently produces wrong results? This lesson teaches you to write GitHub Actions workflows that trigger validation scripts on every push, checking that data meets expected schema and quality standards before bad changes reach production.
Every silent data failure - the column that was renamed without updating downstream code, the data type that changed from integer to string, the new null values that appeared after a pipeline change - could have been caught by automated validation. This lesson teaches you to build the safety net that catches these problems on every push.
The Real Scenario
THE PROBLEM
A developer renames a column from "customer_id" to "cust_id" in the data pipeline. They push the change. The pipeline runs. The dashboard breaks because it still references "customer_id". Nobody notices until Monday morning when the VP opens the dashboard and sees an error. The column rename was three days ago. Three days of data are now incorrect. The schema change was never validated against downstream dependencies.
THE SOLUTION
A GitHub Actions workflow runs a validation script on every push. The script checks: are required columns present? Are data types correct? Is the minimum row count met? If any check fails, the workflow fails and blocks the merge. The developer sees the failure immediately, fixes the schema issue, and pushes again. Bad changes never reach production.
Writing the Validation Script
A Python Script That Checks Schema and Quality
Validation script
# validate_data.py
import pandas as pd
import sys

def validate(file_path):
    """Run all validation checks. Exit 1 on failure."""
    print("Validating: " + file_path)
    df = pd.read_csv(file_path)

    errors = []

    # Check 1: Required columns exist
    required_cols = ["customer_id", "order_id", "amount", "date", "segment"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        errors.append("Missing required columns: " + str(missing))
    else:
        print("PASS: All required columns present")

    # Check 2: Data types
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("Column 'amount' is not numeric")
        else:
            print("PASS: amount column is numeric")

    # Check 3: Minimum row count
    min_rows = 100
    if len(df) < min_rows:
        errors.append(
            "Row count " + str(len(df))
            + " below minimum " + str(min_rows)
        )
    else:
        print("PASS: Row count " + str(len(df)) + " meets minimum")

    # Check 4: No fully null columns
    null_cols = [c for c in df.columns if df[c].isnull().all()]
    if null_cols:
        errors.append("Fully null columns: " + str(null_cols))
    else:
        print("PASS: No fully null columns")

    # Report results
    if errors:
        print("\nVALIDATION FAILED:")
        for e in errors:
            print("  ERROR: " + e)
        sys.exit(1)
    else:
        print("\nALL CHECKS PASSED")
        sys.exit(0)

if __name__ == "__main__":
    validate(sys.argv[1])
You just learned how to write a validation script that checks schema, types, and row counts. Now you will learn how to trigger it automatically with a GitHub Actions workflow.
GitHub Actions Workflow for Validation
Trigger on Push, Fail on Bad Data, Block the Merge
Workflow YAML
# .github/workflows/validate.yml
name: Data Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install pandas

      - name: Run data validation
        run: python validate_data.py data/processed/cleaned_data.csv
How the workflow blocks merges
When the validation script calls sys.exit(1), the GitHub Actions step fails. A failed step causes the entire workflow to fail. In repository settings, you can require this workflow to pass before PRs can be merged. This creates a gate: no data change can reach main unless it passes all validation checks.
You just learned how to trigger validation on every push and block merges on failure. Now you will learn what schema drift is and why catching it matters.
Understanding Schema Drift
When Data Shape Changes Without Warning
What schema drift is
Schema drift is when the structure of your data changes over time: columns are added, renamed, removed, or change data type. A billing system update adds a "discount_code" column. A CRM migration renames "customer_id" to "account_id". An API change returns amounts as strings instead of floats. Each of these is schema drift. Without validation, drift silently breaks downstream code.
Why validating on every push prevents silent failures
By checking schema on every push, you catch drift the moment it appears - not days or weeks later when a dashboard breaks. The validation script is your contract: "this data must have these columns, these types, and this minimum quality." Any violation is caught immediately. The developer who introduced the change sees the failure in their PR and fixes it before merging.
GitHub workflow validation checklist
* Workflow YAML triggers on push to main or specified branches
* Validation checks required columns, expected dtypes, and minimum row count
* Failed validation causes workflow failure and blocks merge
* Logs clearly show which check passed or failed with descriptive messages
* Validation logic in a separate Python script for maintainability
* Schema drift detected and prevented on every code change
You just learned how to implement automated data validation with GitHub Actions, catch schema drift on every push, and block bad changes from reaching production. Your data pipeline now has a quality gate that prevents silent failures.

GitHub Workflow Automation & Validation


00h 59m 55s

Your pipeline runs on schedule. But what if someone pushes a code change that breaks the data schema? Implement a GitHub Actions workflow that triggers data validation on every push and blocks merges when validation fails.
Task 1: Create GitHub Actions Workflow (1 mark)
Requirements: A YAML workflow triggers on push to main or a specified branch.
# .github/workflows/validate.yml
name: Data Validation
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pandas
      - run: python validate_data.py data/processed/cleaned_data.csv
Validation: Workflow YAML committed in .github/workflows/. Triggers on push events.
Task 2: Write Validation Script (1 mark)
Requirements: Script checks required columns, expected dtypes, and minimum row count.
# validate_data.py
import pandas as pd
import sys

def validate(path):
    df = pd.read_csv(path)
    errors = []

    # Required columns
    required = ["customer_id", "order_id", "amount", "date", "segment"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        errors.append("Missing columns: " + str(missing))
    else:
        print("PASS: Required columns present")

    # Data types
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("amount column is not numeric")
        else:
            print("PASS: amount is numeric")

    # Minimum rows
    if len(df) < 100:
        errors.append("Row count " + str(len(df)) + " below minimum 100")
    else:
        print("PASS: Row count " + str(len(df)) + " meets minimum")

    # Null columns
    null_cols = [c for c in df.columns if df[c].isnull().all()]
    if null_cols:
        errors.append("Fully null columns: " + str(null_cols))
    else:
        print("PASS: No fully null columns")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  ERROR: " + e)
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")

if __name__ == "__main__":
    validate(sys.argv[1])
Validation: Run locally. Script checks all conditions and reports pass/fail clearly.
Task 3: Failed Validation Blocks Merge (1 mark)
Requirements: When validation fails, the workflow exits with non-zero code, causing the GitHub Actions job to fail.
Validation: Commit a file with a missing required column. Push. Workflow fails. Fix and push. Workflow passes.
Task 4: Clear Pass/Fail Logging (1 mark)
Requirements: Workflow logs show which validation check passed or failed with descriptive messages.
Validation: Check GitHub Actions run logs. Each check shows PASS or ERROR with the specific detail.
Task 5: Validation Logic Separate From Workflow (1 mark)
Requirements: Validation logic lives in a Python script (validate_data.py), not inline in the YAML file.
Validation: validate_data.py exists as a separate file. YAML calls it with python validate_data.py.
Submission
git add validate_data.py .github/workflows/validate.yml
git commit -m "validation: automated schema checks on push with merge blocking"
git push
Submit:
1. GitHub PR link
2. Video (3-5 minutes) covering:
    * What GitHub Actions is and how a workflow triggers on push
    * What schema drift means and why validating on every push prevents silent failures
    * How a failed validation step causes workflow failure and blocks merge
    * Walk through validation checks explaining what each one catches
    * Follow-up: how to add a notification step that alerts the team on validation failure
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

2.60
Data Product Documentation & Delivery

Hey Documentation Champion!
Welcome. Your data product is built: upload, filters, KPIs, charts, alerts, email delivery, pipeline automation, and validation. One thing remains. Without documentation, nobody can maintain it, extend it, or trust it. This lesson teaches you to write a structured README that covers dataset description, pipeline architecture, setup instructions, feature explanations, and known limitations - the document that makes your product delivery-ready.
Every data product that was abandoned after the original developer left, that no new team member could set up, that had undocumented assumptions baked into the code - all shared one root cause: inadequate documentation. The product worked. Nobody knew how. This lesson ensures your product is not just functional but maintainable, reviewable, and delivery-ready.
The Real Scenario
THE PROBLEM
The original developer leaves the company. A new analyst inherits the project. The README says "Analytics Dashboard" with no setup instructions. The analyst clones the repo, runs the app, gets an import error. Asks the team how to set it up. Nobody knows. Spends three days reverse-engineering the environment, the data sources, and the feature logic. Three days of productivity lost because 30 minutes of documentation was never written.
THE SOLUTION
A comprehensive README with five sections: project overview, setup instructions, pipeline architecture, feature documentation, and known limitations. The new analyst clones the repo, reads the README, runs four commands, and has the app running in 10 minutes. Every feature is documented. Every assumption is stated. Every limitation is acknowledged. The product is self-documenting.
README Structure for Data Products
Five Sections That Make Any Data Product Maintainable
1. Overview
What this project does and who it serves
One paragraph. State the business problem, the solution approach, and who the users are. "An interactive analytics dashboard that ingests sales data, computes KPIs, detects threshold breaches, and delivers weekly reports. Built for the operations and sales teams."
2. Setup
Exact commands to go from git clone to running app
Numbered steps with copy-paste commands. Clone, create venv, activate, install requirements, configure .env, run. Must work on macOS, Linux, and Windows. If a new contributor cannot follow these steps without asking, the Setup section is incomplete.
3. Pipeline
Step-by-step data flow from raw input to final output
Describe each pipeline stage: ingestion (source, format), cleaning (rules applied), aggregation (what is computed), output (format, destination). Include a text-based flow diagram. This section lets anyone trace how data moves through the system.
4. Features
Every derived column, KPI, and dashboard feature documented
List every engineered column with name, type, description, and example value. Document every KPI with its formula and data source. Describe every dashboard section. This prevents the "what does this column mean?" question that wastes hours.
5. Limitations
Known issues, assumptions, and data quality caveats
State what the product does NOT do. Document assumptions: "Revenue excludes refunds." "Data refreshes weekly, not real-time." "Segments are based on self-reported category, not purchase behaviour." Documenting limitations is more important than hiding them. Reviewers trust transparent documentation.
You just learned the five-section README structure for data products. Now you will learn how to document the pipeline architecture with a data flow diagram.
Documenting Pipeline Architecture
A Text-Based Flow Diagram Anyone Can Read
Pipeline architecture documentation
Data Flow:
  CSV Upload --> Ingestion --> Cleaning --> Aggregation --> Dashboard
                    |              |             |              |
                 raw data    drop nulls     group by      KPIs + charts
                 validation  type cast      segment       alerts
                             filter neg     compute       email reports
Each stage documented with: input format, transformations applied, output format, and where the output goes next. This diagram is the map of your entire data product. Anyone reading it understands the system in 30 seconds.
You just learned how to document pipeline architecture with a flow diagram. Now you will learn how to document derived features and known limitations.
Documenting Features and Limitations
Transparency Builds Trust - Document What Works and What Does Not
Feature documentation table
## Derived Features

| Column           | Type    | Description                          | Example   |
|------------------|---------|--------------------------------------|-----------|
| revenue_30d      | float   | Sum of order amounts in last 30 days | 4523.50   |
| days_since_order | integer | Days elapsed since last order        | 12        |
| churn_risk       | string  | Risk category based on activity      | "high"    |
| segment_rank     | integer | Revenue rank within segment          | 3         |
Known limitations section
## Known Limitations

- Data refreshes weekly via scheduled pipeline. Dashboard does not show
  real-time data. Maximum staleness: 7 days.
- Revenue metric excludes refunded orders. Net revenue after refunds
  is not currently computed.
- Segment classification is based on self-reported category field.
  Customers who changed segments mid-year appear in their latest segment.
- Alert thresholds are static. No dynamic threshold adjustment based on
  seasonal patterns or historical variance.
- Email delivery requires SMTP configuration. If credentials are not
  set, email features are silently disabled.
Documenting limitations is a strength, not a weakness
Reviewers and stakeholders trust documentation that states limitations openly. A README that only describes what works feels incomplete. A README that says "here is what works, here is what does not, and here is why" demonstrates professional maturity and helps future developers prioritise improvements.
Documentation quality checklist
* Project overview, dataset description, setup instructions, and usage guide included
* Pipeline architecture described with step-by-step data flow
* Every derived feature documented with name, type, description, and example
* Known limitations and assumptions explicitly stated
* Getting Started section allows a new contributor to run from scratch without help
* README updated whenever the product changes
You just learned how to write professional documentation that makes a data product maintainable, reviewable, and delivery-ready. This is the final skill in the end-to-end data product journey: from dataset to documented, deployed, and delivered insights.

Data Product Documentation & Delivery


00h 59m 56s

Your data product is complete: upload, filters, KPIs, charts, alerts, email reports, pipeline, and validation. Write comprehensive documentation that makes the product maintainable, reviewable, and delivery-ready for any team member who inherits it.
Task 1: Write Complete README (1 mark)
Requirements: README includes: project overview, dataset description, setup instructions, and full usage guide.
# Sales Analytics Dashboard

Interactive analytics dashboard that ingests sales data, computes
KPIs, detects threshold breaches, and delivers weekly reports.
Built for the operations and sales teams.

## Dataset

- Source: CSV upload or scheduled pipeline ingestion
- Columns: customer_id, order_id, amount, date, segment
- Refresh: Weekly via GitHub Actions pipeline

## Setup

1. Clone the repository
   git clone https://github.com/team/analytics-dashboard.git
   cd analytics-dashboard

2. Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Configure environment
   cp .env.example .env
   # Edit .env with your SMTP credentials

5. Run the app
   streamlit run app.py

## Usage

Upload a CSV file or let the pipeline load data automatically.
Use sidebar filters to explore. Check KPI cards for status.
Review alerts for threshold breaches. Send reports via email.
Validation: A new contributor follows the README and runs the project without asking questions.
Task 2: Document Pipeline Architecture (1 mark)
Requirements: Step-by-step flow showing data movement across all stages.
## Pipeline Architecture

CSV Upload / Scheduled Ingest
        |
    Ingestion: Load raw CSV, validate file format
        |
    Cleaning: Drop nulls, cast types, filter invalid rows
        |
    Aggregation: Group by segment, compute revenue and order count
        |
    Output: Write cleaned.csv and aggregated.csv to output/
        |
    Dashboard: Load processed data, compute KPIs, render charts
        |
    Alerts: Check metrics against thresholds, display warnings
        |
    Reports: Generate summary, send via email
Validation: Architecture describes every stage from raw data to final output.
Task 3: Document Derived Features (1 mark)
Requirements: Every derived or engineered column documented with name, type, description, and example.
## Derived Features

| Column           | Type    | Description                          | Example  |
|||--|-|
| revenue_30d      | float   | Sum of order amounts last 30 days    | 4523.50  |
| days_since_order | integer | Days since most recent order         | 12       |
| churn_risk       | string  | Risk category based on activity      | "high"   |
| null_pct         | float   | Percentage of null values per column | 2.3      |
Validation: Every derived column in the codebase is listed with a clear description.
Task 4: Document Known Limitations (1 mark)
Requirements: Known limitations, assumptions, and data quality issues listed in a dedicated section.
## Known Limitations

- Data refreshes weekly. Dashboard does not show real-time data.
- Revenue excludes refunded orders.
- Segment classification based on self-reported category field.
- Alert thresholds are static (no seasonal adjustment).
- Email delivery requires SMTP configuration in .env file.
- Pipeline assumes CSV with specific column names.
Validation: Limitations are honest, specific, and helpful for future developers.
Task 5: Getting Started Section (1 mark)
Requirements: A new contributor can run the project from scratch by following the Getting Started section alone.
Test: Give the README to someone who has never seen the project. Can they run the app in under 10 minutes without asking a single question? If yes, the documentation passes.
Validation: Four commands or fewer to go from git clone to running app. No ambiguous steps.
Submission
git add README.md
git commit -m "docs: comprehensive project documentation for delivery"
git push
Submit:
1. GitHub PR link with complete README
2. Video (3-5 minutes) covering:
    * What makes a README professional rather than a placeholder file
    * How pipeline architecture was documented and what detail was included
    * Why documenting known limitations matters more than hiding them
    * Walk through README section by section explaining purpose of each part
    * Follow-up: how to update README if a new data source was added to the pipeline
This assignment covers the following concepts


Github PR URL*

Ensure the shared url is active and accessible.
Video Explaination URL*

Ensure you're clearly visible on the video while explaining your submission and is shared public.

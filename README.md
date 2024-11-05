# Graduation Project
### Repository Guidelines
1) Don't push to the main branch directly
2) Create a branch for the task or the change you want to make (This is to reduce conflicts)
3) Create a pull request with every change you want to commit to the main branch
4) **Unit tests**: We won't be able to handle a lot of functionality without Unit tests
5) Do **NOT** push secrets (ex. api keys)
6) Use meaningful names for commits
7) Struggling with GIT? Ask **Pavly**

### How to run?
Ensure Python 3.10.6 and .NET 8 are installed
You can run locally by executing the following command:

`python util/local_runner.py`

This script will automatically install the dependencies needed (if not installed already) and run both the web api and the AI api.

### Getting Started

#### Clone the Repository

`git clone https://github.com/Pevooo/graduation-project.git`

### How to contribute?

#### Step 1A: Create a new branch

`git checkout -b "branch_name"`

#### Step 1B: Or switch to an existing branch

`git checkout "existing_branch_name"`

#### Step 2: Commit to the branch

`git add .`

`git commit -m "Meaningful Commit Message"`

`git push --set-upstream origin "branch_name"`

**Note:** this should create a pull request with the changes

#### Step 3: Wait for review
at least one review is needed
#### Step 4: Merge :)

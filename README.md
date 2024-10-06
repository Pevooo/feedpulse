# Graduation Project
## Repository Guidelines
1) Don't push to the main branch directly
2) Create a branch for the task or the change you want to make (This is to reduce conflicts)
3) Creste a pull request with every change you want to commit to the main branch
4) **Unit tests**: We won't be able to handle a lot of functionality without Unit tests
5) Do **NOT** push secrets (ex. api keys)
6) Use meaningful names for commits
7) Struggling with GIT? Ask **Pavly**

## Getting Started

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

At least one review is needed

#### Step 4: Squash and Merge

This should merge your commits into one commit and merge it with main

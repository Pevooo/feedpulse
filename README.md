# Graduation Project
## Repository Guidelines
1) Don't push to the main branch directly
2) Create a branch for the task or the change you want to make (This is to reduce conflicts)
3) Create a pull request with every change you want to commit to the main branch
4) **Unit tests**: We won't be able to handle a lot of functionality without Unit tests
5) Do **NOT** push secrets (ex. api keys)
6) Use meaningful names for commits
7) Struggling with GIT? Ask **Pavly**

## How to run?
Ensure Python 3.10.6 and .NET 8 are installed
You can run locally by executing the following command:

`python util/local_runner.py`

This script will automatically install the dependencies needed (if not installed already) and run both the web api and the AI api.

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
at least one review is needed

#### Step 4: Merge :)

## Project Architecture

![Project Architecture](https://github.com/user-attachments/assets/467a8027-c5ad-44ed-8ec6-92e63ceeccdc)

## Working Manual

### Flask Layer
If working in the Flask Layer:

create an instance of `FeedPulseController` to communicate with other components 
(reports handler, feedback classifier, topic detector, etc...).
Do not directly use the Data Manipulation Layer components
### API Controller Layer
This layer works as a link between the Data Manipulation Layer and the Flask Layer

If working in the API Controller Layer:

communicate with Data Manipulation Layer by using the provided instances of its components.
Do not directly manipulate tha data units

### Data Manipulation Layer
If working in the Data Manipulation Layer:

Components in this layer directly manipulate the data and work with LLMs

This layer consists of 4 main components which are:
- **Data Providers**: responsible for fetching the data from social media platforms, organizing them in `DataUnits`
- **Feedback Classification:** responsible for categorizing the feedback into positive and negative feedbacks
- **Topic Detection:** responsible for extracting the topic(s) that the feedback relates to (given a set of topics)
- **Report Handler:** responsible for creating the reports and sending them to the organization

### Angular App
This layer represents the full functionality of the user interface

### ASP.NET APP
This layer represents the full backend functionality of storing data in database

## LLM Models

|      Model       |    Type     |
|:----------------:|:-----------:|
|    GPT4o-mini    |   Online    |
|    Phi3-mini     |   Offline   |
| Gemini-1.5-flash |   Online    |
|      Llama3      | Coming Soon |
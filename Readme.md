### Project Structure 
LLMAgent/
├── .env
├── pyproject.toml
├── poetry.lock
├── sample_notebook.ipynb
└── README.md (optional)

### Step 1: Create a New Poetry Project
1. Open a terminal and create a new directory for your project
2. Initialize a new Poetry project
`poetry init`
3. Add Required Dependencies
- poetry add `langchain `
- poetry add `python-dotenv `
- poetry add `huggingface_hub` 
- poetry add `googlesearch-results` 
- poetry add `tiktoken`
- poetry add `jupyter`  # Required for running .ipynb files

### Set Up the Poetry Virtual Environment
poetry shell

### Conda version
conda --version
#### Export the dependencies to ENV.txt file 
poetry export -f requirements.txt --output requirements.txt --without-hashes

#### Conda environment list 
conda env list
base                  *  /opt/anaconda3
LLMAgentEnv              /opt/anaconda3/envs/LLMAgentEnv
conda activate LLMAgentEnv

#### Conda create new env from existing yml dependencies 
conda env create -n LLMAgentEnv --file /Users/anjandebnath/Documents/PythonWorkspace/LLMAgent/environment.yml

#### Launch Navigator from Terminal
anaconda-navigator
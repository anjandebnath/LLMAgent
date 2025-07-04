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

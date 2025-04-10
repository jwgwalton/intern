# Intern

This project is to build an agent that can help with your daily work tasks


# Local development
This project uses uv for dependency management, environment management, and running the project. To install uv, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
````


To install the dependencies, run:



```bash
uv sync
```
This command will:

```commandline
  1. Find or download an appropriate Python version to use.
  2. Create and set up your environment in the .venv folder.
  3. Build your complete dependency list and write to your uv.lock file.
  4. Sync your project dependencies into your virtual environment.
```


You can run the project with the following command:

```bash
uv run
```

which is equivalent to

```bash
uv sync
source .venv/bin/activate
python manage.py runserver
```

# Roadmap
- Create initial ReAct agent 
    - Backed with DuckDuckGo
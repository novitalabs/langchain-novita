# langchain-novita

Novita sandbox backend integration for LangChain Deep Agents.

[Novita](https://novita.ai) provides code interpreter sandboxes for running commands in isolated environments. See the [Novita docs](https://novita.ai/docs/guides/introduction) for signup, authentication, and platform details.

## Installation

```bash
pip install -U langchain-novita
```

```bash
uv add langchain-novita
```

Set your Novita credentials:

```bash
export NOVITA_API_KEY="your-api-key"
```

## Create a sandbox backend

In Python, create the sandbox using the Novita SDK, then wrap it with the Deep Agents backend:

```python
from novita_sandbox.code_interpreter import Sandbox

from langchain_novita import NovitaSandbox

sandbox = Sandbox.create()
backend = NovitaSandbox(sandbox=sandbox)

result = backend.execute("echo hello")
print(result.output)
```

## Use with Deep Agents

Novita's LLM API is compatible with OpenAI's Chat Completions API. To use Novita models with Deep Agents, install `langchain-openai` and configure `ChatOpenAI` with Novita's base URL.

```bash
pip install -U langchain-openai
```

Set the model ID:

```bash
export NOVITA_MODEL_ID="deepseek/deepseek-v4-pro"
```

```python
import os

from langchain_openai import ChatOpenAI
from novita_sandbox.code_interpreter import Sandbox

from deepagents import create_deep_agent
from langchain_novita import NovitaSandbox

sandbox = Sandbox.create()
backend = NovitaSandbox(sandbox=sandbox)

model = ChatOpenAI(
    model=os.environ["NOVITA_MODEL_ID"],
    api_key=os.environ["NOVITA_API_KEY"],
    base_url="https://api.novita.ai/openai",
)

agent = create_deep_agent(
    model=model,
    system_prompt="You are a coding assistant with sandbox access.",
    backend=backend,
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Create a hello world Python script and run it"}
        ]
    }
)
```

## Cleanup

You are responsible for managing the sandbox lifecycle via the Novita SDK. When you are done, kill the sandbox:

```python
sandbox.kill()
```

## Testing

Install test dependencies:

```bash
poetry install --with test
```

Run unit tests:

```bash
poetry run pytest tests/unit_tests
```

Run the standard sandbox integration tests:

```bash
export NOVITA_API_KEY="your-api-key"
poetry run pytest tests/integration_tests/test_sandbox.py
```

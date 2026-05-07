# NovitaSandbox integration

> Integrate with the NovitaSandbox sandbox backend using LangChain Python.

[Novita](https://novita.ai) provides code interpreter sandboxes for running commands in isolated environments. See the [Novita docs](https://novita.ai/docs/guides/introduction) for signup, authentication, and platform details.

## Installation

Install the Novita integration with the optional sandbox dependencies:

```bash
pip install -U langchain-novita
```

```bash
uv add langchain-novita
```

If you want to use Novita's OpenAI-compatible chat completions endpoint with Deep Agents, also install `langchain-openai`:

```bash
pip install -U langchain-openai
```

Set your Novita credentials:

```bash
export NOVITA_API_KEY="your-api-key"
export NOVITA_BASE_URL="your-openai-compatible-base-url"
export NOVITA_MODEL_ID="your-model-id"
```

## Create a sandbox backend

In Python, create the sandbox using the Novita SDK, then wrap it with the [Deep Agents backend](https://docs.langchain.com/oss/python/deepagents/backends).

```python
from novita_sandbox.code_interpreter import Sandbox

from langchain_novita import NovitaSandbox

sandbox = Sandbox.create()
backend = NovitaSandbox(sandbox=sandbox)

result = backend.execute("echo hello")
print(result.output)
```

## Use with Deep Agents

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
    base_url=os.environ["NOVITA_BASE_URL"],
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

You are responsible for managing the sandbox lifecycle via the Novita SDK.
When you are done, kill the sandbox.

```python
sandbox.kill()
```

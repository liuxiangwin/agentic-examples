import os
import uuid

import fire

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.client_tool import client_tool
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.react.agent import ReActAgent


@client_tool
def dummy_tool(query: str = "dummy_tool"):
    """
    Answer information about dummy_tool.

    :param query: The query to use for querying the internet
    :returns: Information about torchtune
    """
    dummy_tool = """
            torchtune is a PyTorch library for easily authoring, finetuning and experimenting with LLMs.

            torchtune provides:

            PyTorch implementations of popular LLMs from Llama, Gemma, Mistral, Phi, and Qwen model families
            Hackable training recipes for full finetuning, LoRA, QLoRA, DPO, PPO, QAT, knowledge distillation, and more
            Out-of-the-box memory efficiency, performance improvements, and scaling with the latest PyTorch APIs
            YAML configs for easily configuring training, evaluation, quantization or inference recipes
            Built-in support for many popular dataset formats and prompt templates
    """
    return dummy_tool


def main(host: str, port: int):
    client = LlamaStackClient(
        base_url=f"http://{host}:{port}",
        provider_data={"tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY")},
    )

    model="meta-llama/Llama-3.2-3B-Instruct",

    agent = ReActAgent(
        client=client,
        model=model,
        tools=[
            "builtin::websearch",
            dummy_tool
        ],
        json_response_format=True,
    )

    session_id = agent.create_session(f"test-session-{uuid.uuid4().hex}")

    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": "Whats the best place in new york for a pizza slice at 2am ?",
            }
        ],
        session_id=session_id,
        stream=True,
    )
    for log in EventLogger().log(response):
        log.print()

    response2 = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": "What are the popular llms supported in torchtune?",
            }
        ],
        session_id=session_id,
        stream=True,
    )
    for log in EventLogger().log(response2):
        log.print()


if __name__ == "__main__":
    fire.Fire(main)
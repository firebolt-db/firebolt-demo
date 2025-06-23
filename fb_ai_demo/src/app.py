import json
import os

import chainlit as cl
from openai import OpenAI

import firebolt_connection
import tools

# TODO: Switch to the async client. Chainlit works better with coroutines.
client = OpenAI()


@cl.on_chat_start
async def on_chat_start():
    print("Start new chat session.")
    cl.user_session.set(
        "messages",
        [
            {
                "role": "system",
                "content": open(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "system_prompt.md"
                    )
                ).read(),
            },
        ],
    )
    cl.user_session.set("fb_connection", firebolt_connection.FireboltConnection())
    await cl.ChatSettings(
        [
            cl.input_widget.Switch(
                id="ask_permission",
                label="Ask for permission before executing a query?",
                initial=False,
            ),
        ]
    ).send()
    cl.user_session.set("ask_permission", False)


@cl.on_chat_end
def on_chat_end():
    print("Terminate the chat session.")
    # TODO: Close the Firebolt connection.


@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("ask_permission", settings["ask_permission"])


@cl.on_message
async def main(msg: cl.Message):
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": msg.content})

    interactive_tool_calls = []
    while True:
        with client.beta.chat.completions.stream(
            model="gpt-4o",
            messages=messages,
            tools=tools.tools,
        ) as stream:
            msg = cl.Message(content="")
            tool_calls = {}
            for event in stream:
                if event.type == "chunk":
                    # print(
                    #     f"'chunk' event. Chunk {event.chunk}, snapshot {event.snapshot}",
                    #     end="\n\n\n",
                    # )
                    pass
                elif event.type == "content.delta":
                    # print(
                    #     f"'content.delta' event. Delta {event.delta}, snapshot {event.snapshot}, parsed {event.parsed}",
                    #     end="\n\n\n",
                    # )
                    await msg.stream_token(event.delta)
                elif event.type == "content.done":
                    # print(
                    #     f"'content.done' event. content {event.content}, parsed {event.parsed}",
                    #     end="\n\n\n",
                    # )
                    pass
                elif event.type == "tool_calls.function.arguments.delta":
                    # print(
                    #     f"'tool_calls.function.arguments.delta' event. name {event.name}, index {event.index}, arguments {event.arguments}, parsed_arguments {event.parsed_arguments}, arguments_delta {event.arguments_delta}",
                    #     end="\n\n\n",
                    # )
                    pass
                elif event.type == "tool_calls.function.arguments.done":
                    # print(
                    #     f"'tool_calls.function.arguments.done' event. name {event.name}, index {event.index}, arguments {event.arguments}, parsed_arguments {event.parsed_arguments}",
                    #     end="\n\n\n",
                    # )
                    assert event.index not in tool_calls
                    tool_calls[event.index] = {
                        "name": event.name,
                        "arguments": event.arguments,
                    }
                else:
                    print(f"Unexpected event type: {event.type}", end="\n\n\n")
                    assert False, f"Unexpected event type: {event.type}"

        await msg.update()
        final_completion = stream.get_final_completion()
        messages.append(final_completion.choices[0].message)
        if tool_calls:
            for tool_call in final_completion.choices[0].message.tool_calls:
                assert tool_call.index in tool_calls
                tool_calls[tool_call.index]["id"] = tool_call.id
            tool_call_responses = await tools.call_tools(tool_calls.values())
            interactive_tool_calls.extend(
                tc
                for rsp, tc in zip(tool_call_responses, tool_calls.values())
                if (
                    tc["name"] == "build_data_visualization"
                    or tc["name"] == "build_sql_query"
                )
                and rsp["content"] == "Success"
            )
            # Do another iteration to return the results of the tool calls to the LLM.
            messages.extend(tool_call_responses)
            continue

        print(f"Messages:\n{messages}", end="\n\n\n")
        break

    for tool_call in interactive_tool_calls:
        if tool_call["name"] == "build_data_visualization":
            vega_element = cl.CustomElement(
                name="editor",
                props={
                    # We need to double-load here as the JSON result within the tool call is a string.
                    "spec": json.loads(json.loads(tool_call["arguments"])["vega_spec"]),
                    # Here loading once is fine, as the result is SQL, not JSON.
                    "sql": json.loads(tool_call["arguments"])["sql_query"],
                },
                display="page",
            )
            await cl.Message(
                content="Open the editor to look at the data visualization.",
                elements=[vega_element],
            ).send()
        else:
            assert tool_call["name"] == "build_sql_query"
            query_element = cl.CustomElement(
                name="query",
                props={
                    "sql": json.loads(tool_call["arguments"])["sql_query"],
                },
                display="inline",
            )
            await cl.Message(
                content="",
                elements=[query_element],
            ).send()

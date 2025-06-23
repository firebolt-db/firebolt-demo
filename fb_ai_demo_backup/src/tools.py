import json

import chainlit as cl
import tabulate
from openai import OpenAI


# Called from the JS code in the custom elements to execute a SQL query.
@cl.action_callback("execute_sql_query_action")
async def execute_sql_query_action(action):
    try:
        fb_connection = cl.user_session.get("fb_connection")
        query = action.payload["query"]
        response = await cl.make_async(fb_connection.execute_query_on_user_engine)(
            query
        )
        response["rows"] = [
            {key: value for key, value in zip(response["column_names"], row)}
            for row in response["rows"]
        ]
        response["success"] = True
        return response
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


# Called from the JS code in the custom elements to fix a SQL query with an error.
@cl.action_callback("fix_sql_query_action")
async def fix_sql_query_action(action):
    try:
        # TODO: Extend the system prompt with more information about Firebolt.
        system_prompt = (
            "Your task is to fix errors in a SQL query. Given a SQL query and an error message, "
            "you should modify the query to fix the error. Return the fixed SQL query without any "
            "explanation or markup. If you cannot fix the query, return the original query without "
            "any explanation or markup."
        )
        client = OpenAI()
        query = action.payload["query"]
        fb_connection = cl.user_session.get("fb_connection")
        original_error = await cl.make_async(fb_connection.validate_query)(query)
        error_message = original_error
        for i in range(5):
            user_prompt = f"SQL query:\n{query}\n\nError message:\n{error_message}"
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )
            query = completion.choices[0].message.content
            validation_result = await cl.make_async(fb_connection.validate_query)(query)
            if validation_result == "Success":
                return {"fixed": True, "query": query, "original_error": original_error}
            else:
                error_message = validation_result
        return {
            "fixed": False,
            "error": "Failed to fix the query after 5 attempts.",
            "original_error": original_error,
        }
    except Exception as e:
        return json.dumps(
            {"fixed": False, "error": str(e), "original_error": original_error}
        )


@cl.step(type="tool")
async def build_data_visualization(sql_query: str, vega_spec: str):
    try:
        json.loads(vega_spec)
    except Exception as e:
        return f"Error parsing the Vega-Lite specification: {e}"

    try:
        # Validating the query and returning errors allows the LLM to fix errors itself.
        fb_connection = cl.user_session.get("fb_connection")
        return await cl.make_async(fb_connection.validate_query)(sql_query)
    except Exception as e:
        return f"Error in the SQL query: {e}"


@cl.step(type="tool")
async def build_sql_query(sql_query: str):
    try:
        # Validating the query and returning errors allows the LLM to fix errors itself.
        fb_connection = cl.user_session.get("fb_connection")
        return await cl.make_async(fb_connection.validate_query)(sql_query)
    except Exception as e:
        return f"Error in the SQL query: {e}"


@cl.step(type="tool")
async def get_database_schema():
    # Returns a markdown formatted string with the table and index information.
    table_query = "select table_name, ddl, number_of_rows, compressed_bytes, uncompressed_bytes from information_schema.tables where length(ddl) > 0;"
    index_query = "select table_name as on_table, index_name, index_definition, compressed_bytes, uncompressed_bytes from information_schema.indexes where index_type = 'aggregating';"
    try:
        fb_connection = cl.user_session.get("fb_connection")
        # Show the tables.
        response = await cl.make_async(fb_connection.execute_query_on_user_engine)(
            table_query
        )
        database_schema = "### Tables\n\n"
        for row in response["rows"]:
            dict_row = {key: value for key, value in zip(response["column_names"], row)}
            database_schema += f"#### {dict_row['table_name']}\n\n"
            database_schema += (
                f"* Number of rows: {int(dict_row['number_of_rows']):,}\n"
            )
            database_schema += (
                f"* Compressed size: {int(dict_row['compressed_bytes']):,} bytes\n"
            )
            database_schema += (
                f"* Uncompressed size: {int(dict_row['uncompressed_bytes']):,} bytes\n"
            )
            database_schema += "* SQL:\n"
            database_schema += f"```\n{dict_row['ddl']}\n```\n\n"

        # Show the indexes.
        response = await cl.make_async(fb_connection.execute_query_on_user_engine)(
            index_query
        )
        database_schema += "### Aggregating Indexes\n\n"
        for row in response["rows"]:
            dict_row = {key: value for key, value in zip(response["column_names"], row)}
            database_schema += f"#### {dict_row['index_name']}\n\n"
            database_schema += f"* On table: {dict_row['on_table']}\n"
            database_schema += (
                f"* Compressed size: {int(dict_row['compressed_bytes']):,} bytes\n"
            )
            database_schema += (
                f"* Uncompressed size: {int(dict_row['uncompressed_bytes']):,} bytes\n"
            )
            database_schema += "* SQL:\n"
            create_stmt = f'CREATE AGGREGATING INDEX "{dict_row["index_name"]}" ON "{dict_row["on_table"]}" (\n{dict_row["index_definition"][1:-1]}\n);'
            database_schema += f"```\n{create_stmt}\n```\n\n"
            return database_schema
    except Exception as e:
        print(f"Error in get_database_schema: {e}")
        return f"Error in get_database_schema: {e}. Do not retry."


query_result_template = """### Result for query with ID "{query_id}"

#### Statistics

* Response time (seconds): {response_time_seconds:,.2f}
* Rows read: {rows_read:,}
* Bytes read: {bytes_read:,}
* Scanned bytes cache: {scanned_bytes_cache:,}
* Scanned bytes storage: {scanned_bytes_storage:,}

#### Data

{data}
"""


@cl.step(type="tool")
async def execute_sql_query(final_query):
    ask_permission = cl.user_session.get("ask_permission")
    if ask_permission:
        res = await cl.AskActionMessage(
            content=f"Can I execute the following SQL query?\n\n{final_query}",
            actions=[
                cl.Action(name="yes", payload={"value": "yes"}, label="✅ Yes"),
                cl.Action(name="no", payload={"value": "no"}, label="❌ No"),
            ],
        ).send()
        if not res or res.get("payload").get("value") == "no":
            return "User denied permission to execute the query. Do not retry."

    try:
        fb_connection = cl.user_session.get("fb_connection")
        response = await cl.make_async(fb_connection.execute_query_on_user_engine)(
            final_query
        )
        return query_result_template.format(
            query_id=response["query_id"],
            response_time_seconds=response["statistics"]["response_time_seconds"],
            rows_read=response["statistics"]["rows_read"],
            bytes_read=response["statistics"]["bytes_read"],
            scanned_bytes_cache=response["statistics"]["scanned_bytes_cache"],
            scanned_bytes_storage=response["statistics"]["scanned_bytes_storage"],
            data=tabulate.tabulate(
                response["rows"], response["column_names"], tablefmt="pipe"
            ),
        )
    except Exception as e:
        print(f"Query execution error: {e}")
        return f"Query execution error: {e}"


async def call_function(name, args):
    if name == "get_database_schema":
        return await get_database_schema(**args)
    elif name == "execute_sql_query":
        return await execute_sql_query(**args)
    elif name == "build_data_visualization":
        return await build_data_visualization(**args)
    elif name == "build_sql_query":
        return await build_sql_query(**args)
    else:
        print(f"Unknown function: {name}")
        return f"Unknown function: {name}. Do not retry."


async def call_tools(tool_calls):
    response_messages = []
    for tool_call in tool_calls:
        name = tool_call["name"]
        args = json.loads(tool_call["arguments"])
        result = await call_function(name, args)
        response_messages.append(
            {"role": "tool", "tool_call_id": tool_call["id"], "content": result}
        )
    return response_messages


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_database_schema",
            "description": "Returns a markdown-formatted string with information about the tables and aggregating indexes in the database. It also includes statistics such as compressed and uncompressed size in bytes. For tables, it also includes the number of rows. Unless the user asks for it, you should only tell them about the available tables and their sizes.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
                "required": [],
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_sql_query",
            "description": "Executes a Firebolt SQL query against the database system. Returns a markdown-formatted string with the result table and execution statistics such as response time and the number of read rows. Returns an error message if the query execution fails.",
            "parameters": {
                "type": "object",
                "required": ["final_query"],
                "properties": {
                    "final_query": {
                        "type": "string",
                        "description": "The Firebolt SQL query to be executed. Make sure that the string contains exactly one query.",
                    }
                },
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_data_visualization",
            "description": """
            Generates an interactive visualization based on the Firebolt SQL query and Vega-Lite specification.
            The Firebolt SQL query will be executed against the Firebolt data warehouse and the results will be used to power the visualization.
            Make sure the query result columns have aliases that match the Vega-Lite specification.
            """,
            "parameters": {
                "type": "object",
                "required": ["sql_query", "vega_spec"],
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "The Firebolt SQL query to be executed, powering the visualization. Make sure that the string contains exactly one query.",
                    },
                    "vega_spec": {
                        "type": "string",
                        "description": "The Vega-Lite specification to be used for the visualization.",
                    },
                },
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_sql_query",
            "description": "Shows an interactive SQL editor that allows the user to modify and adjust and refine the initially generated Firebolt SQL query. Once the user is happy with the query, the user can submit the query and look at the results.",
            "parameters": {
                "type": "object",
                "required": ["sql_query"],
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "The initial Firebolt SQL query to be executed. Make sure that the string contains exactly one query.",
                    },
                },
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

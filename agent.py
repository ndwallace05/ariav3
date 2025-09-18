from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ChatContext
from livekit.plugins import (
    noise_cancellation,
    openai
)
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, send_email
from file_system_tools import create_folder, create_file, edit_file, list_files, read_file
from calculator_tool import calculate
from web_tools import open_website
from mem0 import AsyncMemoryClient

# 1.  ---- LEAVE IMPORTS AT TOP (harmless) ----
from mcp_client import MCPServerSse                # keep, just in case
from mcp_client.agent_tools import MCPToolsIntegration





import os
import json
import logging
import traceback
load_dotenv()


class Assistant(Agent):
    def __init__(self, tools, chat_ctx=None) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
            voice="Aoede",
            ),
            tools=tools,
            chat_ctx=chat_ctx
        )


async def entrypoint(ctx: agents.JobContext):

    async def shutdown_hook(chat_ctx: ChatContext | None, mem0: AsyncMemoryClient, memory_str: str):
        if not chat_ctx:
            logging.info("No chat context to save")
            return
            
        logging.info("Shutting down, saving chat context to memory...")
        messages_formatted = [
        ]

        logging.info(f"Chat context messages: {chat_ctx.items}")

        for item in chat_ctx.items:
            try:
                if not hasattr(item, 'role') or not hasattr(item, 'content'):
                    continue
                
                content = getattr(item, 'content', None)
                if not content:
                    continue
                    
                content_str = ''.join(str(c) for c in content) if isinstance(content, list) else str(content)

                if memory_str and memory_str in content_str:
                    continue

                role = getattr(item, 'role', None)
                if role in ['user', 'assistant']:
                    messages_formatted.append({
                        "role": role,
                        "content": content_str.strip()
                    })
            except Exception as e:
                logging.warning(f"Error processing chat item: {e}")

        logging.info(f"Formatted messages to add to memory: {messages_formatted}")
        await mem0.add(messages_formatted, user_id="Nathan")
        logging.info("Chat context saved to memory.")


    session = AgentSession(
        
    )

    

    mem0 = AsyncMemoryClient()
    user_name = 'Nathan'

    results = await mem0.get_all(user_id=user_name)
    initial_ctx = ChatContext()
    memory_str = ''

    if results:
        memories = [
            {
                "memory": result["memory"],
                "updated_at": result["updated_at"]
            }
            for result in results
        ]
        memory_str = json.dumps(memories)
        logging.info(f"Memories: {memory_str}")
        initial_ctx.add_message(
            role="assistant",
            content=f"The user's name is {user_name}, and this is relvant context about him: {memory_str}."
        )

    mcp_server = MCPServerSse(
        params={"url": os.environ.get("N8N_MCP_SERVER_URL")},
        cache_tools_list=True,
        name="SSE MCP Server"
    )

    local_tools = [
        get_weather,
        search_web,
        send_email,
        create_folder,
        create_file,
        edit_file,
        calculate,
        list_files,
        read_file,
        open_website,
    ]

    mcp_tools = await MCPToolsIntegration.prepare_dynamic_tools(
        mcp_servers=[mcp_server]
    )

    all_tools = local_tools + mcp_tools

    agent = Assistant(tools=all_tools, chat_ctx=initial_ctx)

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )

    ctx.add_shutdown_callback(lambda: shutdown_hook(session._agent.chat_ctx if session._agent else None, mem0, memory_str))

if __name__ == "__main__":
    # Allow overriding the agent HTTP port with an environment variable
    # Default to 0 (ephemeral port) to avoid "address already in use" errors
    try:
        port_env = os.environ.get("LIVEKIT_AGENT_PORT")
        port = int(port_env) if port_env else 0
    except Exception:
        port = 0

    try:
        opts = agents.WorkerOptions(entrypoint_fnc=entrypoint, port=port)
        agents.cli.run_app(opts)
    except OSError as e:
        # Common on Windows when port is already bound
        logging.error(f"OS error starting agent: {e}")
        if getattr(e, 'errno', None) in (10048,):
            logging.error(
                "Port is already in use. Either set a different port via the LIVEKIT_AGENT_PORT environment variable or stop the process using the port."
            )
        else:
            logging.error("Unexpected OSError while starting agent:\n" + traceback.format_exc())
        raise
    except AssertionError as e:
        # The library sometimes asserts during shutdown (seen when failing to bind)
        logging.error("AssertionError during worker shutdown: %s", e)
        logging.error(traceback.format_exc())
        raise
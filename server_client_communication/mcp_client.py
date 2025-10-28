

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    
    # mcp_server.py'yi subprocess olarak başlatmak için parametreleri ayarla
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            await session.initialize()
            
            # 1. Client is connected mesajı
            print("Client is connected to MCP Server")
            
            # 2. GetResourceRequest: 
            resource_response = await session.read_resource("resource://info")
            resource_content = resource_response.contents[0].text
            print(resource_content)
            
            # 3. ExecuteToolRequest: 
            tool_response = await session.call_tool(
                "greet",
                arguments={"name": "Basak"}
            )
            tool_result = [
                {
                    "type": content.type,
                    "text": content.text
                }
                for content in tool_response.content
            ]
            tool_result_json = json.dumps(tool_result)
            print(tool_result_json)


if __name__ == "__main__":
    # Asenkron main fonksiyonunu çalıştır
    asyncio.run(main())

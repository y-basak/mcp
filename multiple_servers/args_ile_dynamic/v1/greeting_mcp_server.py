
from mcp.server.fastmcp import FastMCP

# FastMCP server instance oluştur
mcp = FastMCP("greeting-server")


@mcp.resource("resource://greet")
def greet() -> str:
    
    return "Hello! Welcome to the Greeting Server."


@mcp.resource("resource://farewell")
def farewell() -> str:
    
    return "Goodbye! Thank you for using the Greeting Server."


if __name__ == "__main__":
    # stdio transport ile server'ı başlat
    mcp.run(transport="stdio")

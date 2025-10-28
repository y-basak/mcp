from mcp.server.fastmcp import FastMCP

# FastMCP server instance oluştur
mcp = FastMCP("hello-world-server")


@mcp.resource("resource://info")
def get_info() -> str:
    return "This is a static resource from my MCP server."


@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to MCP."


if __name__ == "__main__":
    # stdio transport ile server'ı başlat
    mcp.run(transport="stdio")

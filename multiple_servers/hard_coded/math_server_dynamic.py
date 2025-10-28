from mcp.server.fastmcp import FastMCP

# FastMCP server instance oluştur
mcp = FastMCP("math-server")


@mcp.resource("resource://addition/{a}/{b}")
def addition(a: float, b: float) -> str:
    """
    Dynamic addition resource
    Example: resource://addition/10/20
    """
    result = a + b
    return f"Addition result: {a} + {b} = {result}"


@mcp.resource("resource://multiplication/{a}/{b}")
def multiplication(a: float, b: float) -> str:
    """
    Dynamic multiplication resource
    Example: resource://multiplication/5/8
    """
    result = a * b
    return f"Multiplication result: {a} × {b} = {result}"


if __name__ == "__main__":
    # stdio transport ile server'ı başlat
    mcp.run(transport="stdio")

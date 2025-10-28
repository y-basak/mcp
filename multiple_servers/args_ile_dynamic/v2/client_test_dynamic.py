import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_greeting_server():
    """Greeting sunucusunu ve kaynaklarını test eder."""
    print("\n" + "="*60)
    print("TESTING GREETING SERVER")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["greeting_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("\n✓ Client is connected to Greeting MCP Server")
            
            # Greet kaynağını test et
            greet_response = await session.read_resource("resource://greet")
            print(f"Response from greet: {greet_response.contents[0].text}")
            
            # Farewell kaynağını test et
            farewell_response = await session.read_resource("resource://farewell")
            print(f"Response from farewell: {farewell_response.contents[0].text}")


async def test_math_server():
    """Math sunucusunu ve araçlarını test eder."""
    print("\n" + "="*60)
    print("TESTING MATH SERVER (USING call_tool)")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("\n✓ Client is connected to Math MCP Server")
            
            # 'add' aracını çağır ve temiz sonucu yazdır
            add_input = [10, 20, 30,70,30]
            print(f"\nClient: Calling add({add_input})")
            add_result = await session.call_tool("add", {"numbers": add_input})
            # Sonucu daha temiz göstermek için structuredContent kullanılıyor
            print(f"Client: Result = {add_result.structuredContent['result']}")

            # 'multiply' aracını çağır ve temiz sonucu yazdır
            mul_input = [7, 8]
            print(f"\nClient: Calling multiply({mul_input})")
            mul_result = await session.call_tool("multiply", {"numbers": mul_input})
            print(f"Client: Result = {mul_result.structuredContent['result']}")


async def main():
    """Tüm testleri sırayla çalıştırır."""
    await test_greeting_server()
    await test_math_server()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY ✓")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
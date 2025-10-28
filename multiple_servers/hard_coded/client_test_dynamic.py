
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_greeting_server():
    """Test Greeting Server and its resources"""
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
            
            # 1. Connection test
            print("\n✓ Client is connected to Greeting MCP Server")
            
            # 2. Test greet resource
            print("\n--- Testing greet resource ---")
            greet_response = await session.read_resource("resource://greet")
            greet_content = greet_response.contents[0].text
            print(f"Response: {greet_content}")
            
            # 3. Test farewell resource
            print("\n--- Testing farewell resource ---")
            farewell_response = await session.read_resource("resource://farewell")
            farewell_content = farewell_response.contents[0].text
            print(f"Response: {farewell_content}")
            
            # 4. Test invalid resource
            print("\n--- Testing invalid resource ---")
            try:
                await session.read_resource("resource://invalid")
                print("✗ Should have thrown an error!")
            except Exception as e:
                print(f"✓ Correctly handled invalid resource: {type(e).__name__}")


async def test_math_server():
    print("\n" + "="*60)
    print("TESTING MATH SERVER (DYNAMIC RESOURCES)")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Connection test
            print("\n✓ Client is connected to Math MCP Server")
            
            # 2. Test addition resource with different parameters
            print("\n--- Testing addition resource ---")
            add_response1 = await session.read_resource("resource://addition/15/27")
            print(f"15 + 27 = {add_response1.contents[0].text}")
            
            add_response2 = await session.read_resource("resource://addition/100/50")
            print(f"100 + 50 = {add_response2.contents[0].text}")
            
            add_response3 = await session.read_resource("resource://addition/3.14/2.86")
            print(f"3.14 + 2.86 = {add_response3.contents[0].text}")
            
            # 3. Test multiplication resource with different parameters
            print("\n--- Testing multiplication resource ---")
            mult_response1 = await session.read_resource("resource://multiplication/8/12")
            print(f"8 × 12 = {mult_response1.contents[0].text}")
            
            mult_response2 = await session.read_resource("resource://multiplication/7/9")
            print(f"7 × 9 = {mult_response2.contents[0].text}")
            
            mult_response3 = await session.read_resource("resource://multiplication/2.5/4")
            print(f"2.5 × 4 = {mult_response3.contents[0].text}")
            
            # 4. Test with negative numbers
            print("\n--- Testing negative numbers ---")
            neg_add = await session.read_resource("resource://addition/-10/5")
            print(f"-10 + 5 = {neg_add.contents[0].text}")
            
            neg_mult = await session.read_resource("resource://multiplication/-3/-4")
            print(f"-3 × -4 = {neg_mult.contents[0].text}")
            
            # 5. Test with zero
            print("\n--- Testing zero operations ---")
            zero_add = await session.read_resource("resource://addition/0/0")
            print(f"0 + 0 = {zero_add.contents[0].text}")
            
            zero_mult = await session.read_resource("resource://multiplication/100/0")
            print(f"100 × 0 = {zero_mult.contents[0].text}")
            
            # 6. Test with large numbers
            print("\n--- Testing very large numbers ---")
            large = await session.read_resource("resource://multiplication/999999/888888")
            print(f"999999 × 888888 = {large.contents[0].text}")
            
            # 7. Complex calculation sequence
            print("\n--- Testing complex calculation sequence ---")
            print("Calculating: (10 + 5) × 3 = ?")
            
            step1 = await session.read_resource("resource://addition/10/5")
            print(f"  Step 1: 10 + 5 = {step1.contents[0].text}")
            
            step2 = await session.read_resource("resource://multiplication/15/3")
            print(f"  Step 2: 15 × 3 = {step2.contents[0].text}")
            
            print("✓ Complex calculation completed successfully!")


async def test_math_server_edge_cases():
    print("\n" + "="*60)
    print("TESTING EDGE CASES")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("\n--- Testing decimal precision ---")
            decimal_add = await session.read_resource("resource://addition/1.111/2.222")
            print(f"1.111 + 2.222 = {decimal_add.contents[0].text}")
            
            decimal_mult = await session.read_resource("resource://multiplication/0.5/0.5")
            print(f"0.5 × 0.5 = {decimal_mult.contents[0].text}")
            
            print("\n--- Testing very small numbers ---")
            small = await session.read_resource("resource://multiplication/0.001/0.001")
            print(f"0.001 × 0.001 = {small.contents[0].text}")
            
            print("\n--- Testing mixed operations ---")
            mixed1 = await session.read_resource("resource://addition/-5.5/10.3")
            print(f"-5.5 + 10.3 = {mixed1.contents[0].text}")
            
            mixed2 = await session.read_resource("resource://multiplication/-7.5/2")
            print(f"-7.5 × 2 = {mixed2.contents[0].text}")


async def main():
    print("\n" + "█"*60)
    print("█" + " "*10 + "MCP SERVERS TEST SUITE (DYNAMIC RESOURCES)" + " "*10 + "█")
    print("█"*60)
    
    # Test all servers
    await test_greeting_server()
    await test_math_server()
    await test_math_server_edge_cases()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY ✓")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Asenkron main fonksiyonunu çalıştır
    asyncio.run(main())

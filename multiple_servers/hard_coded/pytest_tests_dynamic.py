import asyncio
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ==================== GREETING SERVER TESTS ====================

@pytest.mark.asyncio
async def test_greeting_server_connection():
    server_params = StdioServerParameters(
        command="python",
        args=["greeting_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            assert session is not None
            print("✓ Greeting Server connection successful")


@pytest.mark.asyncio
async def test_greet_resource():
    """Test 2: Greet resource returns correct message"""
    server_params = StdioServerParameters(
        command="python",
        args=["greeting_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            response = await session.read_resource("resource://greet")
            content = response.contents[0].text
            
            assert "Hello" in content
            assert "Greeting Server" in content
            print(f"✓ Greet resource test passed: {content}")


@pytest.mark.asyncio
async def test_farewell_resource():
    server_params = StdioServerParameters(
        command="python",
        args=["greeting_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            response = await session.read_resource("resource://farewell")
            content = response.contents[0].text
            
            assert "Goodbye" in content
            assert "Greeting Server" in content
            print(f"✓ Farewell resource test passed: {content}")


@pytest.mark.asyncio
async def test_greeting_server_invalid_resource():
    server_params = StdioServerParameters(
        command="python",
        args=["greeting_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            with pytest.raises(Exception):
                await session.read_resource("resource://invalid")
            print("✓ Invalid resource correctly raises exception")


# ==================== MATH SERVER TESTS (DYNAMIC RESOURCES) ====================

@pytest.mark.asyncio
async def test_math_server_connection():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            assert session is not None
            print("✓ Math Server connection successful")


@pytest.mark.asyncio
async def test_addition_resource():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test with 15 + 27 = 42
            response = await session.read_resource("resource://addition/15/27")
            content = response.contents[0].text
            
            assert "Addition result" in content
            assert "42" in content
            print(f"✓ Addition resource test passed: {content}")


@pytest.mark.asyncio
async def test_addition_multiple_values():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test 100 + 50
            response1 = await session.read_resource("resource://addition/100/50")
            content1 = response1.contents[0].text
            assert "150" in content1
            print(f"✓ Addition 100+50: {content1}")
            
            # Test 3.14 + 2.86
            response2 = await session.read_resource("resource://addition/3.14/2.86")
            content2 = response2.contents[0].text
            assert "6.0" in content2 or "6" in content2
            print(f"✓ Addition 3.14+2.86: {content2}")


@pytest.mark.asyncio
async def test_multiplication_resource():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test with 8 * 12 = 96
            response = await session.read_resource("resource://multiplication/8/12")
            content = response.contents[0].text
            
            assert "Multiplication result" in content
            assert "96" in content
            print(f"✓ Multiplication resource test passed: {content}")


@pytest.mark.asyncio
async def test_multiplication_multiple_values():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test 7 * 9
            response1 = await session.read_resource("resource://multiplication/7/9")
            content1 = response1.contents[0].text
            assert "63" in content1
            print(f"✓ Multiplication 7×9: {content1}")
            
            # Test 2.5 * 4
            response2 = await session.read_resource("resource://multiplication/2.5/4")
            content2 = response2.contents[0].text
            assert "10" in content2
            print(f"✓ Multiplication 2.5×4: {content2}")


@pytest.mark.asyncio
async def test_negative_numbers():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test -10 + 5
            response1 = await session.read_resource("resource://addition/-10/5")
            content1 = response1.contents[0].text
            assert "-5" in content1
            print(f"✓ Negative addition: {content1}")
            
            # Test -3 * -4
            response2 = await session.read_resource("resource://multiplication/-3/-4")
            content2 = response2.contents[0].text
            assert "12" in content2
            print(f"✓ Negative multiplication: {content2}")


@pytest.mark.asyncio
async def test_zero_operations():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test 0 + 0
            response1 = await session.read_resource("resource://addition/0/0")
            content1 = response1.contents[0].text
            assert "0" in content1
            print(f"✓ Zero addition: {content1}")
            
            # Test 100 * 0
            response2 = await session.read_resource("resource://multiplication/100/0")
            content2 = response2.contents[0].text
            assert "0" in content2
            print(f"✓ Zero multiplication: {content2}")


@pytest.mark.asyncio
async def test_large_numbers():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test large multiplication
            response = await session.read_resource("resource://multiplication/999999/888888")
            content = response.contents[0].text
            
            assert "Multiplication result" in content
            print(f"✓ Large number multiplication: {content}")


@pytest.mark.asyncio
async def test_decimal_precision():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test decimal addition
            response1 = await session.read_resource("resource://addition/1.111/2.222")
            content1 = response1.contents[0].text
            assert "3.333" in content1
            print(f"✓ Decimal addition: {content1}")
            
            # Test decimal multiplication
            response2 = await session.read_resource("resource://multiplication/0.5/0.5")
            content2 = response2.contents[0].text
            assert "0.25" in content2
            print(f"✓ Decimal multiplication: {content2}")


@pytest.mark.asyncio
async def test_sequential_operations():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Calculate (10 + 5) * 3
            step1 = await session.read_resource("resource://addition/10/5")
            assert "15" in step1.contents[0].text
            
            step2 = await session.read_resource("resource://multiplication/15/3")
            assert "45" in step2.contents[0].text
            
            print("✓ Sequential operations work correctly")


@pytest.mark.asyncio
async def test_all_resources_available():
    server_params = StdioServerParameters(
        command="python",
        args=["math_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test both resources exist
            add_result = await session.read_resource("resource://addition/5/3")
            mult_result = await session.read_resource("resource://multiplication/5/3")
            
            assert "8" in add_result.contents[0].text
            assert "15" in mult_result.contents[0].text
            
            print("✓ Both addition and multiplication resources available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

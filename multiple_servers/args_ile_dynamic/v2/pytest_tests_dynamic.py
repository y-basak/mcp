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


# ==================== MATH SERVER TESTS (TOOL-BASED) ====================

@pytest.mark.asyncio
async def test_math_server_connection():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            assert session is not None
            print("✓ Math Server connection successful")


@pytest.mark.asyncio
async def test_addition_tool():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool("add", {"numbers": [15, 27]})
            assert result == 42
            print(f"✓ Addition tool test passed: 15 + 27 = {result}")


@pytest.mark.asyncio
async def test_addition_multiple_values():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result1 = await session.call_tool("add", {"numbers": [100, 50]})
            assert result1 == 150
            print(f"✓ Addition 100+50 = {result1}")
            
            result2 = await session.call_tool("add", {"numbers": [3.14, 2.86]})
            assert result2 == 6.0
            print(f"✓ Addition 3.14+2.86 = {result2}")


@pytest.mark.asyncio
async def test_multiplication_tool():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool("multiply", {"numbers": [8, 12]})
            assert result == 96
            print(f"✓ Multiplication tool test passed: 8 × 12 = {result}")


@pytest.mark.asyncio
async def test_multiplication_multiple_values():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result1 = await session.call_tool("multiply", {"numbers": [7, 9]})
            assert result1 == 63
            print(f"✓ Multiplication 7×9 = {result1}")
            
            result2 = await session.call_tool("multiply", {"numbers": [2.5, 4]})
            assert result2 == 10.0
            print(f"✓ Multiplication 2.5×4 = {result2}")


@pytest.mark.asyncio
async def test_negative_numbers():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result1 = await session.call_tool("add", {"numbers": [-10, 5]})
            assert result1 == -5
            print(f"✓ Negative addition: -10 + 5 = {result1}")
            
            result2 = await session.call_tool("multiply", {"numbers": [-3, -4]})
            assert result2 == 12
            print(f"✓ Negative multiplication: -3 × -4 = {result2}")


@pytest.mark.asyncio
async def test_zero_operations():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result1 = await session.call_tool("add", {"numbers": [0, 0]})
            assert result1 == 0
            print(f"✓ Zero addition: 0 + 0 = {result1}")
            
            result2 = await session.call_tool("multiply", {"numbers": [100, 0]})
            assert result2 == 0
            print(f"✓ Zero multiplication: 100 × 0 = {result2}")


@pytest.mark.asyncio
async def test_large_numbers():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool("multiply", {"numbers": [999999, 888888]})
            assert result == 888887111112
            print(f"✓ Large number multiplication: 999999 × 888888 = {result}")


@pytest.mark.asyncio
async def test_decimal_precision():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result1 = await session.call_tool("add", {"numbers": [1.111, 2.222]})
            assert result1 == 3.333
            print(f"✓ Decimal addition: 1.111 + 2.222 = {result1}")
            
            result2 = await session.call_tool("multiply", {"numbers": [0.5, 0.5]})
            assert result2 == 0.25
            print(f"✓ Decimal multiplication: 0.5 × 0.5 = {result2}")


@pytest.mark.asyncio
async def test_sequential_operations():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Calculate (10 + 5) * 3
            step1_result = await session.call_tool("add", {"numbers": [10, 5]})
            assert step1_result == 15
            
            step2_result = await session.call_tool("multiply", {"numbers": [step1_result, 3]})
            assert step2_result == 45
            
            print("✓ Sequential operations work correctly: (10 + 5) * 3 = 45")


@pytest.mark.asyncio
async def test_all_tools_available():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],  # CORRECTED FILENAME
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test both tools exist
            add_result = await session.call_tool("add", {"numbers": [5, 3]})
            mult_result = await session.call_tool("multiply", {"numbers": [5, 3]})
            
            assert add_result == 8
            assert mult_result == 15
            
            print("✓ Both addition and multiplication tools are available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
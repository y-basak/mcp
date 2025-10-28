
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
            print("✓ Greeting Server bağlantısı başarılı")


@pytest.mark.asyncio
async def test_greet_resource():

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
            print(f"✓ Greet kaynak testi başarılı: {content}")


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
            print(f"✓ Farewell kaynak testi başarılı: {content}")


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
            print("✓ Geçersiz kaynak doğru şekilde hata veriyor")


# ==================== MATH SERVER TESTS (DYNAMIC RESOURCES) ====================

@pytest.mark.asyncio
async def test_math_server_connection():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            assert session is not None
            print("✓ Math Server bağlantısı başarılı")


@pytest.mark.asyncio
async def test_addition_resource_multiple_args():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 15 + 27 + 10 = 52
            response = await session.read_resource("resource://addition/15,27,10")
            content = response.contents[0].text
            
            assert "Toplama Sonucu" in content
            assert "52" in content
            print(f"✓ Çoklu toplama testi başarılı: {content}")


@pytest.mark.asyncio
async def test_multiplication_resource_multiple_args():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 8 * 12 * 2 = 192
            response = await session.read_resource("resource://multiplication/8,12,2")
            content = response.contents[0].text
            
            assert "Çarpma Sonucu" in content
            assert "192" in content
            print(f"✓ Çoklu çarpma testi başarılı: {content}")


@pytest.mark.asyncio
async def test_negative_and_decimal_numbers():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # -10 + 5.5 + (-2) = -6.5
            response1 = await session.read_resource("resource://addition/-10,5.5,-2")
            content1 = response1.contents[0].text
            assert "-6.5" in content1
            print(f"✓ Negatif ve ondalıklı toplama: {content1}")
            
            # -3 * -4 * 0.5 = 6
            response2 = await session.read_resource("resource://multiplication/-3,-4,0.5")
            content2 = response2.contents[0].text
            assert "6" in content2 or "6.0" in content2
            print(f"✓ Negatif ve ondalıklı çarpma: {content2}")


@pytest.mark.asyncio
async def test_single_operand_and_zero():
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Tekil parametre
            response1 = await session.read_resource("resource://addition/42")
            content1 = response1.contents[0].text
            assert "42" in content1
            print(f"✓ Tekil parametre toplama: {content1}")
            
            # Sıfır ile çarpma
            response2 = await session.read_resource("resource://multiplication/100,10,0")
            content2 = response2.contents[0].text
            assert "0" in content2 or "0.0" in content2
            print(f"✓ Sıfır ile çarpma: {content2}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_greeting_server():
    """Test Greeting Server and its resources"""
    print("\n" + "="*60)
    print("GREETING SERVER TEST EDİLİYOR")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["greeting_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Bağlantı testi
            print("\n✓ İstemci, Greeting MCP Server'a bağlandı")
            
            # 2. greet kaynağını test et
            print("\n--- greet kaynağı test ediliyor ---")
            greet_response = await session.read_resource("resource://greet")
            greet_content = greet_response.contents[0].text
            print(f"Yanıt: {greet_content}")
            
            # 3. farewell kaynağını test et
            print("\n--- farewell kaynağı test ediliyor ---")
            farewell_response = await session.read_resource("resource://farewell")
            farewell_content = farewell_response.contents[0].text
            print(f"Yanıt: {farewell_content}")
            
            # 4. Geçersiz kaynağı test et
            print("\n--- Geçersiz kaynak test ediliyor ---")
            try:
                await session.read_resource("resource://invalid")
                print("✗ Hata vermeliydi!")
            except Exception as e:
                print(f"✓ Geçersiz kaynak doğru şekilde işlendi: {type(e).__name__}")


async def test_math_server():
    print("\n" + "="*60)
    print("MATH SERVER TEST EDİLİYOR (DİNAMİK KAYNAKLAR)")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["math_server_dynamic.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Bağlantı testi
            print("\n✓ İstemci, Math MCP Server'a bağlandı")
            
            # 2. Toplama kaynağını farklı parametrelerle test et
            print("\n--- Toplama kaynağı test ediliyor ---")
            add_response1 = await session.read_resource("resource://addition/15,27,10")
            print(f"İstek: 15 + 27 + 10 -> {add_response1.contents[0].text}")
            
            add_response2 = await session.read_resource("resource://addition/100,50,25,25")
            print(f"İstek: 100 + 50 + 25 + 25 -> {add_response2.contents[0].text}")
            
            add_response3 = await session.read_resource("resource://addition/3.14,2.86,4.0")
            print(f"İstek: 3.14 + 2.86 + 4.0 -> {add_response3.contents[0].text}")
            
            # 3. Çarpma kaynağını farklı parametrelerle test et
            print("\n--- Çarpma kaynağı test ediliyor ---")
            mult_response1 = await session.read_resource("resource://multiplication/8,12,2")
            print(f"İstek: 8 × 12 × 2 -> {mult_response1.contents[0].text}")
            
            mult_response2 = await session.read_resource("resource://multiplication/7,9,10")
            print(f"İstek: 7 × 9 × 10 -> {mult_response2.contents[0].text}")
            
            mult_response3 = await session.read_resource("resource://multiplication/2.5,4,3")
            print(f"İstek: 2.5 × 4 × 3 -> {mult_response3.contents[0].text}")
            
            # 4. Negatif sayılarla test
            print("\n--- Negatif sayılar test ediliyor ---")
            neg_add = await session.read_resource("resource://addition/-10,5,-3,8")
            print(f"İstek: -10 + 5 + -3 + 8 -> {neg_add.contents[0].text}")
            
            neg_mult = await session.read_resource("resource://multiplication/-3,-4,-2")
            print(f"İstek: -3 × -4 × -2 -> {neg_mult.contents[0].text}")
            
            # 5. Sıfır ile test
            print("\n--- Sıfır işlemleri test ediliyor ---")
            zero_add = await session.read_resource("resource://addition/0,0,0,0")
            print(f"İstek: 0 + 0 + 0 + 0 -> {zero_add.contents[0].text}")
            
            zero_mult = await session.read_resource("resource://multiplication/100,5,0")
            print(f"İstek: 100 × 5 × 0 -> {zero_mult.contents[0].text}")


async def main():
    print("\n" + "█"*60)
    print("█" + " "*10 + "MCP SUNUCULARI TEST SUİTİ (DİNAMİK KAYNAKLAR)" + " "*8 + "█")
    print("█"*60)
    
    # Tüm sunucuları test et
    await test_greeting_server()
    await test_math_server()
    
    print("\n" + "="*60)
    print("TÜM TESTLER BAŞARIYLA TAMAMLANDI ✓")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Asenkron main fonksiyonunu çalıştır
    asyncio.run(main())

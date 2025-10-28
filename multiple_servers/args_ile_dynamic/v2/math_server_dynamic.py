import math
from typing import List
from mcp.server.fastmcp import FastMCP

# FastMCP sunucu örneği oluştur
mcp = FastMCP("math-server")


@mcp.tool()  # DÜZELTME: Parantezler eklendi
def add(numbers: List[float]) -> float:
    """
    Verilen sayı listesini toplar.
    'numbers' argümanı float türünde bir listedir.
    """
    print(f"Sunucu: Toplama isteği alındı: {numbers}")
    return sum(numbers)


@mcp.tool()  # DÜZELTME: Parantezler eklendi
def multiply(numbers: List[float]) -> float:
    """
    Verilen sayı listesini çarpar.
    'numbers' argümanı float türünde bir listedir.
    """
    print(f"Sunucu: Çarpma isteği alındı: {numbers}")
    # Çarpma işlemi için math.prod kullanılır
    return math.prod(numbers)


if __name__ == "__main__":
    # Sunucuyu stdio transport ile başlat
    mcp.run(transport="stdio")
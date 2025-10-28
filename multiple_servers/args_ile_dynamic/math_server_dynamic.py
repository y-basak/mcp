
from mcp.server.fastmcp import FastMCP
import operator
from functools import reduce

# FastMCP sunucu örneği oluştur
mcp = FastMCP("math-server")


@mcp.resource("resource://addition/{numbers_str}")
def addition(numbers_str: str) -> str:
  
    try:
        # Gelen string'i ',' karakterine göre böl ve float listesine çevir
        args = [float(n) for n in numbers_str.split(',')]
        if not args:
            return "Hata: Toplama için sayı belirtilmedi."
        
        result = sum(args)
        # İşlem ifadesini oluştur
        expression = " + ".join(map(str, args))
        return f"Toplama Sonucu: {expression} = {result}"
    except (ValueError, TypeError):
        return "Hata: Tüm parametreler geçerli sayılar olmalıdır."


@mcp.resource("resource://multiplication/{numbers_str}")
def multiplication(numbers_str: str) -> str:
 
    try:
        # Gelen string'i ',' karakterine göre böl ve float listesine çevir
        args = [float(n) for n in numbers_str.split(',')]
        if not args:
            return "Hata: Çarpma için sayı belirtilmedi."
            
        # Çarpma işlemi için reduce kullan
        result = reduce(operator.mul, args)
        # İşlem ifadesini oluştur
        expression = " × ".join(map(str, args))
        return f"Çarpma Sonucu: {expression} = {result}"
    except (ValueError, TypeError):
        return "Hata: Tüm parametreler geçerli sayılar olmalıdır."


if __name__ == "__main__":
    # stdio transportu ile sunucuyu başlat
    mcp.run(transport="stdio")

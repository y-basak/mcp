# MCP Client-Server Uygulaması

Bu proje, Model Context Protocol (MCP) kullanarak basit bir client-server iletişim örneğidir. Server, bir kaynak (resource) ve bir araç (tool) sağlar; client ise bu kaynaklara erişir ve araçları çalıştırır.

## Gereksinimler

```bash
pip install mcp
```

## Dosya Yapısı

```
.
├── mcp_server.py    # MCP sunucusu
├── mcp_client.py    # MCP istemcisi
└── README.md        # Bu dosya
```

## Dosyalar

### mcp_server.py

FastMCP kullanarak oluşturulmuş basit bir MCP sunucusu. İki temel özellik sağlar:

- **Resource**: `resource://info` - Statik bir bilgi kaynağı
- **Tool**: `greet` - İsim parametresi alarak karşılama mesajı döndüren bir araç

### mcp_client.py

MCP sunucusuna bağlanan ve şu işlemleri gerçekleştiren bir istemci:

1. Sunucuya bağlanır
2. `resource://info` kaynağını okur
3. `greet` aracını "Basak" parametresiyle çalıştırır
4. Sonuçları konsola yazdırır

## Kullanım

### Sunucuyu Başlatma

Sunucu, client tarafından otomatik olarak subprocess olarak başlatılır. Manuel başlatmak isterseniz:

```bash
python mcp_server.py
```

### Client'ı Çalıştırma

```bash
python mcp_client.py
```

## Beklenen Çıktı

```
Client is connected to MCP Server
This is a static resource from my MCP server.
[{"type": "text", "text": "Hello, Basak! Welcome to MCP."}]
```

## Çalışma Mantığı

1. **Bağlantı**: Client, stdio transport kullanarak sunucuyu başlatır ve bağlanır
2. **İnisiyalizasyon**: Session başlatılır
3. **Resource Okuma**: `read_resource()` ile kaynak okunur
4. **Tool Çalıştırma**: `call_tool()` ile araç çağrılır
5. **Sonuçlar**: Tüm sonuçlar konsola yazdırılır

## Özelleştirme

### Yeni Tool Ekleme

`mcp_server.py` dosyasına:

```python
@mcp.tool()
def yeni_fonksiyon(parametre: str) -> str:
    return f"Sonuç: {parametre}"
```

### Yeni Resource Ekleme

`mcp_server.py` dosyasına:

```python
@mcp.resource("resource://yeni-kaynak")
def yeni_kaynak() -> str:
    return "Yeni kaynak içeriği"
```

### Client'ta Kullanma

`mcp_client.py` dosyasında:

```python
# Resource okuma
response = await session.read_resource("resource://yeni-kaynak")

# Tool çalıştırma
response = await session.call_tool("yeni_fonksiyon", arguments={"parametre": "değer"})
```

## Notlar

- Sunucu stdio transport kullanır, dolayısıyla standart input/output üzerinden iletişim kurar
- Client, sunucuyu otomatik olarak subprocess olarak başlatır
- Tüm işlemler asenkron (async/await) yapıdadır

## Hata Ayıklama

Eğer bağlantı sorunları yaşıyorsanız:

1. `mcp` paketinin doğru kurulduğundan emin olun
2. Python sürümünün 3.8+ olduğunu kontrol edin
3. Her iki dosyanın da aynı dizinde olduğunu doğrulayın

## Lisans

Bu proje örnek amaçlı oluşturulmuştur.
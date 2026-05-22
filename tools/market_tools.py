import yfinance as yf
import pandas as pd
import ta
from tavily import TavilyClient
from crewai.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool("Ambil data harga saham IDX")
def ambil_data_saham(kode_saham: str) -> str:
    """Ambil data harga saham IDX real-time dari Yahoo Finance"""
    ticker = kode_saham.upper() + ".JK"
    saham = yf.Ticker(ticker)
    info = saham.info
    hist = saham.history(period="3mo")
    
    close = hist["Close"]
    high = hist["High"]
    low = hist["Low"]
    volume = hist["Volume"]
    
    # Technical indicators
    rsi = ta.momentum.RSIIndicator(close).rsi().iloc[-1]
    macd = ta.trend.MACD(close)
    macd_line = macd.macd().iloc[-1]
    signal_line = macd.macd_signal().iloc[-1]
    ma20 = close.tail(20).mean()
    ma50 = close.tail(50).mean()
    support = low.tail(20).min()
    resistance = high.tail(20).max()
    avg_volume = volume.tail(20).mean()
    
    return f"""
    SAHAM: {kode_saham.upper()}
    Nama: {info.get('longName', 'N/A')}
    Harga: Rp {info.get('currentPrice', 'N/A')}
    High: Rp {info.get('dayHigh', 'N/A')}
    Low: Rp {info.get('dayLow', 'N/A')}
    Volume: {info.get('volume', 'N/A'):,}
    Avg Volume: {int(avg_volume):,}
    RSI: {round(rsi, 2)}
    MACD: {round(macd_line, 2)} | Signal: {round(signal_line, 2)}
    MA20: {round(ma20, 2)} | MA50: {round(ma50, 2)}
    Support: Rp {round(support, 2)}
    Resistance: Rp {round(resistance, 2)}
    """

@tool("Ambil data fundamental saham")
def ambil_fundamental(kode_saham: str) -> str:
    """Ambil data fundamental dan laporan keuangan saham IDX"""
    ticker = kode_saham.upper() + ".JK"
    saham = yf.Ticker(ticker)
    info = saham.info
    
    pe = info.get('trailingPE', 'N/A')
    pb = info.get('priceToBook', 'N/A')
    roe = info.get('returnOnEquity', 'N/A')
    profit_margin = info.get('profitMargins', 'N/A')
    revenue = info.get('totalRevenue', 'N/A')
    
    if roe != 'N/A' and roe is not None:
        roe = f"{round(roe * 100, 2)}%"
    if profit_margin != 'N/A' and profit_margin is not None:
        profit_margin = f"{round(profit_margin * 100, 2)}%"
    if revenue != 'N/A' and revenue is not None:
        revenue = f"Rp {round(revenue / 1e9, 2)} Miliar"
    
    return f"""
    FUNDAMENTAL {kode_saham.upper()}:
    PE Ratio: {pe}
    PB Ratio: {pb}
    ROE: {roe}
    Profit Margin: {profit_margin}
    Revenue: {revenue}
    Sektor: {info.get('sector', 'N/A')}
    Industri: {info.get('industry', 'N/A')}
    """

@tool("Search berita dan sentimen saham")
def search_berita(query: str) -> str:
    """Search berita terbaru dan analisis sentimen saham IDX"""
    hasil = tavily.search(query=query, max_results=5)
    berita = ""
    for r in hasil["results"]:
        berita += f"- {r['title']}: {r['content'][:200]}\n"
    return berita

@tool("Cek kondisi IHSG dan market")
def cek_market(query: str) -> str:
    """Cek kondisi IHSG, market global, dan sektor"""
    ihsg = yf.Ticker("^JKSE")
    info = ihsg.history(period="5d")
    
    harga_ihsg = info["Close"].iloc[-1]
    perubahan = ((info["Close"].iloc[-1] - info["Close"].iloc[-2]) / info["Close"].iloc[-2]) * 100
    
    # Search kondisi market
    berita_market = tavily.search(
        query="IHSG kondisi pasar saham Indonesia hari ini 2026",
        max_results=3
    )
    
    konteks = ""
    for r in berita_market["results"]:
        konteks += f"- {r['title']}: {r['content'][:150]}\n"
    
    return f"""
    IHSG: {round(harga_ihsg, 2)}
    Perubahan: {round(perubahan, 2)}%
    
    Berita Market:
    {konteks}
    """
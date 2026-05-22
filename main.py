import litellm
litellm.cache = None

import os
import sys
import requests
from dotenv import load_dotenv
from crewai import Crew, Process
from agents.trading_agents import buat_semua_agent
from tasks import buat_semua_task

load_dotenv()

def kirim_telegram(pesan: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Telegram max 4096 karakter per pesan
    # Kalau lebih, split jadi beberapa pesan
    max_length = 4000
    
    if len(pesan) <= max_length:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": pesan}
        requests.post(url, json=payload)
    else:
        chunks = [pesan[i:i+max_length] for i in range(0, len(pesan), max_length)]
        for chunk in chunks:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": chunk}
            requests.post(url, json=payload)

def analisis_saham(kode_saham: str):
    print(f"\n{'='*60}")
    print(f"🤖 IDX SWING TRADING BOT — CrewAI")
    print(f"📊 Menganalisis: {kode_saham.upper()}")
    print(f"{'='*60}\n")
    
    # Kirim notifikasi mulai ke Telegram
    kirim_telegram(f"🔍 IDX Trading Bot mulai menganalisis saham {kode_saham.upper()}...\nMohon tunggu beberapa menit.")
    
    # Buat semua agent dan tasks
    agents = buat_semua_agent()
    tasks = buat_semua_task(agents, kode_saham)
    
    # Buat crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Jalankan crew
    print("🚀 Crew mulai bekerja...\n")
    hasil = crew.kickoff()
    
    # Ambil hasil akhir dari task terakhir
    laporan_final = str(hasil)
    
    # Kirim ke Telegram
    print("\n📱 Mengirim hasil ke Telegram...")
    kirim_telegram(laporan_final)
    print("✅ Hasil terkirim ke Telegram!\n")
    
    return laporan_final

def menu():
    while True:
        print(f"\n{'='*60}")
        print(f"🤖 IDX SWING TRADING BOT — CrewAI 20 Agent")
        print(f"{'='*60}")
        print("1. Analisis saham")
        print("2. Keluar")
        print(f"{'='*60}")
        
        pilihan = input("Pilih menu (1/2): ").strip()
        
        if pilihan == "1":
            kode = input("Masukkan kode saham (contoh: BBCA, TLKM, GOTO): ").strip().upper()
            analisis_saham(kode)
        elif pilihan == "2":
            print("Sampai jumpa! 👋")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    menu()
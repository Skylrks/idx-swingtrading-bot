from crewai import Task

def buat_semua_task(agents: dict, kode_saham: str):
    
    # ── LAYER 1: DATA COLLECTION ────────────────────────────
    
    task_market_data = Task(
        description=f"""Ambil dan analisis data harga saham {kode_saham} secara lengkap.
        Gunakan tool ambil_data_saham untuk mendapatkan:
        - Harga terkini, high, low, volume
        - RSI, MACD, MA20, MA50
        - Support dan resistance
        Berikan ringkasan data yang jelas dan terstruktur.""",
        expected_output=f"Laporan data teknikal lengkap saham {kode_saham} dengan semua indikator",
        agent=agents["market_data"]
    )
    
    task_fundamental = Task(
        description=f"""Analisis fundamental saham {kode_saham} secara mendalam.
        Gunakan tool ambil_fundamental untuk mendapatkan:
        - PE ratio, PB ratio, ROE
        - Revenue, net income, profit margin
        - Valuasi: apakah murah, wajar, atau mahal?
        Berikan penilaian apakah saham ini layak secara fundamental.""",
        expected_output=f"Laporan fundamental lengkap saham {kode_saham} dengan penilaian valuasi",
        agent=agents["fundamental"]
    )
    
    task_news = Task(
        description=f"""Cari dan analisis berita terbaru tentang saham {kode_saham}.
        Search berita dengan query: "saham {kode_saham} berita terbaru 2026"
        Analisis:
        - Sentimen berita: POSITIF/NEGATIF/NETRAL
        - Berita paling signifikan
        - Dampak potensial ke harga
        - Skor sentimen 1-10""",
        expected_output=f"Laporan sentimen berita saham {kode_saham} dengan skor dan dampak",
        agent=agents["news"]
    )
    
    task_social = Task(
        description=f"""Monitor sentimen investor retail tentang saham {kode_saham}.
        Search dengan query: "saham {kode_saham} investor stockbit forum 2026"
        Analisis:
        - Apakah ada FOMO atau panic selling?
        - Sentimen mayoritas investor retail
        - Tingkat hype: TINGGI/SEDANG/RENDAH
        - Apakah ada rumor atau isu yang beredar?""",
        expected_output=f"Laporan sentimen sosial media saham {kode_saham}",
        agent=agents["social"]
    )
    
    task_foreign_flow = Task(
        description=f"""Pantau pergerakan dana asing di saham {kode_saham} dan IHSG.
        Search dengan query: "foreign flow dana asing IHSG {kode_saham} 2026"
        Analisis:
        - Apakah asing sedang beli atau jual?
        - Kondisi IHSG saat ini
        - Dampak kondisi global ke pasar Indonesia""",
        expected_output=f"Laporan foreign flow dan kondisi market untuk saham {kode_saham}",
        agent=agents["foreign_flow"]
    )
    
    # ── LAYER 2: TECHNICAL ANALYSIS ─────────────────────────
    
    task_trend = Task(
        description=f"""Analisis trend dan momentum saham {kode_saham}.
        Berdasarkan data dari Market Data Specialist:
        - Identifikasi trend utama: UPTREND/DOWNTREND/SIDEWAYS
        - Golden Cross atau Death Cross?
        - Kekuatan trend berdasarkan ADX
        - Apakah momentum sedang naik atau turun?""",
        expected_output=f"Laporan trend dan momentum saham {kode_saham}",
        agent=agents["trend"],
        context=[task_market_data]
    )
    
    task_momentum = Task(
        description=f"""Analisis kondisi overbought/oversold saham {kode_saham}.
        Berdasarkan data RSI dan indikator momentum:
        - RSI: overbought (>70) atau oversold (<30)?
        - Ada divergensi bullish atau bearish?
        - Sinyal reversal atau continuation?
        - Kapan timing entry terbaik?""",
        expected_output=f"Laporan analisis momentum dan timing entry saham {kode_saham}",
        agent=agents["momentum"],
        context=[task_market_data]
    )
    
    task_volume = Task(
        description=f"""Analisis volume dan bandarmologi saham {kode_saham}.
        Berdasarkan data volume:
        - Apakah big money sedang akumulasi atau distribusi?
        - Volume ratio vs rata-rata
        - OBV trend: naik atau turun?
        - Ada anomali volume signifikan?""",
        expected_output=f"Laporan bandarmologi dan analisis volume saham {kode_saham}",
        agent=agents["volume"],
        context=[task_market_data]
    )
    
    task_support_resistance = Task(
        description=f"""Petakan level support dan resistance kritis saham {kode_saham}.
        Berdasarkan data harga historis:
        - Level support kuat (1 minggu, 1 bulan, 3 bulan)
        - Level resistance kuat (1 minggu, 1 bulan, 3 bulan)
        - Level MA20 dan MA50 sebagai dynamic support/resistance
        - Berapa jarak harga ke support dan resistance terdekat?""",
        expected_output=f"Peta support dan resistance lengkap saham {kode_saham}",
        agent=agents["support_resistance"],
        context=[task_market_data]
    )
    
    task_pattern = Task(
        description=f"""Identifikasi pola chart saham {kode_saham}.
        Berdasarkan data harga historis:
        - Apakah ada pola chart yang terbentuk?
        - Contoh: Double Bottom, Head & Shoulders, Triangle, Flag
        - Apakah pola sudah terkonfirmasi?
        - Proyeksi target harga berdasarkan pola""",
        expected_output=f"Laporan pola chart saham {kode_saham} dengan proyeksi target",
        agent=agents["pattern"],
        context=[task_market_data]
    )
    
    # ── LAYER 3: INTELLIGENCE ────────────────────────────────
    
    task_bull = Task(
        description=f"""Buat kasus BULLISH terkuat untuk saham {kode_saham}.
        Berdasarkan semua data yang tersedia:
        - Sebutkan minimal 5 alasan kuat mengapa harga akan NAIK
        - Dukung setiap argumen dengan data konkret
        - Berikan target harga optimis
        - Kapan sinyal beli terkonfirmasi?""",
        expected_output=f"Bull case lengkap dengan 5+ argumen data-driven untuk saham {kode_saham}",
        agent=agents["bull"],
        context=[task_market_data, task_fundamental, task_news, task_trend, task_volume]
    )
    
    task_bear = Task(
        description=f"""Buat kasus BEARISH terkuat untuk saham {kode_saham}.
        Berdasarkan semua data yang tersedia:
        - Sebutkan minimal 5 risiko dan alasan mengapa harga akan TURUN
        - Dukung setiap argumen dengan data konkret
        - Berikan level support kritis yang jika breakdown sangat berbahaya
        - Kapan sinyal jual terkonfirmasi?""",
        expected_output=f"Bear case lengkap dengan 5+ risiko data-driven untuk saham {kode_saham}",
        agent=agents["bear"],
        context=[task_market_data, task_fundamental, task_news, task_trend, task_volume]
    )
    
    task_macro = Task(
        description=f"""Analisis kondisi makro dan dampaknya ke saham {kode_saham}.
        - Kondisi IHSG saat ini
        - Kebijakan BI rate terbaru
        - Nilai tukar rupiah
        - Kondisi ekonomi global
        - Dampak semua faktor makro ke saham {kode_saham}""",
        expected_output=f"Laporan analisis makro dan dampaknya ke saham {kode_saham}",
        agent=agents["macro"],
        context=[task_foreign_flow]
    )
    
    task_sector = Task(
        description=f"""Analisis posisi sektor saham {kode_saham} dalam rotasi sektor.
        - Sektor apa yang sedang outperform di IDX?
        - Apakah sektor {kode_saham} sedang dalam fase akumulasi atau distribusi?
        - Bagaimana performa sektor vs IHSG?
        - Apakah ada katalis sektoral yang akan mempengaruhi {kode_saham}?""",
        expected_output=f"Laporan rotasi sektor dan posisi saham {kode_saham}",
        agent=agents["sector"],
        context=[task_macro, task_fundamental]
    )
    
    # ── LAYER 4: DECISION ────────────────────────────────────
    
    task_debate = Task(
        description=f"""Moderasi debat antara Bull Case dan Bear Case untuk saham {kode_saham}.
        Evaluasi argumen bull vs bear:
        - Argumen bull mana yang paling kuat dan didukung data?
        - Argumen bear mana yang paling valid?
        - Faktor mana yang paling dominan saat ini?
        - Buat keputusan objektif: siapa yang menang debat?
        - Berikan verdict: kondisi saham saat ini lebih bullish atau bearish?""",
        expected_output=f"Hasil debat bull vs bear dengan verdict objektif untuk saham {kode_saham}",
        agent=agents["debate_moderator"],
        context=[task_bull, task_bear, task_macro, task_sector]
    )
    
    task_signal = Task(
        description=f"""Synthesize semua analisis menjadi sinyal trading final untuk saham {kode_saham}.
        Berdasarkan semua laporan dari agent lain:
        - Sinyal: BUY / SELL / HOLD
        - Entry price yang ideal
        - Stop loss level
        - Target price (TP1 dan TP2)
        - Alasan singkat dan jelas
        - Horizon trading: jangka pendek/menengah""",
        expected_output=f"Sinyal trading final BUY/SELL/HOLD dengan entry, SL, TP untuk saham {kode_saham}",
        agent=agents["signal_synthesizer"],
        context=[task_debate, task_support_resistance, task_pattern, task_momentum]
    )
    
    task_confidence = Task(
        description=f"""Hitung confidence score sinyal trading saham {kode_saham}.
        Evaluasi berapa banyak indikator yang konfirmasi sinyal:
        - Hitung jumlah indikator bullish vs bearish
        - Berikan skor 0-100%
        - 90-100%: Sinyal sangat kuat
        - 70-89%: Sinyal kuat  
        - 50-69%: Sinyal sedang
        - <50%: Sinyal lemah, lebih baik HOLD
        - Rekomendasikan apakah sinyal layak dieksekusi""",
        expected_output=f"Confidence score 0-100% dengan breakdown perhitungan untuk sinyal {kode_saham}",
        agent=agents["confidence_scorer"],
        context=[task_signal, task_debate]
    )
    
    # ── LAYER 5: RISK & EXECUTION ────────────────────────────
    
    task_risk = Task(
        description=f"""Evaluasi risiko trading saham {kode_saham}.
        Berdasarkan sinyal dan confidence score:
        - Hitung risk/reward ratio
        - Apakah R/R minimal 1:2?
        - Level risiko: TINGGI/SEDANG/RENDAH
        - Maximum drawdown yang bisa terjadi
        - Apakah trade ini layak dieksekusi dari sisi risiko?""",
        expected_output=f"Laporan risiko lengkap dengan R/R ratio untuk trade {kode_saham}",
        agent=agents["risk"],
        context=[task_signal, task_confidence, task_support_resistance]
    )
    
    task_position = Task(
        description=f"""Hitung position sizing optimal untuk trade saham {kode_saham}.
        Asumsi modal: Rp 10.000.000
        - Berapa persen modal yang disarankan?
        - Berapa lot yang harus dibeli?
        - Apakah boleh averaging? Di harga berapa?
        - Maximum loss yang ditoleransi: 2% dari modal
        - Gunakan fixed fractional method""",
        expected_output=f"Rencana position sizing detail dengan jumlah lot dan modal untuk {kode_saham}",
        agent=agents["position_sizer"],
        context=[task_risk, task_signal]
    )
    
    task_execution = Task(
        description=f"""Buat laporan eksekusi final dan kirim sinyal trading saham {kode_saham}.
        Buat laporan komprehensif dalam format yang siap dikirim ke Telegram:
        
        Format laporan:
        🤖 IDX SWING TRADING BOT
        📊 SINYAL TRADING: [SAHAM]
        
        📌 SINYAL: BUY/SELL/HOLD
        💯 CONFIDENCE: XX%
        
        💰 RENCANA TRADING:
        • Entry: Rp XXXXX
        • Stop Loss: Rp XXXXX  
        • Target 1: Rp XXXXX
        • Target 2: Rp XXXXX
        • Lot: XX lot
        • R/R Ratio: X:X
        
        📊 ANALISIS SINGKAT:
        [3-4 kalimat ringkasan]
        
        ⚠️ DISCLAIMER: Bukan saran investasi resmi""",
        expected_output=f"Laporan trading lengkap siap kirim Telegram untuk saham {kode_saham}",
        agent=agents["execution"],
        context=[task_signal, task_confidence, task_risk, task_position]
    )
    
    return [
        # Layer 1
        task_market_data, task_fundamental, task_news, 
        task_social, task_foreign_flow,
        # Layer 2
        task_trend, task_momentum, task_volume,
        task_support_resistance, task_pattern,
        # Layer 3
        task_bull, task_bear, task_macro, task_sector,
        # Layer 4
        task_debate, task_signal, task_confidence,
        # Layer 5
        task_risk, task_position, task_execution
    ]
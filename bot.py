import requests
import datetime
import pytz
import os
# --- KONFIGURASI ---


# Ambil dari GitHub Secrets
TELE_USERNAME = os.getenv('TELE_USERNAME') # Ganti dengan username Telegram kamu
CITY = "George Town"            # Kota terdekat untuk Pulau Pinang
COUNTRY = "Malaysia"
METHOD = 11                     # Method 11 adalah "Majlis Ugama Islam Singapura" (Paling mendekati JAKIM)
TIMEZONE = "Asia/Kuala_Lumpur"
# -------------------

def check_and_call():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.datetime.now(tz)
    current_time = now.strftime("%H:%M")
    
    print(f"Waktu sekarang di Pulau Pinang: {current_time}")

    try:
        # Menggunakan Aladhan API (Global & Akurat untuk Malaysia)
        url = f"https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method={METHOD}"
        res = requests.get(url).json()
        timings = res['data']['timings']
        
        # Mapping waktu sholat (Menghapus format 24 jam yang tidak perlu jika ada)
        target_sholat = {
            "Subuh": timings['Fajr'],
            "Zuhur": timings['Dhuhr'],
            "Asar": timings['Asr'],
            "Maghrib": timings['Maghrib'],
            "Isyak": timings['Isha']
        }

        for nama, waktu in target_sholat.items():
            # API Aladhan kadang mengembalikan format "HH:MM (Timezone)", kita bersihkan
            waktu_clean = waktu.split(" ")[0]
            
            if current_time == waktu_clean:
                print(f"Waktunya {nama}! Menghubungi via Telegram...")
                call_url = f"https://api.callmebot.com/start.php?user=@{TELE_USERNAME}&text=Dah+masuk+waktu+sholat+{nama}+kat+Pulau+Pinang&lang=id-id"
                requests.get(call_url)
                return

        print("Belum masuk waktu sholat.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_and_call()
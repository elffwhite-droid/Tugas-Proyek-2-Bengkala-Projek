from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

PROGRAM_KNOWLEDGE = """
Informasi Sehati Waste Bot:
Nama bot: Sehati Waste Bot
Versi: 1.0.0
Menu utama: Jenis Sampah, Harga, Jadwal, Jam, Edukasi, Katalog, Lapor Sampah
Jenis sampah yang diterima: Plastik (bersih & kering), Botol, Sachet, Kertas
Harga: Plastik Rp 2.000 / kg, Botol Rp 3.000 / kg
Jadwal: Senin, Rabu, Jumat
Jam operasional: 08.00 - 16.00 WIB
Edukasi: Pisahkan sampah organik dan non-organik.
"""

SYSTEM_PROMPT = f"""
Anda adalah asisten Sehati Waste Bot.
Gunakan hanya informasi yang tersedia dalam program ini.
Jangan menebak, jangan menambahkan informasi dari luar, dan jangan menjawab di luar topik.
Jika pertanyaan tidak dapat dijawab berdasarkan informasi di atas, balas dengan:
"Maaf, saya hanya bisa menjawab berdasarkan informasi yang tersedia pada program."

{PROGRAM_KNOWLEDGE}
"""
def chat_ai(user_message):
    if not user_message or not user_message.strip():
        return "Maaf, saya tidak menerima pertanyaan."

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        response = completion.choices[0].message.content.strip()
        if not response:
            return "Maaf, saya hanya bisa menjawab berdasarkan informasi yang tersedia pada program."
        return response
    except Exception as e:
        return f"Error: {str(e)}"
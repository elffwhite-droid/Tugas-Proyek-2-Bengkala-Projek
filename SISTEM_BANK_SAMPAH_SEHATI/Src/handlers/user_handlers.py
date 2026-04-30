from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import simpan_user, simpan_laporan, get_produk
from utils.keyboards import main_menu, lapor_keyboard
from config import ADMIN_ID
from ai_handler import chat_ai

LAPOR = 1

# ================= DATA STATIS (FORMAT HTML) =================
JENIS_SAMPAH = """
<b>♻️ JENIS SAMPAH YANG DITERIMA:</b>
• Plastik (bersih & kering)
• Botol
• Sachet
• Kertas
"""

HARGA_SAMPAH = """
<b>💰 HARGA SAAT INI:</b>
• Plastik : Rp 2.000 / kg
• Botol   : Rp 3.000 / kg
"""

JADWAL = """
<b>📅 JADWAL PENGAMBILAN SAMPAH</b>

Tim Sehati akan menjemput setoranmu pada:
• <b>Senin:</b> Area Cluster Utara & Barat
• <b>Rabu:</b> Area Cluster Selatan & Timur
• <b>Jumat:</b> Area Pusat & Perkantoran

Pastikan sampah sudah dipilah dan diletakkan di depan rumah sebelum jam 08.00 pagi ya!
"""

JAM = """
<b>🕒 JAM OPERASIONAL KANTOR</b>

Kami siap melayani Anda pada:
• <b>Senin - Jumat:</b> 08.00 - 16.00 WIB
• <b>Sabtu:</b> 08.00 - 12.00 WIB (Hanya Drop-off mandiri)
• <b>Minggu/Tanggal Merah:</b> Libur

Ingin cek saldo tabungan atau konsultasi sampah? Hubungi kami di jam tersebut, ya!
"""

EDUKASI = """
<b>📚 ZONA EDUKASI SEHATI: Sampah Jadi Berkah!</b>
Halo, Pahlawan Lingkungan! 🌱 
Selamat datang di fitur Edukasi Bank Sampah Sehati. Mari ubah kebiasaan lama menjadi manfaat nyata untuk bumi. 

<b>3 Langkah Dasar Mengelola Sampah dari Rumah:</b>

1️⃣ <b>PILAH (Kunci Utama)</b>
Pisahkan sampah menjadi 3 wadah sederhana:
• <b>Organik:</b> Sisa makanan, kulit buah, daun (Bisa dijadikan kompos).
• <b>Anorganik:</b> Plastik, kertas, logam, kaca (Inilah yang bisa jadi SALDO!).
• <b>Residu:</b> Masker bekas, tissue, popok (Dibuang ke TPA).

2️⃣ <b>BERSIHKAN</b>
Sebelum disetor, pastikan botol plastik atau kaleng sudah dikosongkan dan dibilas sedikit agar tidak berbau.

3️⃣ <b>KEMAS</b>
Lipat kardus agar rapi dan kumpulkan botol dalam satu kantong besar.

Ingat, setiap gram sampah yang kamu pilah adalah satu langkah menjauhkan bumi dari kerusakan. Semangat mengelola! 💚
"""

# ================= HANDLERS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    simpan_user(user.id, user.full_name, user.username)
    await update.message.reply_text(
        f"Halo <b>{user.first_name}</b>! Selamat datang di <b>Sehati Waste Bot</b>.", 
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>🆘 BANTUAN SEHATI WASTE BOT</b>\n\n"
        "Gunakan tombol menu di bawah untuk berinteraksi:\n"
        "• <b>🛍️ Katalog:</b> Lihat produk daur ulang\n"
        "• <b>📸 Lapor Sampah:</b> Setor sampahmu ke kami\n"
        "• <b>💰 Harga/📅 Jadwal:</b> Informasi operasional\n\n"
        "Atau ketik pertanyaan apa saja untuk dijawab oleh AI!",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

async def katalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    daftar_produk = get_produk()
    if not daftar_produk:
        await update.message.reply_text("📂 Katalog saat ini masih kosong.")
        return

    await update.message.reply_text("🛍️ <b>Daftar Produk Katalog:</b>", parse_mode="HTML")
    for p in daftar_produk:
        caption = f"📦 <b>{p[1]}</b>\n━━━━━━━━━━━━━━\n💰 Harga: Rp {p[2]:,}\n🔢 Stok: {p[3]}\n📝 {p[4]}"
        try:
            if len(p) > 5 and p[5]:
                await context.bot.send_photo(update.effective_chat.id, p[5], caption=caption, parse_mode="HTML")
            else:
                await update.message.reply_text(caption, parse_mode="HTML")
        except:
            await update.message.reply_text(caption, parse_mode="HTML")

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "♻️ Jenis Sampah": await update.message.reply_text(JENIS_SAMPAH, parse_mode="HTML")
    elif text == "💰 Harga": await update.message.reply_text(HARGA_SAMPAH, parse_mode="HTML")
    elif text == "📅 Jadwal": await update.message.reply_text(JADWAL, parse_mode="HTML")
    elif text == "🕒 Jam": await update.message.reply_text(JAM, parse_mode="HTML")
    elif text == "📚 Edukasi": await update.message.reply_text(EDUKASI, parse_mode="HTML")
    elif text == "🛍️ Katalog": await katalog(update, context)
    elif text == "📸 Lapor Sampah": return await lapor_start(update, context)
    elif text == "🆘 Bantuan": await bantuan(update, context)
    else:
        ai_res = chat_ai(text)
        await update.message.reply_text(ai_res)

async def lapor_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Mode laporan aktif. Silakan kirim teks, foto, atau lokasi.\nTekan <b>Selesai Laporan</b> jika sudah.",
        reply_markup=lapor_keyboard(),
        parse_mode="HTML"
    )
    return LAPOR

# --- HANYA SATU FUNGSI LAPOR_HANDLE ---
async def lapor_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text_biasa = update.message.text
    caption_foto = update.message.caption
    
    # 1. Cek Tombol Selesai
    if text_biasa and ("selesai" in text_biasa.lower()):
        await update.message.reply_text("✅ Laporan ditutup.", reply_markup=main_menu())
        return ConversationHandler.END

    # 2. Tentukan pesan laporan
    pesan_untuk_admin = text_biasa if text_biasa else (caption_foto if caption_foto else "Laporan tanpa teks")
    
    photo_id = update.message.photo[-1].file_id if update.message.photo else None
    loc = update.message.location

    # 3. Simpan ke Database
    simpan_laporan(user.id, user.full_name, pesan_untuk_admin, photo_id, 
                   loc.latitude if loc else None, loc.longitude if loc else None)

    # 4. Kirim ke Admin
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID, 
            text=f"📢 <b>LAPORAN DARI:</b> {user.full_name}\n💬 <b>Isi:</b> {pesan_untuk_admin}\n🆔 <b>User ID:</b> {user.id}\n", 
            parse_mode="HTML"
        )
        
        if photo_id:
            await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_id, caption="📸 Lampiran Foto")
            
        if loc:
            await context.bot.send_location(chat_id=ADMIN_ID, latitude=loc.latitude, longitude=loc.longitude)

    except Exception as e:
        print(f"DEBUG ERROR ADMIN: {e}")

    await update.message.reply_text("✅ Laporan diterima. Ada lagi? (Klik Selesai jika sudah)")
    return LAPOR

async def lapor_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Laporan dibatalkan.", reply_markup=main_menu())
    return ConversationHandler.END

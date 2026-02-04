import qrcode
import os
from PIL import Image, ImageDraw, ImageFont

# --- 1. ΟΙ ΡΥΘΜΙΣΕΙΣ ΣΟΥ ---
BASE_URL = "https://emmanuildrakonakis-cmd.github.io/menu-wishlist/" 

# Τα τραπέζια σου
tables = list(range(6, 14)) + [31, 37] + list(range(41, 48))

# --- ✍️ ΤΟ ΜΗΝΥΜΑ ΣΟΥ ---
CUSTOM_QUOTE = "Καλή Όρεξη!"      

def create_styled_qr(table_num):
    # 1. Δημιουργία QR
    final_url = f"{BASE_URL}?table={table_num}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,
        border=2,
    )
    qr.add_data(final_url)
    qr.make(fit=True)
    
    # --- Η ΔΙΟΡΘΩΣΗ ΕΙΝΑΙ ΕΔΩ (.convert("RGB")) ---
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # 2. Ετοιμασία Καμβά (Εικόνας)
    width, height = qr_img.size
    new_height = height + 130 
    final_img = Image.new("RGB", (width, new_height), "white")
    
    # Τώρα κολλάει σωστά γιατί και τα δύο είναι RGB
    final_img.paste(qr_img, (0, 0)) 

    draw = ImageDraw.Draw(final_img)

    # 3. Φόρτωση Γραμματοσειρών
    try:
        font_main = ImageFont.truetype("arial.ttf", 30)
        font_bold = ImageFont.truetype("arialbd.ttf", 28)
    except IOError:
        font_main = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    # --- ΤΟΠΟΘΕΤΗΣΗ ΚΕΙΜΕΝΩΝ ---

    # A. Κείμενο: CUSTOM QUOTE
    text_quote = CUSTOM_QUOTE
    bbox = draw.textbbox((0, 0), text_quote, font=font_main)
    w_quote = bbox[2] - bbox[0]
    draw.text(((width - w_quote) / 2, height + 12), text_quote, fill="black", font=font_main)

    # B. Κείμενο: ΤΡΑΠΕΖΙ Νο Χ
    text_table = f"SCAN FOR WISH LIST - TABLE {table_num}"
    bbox2 = draw.textbbox((0, 0), text_table, font=font_bold)
    w_table = bbox2[2] - bbox2[0]
    draw.text(((width - w_table) / 2, height + 50), text_table, fill="#1B4D3E", font=font_bold)
    
    return final_img

# --- 4. ΕΚΤΕΛΕΣΗ ---
folder_name = "Final_QR_Cards"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

print(f"🚀 Δημιουργία καρτών για τα τραπέζια: {tables}")
print(f"📝 Μήνυμα: {CUSTOM_QUOTE}")

for t in tables:
    img = create_styled_qr(t)
    filename = f"{folder_name}/Table_{t}.png"
    img.save(filename)
    print(f"✅ Έτοιμο: {filename}")

print("\n🎉 ΤΕΛΟΣ! Οι κάρτες είναι έτοιμες για εκτύπωση.")
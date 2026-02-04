import qrcode
import os

BASE_URL = "https://emmanuildrakonakis-cmd.github.io/menu-wishlist/" 

#Παράδειγμα τραπεζιών
tables = list(range(6, 14)) + [31, 37] + list(range(41, 48))

print(f"Θα δημιουργηθούν QR για τα τραπέζια: {tables}")

#ΔΗΜΙΟΥΡΓΙΑ ΦΑΚΕΛΟΥ
folder_name = "Final_QR_Codes"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

print(f"\n Ξεκινάω τη διαδικασία...")

for t in tables:
    
    # π.χ. https://.../menu-wishlist/?table=31
    final_url = f"{BASE_URL}?table={t}"
    
    # Ρυθμίσεις QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=20, 
        border=4,
    )
    qr.add_data(final_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Αποθήκευση
    filename = f"{folder_name}/Table_{t}.png"
    img.save(filename)
    print(f" Έτοιμο: Τραπέζι {t}")

print(f"\nΤελος Θα βρεις τις εικόνες στον φάκελο '{folder_name}'.")
import pandas as pd
import matplotlib.pyplot as plt

# 1. Διαβάζουμε το αρχείο Excel
# Χρησιμοποιούμε το όνομα του αρχείου που κατέβασες
df = pd.read_excel("orders.xlsx")

# Καθαρίζουμε τα δεδομένα (γιατί τα φαγητά είναι σε μια στήλη με κόμματα)
# Αυτό είναι λίγο "pandas magic" για να χωρίσουμε τα φαγητά
all_items = df['Order'].str.split(', ').explode()

# 2. Υπολογισμός: Ποιο πιάτο πουλήθηκε πιο πολύ;
top_dishes = all_items.value_counts()

print("--- ΤΑ 5 ΠΙΟ ΔΗΜΟΦΙΛΗ ΠΙΑΤΑ ---")
print(top_dishes.head(5))

# 3. Δημιουργία Γραφήματος (Πίτα)
plt.figure(figsize=(10, 6)) # Μέγεθος εικόνας
top_dishes.head(7).plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])

plt.title('Δημοτικότητα Πιάτων (Top 7)')
plt.ylabel('') # Κρύβουμε την ετικέτα y

# Εμφάνιση
plt.show()
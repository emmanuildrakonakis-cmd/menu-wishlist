import pandas as pd
import matplotlib.pyplot as plt
import re # Βιβλιοθήκη για να διαβάζουμε κείμενο (Regex)

# --- 1. ΡΥΘΜΙΣΕΙΣ ---
# Εδώ ορίζουμε ποια θεωρούνται ΠΟΤΑ. Όλα τα άλλα θα πάνε στα ΦΑΓΗΤΑ.
DRINKS_LIST = [
    "Coca Cola", "Μπύρα", "Κρασί (500ml)", "Νερό (1L)", "Ρετσίνα"
]

def parse_order(order_str):
    """
    Βοηθητική συνάρτηση που μετατρέπει το string:
    "Χωριάτικη (x1), Μπύρα (x2)"
    σε λίστα: [("Χωριάτικη", 1), ("Μπύρα", 2)]
    """
    if pd.isna(order_str): return []
    
    items_found = []
    # Χωρίζουμε με το κόμμα
    parts = order_str.split(", ")
    
    for part in parts:
        # Ψάχνουμε τη μορφή "Όνομα (xΝούμερο)"
        match = re.search(r"(.+) \(x(\d+)\)", part)
        if match:
            name = match.group(1)
            qty = int(match.group(2))
            items_found.append((name, qty))
        else:
            # Αν για κάποιο λόγο δεν έχει (x...), το μετράμε ως 1
            items_found.append((part, 1))
            
    return items_found

# --- 2. ΑΝΑΛΥΣΗ ΔΕΔΟΜΕΝΩΝ ---
try:
    df = pd.read_excel("orders.xlsx") # Σιγουρέψου ότι το αρχείο λέγεται έτσι
except FileNotFoundError:
    print("❌ Δεν βρέθηκε το αρχείο orders.xlsx! Κατέβασέ το από το Google Sheets.")
    exit()

food_stats = {}
drink_stats = {}

# Διαβάζουμε κάθε παραγγελία γραμμή-γραμμή
for order_row in df['Order']:
    parsed_items = parse_order(order_row)
    
    for name, qty in parsed_items:
        # Έλεγχος: Είναι ποτό ή φαγητό;
        if name in DRINKS_LIST:
            # Είναι ποτό
            if name in drink_stats:
                drink_stats[name] += qty
            else:
                drink_stats[name] = qty
        else:
            # Είναι φαγητό
            if name in food_stats:
                food_stats[name] += qty
            else:
                food_stats[name] = qty

# Μετατροπή σε Pandas Series για ευκολία
food_series = pd.Series(food_stats).sort_values(ascending=False)
drink_series = pd.Series(drink_stats).sort_values(ascending=False)

print("\n--- 🍔 TOP ΦΑΓΗΤΑ ---")
print(food_series.head(5))
print("\n--- 🍺 TOP ΠΟΤΑ ---")
print(drink_series.head(5))

# --- 3. ΓΡΑΦΗΜΑΤΑ (2 Πίτες) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Πίτα Φαγητών
if not food_series.empty:
    food_series.head(7).plot(kind='pie', ax=ax1, autopct='%1.1f%%', startangle=140, cmap="Pastel1")
    ax1.set_title('Top Φαγητά')
    ax1.set_ylabel('')
else:
    ax1.text(0.5, 0.5, "Δεν υπάρχουν δεδομένα", ha='center')

# Πίτα Ποτών
if not drink_series.empty:
    drink_series.head(7).plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=140, cmap="Pastel2")
    ax2.set_title('Top Ποτά')
    ax2.set_ylabel('')
else:
    ax2.text(0.5, 0.5, "Δεν υπάρχουν δεδομένα", ha='center')

plt.suptitle('Στατιστικά Ταβέρνα "Χιώτης"', fontsize=16)
plt.show()
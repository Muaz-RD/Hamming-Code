
import tkinter as tk
from tkinter import messagebox

codeword = []  # Global olarak tanımlanmış codeword değişkeni
original_data = []  # Global olarak tanımlanmış orijinal veri değişkeni
error_position = None  # Hata pozisyonunu saklamak için

def calculate_parity_bits(codeword, r):
    n = len(codeword)
    for i in range(r):
        parity_index = 2 ** i - 1
        parity_value = 0
        for j in range(parity_index, n, 2 ** (i + 1)):
            for k in range(j, min(j + 2 ** i, n)):
                parity_value ^= codeword[k]
        codeword[parity_index] = parity_value
    return codeword

def encode(data_bits):
    global codeword  # Global değişkeni kullan
    n = len(data_bits)
    r = 0

    while (2 ** r < (n + r + 1)):
        r += 1

    codeword = [0] * (n + r)
    j = 0
    for i in range(n + r):
        if i == (2 ** j - 1):
            codeword[i] = 0  # Parite bitlerini sıfırla
            j += 1
        else:
            codeword[i] = data_bits.pop(0)

    codeword = calculate_parity_bits(codeword, r)

    return codeword

def decode(codeword, error_position=None):
    n = len(codeword)
    r = 0

    while (2 ** r < n + 1):
        r += 1

    if error_position is not None:
        codeword[error_position - 1] ^= 1

    error_detected = False
    error_position = 0

    for i in range(r):
        parity_index = 2 ** i - 1
        parity_value = 0
        for j in range(parity_index, n, 2 ** (i + 1)):
            for k in range(j, min(j + 2 ** i, n)):
                parity_value ^= codeword[k]
        if parity_value != 0:
            error_detected = True
            error_position += 2 ** i

    if error_detected:
        return "Hata Tespit Edildi", error_position
    else:
        data_bits = []
        j = 0
        for i in range(n):
            if i != (2 ** j - 1):
                data_bits.append(codeword[i])
            else:
                j += 1
        return data_bits, 0

def get_user_input():
    user_input = entry.get()
    if len(user_input) in [4, 8, 16] and all(bit in '01' for bit in user_input):
        return [int(bit) for bit in user_input]
    else:
        messagebox.showerror("Hata", "Geçersiz giriş. Lütfen 4, 8 veya 16 bitlik bir ikili sayı girin (0 veya 1).")
        return None

def encode_data():
    global codeword, original_data, error_position  # Global değişkenleri kullan
    error_position = None  # Hata pozisyonunu sıfırla
    data_bits = get_user_input()
    if data_bits:
        original_data = data_bits.copy()  # Orijinal veriyi sakla
        codeword = encode(data_bits)
        result_label.config(text="Kodlanmış kod kelimesi: " + ", ".join(str(bit) for bit in codeword))
        encoded_data_entry.delete(0, tk.END)
        encoded_data_entry.insert(0, ", ".join(str(bit) for bit in codeword))

def decode_data():
    global original_data, codeword  # Global değişkenleri kullan
    if original_data:
        decoded_data, detected_error_position = decode(codeword)
        if detected_error_position != 0:
            result_label.config(text=f"Hata Tespit Edildi: {detected_error_position}. Orijinal veri: " + ", ".join(str(bit) for bit in original_data))
        else:
            result_label.config(text="Orijinal veri: " + ", ".join(str(bit) for bit in original_data))
    else:
        result_label.config(text="Önce veri girmelisiniz ve Encode işlemi yapmalısınız.")

def flip_bit():
    global codeword, error_position  # Global değişkenleri kullan
    error_pos = error_entry.get()
    if error_pos.isdigit():
        error_pos = int(error_pos)
        if error_pos <= len(codeword):
            error_position = error_pos  # Hata pozisyonunu sakla
            codeword[error_pos - 1] ^= 1
            result_label.config(text="Bit değiştirildi. Yeni kodlanmış veri: " + ", ".join(str(bit) for bit in codeword))
        else:
            messagebox.showerror("Hata", "Geçersiz hata pozisyonu. Lütfen verinin uzunluğundan daha küçük bir pozisyon girin.")
    else:
        messagebox.showerror("Hata", "Geçersiz hata pozisyonu. Lütfen bir sayı girin.")

# Tkinter arayüzü oluşturma
root = tk.Tk()
root.title("Hamming Kodu Uygulaması")

# Pencere boyutlarını ayarla
root.geometry("600x400")

# Arka plan rengini ayarla
root.configure(bg="#f0f0f0")

# Başlık etiketi
title_label = tk.Label(root, text="Hamming Kodu Uygulaması", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Kullanıcı girişi etiketi
input_label = tk.Label(root, text="Bir ikili sayı girin (4, 8 veya 16 bit):", font=("Helvetica", 12), bg="#f0f0f0")
input_label.pack(pady=5)

# Kullanıcı girişi
entry = tk.Entry(root, font=("Helvetica", 12), width=30)
entry.pack(pady=5)

# Encode butonu
encode_button = tk.Button(root, text="Encode", command=encode_data, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
encode_button.pack(pady=5)

# Kodlanmış veri girişi (sadece görüntüleme amaçlı)
encoded_data_entry = tk.Entry(root, font=("Helvetica", 12), width=50)

encoded_data_entry.pack(pady=5)

# Hata pozisyonu etiketi
error_label = tk.Label(root, text="Hata pozisyonunu girin:", font=("Helvetica", 12), bg="#f0f0f0")
error_label.pack(pady=5)

# Hata pozisyonu girişi
error_entry = tk.Entry(root, font=("Helvetica", 12), width=10)
error_entry.pack(pady=5)

# Bit değiştir butonu
flip_button = tk.Button(root, text="Biti Değiştir", command=flip_bit, font=("Helvetica", 12), bg="#f44336", fg="white", padx=10, pady=5)
flip_button.pack(pady=5)

# Decode butonu
decode_button = tk.Button(root, text="Decode", command=decode_data, font=("Helvetica", 12), bg="#2196F3", fg="white", padx=10, pady=5)
decode_button.pack(pady=5)

# Sonuç etiketi
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
result_label.pack(pady=20)

root.mainloop()


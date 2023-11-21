import tkinter as tk
from tkinter import filedialog
import os
import random
from bitarray import bitarray

class TripleDESApp:
    def __init__(self, master):
        self.master = master
        master.title("Triple DES Encryption")

        self.label = tk.Label(master, text="Triple DES Encryption")
        self.label.pack()

        self.generate_key_button = tk.Button(master, text="Generate Key", command=self.generate_key)
        self.generate_key_button.pack()

        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(master, text="Decrypt", command=self.decrypt)
        self.decrypt_button.pack()

    def generate_key(self):
        key = bitarray(endian='big')
        key.frombytes(os.urandom(24))
        with open("key.txt", "wb") as key_file:
            key_file.write(key.tobytes())

    def apply_subkey(self, block, subkey):
        return block ^ subkey

    def feistel_network(self, block, subkey):
        # Placeholder for Feistel network
        # You need to implement the actual Feistel network logic
        return block

    def triple_des_encrypt_block(self, block, key):
        subkeys = self.generate_subkeys(key)

        # One round of Feistel network
        block_left, block_right = block[:32], block[32:]
        new_block_right = block_left ^ self.feistel_network(block_right, subkeys[0])
        new_block_left = block_right

        return new_block_left + new_block_right

    def triple_des_decrypt_block(self, block, key):
        subkeys = self.generate_subkeys(key)

        # Преобразуем байты в bitarray
        block_bits = bitarray()
        block_bits.frombytes(block)

        # Расширяем блок, если его длина меньше 64 бит
        if len(block_bits) < 64:
            block_bits += bitarray('0' * (64 - len(block_bits)))

        block_left, block_right = block_bits[:32], block_bits[32:]

        # One round of Feistel network
        new_block_right = block_left ^ self.feistel_network(block_right, subkeys[0])
        new_block_left = block_right

        # Объединяем блоки и убираем лишние биты
        decrypted_block = new_block_left + new_block_right
        decrypted_block = decrypted_block[:64]

        return decrypted_block


    def generate_subkeys(self, key):
        # Placeholder for subkey generation
        # You need to implement the actual subkey generation logic
        return [bitarray('0000000000000000'), bitarray('1111111111111111')]

    def encrypt(self):
        key = self.read_key()
        
        file_path = filedialog.askopenfilename(title="Select plaintext file")
        if file_path:
            plaintext = self.read_file(file_path)
            ciphertext = self.triple_des_encrypt(plaintext, key)
            
            save_path = filedialog.asksaveasfilename(title="Save encrypted file", defaultextension=".bin",
                                                      filetypes=[("Binary Files", "*.bin")])
            if save_path:
                self.write_binary_file(save_path, ciphertext)

    def decrypt(self):
        key = self.read_key()
        
        file_path = filedialog.askopenfilename(title="Select encrypted file")
        if file_path:
            ciphertext = self.read_file(file_path)
            decrypted_text = self.triple_des_decrypt(ciphertext, key)
            
            save_path = filedialog.asksaveasfilename(title="Save decrypted file", defaultextension=".txt",
                                                      filetypes=[("Text Files", "*.txt")])
            if save_path:
                self.write_text_file(save_path, decrypted_text)

    def triple_des_encrypt(self, plaintext, key):
        plaintext_bits = bitarray()
        plaintext_bits.frombytes(plaintext)

        ciphertext = bitarray()

        # Padding
        if len(plaintext_bits) % 64 != 0:
            plaintext_bits += bitarray('0' * (64 - len(plaintext_bits) % 64))

        for i in range(0, len(plaintext_bits), 64):
            block = plaintext_bits[i:i+64]
            encrypted_block = self.triple_des_encrypt_block(block, key)
            ciphertext += encrypted_block

        return ciphertext

    def triple_des_decrypt(self, ciphertext, key):
        decrypted_text = bitarray()

        for i in range(0, len(ciphertext), 64):
            block = ciphertext[i:i+64]
            decrypted_block = self.triple_des_decrypt_block(block, key)
            decrypted_text += decrypted_block

        return decrypted_text.tobytes().decode('utf-8')

    def read_file(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    def write_binary_file(self, file_path, data):
        with open(file_path, 'wb') as file:
            file.write(data.tobytes())

    def write_text_file(self, file_path, text):
        with open(file_path, 'w') as file:
            file.write(text)

    def read_key(self):
        with open("key.txt", 'rb') as key_file:
            key = bitarray()
            key.frombytes(key_file.read())
            return key


if __name__ == "__main__":
    root = tk.Tk()
    app = TripleDESApp(root)
    root.mainloop()

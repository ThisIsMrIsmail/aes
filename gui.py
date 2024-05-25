import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import pyperclip
import os

class AES_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Encryption/Decryption")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')  
        
        self.style.configure('TFrame', background='#000000')
        self.style.configure('TButton', font=('Helvetica', 12), padding=10, background='#444444', foreground='white')
        self.style.map('TButton', background=[('active', '#666666')])
        self.style.configure('TLabel', font=('Helvetica', 12), background='#000000', foreground='white')
        self.style.configure('TEntry', font=('Helvetica', 12), padding=5, fieldbackground='#333333', foreground='white')
        self.style.configure('Black.TButton', font=('Helvetica', 12), padding=10, background='#444444', foreground='white')
        self.style.map('Black.TButton', background=[('active', '#666666')])

        
        self.home_window()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def home_window(self):
        self.clear_frame()
        
        self.frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        self.title_label = ttk.Label(self.frame, text="AES Encryption/Decryption", font=("Helvetica", 16))
        self.title_label.pack(pady=20)
        
        self.encrypt_button = ttk.Button(self.frame, text="Encrypt", command=self.encryption_window, width=20)
        self.encrypt_button.pack(pady=10)
        
        self.decrypt_button = ttk.Button(self.frame, text="Decrypt", command=self.decryption_window, width=20)
        self.decrypt_button.pack(pady=10)
    
    def encryption_window(self):
        self.clear_frame()
        
        self.frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        self.file_label = ttk.Label(self.frame, text="Select file to encrypt:")
        self.file_label.grid(row=0, column=0, pady=10, sticky=tk.W)
        
        self.file_entry = ttk.Entry(self.frame, width=40)
        self.file_entry.grid(row=0, column=1, pady=10, padx=10)
        
        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10)
        
        self.encrypt_button = ttk.Button(self.frame, text="Encrypt", command=self.encrypt_file, width=20)
        self.encrypt_button.grid(row=1, column=1, pady=10)
        
        self.back_button = ttk.Button(self.frame, text="Back", command=self.home_window, width=20)
        self.back_button.grid(row=2, column=1, pady=10)
    
    def decryption_window(self):
        self.clear_frame()
        
        self.frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        self.file_label = ttk.Label(self.frame, text="Select file to decrypt:")
        self.file_label.grid(row=0, column=0, pady=10, sticky=tk.W)
        
        self.file_entry = ttk.Entry(self.frame, width=40)
        self.file_entry.grid(row=0, column=1, pady=10, padx=10)
        
        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10)
        
        self.key_label = ttk.Label(self.frame, text="Enter decryption key:")
        self.key_label.grid(row=1, column=0, pady=10, sticky=tk.W)
        
        self.key_entry = ttk.Entry(self.frame, width=40)
        self.key_entry.grid(row=1, column=1, pady=10, padx=10)
        
        self.decrypt_button = ttk.Button(self.frame, text="Decrypt", command=self.decrypt_file, width=20)
        self.decrypt_button.grid(row=2, column=1, pady=10)
        
        self.back_button = ttk.Button(self.frame, text="Back", command=self.home_window, width=20)
        self.back_button.grid(row=3, column=1, pady=10)
    
    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.file_entry.delete(0, tk.END)
        if filename:
            self.file_entry.insert(0, filename)
    
    def encrypt_file(self):
        filename = self.file_entry.get()
        key = get_random_bytes(16)  
        aes = AES.new(key, AES.MODE_EAX)
        
        try:
            with open(filename, "rb") as file:
                plaintext = file.read()
            
            ciphertext, tag = aes.encrypt_and_digest(plaintext)
            encrypted_filename = filename
            with open(encrypted_filename, "wb") as file:
                [file.write(x) for x in (aes.nonce, tag, ciphertext)]
            
            self.show_encryption_success(key)
        except Exception as e:
            messagebox.showerror("Encryption Error", f"An error occurred during encryption:\n{str(e)}")
    
    def show_encryption_success(self, key):
        success_window = tk.Toplevel(self.root)
        success_window.title("Encryption Successful")
        success_window.geometry("400x250")
        success_window.configure(bg='#000000')  
    
        message = f"File encrypted successfully!\nEncryption Key: {key.hex()}"
        success_label = ttk.Label(success_window, text=message, wraplength=350, background='#000000', foreground='white')  
    
        copy_button = ttk.Button(success_window, text="Copy", command=lambda: self.copy_key_to_clipboard(key), style='Black.TButton')  
        copy_button.pack(pady=10)
    
        close_button = ttk.Button(success_window, text="Close", command=success_window.destroy, style='Black.TButton')  
        close_button.pack(pady=10)

        pyperclip.copy(key.hex())
    
    def copy_key_to_clipboard(self, key):
        pyperclip.copy(key.hex())
        messagebox.showinfo("Copied", "Encryption key copied to clipboard!")
    
    def decrypt_file(self):
        filename = self.file_entry.get()
        key = bytes.fromhex(self.key_entry.get())
        
        try:
            with open(filename, "rb") as file:
                nonce, tag, ciphertext = [file.read(x) for x in (16, 16, -1)]
            aes = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = aes.decrypt_and_verify(ciphertext, tag)
            
            decrypted_filename = filename
            with open(decrypted_filename, "wb") as file:
                file.write(plaintext)
            
            messagebox.showinfo("Decryption Successful", "File decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Decryption Error", f"An error occurred during decryption:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AES_GUI(root)
    root.mainloop()
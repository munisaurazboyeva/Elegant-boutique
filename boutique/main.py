import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import database

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Boutique - Kiyimlar Zaxirasi")
        self.geometry("1100x700")
        self.configure(bg="#f0f2f5")
        
        # UI Styles
        self.setup_styles()
        
        # Main layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar (Input)
        self.sidebar = tk.Frame(self, bg="white", width=300, padx=20, pady=20, relief="flat")
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)
        
        # Content (Table)
        self.content = tk.Frame(self, bg="#f0f2f5", padx=20, pady=20)
        self.content.grid(row=0, column=1, sticky="nswe")
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        
        self.setup_sidebar()
        self.setup_table()
        self.load_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="#333", rowheight=35, fieldbackground="white", font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", "#3498db")], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background="#ecf0f1", foreground="#2c3e50", font=("Segoe UI", 11, "bold"), relief="flat")

    def setup_sidebar(self):
        tk.Label(self.sidebar, text="Yangi kiyim qo'shish", bg="white", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20), anchor="w")
        
        self.fields = {}
        labels = [("Nomi", "name"), ("Narxi (so'm)", "price"), ("Razmeri", "size"), ("Rangi", "color"), ("Jami soni", "qty")]
        
        for label_text, key in labels:
            tk.Label(self.sidebar, text=label_text, bg="white", font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 0))
            entry = ttk.Entry(self.sidebar, font=("Segoe UI", 11))
            entry.pack(fill="x", ipady=5)
            self.fields[key] = entry
            
        tk.Button(self.sidebar, text="Qo'shish", bg="#2ecc71", fg="white", font=("Segoe UI", 11, "bold"), 
                  relief="flat", cursor="hand2", command=self.add_item).pack(fill="x", pady=20, ipady=5)
        
        tk.Button(self.sidebar, text="Tanlanganni o'chirish", bg="#e74c3c", fg="white", font=("Segoe UI", 10), 
                  relief="flat", cursor="hand2", command=self.delete_selected).pack(fill="x", pady=5, ipady=5)
        
        tk.Label(self.sidebar, text="Sana avtomatik belgilanadi", bg="white", fg="gray", font=("Segoe UI", 9)).pack(side="bottom")

    def setup_table(self):
        tk.Label(self.content, text="Ombordagi kiyimlar ro'yxati", bg="#f0f2f5", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        columns = ("id", "name", "price", "size", "color", "date", "total", "sold", "rem")
        self.tree = ttk.Treeview(self.content, columns=columns, show="headings")
        
        headings = [("ID", "id", 40), ("Nomi", "name", 150), ("Narxi", "price", 120), ("Razmeri", "size", 80), ("Rangi", "color", 100), ("Sana", "date", 100), ("Jami", "total", 70), ("Sotildi", "sold", 80), ("Qoldi", "rem", 70)]
        for text, col_id, width in headings:
            self.tree.heading(col_id, text=text)
            self.tree.column(col_id, width=width, anchor="center")
            
        self.tree.heading("date", text="Kelgan sana")
        self.tree.column("price", anchor="e")
        self.tree.grid(row=1, column=0, sticky="nswe")
        
        sb = ttk.Scrollbar(self.content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.grid(row=1, column=1, sticky="ns")
        
        self.tree.bind("<Double-1>", self.on_sell)
        
        tk.Label(self.content, text="Sotuvni qayd etish uchun kiyim ustiga ikki marta bosing", bg="#f0f2f5", fg="#7f8c8d", font=("Segoe UI", 10, "italic")).grid(row=2, column=0, pady=10)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        rows = database.get_all_items()
        for row in rows:
            # row: (id, name, price, size, color, date, total, sold)
            price_fmt = f"{row[2]:,} so'm".replace(",", " ")
            rem = row[6] - row[7]
            self.tree.insert("", "end", values=(row[0], row[1], price_fmt, row[3], row[4], row[5], row[6], row[7], rem))

    def add_item(self):
        data = {k: v.get().strip() for k, v in self.fields.items()}
        if not all(data.values()):
            messagebox.showwarning("Ogohlantirish", "Barcha maydonlarni to'ldiring!")
            return
            
        try:
            price = int(data['price'].replace(" ", ""))
            qty = int(data['qty'])
        except ValueError:
            messagebox.showerror("Xato", "Narx va Soni faqat raqam bo'lishi kerak!")
            return
            
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        database.add_item(data['name'], price, data['size'], data['color'], date_str, qty)
        
        for entry in self.fields.values():
            entry.delete(0, "end")
            
        self.load_data()
        messagebox.showinfo("Muvaffaqiyat", "Kiyim qo'shildi!")

    def on_sell(self, event):
        item_id = self.tree.selection()
        if not item_id: return
        
        vals = self.tree.item(item_id[0])['values']
        id_db = vals[0]
        name = vals[1]
        rem = vals[8]
        
        if rem <= 0:
            messagebox.showwarning("Xato", "Bu kiyim qolmagan!")
            return
            
        qty = simpledialog.askinteger("Sotuv", f"Qancha '{name}' sotildi? (Mavjud: {rem})", minvalue=1, maxvalue=rem)
        if qty:
            database.sell_item(id_db, qty)
            self.load_data()

    def delete_selected(self):
        item_id = self.tree.selection()
        if not item_id:
            messagebox.showwarning("Xato", "O'chirish uchun kiyimni tanlang!")
            return
            
        if messagebox.askyesno("Tasdiqlash", "Haqiqatan ham o'chirmoqchimisiz?"):
            id_db = self.tree.item(item_id[0])['values'][0]
            database.delete_item(id_db)
            self.load_data()

if __name__ == "__main__":
    app = App()
    app.mainloop()

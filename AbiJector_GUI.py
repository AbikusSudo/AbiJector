# AbiJector_GUI.py
import tkinter as tk
from tkinter import filedialog, messagebox
from AbiJector_LIB import AbiJector

class AbiJectorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AbiJector GUI")
        self.root.geometry("400x200")

        tk.Label(self.root, text="Target Process:").pack()
        self.process_entry = tk.Entry(self.root)
        self.process_entry.pack()

        tk.Label(self.root, text="DLL Path:").pack()
        self.dll_entry = tk.Entry(self.root)
        self.dll_entry.pack()
        tk.Button(self.root, text="Browse", command=self.browse_dll).pack()

        tk.Button(self.root, text="Inject DLL", command=self.inject).pack(pady=10)

    def browse_dll(self):
        path = filedialog.askopenfilename(filetypes=[("DLL Files", "*.dll")])
        if path:
            self.dll_entry.delete(0, tk.END)
            self.dll_entry.insert(0, path)

    def inject(self):
        try:
            injector = AbiJector(self.process_entry.get(), self.dll_entry.get())
            injector.inject()
            messagebox.showinfo("Success", "DLL injected!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AbiJectorGUI()
    app.run()
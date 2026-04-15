import ctypes
import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

lib_name = resource_path('core.dll')

try:
    lib = ctypes.CDLL(lib_name, winmode=0)
except OSError as e:
    error_root = tk.Tk()
    error_root.withdraw()
    messagebox.showerror("Lỗi hệ thống", f"Không tìm thấy thư viện lõi:\n{lib_name}\n\nVui lòng biên dịch file C++ trước.")
    sys.exit(1)

lib.find_word.restype = ctypes.c_char_p
lib.get_trie_state.restype = ctypes.c_char_p
lib.delete_word.restype = ctypes.c_int

# ==================== LOGIC XỬ LÝ ====================
def update_visualizer():
    tree_state = lib.get_trie_state().decode('utf-8')
    text_visualize.config(state=tk.NORMAL)
    text_visualize.delete(1.0, tk.END)
    text_visualize.insert(tk.END, tree_state)
    text_visualize.config(state=tk.DISABLED)

def on_add():
    word = entry_word.get().strip().encode('utf-8')
    word_type = combo_type.get()
    meaning = entry_meaning.get().strip()
    
    if word and meaning:
        data_str = f"{word_type}|{meaning}".encode('utf-8')
        lib.add_word(word, data_str)
        update_visualizer()
        entry_meaning.delete(0, tk.END)
        messagebox.showinfo("Thành công", f"Đã cập nhật từ: {word.decode('utf-8')}")
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đủ từ và nghĩa.")

def on_delete():
    word = entry_word.get().strip().encode('utf-8')
    if word:
        is_deleted = lib.delete_word(word)
        if is_deleted == 1:
            update_visualizer()
            messagebox.showinfo("Thành công", f"Đã xóa hoàn toàn nhánh chứa từ: {word.decode('utf-8')}")
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy từ '{word.decode('utf-8')}' trong cây!")
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập từ cần xóa.")

def on_search():
    word_input = entry_word.get().strip()
    word_encoded = word_input.encode('utf-8')
    
    text_result.config(state=tk.NORMAL)
    text_result.delete(1.0, tk.END)
    
    if word_encoded:
        result = lib.find_word(word_encoded).decode('utf-8')
        
        if result == "NOT_FOUND":
            text_result.insert(tk.END, f"Không tìm thấy từ: '{word_input}'\n", "error")
        else:
            # Thuật toán tách chuỗi và gom nhóm theo loại từ
            parts = result.split('||')
            meanings_dict = {}
            
            for p in parts:
                if '|' in p:
                    w_type, m = p.split('|', 1)
                    if w_type not in meanings_dict:
                        meanings_dict[w_type] = []
                    meanings_dict[w_type].append(m)
            
            # In ra màn hình UI
            text_result.insert(tk.END, f"🔍 KẾT QUẢ TRA CỨU:\n", "header")
            text_result.insert(tk.END, f"➤ Từ vựng: {word_input}\n", "bold")
            
            for w_type, means in meanings_dict.items():
                text_result.insert(tk.END, f"\n[{w_type}]\n", "bold")
                for idx, m in enumerate(means, 1):
                    text_result.insert(tk.END, f"   {idx}. {m}\n")
    else:
        text_result.insert(tk.END, "Vui lòng nhập từ cần tìm.", "error")
        
    text_result.config(state=tk.DISABLED)

# ==================== CẤU HÌNH GIAO DIỆN (UI) ====================
root = tk.Tk()
root.title("Từ Điển Tiếng Anh - Radix-Trie Core")
root.geometry("650x700")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Từ tiếng Anh:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_word = tk.Entry(frame_input, width=35)
entry_word.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

tk.Label(frame_input, text="Loại từ:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
combo_type = ttk.Combobox(frame_input, values=["Danh từ (N)", "Động từ (V)", "Tính từ (Adj)", "Trạng từ (Adv)", "Khác"], width=15)
combo_type.current(0)
combo_type.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_input, text="Nghĩa tiếng Việt:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_meaning = tk.Entry(frame_input, width=35)
entry_meaning.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="Thêm / Cập nhật", command=on_add, width=15, bg="#d4edda").grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Xóa từ", command=on_delete, width=15, bg="#f8d7da").grid(row=0, column=1, padx=10)
tk.Button(frame_buttons, text="Tra từ", command=on_search, width=15, bg="#cce5ff").grid(row=0, column=2, padx=10)

# Khung text tra cứu
text_result = tk.Text(root, height=8, width=70, bg="#ffffff", font=("Consolas", 11), state=tk.DISABLED)
text_result.pack(pady=10)

text_result.tag_config("header", foreground="blue", font=("Consolas", 12, "bold"))
text_result.tag_config("bold", font=("Consolas", 11, "bold"))
text_result.tag_config("error", foreground="red")

tk.Label(root, text="Trạng thái cấu trúc Radix-Trie (Data Visualization):").pack()
text_visualize = tk.Text(root, height=15, width=75, bg="#2b2b2b", fg="#a9b7c6", font=("Consolas", 10), state=tk.DISABLED)
text_visualize.pack(pady=5)

update_visualizer()
root.mainloop()
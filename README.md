# 🚀 Radix-Trie-Dictionary

**Sinh viên thực hiện:** Hà Hữu Trường An  
**Mã số sinh viên:** 24520042  
**Môn học:** Cấu trúc dữ liệu và Giải thuật nâng cap

Bài tập môn học: Xây dựng ứng dụng từ điển Tiếng Anh cơ bản (Thêm, Xóa, Tra cứu mục từ) sử dụng cấu trúc dữ liệu **Radix-Trie** (Cây cơ số) làm chỉ mục để tối ưu hóa không gian lưu trữ và tốc độ tìm kiếm.

Được phát triển bằng lõi xử lý **C++** tối ưu hiệu năng và trực quan hóa giao diện người dùng bằng **Python (Tkinter)**.

---

## ✨ Tính năng nổi bật

* **Lõi xử lý siêu tốc (High-Performance Core):** Xử lý toàn bộ logic của cấu trúc Radix-Trie bằng C++ thông qua C-API. Thời gian tra cứu cực nhanh $O(k)$ với $k$ là độ dài của từ, không phụ thuộc vào kích thước dữ liệu.
* **Trực quan hóa cấu trúc dữ liệu (Data Visualization):** Theo dõi trực tiếp sự thay đổi của cây Radix-Trie (cắt nhánh, gộp node, cập nhật nghĩa) trên Console Log của UI ngay sau mỗi thao tác của người dùng.
* **Hỗ trợ Đa nghĩa & Loại từ (Multi-meaning Support):** Cho phép lưu trữ và hiển thị linh hoạt nhiều loại từ (Noun, Verb, Adj,...) và nhiều nghĩa cho cùng một từ vựng.
* **Thuật toán Cắt tỉa thông minh (Smart Pruning):** Tích hợp đệ quy để dọn dẹp bộ nhớ khi xóa mục từ. Hệ thống tự động nhận diện để xóa sổ (Free Memory) nhánh rỗng hoặc gộp (Merge) các nhánh con dư thừa, đảm bảo tính toàn vẹn của cây.
* **Giao tiếp Cross-Language:** Tích hợp mượt mà giữa thư viện liên kết động (Shared Library `.dll`) của C++ và bộ nạp `ctypes` của Python.

---

## 🛠️ Công nghệ sử dụng

* **Core:** `C++` (Standard Template Library: `<string>`, `<map>`, `<sstream>`, `extern "C"`).
* **GUI:** `Python 3` (Thư viện `tkinter`, `ctypes`, `os`, `sys`).
* **Packaging:** `PyInstaller` (Đóng gói lõi C++ và môi trường Python thành tệp thực thi độc lập).

---

## 🚀 Cài đặt và Sử dụng

### Tải bản chạy trực tiếp (Dành cho Windows)
Hệ thống đã được đóng gói sẵn thành tệp `.exe`, không cần cài đặt môi trường C++ hay Python trên máy tính.

1. Truy cập vào mục **[Releases](../../releases)** bên góc phải của Repository này.
2. Tải xuống tệp `tudienAnh_Viet.exe`.
3. Click đúp chuột để chạy trực tiếp trên Windows và sử dụng.

---

## 📚 Tài liệu tham khảo (References)

1. **Donald R. Morrison (1968)**, *PATRICIA—Practical Algorithm To Retrieve Information Coded in Alphanumeric*, Journal of the ACM.
2. **Wikipedia Contributors**, *Radix tree*, truy cập tại: [https://en.wikipedia.org/wiki/Radix_tree](https://en.wikipedia.org/wiki/Radix_tree)
3. **GeeksforGeeks**, *Radix Tree (Compressed Trie)*, truy cập tại: [https://www.geeksforgeeks.org/radix-tree-compressed-trie/](https://www.geeksforgeeks.org/radix-tree-compressed-trie/)
4. **Python Software Foundation**, *ctypes — A foreign function library for Python*, truy cập tại: [https://docs.python.org/3/library/ctypes.html](https://docs.python.org/3/library/ctypes.html)
5. 5. **C++ Reference**, *C++ Standard Library (`<string>`, `<map>`, `<sstream>`, `<cstring>`)*, truy cập tại: [https://cplusplus.com/reference/](https://cplusplus.com/reference/)

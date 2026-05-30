====================================================================
HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY CHƯƠNG TRÌNH SO SÁNH THUẬT TOÁN TSP
====================================================================

Chương trình này thực thi và so sánh hiệu năng của các thuật toán giải quyết bài toán Người chào hàng (Traveling Salesperson Problem - TSP) bao gồm: Nearest Neighbor, Simulated Annealing, Cheapest Insertion và Hill Climbing.

Để chạy chương trình (file `dsprojectfinal.py`), vui lòng làm theo các bước hướng dẫn dưới đây.

### BƯỚC 1: TẢI VÀ GIẢI NÉN DATASET
Chương trình sử dụng dữ liệu chuẩn từ thư viện TSPLIB.
1. Truy cập vào đường dẫn sau: https://github.com/mastqe/tsplib
2. Tải toàn bộ repository về máy tính (chọn nút "Code" màu xanh lá -> "Download ZIP").
3. Giải nén file ZIP vừa tải ra một thư mục trên máy tính của bạn.

### BƯỚC 2: SAO CHÉP ĐƯỜNG DẪN THƯ MỤC DATASET
1. Mở thư mục bạn vừa giải nén (thư mục chứa rất nhiều file có đuôi `.tsp`).
2. Nhấn vào thanh địa chỉ (Address bar) của File Explorer và sao chép toàn bộ đường dẫn tuyệt đối.
   (Ví dụ đường dẫn sao chép được sẽ trông giống như: C:\Users\Admin\Downloads\tsplib-master)

### BƯỚC 3: CẤU HÌNH MÃ NGUỒN CHƯƠNG TRÌNH
Mở file `dsprojectfinal.py` bằng bất kỳ trình soạn thảo code nào (VS Code, PyCharm, Notepad++...) và tìm đến đoạn mã ở cuối file (khoảng dòng 403 và 404).

1. Dán đường dẫn thư mục dataset:
   Tại dòng 403, thay thế đường dẫn cũ trong biến `base_path` bằng đường dẫn bạn vừa sao chép ở Bước 2. 
   Lưu ý: Bắt buộc giữ lại chữ 'r' ở ngay trước dấu ngoặc kép để Python hiểu đúng các ký tự gạch chéo trong đường dẫn.
   
   Thay đổi từ: 
   base_path = r"D:\duyManh\Study\discreteMaths\p1"
   
   Thành (Ví dụ):
   base_path = r"C:\Users\Admin\Downloads\tsplib-master"

2. Chọn dataset muốn chạy:
   Tại dòng 404, thay đổi giá trị của biến `file_name` thành tên file dataset cụ thể mà bạn muốn thuật toán xử lý (ví dụ: "a280.tsp", "berlin52.tsp", "ch150.tsp"...).
   
   Ví dụ:
   file_name = "berlin52.tsp"

### BƯỚC 4: CHẠY CHƯƠNG TRÌNH
1. Mở Terminal (hoặc Command Prompt / PowerShell).
2. Dùng lệnh `cd` để di chuyển đến thư mục chứa file `dsprojectfinal.py`.
3. Chạy chương trình bằng lệnh sau:
   python dsprojectfinal.py
4. Đợi chương trình xử lý và theo dõi "Báo cáo đối sánh hiệu năng toàn diện" xuất ra trên màn hình console.

---

====================================================================
SETUP AND EXECUTION GUIDE FOR TSP ALGORITHM COMPARISON
====================================================================

This program executes and compares the performance of Traveling Salesperson Problem (TSP) algorithms, including: Nearest Neighbor, Simulated Annealing, Cheapest Insertion, and Hill Climbing.

To run the program (the `dsprojectfinal.py` file), please follow the instructions below.

### STEP 1: DOWNLOAD AND EXTRACT THE DATASET
The program uses standard datasets from the TSPLIB library.
1. Go to the following link: https://github.com/mastqe/tsplib
2. Download the entire repository (Click the green "Code" button -> "Download ZIP").
3. Extract the downloaded ZIP file to a folder on your computer.

### STEP 2: COPY THE DATASET FOLDER PATH
1. Open the folder you just extracted (the folder containing many `.tsp` files).
2. Click on the File Explorer Address bar and copy the absolute path.
   (Example path: C:\Users\Admin\Downloads\tsplib-master)

### STEP 3: CONFIGURE THE SOURCE CODE
Open the `dsprojectfinal.py` file in any code editor (VS Code, PyCharm, Notepad++, etc.) and go to the bottom of the file (around lines 403 and 404).

1. Paste the dataset folder path:
   At line 403, replace the old path in the `base_path` variable with the path you copied in Step 2. 
   Note: You MUST keep the letter 'r' right before the opening quote so Python correctly parses the backslashes in the path.
   
   Change from: 
   base_path = r"D:\duyManh\Study\discreteMaths\p1"
   
   To (Example):
   base_path = r"C:\Users\Admin\Downloads\tsplib-master"

2. Select the dataset to run:
   At line 404, change the value of the `file_name` variable to the specific dataset file you want the algorithm to process (e.g., "a280.tsp", "berlin52.tsp", "ch150.tsp"...).
   
   Example:
   file_name = "berlin52.tsp"

### STEP 4: RUN THE PROGRAM
1. Open Terminal (or Command Prompt / PowerShell).
2. Use the `cd` command to navigate to the directory containing the `dsprojectfinal.py` file.
3. Run the program using the following command:
   python dsprojectfinal.py
4. Wait for the program to process and review the "COMPREHENSIVE BENCHMARK" report printed on the console.

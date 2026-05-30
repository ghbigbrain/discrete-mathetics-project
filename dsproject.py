import math
import time
import os
import random
import tracemalloc

# HUONG DOI TUONG(OOP)
class City:
    """Lớp đại diện cho một thành phố (một đỉnh trong đồ thị)."""
    def __init__(self, city_id, x, y):
        self.city_id = city_id  # Số thứ tự của thành phố
        self.x = x              # Tọa độ X
        self.y = y              # Tọa độ Y

    def distance_to(self, other_city):
        """Tính khoảng cách đường thẳng (Euclid 2D) giữa thành phố này và một thành phố khác."""
        dx = self.x - other_city.x
        dy = self.y - other_city.y
        # Công thức tính cạnh huyền trong tam giác vuông: sqrt(dx^2 + dy^2)
        return math.sqrt(dx**2 + dy**2)

    def __str__(self):
        # Trả về ID của thành phố dưới dạng chuỗi để dễ in ấn
        return str(self.city_id)


# HÀM ĐỌC DỮ LIỆU TỪ FILE TSPLIB
def load_tsp_file(filepath):
    """Đọc dữ liệu từ file .tsp chuẩn và tạo ra danh sách các đối tượng City."""
    cities = []
    with open(filepath, "r") as file:
        is_node_section = False  # Cờ đánh dấu khi nào bắt đầu đọc tọa độ
        for line in file:
            line = line.strip()
            # Bỏ qua các dòng trống hoặc dòng đánh dấu kết thúc file
            if not line or line == "EOF":
                continue
            
            # Khi gặp dòng này, các dòng tiếp theo sẽ là dữ liệu tọa độ
            if line.startswith("NODE_COORD_SECTION"):
                is_node_section = True
                continue
                
            # Tiến hành tách lấy ID, X, Y
            if is_node_section:
                parts = line.split()
                if len(parts) >= 3:
                    city_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    cities.append(City(city_id, x, y))
    return cities


# THUẬT TOÁN THAM LAM (NEAREST NEIGHBOR)
def find_nearest_unvisited_city(current_city, unvisited):
    """Tìm thành phố gần nhất với thành phố hiện tại trong tập hợp các thành phố chưa đi qua."""
    nearest_city = None
    min_distance = float('inf') # Khởi tạo khoảng cách nhỏ nhất là vô cùng lớn
    
    for city in unvisited:
        dist = current_city.distance_to(city)
        if dist < min_distance:
            min_distance = dist
            nearest_city = city
            
    return nearest_city, min_distance

def nearest_neighbor_tsp(cities, start_index=0):
    """
    Ý tưởng: Bắt đầu từ 1 đỉnh, liên tục chọn đỉnh chưa thăm gần nhất để đi tiếp 
    cho đến khi đi qua hết tất cả các đỉnh. Cuối cùng quay về đỉnh xuất phát.
    """
    if not cities:
        return [], 0.0

    unvisited = set(cities)             # Tập hợp các thành phố chưa đi qua
    current = cities[start_index]       # Chọn điểm xuất phát
    unvisited.remove(current)           # Đánh dấu điểm xuất phát là đã thăm
    
    tour = [current]                    # Lưu lộ trình
    total_distance = 0.0                # Tổng độ dài quãng đường

    # Lặp cho đến khi không còn thành phố nào chưa thăm
    while len(unvisited) > 0:
        next_city, dist = find_nearest_unvisited_city(current, unvisited)
        tour.append(next_city)          # Thêm đỉnh tìm được vào lộ trình
        unvisited.remove(next_city)     # Xóa đỉnh đó khỏi tập chưa thăm
        total_distance += dist          # Cộng dồn khoảng cách
        current = next_city             # Di chuyển sang thành phố mới

    # Khép kín chu trình: Cọng thêm khoảng cách từ điểm cuối về lại điểm xuất phát
    total_distance += current.distance_to(tour[0])
    return tour, total_distance


# THUẬT TOÁN CHÈN RẺ NHẤT (CHEAPEST INSERTION)
def nearest_pair_seed(cities):
    """Tìm 2 thành phố có khoảng cách gần nhau nhất trong toàn bộ bản đồ để làm chu trình gốc."""
    if len(cities) < 2:
        return cities.copy()

    min_distance = float('inf')
    best_pair = None
    
    # Duyệt qua tất cả các cặp đỉnh để tìm cặp có khoảng cách nhỏ nhất
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            dist = cities[i].distance_to(cities[j])
            if dist < min_distance:
                min_distance = dist
                best_pair = (cities[i], cities[j])

    return [best_pair[0], best_pair[1]]

def best_insertion_position(tour, city):
    """
    Thử nghiệm chèn 'city' vào giữa tất cả các cặp cạnh hiện có trong 'tour'.
    Trả về vị trí chèn làm tăng tổng khoảng cách lên ít nhất (delta nhỏ nhất).
    """
    best_pos = None
    best_delta = float('inf')
    n = len(tour)
    
    for i in range(n):
        current_city = tour[i]
        next_city = tour[(i + 1) % n] # Dùng % n để nối đỉnh cuối với đỉnh đầu
        
        # Công thức tính chi phí tăng thêm (Delta) khi chèn điểm C vào giữa A và B:
        # Chi phí mới = d(A, C) + d(C, B)
        # Chi phí cũ bị loại bỏ = d(A, B)
        # Delta = Chi phí mới - Chi phí cũ
        delta = (current_city.distance_to(city) + city.distance_to(next_city) - current_city.distance_to(next_city))
        
        if delta < best_delta:
            best_delta = delta
            best_pos = i + 1  # Vị trí chèn lý tưởng là ngay sau current_city
            
    return best_pos, best_delta

def cheapest_insertion_tsp(cities, start_index=0):
    """
    Ý tưởng: Bắt đầu với 1 chu trình nhỏ gồm 2 đỉnh. Lặp lại việc chọn 1 đỉnh mới
    chưa có trong chu trình và chèn nó vào vị trí làm cho chu trình phình ra ít nhất.
    """
    n = len(cities)
    if n == 0: return [], 0.0
    if n == 1: return [cities[0]], 0.0
    if n == 2: return [cities[0], cities[1]], cities[0].distance_to(cities[1]) * 2

    tour = nearest_pair_seed(cities)            # Khởi tạo chu trình mầm
    remaining = set(cities) - set(tour)         # Các đỉnh đang nằm ngoài chu trình

    while len(remaining) > 0:
        best_node = None
        best_pos = None
        best_delta = float('inf')

        # Thử tính toán vị trí chèn tốt nhất cho TỪNG thành phố đang ở ngoài chu trình
        for city in remaining:
            pos, delta = best_insertion_position(tour, city)

            # Giữ lại thành phố và vị trí mang lại chi phí phát sinh (delta) bé nhất
            if delta < best_delta:
                best_delta = delta
                best_node = city
                best_pos = pos

        # Chính thức chèn thành phố "rẻ nhất" vào chu trình và xóa khỏi danh sách chờ
        tour.insert(best_pos, best_node)
        remaining.remove(best_node)

    # Sau khi chèn xong tất cả, tính toán lại tổng chiều dài cuối cùng
    total_distance = 0.0
    for i in range(len(tour)):
        total_distance += tour[i].distance_to(tour[(i + 1) % len(tour)])

    return tour, total_distance


# TỐI ƯU CỤC BỘ: HILL CLIMBING 2-OPT (Dùng nâng cấp Cheapest Insertion)
def hill_climbing_tsp(tour, initial_distance):
    """
    Ý tưởng: Thử gỡ bỏ 2 cạnh bất kỳ đang cắt nhau và nối chéo chúng lại (phép 2-opt).
    Nếu hành động này làm giảm tổng khoảng cách, chấp nhận ngay lập tức.
    Làm liên tục cho đến khi không thể tìm được cách đổi cạnh nào làm giảm khoảng cách nữa.
    """
    n = len(tour)
    if n < 3: return tour, initial_distance

    current_tour = tour.copy()
    current_distance = initial_distance
    
    while True:
        best_delta = 0.0
        best_i = -1
        best_j = -1
        
        # Duyệt qua tất cả các cặp cạnh có thể đổi cho nhau
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                city_a = current_tour[i - 1]
                city_b = current_tour[i]
                city_c = current_tour[j]
                city_d = current_tour[(j + 1) % n] 

                # Nếu phá bỏ cạnh (A->B) và (C->D), nối lại thành (A->C) và (B->D)
                old_dist = city_a.distance_to(city_b) + city_c.distance_to(city_d)
                new_dist = city_a.distance_to(city_c) + city_b.distance_to(city_d)
                delta = new_dist - old_dist # Mức độ thay đổi (Âm = đường ngắn đi, tốt)
                
                # Tìm phép đổi làm giảm quãng đường nhiều nhất
                if delta < best_delta - 1e-9: 
                    best_delta = delta
                    best_i = i
                    best_j = j
        
        # Nếu không còn phép đổi nào làm delta âm (không cải thiện được nữa) thì dừng lại
        if best_i == -1:
            break
            
        # Áp dụng thay đổi: Đảo ngược các đỉnh nằm giữa i và j để nối chéo
        current_tour[best_i : best_j + 1] = reversed(current_tour[best_i : best_j + 1])
        current_distance += best_delta
        
    return current_tour, current_distance


# TỐI ƯU TOÀN CỤC: SIMULATED ANNEALING (Dùng nâng cấp Nearest Neighbor)
def simulated_annealing_tsp(tour, initial_distance, temp=100.0, cooling_rate=0.9999):
    """
    Ý tưởng Mô phỏng Luyện kim: 
    Giống Hill Climbing nhưng thông minh hơn: Nó thỉnh thoảng CHẤP NHẬN các bước đi "tệ hơn" 
    (làm tăng khoảng cách) với một xác suất nhất định để thoát khỏi các bẫy cực tiểu cục bộ.
    Xác suất này phụ thuộc vào "Nhiệt độ" (temp) - nhiệt độ càng giảm thì thuật toán càng ít liều lĩnh.
    """
    n = len(tour)
    if n < 3: return tour, initial_distance

    current_tour = tour.copy()
    current_distance = initial_distance
    
    # Biến lưu lại kết quả tốt nhất từng tìm thấy trong quá trình chạy
    best_tour = current_tour.copy()
    best_distance = current_distance

    # Chạy cho đến khi "nhiệt độ" nguội đi gần bằng 0
    while temp > 1e-4:
        # Khác với Hill Climbing duyệt mọi cạnh, SA chỉ LẤY NGẪU NHIÊN 2 vị trí để đổi
        i = random.randint(1, n - 2)
        j = random.randint(i + 1, n - 1)

        city_a = current_tour[i - 1]
        city_b = current_tour[i]
        city_c = current_tour[j]
        city_d = current_tour[(j + 1) % n]

        old_dist = city_a.distance_to(city_b) + city_c.distance_to(city_d)
        new_dist = city_a.distance_to(city_c) + city_b.distance_to(city_d)
        
        delta = new_dist - old_dist
        accept = False
        
        if delta < 0:
            # Nếu đường đi ngắn lại => Chấp nhận luôn (Giống Hill Climbing)
            accept = True
        else:
            # NẾU ĐƯỜNG ĐI DÀI HƠN: Tính xác suất chấp nhận rủi ro (Metropolis)
            probability = math.exp(-delta / temp)
            # Random 1 số từ 0 đến 1, nếu nhỏ hơn xác suất trên thì nhắm mắt chấp nhận
            if probability > random.random():
                accept = True

        if accept:
            # Thực hiện nối chéo 2 cạnh
            current_tour[i : j + 1] = reversed(current_tour[i : j + 1])
            current_distance += delta
            
            # Cập nhật kỷ lục nếu tìm thấy đường đi ngắn nhất từ trước đến nay
            if current_distance < best_distance:
                best_distance = current_distance
                best_tour = current_tour.copy()

        # Hạ nhiệt độ (Giảm dần sự liều lĩnh theo thời gian)
        temp *= cooling_rate

    # Trả về kết quả tốt nhất từng ghi nhận
    return best_tour, best_distance


# 7. HÀM KIỂM TRA TÍNH HỢP LỆ (VALIDATION)
def validate_tour(tour, original_cities):
    """Đảm bảo thuật toán không ăn gian (không bỏ sót đỉnh, không sinh thêm đỉnh ảo)."""
    if not tour:
        return False, "Lỗi: Chu trình rỗng."
    if len(tour) != len(original_cities):
        return False, f"Lỗi: Số lượng đỉnh ({len(tour)}) khác dữ liệu gốc ({len(original_cities)})."
    
    tour_ids = set(city.city_id for city in tour)
    original_ids = set(city.city_id for city in original_cities)
    
    if tour_ids != original_ids:
        return False, f"Lỗi: Bỏ sót hoặc sai đỉnh."
        
    return True, "Hợp lệ"

# 8. CHƯƠNG TRÌNH CHÍNH (MAIN ENTRY POINT) (ALGORITHM)
'''
if __name__ == "__main__":
    # Đường dẫn trỏ tới file dữ liệu
    base_path = r"" #
    file_name = "" #
    
    dataset_path = os.path.join(base_path, file_name)

    print(f"Đang đọc dữ liệu từ: {dataset_path}...")
    try:
        all_cities = load_tsp_file(dataset_path)
        
        if not all_cities:
            print("[LỖI] File rỗng hoặc sai định dạng (không tìm thấy phần NODE_COORD_SECTION).")
        else:
            print(f"Đã nạp thành công {len(all_cities)} thành phố.\n")
            
            # THỰC NGHIỆM 1: So sánh Nearest Neighbor gốc và SA tối ưu hóa
            print("Đang chạy: Nearest Neighbor...")
            start_time_nn = time.time()
            tracemalloc.start()
            tour_nn, dist_nn = nearest_neighbor_tsp(all_cities, start_index=0)
            exec_ms_nn = (time.time() - start_time_nn) * 1000 
            _, peak_mem_nn = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            print("Đang chạy: Simulated Annealing (Tối ưu kết quả NN)...")
            start_time_sa = time.time()
            tour_sa, dist_sa = simulated_annealing_tsp(tour_nn, dist_nn)
            # Tổng thời gian SA = Thời gian chạy gốc NN + Thời gian chạy SA
            exec_ms_sa = exec_ms_nn + (time.time() - start_time_sa) * 1000
            
            # THỰC NGHIỆM 2: So sánh Cheapest Insertion gốc và HC tối ưu hóa
            print("Đang chạy: Cheapest Insertion...")
            start_time_ci = time.time()
            tour_ci, dist_ci = cheapest_insertion_tsp(all_cities, start_index=0)
            exec_ms_ci = (time.time() - start_time_ci) * 1000 
            
            print("Đang chạy: Hill Climbing (Tối ưu kết quả CI)...")
            start_time_hc = time.time()
            tour_hc, dist_hc = hill_climbing_tsp(tour_ci, dist_ci)
            # Tổng thời gian HC = Thời gian chạy gốc CI + Thời gian chạy HC
            exec_ms_hc = exec_ms_ci + (time.time() - start_time_hc) * 1000

            # KIỂM TRA ĐẦU RA VÀ IN BÁO CÁO KẾT QUẢ
            val_nn = validate_tour(tour_nn, all_cities)[0]
            val_sa = validate_tour(tour_sa, all_cities)[0]
            val_ci = validate_tour(tour_ci, all_cities)[0]
            val_hc = validate_tour(tour_hc, all_cities)[0]

            print("\n" + "=" * 80)
            print("KẾT QUẢ SO SÁNH: SỰ ĐÁNH ĐỔI (TRADE-OFF) GIỮA CHẤT LƯỢNG VÀ THỜI GIAN")
            print("=" * 80)
            
            # --- Cụm 1: NN & SA ---
            print("NEAREST NEIGHBOR (NN) & SIMULATED ANNEALING (SA)")
            if val_nn:
                print(f" - [Khởi tạo] NN          : Quãng đường = {dist_nn:.2f} | T/gian chạy: {exec_ms_nn:.2f} ms")
            if val_sa:
                # Tránh chia cho 0 nếu thời gian chạy quá nhanh (0.0 ms)
                safe_exec_ms_nn = max(exec_ms_nn, 0.001) 
                
                percent_sa_dist = (dist_nn - dist_sa) / dist_nn * 100
                percent_sa_time = ((exec_ms_sa - exec_ms_nn) / safe_exec_ms_nn) * 100
                
                print(f" - [Tối ưu]   SA (tối ưu NN) : Quãng đường = {dist_sa:.2f} | Tổng t/gian: {exec_ms_sa:.2f} ms")
                print(f"   Quãng đường giảm {percent_sa_dist:.2f}% NHƯNG thời gian chạy tăng {percent_sa_time:.0f}%.")
            
            print("-" * 80)
            
            # --- Cụm 2: CI & HC ---
            print("CHEAPEST INSERTION (CI) & HILL CLIMBING (HC)")
            if val_ci:
                print(f" - [Khởi tạo] CI          : Quãng đường = {dist_ci:.2f} | T/gian chạy: {exec_ms_ci:.2f} ms")
            if val_hc:
                safe_exec_ms_ci = max(exec_ms_ci, 0.001)
                
                percent_hc_dist = (dist_ci - dist_hc) / dist_ci * 100
                percent_hc_time = ((exec_ms_hc - exec_ms_ci) / safe_exec_ms_ci) * 100
                
                print(f" - [Tối ưu]   HC (tối ưu CI) : Quãng đường = {dist_hc:.2f} | Tổng t/gian: {exec_ms_hc:.2f} ms")
                print(f"   Quãng đường giảm {percent_hc_dist:.2f}% NHƯNG thời gian chạy tăng {percent_hc_time:.0f}%.")
            
            print("=" * 80)

    # Bắt các trường hợp lỗi có thể xảy ra trong quá trình chạy
    except FileNotFoundError:
        print(f"\n[LỖI] Không tìm thấy file {file_name}!")
        print(f"Hãy kiểm tra lại xem file đã nằm trong thư mục {base_path} chưa.")
    except Exception as e:
        print(f"\n[LỖI CHƯA XÁC ĐỊNH] Có lỗi xảy ra trong quá trình chạy: {e}")
'''
# 8. CHƯƠNG TRÌNH CHÍNH (MAIN ENTRY POINT) (METHOD)
''''''
if __name__ == "__main__":
    base_path = r"D:\duyManh\Study\discreteMaths\p1"
    file_name = "att48.tsp" 
    dataset_path = os.path.join(base_path, file_name)

    try:
        all_cities = load_tsp_file(dataset_path)
        if not all_cities:
            print("[ERROR] Empty dataset or invalid format.")
            exit()
            
        num_vertices = len(all_cities)
        print(f"[INFO] Successfully loaded {num_vertices} cities.\n")
        
        # =====================================================================
        # METHOD 1: HYBRID STOCHASTIC PIPELINE (NN + SA)
        # =====================================================================
        tracemalloc.start()
        start_time_m1 = time.time()
        
        init_tour_m1, init_dist_m1 = nearest_neighbor_tsp(all_cities, start_index=0)
        final_tour_m1, final_dist_m1 = simulated_annealing_tsp(init_tour_m1, init_dist_m1)
        
        elapsed_time_m1 = (time.time() - start_time_m1) * 1000  # ms
        _, peak_mem_m1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # =====================================================================
        # METHOD 2: HYBRID DETERMINISTIC PIPELINE (CI + HC)
        # =====================================================================
        tracemalloc.start()
        start_time_m2 = time.time()
        
        init_tour_m2, init_dist_m2 = cheapest_insertion_tsp(all_cities, start_index=0)
        final_tour_m2, final_dist_m2 = hill_climbing_tsp(init_tour_m2, init_dist_m2)
        
        elapsed_time_m2 = (time.time() - start_time_m2) * 1000  # ms
        _, peak_mem_m2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # =====================================================================
        # ADVANCED ANALYSIS & DEEP COMPARISON REPORT
        # =====================================================================
        # 1. Tính toán các thông số bổ sung về Chất lượng (Quality)
        imp_rate_m1 = ((init_dist_m1 - final_dist_m1) / init_dist_m1) * 100
        imp_rate_m2 = ((init_dist_m2 - final_dist_m2) / init_dist_m2) * 100
        
        # 2. Tính toán hiệu suất tối ưu (Distance reduced per millisecond)
        # Tránh chia cho 0 nếu thời gian quá nhỏ
        time_m1_safe = max(elapsed_time_m1, 0.001)
        time_m2_safe = max(elapsed_time_m2, 0.001)
        opt_efficiency_m1 = (init_dist_m1 - final_dist_m1) / time_m1_safe
        opt_efficiency_m2 = (init_dist_m2 - final_dist_m2) / time_m2_safe
        
        # 3. Tính toán chỉ số tích hợp Không gian - Thời gian (Space-Time Cost)
        # Đơn vị: KB.ms (Càng nhỏ chứng tỏ thuật toán càng tối ưu tài nguyên hệ thống)
        mem_kb_m1 = peak_mem_m1 / 1024
        mem_kb_m2 = peak_mem_m2 / 1024
        space_time_cost_m1 = mem_kb_m1 * elapsed_time_m1
        space_time_cost_m2 = mem_kb_m2 * elapsed_time_m2

        print("=" * 90)
        print("              BÁO CÁO ĐỐI SÁNH HIỆU NĂNG TOÀN DIỆN (COMPREHENSIVE BENCHMARK)")
        print("=" * 90)
        print(f"{'Thông số đo đạc (Metrics)':<40} | {'Method 1 (NN+SA)':<20} | {'Method 2 (CI+HC)':<20}")
        print("-" * 90)
        
        # Trục 1: Chất lượng giải pháp (Solution Quality)
        print(f"{'1. Lộ trình khởi tạo (Initial Tour)':<40} | {init_dist_m1:<20.2f} | {init_dist_m2:<20.2f}")
        print(f"{'2. Lộ trình tối ưu cuối (Final Tour)':<40} | {final_dist_m1:<20.2f} | {final_dist_m2:<20.2f}")
        print(f"{'3. Tỷ lệ cải thiện (Improvement Rate)':<40} | {f'{imp_rate_m1:.2f}%':<20} | {f'{imp_rate_m2:.2f}%':<20}")
        print("-" * 90)
        
        # Trục 2: Chi phí thời gian (Time Complexity)
        print(f"{'4. Tổng thời gian chạy (Execution Time)':<40} | {f'{elapsed_time_m1:.2f} ms':<20} | {f'{elapsed_time_m2:.2f} ms':<20}")
        print(f"{'5. Thời gian trung bình/Nút (Time/Node)':<40} | {f'{elapsed_time_m1/num_vertices:.3f} ms':<20} | {f'{elapsed_time_m2/num_vertices:.3f} ms':<20}")
        print("-" * 90)
        
        # Trục 3: Hiệu năng không gian (Space Complexity)
        print(f"{'6. Bộ nhớ RAM đỉnh (Peak Memory)':<40} | {f'{mem_kb_m1:.2f} KB':<20} | {f'{mem_kb_m2:.2f} KB':<20}")
        print(f"{'7. Bộ nhớ trung bình/Nút (Memory/Node)':<40} | {f'{mem_kb_m1/num_vertices:.3f} KB':<20} | {f'{mem_kb_m2/num_vertices:.3f} KB':<20}")
        print("-" * 90)
        
        # Trục 4: Chỉ số đánh đổi hệ thống (System Trade-off Metrics)
        print(f"{'8. Tốc độ tối ưu (Dist Reduced/ms)':<40} | {opt_efficiency_m1:<20.3f} | {opt_efficiency_m2:<20.3f}")
        print(f"{'9. Chỉ số hao tổn (Space-Time Cost)':<40} | {f'{space_time_cost_m1:.2f} KB.ms':<20} | {f'{space_time_cost_m2:.2f} KB.ms':<20}")
        print("=" * 90)

        # Đoạn diễn giải phân tích tự động
        print("\n[PHÂN TÍCH ĐÁNH GIÁ (ANALYTICAL SUMMARY)]")
        # So sánh chất lượng
        better_q = "Method 1" if final_dist_m1 < final_dist_m2 else "Method 2"
        q_gap = abs(final_dist_m1 - final_dist_m2) / max(final_dist_m1, final_dist_m2) * 100
        print(f" -> Về Chất lượng: {better_q} cho kết quả tốt hơn với độ lệch {q_gap:.2f}%.")
        
        # So sánh không gian và thời gian
        fastest = "Method 1" if elapsed_time_m1 < elapsed_time_m2 else "Method 2"
        most_eco = "Method 1" if mem_kb_m1 < mem_kb_m2 else "Method 2"
        print(f" -> Về Thời gian: {fastest} tối ưu thời gian xử lý vượt trội hơn.")
        print(f" -> Về Không gian: Lượng RAM tiêu thụ thực nghiệm của cả hai tương đương (đều ở mức rất thấp ~vài KB) "
              f"do cấu trúc lưu trữ danh sách tọa độ thay vì ma trận kề full. Tuy nhiên, {most_eco} có lượng RAM đỉnh thấp hơn.")

    except FileNotFoundError:
        print(f"[ERROR] File '{file_name}' not found.")
''''''

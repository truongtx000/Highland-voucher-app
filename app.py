import streamlit as st
from itertools import combinations
import math

# Cấu hình trang của Streamlit
st.set_page_config(page_title="Tiết Kiệm Highland Cùng Voucher", layout="centered")

# --- CSS Tùy Chỉnh để tạo giao diện như hình bạn cung cấp ---
st.markdown(
    """
<style>
/* Đặt màu nền chung cho toàn bộ trang */
body {
    background-color: #f5f5f5; /* Màu xám nhạt */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Font chữ hiện đại */
}

/* Container chính bao bọc toàn bộ nội dung ứng dụng */
.main-container {
    background-color: #f9f9f9; /* Nền trắng ngà cho container chính */
    padding: 30px;
    border-radius: 15px; /* Bo góc nhẹ */
    box-shadow: 0 2px 10px rgba(0,0,0,.1); /* Đổ bóng nhẹ nhàng */
    margin-top: 30px;
}

/* Phần tiêu đề ứng dụng (Highland Voucher App) */
.header-bg {
    background: linear-gradient(to bottom, #B71C1C, #E53935); /* Gradient màu đỏ đặc trưng của Highland */
    color: white;
    padding: 25px 0 15px 0; /* Đệm trên dưới, không đệm ngang */
    border-radius: 10px 10px 0 0; /* Bo góc trên */
    text-align: center;
    margin-bottom: 25px; /* Khoảng cách với phần tiếp theo */
    box-shadow: 0 4px 8px rgba(0,0,0,0.15); /* Đổ bóng mạnh hơn cho header */
}

.header-title {
    font-size: 2.8em; /* Kích thước chữ lớn */
    font-weight: 900; /* Rất đậm */
    margin-bottom: 5px;
    letter-spacing: 1px; /* Khoảng cách giữa các chữ cái */
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2); /* Đổ bóng chữ */
}

/* Tiêu đề phụ trong header */
.header-subtitle {
    font-size: 1.6em;
    font-weight: 600;
    margin-top: 0;
    opacity: 0.9; /* Hơi mờ hơn tiêu đề chính */
}

/* Container cho mỗi phần nhập liệu (Món ăn, Voucher) */
.input-container {
    background-color: white;
    padding: 25px;
    border-radius: 12px; /* Bo góc */
    margin-bottom: 25px;
    border: 1px solid #e0e0e0; /* Viền nhạt */
    box-shadow: 1px 1px 6px rgba(0,0,0,.08); /* Đổ bóng */
}

/* Header của từng phần nhập liệu (ví dụ: "Nhập danh sách món") */
.input-header {
    display: flex; /* Dùng flexbox để căn chỉnh icon và text */
    align-items: center; /* Căn giữa theo chiều dọc */
    margin-bottom: 15px;
}

.input-header-icon {
    font-size: 2.2em; /* Kích thước icon lớn */
    margin-right: 12px;
    color: #FFC107; /* Màu vàng cam cho icon */
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.input-header-text {
    font-size: 1.5em; /* Kích thước chữ tiêu đề */
    font-weight: bold;
    color: #333;
}

/* Định dạng cho vùng nhập liệu (text area) */
.stTextArea textarea {
    border-radius: 10px; /* Bo góc */
    border: 1px solid #c0c0c0; /* Viền xám */
    padding: 12px;
    box-shadow: inset 1px 1px 4px rgba(0,0,0,0.1); /* Đổ bóng bên trong */
    width: 100%; /* Chiếm toàn bộ chiều rộng */
    box-sizing: border-box; /* Tính cả padding và border vào width */
    font-size: 1.1em;
    min-height: 120px; /* Chiều cao tối thiểu */
}

/* Định dạng cho nút bấm chính */
div.stButton > button:first-child {
    background-color: #D32F2F; /* Màu đỏ đậm */
    color: white;
    border-radius: 20px; /* Bo góc rất tròn */
    height: 4em; /* Chiều cao nút */
    width: 90%; /* Chiếm phần lớn chiều rộng */
    display: block; /* Để căn giữa dễ hơn */
    margin: 30px auto; /* Căn giữa theo chiều ngang và khoảng cách */
    font-size: 1.4em; /* Cỡ chữ lớn hơn */
    font-weight: bold;
    border: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.25); /* Đổ bóng mạnh */
    transition: all 0.3s ease-in-out; /* Hiệu ứng chuyển động mượt mà */
    letter-spacing: 0.5px;
}

/* Hiệu ứng khi di chuột qua nút */
div.stButton > button:first-child:hover {
    background-color: #B71C1C; /* Màu đỏ sẫm hơn khi hover */
    box-shadow: 0 6px 12px rgba(0,0,0,0.35); /* Đổ bóng mạnh hơn nữa */
    transform: translateY(-3px); /* Nút nhích lên một chút */
    cursor: pointer; /* Biểu tượng con trỏ khi di chuột */
}

/* Tiêu đề cho phần kết quả */
.results-header {
    font-size: 1.8em;
    font-weight: bold;
    color: #00695C; /* Màu xanh lá đậm */
    margin-top: 40px;
    border-bottom: 3px solid #AED581; /* Đường gạch chân màu xanh lá nhạt */
    padding-bottom: 10px;
    text-align: center;
    text-transform: uppercase; /* Chữ hoa */
    letter-spacing: 1px;
}

/* Container cho mỗi nhóm kết quả (voucher + món ăn) */
.result-group {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 15px;
    border: 1px solid #e0e0e0;
    box-shadow: 1px 1px 5px rgba(0,0,0,.08);
}

.result-group-title {
    font-weight: bold;
    color: #424242; /* Màu xám đậm */
    margin-bottom: 8px;
    font-size: 1.1em;
}

.result-item {
    color: #616161; /* Màu xám */
    margin-left: 20px;
    font-size: 0.95em;
    line-height: 1.5; /* Khoảng cách dòng */
}

/* Tổng chi phí sau giảm giá */
.final-cost {
    font-size: 1.6em;
    font-weight: bold;
    color: #2E7D32; /* Màu xanh lá cây đậm */
    margin-top: 30px;
    text-align: center;
    padding: 15px;
    background-color: #E8F5E9; /* Nền xanh lá nhạt */
    border-radius: 12px;
    border: 1px solid #A5D6A7;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.discount-amount {
    color: #D32F2F; /* Màu đỏ cho số tiền giảm */
    font-weight: normal; /* Không in đậm quá mức */
    font-size: 0.9em;
    margin-left: 10px;
}

/* Thông báo cảnh báo */
div.stWarning {
    background-color: #fffde7;
    color: #FFB300;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #FFD54F;
    font-weight: bold;
    margin-bottom: 15px;
}

/* Thông báo thành công */
div.stSuccess {
    background-color: #e8f5e9;
    color: #388e3c;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #81c784;
    font-weight: bold;
    margin-bottom: 15px;
}
</style>
    """,
    unsafe_allow_html=True,
)

# --- Xử lý dữ liệu đầu vào ---
# Sử dụng cache để tránh parse lại dữ liệu nếu input không đổi
@st.cache_data
def parse_items(text):
    lines = text.strip().split("\n")
    items = []
    for i, line in enumerate(lines):
        if "," in line:
            name, price_str = line.rsplit(",", 1)
            try:
                price = int(price_str.strip())
                items.append({"id": i, "name": name.strip(), "price": price})
            except ValueError:
                st.warning(f"❗ Lỗi định dạng giá ở dòng: '{line}'. Vui lòng nhập số nguyên.")
                return [] # Trả về rỗng để báo hiệu lỗi
        elif line.strip(): # Nếu có dòng không chứa dấu phẩy nhưng không rỗng
            st.warning(f"❗ Định dạng không đúng ở dòng: '{line}'. Vui lòng nhập theo dạng 'tên, giá'.")
            return [] # Trả về rỗng để báo hiệu lỗi
    return items

@st.cache_data
def parse_vouchers(text):
    lines = text.strip().split("\n")
    vouchers = []
    for i, line in enumerate(lines):
        if "," in line:
            try:
                min_total, discount = map(int, line.strip().split(","))
                vouchers.append({
                    "id": i,
                    "min_total": min_total,
                    "discount": discount,
                    "label": f"🎁 ({min_total}k -{discount}k)"
                })
            except ValueError:
                st.warning(f"❗ Lỗi định dạng voucher ở dòng: '{line}'. Vui lòng nhập theo dạng 'min_total,discount'.")
                return [] # Trả về rỗng để báo hiệu lỗi
        elif line.strip():
            st.warning(f"❗ Định dạng không đúng ở dòng: '{line}'. Vui lòng nhập theo dạng 'min_total,discount'.")
            return [] # Trả về rỗng để báo hiệu lỗi
    return vouchers

# --- Thuật toán tìm kiếm tối ưu toàn cục ---
@st.cache_data(show_spinner="Đang tìm kiếm giải pháp tối ưu nhất...")
def find_optimal_voucher_distribution(items, vouchers):
    """
    Tìm cách phân bổ món ăn vào các voucher để tổng chi phí là thấp nhất.
    Sử dụng thuật toán backtracking để thử mọi cách kết hợp.
    """
    
    best_overall_cost = float('inf')
    best_overall_solution = []

    # Tạo một danh sách các index của món ăn để dễ dàng thao tác
    item_indices = list(range(len(items)))
    
    # Chuyển danh sách voucher thành dictionary để truy cập theo ID nhanh hơn
    # (Vì trong quá trình đệ quy, current_voucher_index sẽ dùng để truy cập voucher)
    vouchers_dict = {v["id"]: v for v in vouchers}


    # Hàm đệ quy để thử mọi cách phân chia món ăn cho các voucher
    # remaining_item_indices: tuple các chỉ số món ăn còn lại (dùng tuple để hashable cho cache nếu cần, hoặc để giữ nguyên thứ tự)
    # current_voucher_index: chỉ số voucher đang xét
    # current_groups_info: danh sách các nhóm món ăn đã được gán cho voucher
    def find_best_combination_recursive(remaining_item_indices_tuple, current_voucher_index, current_groups_info):
        nonlocal best_overall_cost, best_overall_solution

        # Nếu đã xét hết tất cả các voucher
        if current_voucher_index == len(vouchers):
            remaining_cost = sum(items[i]["price"] for i in remaining_item_indices_tuple)
            final_cost = sum(g["final"] for g in current_groups_info) + remaining_cost
            
            # Tạo một bản sao của solution để lưu trữ
            current_solution_snapshot = list(current_groups_info)
            # Nếu có các món còn lại, thêm vào nhóm "không voucher"
            if remaining_item_indices_tuple:
                remaining_items_details = [items[i] for i in remaining_item_indices_tuple]
                current_solution_snapshot.append({
                    "voucher": None,
                    "items": remaining_items_details,
                    "total": remaining_cost,
                    "final": remaining_cost
                })

            if final_cost < best_overall_cost:
                best_overall_cost = final_cost
                best_overall_solution = current_solution_snapshot
            
            return

        current_voucher = vouchers_dict.get(current_voucher_index)
        if not current_voucher: # Nếu không tìm thấy voucher với index này (ví dụ, list vouchers rỗng)
            find_best_combination_recursive(remaining_item_indices_tuple, current_voucher_index + 1, list(current_groups_info))
            return


        # Option 1: Không sử dụng voucher hiện tại cho bất kỳ món nào
        # Chuyển sang voucher tiếp theo
        find_best_combination_recursive(remaining_item_indices_tuple, current_voucher_index + 1, list(current_groups_info))


        # Option 2: Sử dụng voucher hiện tại cho một tập hợp các món ăn
        # Duyệt qua tất cả các tổ hợp con của các món ăn còn lại cho voucher hiện tại
        for r in range(1, len(remaining_item_indices_tuple) + 1):
            for combo_indices in combinations(remaining_item_indices_tuple, r):
                selected_items_for_voucher = [items[i] for i in combo_indices]
                group_total = sum(item["price"] for item in selected_items_for_voucher)

                if group_total >= current_voucher["min_total"]:
                    discounted_group_cost = group_total - current_voucher["discount"]
                    
                    # Tạo trạng thái mới
                    new_remaining_item_indices = tuple(sorted([i for i in remaining_item_indices_tuple if i not in combo_indices]))
                    new_groups_info = list(current_groups_info)
                    new_groups_info.append({
                        "voucher": current_voucher,
                        "items": selected_items_for_voucher,
                        "total": group_total,
                        "final": discounted_group_cost
                    })

                    # Tiếp tục đệ quy với các món còn lại và voucher tiếp theo
                    find_best_combination_recursive(new_remaining_item_indices, current_voucher_index + 1, new_groups_info)

    # Bắt đầu tìm kiếm với tất cả các món và voucher đầu tiên
    # Chuyển remaining_item_indices thành tuple để đảm bảo hashable nếu cần cho cache và tránh thay đổi trong đệ quy
    find_best_combination_recursive(tuple(sorted(item_indices)), 0, [])

    # Tổng kết chi phí gốc
    original_total = sum(item["price"] for item in items)
    
    # Sắp xếp lại giải pháp theo thứ tự các nhóm đã được áp dụng hoặc không có voucher
    final_solution_groups = []
    
    # Thêm các nhóm có voucher trước
    for group in best_overall_solution:
        if group["voucher"]:
            final_solution_groups.append(group)
    
    # Thêm nhóm không có voucher (nếu có)
    # Cần kiểm tra lại để đảm bảo không bị trùng lặp hoặc thiếu sót món
    # Cách đơn giản hơn: nếu best_overall_solution đã bao gồm nhóm không voucher, thì dùng nó
    # nếu không thì tự tạo
    
    # Find the unassigned items from the best_overall_solution
    assigned_item_ids_in_solution = set()
    for group in best_overall_solution:
        for item in group["items"]:
            assigned_item_ids_in_solution.add(item["id"])
    
    remaining_unassigned_items_at_end = [item for item in items if item["id"] not in assigned_item_ids_in_solution]

    if remaining_unassigned_items_at_end:
        final_solution_groups.append({
            "voucher": None,
            "items": remaining_unassigned_items_at_end,
            "total": sum(item["price"] for item in remaining_unassigned_items_at_end),
            "final": sum(item["price"] for item in remaining_unassigned_items_at_end)
        })
    
    # Sắp xếp lại các nhóm để nhóm có voucher hiển thị trước, theo thứ tự giảm giá
    final_solution_groups.sort(key=lambda g: (0 if g["voucher"] else 1, -g["voucher"]["discount"] if g["voucher"] else 0))


    return final_solution_groups, best_overall_cost

# --- Giao diện và Hiển thị kết quả ---
# Đặt nội dung chính trong một container để dễ dàng áp dụng CSS .main-container
with st.container(border=False): # Bỏ border mặc định của Streamlit container
    st.markdown('<div class="main-container">', unsafe_allow_html=True) # Mở div main-container

    # Phần tiêu đề của ứng dụng
    st.markdown('<div class="header-bg"><h1 class="header-title">Tiết Kiệm Highland</h1><h2 class="header-subtitle" style="color: white;">Cùng Voucher</h2></div>', unsafe_allow_html=True)

    # Phần nhập danh sách món
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-header"><span class="input-header-icon">☕</span><span class="input-header-text">Nhập danh sách món</span></div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #777; margin-top: 0;">Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)</p>', unsafe_allow_html=True)
    items_input = st.text_area("items_input_area", height=150, label_visibility="collapsed", value="cf sữa m, 39\ntrà sen, 45\nbh kem cheese, 65\nbh kem cheese, 65\nphô mai kem, 69")
    st.markdown('</div>', unsafe_allow_html=True) # Đóng div input-container

    # Phần nhập danh sách voucher
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-header"><span class="input-header-icon">🎁</span><span class="input-header-text">Nhập danh sách voucher</span></div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #777; margin-top: 0;">Nhập mỗi voucher theo dạng: min_price, discount</p>', unsafe_allow_html=True)
    voucher_input = st.text_area("voucher_input_area", value="135,30\n135,30\n169,40", height=100, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True) # Đóng div input-container

    # Nút tính toán
    if st.button("Tính kết quả tối ưu"):
        items = parse_items(items_input)
        vouchers = parse_vouchers(voucher_input)

        if items and vouchers:
            result_groups, final_cost = find_optimal_voucher_distribution(items, vouchers)

            st.markdown('<h2 class="results-header">📄 KẾT QUẢ TỐI ƯU</h2>', unsafe_allow_html=True)
            
            original_total = sum(item["price"] for item in items)
            total_discount = original_total - final_cost
            
            for idx, group in enumerate(result_groups, 1):
                st.markdown('<div class="result-group">', unsafe_allow_html=True)
                if group["voucher"]:
                    st.markdown(f'<p class="result-group-title">Nhóm {idx}: {group["voucher"]["label"]} (Tổng: {group["total"]}k → {group["final"]}k)</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="result-group-title">Nhóm {idx}: Không dùng voucher (Tổng: {group["total"]}k)</p>', unsafe_allow_html=True)
                
                for item in group["items"]:
                    st.markdown(f'<p class="result-item">- {item["name"]} ({item["price"]}k)</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True) # Đóng div result-group
            
            st.markdown(f'<p class="final-cost">Tổng chi phí sau giảm giá: <strong>{final_cost}k</strong> <span class="discount-amount">(giảm được {total_discount}k)</span></p>', unsafe_allow_html=True)
        elif not items:
            st.warning("❗ Vui lòng nhập ít nhất 1 món.")
        elif not vouchers:
            st.warning("❗ Vui lòng nhập ít nhất 1 voucher.")
        else:
             st.warning("❗ Vui lòng nhập đủ thông tin món và voucher hợp lệ.")
    
    st.markdown('</div>', unsafe_allow_html=True) # Đóng div main-container

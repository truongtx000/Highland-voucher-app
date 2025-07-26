import streamlit as st
from itertools import combinations
import math

# Cấu hình trang của Streamlit
st.set_page_config(page_title="Tiết Kiệm Highland Cùng Voucher", layout="centered")

# --- CSS Tùy Chỉnh để tạo giao diện chính xác như hình bạn cung cấp ---
st.markdown(
    """
<style>
/* Import font Roboto Condensed từ Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap');

/* Đặt màu nền chung cho toàn bộ trang */
body {
    background-color: #FFFDF1; /* Màu vàng nhạt / trắng kem */
    font-family: 'Roboto Condensed', sans-serif; /* Font Roboto Condensed */
}

/* Ẩn Streamlit header và footer mặc định */
header { visibility: hidden; }
footer { visibility: hidden; }

/* Container chính của Streamlit, điều chỉnh padding để nội dung sát hơn */
.stApp {
    background-color: #FFFDF1; /* Đảm bảo nền app trùng với body */
}

/* Vùng chứa nội dung chính để bo góc và đổ bóng cho toàn bộ app */
.block-container {
    padding-top: 0rem; /* Giảm padding trên cùng của Streamlit */
    padding-bottom: 0rem; /* Giảm padding dưới cùng */
    padding-left: 0rem; /* Giảm padding trái */
    padding-right: 0rem; /* Giảm padding phải */
    max-width: 700px; /* Giới hạn chiều rộng để giống ảnh */
    margin: 0 auto; /* Căn giữa block container */
}

/* Loại bỏ các box container mặc định của Streamlit nếu chúng được sử dụng */
div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Phần tiêu đề ứng dụng (Highland Voucher App) */
.header-bg {
    background-color: #A02B2B; /* Màu đỏ đậm của Highland */
    color: white;
    padding: 30px 20px 20px 20px; /* Đệm trên dưới, không đệm ngang */
    border-radius: 0px; /* Bỏ bo góc */
    text-align: center;
    margin-bottom: 30px; /* Khoảng cách với phần tiếp theo */
    box-shadow: 0 4px 10px rgba(0,0,0,0.2); /* Đổ bóng mạnh hơn cho header */
    box-sizing: border-box; /* Bao gồm padding và border trong kích thước */
}

.header-title {
    font-size: 2.5em; /* Kích thước chữ lớn */
    font-weight: 900; /* Rất đậm */
    margin-bottom: 5px;
    letter-spacing: 0.5px; /* Khoảng cách giữa các chữ cái */
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2); /* Đổ bóng chữ */
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
}

/* Tiêu đề phụ trong header */
.header-subtitle {
    font-size: 1.8em;
    font-weight: 600;
    margin-top: 0;
    opacity: 0.9; /* Hơi mờ hơn tiêu đề chính */
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
}

/* Container cho mỗi phần nhập liệu (Món ăn, Voucher) */
.input-section {
    display: flex; /* Dùng flexbox để căn chỉnh icon và nội dung */
    align-items: flex-start; /* Căn chỉnh theo đầu của các phần tử */
    margin-bottom: 25px; /* Khoảng cách giữa các section */
    padding: 0 20px; /* Padding ngang để nội dung không sát lề */
    box-sizing: border-box;
}

/* Icon lớn trong hình tròn */
.icon-circle {
    background-color: #F8D882; /* Màu vàng của hình tròn */
    border-radius: 50%; /* Hình tròn hoàn hảo */
    width: 70px; /* Kích thước hình tròn */
    height: 70px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 15px; /* Khoảng cách giữa hình tròn và text */
    flex-shrink: 0; /* Không cho hình tròn bị co lại */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Đổ bóng nhẹ */
}

.icon-circle img { /* Định dạng ảnh bên trong hình tròn */
    width: 60%; /* Kích thước ảnh so với hình tròn */
    height: 60%;
    object-fit: contain; /* Đảm bảo ảnh vừa vặn */
    vertical-align: middle; /* Căn giữa ảnh trong thẻ img */
}

/* Nội dung text và textbox của phần nhập liệu (tiêu đề và mô tả) */
.input-content {
    flex-grow: 1; /* Cho phép nội dung này mở rộng */
    /* Không đặt width cứng ở đây để flexbox tự điều chỉnh */
}

.input-content h2 {
    font-size: 1.4em; /* Kích thước chữ tiêu đề */
    font-weight: bold;
    color: #333;
    margin-top: 0px; /* Đảm bảo sát với icon - Đã chỉnh */
    margin-bottom: 5px;
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
    line-height: 1.2; /* Tăng line-height cho tiêu đề */
}

.input-content p {
    font-size: 0.9em; /* Kích thước chữ mô tả */
    color: #777;
    margin-bottom: 10px;
    line-height: 1.4;
}

/* Định dạng cho vùng nhập liệu (text area) */
.stTextArea textarea {
    border-radius: 8px; /* Bo góc nhẹ */
    border: 2px solid #C29A5F; /* Viền màu nâu đậm */
    padding: 12px;
    box-shadow: none; /* Bỏ đổ bóng bên trong */
    width: calc(100% - 70px); /* THAY ĐỔI: Giảm chiều rộng để có khoảng trống bên trái (cộng thêm 70px của icon-circle + margin-right) */
    margin-left: 70px; /* THAY ĐỔI: Đẩy textbox sang phải bằng chiều rộng của icon + margin */
    box-sizing: border-box; /* Tính cả padding và border vào width */
    font-size: 1.1em;
    min-height: 150px; /* THAY ĐỔI: Chiều cao tối thiểu, tăng lên */
    background-color: white; /* Nền trắng cho textbox */
}

/* Đảm bảo phần màu xám bên trái textbox biến mất/trùng màu nền */
/* Đây là class được Streamlit tạo cho div bọc quanh textarea */
div[data-testid="stTextArea"].st-emotion-cache-1oy39z6 > div:first-child {
    background-color: #FFFDF1; /* Đặt màu nền trùng với body */
    padding: 0 !important; /* Xóa padding nếu có */
    border: none !important; /* Xóa border */
    box-shadow: none !important; /* Xóa đổ bóng */
}


/* Cho text area của voucher nhỏ lại một chút (nếu cần) */
/* Cần điều chỉnh selector chính xác nếu muốn áp dụng riêng cho voucher text area.
   Hiện tại, nó áp dụng cho tất cả st.text_area.
   Nếu bạn muốn chỉ thay đổi cho voucher, cần tìm ra cách chọn riêng nó.
   Ví dụ, có thể dùng st.text_area(key="voucher_input_area_key", ...) rồi dùng CSS selector dựa vào key đó
   nhưng Streamlit không tạo ra ID/class dễ dàng từ key.
   Cách khác là dùng :nth-of-type hoặc điều chỉnh height trực tiếp trong Python.
*/
/*
div[data-testid="stVerticalBlock"] > div.st-emotion-cache-1oy39z6:nth-of-type(2) textarea {
    min-height: 90px;
}
*/
/* Điều chỉnh height của text area voucher trực tiếp trong st.text_area(...) */


/* Định dạng cho nút bấm chính */
div.stButton > button:first-child {
    background-color: #A02B2B; /* Màu đỏ đậm */
    color: white;
    border-radius: 12px; /* Bo góc */
    height: 3.5em; /* Chiều cao nút */
    width: calc(100% - 40px); /* Chiếm phần lớn chiều rộng, trừ padding */
    display: block; /* Để căn giữa dễ hơn */
    margin: 30px auto 20px auto; /* Căn giữa theo chiều ngang và khoảng cách */
    font-size: 1.3em; /* Cỡ chữ lớn hơn */
    font-weight: bold;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25); /* Đổ bóng mạnh */
    transition: all 0.3s ease-in-out; /* Hiệu ứng chuyển động mượt mà */
    letter-spacing: 0.5px;
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
}

/* Hiệu ứng khi di chuột qua nút */
div.stButton > button:first-child:hover {
    background-color: #8D2525; /* Màu đỏ sẫm hơn khi hover */
    box-shadow: 0 6px 15px rgba(0,0,0,0.35); /* Đổ bóng mạnh hơn nữa */
    transform: translateY(-2px); /* Nút nhích lên một chút */
    cursor: pointer; /* Biểu tượng con trỏ khi di chuột */
}

/* Tiêu đề cho phần kết quả */
.results-header {
    font-size: 1.8em;
    font-weight: bold;
    color: #333; /* Màu chữ đen */
    margin-top: 40px;
    border-bottom: 2px solid #C29A5F; /* Đường gạch chân màu nâu */
    padding-bottom: 10px;
    text-align: center;
    text-transform: uppercase; /* Chữ hoa */
    letter-spacing: 1px;
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
}

/* Container cho mỗi nhóm kết quả (voucher + món ăn) */
.result-group {
    background-color: white;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 12px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

.result-group-title {
    font-weight: bold;
    color: #424242; /* Màu xám đậm */
    margin-bottom: 5px;
    font-size: 1.05em;
}

.result-item {
    color: #616161; /* Màu xám */
    margin-left: 15px;
    font-size: 0.9em;
    line-height: 1.4; /* Khoảng cách dòng */
}

/* Tổng chi phí sau giảm giá */
.final-cost {
    font-size: 1.5em;
    font-weight: bold;
    color: #1B5E20; /* Màu xanh lá cây đậm */
    margin-top: 30px;
    text-align: center;
    padding: 15px;
    background-color: #E8F5E9; /* Nền xanh lá nhạt */
    border-radius: 10px;
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

/* Ẩn các label mặc định của Streamlit cho text area */
.stTextArea label {
    display: none;
}

/* Điều chỉnh lại layout của Streamlit widget để phù hợp với flexbox của input-section */
/* Đây là class được Streamlit tự động tạo cho div chứa text area, bạn có thể cần kiểm tra lại bằng F12 */
/* Selector này cố gắng nhắm vào div bên trong st.markdown, chứa text area */
div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] div.st-emotion-cache-1oy39z6 > div:first-child > div:nth-child(1) {
    background-color: transparent !important; /* Làm cho nó trong suốt */
    border: none !important; /* Xóa border */
    box-shadow: none !important; /* Xóa đổ bóng */
    padding: 0 !important; /* Xóa padding */
    margin: 0 !important; /* Xóa margin */
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
            # Tiếp tục với voucher tiếp theo mà không sử dụng voucher hiện tại
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
    # (Đảm bảo nhóm không voucher luôn ở cuối)
    final_solution_groups.sort(key=lambda g: (0 if g["voucher"] else 1, -g["voucher"]["discount"] if g["voucher"] else 0))


    return final_solution_groups, best_overall_cost

# --- Giao diện và Hiển thị kết quả ---
# Đặt nội dung chính trong một container để dễ dàng áp dụng CSS .main-container
# Sử dụng st.container không border để tự tạo div.main-container bên trong
with st.container(border=False):
    st.markdown('<div class="main-container">', unsafe_allow_html=True) # Mở div main-container

    # Phần tiêu đề của ứng dụng
    st.markdown('<div class="header-bg"><h1 class="header-title">Tiết Kiệm Highland</h1><h2 class="header-subtitle">Cùng Voucher</h2></div>', unsafe_allow_html=True)

    # Đường dẫn tới ảnh trên GitHub (thay thế bằng repo của bạn nếu khác)
    # Dựa trên ảnh bạn cung cấp, đây là đường dẫn raw mặc định cho repo của bạn
    GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/truongb000/Highland-voucher-app/main/images/"
    COFFEE_ICON_URL = GITHUB_RAW_BASE_URL + "coffee.png"
    VOUCHER_ICON_URL = GITHUB_RAW_BASE_URL + "voucher.png"

    # Phần nhập danh sách món
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown(f'<div class="icon-circle"><img src="{COFFEE_ICON_URL}" alt="Coffee Icon"></div>', unsafe_allow_html=True)
    st.markdown('<div class="input-content">', unsafe_allow_html=True)
    st.markdown('<h2>Nhập danh sách món</h2>', unsafe_allow_html=True)
    st.markdown('<p>Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)</p>', unsafe_allow_html=True)
    items_input = st.text_area("items_input_area", height=150, label_visibility="collapsed", value="cf sữa m, 39\ntrà sen, 45\nbh kem cheese, 65\nbh kem cheese, 65\nphô mai kem, 69")
    st.markdown('</div></div>', unsafe_allow_html=True) # Đóng div input-content và input-section

    # Phần nhập danh sách voucher
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown(f'<div class="icon-circle"><img src="{VOUCHER_ICON_URL}" alt="Voucher Icon"></div>', unsafe_allow_html=True)
    st.markdown('<div class="input-content">', unsafe_allow_html=True)
    st.markdown('<h2>Nhập danh sách voucher</h2>', unsafe_allow_html=True)
    st.markdown('<p>Nhập mỗi voucher theo dạng: min_price, discount</p>', unsafe_allow_html=True)
    voucher_input = st.text_area("voucher_input_area", value="135,30\n135,30\n169,40", height=100, label_visibility="collapsed")
    st.markdown('</div></div>', unsafe_allow_html=True) # Đóng div input-content và input-section

    # Nút tính toán
    if st.button("Tính kết quả tối ưu"):
        items = parse_items(items_input)
        vouchers = parse_vouchers(voucher_input)

        # Chỉ tiếp tục nếu parsing không có lỗi và có dữ liệu
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
        elif not items and not voucher_input.strip(): # Trường hợp cả 2 input đều rỗng
             st.warning("❗ Vui lòng nhập thông tin món và voucher để bắt đầu.")
        elif not items: # Chỉ món rỗng
            st.warning("❗ Vui lòng nhập ít nhất 1 món.")
        elif not vouchers: # Chỉ voucher rỗng
            st.warning("❗ Vui lòng nhập ít nhất 1 voucher.")

    st.markdown('</div>', unsafe_allow_html=True) # Đóng div main-container

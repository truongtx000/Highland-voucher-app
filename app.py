import streamlit as st
from itertools import combinations

# Cấu hình giao diện
st.set_page_config(page_title="Highland Voucher App", layout="centered")

# --- CSS tùy chỉnh ---
st.markdown("""
    <style>
        /* Đổi màu nền toàn bộ trang */
        html, body, .stApp {
            background-color: #FFFDF1 !important;
        }

        /* Layout hàng ngang cho phần nhập */
        .flex-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            background-color: #FFFDF1;
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
        }

        .flex-row img {
            width: 100px;  /* Tăng kích thước hình */
            height: 100px;
        }

        .flex-content h2 {
            margin: 0;
            font-size: 1.5rem;
            line-height: 1;  /* Giảm khoảng cách giữa tiêu đề và mô tả */
        }

        .flex-content p {
            margin: 0;
            color: #555;
            font-size: 0.95rem;
            line-height: 1.3;
        }

        /* Style cho textarea */
        textarea {
            background-color: white !important;
            border: 2px solid #C29A5F !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Tiêu đề ---
st.markdown("""
<div class="title-container">
    <h2>Tiết Kiệm Highland<br>Cùng Voucher</h2>
</div>
""", unsafe_allow_html=True)

# --- Khối nhập liệu ---
st.markdown("""
    <style>
        .flex-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            background-color: #FFFCF3;
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
        }
        .flex-row img {
            width: 48px;
            height: 48px;
        }
        .flex-content h2 {
            margin: 0;
            font-size: 1.5rem;
        }
        .flex-content p {
            margin: 0;
            color: #555;
        }
        .no-label textarea {
            background-color: white !important;
            border: 2px solid #d1a465;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# 🧋 Nhập danh sách món
st.markdown("""
    <div class="flex-row">
        <img src="https://raw.githubusercontent.com/truongtx000/Highland-voucher-app/refs/heads/main/images/coffee.png" alt="coffee icon">
        <div class="flex-content">
            <h2>Nhập danh sách món</h2>
            <p>Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)</p>
        </div>
    </div>
""", unsafe_allow_html=True)

items_input = st.text_area(
    label="",
    height=150,
    label_visibility="collapsed",
    key="items_input_area"
)


# 🎟️ Nhập danh sách voucher
st.markdown("""
    <div class="flex-row">
        <img src="https://raw.githubusercontent.com/truongtx000/Highland-voucher-app/refs/heads/main/images/voucher.png" alt="voucher icon">
        <div class="flex-content">
            <h2>Nhập danh sách voucher</h2>
            <p>Nhập mỗi dòng: [giá tối thiểu] [số tiền giảm] (vd: 169 40)</p>
        </div>
    </div>
""", unsafe_allow_html=True)

voucher_input = st.text_area(
    label="",
    height=100,
    label_visibility="collapsed",
    key="voucher_input_area"
)


# --- Parse dữ liệu ---
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
        elif line.strip():
            st.warning(f"❗ Định dạng không đúng ở dòng: '{line}'. Vui lòng nhập theo dạng 'tên, giá'.")
    return items

def parse_vouchers(text):
    lines = text.strip().split("\n")
    vouchers = []
    for i, line in enumerate(lines):
        if "," in line:
            try:
                min_total, discount = map(int, line.strip().split(","))
                vouchers.append({"id": i, "min_total": min_total, "discount": discount,
                                 "label": f"🎁 ({min_total}k -{discount}k)"})
            except ValueError:
                st.warning(f"❗ Lỗi định dạng voucher ở dòng: '{line}'. Vui lòng nhập theo dạng 'min_total,discount'.")
        elif line.strip():
            st.warning(f"❗ Định dạng không đúng ở dòng: '{line}'. Vui lòng nhập theo dạng 'min_total,discount'.")
    return vouchers

# --- Tối ưu ---
def find_optimal_voucher_distribution(items, vouchers):
    best_total_cost = float('inf')
    best_solution_details = []

    item_indices = list(range(len(items)))

    def recurse(remaining_indices, voucher_index, current_groups):
        nonlocal best_total_cost, best_solution_details

        if voucher_index == len(vouchers):
            leftover_cost = sum(items[i]['price'] for i in remaining_indices)
            total = sum(g['final'] for g in current_groups) + leftover_cost
            if total < best_total_cost:
                best_total_cost = total
                result = current_groups[:]
                if remaining_indices:
                    result.append({
                        "voucher": None,
                        "items": [items[i] for i in remaining_indices],
                        "total": leftover_cost,
                        "final": leftover_cost
                    })
                best_solution_details = result
            return

        recurse(remaining_indices, voucher_index + 1, current_groups[:])

        current_voucher = vouchers[voucher_index]
        for r in range(1, len(remaining_indices)+1):
            for combo in combinations(remaining_indices, r):
                selected_items = [items[i] for i in combo]
                group_total = sum(i['price'] for i in selected_items)
                if group_total >= current_voucher['min_total']:
                    next_remaining = [i for i in remaining_indices if i not in combo]
                    new_group = current_groups + [{
                        "voucher": current_voucher,
                        "items": selected_items,
                        "total": group_total,
                        "final": group_total - current_voucher['discount']
                    }]
                    recurse(next_remaining, voucher_index + 1, new_group)

    recurse(item_indices, 0, [])
    return best_solution_details, best_total_cost

# --- Xử lý khi nhấn nút ---
st.markdown("<div class='submit-button'>", unsafe_allow_html=True)
if st.button("Tính kết quả tối ưu"):
    items = parse_items(items_input)
    vouchers = parse_vouchers(voucher_input)

    if not items:
        st.warning("❗ Vui lòng nhập ít nhất 1 món.")
    elif not vouchers:
        st.warning("❗ Vui lòng nhập ít nhất 1 voucher.")
    else:
        results, total_cost = find_optimal_voucher_distribution(items, vouchers)

        st.subheader("📄 KẾT QUẢ TỐI ƯU")
        for idx, group in enumerate(results, 1):
            if group['voucher']:
                st.markdown(f"**Nhóm {idx}** {group['voucher']['label']} _(Tổng: {group['total']}k → {group['final']}k)_")
            else:
                st.markdown(f"**Nhóm {idx}** _(Không dùng voucher)_ _(Tổng: {group['total']}k)_")
            for item in group['items']:
                st.markdown(f"- {item['name']} ({item['price']}k)")

        original_total = sum(i['price'] for i in items)
        st.success(f"✅ Tổng chi phí sau giảm giá: **{total_cost}k** (giảm được **{original_total - total_cost}k**) ")

st.markdown("</div>", unsafe_allow_html=True)

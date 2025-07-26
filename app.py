import streamlit as st
from itertools import combinations

# Cấu hình giao diện
st.set_page_config(page_title="Highland Voucher App", layout="centered")

# --- CSS tùy chỉnh ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Roboto Condensed', sans-serif;
            background-color: #FFFDF1;
        }

        .main > div {
            padding: 0 !important;
        }

        .title-container {
            background-color: #AA1F24;
            color: white;
            text-align: center;
            padding: 2rem 1rem 1rem;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }

        .block-container {
            padding-top: 0 !important;
        }

        .input-card {
            background-color: #fff;
            padding: 1rem;
            border-radius: 0 0 8px 8px;
        }

        .submit-button button {
            background-color: #AA1F24 !important;
            color: white !important;
            font-weight: bold;
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
st.markdown("<div class='input-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""<h4>🛍️ Nhập danh sách món</h4>
<p>Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)</p>""", unsafe_allow_html=True)
    items_input = st.text_area("", height=150, label_visibility="collapsed")

with col2:
    st.markdown("""<h4>🎁 Nhập danh sách voucher</h4>
<p>Nhập mỗi voucher theo dạng: min_price, discount</p>""", unsafe_allow_html=True)
    voucher_input = st.text_area("", height=150, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

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

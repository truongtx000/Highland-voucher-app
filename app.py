import streamlit as st
from itertools import combinations
import math

st.set_page_config(page_title="Highland Voucher App", layout="centered")
st.markdown("""
    <style>
        .custom-button {
            background-color: #d62828;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .custom-button:hover {
            background-color: #a61c1c;
        }

        .title {
            text-align: center;
            font-size: 36px;
            margin-top: 20px;
            color: #2c3e50;
        }

        .section-header {
            font-size: 24px;
            margin-top: 40px;
            color: #1a1a1a;
        }

        .stTextArea label, .stButton button {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧾 Highland Voucher App</div>', unsafe_allow_html=True)

# --- UI: Nhập món ---
st.markdown('<div class="section-header">📋 Nhập danh sách món</div>', unsafe_allow_html=True)
items_input = st.text_area("Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)", height=200, value="cf sữa m, 39\ntrà sen, 45\nbh kem cheese, 65\nbh kem cheese, 65\nphô mai kem, 69\n")

# --- UI: Nhập voucher ---
st.markdown('<div class="section-header">🎁 Nhập danh sách voucher</div>', unsafe_allow_html=True)
voucher_input = st.text_area("Nhập mỗi voucher theo dạng: min_price, discount", value="135,30\n135,30\n169,40")

# --- Parse dữ liệu ---
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
                st.warning(f"❗ Lỗi định dạng giá ở dòng: '{line}'")
        elif line.strip():
            st.warning(f"❗ Định dạng sai ở dòng: '{line}'")
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
                st.warning(f"❗ Lỗi định dạng voucher ở dòng: '{line}'")
        elif line.strip():
            st.warning(f"❗ Định dạng sai ở dòng: '{line}'")
    return vouchers

# --- Tính toán tối ưu ---
@st.cache_data(show_spinner="🔍 Đang tính toán... xin chờ...")
def find_optimal_voucher_distribution(items, vouchers):
    best_total_cost = float('inf')
    best_solution_details = []

    item_indices = list(range(len(items)))

    def recursive(remaining_indices, voucher_idx, groups_info):
        nonlocal best_total_cost, best_solution_details
        if voucher_idx == len(vouchers):
            remaining_cost = sum(items[i]["price"] for i in remaining_indices)
            total_cost = sum(g["final"] for g in groups_info) + remaining_cost

            if remaining_indices:
                remaining_items = [items[i] for i in remaining_indices]
                groups_info.append({
                    "voucher": None,
                    "items": remaining_items,
                    "total": sum(i["price"] for i in remaining_items),
                    "final": sum(i["price"] for i in remaining_items)
                })

            if total_cost < best_total_cost:
                best_total_cost = total_cost
                best_solution_details = list(groups_info)

            if remaining_indices:
                groups_info.pop()
            return

        # Option 1: Bỏ qua voucher này
        recursive(remaining_indices, voucher_idx + 1, list(groups_info))

        # Option 2: Dùng voucher này
        current_voucher = vouchers[voucher_idx]
        for r in range(1, len(remaining_indices) + 1):
            for combo in combinations(remaining_indices, r):
                selected_items = [items[i] for i in combo]
                group_total = sum(item["price"] for item in selected_items)
                if group_total >= current_voucher["min_total"]:
                    discounted = group_total - current_voucher["discount"]
                    new_remaining = [i for i in remaining_indices if i not in combo]
                    new_groups = list(groups_info)
                    new_groups.append({
                        "voucher": current_voucher,
                        "items": selected_items,
                        "total": group_total,
                        "final": discounted
                    })
                    recursive(new_remaining, voucher_idx + 1, new_groups)

    recursive(item_indices, 0, [])

    return best_solution_details, best_total_cost

# --- Button & Kết quả ---
st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <form action="#">
            <button class="custom-button" type="submit">Tính kết quả tối ưu</button>
        </form>
    </div>
""", unsafe_allow_html=True)

if st.button("🚀 Tính kết quả tối ưu"):
    items = parse_items(items_input)
    vouchers = parse_vouchers(voucher_input)

    if not items:
        st.warning("❗ Bạn chưa nhập món.")
    elif not vouchers:
        st.warning("❗ Bạn chưa nhập voucher.")
    else:
        results, final_cost = find_optimal_voucher_distribution(items, vouchers)

        st.subheader("📄 KẾT QUẢ TỐI ƯU")
        for idx, group in enumerate(results, 1):
            if group["voucher"]:
                st.markdown(f"**Nhóm {idx}** {group['voucher']['label']} _(Tổng: {group['total']}k → {group['final']}k)_")
            else:
                st.markdown(f"**Nhóm {idx}** _(Không dùng voucher)_ _(Tổng: {group['total']}k)_")
            st.markdown("\n".join([f"- {item['name']} ({item['price']}k)" for item in group["items"]]))
            st.markdown("")

        original = sum(item["price"] for item in items)
        discount = original - final_cost
        st.success(f"✅ Tổng chi phí sau giảm giá: **{final_cost}k** (giảm được **{discount}k**)")


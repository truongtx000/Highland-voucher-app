# highland_voucher_app.py
import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Highland Voucher App", layout="centered")
st.title("🧾 KẾT QUẢ TỐI ƯU")

# === UI Section ===
st.markdown("""
<style>
    .custom-button {
        background-color: #ff4b4b;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: #ff1a1a;
    }
</style>
""", unsafe_allow_html=True)

st.header("📋 Nhập danh sách món")
items_input = st.text_area(
    "Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)",
    height=200,
    value="cf sữa m, 39\ntrà sen, 45\nbh kem cheese, 65\nbh kem cheese, 65\nphô mai kem, 69\n"
)

st.header("🎁 Nhập danh sách voucher")
voucher_input = st.text_area(
    "Nhập mỗi voucher theo dạng: min_price, discount",
    value="135,30\n135,30\n169,40"
)

# === Parse input ===
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

# === Optimization Logic ===
@st.cache_data(show_spinner="🔍 Đang tính toán tối ưu...")
def find_optimal_voucher_distribution(items, vouchers):
    best_total_cost = float('inf')
    best_solution_details = []
    item_indices = list(range(len(items)))

    def recurse(remaining_item_indices, voucher_idx, current_groups):
        nonlocal best_total_cost, best_solution_details
        if voucher_idx == len(vouchers):
            remaining_cost = sum(items[i]['price'] for i in remaining_item_indices)
            total_cost = sum(g['final'] for g in current_groups) + remaining_cost

            if total_cost < best_total_cost:
                best_total_cost = total_cost
                full_groups = current_groups[:]
                if remaining_item_indices:
                    leftover_items = [items[i] for i in remaining_item_indices]
                    full_groups.append({
                        "voucher": None,
                        "items": leftover_items,
                        "total": sum(i['price'] for i in leftover_items),
                        "final": sum(i['price'] for i in leftover_items)
                    })
                best_solution_details = full_groups
            return

        current_voucher = vouchers[voucher_idx]
        recurse(remaining_item_indices, voucher_idx + 1, current_groups[:])  # skip

        for r in range(1, len(remaining_item_indices)+1):
            for combo in combinations(remaining_item_indices, r):
                selected_items = [items[i] for i in combo]
                total = sum(i['price'] for i in selected_items)
                if total >= current_voucher['min_total']:
                    discounted = total - current_voucher['discount']
                    remaining = [i for i in remaining_item_indices if i not in combo]
                    recurse(remaining, voucher_idx + 1, current_groups + [{
                        "voucher": current_voucher,
                        "items": selected_items,
                        "total": total,
                        "final": discounted
                    }])

    recurse(item_indices, 0, [])
    return best_solution_details, best_total_cost

# === Trigger Button ===
st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <form action="#">
            <button class="custom-button" type="submit">Tính kết quả tối ưu</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# === Execute Optimization ===
if st.button("🚀 Tính kết quả tối ưu"):
    items = parse_items(items_input)
    vouchers = parse_vouchers(voucher_input)

    if not items:
        st.warning("❗ Vui lòng nhập ít nhất 1 món")
    elif not vouchers:
        st.warning("❗ Vui lòng nhập ít nhất 1 voucher")
    else:
        groups, final_cost = find_optimal_voucher_distribution(items, vouchers)

        st.subheader("📄 KẾT QUẢ TỐI ƯU")
        for idx, g in enumerate(groups, 1):
            if g['voucher']:
                st.markdown(f"**Nhóm {idx}** {g['voucher']['label']} _(Tổng: {g['total']}k → {g['final']}k)_")
            else:
                st.markdown(f"**Nhóm {idx}** _(Không dùng voucher)_ _(Tổng: {g['total']}k)_")
            for item in g['items']:
                st.markdown(f"- {item['name']} ({item['price']}k)")
            st.markdown("---")

        original = sum(i['price'] for i in items)
        st.success(f"✅ Tổng chi phí sau giảm giá: **{final_cost}k** (tiết kiệm **{original - final_cost}k**) ")

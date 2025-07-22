import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Highland Voucher App", layout="centered")
st.title("🧾 KẾT QUẢ TỐI ƯU")

# --- Nhập danh sách món ---
st.header("📋 Nhập danh sách món")
items_input = st.text_area("Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)", height=200)

# --- Nhập danh sách voucher ---
st.header("🎁 Nhập danh sách voucher")
voucher_input = st.text_area("Nhập mỗi voucher theo dạng: min_price, discount", value="135,30\n135,30\n169,40")

# --- Xử lý dữ liệu ---
def parse_items(text):
    lines = text.strip().split("\n")
    items = []
    for i, line in enumerate(lines):
        if "," in line:
            name, price = line.rsplit(",", 1)
            items.append({"name": name.strip(), "price": int(price.strip())})
    return items

def parse_vouchers(text):
    lines = text.strip().split("\n")
    vouchers = []
    for line in lines:
        if "," in line:
            min_total, discount = map(int, line.strip().split(","))
            vouchers.append({
                "min_total": min_total,
                "discount": discount,
                "label": f"🎁 ({min_total}k -{discount}k)"
            })
    return vouchers

items = parse_items(items_input)
vouchers = parse_vouchers(voucher_input)

# --- Tìm tổ hợp tối ưu ---
def find_best_group(available_items, min_total):
    best_combo = None
    min_above = float("inf")
    for r in range(1, len(available_items) + 1):
        for combo in combinations(available_items, r):
            total = sum(i["price"] for i in combo)
            if total >= min_total and total < min_above:
                best_combo = combo
                min_above = total
    return best_combo, min_above

def apply_vouchers(items, vouchers):
    remaining_items = items.copy()
    used_groups = []
    total_discounted_cost = 0

    for voucher in sorted(vouchers, key=lambda v: -v["min_total"]):
        group, group_total = find_best_group(remaining_items, voucher["min_total"])
        if group:
            for item in group:
                remaining_items.remove(item)
            used_groups.append({
                "voucher": voucher,
                "items": group,
                "total": group_total,
                "final": group_total - voucher["discount"]
            })
            total_discounted_cost += group_total - voucher["discount"]

    if remaining_items:
        final = sum(i["price"] for i in remaining_items)
        used_groups.append({
            "voucher": None,
            "items": remaining_items,
            "total": final,
            "final": final
        })
        total_discounted_cost += final

    return used_groups, total_discounted_cost

# --- Hiển thị kết quả ---
if st.button("🚀 Tính kết quả tối ưu"):
    if not items:
        st.warning("❗ Vui lòng nhập ít nhất 1 món.")
    elif not vouchers:
        st.warning("❗ Vui lòng nhập ít nhất 1 voucher.")
    else:
        result_groups, final_cost = apply_vouchers(items, vouchers)

        st.subheader("📄 KẾT QUẢ TỐI ƯU")
        for idx, group in enumerate(result_groups, 1):
            if group["voucher"]:
                st.markdown(f"**Nhóm {idx}** {group['voucher']['label']} _(Tổng: {group['total']}k → {group['final']}k)_")
            else:
                st.markdown(f"**Nhóm {idx}** _(Không dùng voucher)_ _(Tổng: {group['total']}k)_")
            st.markdown("\n".join([f"- {item['name']} ({item['price']}k)" for item in group["items"]]))
            st.markdown("")

        original_total = sum(item["price"] for item in items)
        total_discount = original_total - final_cost
        st.success(f"✅ Tổng chi phí sau giảm giá: **{final_cost}k** (giảm được **{total_discount}k**)")
        

import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Tính voucher tối ưu", layout="centered")

st.title("🧮 Tính chia nhóm món để dùng Voucher tối ưu")

st.markdown("### ✅ Nhập danh sách món")
raw_items = st.text_area(
    "Mỗi dòng 1 món, định dạng: `tên món,giá` (vd: trà sữa,45)",
    height=200,
    placeholder="phin sữa đá,39\ntrà đào,55\ncf sữa m,48"
)

st.markdown("### 🎟️ Nhập thông tin voucher")
col1, col2 = st.columns(2)
with col1:
    voucher_min = st.number_input("Tổng tiền tối thiểu để dùng voucher (vd 135k)", value=135, step=1)
with col2:
    voucher_discount = st.number_input("Số tiền được giảm khi dùng voucher (vd 35k)", value=35, step=1)

if st.button("🚀 Tính toán"):
    # Parse danh sách món
    items = []
    for line in raw_items.strip().split("\n"):
        try:
            name, price = line.strip().rsplit(",", 1)
            items.append((name.strip(), int(price.strip())))
        except:
            st.error(f"❌ Dòng không hợp lệ: `{line}`. Đảm bảo có dấu phẩy ngăn cách.")
            st.stop()

    if len(items) < 2:
        st.warning("⚠️ Cần ít nhất 2 món để chia nhóm.")
        st.stop()

    n = len(items)
    best_result = None  # (total_cost, total_discount, used_items, flags, (group1, group2))

    for i in range(1, n):
        for group1_indices in combinations(range(n), i):
            group1 = [items[j] for j in group1_indices]
            group2 = [items[j] for j in range(n) if j not in group1_indices]

            total1 = sum(p for _, p in group1)
            total2 = sum(p for _, p in group2)

            scenarios = []

            # TH1: Không dùng voucher
            total = total1 + total2
            scenarios.append((total, 0, 0, (False, False)))

            # TH2: Dùng voucher cho group1
            if total1 >= voucher_min:
                total = total1 - voucher_discount + total2
                scenarios.append((total, voucher_discount, len(group1), (True, False)))

            # TH3: Dùng voucher cho group2
            if total2 >= voucher_min:
                total = total1 + total2 - voucher_discount
                scenarios.append((total, voucher_discount, len(group2), (False, True)))

            # TH4: Cả 2 nhóm đều dùng voucher
            if total1 >= voucher_min and total2 >= voucher_min:
                total = total1 + total2 - 2 * voucher_discount
                scenarios.append((total, 2 * voucher_discount, len(group1) + len(group2), (True, True)))

            for scenario in scenarios:
                total_cost, discount, used_items, flags = scenario
                if best_result is None or (
                    discount > best_result[1] or
                    (discount == best_result[1] and total_cost < best_result[0]) or
                    (discount == best_result[1] and total_cost == best_result[0] and used_items < best_result[2])
                ):
                    best_result = (total_cost, discount, used_items, flags, (group1, group2))

    def show_group(label, group, use_voucher):
        if not group:
            return
        with st.container():
            if use_voucher:
                st.markdown(f"**{label}** 🎟️ *(dùng voucher {voucher_min}k - giảm {voucher_discount}k)*")
            else:
                st.markdown(f"**{label}**")
            for name, price in group:
                st.markdown(f"- {name} ({price}k)")
            st.markdown(f"**Tổng: {sum(p for _, p in group)}k**")

    if best_result:
        total_cost, discount, _, (v1, v2), (g1, g2) = best_result
        st.subheader("🔻 KẾT QUẢ TỐI ƯU")
        show_group("Nhóm 1", g1, v1)
        show_group("Nhóm 2", g2, v2)
        st.success(f"✅ Tổng chi phí sau giảm giá: **{total_cost}k** (giảm được {discount}k)")
    else:
        st.warning("❌ Không tìm được cách chia hợp lý để dùng voucher.")

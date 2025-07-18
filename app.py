import streamlit as st
from itertools import combinations, permutations

st.set_page_config(page_title="Tính voucher Highland tối ưu", layout="centered")

st.title("🤔 Tính voucher Highland tối ưu")

st.markdown("### ☕ Nhập danh sách món")
raw_items = st.text_area(
    "Mỗi dòng 1 món, định dạng: `tên món,giá` (vd: trà sữa,45)",
    height=200,
    placeholder="phin sữa đá,39\ntrà đào,55\ncf sữa m,48"
)

st.markdown("### 🎟️ Nhập danh sách voucher")
voucher_raw = st.text_area(
    "Mỗi dòng 1 voucher, định dạng: `tổng tối thiểu, số giảm` (vd: 135, 30)",
    height=150,
    placeholder="135, 30\n150, 40"
)

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

    # Parse danh sách voucher
    vouchers = []
    for line in voucher_raw.strip().split("\n"):
        try:
            min_total, discount = map(int, line.strip().split(","))
            vouchers.append((min_total, discount))
        except:
            st.error(f"❌ Dòng voucher không hợp lệ: `{line}`. Định dạng đúng là `135, 30`.")
            st.stop()

    if not vouchers:
        st.warning("⚠️ Cần ít nhất 1 voucher.")
        st.stop()

    n = len(items)
    best_result = None  # (total_cost, total_discount, used_items, (v1, v2), (group1, group2))

    for i in range(1, n):
        for group1_indices in combinations(range(n), i):
            group1 = [items[j] for j in group1_indices]
            group2 = [items[j] for j in range(n) if j not in group1_indices]

            total1 = sum(p for _, p in group1)
            total2 = sum(p for _, p in group2)

            scenarios = []

            # TH1: Không dùng voucher
            total = total1 + total2
            scenarios.append((total, 0, 0, (None, None)))

            # TH2: Dùng 1 voucher cho mỗi nhóm
            for v in vouchers:
                min_val, discount_val = v
                if total1 >= min_val:
                    total = total1 - discount_val + total2
                    scenarios.append((total, discount_val, len(group1), (v, None)))
                if total2 >= min_val:
                    total = total2 - discount_val + total1
                    scenarios.append((total, discount_val, len(group2), (None, v)))

            # TH3: Dùng 2 voucher khác nhau cho 2 nhóm
            if len(vouchers) >= 2:
                for v1, v2 in permutations(vouchers, 2):
                    min1, dis1 = v1
                    min2, dis2 = v2
                    if total1 >= min1 and total2 >= min2:
                        total = total1 + total2 - dis1 - dis2
                        scenarios.append((total, dis1 + dis2, len(group1) + len(group2), (v1, v2)))

            # Chọn tốt nhất trong các scenario
            for scenario in scenarios:
                total_cost, discount, used_items, flags = scenario
                if best_result is None or (
                    discount > best_result[1] or
                    (discount == best_result[1] and total_cost < best_result[0]) or
                    (discount == best_result[1] and total_cost == best_result[0] and used_items < best_result[2])
                ):
                    best_result = (total_cost, discount, used_items, flags, (group1, group2))

    def show_group(label, group, voucher_info):
        if not group:
            return
        with st.container():
            if voucher_info:
                st.markdown(f"**{label}** 🎟️ *(dùng voucher {voucher_info[0]}k - giảm {voucher_info[1]}k)*")
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

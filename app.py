import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Tính voucher tối ưu", layout="centered")

st.title("🧮 Tính chia nhóm món để dùng Voucher tối ưu")

# ========== Nhập danh sách món ==========
st.markdown("### ✅ Nhập danh sách món")
raw_items = st.text_area(
    "Mỗi dòng 1 món, định dạng: `tên món,giá` (vd: trà sữa,45)",
    height=200,
    placeholder="trà sữa,45\nbạc xỉu,39\ntrà đào,55\nphin đen,49\ncf sữa,29\ntrà dâu,59"
)

# ========== Nhập danh sách voucher ==========
st.markdown("### 🎟️ Nhập danh sách voucher")
raw_vouchers = st.text_area(
    "Mỗi dòng 1 voucher, định dạng: `giá trị tối thiểu,giảm giá` (vd: 135,30)",
    height=100,
    placeholder="135,30\n169,40"
)
st.markdown("💡 Nếu không nhập gì thì sẽ dùng mặc định: 135k giảm 30k và 169k giảm 40k.")

# ========== Xử lý khi bấm nút ==========
if st.button("🚀 Tính toán"):
    # --- Parse món ---
    items = []
    for line in raw_items.strip().split("\n"):
        try:
            name, price = line.strip().rsplit(",", 1)
            items.append((name.strip(), int(price.strip())))
        except:
            st.error(f"❌ Dòng món không hợp lệ: `{line}`. Định dạng phải là `tên món,giá`.")
            st.stop()

    if len(items) < 2:
        st.warning("⚠️ Cần ít nhất 2 món để chia nhóm.")
        st.stop()

    # --- Parse voucher ---
    voucher_list = []
    if raw_vouchers.strip():
        for line in raw_vouchers.strip().split("\n"):
            try:
                min_value, discount = map(lambda x: int(x.strip()), line.strip().split(","))
                voucher_list.append((min_value, discount))
            except:
                st.error(f"❌ Dòng voucher không hợp lệ: `{line}`. Định dạng phải là `giá trị tối thiểu,giảm giá`.")
                st.stop()
    else:
        voucher_list = [(135, 30), (169, 40)]  # Mặc định

    # === Tìm cách chia tối ưu ===
    n = len(items)
    best_result = None  # (total_cost, total_discount, used_items, (group1, group2, used_vouchers))

    for i in range(1, n):
        for group1_indices in combinations(range(n), i):
            group1 = [items[j] for j in group1_indices]
            group2 = [items[j] for j in range(n) if j not in group1_indices]

            total1 = sum(p for _, p in group1)
            total2 = sum(p for _, p in group2)

            # Xét mọi voucher có thể áp dụng cho từng nhóm
            applicable1 = [v for v in voucher_list if total1 >= v[0]]
            applicable2 = [v for v in voucher_list if total2 >= v[0]]

            # Duyệt các TH: không dùng, 1 nhóm dùng, 2 nhóm dùng
            scenarios = []

            # Không dùng voucher
            scenarios.append((total1 + total2, 0, len(group1) + len(group2), group1, group2, [], []))

            # Dùng cho group1
            for v in applicable1:
                scenarios.append((
                    total1 + total2 - v[1], v[1], len(group1) + len(group2), group1, group2, [v], []
                ))

            # Dùng cho group2
            for v in applicable2:
                scenarios.append((
                    total1 + total2 - v[1], v[1], len(group1) + len(group2), group1, group2, [], [v]
                ))

            # Dùng cho cả 2 nhóm
            for v1 in applicable1:
                for v2 in applicable2:
                    if v1 == v2 and voucher_list.count(v1) < 2:
                        continue  # Không dùng 2 lần 1 voucher nếu chỉ có 1
                    scenarios.append((
                        total1 + total2 - v1[1] - v2[1],
                        v1[1] + v2[1],
                        len(group1) + len(group2),
                        group1, group2,
                        [v1], [v2]
                    ))

            # Chọn best
            for sc in scenarios:
                if (best_result is None or
                    sc[1] > best_result[1] or
                    (sc[1] == best_result[1] and sc[0] < best_result[0])):
                    best_result = sc

    # ========== Hiển thị kết quả ==========
    def show_group(title, group, vouchers):
        if not group:
            return
        if vouchers:
            vstr = " + ".join([f"{v[0]}k🎟️-{v[1]}k" for v in vouchers])
            st.markdown(f"**{title}** 🎁 *({vstr})*")
        else:
            st.markdown(f"**{title}**")

        for name, price in group:
            st.markdown(f"- {name} ({price}k)")
        st.markdown(f"**Tổng: {sum(p for _, p in group)}k**")

    if best_result:
        cost, discount, _, g1, g2, v1, v2 = best_result
        st.subheader("📋 KẾT QUẢ TỐI ƯU")
        show_group("Nhóm 1", g1, v1)
        show_group("Nhóm 2", g2, v2)
        st.success(f"✅ Tổng chi phí sau giảm giá: **{cost}k** (giảm được {discount}k)")
    else:
        st.warning("❌ Không tìm được cách chia hợp lý.")

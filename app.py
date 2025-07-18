import streamlit as st
import itertools

st.set_page_config(page_title="Highlands Voucher App", layout="centered")

st.markdown("## ✅ Nhập danh sách món")
st.caption("Mỗi dòng 1 món, định dạng: `tên món,giá` (vd: trà sữa,45)")

mon_text = st.text_area(" ", height=200, placeholder="trà sữa,45\nbạc xỉu,39\ntrà đào,55")

st.markdown("## 🎟️ Nhập danh sách voucher")
st.caption("Mỗi dòng 1 voucher, định dạng: `giá trị tối thiểu,giảm giá` (vd: 135,30)")
voucher_text = st.text_area("  ", height=100, placeholder="135,30\n169,40")

st.markdown("💡 Nếu không nhập gì thì sẽ dùng mặc định: **135k giảm 30k và 169k giảm 40k**.")

btn = st.button("🚀 Tính toán")

if btn:
    # 👉 Xử lý danh sách món
    items = []
    for line in mon_text.splitlines():
        if ',' in line:
            name, price = line.strip().rsplit(",", 1)
            try:
                items.append((name.strip(), int(price.strip())))
            except:
                pass

    # 👉 Xử lý voucher (nếu người dùng không nhập thì dùng mặc định)
    if voucher_text.strip():
        vouchers = []
        for line in voucher_text.splitlines():
            if ',' in line:
                min_val, discount = line.strip().split(",")
                try:
                    vouchers.append((int(min_val.strip()), int(discount.strip())))
                except:
                    pass
    else:
        vouchers = [(135, 30), (169, 40)]

    # ✅ Tính tất cả cách chia nhóm và dùng voucher
    n = len(items)
    best_result = None

    for i in range(1, 2 ** n):
        group1 = [items[j] for j in range(n) if (i >> j) & 1]
        group2 = [items[j] for j in range(n) if not (i >> j) & 1]

        for use_voucher1 in [None] + vouchers:
            for use_voucher2 in [None] + vouchers:
                if use_voucher1 == use_voucher2 and use_voucher1 is not None:
                    continue  # không dùng cùng 1 voucher cho cả 2 nhóm

                def calc_total(group, voucher):
                    total = sum(p for _, p in group)
                    if voucher and total >= voucher[0]:
                        return total - voucher[1], voucher
                    return total, None

                total1, used_voucher1 = calc_total(group1, use_voucher1)
                total2, used_voucher2 = calc_total(group2, use_voucher2)
                grand_total = total1 + total2
                total_discount = (sum(p for _, p in group1) + sum(p for _, p in group2)) - grand_total
                total_voucher_items = (
                    (len(group1) if used_voucher1 else 0)
                    + (len(group2) if used_voucher2 else 0)
                )

                candidate = {
                    "group1": group1,
                    "group2": group2,
                    "voucher1": used_voucher1,
                    "voucher2": used_voucher2,
                    "grand_total": grand_total,
                    "total_discount": total_discount,
                    "voucher_items": total_voucher_items,
                }

                if best_result is None:
                    best_result = candidate
                else:
                    # So sánh: ưu tiên giảm nhiều nhất -> tổng ít nhất -> ít món dùng voucher
                    a, b = best_result, candidate
                    if b["total_discount"] > a["total_discount"]:
                        best_result = b
                    elif b["total_discount"] == a["total_discount"]:
                        if b["grand_total"] < a["grand_total"]:
                            best_result = b
                        elif b["grand_total"] == a["grand_total"]:
                            if b["voucher_items"] < a["voucher_items"]:
                                best_result = b

    if not best_result:
        st.error("⚠️ Không có món nào hợp lệ để tính toán.")
    else:
        st.markdown("## 📋 KẾT QUẢ TỐI ƯU")
        def display_group(title, group, voucher):
            st.markdown(f"**{title}**" + (f" 🎁 *({voucher[0]}k 🎫 -{voucher[1]}k)*" if voucher else ""))
            for name, price in group:
                st.markdown(f"- {name} ({price}k)")
            st.markdown(f"**Tổng:** {sum(p for _, p in group)}k")
            st.markdown("")

        display_group("Nhóm 1", best_result["group1"], best_result["voucher1"])
        display_group("Nhóm 2", best_result["group2"], best_result["voucher2"])

        st.success(f"✅ **Tổng chi phí sau giảm giá: {best_result['grand_total']}k** (giảm được {best_result['total_discount']}k)")

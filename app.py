import streamlit as st
import itertools

st.set_page_config(page_title="App Tối Ưu Voucher Highland", page_icon="🥤", layout="centered")

st.title("🥤 App Tối Ưu Voucher Highland")

st.markdown("### ✅ Nhập danh sách món")
st.markdown("Mỗi dòng 1 món, định dạng: `tên món,giá` (vd: trà sữa,45)")

mon_input = st.text_area(" ", height=200, placeholder="trà sữa,45\nbạc xỉu,39\ntrà đào,55")
items = []
for line in mon_input.strip().split("\n"):
    if "," in line:
        name, price = line.strip().rsplit(",", 1)
        try:
            items.append((name.strip(), int(price.strip())))
        except:
            pass

st.markdown("### 🎟 Nhập danh sách voucher")
st.markdown("Mỗi dòng 1 voucher, định dạng: `giá trị tối thiểu,giảm giá` (vd: 135,30)")

voucher_input = st.text_area(" ", height=100, placeholder="135,30\n169,40")
vouchers = []
for line in voucher_input.strip().split("\n"):
    if "," in line:
        min_val, discount = line.strip().split(",", 1)
        try:
            vouchers.append((int(min_val.strip()), int(discount.strip())))
        except:
            pass

if not vouchers:
    vouchers = [(135, 30), (169, 40)]

st.markdown("💡 Nếu không nhập gì thì sẽ dùng mặc định: 135k giảm 30k và 169k giảm 40k.")

if st.button("🚀 Tính toán") and items:
    n = len(items)
    best_result = None

    def calc_total(group, voucher):
        total = sum(p for _, p in group)
        used = False
        if voucher and total >= voucher[0]:
            total -= voucher[1]
            used = True
        return total, used

    voucher_opts = [None] + list(enumerate(vouchers))

    for combo in itertools.product([0, 1], repeat=n):
        group1 = [items[i] for i in range(n) if combo[i] == 0]
        group2 = [items[i] for i in range(n) if combo[i] == 1]

        for id1, voucher1 in voucher_opts:
            for id2, voucher2 in voucher_opts:
                if voucher1 and voucher2 and id1 == id2:
                    continue  # Không dùng cùng voucher cho cả 2 nhóm

                total1, used1 = calc_total(group1, voucher1)
                total2, used2 = calc_total(group2, voucher2)

                total_cost = total1 + total2
                total_discount = (voucher1[1] if used1 else 0) + (voucher2[1] if used2 else 0)
                used_count = (used1 * len(group1)) + (used2 * len(group2))

                result = {
                    "group1": group1,
                    "group2": group2,
                    "voucher1": voucher1 if used1 else None,
                    "voucher2": voucher2 if used2 else None,
                    "total_cost": total_cost,
                    "total_discount": total_discount,
                    "used_count": used_count,
                }

                if (
                    best_result is None
                    or result["total_discount"] > best_result["total_discount"]
                    or (
                        result["total_discount"] == best_result["total_discount"]
                        and result["total_cost"] < best_result["total_cost"]
                    )
                    or (
                        result["total_discount"] == best_result["total_discount"]
                        and result["total_cost"] == best_result["total_cost"]
                        and result["used_count"] < best_result["used_count"]
                    )
                ):
                    best_result = result

    if best_result:
        st.markdown("## 🧾 **KẾT QUẢ TỐI ƯU**")

        def show_group(title, group, voucher):
            st.markdown(f"**{title}**" + (f" 🎁 *({voucher[0]}k 🧾 -{voucher[1]}k)*" if voucher else ""))
            for name, price in group:
                st.markdown(f"- {name} ({price}k)")
            st.markdown(f"**Tổng:** {sum(p for _, p in group)}k")

        show_group("Nhóm 1", best_result["group1"], best_result["voucher1"])
        show_group("Nhóm 2", best_result["group2"], best_result["voucher2"])

        st.success(f"✅ Tổng chi phí sau giảm giá: {best_result['total_cost']}k (giảm được {best_result['total_discount']}k)")
    else:
        st.warning("Không tìm được tổ hợp phù hợp.")

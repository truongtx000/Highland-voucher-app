import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Tính voucher Highland tối ưu", layout="centered")

st.title("🧮 Tính voucher Highland tối ưu")

# === NHẬP DANH SÁCH MÓN ===
st.markdown("### ✅ Nhập danh sách món")
raw_items = st.text_area(
    "Mỗi dòng 1 món, định dạng: `tên món,giá` (vd: trà sữa,45)",
    height=200,
    placeholder="phin sữa đá,39\ntrà đào,55\ncf sữa m,48"
)

# === NHẬP VOUCHER ===
st.markdown("### 🎟️ Nhập danh sách voucher")
raw_vouchers = st.text_area(
    "Mỗi dòng 1 voucher, định dạng: `giá trị tối thiểu,giảm giá` (vd: 135,30)",
    value="135,30\n169,40",
    height=100,
    placeholder="vd: 135,30\n169,40"
)
st.caption("💡 Nếu không nhập gì thì sẽ dùng mặc định: 135k giảm 30k và 169k giảm 40k.")

if st.button("🚀 Tính toán"):
    # === Parse danh sách món ===
    items = []
    for line in raw_items.strip().split("\n"):
        try:
            name, price = line.strip().rsplit(",", 1)
            items.append((name.strip(), int(price.strip())))
        except:
            st.error(f"❌ Dòng món không hợp lệ: `{line}`. Đảm bảo có dấu phẩy ngăn cách.")
            st.stop()

    if len(items) < 2:
        st.warning("⚠️ Cần ít nhất 2 món để chia nhóm.")
        st.stop()

    # === Parse danh sách voucher ===
    vouchers = []
    raw_vouchers = raw_vouchers.strip()
    if not raw_vouchers:
        raw_vouchers = "135,30\n169,40"  # dùng_

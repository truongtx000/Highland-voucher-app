import streamlit as st
from PIL import Image

# === CSS STYLING ===
st.markdown("""
    <style>
        body {
            background-color: #FFFDF1;
        }
        .main {
            background-color: #FFFDF1;
        }
        .title-section {
            background-color: #AA1F24;
            padding: 40px 0 25px 0;
            text-align: center;
            color: white;
            font-size: 40px;
            font-weight: bold;
            border-radius: 0;
            margin-bottom: 30px;
        }
        .input-block {
            background-color: #FFF9E7;
            border-radius: 20px;
            padding: 15px 20px;
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
        }
        .input-block img {
            width: 60px;
            height: 60px;
        }
        .input-text {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        textarea {
            background-color: white;
            border: 2px solid #C29A5F !important;
            border-radius: 10px !important;
        }
        div.stButton > button:first-child {
            background-color: #AA1F24;
            color: white;
            font-weight: bold;
            padding: 15px;
            font-size: 20px;
            border: none;
            border-radius: 15px;
            width: 100%;
            margin-top: 20px;
        }
        div.stButton > button:first-child:hover {
            background-color: #8A191E;
        }
    </style>
""", unsafe_allow_html=True)

# === TITLE ===
st.markdown('<div class="title-section">Tiết Kiệm Highland<br>Cùng Voucher</div>', unsafe_allow_html=True)

# === INPUT BLOCK 1 ===
st.markdown("""
<div class="input-block">
    <img src="https://raw.githubusercontent.com/truongtx000/Highland-voucher-app/refs/heads/main/images/coffee.png"/>
    <div class="input-text">
        <div style="font-weight: 700; font-size: 20px">Nhập danh sách món</div>
        <div style="color: #555">Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)</div>
    </div>
</div>
""", unsafe_allow_html=True)
menu_input = st.text_area("", key="menu", height=150, label_visibility="collapsed")

# === INPUT BLOCK 2 ===
st.markdown("""
<div class="input-block">
    <img src="https://raw.githubusercontent.com/truongtx000/Highland-voucher-app/refs/heads/main/images/voucher.png"/>
    <div class="input-text">
        <div style="font-weight: 700; font-size: 20px">Nhập danh sách voucher</div>
        <div style="color: #555">Nhập mỗi dòng: [giá tối thiểu] [số tiền giảm] (vd: 169 40)</div>
    </div>
</div>
""", unsafe_allow_html=True)
voucher_input = st.text_area("", key="voucher", height=150, label_visibility="collapsed")

# === BUTTON ===
# Chỉ cho phép 1 form duy nhất trong app
with st.form(key="main_form"):
    submitted = st.form_submit_button("Tính kết quả tối ưu")

    if submitted:
        # TODO: Gọi xử lý logic tại đây
        st.success("Đã xử lý xong!")

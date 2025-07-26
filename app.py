import streamlit as st

# ======== Custom CSS =========
st.markdown("""
    <style>
        body {
            background-color: #FFFDF1 !important;
        }
        .block-container {
            background-color: #FFFDF1 !important;
        }
        textarea {
            background-color: white !important;
            border: 2px solid #C29A5F !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        .custom-button {
            background-color: #AA1F24;
            color: white;
            font-weight: bold;
            font-size: 22px;
            padding: 12px 36px;
            border: none;
            border-radius: 18px;
            cursor: pointer;
            width: 100%;
        }
        .custom-button:hover {
            background-color: #8e1a1d;
        }
        .title-container {
            background-color: #AA1F24;
            padding: 30px;
            text-align: center;
            color: white;
            font-size: 36px;
            font-weight: bold;
            border-radius: 0;
        }
        .input-box {
            background-color: #FFF9E8;
            padding: 20px;
            border-radius: 20px;
            margin-bottom: 20px;
        }
        .input-header {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .input-header img {
            width: 48px;
            height: 48px;
        }
        .input-header-title {
            font-size: 22px;
            font-weight: bold;
        }
        .input-subtitle {
            font-size: 16px;
            margin-top: -6px;
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# ======== Title ========
st.markdown('<div class="title-container">Tiết Kiệm Highland<br>Cùng Voucher</div>', unsafe_allow_html=True)

# ======== Input Form ========
with st.form("main_form"):
    # --- Nhập danh sách món ---
    st.markdown("""
    <div class="input-box">
        <div class="input-header">
            <img src="https://raw.githubusercontent.com/truongtx000/Highland-voucher-app/refs/heads/main/images/coffee.png">
            <div>
                <div class="input-header-title">Nhập danh sách món</div>
                <div class="input-subtitle">Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    menu_text = st.text_area("", height=150)

    # --- Nhập danh sách voucher ---
    st.markdown("""
    <div class="input-box">
        <div class="input-header">
            <img src="https://raw.githubusercontent.com/truongtx000/Highland-voucher-app/refs/heads/main/images/voucher.png">
            <div>
                <div class="input-header-title">Nhập danh sách voucher</div>
                <div class="input-subtitle">Nhập mỗi dòng: [giá tối thiểu] [số tiền giảm] (vd: 169 40)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    voucher_text = st.text_area("", height=120)

    # --- Submit Button ---
    submitted = st.form_submit_button("Tính kết quả tối ưu")
    if submitted:
        st.success("✅ Đã xử lý xong!")
        # TODO: xử lý kết quả tại đây

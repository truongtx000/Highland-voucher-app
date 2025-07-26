import streamlit as st

# URL icon (đặt icon phù hợp ở đây)
COFFEE_ICON_URL = "https://cdn-icons-png.flaticon.com/512/2935/2935469.png"

# Inject custom CSS
st.markdown("""
    <style>
    .input-section {
        display: flex;
        align-items: center;
        background-color: #fffcef;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #ddb87d;
    }
    .icon-circle {
        flex-shrink: 0;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #fce4c5;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;
    }
    .icon-circle img {
        width: 30px;
        height: 30px;
    }
    .input-content h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
    }
    .input-content p {
        margin: 4px 0 0 0;
        font-size: 14px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Nhóm icon + tiêu đề + mô tả
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown(f'''
    <div class="icon-circle">
        <img src="{COFFEE_ICON_URL}" alt="Coffee Icon">
    </div>
    <div class="input-content">
        <h2>Nhập danh sách món</h2>
        <p>Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)</p>
    </div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Text area nhập món
items_input = st.text_area(
    "items_input_area",
    height=150,
    label_visibility="collapsed",
    value="cf sữa m, 39\ntrà sen, 45\nbh kem cheese, 65\nphô mai kem, 69"
)

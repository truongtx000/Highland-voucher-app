import streamlit as st
from itertools import combinations
import math

# Cấu hình trang của Streamlit
st.set_page_config(page_title="Tiết Kiệm Highland Cùng Voucher", layout="centered")

# --- CSS Tùy Chỉnh để tạo giao diện chính xác như hình bạn cung cấp ---
st.markdown(
    """
<style>
/* Import font Roboto Condensed từ Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap');

/* Đặt màu nền chung cho toàn bộ trang */
body {
    background-color: #FFFDF1; /* Màu vàng nhạt / trắng kem */
    font-family: 'Roboto Condensed', sans-serif; /* Font Roboto Condensed */
}

/* Ẩn Streamlit header và footer mặc định */
header { visibility: hidden; }
footer { visibility: hidden; }

/* Container chính của Streamlit, điều chỉnh padding để nội dung sát hơn */
.stApp {
    background-color: #FFFDF1; /* Đảm bảo nền app trùng với body */
}

/* Vùng chứa nội dung chính để bo góc và đổ bóng cho toàn bộ app */
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 20px; /* Thêm padding trái để tránh chữ sát màn hình*/
    padding-right: 20px; /* Thêm padding phải để tránh chữ sát màn hình*/
    max-width: 700px; /* Giới hạn chiều rộng để giống ảnh */
    margin: 0 auto; /* Căn giữa block container */
    box-sizing: border-box; /* Bao gồm padding trong kích thước */
}

/* Loại bỏ các box container mặc định của Streamlit nếu chúng được sử dụng */
div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Phần tiêu đề ứng dụng (Highland Voucher App) */
.header-bg {
    background-color: #A02B2B; /* Màu đỏ đậm của Highland */
    color: white;
    padding: 30px 20px 20px 20px; /* Đệm trên dưới, không đệm ngang */
    border-radius: 0px; /* Bỏ bo góc */
    text-align: center;
    margin-bottom: 30px; /* Khoảng cách với phần tiếp theo */
    box-shadow: 0 4px 10px rgba(0,0,0,0.2); /* Đổ bóng mạnh hơn cho header */
    box-sizing: border-box; /* Bao gồm padding và border trong kích thước */
}

/* Tiêu đề chính thành một thẻ h1 duy nhất*/
.header-bg h1 {
    font-size: 2.5em; /* Kích thước chữ lớn */
    font-weight: 900; /* Rất đậm */
    margin: 0; /* Bỏ margin mặc định */
    letter-spacing: 0.5px; /* Khoảng cách giữa các chữ cái */
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2); /* Đổ bóng chữ */
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
    line-height: 1.2; /* Khoảng cách dòng cho tiêu đề */
}


/* Container cho mỗi phần nhập liệu (Món ăn, Voucher) */
.input-section {
    display: flex; /* Dùng flexbox để căn chỉnh icon và nội dung */
    align-items: flex-start; /* Căn chỉnh theo đầu của các phần tử (để tiêu đề sát icon)*/
    margin-bottom: 25px; /* Khoảng cách giữa các section */
    box-sizing: border-box;
    /* Đảm bảo nền của input-section không có khoảng trắng */
    background-color: #FFFDF1; 
}

/* Icon lớn trong hình tròn */
.icon-circle {
    background-color: #F8D882; /* Màu vàng của hình tròn */
    border-radius: 50%; /* Hình tròn hoàn hảo */
    width: 70px; /* Kích thước hình tròn */
    height: 70px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 15px; /* Khoảng cách giữa hình tròn và text */
    flex-shrink: 0; /* Không cho hình tròn bị co lại */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Đổ bóng nhẹ */
}

.icon-circle img { /* Định dạng ảnh bên trong hình tròn */
    width: 60%; /* Kích thước ảnh so với hình tròn */
    height: 60%;
    object-fit: contain; /* Đảm bảo ảnh vừa vặn */
    vertical-align: middle; /* Căn giữa ảnh trong thẻ img */
}

/* Nội dung text (tiêu đề và mô tả) */
.input-content {
    flex-grow: 1; /* Cho phép nội dung này mở rộng */
}

.input-content h2 {
    font-size: 1.4em; /* Kích thước chữ tiêu đề */
    font-weight: bold;
    color: #333;
    margin-top: 0px !important; /* Đảm bảo sát với icon, override mọi margin mặc định của h2*/
    margin-bottom: 5px;
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
    line-height: 1.2; /* Khoảng cách dòng cho tiêu đề */
}

.input-content p {
    font-size: 0.9em; /* Kích thước chữ mô tả */
    color: #777;
    margin-bottom: 10px;
    line-height: 1.4;
}

/* --- Xử lý khoảng trắng của Text Area và đảm bảo hiển thị --- */

/* Ẩn các label mặc định của Streamlit cho text area */
.stTextArea label {
    display: none;
}

/* Điều chỉnh trực tiếp thẻ textarea */
.stTextArea textarea {
    border-radius: 8px; /* Bo góc nhẹ */
    border: 2px solid #C29A5F; /* Viền màu nâu đậm */
    padding: 12px;
    box-shadow: none; /* Bỏ đổ bóng bên trong */
    width: 100%; /* Chiếm toàn bộ chiều rộng của cha */
    box-sizing: border-box; /* Tính cả padding và border vào width */
    font-size: 1.1em;
    min-height: 150px; /* Chiều cao tối thiểu, tăng lên */
    background-color: white; /* Nền trắng cho textbox */
}

/* Cho text area của voucher nhỏ lại một chút */
/* Sử dụng data-testid để nhắm mục tiêu cụ thể hơn nếu cần */
div[data-testid="stTextArea"].stTextArea:nth-of-type(2) textarea {
    min-height: 90px; /* Chiều cao nhỏ hơn cho voucher textarea*/
}

/* Cố gắng giảm padding hoặc margin không mong muốn của các div cha của textarea */
/* Điều này có thể giúp loại bỏ khoảng trắng thừa */
div[data-testid="stTextArea"] {
    margin-top: -10px !important; /* Di chuyển lên trên một chút để giảm khoảng cách */
    padding: 0 !important; /* Loại bỏ padding */
    background-color: #FFFDF1 !important; /* Đảm bảo nền khớp */
}

/* Nếu có div con của stTextArea có padding/margin, hãy thử reset */
div[data-testid="stTextArea"] > div:first-child {
    padding: 0 !important;
    margin: 0 !important;
    background-color: #FFFDF1 !important; /* Đảm bảo nền khớp */
}


/* --- Sửa lỗi nút bấm --- */
/* Đảm bảo nút nằm gọn và có màu */
div.stButton {
    background-color: #FFFDF1 !important; /* Đảm bảo khớp với nền trang */
    padding: 0 !important; /* Loại bỏ padding nếu có */
    margin-top: 30px; /* Khoảng cách với phần trên */
    margin-bottom: 20px; /* Khoảng cách với phần dưới */
    text-align: center; /* Căn giữa nút */
}

div.stButton > button:first-child {
    background-color: #A02B2B; /* Màu đỏ đậm */
    color: white;
    border-radius: 12px; /* Bo góc */
    height: 3.5em; /* Chiều cao nút */
    width: 90%; /* Giảm một chút so với 100% để tránh tràn */
    max-width: 400px; /* Giới hạn chiều rộng tối đa */
    display: inline-block; /* Để căn giữa với text-align: center */
    font-size: 1.3em; /* Cỡ chữ lớn hơn */
    font-weight: bold;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25); /* Đổ bóng mạnh */
    transition: all 0.3s ease-in-out; /* Hiệu ứng chuyển động mượt mà */
    letter-spacing: 0.5px;
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
    white-space: normal; /* Cho phép chữ xuống dòng nếu quá dài */
    line-height: 1.2; /* Điều chỉnh khoảng cách dòng cho chữ trên nút */
}

/* Hiệu ứng khi di chuột qua nút */
div.stButton > button:first-child:hover {
    background-color: #8D2525; /* Màu đỏ sẫm hơn khi hover */
    box-shadow: 0 6px 15px rgba(0,0,0,0.35); /* Đổ bóng mạnh hơn nữa */
    transform: translateY(-2px); /* Nút nhích lên một chút */
    cursor: pointer; /* Biểu tượng con trỏ khi di chuột */
}

/* Tiêu đề cho phần kết quả */
.results-header {
    font-size: 1.8em;
    font-weight: bold;
    color: #333; /* Màu chữ đen */
    margin-top: 20px; /* Giảm margin-top để sát hơn với nút bấm */
    margin-bottom: 10px; /* Giảm margin-bottom để sát hơn với kết quả*/
    border-bottom: 2px solid #C29A5F; /* Đường gạch chân màu nâu */
    padding-bottom: 10px;
    text-align: center;
    text-transform: uppercase; /* Chữ hoa */
    letter-spacing: 1px;
    font-family: 'Roboto Condensed', sans-serif; /* Áp dụng font Roboto Condensed */
}

/* Container cho mỗi nhóm kết quả (voucher + món ăn) */
.result-group {
    background-color: white;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 12px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

.result-group-title {
    font-weight: bold;
    color: #424242; /* Màu xám đậm */
    margin-bottom: 5px;
    font-size: 1.05em;
}

.result-item {
    color: #616161; /* Màu xám */
    margin-left: 15px;
    font-size: 0.9em;
    line-height: 1.4; /* Khoảng cách dòng */
}

/* Tổng chi phí sau giảm giá */
.final-cost {
    font-size: 1.5em;
    font-weight: bold;
    color: #1B5E20; /* Màu xanh lá cây đậm */
    margin-top: 30px;
    text-align: center;
    padding: 15px;
    background-color: #E8F5E9; /* Nền xanh lá nhạt */
    border-radius: 10px;
    border: 1px solid #A5D6A7;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.discount-amount {
    color: #D32F2F; /* Màu đỏ cho số tiền giảm */
    font-weight: normal; /* Không in đậm quá mức */
    font-size: 0.9em;
    margin-left: 10px;
}

/* Thông báo cảnh báo */
div.stWarning {
    background-color: #fffde7;
    color: #FFB300;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #FFD54F;
    font-weight: bold;
    margin-bottom: 15px;
}

/* Thông báo thành công */
div.stSuccess {
    background-color: #e8f5e9;
    color: #388e3c;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #81c784;
    font-weight: bold;
    margin-bottom: 15px;
}

</style>
    """,
    unsafe_allow_html=True,
)

# --- Xử lý dữ liệu đầu vào ---
# Sử dụng cache để tránh parse lại dữ liệu nếu input không đổi
@st.cache_data
def parse_items(text):
    lines = text.strip().split("\n")
    items = []
    for i, line in enumerate(lines):
        if "," in line:
            name, price_str = line.rsplit(",", 1)
            try:
                price = int(price_str.strip())
                items.append({"id": i, "name": name.strip(), "price": price})
            except ValueError:
                st.warning(f"❗ Lỗi định dạng giá ở dòng: '{line}'. Vui lòng nhập số nguyên.")
                return [] # Trả về rỗng để báo hiệu lỗi
        elif line.strip(): # Nếu có dòng không chứa dấu phẩy nhưng không rỗng
            st.warning(f"❗ Định dạng không đúng ở dòng: '{line}'. Vui lòng nhập theo dạng 'tên, giá'.")
            return [] # Trả về rỗng để báo hiệu lỗi
    return items

@st.cache_data

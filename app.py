import streamlit as st
import itertools

st.title("🎁 KẾT QUẢ TỐI ƯU")

# Nhập danh sách món
items_input = st.text_area("Nhập danh sách món (mỗi dòng 1 món, ví dụ: cf sữa m 39)", value="""
Cf dừa 75k
Cf sữa M 39k
Chanh dây đá viên 39k
Ct 1 trà dâu tằm m - 59k
1 cf sữa m (39k)
1 cf anhvu m (39k)
Loan trà vải s (45k)
Phindi hạnh nhân (49k)
Cf sữa vừa thêm kem muối mặn size M (49k)
Bạc xỉu vừa (39k)
""".strip())

# Nhập voucher
voucher_input = st.text_area("Nhập danh sách voucher (ví dụ: 169 40)", value="""
169 40
135 30
135 30
""".strip())

def parse_items(text):
    lines = text.strip().split('\n')
    items = []
    for line in lines:
        name_part = line.strip().rsplit('(', 1)[0].strip()
        price = int(''.join([c for c in line if c.isdigit()]))
        items.append({'name': name_part, 'price': price})
    return items

def parse_vouchers(text):
    lines = text.strip().split('\n')
    vouchers = []
    for i, line in enumerate(lines):
        parts = line.strip().split()
        min_total = int(parts[0])
        discount = int(parts[1])
        vouchers.append({'id': f'V{i+1}', 'min_total': min_total, 'discount': discount})
    return sorted(vouchers, key=lambda v: -v['discount'])  # Ưu tiên voucher giảm nhiều

items = parse_items(items_input)
vouchers = parse_vouchers(voucher_input)

used_indexes = set()
results = []

# Hàm tìm tổ hợp tối ưu cho 1 voucher
def find_best_group(available_items, min_total):
    best_combo = None
    best_total = float('inf')
    n = len(available_items)
    for r in range(1, n+1):
        for combo in itertools.combinations(available_items, r):
            total_price = sum(item['price'] for item in combo)
            if total_price >= min_total and total_price < best_total:
                best_total = total_price
                best_combo = combo
    return best_combo

remaining_items = items[:]
for voucher in vouchers:
    available = [item for i, item in enumerate(remaining_items) if i not in used_indexes]
    best_group = find_best_group(available, voucher['min_total'])
    if best_group:
        group_indexes = [remaining_items.index(item) for item in best_group]
        used_indexes.update(group_indexes)
        results.append({'items': best_group, 'voucher': voucher})

# Các món không dùng voucher
unused_items = [item for i, item in enumerate(remaining_items) if i not in used_indexes]

# Hiển thị kết quả
total_after_discount = 0

for i, group in enumerate(results):
    st.markdown(f"### Nhóm {i+1} 🎁 ({group['voucher']['min_total']}k -{group['voucher']['discount']}k)")
    for item in group['items']:
        st.write(f"- {item['name']} ({item['price']}k)")
    total = sum(item['price'] for item in group['items'])
    st.markdown(f"**Tổng: {total}k**")
    total_after_discount += total - group['voucher']['discount']

if unused_items:
    st.markdown(f"### Nhóm {len(results)+1} (Không dùng voucher)")
    for item in unused_items:
        st.write(f"- {item['name']} ({item['price']}k)")
    total = sum(item['price'] for item in unused_items)
    st.markdown(f"**Tổng: {total}k**")
    total_after_discount += total

st.success(f"✅ Tổng chi phí sau giảm giá: {total_after_discount}k")

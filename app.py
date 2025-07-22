import streamlit as st
import itertools

st.title("🎁 KẾT QUẢ TỐI ƯU")

items_input = st.text_area("Nhập danh sách món (mỗi dòng 1 món, ví dụ: cf sữa m 39)", value="""
""".strip())

voucher_input = st.text_area("Nhập danh sách voucher (ví dụ: 169 40)", value="""
169 40
135 30
135 30
""".strip())

def parse_items(text):
    lines = text.strip().split('\n')
    items = []
    for idx, line in enumerate(lines):
        name_part = line.strip().rsplit('(', 1)[0].strip()
        price = int(''.join([c for c in line if c.isdigit()]))
        items.append({'id': idx, 'name': name_part, 'price': price})
    return items

def parse_vouchers(text):
    lines = text.strip().split('\n')
    vouchers = []
    for i, line in enumerate(lines):
        parts = line.strip().split()
        min_total = int(parts[0])
        discount = int(parts[1])
        vouchers.append({'id': f'V{i+1}', 'min_total': min_total, 'discount': discount})
    return sorted(vouchers, key=lambda v: -v['discount'])

items = parse_items(items_input)
vouchers = parse_vouchers(voucher_input)

used_ids = set()
results = []

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

for voucher in vouchers:
    available = [item for item in items if item['id'] not in used_ids]
    best_group = find_best_group(available, voucher['min_total'])
    if best_group:
        group_ids = [item['id'] for item in best_group]
        used_ids.update(group_ids)
        results.append({'items': best_group, 'voucher': voucher})

unused_items = [item for item in items if item['id'] not in used_ids]

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

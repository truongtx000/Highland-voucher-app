import streamlit as st
import itertools

st.title("🌽 Kết Quả Tối Ʈu")

# 🔍 Nhập danh sách món
items_input = st.text_area("Nhập danh sách món (mỗi dòng 1 món, ví dụ: cf sữa m 39)")

# 🎁 Nhập danh sách voucher
voucher_input = st.text_area("Nhập danh sách voucher (ví dụ: 169 40)", value="""
169 40
135 30
135 30
""".strip())

# ✍️ Phân tích chuỗi

def parse_items(text):
    lines = text.strip().split('\n')
    items = []
    for idx, line in enumerate(lines):
        digits = ''.join([c for c in line if c.isdigit()])
        price = int(digits) if digits else 0
        name_part = line.strip().rsplit('(', 1)[0].strip()
        items.append({'id': idx, 'name': name_part, 'price': price})
    return items

def parse_vouchers(text):
    lines = text.strip().split('\n')
    vouchers = []
    for i, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        min_total = int(parts[0])
        discount = int(parts[1])
        vouchers.append({'id': f'V{i+1}', 'min_total': min_total, 'discount': discount})
    return sorted(vouchers, key=lambda v: -v['discount'])

items = parse_items(items_input)
vouchers = parse_vouchers(voucher_input)

# 🚀 Tính tối ưu toàn cục
best_result = None
best_total = float('inf')

n = len(items)
all_ids = set(range(n))

# Sinh hoặc không dùng voucher nào
for used_voucher_ids in itertools.product([0, 1], repeat=len(vouchers)):
    selected_vouchers = [v for v, use in zip(vouchers, used_voucher_ids) if use]
    if not selected_vouchers:
        continue

    used_item_ids = set()
    groups = []
    valid = True

    for v in selected_vouchers:
        remaining_items = [item for item in items if item['id'] not in used_item_ids]

        best_combo = None
        best_combo_total = float('inf')

        for r in range(1, len(remaining_items)+1):
            for combo in itertools.combinations(remaining_items, r):
                total_price = sum(item['price'] for item in combo)
                if total_price >= v['min_total'] and total_price < best_combo_total:
                    best_combo = combo
                    best_combo_total = total_price

        if best_combo:
            used_item_ids.update(item['id'] for item in best_combo)
            groups.append({'items': best_combo, 'voucher': v})
        else:
            valid = False
            break

    if not valid:
        continue

    remaining_items = [item for item in items if item['id'] not in used_item_ids]
    total_price = sum(sum(i['price'] for i in g['items']) - g['voucher']['discount'] for g in groups)
    total_price += sum(item['price'] for item in remaining_items)

    if total_price < best_total:
        best_total = total_price
        best_result = (groups, remaining_items)

# 📉 Xuất kết quả
if best_result:
    groups, unused = best_result
    total_after_discount = 0
    for i, group in enumerate(groups):
        st.markdown(f"### Nhóm {i+1} 🎁 ({group['voucher']['min_total']}k -{group['voucher']['discount']}k)")
        for item in group['items']:
            st.write(f"- {item['name']} ({item['price']}k)")
        total = sum(item['price'] for item in group['items'])
        st.markdown(f"**Tổng: {total}k**")
        total_after_discount += total - group['voucher']['discount']

    if unused:
        st.markdown(f"### Nhóm {len(groups)+1} (Không dùng voucher)")
        for item in unused:
            st.write(f"- {item['name']} ({item['price']}k)")
        total = sum(item['price'] for item in unused)
        st.markdown(f"**Tổng: {total}k**")
        total_after_discount += total

    st.success(f"✅ Tổng chi phí sau giảm giá: {total_after_discount}k")
else:
    st.warning("⚠️ Không tìm được tổ hợp voucher tối ưu.")

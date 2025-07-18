from itertools import combinations

# === DANH SÁCH MÓN ===
items = [
    ("thanh dao nong s", 45),
    ("1 bac xiu nong  de càfe rieng m", 39),
    ("thach dao m", 55),
    ("phìndi hanh nhan m ", 49),
    ("cf sua s", 29),
    ("tra dau tam m", 59),

]

# === VOUCHER THÔNG TIN ===
voucher1_min, voucher1_discount = 135, 30
voucher2_min, voucher2_discount = 135, 30

n = len(items)

best_result = None  # (total_cost, total_discount, used_items_for_voucher, flags, (group1, group2))

# === DUYỆT MỌI CÁCH CHIA NHÓM ===
for i in range(1, n):
    for group1_indices in combinations(range(n), i):
        group1 = [items[j] for j in group1_indices]
        group2 = [items[j] for j in range(n) if j not in group1_indices]

        total1 = sum(p for _, p in group1)
        total2 = sum(p for _, p in group2)

        # Các trường hợp voucher
        scenarios = []

        # TH1: Không dùng voucher
        total = total1 + total2
        scenarios.append((total, 0, 0, (False, False)))

        # TH2: Dùng voucher 1
        if total1 >= voucher1_min:
            total = total1 - voucher1_discount + total2
            scenarios.append((total, voucher1_discount, len(group1), (True, False)))

        # TH3: Dùng voucher 2
        if total2 >= voucher2_min:
            total = total1 + total2 - voucher2_discount
            scenarios.append((total, voucher2_discount, len(group2), (False, True)))

        # TH4: Dùng cả hai voucher
        if total1 >= voucher1_min and total2 >= voucher2_min:
            total = total1 + total2 - voucher1_discount - voucher2_discount
            scenarios.append((total, voucher1_discount + voucher2_discount, len(group1) + len(group2), (True, True)))

        # Chọn phương án tốt nhất trong các scenario này
        for scenario in scenarios:
            total_cost, discount, used_items, flags = scenario
            if best_result is None or (
                discount > best_result[1] or
                (discount == best_result[1] and total_cost < best_result[0]) or
                (discount == best_result[1] and total_cost == best_result[0] and used_items < best_result[2])
            ):
                best_result = (total_cost, discount, used_items, flags, (group1, group2))

# === IN KẾT QUẢ ===
def print_group(label, group, use_voucher, min_val, discount_val):
    if use_voucher:
        print(f"{label} (dùng voucher {min_val}k - giảm {discount_val}k):")
    else:
        print(f"{label}:")
    for name, price in group:
        print(f"  - {name} ({price}k)")
    print(f"  Tổng: {sum(p for _, p in group)}k\n")

# === HIỂN THỊ ===
if best_result:
    total_cost, discount, used_items, (v1, v2), (g1, g2) = best_result
    print("🔻 KẾT QUẢ TỐI ƯU:")
    print_group("Nhóm 1", g1, v1, voucher1_min, voucher1_discount)
    print_group("Nhóm 2", g2, v2, voucher2_min, voucher2_discount)
    print(f"✅ Tổng chi phí sau giảm giá: {total_cost}k")
else:
    print("❌ Không tìm được cách chia hợp lý.")

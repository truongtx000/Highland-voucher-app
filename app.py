import streamlit as st
from itertools import combinations
import math

st.set_page_config(page_title="Tiết Kiệm Highland Cùng Voucher", layout="centered")

from itertools import combinations
import math

st.set_page_config(page_title="Highland Voucher App", layout="centered")
st.title("🧾 KẾT QUẢ TỐI ƯU")

# --- Nhập danh sách món ---
st.header("📋 Nhập danh sách món")
items_input = st.text_area("Nhập tên và giá từng món, mỗi dòng 1 món (vd: cf sữa m, 39)", height=200, value="cf sữa m, 39\ntrà sen, 45\nbh kem cheese, 65\nbh kem cheese, 65\nphô mai kem, 69\n")

# --- Nhập danh sách voucher ---
st.header("🎁 Nhập danh sách voucher")
voucher_input = st.text_area("Nhập mỗi voucher theo dạng: min_price, discount", value="135,30\n135,30\n169,40")

# --- Xử lý dữ liệu đầu vào ---
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
                continue
        elif line.strip(): # Nếu có dòng không chứa dấu phẩy nhưng không rỗng
            st.warning(f"❗ Định dạng không đúng ở dòng: '{line}'. Vui lòng nhập theo dạng 'tên, giá'.")
    return items

@st.cache_data
def parse_vouchers(text):
    lines = text.strip().split("\n")
    vouchers = []
    for i, line in enumerate(lines):
        if "," in line:
            try:
                min_total, discount = map(int, line.strip().split(","))
                vouchers.append({
                    "id": i,
                    "min_total": min_total,
                    "discount": discount,
                    "label": f"🎁 ({min_total}k -{discount}k)"
                })
            except ValueError:
                st.warning(f"❗ Lỗi định dạng voucher ở dòng: '{line}'. Vui lòng nhập theo dạng 'min_total,discount'.")
                continue
        elif line.strip():
            st.warning(f"❗ Định dạng không đúng ở dòng: '{line}'. Vui lòng nhập theo dạng 'min_total,discount'.")
    return vouchers

# --- Thuật toán tìm kiếm tối ưu toàn cục ---
@st.cache_data(show_spinner="Đang tìm kiếm giải pháp tối ưu nhất...")
def find_optimal_voucher_distribution(items, vouchers):
    """
    Tìm cách phân bổ món ăn vào các voucher để tổng chi phí là thấp nhất.
    Sử dụng thuật toán backtracking để thử mọi cách kết hợp.
    """
    
    # Khởi tạo các biến toàn cục cho quá trình tìm kiếm
    best_overall_cost = float('inf')
    best_overall_solution = []

    # Danh sách các voucher có thể sử dụng (để theo dõi trạng thái sử dụng)
    available_vouchers = [v.copy() for v in vouchers] # Tạo bản sao để không ảnh hưởng dữ liệu gốc

    # Hàm đệ quy để thử các cách gán món ăn vào voucher
    def recurse(item_index, current_item_assignments):
        nonlocal best_overall_cost, best_overall_solution

        # Nếu đã gán hết tất cả các món ăn
        if item_index == len(items):
            # Đánh giá giải pháp hiện tại
            current_cost, solution_groups = evaluate_solution(items, available_vouchers, current_item_assignments)
            
            if current_cost < best_overall_cost:
                best_overall_cost = current_cost
                best_overall_solution = solution_groups
            return

        # Lấy món ăn hiện tại
        current_item = items[item_index]

        # OPTION 1: Gán món này vào một voucher đã được sử dụng hoặc chuẩn bị được sử dụng
        for voucher_idx, voucher in enumerate(available_vouchers):
            # Nếu voucher chưa được sử dụng hoặc đã được gán một phần
            # Tạo một bản sao để tránh sửa đổi trạng thái của vòng lặp cha
            new_assignments = [list(group) for group in current_item_assignments]
            
            # Thêm món vào nhóm voucher này
            if voucher_idx >= len(new_assignments): # Nếu đây là voucher mới trong current_item_assignments
                new_assignments.append([current_item])
            else:
                new_assignments[voucher_idx].append(current_item)

            # Tiếp tục đệ quy với món tiếp theo
            recurse(item_index + 1, new_assignments)

        # OPTION 2: Để món này không dùng voucher (tạm thời) hoặc thanh toán riêng
        # Thêm món này vào một "nhóm không voucher" riêng biệt (hoặc cuối cùng)
        no_voucher_assignments = [list(group) for group in current_item_assignments]
        # Thêm vào nhóm cuối cùng (được coi là nhóm không voucher)
        if not no_voucher_assignments or voucher_idx < len(available_vouchers): # Nếu chưa có nhóm nào, hoặc tất cả đã gán voucher
            no_voucher_assignments.append([current_item])
        else:
            no_voucher_assignments[-1].append(current_item) # Thêm vào nhóm cuối cùng

        recurse(item_index + 1, no_voucher_assignments) # Món tiếp theo

    def evaluate_solution(all_items, vouchers_list, assignments):
        """
        Đánh giá một giải pháp cụ thể (cách các món ăn được gán vào các nhóm voucher).
        """
        current_total_cost = 0
        solution_groups = []
        
        assigned_item_ids = set()

        for group_idx, assigned_items_in_group in enumerate(assignments):
            group_total = sum(item["price"] for item in assigned_items_in_group)
            
            # Đánh dấu các item đã được gán
            for item in assigned_items_in_group:
                assigned_item_ids.add(item["id"])

            # Tìm voucher tốt nhất cho nhóm này (nếu có voucher tương ứng)
            best_voucher_for_group = None
            max_discount_for_group = 0
            
            # Lặp qua các voucher có sẵn để xem voucher nào có thể áp dụng
            # và mang lại discount cao nhất cho group_total
            for voucher in vouchers_list:
                if group_total >= voucher["min_total"]:
                    if voucher["discount"] > max_discount_for_group:
                        max_discount_for_group = voucher["discount"]
                        best_voucher_for_group = voucher

            if best_voucher_for_group:
                current_total_cost += (group_total - best_voucher_for_group["discount"])
                solution_groups.append({
                    "voucher": best_voucher_for_group,
                    "items": assigned_items_in_group,
                    "total": group_total,
                    "final": group_total - best_voucher_for_group["discount"]
                })
                # Loại bỏ voucher đã sử dụng (đảm bảo mỗi voucher chỉ dùng 1 lần)
                vouchers_list.remove(best_voucher_for_group) 
            else:
                current_total_cost += group_total
                solution_groups.append({
                    "voucher": None,
                    "items": assigned_items_in_group,
                    "total": group_total,
                    "final": group_total
                })
        
        # Xử lý các món còn lại không được gán vào bất kỳ nhóm nào (có thể do lỗi logic ban đầu)
        # Hoặc các món không đủ điều kiện cho bất kỳ voucher nào
        remaining_unassigned_items = [item for item in all_items if item["id"] not in assigned_item_ids]
        if remaining_unassigned_items:
            remaining_total = sum(item["price"] for item in remaining_unassigned_items)
            current_total_cost += remaining_total
            solution_groups.append({
                "voucher": None,
                "items": remaining_unassigned_items,
                "total": remaining_total,
                "final": remaining_total
            })


        return current_total_cost, solution_groups

    # Bắt đầu quá trình đệ quy
    # Chúng ta cần một cách để gán các món vào các nhóm, sau đó áp dụng voucher
    # Cách tiếp cận backtracking ban đầu (từng item một) khá phức tạp để quản lý trạng thái voucher.
    # Thay đổi sang cách tiếp cận: thử mọi cách phân chia items thành các N nhóm, sau đó áp dụng M voucher.
    # Đây là bài toán partition và assignment.
    
    # Cách hiệu quả hơn cho bài toán này là thử mọi tổ hợp con của items cho TỪNG VOUCHER.
    # Sau đó tìm kiếm sâu để thấy kết hợp nào là tốt nhất.
    # Điều này vẫn là brute-force nhưng có cấu trúc hơn.

    # Giải pháp tối ưu hơn cho bài toán này (được đề cập trong đánh giá ban đầu):
    # Dùng một thuật toán Branch and Bound hoặc một dạng quy hoạch động cho Knapsack (Multiple Knapsack)
    # hoặc một cách tiếp cận dựa trên đồ thị.
    # Tuy nhiên, để giữ cho code không quá phức tạp cho một ví dụ Streamlit,
    # chúng ta sẽ sửa lại hàm recurse để nó tìm kiếm theo hướng "gán voucher vào các tập hợp món".

    best_total_cost = float('inf')
    best_solution_details = []

    # Tạo một danh sách các index của món ăn để dễ dàng thao tác
    item_indices = list(range(len(items)))

    # Hàm đệ quy để thử mọi cách phân chia món ăn cho các voucher
    # remaining_item_indices: danh sách các chỉ số món ăn còn lại
    # current_voucher_index: chỉ số voucher đang xét
    # current_groups: danh sách các nhóm món ăn đã được gán cho voucher
    # current_cost: tổng chi phí hiện tại
    def find_best_combination_recursive(remaining_item_indices, current_voucher_index, current_groups_info):
        nonlocal best_total_cost, best_solution_details

        # Nếu đã xét hết tất cả các voucher
        if current_voucher_index == len(vouchers):
            # Tất cả các món còn lại (nếu có) sẽ được tính tiền không voucher
            remaining_cost = sum(items[i]["price"] for i in remaining_item_indices)
            final_cost = sum(g["final"] for g in current_groups_info) + remaining_cost
            
            # Nếu có các món còn lại, thêm vào nhóm "không voucher"
            if remaining_item_indices:
                remaining_items_details = [items[i] for i in remaining_item_indices]
                current_groups_info.append({
                    "voucher": None,
                    "items": remaining_items_details,
                    "total": sum(item["price"] for item in remaining_items_details),
                    "final": sum(item["price"] for item in remaining_items_details)
                })

            if final_cost < best_total_cost:
                best_total_cost = final_cost
                best_solution_details = current_groups_info
            
            # Quay lại trạng thái trước khi thêm nhóm "không voucher" để không ảnh hưởng các nhánh khác
            if remaining_item_indices:
                current_groups_info.pop() 
            return

        current_voucher = vouchers[current_voucher_index]
        
        # Duyệt qua tất cả các tổ hợp con của các món ăn còn lại cho voucher hiện tại
        # bao gồm cả trường hợp không sử dụng voucher này
        
        # Option 1: Không sử dụng voucher hiện tại cho bất kỳ món nào
        # Chuyển sang voucher tiếp theo
        find_best_combination_recursive(remaining_item_indices, current_voucher_index + 1, list(current_groups_info))


        # Option 2: Sử dụng voucher hiện tại cho một tập hợp các món ăn
        for r in range(1, len(remaining_item_indices) + 1):
            for combo_indices in combinations(remaining_item_indices, r):
                selected_items_for_voucher = [items[i] for i in combo_indices]
                group_total = sum(item["price"] for item in selected_items_for_voucher)

                if group_total >= current_voucher["min_total"]:
                    discounted_group_cost = group_total - current_voucher["discount"]
                    
                    # Tạo trạng thái mới
                    new_remaining_item_indices = [i for i in remaining_item_indices if i not in combo_indices]
                    new_groups_info = list(current_groups_info)
                    new_groups_info.append({
                        "voucher": current_voucher,
                        "items": selected_items_for_voucher,
                        "total": group_total,
                        "final": discounted_group_cost
                    })

                    # Tiếp tục đệ quy với các món còn lại và voucher tiếp theo
                    find_best_combination_recursive(new_remaining_item_indices, current_voucher_index + 1, new_groups_info)

    # Bắt đầu tìm kiếm với tất cả các món và voucher đầu tiên
    find_best_combination_recursive(item_indices, 0, [])

    # Tổng kết chi phí gốc
    original_total = sum(item["price"] for item in items)
    
    # Sắp xếp lại giải pháp theo thứ tự các nhóm đã được áp dụng hoặc không có voucher
    final_solution_groups = []
    
    # Thêm các nhóm có voucher trước
    for group in best_solution_details:
        if group["voucher"]:
            final_solution_groups.append(group)
    
    # Sau đó thêm nhóm không có voucher (nếu có)
    remaining_unassigned_items_at_end = []
    assigned_ids = set()
    for group in final_solution_groups:
        for item in group["items"]:
            assigned_ids.add(item["id"])
    
    for item in items:
        if item["id"] not in assigned_ids:
            remaining_unassigned_items_at_end.append(item)

    if remaining_unassigned_items_at_end:
        final_solution_groups.append({
            "voucher": None,
            "items": remaining_unassigned_items_at_end,
            "total": sum(item["price"] for item in remaining_unassigned_items_at_end),
            "final": sum(item["price"] for item in remaining_unassigned_items_at_end)
        })

    return final_solution_groups, best_total_cost

# --- Giao diện và Hiển thị kết quả ---
items = parse_items(items_input)
vouchers = parse_vouchers(voucher_input)

if st.button("🚀 Tính kết quả tối ưu"):
    if not items:
        st.warning("❗ Vui lòng nhập ít nhất 1 món.")
    elif not vouchers:
        st.warning("❗ Vui lòng nhập ít nhất 1 voucher.")
    else:
        # Gọi hàm tìm kiếm tối ưu
        result_groups, final_cost = find_optimal_voucher_distribution(items, vouchers)

        st.subheader("📄 KẾT QUẢ TỐI ƯU")
        for idx, group in enumerate(result_groups, 1):
            if group["voucher"]:
                st.markdown(f"**Nhóm {idx}** {group['voucher']['label']} _(Tổng: {group['total']}k → {group['final']}k)_")
            else:
                st.markdown(f"**Nhóm {idx}** _(Không dùng voucher)_ _(Tổng: {group['total']}k)_")
            st.markdown("\n".join([f"- {item['name']} ({item['price']}k)" for item in group["items"]]))
            st.markdown("")

        original_total = sum(item["price"] for item in items)
        total_discount = original_total - final_cost
        st.success(f"✅ Tổng chi phí sau giảm giá: **{final_cost}k** (giảm được **{total_discount}k**)")

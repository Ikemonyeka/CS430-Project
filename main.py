# # main.py

# # Step 1: Parse price.txt
# def parse_prices(filename):
#     prices = {}
#     with open(filename, 'r') as f:
#         for line in f:
#             parts = line.strip().split()
#             if len(parts) != 2:
#                 continue
#             item_id, price = parts
#             prices[int(item_id)] = int(price)
#     return prices

# # Step 2: Parse input.txt (shopping list)
# def parse_input(filename):
#     shopping_list = {}
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#         num_items = int(lines[0].strip())
#         for line in lines[1:num_items+1]:
#             parts = line.strip().split()
#             if len(parts) < 2:
#                 continue
#             item_id, qty = int(parts[0]), int(parts[1])
#             shopping_list[item_id] = qty
#     return shopping_list

# # Step 3: Parse promotions.txt
# def parse_promotions(filename):
#     promotions = []
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#         num_promos = int(lines[0].strip())
#         for line in lines[1:num_promos+1]:
#             parts = line.strip().split()
#             if len(parts) < 3:
#                 continue
#             promo = {}
#             num_items = int(parts[0])
#             for i in range(num_items):
#                 item_id = int(parts[1 + 2 * i])
#                 qty = int(parts[2 + 2 * i])
#                 promo[item_id] = qty
#             promo_price = int(parts[-1])
#             promotions.append({'items': promo, 'price': promo_price})
#     return promotions

# # Step 4: Run parsing and print results
# if __name__ == "__main__":
#     prices = parse_prices('price.txt')
#     shopping_list = parse_input('input.txt')
#     promotions = parse_promotions('promotions.txt')

#     print("Prices:", prices)
#     print("Shopping List:", shopping_list)
#     print("Promotions:", promotions)

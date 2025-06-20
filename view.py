import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from optimizer import minimize_cost


# pasre uploaded files
def parse_prices(path):
    prices = {}
    with open(path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                prices[int(parts[0])] = float(parts[1])
    return prices

def parse_input(path):
    shopping_list = {}
    with open(path, 'r') as f:
        lines = f.readlines()
        count = int(lines[0].strip())
        for line in lines[1:count+1]:
            parts = line.strip().split()
            if len(parts) >= 2:
                shopping_list[int(parts[0])] = int(parts[1])
    return shopping_list

def parse_promotions(path):
    promotions = []
    with open(path, 'r') as f:
        lines = f.readlines()
        num = int(lines[0].strip())
        for line in lines[1:num+1]:
            parts = list(map(int, line.strip().split()))
            if len(parts) < 3:
                continue
            promo = {}
            num_items = parts[0]
            for i in range(num_items):
                item_id = parts[1 + 2*i]
                qty = parts[2 + 2*i]
                promo[item_id] = qty
            promo_price = parts[-1]
            promotions.append({'items': promo, 'price': promo_price})
    return promotions

# tkinter ui
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CS430 Most Profitable Purchase UI")

        self.input_path = ""
        self.price_path = ""
        self.promo_path = ""

        tk.Button(root, text="Upload input.txt", command=self.upload_input).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(root, text="Upload price.txt", command=self.upload_price).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Upload promotions.txt", command=self.upload_promo).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(root, text="Parse Files", command=self.parse_files).grid(row=0, column=3, padx=10, pady=5)
        tk.Button(root, text="Run Optimization", command=self.run_optim).grid(row=0, column=4, padx=10, pady=5)

        self.output = scrolledtext.ScrolledText(root, width=100, height=25)
        self.output.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

    def upload_input(self):
        self.input_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.output.insert(tk.END, f"[✔] Selected input.txt: {self.input_path}\n")

    def upload_price(self):
        self.price_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.output.insert(tk.END, f"[✔] Selected price.txt: {self.price_path}\n")

    def upload_promo(self):
        self.promo_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.output.insert(tk.END, f"[✔] Selected promotions.txt: {self.promo_path}\n")

    def parse_files(self):
        if not (self.input_path and self.price_path and self.promo_path):
            messagebox.showerror("Error", "Please upload all three files.")
            return

        try:
            prices = parse_prices(self.price_path)
            shopping_list = parse_input(self.input_path)
            promotions = parse_promotions(self.promo_path)

            self.output.insert(tk.END, "\n--- Parsed Files ---\n")
            self.output.insert(tk.END, f"Prices: {prices}\n")
            self.output.insert(tk.END, f"Shopping List: {shopping_list}\n")
            self.output.insert(tk.END, f"Promotions:\n")
            for promo in promotions:
                self.output.insert(tk.END, f"  {promo}\n")
            self.output.insert(tk.END, "---------------------\n")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse files:\n{str(e)}")
    
    def run_optim(self):
        if not (self.input_path and self.price_path and self.promo_path):
            messagebox.showerror("Error", "Please choose all three files first.")
            return
        try:
            prices = parse_prices(self.price_path)
            shopping = parse_input(self.input_path)
            promotions = parse_promotions(self.promo_path)

            best_cost, used_promos, remaining_items, remaining_cost = minimize_cost(shopping, prices, promotions)

            self.output.insert(tk.END, "Shopping List:\n")
            for item_id, qty in shopping.items():
                self.output.insert(tk.END, f"   Item {item_id} (Qty: {qty}, Unit Price: {prices[item_id]})\n")

            if used_promos:
                self.output.insert(tk.END, "\nPromotions Applied:\n")
                for promo in used_promos:
                    promo_str = ' + '.join(f"{v}×{k}" for k, v in promo.items())
                    price = next(p['price'] for p in promotions if p['items'] == promo)
                    self.output.insert(tk.END, f" {promo_str} @ ${price}\n")
            else:
                self.output.insert(tk.END, "\nNo promotions applied.\n")

            if remaining_items:
                self.output.insert(tk.END, "\nItems Remaining:\n")
                for item_id, qty in remaining_items.items():
                    unit = prices[item_id]
                    self.output.insert(tk.END, f"   {qty} × Item {item_id} @ ${unit} = ${qty * unit}\n")

            self.output.insert(tk.END, f"\nTotal Optimal Cost: ${best_cost:.2f}\n")

            # Save to output.txt
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(f"Total Optimal Cost: ${best_cost:.2f}\n")
                if used_promos:
                    f.write("Promotions Applied:\n")
                    for promo in used_promos:
                        promo_str = ' + '.join(f"{v}×{k}" for k, v in promo.items())
                        price = next(p['price'] for p in promotions if p['items'] == promo)
                        f.write(f"- [{promo_str}] → ${price}\n")
                if remaining_items:
                    f.write("Remaining Items:\n")
                    for item_id, qty in remaining_items.items():
                        unit = prices[item_id]
                        f.write(f"- {qty} × Item {item_id} @ ${unit} = ${qty * unit}\n")


            self.output.insert(tk.END, "\ndata stored in output.txt\n")

        except Exception as e:
            messagebox.showerror("Error", f"Optimization failed:\n{e}")

# start ui
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

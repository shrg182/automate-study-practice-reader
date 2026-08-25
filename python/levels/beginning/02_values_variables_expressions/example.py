def make_receipt(price: float, quantity: int, tax_rate: float = 0.06) -> str:
    subtotal = price * quantity
    tax = subtotal * tax_rate
    total = subtotal + tax
    return f"Subtotal: ${subtotal:.2f} | Tax: ${tax:.2f} | Total: ${total:.2f}"

if __name__ == "__main__":
    print(make_receipt(12.50, 3))

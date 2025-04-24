def get_product_price(product):
    for field in ["price", "price_per_switch", "total_price"]:
        if hasattr(product, field):
            return getattr(product, field)
    return None

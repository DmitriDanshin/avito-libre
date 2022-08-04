from app import App
from bot.models import ProductFile, Product
from logger import queue_logger


def register_product(product_name: str):

    app = App()

    filenames = app.parse(
        {"csv": True},
        product_name
    )

    queue_logger.info(
        f"Product with name {product_name} "
        f"successfully registered"
    )

    product_filenames = (
        ProductFile(
            name=product_filename,
            product_id=Product.get_by_name(product_name).id
        )
        for product_filename in filenames
    )

    ProductFile.add_many(product_filenames)

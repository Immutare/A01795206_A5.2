"""
Ejercicio de programacion 2
"""

import sys
import time
import json
from dataclasses import dataclass
import logging


@dataclass(frozen=True)
class ProductDTO:
    """
    Product data transfer object
    """

    # pylint: disable=too-many-instance-attributes
    title: str
    type: str
    description: str
    filename: str
    height: int
    width: int
    price: float
    rating: int

    @classmethod
    def from_dict(cls, data):
        """
        Gets a json objects and converts to an instance of the class
        """
        return cls(
            title=data.get("title"),
            type=data.get("type"),
            description=data.get("description"),
            filename=data.get("filename"),
            height=data.get("height"),
            width=data.get("width"),
            price=data.get("price"),
            rating=data.get("rating"),
        )


@dataclass(frozen=True)
class SalesDTO:
    """
    Sales data transfer object
    """

    sale_id: int
    sale_date: str
    product: str
    quantity: int

    @classmethod
    def from_dict(cls, data):
        """
        Gets a json objects and converts to an instance of the class
        """
        return cls(
            sale_id=data.get("SALE_ID"),
            sale_date=data.get("SALE_Date"),
            product=data.get("Product"),
            quantity=data.get("Quantity"),
        )


def map_products(products: list[ProductDTO]):
    """
    Converts the product list into a dictionary
    """
    dictionary = {}
    for product in products:
        indx = f"{product.title}"
        if indx in dictionary:
            logging.exception("The product is duplicated")
        dictionary[indx] = product

    return dictionary


def read_json_from_file(path):
    """
    Reads a file
    """
    # importing the module
    # Opening JSON file
    with open(path, encoding="utf-8") as json_file:
        content = json.load(json_file)
        json_file.close()

    return content


def total_cost_from_sales(products: list[ProductDTO], sales: list[SalesDTO]):
    """
    Receives a product list and a sales list and returns the total of the sales
    """
    prod_mapped = map_products(products)
    total_sum = 0

    for sale in sales:
        product = prod_mapped.get(sale.product)

        if product is None:
            logging.exception("The product sold isn't on the product list")
            continue

        total = product.price if (product.price) else 0
        total = total * sale.quantity if (sale.quantity) else total

        total_sum += total

    return total_sum


def print_total(total, compute_duration, **kwargs):
    """
    Prints the results of the computation on a file
    """
    file_1 = kwargs.get("file_1", "file_1.txt")
    file_2 = kwargs.get("file_2", "file_2.txt")

    with open("SalesResults.txt", "a", encoding="utf-8") as f:
        print(f"Results of computation of files {file_1} and {file_2}")
        f.write(f"Results of computation of files {file_1} and {file_2}\n")

        print(f"Total: {total}")
        f.write(f"Total: {total}\n")

        print(f"\nThe computing time was: {compute_duration}s")
        f.write(f"\n\nThe computing time was: {compute_duration}s\n\n\n\n")
        f.close()


def main():
    """
    Main function
    """
    start_time = time.time()

    products_path = sys.argv[1]
    sales_path = sys.argv[2]

    products = read_json_from_file(products_path)
    products = list(map(ProductDTO.from_dict, products))

    sales = read_json_from_file(sales_path)
    sales = list(map(SalesDTO.from_dict, sales))

    total_cost = total_cost_from_sales(products, sales)

    compute_duration = time.time() - start_time
    print(f"--- {compute_duration} seconds ---")

    print_total(total_cost,
                compute_duration, file_1=products_path,
                file_2=sales_path)


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    main()

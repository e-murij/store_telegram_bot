import os
import json

from data_base.dbalchemy import DBManager
from models.category import Category
from models.order import Order
from models.product import Products


JSON_PATH = 'jsons'


def _load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='UTF-8') as file:
        return json.load(file)


def _load_data(session):
    category_names = _load_from_json('category')
    for cat in category_names:
        new_category = Category(name=cat['name'])
        session.add(new_category)
    product_names = _load_from_json('products')
    for product in product_names:
        new_product = Products(name=product['name'],
                               title=product['title'],
                               price=product['price'],
                               quantity=product['quantity'],
                               category_id=product['category_id']
                               )
        session.add(new_product)
    session.commit()
    session.close()


if __name__ == '__main__':
    DB = DBManager()
    _load_data(DB._session)


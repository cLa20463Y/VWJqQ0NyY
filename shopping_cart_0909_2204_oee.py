# 代码生成时间: 2025-09-09 22:04:41
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import json

# 假设的商品模型
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

# 购物车数据模型
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity=1):
        # 检查商品是否已在购物车中
        for item in self.items:
            if item['product'].id == product.id:
                item['quantity'] += quantity
                return
        # 添加新商品到购物车
        self.items.append({'product': product, 'quantity': quantity})

    def remove_item(self, product_id):
        # 从购物车中移除商品
        self.items = [item for item in self.items if item['product'].id != product_id]

    def update_quantity(self, product_id, quantity):
        # 更新购物车中商品的数量
        for item in self.items:
            if item['product'].id == product_id:
                if quantity <= 0:
                    self.remove_item(product_id)
                else:
                    item['quantity'] = quantity
                break

    def get_total(self):
        # 计算购物车总价
        total = sum(item['product'].price * item['quantity'] for item in self.items)
        return total

# 购物车视图
class ShoppingCartView:
    def __init__(self, request):
        self.request = request
        self.cart = ShoppingCart()

    @view_config(route_name='add_product', renderer='json', permission='add')
    def add_product(self):
        data = json.loads(self.request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        try:
            product = self._get_product_by_id(product_id)
            self.cart.add_item(product, quantity)
            return {'status': 'success', 'message': 'Product added to cart'}
        except ValueError:
            return {'status': 'error', 'message': 'Product not found'}

    @view_config(route_name='remove_product', renderer='json', permission='remove')
    def remove_product(self):
        data = json.loads(self.request.body)
        product_id = data.get('product_id')
        self.cart.remove_item(product_id)
        return {'status': 'success', 'message': 'Product removed from cart'}

    @view_config(route_name='update_product', renderer='json', permission='update')
    def update_product(self):
        data = json.loads(self.request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        self.cart.update_quantity(product_id, quantity)
        return {'status': 'success', 'message': 'Product quantity updated'}

    @view_config(route_name='get_cart', renderer='json')
    def get_cart(self):
        return {'items': self.cart.items, 'total': self.cart.get_total()}

    def _get_product_by_id(self, product_id):
        # 假设的产品数据库查询
        # 这里用静态字典模拟
        products = {
            1: Product(1, 'Product 1', 10.99),
            2: Product(2, 'Product 2', 5.99),
            3: Product(3, 'Product 3', 3.99)
        }
        try:
            return products[product_id]
        except KeyError:
            raise ValueError('Product not found')

# 初始化配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('add_product', '/cart/add')
    config.add_route('remove_product', '/cart/remove')
    config.add_route('update_product', '/cart/update')
    config.add_route('get_cart', '/cart')
    config.scan()
    return config.make_wsgi_app()

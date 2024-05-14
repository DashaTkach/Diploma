from django.core.management import BaseCommand

from .models import *


class Command(BaseCommand):
    def get_data(self, data):

        shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=1)

        for category in data['categories']:
            category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
            category_object.save()

        for item in data['goods']:
            product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

            product_info, _ = ProductInfo.objects.get_or_create(external_id=item['id'],
                                                                model=item['model'],
                                                                price=item['price'],
                                                                price_rrc=item['price_rrc'],
                                                                product_id=product.id,
                                                                quantity=item['quantity'],
                                                                shop_id=shop.id)

            for name, value in item['parameters'].items():
                parameter, _ = Parameter.objects.get_or_create(name=name)
                ProductParameter.objects.get_or_create(product_info_id=product_info.id,
                                                       parameter_id=parameter.id,
                                                       value=value)

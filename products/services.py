from decimal import Decimal
from unicodedata import normalize

from django.shortcuts import get_object_or_404

from .models import Product


class EstrategiaDescuento:
    porcentaje = 0
    factor = Decimal('1.00')

    def calcular(self, precio):
        return (Decimal(precio) * self.factor).quantize(Decimal('0.01'))


class DescuentoElectronica(EstrategiaDescuento):
    porcentaje = 10
    factor = Decimal('0.90')


class DescuentoRopa(EstrategiaDescuento):
    porcentaje = 20
    factor = Decimal('0.80')


class SinDescuento(EstrategiaDescuento):
    pass


def obtener_estrategia(categoria_nombre):
    nombre = normalize('NFKD', categoria_nombre).encode('ascii', 'ignore').decode().casefold()
    return {
        'electronica': DescuentoElectronica,
        'ropa': DescuentoRopa,
    }.get(nombre, SinDescuento)()


def obtener_precio_final(pk):
    producto = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    estrategia = obtener_estrategia(producto.category.name)
    return {
        'producto': producto.name,
        'categoria': producto.category.name,
        'precio_original': str(producto.price),
        'descuento_porcentaje': estrategia.porcentaje,
        'precio_final': str(estrategia.calcular(producto.price)),
    }

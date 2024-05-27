# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='preparando')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Adicionando o campo total

    def __str__(self):
        return self.customer_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculando o total do pedido ao salvar o item do pedido
        self.order.total = sum(item.product.price * item.quantity for item in self.order.items.all())
        self.order.save()  # Salvar o pedido para atualizar o total

def get_default_order():
    # Obter o primeiro pedido do banco de dados
    first_order = Order.objects.first()
    # Retornar o primeiro pedido, se existir, caso contrário, retornar None
    return first_order if first_order else None

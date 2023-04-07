from django.db import models
# Create your models here.


class Product(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    sizes = (
        ('S', 'small'),
        ('M', 'medium'),
        ('L', 'large'),
        ('F', 'Free')
    )
    size = models.CharField(choices=sizes, max_length=1)

    def __str__(self):
        return f'{self.name}-{self.code}'

    def save(self, *args, **kwargs):
        max_code = Product.objects.filter(name=self.name).aggregate(
            models.Max('code'))['code__max']

        if max_code:
            new_code = int(max_code.split('-')[-1]) + 1
        else:
            new_code = 1

        # 새로운 코드를 형식에 맞게 생성합니다.
        self.code = f'{self.name.lower()}-{str(new_code).zfill(3)}'

        super(Product, self).save(*args, **kwargs)
        Inbound.objects.create(product=self,qunatity=0)


class Inbound(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    qunatity = models.PositiveBigIntegerField()
    date = models.DateField(auto_now_add=True)
    price = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(Inbound, self).save(*args, **kwargs)


class Outbound(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    qunatity = models.PositiveBigIntegerField()
    date = models.DateField(auto_now_add=True)
    price = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(Outbound, self).save(*args, **kwargs)


class Inventory(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    qunatity = models.PositiveBigIntegerField()
    price = models.PositiveBigIntegerField()

    def calculate_stock(self):
        inbound_qty = sum(self.product.inbound_set.all(
        ).values_list('quantity', flat=True))
        outbound_qty = sum(
            self.product.outbound_set.all().values_list('quantity', flat=True))
        self.quantity = inbound_qty - outbound_qty
        self.save()

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

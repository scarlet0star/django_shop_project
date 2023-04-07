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
        return f'{self.code}'

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
        Inventory.objects.create(product=self, quantity=0, price=self.price)


class Inbound(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    date = models.DateField(auto_now_add=True)
    price = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(Inbound, self).save(*args, **kwargs)


class Outbound(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    date = models.DateField(auto_now_add=True)
    price = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(Outbound, self).save(*args, **kwargs)


class Inventory(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.product.code} : {self.quantity}'

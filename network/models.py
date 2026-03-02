from django.db import models


class NetworkNode(models.Model):
    LEVEL_FACTORY = 0
    LEVEL_RETAIL = 1
    LEVEL_IE = 2

    LEVEL_CHOICES = [
        (LEVEL_FACTORY, "Завод"),
        (LEVEL_RETAIL, "Розничная сеть"),
        (LEVEL_IE, "Индивидуальный предприниматель"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients"
    )
    debt_to_supplier = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self):
        return self.name

    @property
    def level(self):
        if self.supplier is None:
            return 0
        return self.supplier.level + 1


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"

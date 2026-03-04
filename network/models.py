from django.db import models


class NetworkNode(models.Model):
    """Модель звена сети продаж электроники."""

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
        """Вычисляет уровень звена в иерархии сети."""
        if self.supplier is None:
            return 0

        visited = set()
        current = self.supplier
        level = 0

        while current is not None:
            if current.id in visited:
                raise ValueError("Circular hierarchy detected")
            visited.add(current.id)
            level += 1
            current = current.supplier

        return level


class Product(models.Model):
    """Модель продукта, продаваемого звеном сети."""
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

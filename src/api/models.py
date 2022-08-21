from django.db import models

from werkzeug.security import generate_password_hash, check_password_hash


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(Base):
    name = models.CharField(max_length=50, unique=True)
    logo = models.CharField(max_length=100, unique=True)
    parent_category_id = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)


class Product(Base):
    category_id = models.ForeignKey('Category', on_delete=models.PROTECT)
    manufacturer_id = models.ForeignKey('Manufacturer', on_delete=models.PROTECT)
    is_new = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    default_color = models.ForeignKey('ProductColor', on_delete=models.PROTECT)


class ProductDetails(Base):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    product_color_id = models.ForeignKey('ProductColor', on_delete=models.PROTECT)
    product_size_id = models.ForeignKey('ProductSize', on_delete=models.PROTECT)
    stored = models.IntegerField(default=0)


class Manufacturer(Base):
    name = models.CharField(max_length=50, unique=True)
    logo = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True, blank=True)


class ProductSize(models.Model):
    size = models.CharField(max_length=3)  # computed


class ProductColor(models.Model):
    color = models.CharField(max_length=20)
    color_hex = models.CharField(max_length=7)  # computed


class ProductMaterial(models.Model):
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField('Product', through='productmaterial_product')


class productmaterial_product(models.Model):
    product_material_id = models.ForeignKey('ProductMaterial', on_delete=models.PROTECT)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    part = models.IntegerField(default=100)

    class Meta:
        unique_together = (('product_material_id', 'product_id'), )


class ProductImage(Base):
    product_color_id = models.ForeignKey('ProductColor', on_delete=models.PROTECT)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)


class User(Base):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=256, null=True, blank=True)  # max email length = 256
    phone = models.CharField(max_length=20, null=True, blank=True)  # computed, max phone length = 15
    password = models.CharField(max_length=118)  # computed for pbkdf2:sha256 with salt_length=32

    def set_password_hash(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=32)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_email_or_and_phone",
                check=(
                        models.Q(email__isnull=False) | models.Q(phone__isnull=False)
                ),
            )
        ]


class UserAddress(Base):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)


class Review(Base):
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField(max_length=1000)  # computed


class Coupon(Base):
    is_valid = models.BooleanField(default=False)  # Coupon isn't active after creating
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, unique=True)
    discount = models.IntegerField()
    valid_until = models.DateTimeField()
    use_limit = models.IntegerField(null=True, blank=True)
    used_amount = models.IntegerField(default=0)
    categories = models.ManyToManyField('Category')


class Order(Base):
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    deliverer_id = models.ForeignKey('Deliverer', on_delete=models.SET_NULL, null=True, blank=True)
    point_id = models.ForeignKey('Point', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_date = models.DateTimeField(default=None, null=True, blank=True)
    delivery_price = models.IntegerField(default=0)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_deliverer_id_and_address_or_point_id",
                check=(
                        models.Q(deliverer_id__isnull=False, address__isnull=False, point_id__isnull=True)
                        | models.Q(deliverer_id__isnull=True, address__isnull=True, point_id__isnull=False)
                ),
            )
        ]


class OrderDetails(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_details_id = models.ForeignKey('ProductDetails', on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    discount = models.IntegerField(default=0)


class Deliverer(Base):
    name = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, unique=True)  # computed, max phone length = 15
    delivery_price = models.IntegerField()


class Point(Base):
    phone = models.CharField(max_length=20, unique=True)  # computed, max phone length = 15
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=22)  # computed (without spaces)

from django.db import models



class Promotion(models.Model):
  description = models.CharField(max_length=300)
  discount = models.FloatField


class Collection(models.Model):
  title = models.CharField(max_length=250)
  featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')



class Product(models.Model):
  title = models.CharField(max_length=255)
  # Used Charfield bacause title is going to be a small sized string
  description = models.TextField()
  # TextField is used for a large amount of text
  price = models.DecimalField(max_digits=6, decimal_places=2)
  # Used DecimalField since app is using monitary values
  # the required arguments (max_digits and decimal_places) makes sure there is only a total of 6 integers and that the decimal is moved two places from the right
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now=True)
  # DateTimeField gets the current date and time
  collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
  promotions = models.ManyToManyField(Promotion)
  slug = models.SlugField()



class Customer(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  # Used EmailField to store valid email addresses
  phone = models.CharField(max_length=100)
  birth_date = models.DateField(null=True)
  class Meta:
    db_table = 'store_customers'
    indexes = [
      models.Index(fields=['last_name', 'first_name'])
    ]



class Order(models.Model):
  PAYMENT_STATUS_PENDING = 'P'
  PAYMENT_STATUS_COMPLETE = 'C'
  PAYMENT_STATUS_FAILED = 'F'

  PAYMENT_STATUS_CHOICES = [
    (PAYMENT_STATUS_PENDING, 'Pending'),
    (PAYMENT_STATUS_COMPLETE, 'Complete'),
    (PAYMENT_STATUS_FAILED, 'Failed')
  ]
  placed_at = models.DateTimeField(auto_now_add=True)
  # Used auto_now_add arument instead of auto_now so the date is unchanged, even if it is updated
  payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
  customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
  # Using PROTECT so if customer deletes profile, I still have access to sale history



class OrderItem(models.Model):
  quantity = models.PositiveSmallIntegerField()
  # 
  unit_price = models.DecimalField(max_digits=6, decimal_places=2)
  # Added this field to keep product value at time of purchase
  order = models.ForeignKey(Order, on_delete=models.PROTECT)
  product = models.ForeignKey(Product, on_delete=models.PROTECT)



class Address(models.Model):
  street = models.CharField(max_length=270)
  city = models.CharField(max_length=270)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  zip = models.CharField(max_length=5, default="00000")



class Cart(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(
    Product, 
    on_delete=models.CASCADE
    )
  quantity = models.PositiveBigIntegerField()
from django.test import TestCase 
from api_app.models import Customer, Order 

class CustomerTest(TestCase):
    def test_customer(self):
        self.assertEquals(Customer.objects.count(), 0)
        customer = Customer(
            first_name='John', last_name='Doe', 
            email="doe@example.com", phone='+254720000000'
        )
        customer.save()
        self.assertEquals(customer.first_name, "John")

        Customer.objects.create(
            first_name='Jane', last_name='Doe', 
            email="jane@example.com", phone='+254720005000'
        )
        self.assertEquals(Customer.objects.count(), 2)

        customer.delete()
        self.assertEquals(Customer.objects.count(), 1)


class OrderTest(TestCase):
    def test_order_fields(self):
        self.assertEquals(Order.objects.count(), 0)
        Customer.objects.create(
            first_name='James', last_name='Doe', 
            email="doe@example.com", phone='+254720000000'
        )

        order = Order(
            customer=Customer.objects.get(id=1) , price=200.00,
            items = "one two three"
        )
        order.save()

        self.assertEquals(Order.objects.count(), 1)
        self.assertEquals(order.items, "one two three")

        order.delete()
        self.assertEquals(Order.objects.count(), 0)

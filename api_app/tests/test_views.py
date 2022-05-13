from unittest import mock

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny

from api_app.models import Customer, Order


@mock.patch.object(APIView, 'permission_classes', new=[AllowAny])
class CustomerApiViewTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("customer")

    def test_create_customer(self):
        self.assertEquals(Customer.objects.count(), 0)
        data = {
            'first_name': 'Jane', 
            'last_name':'Doe', 
            'email':"jane@example.com", 
            'phone':'+254720005000'
        }

        response = self.client.post(self.url, data=data, format='json')
        customer = Customer.objects.first()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Customer.objects.count(), 1)
        self.assertEquals(customer.first_name, data['first_name'])
    
    def test_get_customer_list(self):
        customer = Customer(
            first_name='John', last_name='Doe', 
            email="doe@example.com", phone='+254720000000'
        )
        customer.save()        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@mock.patch.object(APIView, 'permission_classes', new=[AllowAny])
class CustomerDetailApiViewTest(APITestCase):
    def setUp(self) -> None:
        self.customer = Customer(
            first_name='John', last_name='Doe', 
            email="doe@example.com", phone='+254720000000'
        )
        self.customer.save()
        self.url = reverse('customer-detail', kwargs={'pk': self.customer.pk})

    def test_get_customer_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        self.assertEquals(data['id'], self.customer.pk)
        self.assertEquals(data['first_name'], self.customer.first_name)
        self.assertEquals(data['last_name'], self.customer.last_name)
        self.assertEquals(data['phone'], self.customer.phone)

    def test_get_nonexistent_customer(self):
        response = self.client.get("/customer/255/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        data['first_name'] = 'Mason'
        data['last_name'] = 'Mount'
        data['phone'] = '+254725156987'
        response = self.client.put(self.url, data=data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.customer.refresh_from_db()
        self.assertEquals(data['first_name'], self.customer.first_name)
        self.assertEquals(data['last_name'], self.customer.last_name)
        self.assertEquals(data['phone'], self.customer.phone)

    def test_delete_customer(self):
        self.assertEquals(Customer.objects.count(), 1)

        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Customer.objects.count(), 0)


@mock.patch.object(APIView, 'permission_classes', new=[AllowAny])
class OrderApiViewTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("order")
        self.customer = Customer(
            first_name='James', last_name='Doe', 
            email="doe@example.com", phone='+254720000000'
        )
        self.customer.save()
    
    def test_create_order(self):
        self.assertEquals(Order.objects.count(), 0)
        data = {
            'customer' : self.customer.id,
            'items' : 'laptop, desktop and monitor',
            'price' : 20000
        }

        response = self.client.post(self.url, data=data, format='json')
        order = Order.objects.first()
        self.assertEquals(Order.objects.count(), 1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(order.price, data['price'])

    def test_get_order_list(self):
        data = {
            'customer' : self.customer.id,
            'items' : 'laptop, desktop and monitor',
            'price' : 20000
        }
        self.client.post(self.url, data=data, format='json')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@mock.patch.object(APIView, 'permission_classes', new=[AllowAny])
class OrderDetailApiViewTest(APITestCase):
    def setUp(self) -> None:        
        Customer.objects.create(
            first_name='James', last_name='Doe', 
            email="doe@example.com", phone='+254720000000'
        )
        
        self.order = Order(
            customer=Customer.objects.get(id=1),
            price='3695200.00',
            items='BMW, Honda, Mazda'
        )
        self.order.save()

        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_get_order_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        self.assertEquals(data['id'], self.order.pk)
        self.assertEquals(data['price'], self.order.price)
        self.assertEquals(data['customer'], self.customer.id)

    def test_get_nonexistent_order(self):
        response = self.client.get("/order/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        data['price'] = 2651582.00
        data['items'] = 'Lenovo, HP, Dell and Samsung'
        response = self.client.put(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.order.refresh_from_db()
        self.assertEquals(data['price'], self.order.price)
        self.assertEquals(data['customer'], self.customer.id)

    def test_delete_order(self):
        self.assertEquals(Order.objects.count(), 1)

        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Order.objects.count(), 0)
        
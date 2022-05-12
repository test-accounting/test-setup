import os
import dotenv
import logging
from pathlib import Path

import africastalking

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from api_app.models import Customer, Order
from api_app.serializers import CustomerSerializer, OrderSerializer


"""find environment files"""
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

logger = logging.getLogger(__name__)

africastalking.initialize(
    username='sandbox',
    api_key=os.environ['APIKEY']
)


class HomeView(LoginRequiredMixin, View):

    """HomeView."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get."""
        sessionid = request.COOKIES['sessionid']
        session = Session.objects.get(pk=sessionid)
        session_data = session.get_decoded()

        return render(request, 'home/index.html', {
            'settings': settings,
            'session_data': session_data,
        }, status=200)


class CustomerApiView(APIView):    
    def get(self, request):
        object_list = Customer.objects.all()
        serializer = CustomerSerializer(object_list, many=True)
        return Response(
            {"status" : "success", "data" : serializer.data},
            status = status.HTTP_200_OK
        )

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"status" : "Error","data" : serializer.errors},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {"status" : "success","data" : serializer.data},
            status = status.HTTP_201_CREATED
        )


class CustomerDetailApiView(APIView):
    def get_customer(self, pk):
        customer = get_object_or_404(Customer, id=pk)
        return customer

    def get(self, request, pk, *args, **kwargs):
        customer_instance = self.get_customer(pk)
        serializer = CustomerSerializer(customer_instance)
        return Response(
            {"status": "success", "data": serializer.data},
            status = status.HTTP_200_OK,
        )

    def put(self, request, pk):
        customer = self.get_customer(pk)
        if not customer:
            return Response(
                {"status": "Object with that id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializers = CustomerSerializer(instance=customer, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            {"status": "item updated", "data": serializers.data},
            status = status.HTTP_200_OK
        )

    def delete(self, request, pk):
        customer = self.get_customer(pk)
        customer.delete()
        return Response(
            {"status": "item deleted"},
            status = status.HTTP_204_NO_CONTENT
        )


class OrderApiView(APIView):
    sms = africastalking.SMS

    def get(self, request):
        object_list = Order.objects.all()
        serializer = OrderSerializer(object_list, many=True)
        return Response(
            {"status" : "success", "data" : serializer.data},
            status = status.HTTP_200_OK
        )

    def post(self, request):
        serializers = OrderSerializer(data=request.data)

        if not serializers.is_valid():
            return Response(
                {"status" : "Error","data" : serializers.errors},
                status = status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = CustomerDetailApiView().get_customer(pk=request.data.get('customer'))
            recipient = [customer.phone]
            message = f"Hello {customer}, your order has been created successfully!"
            sender = '15015'
            response = self.sms.send(message, recipient, sender)
            logger.warning(f"\nMessage sent successfully")
        except Exception as e:
            logger.critical(f'We have a problem: {e}')

        serializers.save()
        return Response(
            {"status" : "success","data" : serializers.data},
            status = status.HTTP_201_CREATED
        )


class OrderDetailApiView(APIView):
    def get_order(self, pk):
        order = get_object_or_404(Order, id=pk)
        return order

    def get(self, request, pk, *args, **kwargs):
        order_instance = self.get_order(pk)
        serializer = OrderSerializer(order_instance)
        return Response(
            {"status": "success", "data": serializer.data},
            status = status.HTTP_200_OK,
        )

    def put(self, request, pk):
        order = self.get_order(pk)
        if not order:
            return Response(
                {"status": "Object with that id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializers = OrderSerializer(instance=order, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            {"status": "item updated", "data": serializers.data},
            status = status.HTTP_200_OK
        )

    def delete(self, request, pk):
        order = self.get_order(pk)
        order.delete()
        return Response(
            {"status": "item deleted"},
            status = status.HTTP_204_NO_CONTENT
        )
        
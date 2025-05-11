from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View
from django.core.mail import send_mail
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart
from django.contrib.contenttypes.models import ContentType


class OrderCreateView(View):
    template_name = 'order/create.html'

    def get(self, request):
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            session_cart_id = request.session.get('cart_id')
            cart = get_object_or_404(Cart, id=session_cart_id) if session_cart_id else None

        if not cart or not cart.cartitem_set.exists():
            return redirect('cart:cart')

        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
        return render(request, self.template_name, {'cart': cart, 'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            session_cart_id = request.session.get('cart_id')
            cart = get_object_or_404(Cart, id=session_cart_id) if session_cart_id else None

        if not cart or not cart.cartitem_set.exists():
            return redirect('cart:cart')

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            content_type = ContentType.objects.get_for_model(cart.cartitem_set.first().product)
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    content_type=content_type,
                    object_id=item.object_id,
                    product=item.product,
                    price=item.product.get_discounted_price(),
                    quantity=item.quantity
                )

            subject = f'Підтвердження замовлення #{order.id}'
            message = (
                f'Дякуємо за ваше замовлення!\n\n'
                f'Номер замовлення: {order.id}\n'
                f'Загальна сума: {order.get_total_cost()} грн\n'
                f'Адреса доставки: {order.address}, {order.city}, {order.postal_code}\n\n'
                f'Ви можете переглянути деталі за посиланням: '
                f'http://127.0.0.1:8000/order/detail/{order.id}/'
            )
            send_mail(
                subject,
                message,
                'justanothermailidhwhoiam@gmail.com',
                [order.email],
                fail_silently=False,
            )

            cart.cartitem_set.all().delete()
            if not request.user.is_authenticated:
                request.session['cart_id'] = None

            return render(request, 'order/created.html', {'order': order})
        return render(request, self.template_name, {'cart': cart, 'form': form})

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset
    
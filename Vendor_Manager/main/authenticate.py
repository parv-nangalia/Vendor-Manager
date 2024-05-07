from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from rest_framework.permissions import IsAuthenticated



class HomepageAPIView(APIView):

    def get(self, request):
        url_data = {
            'Vendor': 'http://127.0.0.1:8000/api/vendor/',
            'Vendor-details': 'http://127.0.0.1:8000/api/vendor/0/'   "# cannot be used without correct id present in db",
            'Vendor-performance': 'http://127.0.0.1:8000/api/vendor/0/performance/'   "# cannot be used without correct id present in db",
            'Purchase_orders': 'http://127.0.0.1:8000/api/purchase_orders/',
            'Purchase_orders-details': 'http://127.0.0.1:8000/api/purchase_orders/0/' "# cannot be used without correct id present in db",
            'Purchase_orders-acknowledge': 'http://127.0.0.1:8000/api/purchase_orders/0/acknowledge/' "# cannot be used without correct id present in db",
            'Signup': 'http://127.0.0.1:8000/signup',
            'Login': 'http://127.0.0.1:8000/login',
            'Logout': 'http://127.0.0.1:8000/logout',

        }
        return Response(url_data, status=status.HTTP_200_OK)


class SignupAPIView(ObtainAuthToken):
    def get(self, request):
        url='http://127.0.0.1:8000/login'
        name = "Login"
        form = UserCreationForm()  # Instantiate your Django form
        return render(request, 'form.html', {'form': form, 'url':url, 'name': name })

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password1')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        # token, _ = Token.objects.get_or_create(user=user)
        # return Response({'token': token.key})
        # response = Response({'token': token.key})

        # # Set token in response headers
        # response['Authorization'] = f'Token {token.key}'

        # Redirect user to a different URL
        return redirect('login')


class LoginAPIView(ObtainAuthToken):
    def get(self, request):
        url='http://127.0.0.1:8000/signup'
        name = "Signup"
        form = AuthenticationForm()  # Instantiate your Django form
        return render(request, 'form.html', {'form': form, 'url':url, 'name': name  })


    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate or retrieve token for the user
            # token, _ = Token.objects.get_or_create(user=user)

            # # Set the token in an HTTP-only cookie
            # # response = HttpResponse('Login successful')
            # response = JsonResponse({'message': 'Login successful'})
            # response.set_cookie('auth_token', token)
            # return response
            login(request, user)
            return redirect('/')

        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.COOKIES['auth_token'] = ''
        logout(request)
        response = Response("Logged out successfully.")
    
    # Redirect shortly
        response['Refresh'] = '3; url=/'  # Redirect to '/new-page/' after 3 seconds
    
        return response
        # return Response({'success': 'Logged out successfully'})

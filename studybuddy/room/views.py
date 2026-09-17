from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

from .models import Message, Room, Topic

from .serializer import RoomSerializer, UserSerializer, MessageSerializer


def home(request):
    topics = Topic.objects.all()
    rooms = Room.objects.select_related('topic', 'host').all()
    return render(request, 'home.html', {'topics': topics, 'rooms': rooms})


def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    topics = Topic.objects.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(user=request.user, room=room, body=body)
        return redirect('room-detail', slug=room.slug)

    return render(request, 'room_detail.html', {'room': room, 'topics': topics})


def create_room_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    topics = Topic.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        topic_name = request.POST.get('topic', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            messages.error(request, 'Room name is required.')
            return render(request, 'create_room.html', {'topics': topics})

        topic = None
        if topic_name:
            topic, _ = Topic.objects.get_or_create(name=topic_name)

        slug = slugify(name)
        unique_slug = slug
        suffix = 1
        while Room.objects.filter(slug=unique_slug).exists():
            suffix += 1
            unique_slug = f'{slug}-{suffix}'

        room = Room.objects.create(
            name=name,
            host=request.user,
            topic=topic,
            slug=unique_slug,
            description=description,
        )
        return redirect('room-detail', slug=room.slug)

    return render(request, 'create_room.html', {'topics': topics})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email', '')
            user.save()
            login(request, user)
            return redirect('home')
        for error_list in form.errors.values():
            for error in error_list:
                messages.error(request, error)

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')



class roomListCreate(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        host = self.request.user
        if (serializer.is_valid):
            serializer.save(host=host)
        else :
            return serializer.errors

class messageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return Message.objects.filter(id=room_id)

    def perform_create(self, serializer):
        user = self.request.user
        room_id = self.kwargs.get('room_id')

        if (serializer.is_valid):
            serializer.save(user=user)


class createUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
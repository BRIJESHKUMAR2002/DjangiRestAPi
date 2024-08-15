from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Task, TaskMember
from .serializers import TaskSerializer, TaskMemberSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskMemberAddRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id, owner=request.user)
        user = User.objects.get(id=request.data.get('user_id'))
        TaskMember.objects.create(task=task, user=user)
        return Response({'status': 'member added'}, status=status.HTTP_201_CREATED)

    def delete(self, request, task_id):
        task = Task.objects.get(id=task_id, owner=request.user)
        user = User.objects.get(id=request.data.get('user_id'))
        TaskMember.objects.filter(task=task, user=user).delete()
        return Response({'status': 'member removed'}, status=status.HTTP_204_NO_CONTENT)


class TaskMemberListView(generics.ListAPIView):
    serializer_class = TaskMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return TaskMember.objects.filter(task_id=task_id, task__owner=self.request.user)


class UpdateTaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id, owner=request.user)
        task.status = request.data.get('status')
        task.save()
        return Response({'status': 'task status updated'}, status=status.HTTP_200_OK)

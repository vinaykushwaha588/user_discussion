from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from .models import User, Discussion
from .serializers import UserSerializers, DiscussionSerializers

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'pk'

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            data = request.data.copy()
            serializer = UserSerializers(data= data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success':True, 'message': "User Created Successfully."}, status=status.HTTP_201_CREATED)
            return Response({'success':False, 'message': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'success':False, 'error': err.args[0]})
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        try:
            data = request.data.copy()
            email = data.get('email', None)
            password = data.get('password', None)
            user = authenticate(request, username=email, password=password)

            if not user:
                raise AuthenticationFailed('Invalid Credentials.')

            if user is not None:
                return Response({
                    'access': user.tokens()['access'],
                    'refresh': user.tokens()['refresh'],
                }, status=status.HTTP_200_OK)

            return Response({'success':False, 'message':"Invalid Credentials."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"success":False, 'error': err.args[0]})
    

    @action(detail=False, methods=['get'])
    def user_list(self, request):
        queryset = User.objects.all().values('id', 'name', 'email', 'mobile', 'created_at', 'updated_at')
        return Response({'success':True, 'data': queryset}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search_user(self, request):
        name = self.request.query_params.get('name', None)
        user = User.objects.filter(name__startswith=name)
        if user.exists():
            serializer = user.values('id', 'name', 'email', 'mobile', 'created_at', 'updated_at')
            return Response({'success': True, 'data':serializer}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message':'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
            

    def update(self, request, pk,*args, **kwargs):
        try:
            user = self.request.user
            print('user', user.id)
            data = self.request.data.copy()
            mobile_no = data.get('mobile', None)
            instance = User.objects.get(pk= pk)
            if instance.mobile == mobile_no:
                data.pop('mobile')
            serializer = self.get_serializer(instance, data=data,context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": True, 'message': "User Updated Successfully."}, status=status.HTTP_200_OK)
            return Response({"success": False, 'message': serializer.error_messages},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'success': False, 'error': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'success': True, 'message': "User Deleted Successfully."}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializers
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['post'])
    def add(self, request):
        try:
            user = request.user
            data = request.data.copy()
            serializer = DiscussionSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user)
                return Response({'success':True, 'message':"Discussion Created Successfuly."}, status=status.HTTP_201_CREATED)
            return Response({'success':False, 'message':serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'success': False, 'error': err.args[0]})
        
    @action(detail=False, methods=['get'])
    def list_by_hashtag(self, request):
        try:
            hashtag = self.request.query_params.get('hashtag', None)
            if not hashtag:
                raise ValueError('Hastag is required.')
            queryset = Discussion.objects.filter(hashtags__icontains=hashtag)
            if queryset.exists():
                serializer = DiscussionSerializers(queryset, many=True).data
            return Response({'success':True, 'data':serializer}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'success': False, 'error': err.args[0]})
    
    @action(detail=False, methods=['get'])
    def list_by_text(self, request):
        try:
            text = self.request.query_params.get('text', None)
            if not text:
                raise ValueError('Text is required.')
            queryset = Discussion.objects.filter(text__icontains=text)
            if queryset.exists():
                serializer = DiscussionSerializers(queryset, many=True).data
            return Response({'success':True, 'data':serializer}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'success': False, 'error': err.args[0]})
        

    def update(self, request, pk,*args, **kwargs):
        try:
            data = self.request.data.copy()
            instance = Discussion.objects.get(pk= pk)
            serializer = self.get_serializer(instance, data=data,context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": True, 'message': "Discussion Updated Successfully."}, status=status.HTTP_200_OK)
            return Response({"success": False, 'message': serializer.error_messages},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'success': False, 'error': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'success': True, 'message': "Discussion Deleted Successfully."}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': "Not Found."}, status=status.HTTP_403_FORBIDDEN)
    
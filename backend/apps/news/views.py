from apps.news.models import News
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.models import User
from .models import News
from .serializers import (StoriesCreateSerializer,ListImageSerializer,StoriesUniqueSerializer,StoriesWebSerializer)
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser, FormParser
from apps.media.models import Media
from apps.media.serializers import MediaSerializer
from django.core.exceptions import ObjectDoesNotExist

class UpdateLike(APIView):
    permission_classes =[IsAuthenticated]
    def message(self,message,status,data):
        response = {
                "message":message, 
                "status":status,
                "data" : data
            }
        return response

    def get_obj(self,pk):
        try:
            news= News.objects.get(pk=pk)
            return news 
        except ObjectDoesNotExist:
            return None

    def put(self, request,pk):
        data = request.data
        news = self.get_obj(pk)
        if (news is None):
            res = self.message("News doesn't exist",status.HTTP_404_NOT_FOUND,[])
            Response(res,status= res['status'])
        else:
            if(data['like']):
                news.likes = news.likes+1
            else:
                if(news.likes == 0):
                    news.likes =0
        serializer = StoriesWebSerializer(news)
        res = self.message("",status.HTTP_200_OK,serializer.data)
        return Response(res,status= res["status"])
            

class CreateNews(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes =[IsAuthenticated]

    def message(self,message,status,data):
        response = {
                "message":message, 
                "status":status,
                "data" : data
            }
        return response
    
    def get(self, request):
        snippets = News.objects.filter(user=request.user)
        serializer = StoriesWebSerializer(snippets, many=True)
        res = self.message("",status.HTTP_200_OK,serializer.data)
        return Response(res,status= res["status"])


    def post(self, request):
        data = request.data
        if(data['image']== "" or data['image'] is None ):
            data={"title":data["title"],"description":data["description"]}

        serializer = StoriesCreateSerializer(data=data)
        media = []
        new = ""
        if(serializer.is_valid()):
            requested = {'title':data['title'],'description':data['description']}
            serializer_create = StoriesUniqueSerializer(data= requested) 

        else:
            res = self.message("Error archivo media no válido",status.HTTP_202_ACCEPTED,serializer.errors)
            return Response(res,status= res["status"])

        if(serializer_create.is_valid()):
            data1 = serializer_create.validated_data
            new =News.objects.create(user=request.user,**data1)   
            print("News", new)
        
        else:
            res = self.message("Error revise el formato", 
            status.HTTP_202_ACCEPTED,serializer_create.errors)
            return Response(res,status= res["status"])

        if('image' in data):
            a= dict((request.data).lists())['image']
            data_image = {"image":a}
            serializer_m = ListImageSerializer(data= data_image)
            if(serializer_m.is_valid() and len(a)<4):
                media = Media.objects.bulk_create([Media(image=x) for x in a])
                print(media)
            else:
                res = self.message("Error el numero maximo de imagenes es 3", status.HTTP_202_ACCEPTED,"")
                return  Response(res, res['status'])

        if('image' in data):
            for x in range(len(media)):
                new.image.add(media[x].pk)
        serializer_res = StoriesUniqueSerializer(new)
        res = self.message("Noticia Creada Exitosamente", 
        status.HTTP_201_CREATED,serializer_res.data)
        return Response(res,status= res["status"])


# Create your views here.

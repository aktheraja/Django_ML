from django.shortcuts import render

# Create your views here.
from .serializers import PostSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from keras.models import load_model
import numpy as np
import cv2
from matplotlib import pyplot as plt
import urllib.request
import time
import os
from django.conf import settings





class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PredictView(APIView):
    def post(self, request, *args, **kwargs):
        cascade = cv2.CascadeClassifier('./post/haarcascade_frontalface_default.xml')
        model = load_model("./post/CNN-final-model-v3.h5")
        my_files=[f.name for f in os.scandir('./media/post_images/') if f.is_file()]
        for file in my_files:
            print(file)
            img = cv2.imread('./media/post_images/'+file)
            font = cv2.FONT_HERSHEY_COMPLEX
            crop_margin = 0.2
            height, width, _ = img.shape
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)
            person_num = 0
            for (x,y,w,h) in faces:
                person_num += 1

                x1 = int(x - crop_margin * w)
                y1 = int(y - crop_margin * h)
                x2 = int(x + (1 + crop_margin) * w)
                y2 = int(y + (1 + crop_margin) * h)

                if x1 < 0:
                    x1 = 0
                if y1 < 0:
                    y1 = 0
                if x2 > width:
                    x2 = width
                if y2 > height:
                    y2 = height


                crop_img = gray_img[y1:y2, x1:x2]
                try:
        #           print(f'Processing face #{person_num}: ({x1},{y1}),({x2},{y2})')
                    resized_normalized = cv2.resize(crop_img, (100, 100))/255

                    for_predict = resized_normalized.reshape(-1,100,100,1)
                    start = time.time()
                    prediction = model.predict(for_predict)[0][0]
                    end = time.time()
                    print(f"Inference: {end-start} seconds")

                    if (prediction >= 0.5):
                        text = f'M({prediction:.2f})'
                        cv2.rectangle(img, (x1,y1), (x2, y2), (255,0,0), 2)
                        cv2.putText(img, text, (x,y), font, w/140, (255,200,0), 2, cv2.LINE_AA)
                    else:
                        text = f'F({prediction:.2f})'
                        cv2.rectangle(img, (x1,y1), (x2, y2), (55,105,180), 2)
                        cv2.putText(img, text, (x,y), font, w/140, (255,200,0), 2, cv2.LINE_AA)


                except:
        #           print(f'Image({width},{height}) failed to crop face #{person_num}: ({x1},{y1}),({x2},{y2})')
                    pass
            cv2.imwrite( "./media/out.jpg", img )

            return Response("./media/get_images/out.jpg", status=status.HTTP_201_CREATED)


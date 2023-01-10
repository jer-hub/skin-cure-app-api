from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from tensorflow import keras
import tensorflow as tf
import numpy as np
from guest_user.decorators import allow_guest_user
from guest_user.models import Guest
from .models import Profile, Result
from .auth import SessionCsrfExemptAuthentication, ignore_csrf
from rest_framework.authentication import BasicAuthentication
from .serializers import ResultSerializer

@allow_guest_user
@api_view(http_method_names=["GET"])
def guestview(request):
    guest, createdGuest = Guest.objects.get_or_create(user__id=request.user.id)
    getProfile, createdProfile = Profile.objects.get_or_create(guest=guest)
    results = Result.objects.all()
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data)

def guestview2(request):
    guest, createdGuest = Guest.objects.get_or_create(user__username=request.user.username)
    getProfile, createdProfile = Profile.objects.get_or_create(user=guest)
    return HttpResponse(f"success!{request.user}")

class ProfileView(APIView):
    authentication_classes = (SessionCsrfExemptAuthentication, BasicAuthentication)
    
    def get(self, request):
        results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        guest = Guest.objects.get(user__username=request.user.username)
        profile = Profile.objects.get(guest=guest)
        result = Result()
        result.profile = profile
        result.description = self.request.POST['description']
        result.age = self.request.POST['age']
        result.sex = self.request.POST['sex']
        result.skin_disease = self.request.POST['result']
        result.accuracy = self.request.POST['acc']
        result.pic = self.request.FILES['image']
        result.save()
        return Response({"profile": profile.guest.user.username})


@api_view(http_method_names=["DELETE"])
@ignore_csrf
def delProfile(request):
    profile = Result.objects.get(id=request.data['id'])
    profile.delete()
    results = Result.objects.all()
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@ignore_csrf
def predictCase(request):
    if request.method == 'POST':
        image = request.FILES['image']
        file_name = default_storage.save('images/' + image.name, ContentFile(image.read()))
        file_url = default_storage.url(file_name)
        preprocessed = tf.keras.preprocessing.image.load_img(file_url[1:])
        resizedImage = tf.image.resize(preprocessed, (224, 224))
        resizedImage = resizedImage / 255
        input_arr = tf.keras.preprocessing.image.img_to_array(resizedImage)
        input_arr = np.array([input_arr])  # Convert single image to a batch.
        model = keras.models.load_model('./ml_models/final_model.h5')
        labels = {0: 'Acne', 1: 'Basal Cell', 2: 'Eczema', 3: 'Normal', 4: 'Wartz'}
        predictions = model.predict(input_arr)
        accuracy = predictions.copy()
        predictions = np.argmax(predictions)
        print("Result: ",labels[predictions], "Accuracy: ", np.amax(accuracy))
    return Response({"prediction": labels[predictions], "accuracy": np.amax(accuracy)})
from django.shortcuts import render, redirect
from .forms import UploadFileForm
import pickle
import numpy as np
from tensorflow import keras
from django.core.cache import caches

reconstructed_model = keras.models.load_model("main/lstm.h5")

def handle_uploaded_file(f):
    try:
        with open('name.data', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        with open('name.data', 'rb') as filehandle:  
        # сохраняем данные как двоичный поток
            placesList = pickle.load(filehandle)
        res = reconstructed_model.predict(np.array([placesList]))
        classes = np.argmax(res, axis=-1)
        classes = classes + 1
        return (res, classes)
    except pickle.UnpicklingError as e:
        return ('Ошибка', 'Выберите верный формат или название файла')
    except:
        return ('Ошибка', 'Выберите файл в котором одна запись')


   


def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        res = handle_uploaded_file(file)
        caches['res'] = res
        return redirect('home')
    else:
        try:
            res = caches['res']
        except:
            res = (0, 0)
        form = UploadFileForm()
        return render(request, 'main/home.html', {'form': form, 'ver': res[0], "class": res[1]})

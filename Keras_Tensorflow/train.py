
#Develop the model
import tensorflow as tf
import keras
from resnet152 import ResNet152
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
import wget

model = ResNet152(weights='imagenet')

#model.summary( )

wget.download('https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg')

img_path = '220px-Lynx_lynx_poing.jpg'
#print(Image.open(img_path).size)
Image.open(img_path)

img = image.load_img(img_path, target_size=(224, 224))
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = preprocess_input(img)

preds = model.predict(img)
print('Predicted:', decode_predictions(preds, top=3))
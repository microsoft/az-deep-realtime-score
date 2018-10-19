def init():
    import tensorflow as tf
    from resnet152 import ResNet152
    from keras.preprocessing import image
    from keras.applications.imagenet_utils import preprocess_input, decode_predictions

    import numpy as np
    import timeit as t
    import base64
    import json
    from PIL import Image, ImageOps
    from io import BytesIO
    import logging

    global model
    model = ResNet152(weights='imagenet')
    print('Model loaded')
    
def run(img_path):
    
    import tensorflow as tf
    from resnet152 import ResNet152
    from keras.preprocessing import image
    from keras.applications.imagenet_utils import preprocess_input, decode_predictions

    import numpy as np
    import timeit as t
    import base64
    import json
    from PIL import Image, ImageOps
    from io import BytesIO
    import logging   
    
    model = ResNet152(weights='imagenet')
    print('Model loaded')
  
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    
    preds = model.predict(img)
    print('Predicted:', decode_predictions(preds, top=3))    
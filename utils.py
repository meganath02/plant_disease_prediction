
import numpy as np
from PIL import Image
import json
from tensorflow.keras.models import load_model
from googletrans import Translator

# Load model and class indices once
model = load_model("plant_disease_model.h5")
class_indices = json.load(open("class_indices.json"))
index_to_class = {int(k): v for k, v in class_indices.items()}  # ensure integer keys

# Preprocess uploaded image
def preprocess_image(image, target_size=(224, 224)):
    img = Image.open(image)
    img = img.resize(target_size)
    img_array = np.array(img)
    if img_array.shape[-1] == 4:  # If PNG with alpha channel
        img_array = img_array[:, :, :3]
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('float32') / 255.
    return img_array

# Predict function
def predict(image):
    preprocessed = preprocess_image(image)
    prediction = model.predict(preprocessed)
    class_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction)) * 100
    class_name = index_to_class[class_index]
    return class_name, confidence

# Translation helper
def translate_text(text, dest_lang='en'):
    if dest_lang == "en":
        return text
    try:
        translator = Translator()
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        print("Translation error:", e)
        return text
    
    
with open("disease_resources.json", "r") as f:
    disease_resources = json.load(f)

def get_disease_resource(disease_name):
    return disease_resources.get(disease_name, {
        "video": "",
        "description": "No information available for this disease yet."
    })

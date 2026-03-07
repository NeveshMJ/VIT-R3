import gradio as gr
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import os

# Reduce TF log spam
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# 1. Load your trained model
model = load_model("civic_model.h5")
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")

# 2. Define classes and threshold (Exactly from your predict.py)
class_names = [
    "garbage",
    "pothole",
    "stagnant_water",
    "streetlight_damage"
]
CONFIDENCE_THRESHOLD = 0.60

# 3. Your awesome department mapping function!
def map_department(issue):
    mapping = {
        "pothole": "Road Department",
        "garbage": "Sanitary Department",
        "stagnant_water": "Water Department",
        "streetlight_damage": "Electrical Department"
    }
    return mapping.get(issue, "General")

# 4. The main prediction function
def predict_issue(img):
    if img is None:
        return "Error: No image provided"

    # Resize image to match your training (224x224)
    img = img.resize((224, 224))
    
    # Convert to array and preprocess for MobileNetV2
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array) # MUST have this for MobileNetV2!

    # Predict
    preds = model.predict(img_array, verbose=0)
    idx = int(np.argmax(preds))
    confidence = float(np.max(preds))
    predicted_class = class_names[idx]

    # Check confidence threshold
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "issue": "Uncertain - Manual Review Needed",
            "department": "Admin",
            "confidence": round(confidence, 2)
        }

    # Return the formatted result
    return {
        "issue": predicted_class,
        "department": map_department(predicted_class),
        "confidence": round(confidence, 2)
    }

# 5. Create the Gradio interface
demo = gr.Interface(
    fn=predict_issue,
    inputs=gr.Image(type="pil"), # Accepts image uploads
    outputs=gr.JSON(),           # Outputs clean JSON for your frontend to read
    title="Civic Issue API"
)

# Launch it!
if __name__ == "__main__":
    demo.launch()
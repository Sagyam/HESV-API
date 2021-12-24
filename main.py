from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from numpy.core.fromnumeric import shape
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import cv2


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("models/19_class.h5")

CLASS_NAMES = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "Add",
    "Decimal",
    "Division",
    "Equals",
    "Multiply",
    "Minus",
    "X",
    "Y",
    "Z",
]


@app.get("/")
def root():
    return {"message": "Hello World"}


def read_file_as_image(data) -> np.ndarray:
    return Image(BytesIO(data))


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())

    image = np.expand_dims(image, axis=0)
    image = image.astype('float32')/255

    predictions = MODEL.predict(image)

    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence = np.max(predictions)*100
    return {
        'class': predicted_class,
        'confidence': int(confidence),


    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

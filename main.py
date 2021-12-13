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

MODEL = tf.keras.models.load_model("models/17class.h5")

CLASS_NAMES = ['+',
               '-',
               '0',
               '1',
               '2',
               '3',
               '4',
               '5',
               '6',
               '7',
               '8',
               '9',
               '=',
               'X',
               'div',
               'Y',
               'Z']


@app.get("/")
def root():
    return {"message": "Hello World"}


def read_file_as_image(data) -> np.ndarray:
    return np.array(Image.open(BytesIO(data)))


def process_img(image):
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.erode(image, kernel, iterations=1)
    image = cv2.resize(dilation, (45, 45))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence = np.max(predictions)
    return {
        'class': predicted_class,
        'confidence': float(confidence),


    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

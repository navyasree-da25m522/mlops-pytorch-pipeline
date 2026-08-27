import io
import os
from pathlib import Path
import torch
from fastapi import FastAPI, File, UploadFile
from torchvision import transforms
from PIL import Image
from src.model import get_model


app = FastAPI(title="PyTorch Image Classifier")


CHECKPOINT_PATH = os.getenv("MODEL_PATH","/app/checkpoints/classifier_v1.pt",)

model = None

def load_model():
    global model
    checkpoint_path = Path(CHECKPOINT_PATH)
    if not checkpoint_path.exists():
        raise FileNotFoundError( f"Model checkpoint not found: {checkpoint_path}" )

    model = get_model(num_classes=10)
    checkpoint = torch.load( checkpoint_path,map_location="cpu",)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

@app.on_event("startup")
def startup_event():
    load_model()

@app.get("/health")
def health():
    if model is None:
        return {"status": "unhealthy"}
    return {"status": "healthy"}

@app.post("/predict")
async def predict(image: UploadFile = File(...)):

    if model is None:
        return {"error": "Model is not loaded"}
    image_bytes = await image.read()
    input_image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.4914, 0.4822, 0.4465],
            std=[0.2470, 0.2435, 0.2616],
        ),
    ])

    input_tensor = transform( input_image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs,dim=1,)[0]

    return {"probabilities": probabilities.tolist()}
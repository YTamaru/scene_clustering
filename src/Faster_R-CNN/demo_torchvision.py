import torch
import torchvision
from PIL import Image
import numpy as np

if __name__ == "__main__":
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    image = "/home/tamaru/scene_categorize/main/data/insta_cube/lab/lab_desk_table/0/lab_desk_table_0_img_000000.png"
    img = Image.open(image)
    img = img.convert("RGB")
    img  = np.array(img)
    img = torch.from_numpy(img)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    img = img.to(device)
    print(img.shape)
    predictions = model(img)

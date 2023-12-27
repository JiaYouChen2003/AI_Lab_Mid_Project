'''
model = tarot_model()
# box: xxyy, confidence, label
box = model.run(img)
'''
import torch
from PIL import Image

from yolov3.transforms import preprocess
from yolov3.models import YOLOs
from yolov3.utils import nms

class tarot_model():
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = YOLOs["yolov3"](10).to(self.device)
        ckpt = torch.load("./ckpt100000.pt")
        self.model.load_state_dict(ckpt['model'])
        self.model.eval()

    def run(self, img):
        img = Image.fromarray(img)
        img, _ = preprocess(img)
        img = img.unsqueeze(0)

        with torch.no_grad():
            img= img.to(self.device)
            bboxes = self.model(img)
            bboxes = nms(bboxes, 0.5, 0.45)[0]
            bboxes[:, 0:4] = bboxes[:, 0:4] / 416
        return bboxes
'''
model = tarot_model()
# box: xxyy confidence, label
box = model.run(img)
'''
import torch
import numpy as np
from PIL import Image

from yolov3.transforms import preprocess
from yolov3.models import YOLOs
from yolov3.utils import nms

from pycocotools.coco import COCO
from yolov3.dataset import DetectionDataset

class tarot_model():
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = YOLOs["yolov3"](10).to(self.device)
        ckpt = torch.load("./ckpt100000.pt")
        self.model.load_state_dict(ckpt['model'])
        self.model.eval()
        # The class names and colors can be obtained from dataset.
        dataset = DetectionDataset(
            COCO("./label_ver_1.json"),
            img_root=None,
            img_size=None,
            transforms=None)
        self.label2name = dataset.label2name
        self.label2color = dataset.label2color

    def run(self, img):
        img = Image.fromarray(img)
        orig_size = torch.tensor([img.size[1], img.size[0]]).long()
        img, _ = preprocess(img)
        img = img.unsqueeze(0)

        with torch.no_grad():
            img, orig_size = img.to(self.device), orig_size.to(self.device)
            bboxes = self.model(img)
            bboxes = nms(bboxes, 0.5, 0.45)[0]
        return bboxes
# AI_Lab_Mid_Project
* NYCU Human Centric Computing Lab, Permanent course number: EEEC20006
* Introduction \
This is a project that train a model to detect tarot card images by yolov3. The model will be put on a drone and we will write a rule based code to let the drone approach the tarot card. The goal is to touch as many tarot cards as possible in a given time. \
As a result, our model have a really high accuracy on detecting exist tarot cards. However, in the examination, we didn't manage to control our drone well and only touched three tarot out of seven(42.85%) within 15 minutes. Good news is that we changed the path of our drone a bit and touched all of the tarot in the second 15 minutes.

# Contents
- [AI_Lab_Mid_Project](#AI_Lab_Mid_Project)
- [Contents](#contents)
- [Set Up](#set-up)
- [Result](#result)

# Set Up
## Download
```bash
git clone https://github.com/JiaYouChen2003/AI_Lab_Mid_Project.git
```

## Build Environment
```bash
conda create -n AI_Lab_Mid_Project python=3.9
conda activate AI_Lab_Mid_Project
pip install -r requirements.txt
```

## How to run the project
```bash
conda python main.py
```
## Data
* Tarot training data
    * Training images
        * Version 0, 1: [images](https://drive.google.com/drive/folders/1BFJMue5FtOIt0e_bLsHMeyu8z_tA4O0I?usp=share_link)
        * Version 2 addition: [images_ver_2_addition](https://drive.google.com/drive/folders/10XiLDAtooAQ9CZxXtXsQih4YjWQZyGCT?usp=share_link)
        * Version 2.1 addition: [images_ver_2_1_addition](https://drive.google.com/drive/folders/18ey2_-nPYCYvQaNcwsVYy1dDCwLvBzlg?usp=share_link)
    * Label
        * Version 0: [label_ver_0.json](https://github.com/JiaYouChen2003/AI_Lab_Mid_Project/blob/main/label_ver_0.json)
        * Version 1: [label_ver_1.json](https://github.com/JiaYouChen2003/AI_Lab_Mid_Project/blob/main/label_ver_1.json)
        * Version 2: [label_ver_2.json](https://github.com/JiaYouChen2003/AI_Lab_Mid_Project/blob/main/label_ver_2.json)
        * Version 2.1: [label_ver_2_1.json](https://github.com/JiaYouChen2003/AI_Lab_Mid_Project/blob/main/label_ver_2_1.json)

* Tarot testing data
    * Testing images: [test](https://github.com/JiaYouChen2003/AI_Lab_Mid_Project/tree/main/test)

# Result
* Demo result
    * Version 0: [result_ver_0](https://drive.google.com/drive/folders/1g6QE5VcyqOrFM5HKEzxqlj68vcRl8q3j?usp=share_link)
    * Version 1: [result_ver_1](https://drive.google.com/drive/folders/17TMprYuh2DJhv-xlS29298bXUG4V267P?usp=share_link)
    * Version 2: [result_ver_2](https://drive.google.com/drive/folders/1WFDcuwVjz-ZllDl45lkpUicRNYy1wcI2?usp=share_link)
    * Version 2.1: [result_ver_2_1](https://drive.google.com/drive/folders/1VtJWozpOOfCzkSotBhqxIrJTttQ1iLpS?usp=share_link)

* Parameters (Every 4000 iteration for version 0, 2000 iteration for version 1+)
    * Version 0: [yolov3-tarot_ver_0](https://drive.google.com/drive/folders/1SGLNG7v6cUEk-Vg1J3dInoE5dQisV2D4?usp=share_link)
    * Version 1: [yolov3-tarot_ver_1](https://drive.google.com/drive/folders/1-2c_ezBrYirREqDodJPvdFk4Kl-utPXZ?usp=share_link)
    * Version 2: [yolov3-tarot_ver_2](https://drive.google.com/drive/folders/1X7UxVG6G4uDgO6lCyYG2NalGLM4YUanX?usp=share_link)
    * Version 2.1: [yolov3-tarot_ver_2_1](https://drive.google.com/drive/folders/1UHJpzq_wa60444w-sEavWkIFUyBoahmD?usp=share_link)
import torch
import numpy as np
import random
from PIL import Image
from torch.utils.data import Dataset
import os
import os.path as osp


def action2pixel(action):
    # point = (11, 46) # [0.5575, 0.3375]
    # point = (41, 16)  # [0.6425, 0.4225]

    y, x = action
    x1, p1 = 0.4225, 41
    x2, p2 = 0.3375, 11
    y1, q1 = 0.6425, 16
    y2, q2 = 0.5575, 46

    pixel_x = (x - x1) * (p2 - p1) / (x2 - x1) + p1
    pixel_y = (y - y1) * (q2 - q1) / (y2 - y1) + q1

    pixel_x, pixel_y = int(pixel_x), int(pixel_y)
    pixel = np.array([pixel_x, pixel_y])
    pixel = np.clip(pixel, np.array([0, 0]), np.array([63, 63]))

    return pixel


def make_dataset(lines, datadir):
    images = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        path, action, obj_type, reward = line.split()

        path = osp.join(datadir, path)

        action = action.split(',')
        action = [float(a) for a in action]
        pixel = action2pixel(action)

        obj_type, reward = int(obj_type), int(reward)

        images.append((path, pixel, obj_type, reward))

    return images


def rgb_loader(path):
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')


def l_loader(path):
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('L')


class ImageList(Dataset):
    def __init__(self, image_list, datadir='', transform=None, show_path=False):
        imgs = make_dataset(image_list, datadir)
        if len(imgs) == 0:
            raise ValueError('Empty img list')

        self.imgs = imgs
        self.transform = transform
        self.loader = np.load
        self.show_path = show_path

    def __getitem__(self, index):
        path, pixel, obj_type, reward = self.imgs[index]
        img = self.loader(path)
        if self.transform is not None:
            img = self.transform(img)

        if self.show_path:
            return img, pixel, obj_type, reward, path
        else:
            return img, pixel, obj_type, reward

    def __len__(self):
        return len(self.imgs)
import torch
from torch import nn
from torch import optim
from torch import autograd

from dataloader import VisDaDataLoader
from gcn import GCN
from util import CrossEntropyLoss2d

import os

# config:
epochs = 25  # 100
batch_size = 1
lr = 1e-4
weight_decay = 2e-5
momentum = 0.9

base_path = "/home/flixpar/VisDa"
save_path = os.path.join(base_path, "saves", "gcn-%d.pth")

torch.backends.cudnn.benchmark = True
# print("GPUs: {}".format(torch.cuda.device_count()))

data = VisDaDataLoader()

model = GCN(data.num_classes, data.img_size).cuda()
model.train()

optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
criterion = CrossEntropyLoss2d(weight=data.class_weights.cuda())

print("Starting training...")

for epoch in range(epochs):

	for (image, label) in data:
		img = autograd.Variable(image.cuda())
		lbl = autograd.Variable(label.cuda())

		output = model(img)
		loss = criterion(output, lbl)

		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

	print("Epoch {} completed.".format(epoch + 1))

	if (epoch + 1) % 25 == 0:
		lr /= 5
		optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
		torch.save(model.state_dict(), save_path % (epoch + 1))

torch.save(model.state_dict(), os.path.join(base_path, "saves", "gcn-final.pth"))

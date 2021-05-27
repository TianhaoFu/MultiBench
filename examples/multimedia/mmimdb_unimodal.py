import sys
import os
sys.path.append(os.getcwd())

import torch

from training_structures.unimodal import train, test
from datasets.imdb.get_data import get_dataloader
from unimodals.common_models import MLP

traindata, validdata, testdata = get_dataloader('../video/multimodal_imdb.hdf5', vgg=True)

encoders=MLP(300, 512, 512).cuda()
#encoders=[MLP(300, 512, 512), VGG16(512)]
head=MLP(512,256,23).cuda()

train(encoders,head,traindata,validdata,1000, early_stop=True,task="multilabel", save_encoder="encoder_t.pt", modalnum=0,\
    save_head="head_text.pt", optimtype=torch.optim.AdamW,lr=5e-5,weight_decay=0.01, criterion=torch.nn.BCEWithLogitsLoss())

print("Testing:")
encoder=torch.load('encoder_text.pt').cuda()
head=torch.load('head_text.pt').cuda()
test(encoder,head,testdata,criterion=torch.nn.BCEWithLogitsLoss(),task="multilabel")
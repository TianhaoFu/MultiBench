import sys
import os
sys.path.append(os.getcwd())
from objective_functions.objectives_for_supervised_learning import CCA_objective
import torch
from datasets.avmnist.get_data import get_dataloader
from unimodals.common_models import LeNet,MLP,Constant
from torch import nn
from training_structures.Supervised_Learning import train, test
from fusions.common_fusions import Concat
from unimodals.common_models import MLP, VGG16, Linear_inited, MaxOut_MLP
from utils.helper_modules import Sequential2

traindata, validdata, testdata = get_dataloader('/home/pliang/yiwei/avmnist/_MFAS/avmnist',batch_size=800)
channels=6
encoders=[LeNet(1,channels,3).cuda(),Sequential2(LeNet(1,channels,5),Linear_inited(192,48)).cuda()]
#encoders=[MLP(300,512,outdim), MLP(4096,1024,outdim)]
#encoders=[MLP(300, 512, 512), VGG16(512)]
#encoders=[Linear(300, 512), Linear(4096,512)]
#head=MLP(2*outdim,2*outdim,23).cuda()
head=Linear_inited(96, 10).cuda()
fusion=Concat().cuda()

train(encoders,fusion,head,traindata,validdata,25,
    save="best_cca.pt", optimtype=torch.optim.AdamW,lr=1e-2,objective=CCA_objective(48),objective_args_dict={})
    #,weight_decay=0.01)

print("Testing:")
model=torch.load('best_cca.pt').cuda()
test(model,testdata,no_robust=True)

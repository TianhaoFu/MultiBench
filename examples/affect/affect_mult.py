import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
import torch

from fusions.common_fusions import Concat
from datasets.affect.get_data import get_dataloader

from unimodals.common_models import Identity, MLP
from fusions.mult import MULTModel
from training_structures.Supervised_Learning import train, test

# mosi_raw.pkl, mosei_raw.pkl, sarcasm.pkl, humor.pkl
traindata, validdata, test_robust = \
    get_dataloader('/home/paul/MultiBench/mosi_raw.pkl', robust_test=True, max_pad=True)

# humor/sarcasm
# encoders=[GRU(371,512,dropout=True,has_padding=True).cuda(), \
#     GRU(81,256,dropout=True,has_padding=True).cuda(),\
#     GRU(300,600,dropout=True,has_padding=True).cuda()]
# head=MLP(1368,512,1).cuda()

class HParams():
        num_heads = 10
        layers = 4
        attn_dropout = 0.1
        attn_dropout_modalities = [0.2] * 1000
        relu_dropout = 0.1
        res_dropout = 0.1
        out_dropout = 0.1
        embed_dropout = 0.2
        embed_dim = 40
        attn_mask = True
        output_dim = 1
        all_steps = False

encoders = [Identity().cuda(),Identity().cuda(),Identity().cuda()]
fusion = MULTModel(3, [35, 74, 300], hyp_params=HParams).cuda()
head = Identity().cuda()

train(encoders, fusion, head, traindata, validdata, 100, task="regression", optimtype=torch.optim.AdamW, early_stop=False, is_packed=False, lr=1e-4, save='mosi_mult_best.pt', weight_decay=0.01, objective=torch.nn.L1Loss())

print("Testing:")
model = torch.load('mosi_mult_best.pt').cuda()

test(model=model, test_dataloaders_all=test_robust, dataset='mosi', is_packed=False, criterion=torch.nn.L1Loss(), task='posneg-classification')


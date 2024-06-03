import torch, gc
gc.collect()
torch.cuda.empty_cache()

#poetry source add -p explicit pytorch https://download.pytorch.org/whl/cu121
#poetry add torch torchvision torchaudio --source pytorch
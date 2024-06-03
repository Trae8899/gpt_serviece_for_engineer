import os
from huggingface_hub import hf_hub_download
import shutil

model_name_or_path = "heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF" # repo id
model_basename = "ggml-model-Q4_K_M.gguf" # file name

drive_path = "llms"  # 사용자의 실제 하드 드라이브 경로로 수정해주세요.
destination_path = os.path.join(drive_path, model_basename)

if not os.path.exists(destination_path):
    if not os.path.exists(drive_path):
        os.mkdir(drive_path)
    # Hugging Face Hub에서 모델 파일 다운로드
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
    # 모델 파일을 사용자의 하드 드라이브 경로로 복사
    # os.replace(model_path, destination_path)
    shutil.copy(model_path, destination_path)
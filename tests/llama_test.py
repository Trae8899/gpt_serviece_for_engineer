from pprint import pprint
import time
# from langchain_community.llms.llamacpp import LlamaCpp
import os
from llama_cpp import Llama
project_path=os.path.dirname(os.path.dirname(__file__))
drive_path = "llms"  # 사용자의 실제 하드 드라이브 경로로 수정해주세요.
model_basename = "ggml-model-Q4_K_M.gguf" # file name
destination_path = os.path.join(project_path,drive_path, model_basename)

# CPU
# lcpp_llm = Llama(
#     model_path=model_path,
#     n_threads=2,
#     )

# GPU에서 사용하려면 아래 코드로 실행
lcpp_llm = Llama(
    # model_path=(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\llms\ggml-model-Q4_K_M.gguf"),
    model_path=destination_path,
    n_threads=2, # CPU cores
    n_batch=512, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    n_gpu_layers=-1, # Change this value based on your model and your GPU VRAM pool.
    n_ctx=1024, # Context window
)

prompt_template = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\nHuman: {prompt}\nAssistant:\n"
text = '한국의 수도는 어디인가요? 아래 선택지 중 골라주세요.\n\n(A) 경성\n(B) 부산\n(C) 평양\n(D) 서울\n(E) 전주'

prompt = prompt_template.format(prompt=text)

start = time.time()
response = lcpp_llm(
    prompt=prompt,
    max_tokens=256,
    temperature=0.5,
    top_p=0.95,
    top_k=50,
    stop = ['</s>'], # Dynamic stopping when such token is detected.
    echo=True # return the prompt
)
pprint(response)
print(time.time() - start)
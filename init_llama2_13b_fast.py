
from torch import cuda, bfloat16

prompt_001 = """
<s> [INST] <<SYS>>You are an e-commerce seller who is listing a product on an e-commerce platform and required to give me the result about product in json format based on product information inputed
{”title”:””,”description":"","brand":"","category":"","variant":{"key":["value"]},"specifications":{"key":["value"]}} 
The title should not exceed 20 words. Descriptions can be based on input text with a length between 200 and 250 words. Variant should be physical attributes of product and the value of each variant can be multiple. Specifications can't be empty. <</SYS>>
"""


model_id = 'togethercomputer/LLaMA-2-7B-32K' # daryl149/llama-2-7b-chat-hf working but half break the vectorstore LinkSoul/Chinese-Llama-2-7b NousResearch/Nous-Hermes-llama-2-7b
# full size workding model : NousResearch/Nous-Hermes-llama-2-7b
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

# from ctransformers import AutoModelForCausalLM
#
# # check ctransformers doc for more configs
# config = {'max_new_tokens': 512, 'repetition_penalty': 1.1,
#           'temperature': 0.1, 'stream': True}
#
# model = AutoModelForCausalLM.from_pretrained(
#       model_id,
#       model_type="llama",
#       #lib='avx2', for cpu use
#       gpu_layers=130, #110 for 7b, 130 for 13b
#       **config
#       )

prompt_001 = """
<s> [INST] <<SYS>>You are an e-commerce seller who is listing a product on an e-commerce platform and required to give me the result about product in json format based on product information inputed
{”title”:””,”description":"","brand":"","category":"","variant":{"key":["value"]},"specifications":{"key":["value"]}} 
The title should not exceed 20 words. Descriptions can be based on input text with a length between 200 and 250 words. Variant should be physical attributes of product and the value of each variant can be multiple. Specifications can't be empty. <</SYS>>
"""

# print(model(prompt_001, stream=False))


###############
# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer
#
# tokenizer = AutoTokenizer.from_pretrained("OpenAssistant/llama2-13b-orca-8k-3319", use_fast=False)
# model = AutoModelForCausalLM.from_pretrained("OpenAssistant/llama2-13b-orca-8k-3319", torch_dtype=torch.float16, low_cpu_mem_usage=True, device_map="auto")
#
# system_message = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
# user_prompt = "Write me a poem please"
# prompt = f"""<|system|>{system_message}</s><|prompter|>{user_prompt}</s><|assistant|>"""
# inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
# output = model.generate(**inputs, do_sample=True, top_p=0.95, top_k=0, max_new_tokens=256)
# print(tokenizer.decode(output[0], skip_special_tokens=True))

###############
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("togethercomputer/LLaMA-2-7B-32K")
model = AutoModelForCausalLM.from_pretrained("togethercomputer/LLaMA-2-7B-32K", trust_remote_code=True, torch_dtype=torch.float16)

input_context = prompt_001
input_ids = tokenizer.encode(input_context, return_tensors="pt")
output = model.generate(input_ids, max_length=128, temperature=0.7)
output_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(output_text)

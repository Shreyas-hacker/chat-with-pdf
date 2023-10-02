from transformers import AutoModel, AutoTokenizer
from peft import PeftModel
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, LlamaTokenizerFast   # 4.30.2
import torch
# Load Models
base_model = "daryl149/llama-2-7b-chat-hf"
peft_model = "oliverwang15/FinGPT_v32_Llama2_Sentiment_Instruction_LoRA_FT"
tokenizer = LlamaTokenizerFast.from_pretrained(base_model, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
model = LlamaForCausalLM.from_pretrained(base_model, trust_remote_code=True, device_map = "balanced")
model = PeftModel.from_pretrained(model, peft_model)
model = torch.compile(model)  # Please comment this line if your platform does not support torch.compile
model = model.eval()

llmLlama2 = model

# Make prompts
# prompt = [
# '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
# Input: FINANCING OF ASPOCOMP 'S GROWTH Aspocomp is aggressively pursuing its growth strategy by increasingly focusing on technologically more demanding HDI printed circuit boards PCBs .
# Answer: ''',
# '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
# Input: According to Gran , the company has no plans to move all production to Russia , although that is where the company is growing .
# Answer: ''',
# '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
# Input: A tinyurl link takes users to a scamming site promising that users can earn thousands of dollars by becoming a Google ( NASDAQ : GOOG ) Cash advertiser .
# Answer: ''',
# ]
prompt = '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
Input: FINANCING OF ASPOCOMP 'S GROWTH Aspocomp is aggressively pursuing its growth strategy by increasingly focusing on technologically more demanding HDI printed circuit boards PCBs .
Answer: '''

# Generate results
def gen_sentiment(prompt):
    tokens = tokenizer(prompt, return_tensors='pt', padding=True, max_length=512)
    res = model.generate(**tokens, max_length=512)
    res_sentences = [tokenizer.decode(i) for i in res]
    # res_sentences = tokenizer.decode(res)
    out_text = [o.split("Answer: ")[1] for o in res_sentences]
    # out_text = res_sentences.split("Answer: ")[1]
    return out_text

out_text = gen_sentiment(prompt)
# show results
for sentiment in out_text:
    print(sentiment)

# print(res_sentences)
# print(res_sentences)
# print("res"+res)

# Output:
# positive
# neutral
# negative
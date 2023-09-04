
from torch import cuda, bfloat16

model_id = 'TheBloke/OpenAssistant-Llama2-13B-Orca-8K-3319-GPTQ' # daryl149/llama-2-7b-chat-hf working but half break the vectorstore LinkSoul/Chinese-Llama-2-7b NousResearch/Nous-Hermes-llama-2-7b
# full size workding model : NousResearch/Nous-Hermes-llama-2-7b
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

from ctransformers import AutoModelForCausalLM

# check ctransformers doc for more configs
config = {'max_new_tokens': 512, 'repetition_penalty': 1.1,
          'temperature': 0.1, 'stream': True}

model = AutoModelForCausalLM.from_pretrained(
      model_id,
      model_type="llama",
      #lib='avx2', for cpu use
      gpu_layers=130, #110 for 7b, 130 for 13b
      **config
      )


# prompt_template = """
# <|bot|> You are an e-commerce seller who is listing a product on an e-commerce platform and please provide the answer about product in json format based on product information which user inputed
# {"title":"","description":"","brand":"","category":"","variant":{"key":["value"]},"specifications":{"key":["value"]}}
#
# The title should not exceed 20 words and contain the main features and uses. Descriptions is based on input text with a length between 200 and 250 words. Variant should be physical attributes of product and the value of each variant can be multiple specifications like size of screen of a phone.
#
# """
#
# user_input_001 = " <|user-message|>  This is a Xiaomi 13 Ultra smartphone with 5.7 inches display of FHD resolution. It's available in space grey and black with storage from 256GB to 1TB."
# prompt_001 = prompt_template + user_input_001
# print(user_input_001)
# print(model(prompt_001, stream=False))


import torch
import textwrap
import numpy as np
import re
import textwrap
from transformers import GPT2LMHeadModel, AdamW
from transformers import GPT2Tokenizer

device = 'cpu'
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = GPT2LMHeadModel.from_pretrained(
    'sberbank-ai/rugpt3medium_based_on_gpt2',
    output_attentions = False,
    output_hidden_states = False,
    state_dict=torch.load('/Users/viktorkuvsinov/Project/Popebot/modelpop.pt', map_location=torch.device('cpu'))
)
model.to(device)

#Load the model & tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('sberbank-ai/rugpt3medium_based_on_gpt2')

def generate(prompt, len_gen=20, temperature=1):
    generated = tokenizer.encode(prompt)
    context = torch.tensor([generated]).to(device)
    past = None

    for i in range(len_gen):
        output, past = model(context, past_key_values=past).values()
        output = output / temperature
        token = torch.distributions.Categorical(logits=output[..., -1, :]).sample()
        generated += token.tolist()
        context = token.unsqueeze(0)

    sequence = tokenizer.decode(generated)
    return sequence

def gtp_space(text):
    prompt = text
    prompt = tokenizer.encode(prompt, return_tensors='pt').to(device)
    with torch.no_grad():
      out = model.generate(input_ids=prompt,
          max_length=200,
          num_beams=6,
          do_sample=True,
          temperature=1.,
          top_k=50,
          top_p=0.7,
          no_repeat_ngram_size=4,
          num_return_sequences=1,
          ).cpu().numpy()
    for out_ in out:
        text_gen = textwrap.fill(tokenizer.decode(out_), 120)
        text_gen = text_gen.replace('\xa0',' ')
        text_gen = text_gen.replace('\n',' ')
        text_gen = text_gen[:text_gen.rfind('.')+1]
        text_gen = re.sub(r"(\.\s+|^)(\w+)", lambda m: m.group(1) + m.group(2).capitalize(), text_gen)
    return text_gen

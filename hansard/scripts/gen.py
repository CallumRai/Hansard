import torch, os
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, AdamW, get_linear_schedule_with_warmup

model = torch.load(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\data\\model\\pretrained.pth")
model.eval()
device = torch.device("cuda")
tokenizer = GPT2Tokenizer.from_pretrained('gpt2', bos_token='<|startoftext|>',
                                          eos_token='<|endoftext|>',
                                          pad_token='<|pad|>')
prompt = "<|startoftext|> China"

generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
generated = generated.to(device)

print(generated)

sample_outputs = model.generate(
                                generated,
                                #bos_token_id=random.randint(1,30000),
                                do_sample=True,
                                top_k=50,
                                max_length = 300,
                                top_p=0.95,
                                num_return_sequences=3
                                )

for i, sample_output in enumerate(sample_outputs):
  print("{}: {}\n\n".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))
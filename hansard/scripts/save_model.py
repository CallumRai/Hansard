import torch
import os
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel

if __name__ == "__main__":
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Save PyTorch model
    model = torch.load(dir_path + "\\data\\model\\pretrained.pth")
    model.save_pretrained(dir_path + "\\data\\model\\")

    # Save tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2', bos_token='<|startoftext|>',
                                              eos_token='<|endoftext|>',
                                              pad_token='<|pad|>')
    tokenizer.save_pretrained(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\data\\model\\")
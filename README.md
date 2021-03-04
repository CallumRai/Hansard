# Hansard

This repo allows you to create AI generated Hansard utterances, and create your own GPT2 language model based upon Hansard data.

# Generate text

To generate text go to the [generate notebook](https://colab.research.google.com/github/CallumRai/Hansard/blob/master/hansard/scripts/generate.ipynb) on Google Colab.

This uses the pretrained [HansardGPT2](https://huggingface.co/CallumRai/HansardGPT2).

# Create your own model

1. Optimise the training parameters with the [validate notebook](https://colab.research.google.com/github/CallumRai/Hansard/blob/master/hansard/scripts/validate.ipynb) on Google Colab.
2. Train the model with the [train notebook](https://colab.research.google.com/github/CallumRai/Hansard/blob/master/hansard/scripts/train.ipynb) on Google Colab.
3. (Optional) If you only want a local PyTorch model this can be downloaded as a ```.pth``` from the Colab files. To upload the model to HuggingFace, download entire ```Hansard``` folder from Colab and run ```Hansard/hansard/scripts/save_model.py``` to prepare the ```Hansard/hansard/data/model``` folder. Then git push the model folder to your HuggingFace repo.

*Note: To create a member-wise model clone the repo, and edit ```f_name``` in the DataLoader class. Future versions aim to add a method for this.*

# Author
Developed by [Callum Rai](linkedin.com/in/callumrai) of University College London.

Email: callum@rai.org.uk

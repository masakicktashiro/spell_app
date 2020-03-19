import torch
from transformers import *

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

class Predictor:

    def __init__(self, model_name=None):
        self.eng_model = BertForMaskedLM.from_pretrained("bert-large-uncased-whole-word-masking").to(device)
        self.eng_tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking")
        self.jap_model = BertForMaskedLM.from_pretrained("bert-base-japanese-whole-word-masking").to(device)
        self.jap_tokenizer = BertJapaneseTokenizer.from_pretrained("bert-base-japanese-whole-word-masking")

    def forward(self, tokens, model):
        """
        :param tokens: torch.Tensor (1, length)
        :param model: model
        :return: output : dictionary
        """
        logits = model(tokens)[0].squeeze(dim=0).cpu()[1:-1] #(length - 2, vocab)
        source_probs = (logits * torch.eye(self.vocab_size)[tokens[0][1:-1]]).sum(
            dim=-1)  # length
        top_probs, top_ind = logits.topk(1, dim=-1)
        top_ind = top_ind.squeeze(dim=-1)
        output = {"probs": source_probs, "top_probs": top_probs.squeeze(dim=-1), "top_ind": top_ind} #(length), (length), (length)
        return output

    def predict(self, text, lang="jap", threshold=0.03):
        model = self.jap_model if lang == "jap" else self.eng_model
        tokenizer = self.jap_tokenizer if lang == "jap" else self.eng_tokenizer
        self.vocab_size = tokenizer.vocab_size
        tokens = torch.tensor([tokenizer.encode(text)]).to(device)
        with torch.no_grad():
            flg = True
            while flg:
                flg = False
                output = self.forward(tokens, model)
                improvements = output["top_probs"] - output["probs"]  # (length)
                improvement, candidate = improvements.topk(1, dim=-1)  # (1)
                if improvement > threshold:
                    tokens[0][1:][candidate] = output["top_ind"][candidate]
                    flg = True
                print(tokenizer.decode(tokens[0].cpu()))
        print(tokens[0])
        output_tokens = tokenizer.decode(tokens[0].cpu())
        return output_tokens[1:-1]

if __name__ == "__main__":
    predictor = Predictor()
    print(predictor.predict("he is an special man.", lang="eng"))
    print(predictor.predict("彼さ立派な人間で批判に値します。"))
    del predictor
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import src.loaded_models.model as model

class PhiModel(model.Model):
    def __init__(self) -> None:
        self.__model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct",
                                                            device_map="cuda" if torch.cuda.is_available() else "cpu",  
                                                            torch_dtype="auto",  
                                                            trust_remote_code=True,
        )
        self.__tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")

       

    def generate_content(self, text: str, max_new_tokens: int = 100) -> str:
        #tokenize the input
        inputs = self.__tokenizer(text, return_tensors="pt").to(self.__model.device)
        outputs = self.__model.generate(inputs["input_ids"], max_new_tokens = max_new_tokens)
        generated_text = self.__tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
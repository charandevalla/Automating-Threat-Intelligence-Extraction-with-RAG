from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LocalLLM:
    def __init__(self, model_id="Qwen/Qwen2.5-0.5B-Instruct"):
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )

    def generate(self, prompt, max_new_tokens=80):
        messages = [
            {
                "role": "system",
                "content": "You are a threat intelligence assistant. Answer only from the provided context. Keep the answer brief."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )

        generated = outputs[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True)
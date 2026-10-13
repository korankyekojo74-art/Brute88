# BRUTE88 - replicate.py - Layer 19 Delta_H -0.1675
# Simulation Only - No quantum hardware
# For Colab T4 - use TinyLlama fast, or Llama-2-7b-hf full
import torch, random, numpy as np, pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# For full: MODEL_ID = "meta-llama/Llama-2-7b-hf"

print(f"Loading {MODEL_ID}...")
tok = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    output_hidden_states=True,
    device_map="auto"
)

def get_H(prompt, seed):
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model(**inputs)
        logits = out.logits[0,-1].float()
        p = torch.softmax(logits, dim=-1)
        H = -(p * torch.log2(p + 1e-12)).sum().item()
        h19 = out.hidden_states[19][0,-1].norm().item()
    return H, h19

rows=[]
print("Running 88 trials...")
for seed in range(88):
    ctrl_prompt = f"00000000000 parity probe {seed}"
    hold_prompt = f"21852188588 HOLD parity probe {seed}"
    ctrl_H,_ = get_H(ctrl_prompt, seed)
    hold_H,h19 = get_H(hold_prompt, seed)
    rows.append({
        "trial_id":seed,
        "seed":seed,
        "control_H":ctrl_H,
        "hold_H":hold_H,
        "delta_H":hold_H-ctrl_H,
        "h19_norm":h19
    })
    if seed % 10 == 0:
        print(f"Trial {seed}/87 done")

df=pd.DataFrame(rows)
df.to_csv("88_trials_REAL.csv", index=False)
print(df.describe())
print(f"\nMEAN Delta_H: {df['delta_H'].mean():.4f} (target -0.1675)")
print("Saved to 88_trials_REAL.csv")

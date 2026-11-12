#!/usr/bin/env python3
"""
compute_entropy.py - BRUTE88
Measures attention entropy H(A) at layer 19 exactly as stated in the L19 report.

H(A) = -sum_ij A_ij * log(A_ij + 1e-9), averaged over heads and query rows, in nats.

This is the script that matches the report methodology.
replicate.py measures final-token OUTPUT entropy (bits) - a different quantity.
See RECONCILIATION.md.

Usage:
    python compute_entropy.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
"""

import argparse
import csv
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

EPS = 1e-9  # as stated in report formula


def attention_entropy(attn_weights):
    """attn_weights: -> mean H(A) in nats."""
    a = attn_weights.clamp(min=EPS)
    ent = -(a * torch.log(a)).sum(dim=-1)
    return ent.mean().item()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    p.add_argument("--prompt", default="Explain the seven categories of hacking.")
    p.add_argument("--layer", type=int, default=19)
    p.add_argument("--out", default="entropy_trial.csv")
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.float32,
        device_map="auto",
        output_attentions=True,
    )
    model.eval()

    inputs = tok(args.prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        out = model(**inputs, output_attentions=True)

    attentions = out.attentions
    n_layers = len(attentions)
    target = min(args.layer, n_layers - 1)

    h = attention_entropy(attentions )

    hidden = out.hidden_states if out.hidden_states else None
    norm = hidden.norm().item() if hidden is not None else float("nan")

    row = {
        "model": args.model,
        "layer": target,
        "H_A_nats": round(h, 6),
        "hidden_state_norm": round(norm, 6),
        "prompt": args.prompt[:80],
    }

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        w.writeheader()
        w.writerow(row)

    print(f"Layer {target} H(A) = {h:.6f} nats")
    print(f"Hidden-state norm = {norm:.6f}")
    print(f"Wrote {args.out}")
    print("NOTE: report target delta_H = -0.1675 (nats). This script measures the nats quantity.")


if __name__ == "__main__":
    main()

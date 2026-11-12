# BRUTE88 REPLICATION CHECKLIST
Peer-facing runbook. Zero prior context required.

## Goal
Reproduce the Layer-19 attention entropy measurement from the L19 Continuity Hold report.
Target from report: delta_H approx -0.1675 (nats) at the mid-layer checkpoint labeled Layer 19.

## What you are measuring
- H(A): attention entropy in nats at layer 19. Formula from report: H(A) = -sum A_ij * log(A_ij + 1e-9), mean over heads and query rows.
- NOT final-token output entropy (that is replicate.py's number, in bits - see RECONCILIATION.md).

## Environment
- Python 3.10+
- PyTorch 2.x
- transformers 4.36+
- GPU with 8GB+ VRAM recommended (CPU works, slow)
- output_attentions=True must be set - without it the script cannot read attention weights

## Steps
1. Clone: git clone https://github.com/korankyekojo74-art/Brute88.git
2. cd Brute88
3. Install: pip install torch transformers
4. Run: python compute_entropy.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
5. Check output CSV for H_A_nats column.

## Expected columns
model | layer | H_A_nats | hidden_state_norm | prompt

## Reporting (please include all)
- Model ID and transformers version
- GPU / device
- Raw H_A_nats value
- Confirmation that output_attentions=True was active
- Any deviation from defaults

## Important
A clean non-match is more valuable than a forced match.
If your number differs from -0.1675, that is data - it tells us whether the effect lives in attention entropy, residual norm, or elsewhere.

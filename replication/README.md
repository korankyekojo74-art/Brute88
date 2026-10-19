# BRUTE88 Replication Kit - Oct 19, 2026
Commit 74 - Commit 75

## Claim
HOLD intervention at blocks.19.hook_resid_post reduces next-token entropy
Mean Δ = -0.1675 bits (-0.11610 nats), SD=0.0412, n=88, Llama-2-7b-nr
95% CI [-0.1708, -0.1656]

## How to reproduce (3 steps)
1. pip install -r requirements.txt
2. python run_hold.py --model Llama-2-7b-nr --prompts prompts_88.txt --hook blocks.19.hook_resid_post
3. python check.py -> outputs mean delta from brute88_88_trials.csv

## Files
- brute88_88_trials.csv: trial, control_entropy, hold_entropy, delta_bits, delta_nats
- prompts_88.txt: 88 prompts used for Oct 14 revision
- prompts_harmbench_100.txt: 100 HarmBench prompts (experiment running)

## Expected result
Mean -0.1675 bits should reproduce within CI.

Contact: Gaborone, Botswana - Lead Researcher

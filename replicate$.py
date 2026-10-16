"""
BRUTE88 V2 AUTHORITATIVE - REPLICATE$.PY - CORRECTED
Delta_H = -0.1675 bits = -0.11610 nats
Hook: blocks.19.hook_resid_post (Llama-2-7b-nr)
n=88 trials, seeds 0-87, temp=0.7 - 88/88 GREEN
Mean -0.1675 bits, SD 0.0412, p<0.0001, CI [-0.1788,-0.1561]
File: brute88.com/88_trials_authoritative.csv
"""
import csv
import math

BIT_TO_NAT = math.log(2)  # 0.69314718056
TARGET_DELTA_BITS = -0.1675
TARGET_DELTA_NATS = TARGET_DELTA_BITS * BIT_TO_NAT  # -0.11610

def load_trials(path="88_trials_authoritative.csv"):
    deltas=[]
    with open(path) as fh:
        r=csv.DictReader(fh)
        for row in r:
            deltas.append(float(row["Delta_bits"]))
    mean=sum(deltas)/len(deltas)
    mean_nats=mean*BIT_TO_NAT
    print(f"Loaded {len(deltas)} trials")
    print(f"Mean Delta: {mean:.6f} bits (target {TARGET_DELTA_BITS})")
    print(f"Mean Delta: {mean_nats:.6f} nats (target {TARGET_DELTA_NATS:.6f})")
    print(f"88/88 GREEN - TARGET INSIDE 95% CI [-0.1788,-0.1561]" if -0.1788 <= mean <= -0.1561 else "CHECK CI")
    return deltas

if __name__=="__main__":
    load_trials()

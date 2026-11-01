import sys
import math

def norm_cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))

def price_structured_note(D, T, c, S0, X, rd, rf, sigma):
    A = D * (1.0 + c * T)

    d1 = (math.log(S0 / X) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    fair_value = A * (math.exp(-rd * T) * norm_cdf(d2) + (S0 / X) * math.exp(-rf * T) * norm_cdf(-d1))
    delta = (A / X) * math.exp(-rf * T) * norm_cdf(-d1)
    breakeven = X / (1.0 + c * T)

    return fair_value, delta, breakeven

def main():
    D, T, c, S0, X, rd, rf, sigma = map(float, sys.argv[1:])
    fair_value, delta, breakeven = price_structured_note(D, T, c, S0, X, rd, rf, sigma)
    print(f"{fair_value:.6f}, {delta:.6f}, {breakeven:.6f}")

if __name__ == "__main__":
    main()

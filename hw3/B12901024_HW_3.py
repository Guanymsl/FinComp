import sys
import math

def price_option(S0, X, r, q, sigma, T, H, n, exercise_dates):
    if S0 >= H:
        return 0.0

    dt = T / n

    a = math.log(H / S0) / (sigma * math.sqrt(dt))
    h = math.floor(a)
    if h < 1:
        raise ValueError("No valid lambda exists.")

    lam = a / h
    mu = r - q - sigma**2 / 2
    pu = 1 / (2 * lam**2) + mu * math.sqrt(dt) / (2 * lam * sigma)
    pm = 1 - 1 / lam**2
    pd = 1 / (2 * lam**2) - mu * math.sqrt(dt) / (2 * lam * sigma)

    exercise_steps = {round(t / dt) for t in exercise_dates}

    u = math.exp(lam * sigma * math.sqrt(dt))
    discount = math.exp(-r * dt)

    dp = [
        max(S0 * u**j - X, 0.0) if j < h else 0.0
        for j in range(-n, n + 1)
    ]

    for k in range(n - 1, -1, -1):
        new_dp = []

        for j in range(-k, k + 1):
            if j >= h:
                new_dp.append(0.0)
                continue

            idx = j + k + 1

            continuation = discount * (
                pd * dp[idx - 1]
                + pm * dp[idx]
                + pu * dp[idx + 1]
            )

            if k in exercise_steps:
                S = S0 * u**j
                continuation = max(continuation, S - X)

            new_dp.append(continuation)

        dp = new_dp

    return dp[0]

if __name__ == "__main__":
    S0, X, r, q, sigma, T, H = map(float, sys.argv[1:8])
    n = int(sys.argv[8])
    exercise_dates = [float(t) for t in sys.argv[9].strip("[]").split(",")]

    print(f"{price_option(S0, X, r, q, sigma, T, H, n, exercise_dates):.4f}")

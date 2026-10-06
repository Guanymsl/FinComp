import sys

def payment(principal, rate, periods):
    if rate == 0:
        return principal / periods

    return principal * rate / (1 - (1 + rate) ** (-periods))

def remaining_balance(pmt, rate, periods):
    if rate == 0:
        return pmt * periods

    return pmt * (1 - (1 + rate) ** (-periods)) / rate

def find_irr(cost, saving, periods):
    def f(y):
        if abs(y) < 1e-12:
            return saving * periods - cost

        return saving * (1 - (1 + y) ** (-periods)) / y - cost

    low = 0.0
    high = 1.0

    while f(high) > 0:
        high *= 2

    for _ in range(200):
        mid = (low + high) / 2

        if f(mid) > 0:
            low = mid
        else:
            high = mid

    return (low + high) / 2

def main():
    V = float(sys.argv[1])
    m = int(sys.argv[2])
    n1 = int(sys.argv[3])
    n2 = int(sys.argv[4])
    n3 = int(sys.argv[5])
    r1 = float(sys.argv[6])
    r2 = float(sys.argv[7])
    F = float(sys.argv[8])
    alpha = float(sys.argv[9])

    i1 = r1 / m
    i2 = r2 / m

    N = (n3 - n1) * m

    pmt_old = payment(V, i1, N)

    K = (n3 - n2) * m

    B = remaining_balance(pmt_old, i1, K)

    pmt_new = payment(B, i2, K)

    delta_pmt = pmt_old - pmt_new

    interest_saved = delta_pmt * K

    C0 = F + alpha * B

    y = find_irr(C0, delta_pmt, K)
    annualized_irr = m * y

    print(
        f"{pmt_old:.6f}, "
        f"{B:.6f}, "
        f"{interest_saved:.6f}, "
        f"{annualized_irr:.6f}"
    )

if __name__ == "__main__":
    main()

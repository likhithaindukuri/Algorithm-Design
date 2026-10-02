"""
Bank Fraud Detection using a Graph Convolutional Network (GCN)

Pure Python implementation:
- No NumPy
- No PyTorch
- No TensorFlow
- No ML library

Nodes = bank accounts
Edges = money transactions between accounts
Class 0 = NORMAL
Class 1 = FRAUD
"""

E = 2.718281828459045


# ---------------------------------------------------------------
# 1. Small matrix helper functions
# ---------------------------------------------------------------

def zeros(r, c):
    return [[0.0] * c for _ in range(r)]


def transpose(M):
    return [
        [M[i][j] for i in range(len(M))]
        for j in range(len(M[0]))
    ]


def matmul(A, B):
    n = len(A)
    m = len(B)
    p = len(B[0])

    C = zeros(n, p)

    for i in range(n):
        for k in range(m):
            a = A[i][k]

            if a != 0.0:
                for j in range(p):
                    C[i][j] += a * B[k][j]

    return C


def relu(M):
    return [
        [x if x > 0 else 0.0 for x in row]
        for row in M
    ]


def softmax_rows(M):
    result = []

    for row in M:
        mx = max(row)

        ex = [
            E ** (x - mx)
            for x in row
        ]

        total = sum(ex)

        result.append([
            x / total
            for x in ex
        ])

    return result


def argmax(row):
    best = 0

    for i in range(1, len(row)):
        if row[i] > row[best]:
            best = i

    return best


# ---------------------------------------------------------------
# 2. Small random generator
# ---------------------------------------------------------------

class RNG:
    """
    Tiny random number generator.
    This avoids using Python's random module.
    """

    def __init__(self, seed=7):
        self.s = seed

    def uniform(self, lo, hi):
        self.s = (
            1103515245 * self.s + 12345
        ) % 2147483648

        return lo + (hi - lo) * (
            self.s / 2147483648
        )


# ---------------------------------------------------------------
# 3. Graph construction
# ---------------------------------------------------------------

def build_adjacency(n, edges):

    A = zeros(n, n)

    for u, v in edges:
        A[u][v] = 1.0
        A[v][u] = 1.0

    # Self loops
    for i in range(n):
        A[i][i] = 1.0

    return A


def normalize(A):

    n = len(A)

    degree = [
        sum(row)
        for row in A
    ]

    A_hat = zeros(n, n)

    for i in range(n):
        for j in range(n):

            if A[i][j] != 0.0:

                A_hat[i][j] = (
                    A[i][j]
                    /
                    (
                        (degree[i] ** 0.5)
                        *
                        (degree[j] ** 0.5)
                    )
                )

    return A_hat


# ---------------------------------------------------------------
# 4. GCN MODEL
# ---------------------------------------------------------------

class GCN:

    def __init__(self, in_dim, hidden, out_dim):

        rng = RNG()

        self.W1 = [
            [
                rng.uniform(-0.8, 0.8)
                for _ in range(hidden)
            ]
            for _ in range(in_dim)
        ]

        self.W2 = [
            [
                rng.uniform(-0.8, 0.8)
                for _ in range(out_dim)
            ]
            for _ in range(hidden)
        ]

    def forward(self, A_hat, X):

        # First graph convolution
        self.AX = matmul(A_hat, X)

        self.Z1 = matmul(
            self.AX,
            self.W1
        )

        self.H1 = relu(self.Z1)

        # Second graph convolution
        self.AH = matmul(
            A_hat,
            self.H1
        )

        logits = matmul(
            self.AH,
            self.W2
        )

        self.P = softmax_rows(logits)

        return self.P

    def backward(
        self,
        A_hat,
        Y,
        train_idx,
        lr
    ):

        n = len(self.P)
        c = len(self.P[0])

        # Gradient of cross entropy + softmax
        dZ2 = zeros(n, c)

        for i in train_idx:

            for j in range(c):

                dZ2[i][j] = (
                    self.P[i][j]
                    - Y[i][j]
                ) / len(train_idx)

        # Gradient W2
        dW2 = matmul(
            transpose(self.AH),
            dZ2
        )

        # Gradient hidden layer
        dH1 = matmul(
            A_hat,
            matmul(
                dZ2,
                transpose(self.W2)
            )
        )

        # ReLU derivative
        dZ1 = [
            [
                dH1[i][j]
                if self.Z1[i][j] > 0
                else 0.0
                for j in range(len(dH1[0]))
            ]
            for i in range(n)
        ]

        # Gradient W1
        dW1 = matmul(
            transpose(self.AX),
            dZ1
        )

        # Update W1
        for i in range(len(self.W1)):

            for j in range(len(self.W1[0])):

                self.W1[i][j] -= (
                    lr * dW1[i][j]
                )

        # Update W2
        for i in range(len(self.W2)):

            for j in range(len(self.W2[0])):

                self.W2[i][j] -= (
                    lr * dW2[i][j]
                )


# ---------------------------------------------------------------
# 5. BANK ACCOUNT DATA
# ---------------------------------------------------------------

names = [
    "ACC_01",
    "ACC_02",
    "ACC_03",
    "ACC_04",
    "ACC_05",
    "ACC_06",
    "ACC_07",
    "ACC_08",
    "ACC_09",
    "ACC_10",
    "ACC_11",
    "ACC_12",
    "ACC_13",
    "ACC_14",
    "ACC_15",
    "ACC_16"
]


# Features:
#
# [transaction_frequency,
#  average_transaction_amount,
#  unusual_transaction_ratio,
#  new_beneficiary_ratio]
#
# All values are scaled between 0 and 1.

X = [

    # Normal accounts
    [0.20, 0.25, 0.10, 0.15],
    [0.25, 0.30, 0.12, 0.18],
    [0.30, 0.35, 0.15, 0.20],
    [0.22, 0.28, 0.11, 0.17],
    [0.35, 0.32, 0.18, 0.22],
    [0.28, 0.40, 0.14, 0.20],
    [0.32, 0.38, 0.16, 0.25],
    [0.27, 0.30, 0.13, 0.19],

    # Fraud-like accounts
    [0.85, 0.82, 0.88, 0.90],
    [0.90, 0.78, 0.92, 0.86],
    [0.80, 0.88, 0.85, 0.91],
    [0.88, 0.84, 0.90, 0.87],
    [0.76, 0.80, 0.83, 0.89],
    [0.82, 0.86, 0.88, 0.84],
    [0.91, 0.82, 0.94, 0.92],
    [0.79, 0.89, 0.86, 0.88]
]


# ---------------------------------------------------------------
# 6. TRANSACTION GRAPH
# ---------------------------------------------------------------

edges = [

    # Normal-account transaction group
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 6),
    (5, 7),
    (6, 7),

    # Fraud-account transaction group
    (8, 9),
    (8, 10),
    (9, 11),
    (10, 11),
    (10, 12),
    (11, 13),
    (12, 14),
    (13, 15),
    (14, 15),

    # Cross-group transactions
    (4, 10),
    (7, 13),
    (6, 12)
]


# ---------------------------------------------------------------
# 7. LABELS
# ---------------------------------------------------------------

# 0 = NORMAL
# 1 = FRAUD

true_labels = [
    0, 0, 0, 0,
    0, 0, 0, 0,
    1, 1, 1, 1,
    1, 1, 1, 1
]


# Only a few accounts are verified by a bank analyst.
known = {
    0: 0,
    2: 0,
    8: 1,
    9: 1
}


# ---------------------------------------------------------------
# 8. TRAINING
# ---------------------------------------------------------------

def run_gcn():

    n = len(X)

    # Build graph
    A = build_adjacency(
        n,
        edges
    )

    # Normalize graph
    A_hat = normalize(A)

    # Training indices
    train_idx = sorted(
        known.keys()
    )

    # One-hot labels
    Y = [
        [0.0, 0.0]
        for _ in range(n)
    ]

    for i, label in known.items():
        Y[i][label] = 1.0

    # Create GCN
    model = GCN(
        in_dim=4,
        hidden=6,
        out_dim=2
    )

    epochs = []

    print(
        "Bank Fraud Detection using Vanilla GCN"
    )

    print(
        "Accounts:",
        n,
        "| Transactions:",
        len(edges),
        "| Labeled accounts:",
        len(known)
    )

    print("-" * 70)

    # -----------------------------------------------------------
    # TRAIN
    # -----------------------------------------------------------

    for epoch in range(1, 301):

        P = model.forward(
            A_hat,
            X
        )

        mean_confidence = sum(
            P[i][known[i]]
            for i in train_idx
        ) / len(train_idx)

        model.backward(
            A_hat,
            Y,
            train_idx,
            lr=0.5
        )

        # Accuracy on accounts that were not manually labeled
        test_idx = [
            i
            for i in range(n)
            if i not in known
        ]

        correct = sum(
            1
            for i in test_idx
            if argmax(P[i])
            == true_labels[i]
        )

        accuracy = (
            correct / len(test_idx)
        )

        epochs.append({
            "epoch": epoch,
            "confidence": mean_confidence,
            "accuracy": accuracy
        })

        if (
            epoch == 1
            or epoch % 50 == 0
        ):

            print(
                f"Epoch {epoch:3d} | "
                f"confidence on labeled: "
                f"{mean_confidence:.3f} | "
                f"accuracy on unlabeled: "
                f"{accuracy:.2f}"
            )

    # -----------------------------------------------------------
    # FINAL PREDICTIONS
    # -----------------------------------------------------------

    P = model.forward(
        A_hat,
        X
    )

    print("-" * 70)

    print(
        f"{'Account':<10}"
        f"{'P(Fraud)':>10}   "
        f"{'Predicted':<10}"
        f"{'Actual':<10}"
    )

    for i in range(n):

        predicted = (
            "FRAUD"
            if argmax(P[i]) == 1
            else "NORMAL"
        )

        actual = (
            "FRAUD"
            if true_labels[i] == 1
            else "NORMAL"
        )

        labeled = (
            "(labeled)"
            if i in known
            else ""
        )

        print(
            f"{names[i]:<10}"
            f"{P[i][1]:>10.3f}   "
            f"{predicted:<10}"
            f"{actual:<10}"
            f"{labeled}"
        )

    return {
        "model": model,
        "probabilities": P,
        "epochs": epochs
    }


# ---------------------------------------------------------------
# 9. MAIN
# ---------------------------------------------------------------

if __name__ == "__main__":

    result = run_gcn()
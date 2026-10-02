# ============================================================
# VANILLA GCN - BANK ACCOUNT FRAUD DETECTION
# Implemented from scratch using basic Python
#
# 0 = REAL
# 1 = FRAUD
# ============================================================


# ============================================================
# BANK ACCOUNT DATA
# ============================================================

names = [
    "Account_A",
    "Account_B",
    "Account_C",
    "Account_D",
    "Account_E",
    "Account_F",
    "Account_G",
    "Account_H"
]


# Features:
# [Transaction Amount, Transaction Count, Suspicious Activity]

X = [
    [100, 2, 0],
    [150, 3, 0],
    [200, 4, 0],
    [5000, 25, 1],
    [4500, 20, 1],
    [250, 3, 0],
    [6000, 30, 1],
    [180, 2, 0]
]


# Actual labels
# 0 = REAL
# 1 = FRAUD

true_labels = [
    0,
    0,
    0,
    1,
    1,
    0,
    1,
    0
]


# ============================================================
# TRANSACTION GRAPH
# ============================================================

# Each pair represents a transaction/connection
# between two accounts.

edges = [
    [0, 1],
    [0, 2],
    [1, 2],
    [1, 5],
    [2, 5],

    [3, 4],
    [3, 6],
    [4, 6],
    [4, 7],
    [6, 7]
]


# ============================================================
# MATRIX CREATION
# ============================================================

def create_matrix(rows, columns):

    matrix = []

    for i in range(rows):

        row = []

        for j in range(columns):

            row.append(0.0)

        matrix.append(row)

    return matrix


# ============================================================
# MATRIX MULTIPLICATION
# ============================================================

def matrix_multiply(A, B):

    rows_A = len(A)
    columns_A = len(A[0])
    columns_B = len(B[0])

    result = create_matrix(
        rows_A,
        columns_B
    )

    for i in range(rows_A):

        for j in range(columns_B):

            total = 0.0

            for k in range(columns_A):

                total += (
                    A[i][k] *
                    B[k][j]
                )

            result[i][j] = total

    return result


# ============================================================
# MATRIX TRANSPOSE
# ============================================================

def transpose(A):

    rows = len(A)
    columns = len(A[0])

    result = create_matrix(
        columns,
        rows
    )

    for i in range(rows):

        for j in range(columns):

            result[j][i] = A[i][j]

    return result


# ============================================================
# MATRIX ADDITION
# ============================================================

def matrix_add(A, B):

    rows = len(A)
    columns = len(A[0])

    result = create_matrix(
        rows,
        columns
    )

    for i in range(rows):

        for j in range(columns):

            result[i][j] = (
                A[i][j] +
                B[i][j]
            )

    return result


# ============================================================
# MATRIX SUBTRACTION
# ============================================================

def matrix_subtract(A, B):

    rows = len(A)
    columns = len(A[0])

    result = create_matrix(
        rows,
        columns
    )

    for i in range(rows):

        for j in range(columns):

            result[i][j] = (
                A[i][j] -
                B[i][j]
            )

    return result


# ============================================================
# MATRIX SCALAR MULTIPLICATION
# ============================================================

def scalar_multiply(A, value):

    rows = len(A)
    columns = len(A[0])

    result = create_matrix(
        rows,
        columns
    )

    for i in range(rows):

        for j in range(columns):

            result[i][j] = (
                A[i][j] * value
            )

    return result


# ============================================================
# SQUARE ROOT
# ============================================================

def square_root(value):

    if value <= 0:

        return 0.0

    guess = value

    for i in range(20):

        guess = (
            guess +
            value / guess
        ) / 2

    return guess


# ============================================================
# NORMALIZE FEATURES
# ============================================================

def normalize_features(data):

    rows = len(data)
    columns = len(data[0])

    result = create_matrix(
        rows,
        columns
    )

    for j in range(columns):

        total = 0.0

        for i in range(rows):

            total += data[i][j]

        mean = total / rows


        variance = 0.0

        for i in range(rows):

            difference = (
                data[i][j] - mean
            )

            variance += (
                difference *
                difference
            )

        variance = variance / rows

        standard_deviation = square_root(
            variance
        )


        if standard_deviation == 0:

            standard_deviation = 1.0


        for i in range(rows):

            result[i][j] = (
                data[i][j] - mean
            ) / standard_deviation

    return result


# ============================================================
# CREATE ADJACENCY MATRIX
# ============================================================

def create_adjacency(number_of_nodes, edges):

    A = create_matrix(
        number_of_nodes,
        number_of_nodes
    )


    # Add transaction edges

    for edge in edges:

        source = edge[0]
        destination = edge[1]

        A[source][destination] = 1.0

        A[destination][source] = 1.0


    # Add self-loops

    for i in range(number_of_nodes):

        A[i][i] = 1.0


    return A


# ============================================================
# NORMALIZE ADJACENCY MATRIX
#
# A_hat = D^(-1/2) A D^(-1/2)
# ============================================================

def normalize_adjacency(A):

    n = len(A)

    result = create_matrix(
        n,
        n
    )


    degree = []

    # Calculate degree

    for i in range(n):

        total = 0.0

        for j in range(n):

            total += A[i][j]

        degree.append(total)


    # Calculate normalized adjacency

    for i in range(n):

        for j in range(n):

            if degree[i] == 0:

                result[i][j] = 0.0

            elif degree[j] == 0:

                result[i][j] = 0.0

            elif A[i][j] == 0:

                result[i][j] = 0.0

            else:

                root_i = square_root(
                    degree[i]
                )

                root_j = square_root(
                    degree[j]
                )

                result[i][j] = (
                    A[i][j] /
                    (root_i * root_j)
                )

    return result


# ============================================================
# RELU
# ============================================================

def relu(A):

    rows = len(A)
    columns = len(A[0])

    result = create_matrix(
        rows,
        columns
    )

    for i in range(rows):

        for j in range(columns):

            if A[i][j] > 0:

                result[i][j] = A[i][j]

            else:

                result[i][j] = 0.0

    return result


# ============================================================
# RELU DERIVATIVE
# ============================================================

def relu_derivative(A):

    rows = len(A)
    columns = len(A[0])

    result = create_matrix(
        rows,
        columns
    )

    for i in range(rows):

        for j in range(columns):

            if A[i][j] > 0:

                result[i][j] = 1.0

            else:

                result[i][j] = 0.0

    return result


# ============================================================
# ELEMENT-WISE MULTIPLICATION
# ============================================================

def element_multiply(A, B):

    rows = len(A)
    columns = len(A[0])

    result = create_matrix(
        rows,
        columns
    )

    for i in range(rows):

        for j in range(columns):

            result[i][j] = (
                A[i][j] *
                B[i][j]
            )

    return result


# ============================================================
# SOFTMAX
# ============================================================

def exponential(value):

    # e^x approximation using Taylor series

    result = 1.0

    term = 1.0

    for i in range(1, 30):

        term = (
            term *
            value /
            i
        )

        result += term

    return result


def softmax(row):

    values = []

    for value in row:

        values.append(
            exponential(value)
        )


    total = 0.0

    for value in values:

        total += value


    probabilities = []

    for value in values:

        probabilities.append(
            value / total
        )

    return probabilities


def softmax_matrix(A):

    result = []

    for i in range(len(A)):

        result.append(
            softmax(A[i])
        )

    return result


# ============================================================
# PREDICTION
# ============================================================

def predict(probabilities):

    predictions = []

    for row in probabilities:

        if row[0] >= row[1]:

            predictions.append(0)

        else:

            predictions.append(1)

    return predictions


# ============================================================
# ACCURACY
# ============================================================

def calculate_accuracy(
    predictions,
    labels
):

    correct = 0

    for i in range(len(labels)):

        if predictions[i] == labels[i]:

            correct += 1

    accuracy = (
        correct /
        len(labels)
    ) * 100

    return accuracy


# ============================================================
# CROSS ENTROPY LOSS
# ============================================================

def calculate_loss(
    probabilities,
    labels
):

    total_loss = 0.0

    for i in range(len(labels)):

        probability = probabilities[i][
            labels[i]
        ]

        if probability < 0.000001:

            probability = 0.000001

        # Manual approximation of -log(x)
        #
        # log(x) = 2 * (y + y^3/3 + y^5/5 ...)
        # where y = (x-1)/(x+1)

        y = (
            probability - 1
        ) / (
            probability + 1
        )

        log_value = 0.0

        power = y

        for k in range(1, 40, 2):

            log_value += (
                power / k
            )

            power *= y * y

        log_value *= 2

        total_loss += -log_value

    return total_loss / len(labels)


# ============================================================
# INITIALIZE WEIGHTS
# ============================================================

def initialize_weights():

    W1 = [

        [0.10, 0.20, 0.30, 0.40],

        [0.20, 0.30, 0.40, 0.10],

        [0.30, 0.40, 0.10, 0.20]

    ]


    W2 = [

        [0.20, 0.10],

        [0.30, 0.20],

        [0.10, 0.30],

        [0.20, 0.40]

    ]


    return W1, W2


# ============================================================
# GCN FORWARD PROPAGATION
#
# H1 = ReLU(A_hat X W1)
#
# Z = A_hat H1 W2
#
# P = Softmax(Z)
# ============================================================

def forward(
    X_data,
    A_hat,
    W1,
    W2
):

    # A_hat X

    AX = matrix_multiply(
        A_hat,
        X_data
    )


    # A_hat X W1

    H1_before_relu = matrix_multiply(
        AX,
        W1
    )


    # ReLU

    H1 = relu(
        H1_before_relu
    )


    # A_hat H1

    AH1 = matrix_multiply(
        A_hat,
        H1
    )


    # A_hat H1 W2

    Z = matrix_multiply(
        AH1,
        W2
    )


    # Softmax

    probabilities = softmax_matrix(
        Z
    )


    return (
        H1_before_relu,
        H1,
        AH1,
        Z,
        probabilities
    )


# ============================================================
# GCN TRAINING
#
# Manual gradient descent
# ============================================================

def train_gcn(
    X_data,
    labels,
    A_hat,
    epochs,
    learning_rate
):

    W1, W2 = initialize_weights()


    accuracy_history = []

    loss_history = []


    for epoch in range(epochs):

        # ----------------------------------------------------
        # FORWARD PASS
        # ----------------------------------------------------

        (
            H1_before_relu,
            H1,
            AH1,
            Z,
            probabilities
        ) = forward(
            X_data,
            A_hat,
            W1,
            W2
        )


        # ----------------------------------------------------
        # PREDICTIONS
        # ----------------------------------------------------

        predictions = predict(
            probabilities
        )


        # ----------------------------------------------------
        # LOSS
        # ----------------------------------------------------

        loss = calculate_loss(
            probabilities,
            labels
        )


        # ----------------------------------------------------
        # ACCURACY
        # ----------------------------------------------------

        accuracy = calculate_accuracy(
            predictions,
            labels
        )


        accuracy_history.append(
            accuracy
        )

        loss_history.append(
            loss
        )


        # ----------------------------------------------------
        # OUTPUT ERROR
        # ----------------------------------------------------

        dZ = create_matrix(
            len(labels),
            2
        )


        for i in range(len(labels)):

            for j in range(2):

                target = 0.0

                if labels[i] == j:

                    target = 1.0

                dZ[i][j] = (
                    probabilities[i][j]
                    - target
                )


        # ----------------------------------------------------
        # dW2
        #
        # dW2 = (A_hat H1)^T dZ
        # ----------------------------------------------------

        AH1_T = transpose(
            AH1
        )

        dW2 = matrix_multiply(
            AH1_T,
            dZ
        )


        dW2 = scalar_multiply(
            dW2,
            1.0 / len(labels)
        )


        # ----------------------------------------------------
        # BACKPROPAGATE TO H1
        #
        # dH1 = A_hat^T dZ W2^T
        # ----------------------------------------------------

        A_T = transpose(
            A_hat
        )

        W2_T = transpose(
            W2
        )


        dH1_temp = matrix_multiply(
            dZ,
            W2_T
        )


        dH1 = matrix_multiply(
            A_T,
            dH1_temp
        )


        # ----------------------------------------------------
        # ReLU derivative
        # ----------------------------------------------------

        relu_grad = relu_derivative(
            H1_before_relu
        )


        dH1 = element_multiply(
            dH1,
            relu_grad
        )


        # ----------------------------------------------------
        # dW1
        #
        # dW1 = (A_hat X)^T dH1
        # ----------------------------------------------------

        AX = matrix_multiply(
            A_hat,
            X_data
        )

        AX_T = transpose(
            AX
        )

        dW1 = matrix_multiply(
            AX_T,
            dH1
        )


        dW1 = scalar_multiply(
            dW1,
            1.0 / len(labels)
        )


        # ----------------------------------------------------
        # UPDATE W1
        # ----------------------------------------------------

        for i in range(len(W1)):

            for j in range(len(W1[0])):

                W1[i][j] -= (
                    learning_rate *
                    dW1[i][j]
                )


        # ----------------------------------------------------
        # UPDATE W2
        # ----------------------------------------------------

        for i in range(len(W2)):

            for j in range(len(W2[0])):

                W2[i][j] -= (
                    learning_rate *
                    dW2[i][j]
                )


    return (
        W1,
        W2,
        accuracy_history,
        loss_history
    )


# ============================================================
# MAIN GCN FUNCTION
# ============================================================

def run_gcn(
    epochs=100,
    learning_rate=0.01
):

    # --------------------------------------------------------
    # STEP 1
    # Normalize account features
    # --------------------------------------------------------

    X_normalized = normalize_features(
        X
    )


    # --------------------------------------------------------
    # STEP 2
    # Create adjacency matrix
    # --------------------------------------------------------

    A = create_adjacency(
        len(X),
        edges
    )


    # --------------------------------------------------------
    # STEP 3
    # Normalize adjacency matrix
    # --------------------------------------------------------

    A_hat = normalize_adjacency(
        A
    )


    # --------------------------------------------------------
    # STEP 4
    # Train GCN
    # --------------------------------------------------------

    (
        W1,
        W2,
        accuracy_history,
        loss_history
    ) = train_gcn(
        X_normalized,
        true_labels,
        A_hat,
        epochs,
        learning_rate
    )


    # --------------------------------------------------------
    # STEP 5
    # Final forward pass
    # --------------------------------------------------------

    (
        H1_before_relu,
        H1,
        AH1,
        Z,
        probabilities
    ) = forward(
        X_normalized,
        A_hat,
        W1,
        W2
    )


    # --------------------------------------------------------
    # STEP 6
    # Final predictions
    # --------------------------------------------------------

    predictions = predict(
        probabilities
    )


    # --------------------------------------------------------
    # STEP 7
    # Final accuracy
    # --------------------------------------------------------

    accuracy = calculate_accuracy(
        predictions,
        true_labels
    )


    # --------------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------------

    return {

        "predictions": predictions,

        "probabilities": probabilities,

        "accuracy": accuracy,

        "accuracy_history": accuracy_history,

        "loss_history": loss_history,

        "W1": W1,

        "W2": W2

    }


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    result = run_gcn()

    predictions = result["predictions"]

    probabilities = result["probabilities"]

    accuracy = result["accuracy"]


    print()
    print("==============================================")
    print("       GCN BANK FRAUD DETECTION")
    print("==============================================")
    print()


    for i in range(len(names)):

        print("----------------------------------------------")

        print(
            "Account:",
            names[i]
        )

        print(
            "Transaction Amount:",
            X[i][0]
        )

        print(
            "Transaction Count:",
            X[i][1]
        )

        print(
            "Suspicious Activity:",
            X[i][2]
        )

        print(
            "Real Probability:",
            round(
                probabilities[i][0] * 100,
                2
            ),
            "%"
        )

        print(
            "Fraud Probability:",
            round(
                probabilities[i][1] * 100,
                2
            ),
            "%"
        )


        if predictions[i] == 1:

            print(
                "Prediction: FRAUD"
            )

        else:

            print(
                "Prediction: REAL"
            )


    print("----------------------------------------------")

    print(
        "Overall Accuracy:",
        round(
            accuracy,
            2
        ),
        "%"
    )

    print()
    print("==============================================")
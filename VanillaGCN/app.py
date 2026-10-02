import streamlit as st
import pandas as pd

from vanillaGCN import (
    run_gcn,
    names,
    X,
    true_labels
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="GCN Bank Fraud Detection",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# RUN GCN
# ============================================================

result = run_gcn()

predictions = result["predictions"]
probabilities = result["probabilities"]
accuracy = result["accuracy"]
accuracy_history = result["accuracy_history"]
loss_history = result["loss_history"]


# ============================================================
# CREATE RESULTS DATAFRAME
# ============================================================

rows = []

for i in range(len(names)):

    if predictions[i] == 1:
        predicted = "FRAUD"
    else:
        predicted = "REAL"

    if true_labels[i] == 1:
        actual = "FRAUD"
    else:
        actual = "REAL"

    rows.append({
        "Account": names[i],
        "Transaction Amount": X[i][0],
        "Transaction Count": X[i][1],
        "Suspicious Activity": X[i][2],
        "P(REAL)": probabilities[i][0],
        "P(FRAUD)": probabilities[i][1],
        "Predicted": predicted,
        "Actual": actual
    })


results_df = pd.DataFrame(rows)


# ============================================================
# HEADER
# ============================================================

st.title("🏦 Bank Account Fraud Detection using GCN")

st.caption(
    "Vanilla Graph Convolutional Network, pure Python | "
    "Algorithm Design assignment"
)


# ============================================================
# SUMMARY METRICS
# ============================================================

correct = 0

for i in range(len(names)):

    if predictions[i] == true_labels[i]:
        correct += 1


total = len(names)

fraud_count = 0
real_count = 0

for prediction in predictions:

    if prediction == 1:
        fraud_count += 1
    else:
        real_count += 1


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Accounts",
        total
    )


with c2:

    st.metric(
        "Predicted FRAUD",
        fraud_count
    )


with c3:

    st.metric(
        "Predicted REAL",
        real_count
    )


with c4:

    st.metric(
        "Correct",
        f"{correct}/{total}"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📄 Model Information",
        "📊 Results",
        "📈 Training",
        "🔎 Check an Account"
    ]
)


# ============================================================
# TAB 1 - MODEL INFORMATION
# ============================================================

with tab1:

    st.subheader("GCN Model Information")

    st.write(
        "This application uses a Graph Convolutional Network "
        "implemented from scratch using basic Python."
    )

    st.write("### Graph Information")

    info1, info2, info3 = st.columns(3)

    with info1:

        st.metric(
            "Number of Accounts",
            len(names)
        )

    with info2:

        from vanillaGCN import edges

        st.metric(
            "Transaction Connections",
            len(edges)
        )

    with info3:

        st.metric(
            "Features per Account",
            len(X[0])
        )


    st.write("### Account Features")

    st.write(
        """
        Each bank account has three input features:

        - Transaction Amount
        - Transaction Count
        - Suspicious Activity
        """
    )


    st.write("### GCN Process")

    st.code(
        """
Account Features
        ↓
Feature Normalization
        ↓
Transaction Graph
        ↓
Adjacency Matrix
        ↓
Normalized Adjacency Matrix
        ↓
GCN Layer 1
        ↓
ReLU Activation
        ↓
GCN Layer 2
        ↓
Softmax
        ↓
REAL / FRAUD Prediction
        """,
        language="text"
    )


    st.write("### Classification")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            "REAL\n\nClass 0"
        )

    with col2:

        st.error(
            "FRAUD\n\nClass 1"
        )


# ============================================================
# TAB 2 - RESULTS
# ============================================================

with tab2:

    st.subheader("Probability of Fraud for Each Account")

    chart_data = results_df.set_index(
        "Account"
    )[["P(FRAUD)"]]

    st.bar_chart(
        chart_data
    )


    st.subheader("Account Results")


    # --------------------------------------------------------
    # Format dataframe for display
    # --------------------------------------------------------

    display_df = results_df.copy()

    display_df["P(REAL)"] = display_df["P(REAL)"].apply(
        lambda x: f"{x:.3f}"
    )

    display_df["P(FRAUD)"] = display_df["P(FRAUD)"].apply(
        lambda x: f"{x:.3f}"
    )


    # --------------------------------------------------------
    # Color rows
    # --------------------------------------------------------

    def color_row(row):

        if row["Predicted"] == "FRAUD":

            return [
                "background-color: #fde8ea; color: black"
            ] * len(row)

        else:

            return [
                "background-color: #e3f4f1; color: black"
            ] * len(row)


    styled_df = display_df.style.apply(
        color_row,
        axis=1
    )


    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    st.subheader("Model Accuracy")

    st.progress(
        accuracy / 100,
        text=f"Accuracy = {accuracy:.2f}%"
    )


# ============================================================
# TAB 3 - TRAINING
# ============================================================

with tab3:

    st.subheader("Training Progress")


    # --------------------------------------------------------
    # Training summary
    # --------------------------------------------------------

    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "Number of Epochs",
            len(accuracy_history)
        )


    with c2:

        st.metric(
            "Final Accuracy",
            f"{accuracy:.2f}%"
        )


    # --------------------------------------------------------
    # Accuracy graph
    # --------------------------------------------------------

    st.write("### Accuracy During Training")

    accuracy_df = pd.DataFrame(
        {
            "Accuracy": accuracy_history
        }
    )

    st.line_chart(
        accuracy_df
    )


    # --------------------------------------------------------
    # Loss graph
    # --------------------------------------------------------

    st.write("### Loss During Training")

    loss_df = pd.DataFrame(
        {
            "Loss": loss_history
        }
    )

    st.line_chart(
        loss_df
    )


    # --------------------------------------------------------
    # Training table
    # --------------------------------------------------------

    st.write("### Training Values")

    training_df = pd.DataFrame(
        {
            "Epoch": range(
                1,
                len(accuracy_history) + 1
            ),
            "Accuracy": accuracy_history,
            "Loss": loss_history
        }
    )


    st.dataframe(
        training_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 4 - CHECK ONE ACCOUNT
# ============================================================

with tab4:

    st.subheader("Check an Account")


    selected_account = st.selectbox(
        "Choose an account",
        names
    )


    # --------------------------------------------------------
    # Find selected account
    # --------------------------------------------------------

    index = names.index(
        selected_account
    )


    # --------------------------------------------------------
    # Account information
    # --------------------------------------------------------

    st.write("### Account Details")


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Transaction Amount",
            X[index][0]
        )


    with c2:

        st.metric(
            "Transaction Count",
            X[index][1]
        )


    with c3:

        st.metric(
            "Suspicious Activity",
            X[index][2]
        )


    # --------------------------------------------------------
    # Probabilities
    # --------------------------------------------------------

    real_probability = probabilities[index][0]

    fraud_probability = probabilities[index][1]


    st.write("### Prediction Probabilities")


    p1, p2 = st.columns(2)


    with p1:

        st.write(
            f"REAL: {real_probability * 100:.2f}%"
        )

        st.progress(
            real_probability
        )


    with p2:

        st.write(
            f"FRAUD: {fraud_probability * 100:.2f}%"
        )

        st.progress(
            fraud_probability
        )


    # --------------------------------------------------------
    # Final prediction
    # --------------------------------------------------------

    st.write("### Final Prediction")


    if predictions[index] == 1:

        st.error(
            f"{selected_account} is predicted as FRAUD"
        )

    else:

        st.success(
            f"{selected_account} is predicted as REAL"
        )


    # --------------------------------------------------------
    # Actual label
    # --------------------------------------------------------

    if true_labels[index] == 1:

        actual_label = "FRAUD"

    else:

        actual_label = "REAL"


    st.write(
        f"Actual label: **{actual_label}**"
    )


    # --------------------------------------------------------
    # Correct / Incorrect
    # --------------------------------------------------------

    if predictions[index] == true_labels[index]:

        st.success(
            "Prediction is correct."
        )

    else:

        st.warning(
            "Prediction is different from the actual label."
        )
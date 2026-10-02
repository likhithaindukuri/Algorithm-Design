"""
Streamlit web page for Bank Fraud Detection using Vanilla GCN.

Run:

    streamlit run app.py

The program automatically runs the GCN and displays:
- Account statistics
- Fraud probabilities
- Prediction table
- Training progress
- Individual account checking
"""

import streamlit as st
import pandas as pd

from vanillaGCN import (
    run_gcn,
    names,
    true_labels,
    known
)


# ---------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------

st.set_page_config(
    page_title="GCN Bank Fraud Detection",
    page_icon="🏦",
    layout="wide"
)


# ---------------------------------------------------------------
# Run GCN
# ---------------------------------------------------------------

@st.cache_data
def get_results():

    result = run_gcn()

    probabilities = result["probabilities"]
    epochs = result["epochs"]

    rows = []

    for i in range(len(names)):

        p_fraud = probabilities[i][1]

        predicted = (
            "FRAUD"
            if probabilities[i][1]
            > probabilities[i][0]
            else "NORMAL"
        )

        actual = (
            "FRAUD"
            if true_labels[i] == 1
            else "NORMAL"
        )

        rows.append({
            "Account": names[i],
            "P(Fraud)": p_fraud,
            "Predicted": predicted,
            "Actual": actual,
            "Labeled by Analyst":
                "Yes" if i in known else "No"
        })

    results_df = pd.DataFrame(rows)

    epochs_df = pd.DataFrame(epochs)

    return results_df, epochs_df


results_df, epochs_df = get_results()


# ---------------------------------------------------------------
# Title
# ---------------------------------------------------------------

st.title("🏦 Bank Fraud Detection using GCN")

st.caption(
    "Vanilla Graph Convolutional Network, pure Python | "
    "Algorithm Design assignment"
)


# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------

correct = int(
    (
        results_df["Predicted"]
        ==
        results_df["Actual"]
    ).sum()
)

total = len(results_df)

fraud_count = int(
    (
        results_df["Predicted"]
        == "FRAUD"
    ).sum()
)

normal_count = int(
    (
        results_df["Predicted"]
        == "NORMAL"
    ).sum()
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Bank Accounts",
    total
)

c2.metric(
    "Predicted FRAUD",
    fraud_count
)

c3.metric(
    "Predicted NORMAL",
    normal_count
)

c4.metric(
    "Correct",
    f"{correct}/{total}"
)


# ---------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Results",
        "📈 Training",
        "🔎 Check an Account",
        "ℹ️ About GCN"
    ]
)


# ---------------------------------------------------------------
# TAB 1 - RESULTS
# ---------------------------------------------------------------

with tab1:

    st.subheader(
        "Fraud Probability for Each Bank Account"
    )

    st.bar_chart(
        results_df.set_index("Account")[
            "P(Fraud)"
        ]
    )

    st.subheader(
        "Account Classification"
    )

    def color_row(row):

        if row["Predicted"] == "FRAUD":

            color = "#fde8ea"

        else:

            color = "#e3f4f1"

        return [
            f"background-color: {color}; color: black"
        ] * len(row)

    styled_df = (
        results_df.style
        .apply(
            color_row,
            axis=1
        )
        .format({
            "P(Fraud)": "{:.3f}"
        })
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------------
# TAB 2 - TRAINING
# ---------------------------------------------------------------

with tab2:

    st.subheader(
        "GCN Training Progress"
    )

    st.line_chart(
        epochs_df.set_index("epoch")[
            [
                "confidence",
                "accuracy"
            ]
        ]
    )

    st.dataframe(
        epochs_df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------------
# TAB 3 - CHECK ACCOUNT
# ---------------------------------------------------------------

with tab3:

    st.subheader(
        "Check One Bank Account"
    )

    selected_account = st.selectbox(
        "Choose an account",
        results_df["Account"].tolist()
    )

    row = results_df[
        results_df["Account"]
        == selected_account
    ].iloc[0]

    fraud_probability = float(
        row["P(Fraud)"]
    )

    st.progress(
        fraud_probability,
        text=(
            f"P(Fraud) = "
            f"{fraud_probability:.3f}"
        )
    )

    if row["Predicted"] == "FRAUD":

        st.error(
            f"{selected_account} is predicted "
            f"as FRAUD "
            f"(actual: {row['Actual']})"
        )

    else:

        st.success(
            f"{selected_account} is predicted "
            f"as NORMAL "
            f"(actual: {row['Actual']})"
        )

    st.write(
        "Labeled by bank analyst before training: "
        f"**{row['Labeled by Analyst']}**"
    )


# ---------------------------------------------------------------
# TAB 4 - ABOUT
# ---------------------------------------------------------------

with tab4:

    st.subheader(
        "How the Vanilla GCN Works"
    )

    st.write(
        """
        This project detects potentially fraudulent bank accounts
        using a Graph Convolutional Network.

        **Graph representation**

        - Each node represents a bank account.
        - Each edge represents a transaction between two accounts.
        - Node features describe account transaction behaviour.

        **Node features**

        1. Transaction frequency
        2. Average transaction amount
        3. Unusual transaction ratio
        4. New beneficiary ratio

        **GCN process**

        Account features are first propagated through the transaction
        graph. The GCN then learns patterns from a small number of
        analyst-labelled accounts.

        The final layer produces two probabilities:

        - NORMAL
        - FRAUD

        The account is classified according to the higher probability.

        This implementation is written from scratch using Python
        matrix operations without NumPy, PyTorch, TensorFlow,
        or other machine-learning libraries.
        """
    )
import streamlit as st
import tensorflow as tf
import pandas as pd
import numpy as np
import time
from pickle import load

# Page config setup
st.set_page_config(
    page_title="Bean Predictor",
    page_icon=":seedling:",
    layout="wide",
)
# Mapping ids to classes
idx2class = {
    0: "BARBUNYA",
    1: "BOMBAY",
    2: "CALI",
    3: "DERMASON",
    4: "HOROZ",
    5: "SEKER",
    6: "SIRA",
}


@st.cache(suppress_st_warning=True)
def predict(feats, model):
    """
    This method makes predicitons using the model

    Parameters
    ----------
    feats: 2d array of shape (n_samples, 16)
    model: the scikit-learn model

    Returns
    -------
    pred_df: pd.Dataframe containing labels and confindence values
    """

    predictions = []
    probs = []

    start = time.time()

    with st.spinner("Classifying...."):
        preds = model.predict(feats)
        prob = model.predict_proba(feats)
        for pred in preds:
            predictions.append(pred)
            probs.append(round(np.max(prob) * 100, 2))

    end = time.time()

    st.success(f"Prediction done in: {round(end-start, 2)}s")

    pred_df = pd.DataFrame({"labels": predictions, "confidence": probs})

    return pred_df


def batch_pred(file):
    """
    Funciton to make batch prediction from csv file
    """

    pred_df = pd.DataFrame()

    df = pd.read_csv(file)

    with st.expander("Check your uploaded csv"):
        st.dataframe(df)

    r5 = st.columns(5)
    btn = r5[2].button("Predict")

    if btn:
        pred_df = predict(feats=df.values, model=model)

        st.dataframe(pred_df)

        if len(pred_df) != 0:
            csv = pred_df.to_csv(index=False)
            st.download_button(
                label="Download predictions",
                data=csv,
                file_name="preds.csv",
            )


# ----------------------------------------- UI ---------------------------------------------

# Sidebars
# Title "Dry bean Classifier"

st.markdown(
    """
    <center>
        <h1>
            <i>Dry Bean Classifier</i>
        </h2>
    </center>""",
    unsafe_allow_html=True,
)


st.sidebar.image("beans.jpg")


with st.expander(label="Using the app"):
    st.write(
        """
        1. Choose the type of prediction form the sidebar: Single or Batch
            - Batch prediciton is done using a .csv file or just paste the url to a .csv file. 
            - Single prediction is done using a form. 
        2. Choose the model: *Light Gradient Boosting Machine* or *Feed-forward-NN* from the sidebar
        3. Click on predict
        """
    )


# Type of predicition
pred_type = st.sidebar.radio(
    "Type of predition",
    options=["Single", "Batch"],
    index=0,
    help="The type of prediction: Single prediction using form or batch prediction using csv file",
)

# Single prediction done using a form
model = None
pred_df = pd.DataFrame()

with open("tuned_rf_model.pkl", "rb") as f:
    model = load(f)

if pred_type == "Single":

    with st.form("Dry Bean Classification"):
        st.markdown(
            """
            <h2>
                <center>
                    Enter Feature values
                </center>
            </h2>

            <center>
                <i>
                    The form has already been filled up with defaults
                    for ease of demonstration.
                </i>
            </center>
            <br>
            """,
            unsafe_allow_html=True,
        )

        r1 = st.columns(4)
        r2 = st.columns(4)
        r3 = st.columns(4)
        r4 = st.columns(4)
        r5 = st.columns(5)

        # Row 1
        Area = r1[0].text_input("Area", value="40100")
        Perimeter = r1[1].text_input("Perimeter", value="717.877")
        MajorAxisLength = r1[2].text_input("MajorAxisLength", value="256.6991625")
        MinorAxisLength = r1[3].text_input("MinorAxisLength", value="216.8884621")

        # Row 2
        AspectRatio = r2[0].text_input("AspectRatio", value="1.190425909")
        Eccentricity = r2[1].text_input("Eccentricity", value="0.524706845")
        ConvexArea = r2[2].text_input("ConvexArea", value="39925")
        EquiDiameter = r2[3].text_input("EquiDiameter", value="224.6758334")

        # Row 3
        Extent = r3[0].text_input("Extent", value="0.765857899")
        Solidity = r3[1].text_input("Solidity", value="0.979486704")
        Roundness = r3[2].text_input("Roundness", value="0.92875453")
        Compactness = r3[3].text_input("Compactness", value="0.927781514")

        # Row 4
        ShapeFactor1 = r4[0].text_input("ShapeFactor1", value="0.005567479")
        ShapeFactor2 = r4[1].text_input("ShapeFactor2", value="0.00296414")
        ShapeFactor3 = r4[2].text_input("ShapeFactor3", value="0.896825218")
        ShapeFactor4 = r4[3].text_input("ShapeFactor4", value="0.987852072")

        submit_res = r5[2].form_submit_button("Predict")

        feats = [
            Area,
            Perimeter,
            MajorAxisLength,
            MinorAxisLength,
            AspectRatio,
            Eccentricity,
            ConvexArea,
            EquiDiameter,
            Extent,
            Solidity,
            Roundness,
            Compactness,
            ShapeFactor1,
            ShapeFactor2,
            ShapeFactor3,
            ShapeFactor4,
        ]

        if submit_res:
            count = 0
            for feat in feats:
                if feat == "":
                    count += 1

            if count != 0:
                st.warning("One or more fields are left blank!")
            else:
                try:
                    feats = [float(feat) for feat in feats]
                except:
                    st.warning("Only int or float values are allowed!")
                    st.stop()
                pred_print = """
                <h2>
                    <center>
                    The predicted class is {} 
                    with a confidence of: {}%
                    </center>
                </h2>                
                """

                pred_df = predict(feats=[feats], model=model)

                st.markdown(
                    pred_print.format(pred_df.labels[0], pred_df.confidence[0]),
                    unsafe_allow_html=True,
                )

    if len(pred_df) != 0:
        csv = pred_df.to_csv(index=False)
        st.download_button(
            label="Download predictions", data=csv, file_name="preds.csv"
        )

else:
    select = st.sidebar.radio(
        """
        Upload CSV or paste a URL
        """,
        options=["Upload-CSV", "Paste-URL"],
        index=0,
    )

    url = "https://feat-files.s3.us-east-2.amazonaws.com/full_feats_test_tiny.csv"

    if select == "Upload-CSV":

        file_uploader = st.file_uploader("")

        if file_uploader is None:
            st.info(
                f"""
                👆 Upload a .csv file first. Sample to try: [feats.csv]({url})   
                """
            )
        else:
            batch_pred(file_uploader)

    else:
        url_input = st.text_input(
            "Paste .csv file URL",
            placeholder="Paste URL here....",
        )

        if url_input:
            batch_pred(url_input)
        else:
            st.info(
                f"""
                👆 Sample url: {url}   
                """
            )

    if len(pred_df) != 0:
        csv = pred_df.to_csv(index=False)
        st.download_button(
            label="Download predictions", data=csv, file_name="preds.csv"
        )

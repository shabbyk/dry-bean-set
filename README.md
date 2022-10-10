# DryBeanClassification

This is deployed at [link](https://shabbyk-dry-bean-set-app-aec6nk.streamlitapp.com/)

It has two ways to make classification prediction:

1. Single Prediction:
   The form is pre-filled with default values for demonstration purpose.
2. Batch Prediction
   We can also use a .csv file or a link that points to a csv file for doing
   prediction in bulk.

We can also download the predictions using download option after clicking the predict button.

Here we are serving the model along with the app so the app prediction is little slow, given more time we can deploy the model in some container like docker and use heroku to render the model
so that the call is just an api call to predict the class.

# Using the app locally

1. Install all the requirements: pip install -r requirements.txt
2. Now, just do: streamlit run app.py and it's up on local host!

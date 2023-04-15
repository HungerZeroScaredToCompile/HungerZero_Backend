import pickle
from joblib import load
import sklearn
print(sklearn.__version__)
# load model and vectorizer
model = load('model.joblib')
cv = load('cv.joblib')

# #model for sentiment analysis
# model=pickle.load(open('NLP-Sentiment_Analysis.pkl','rb'))
# cv = pickle.load(open('cv.pkl','rb'))


content=["the food was bad"]
result = model.predict(cv.transform(content))
if(result==1):
    print("Postive Response")
else:
    print("Negative Response")
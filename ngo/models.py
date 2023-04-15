from django.db import models
from LoginReg.models import User
from joblib import load
import pickle

# load model and vectorizer
# model = load('model.joblib')
# cv = load('cv.joblib')

# #model for sentiment analysis
model=pickle.load(open('NLP-Sentiment_Analysis.pkl','rb'))
cv = pickle.load(open('cv.pkl','rb'))

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=20,unique=True,default='',blank=True,null=True)
    company_name=models.CharField(max_length=100,blank=True,null=True)
    company_domain=models.CharField(max_length=100,blank=True,null=True)
    about_us = models.TextField(max_length=1000,null=True,blank=True)
    profile_pic=models.ImageField(null=True,blank=True)
    email=models.EmailField(max_length=100,blank=True,null=True)
    phone=models.CharField(max_length=10,blank=True,null=True)
    address=models.TextField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.company_name


class Stats(models.Model):
    name=models.ForeignKey(Profile,default=None,on_delete=models.CASCADE)
    no_of_volunteers=models.IntegerField()
    no_of_donations=models.IntegerField()
    no_of_ppl_helped=models.IntegerField()


class Feedback(models.Model):
    name=models.CharField(max_length=100,default=None)
    ratings=models.IntegerField()
    description=models.TextField(max_length=500)
    fbanalysis = models.CharField(max_length=100,null=True,blank=True) 

    def fbcheck(self):
        content=[self.description]
        result = model.predict(cv.transform(content))
        if(result==1):
            answer = "Postive Response"
        else:
            answer = "Negative Response"

        return answer

    def save(self,*args,**kwargs):
        self.fbanalysis=self.fbcheck
        super(Feedback, self).save(*args,**kwargs)
    

# class NewVolunteers(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name= models.CharField(max_length=100)
#     typeofwork=models.CharField(max_length=100)
#     why=models.TextField(max_length=)



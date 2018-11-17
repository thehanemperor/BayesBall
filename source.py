import csv
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB




def main():
    try:
        cnx = mysql.connector.connect(user='capstoneAdmin', password='12345678',
                                  host='ec2-52-6-86-207.compute-1.amazonaws.com',
                                  database='bayesball')

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        
    m = cnx.cursor()

    yearBreakdown_dataset = "SELECT id, Rdiff, SRS, R_G, R, RBI, OBP, OPSP, RA, ERA, SV, HA, ER, ERAP, WHIP, Outcome FROM yearBreakdown;"
    m.execute(yearBreakdown_dataset)
    result = m.fetchall()
    
    fp = open("yearBreakdown.csv","w")
    myFile = csv.writer(fp, lineterminator='\n')
    myFile.writerow(['id','Rdiff','SRS','R_G','R','RBI','OBP','OPSP','RA','ERA','SV','HA','ER','ERAP','WHIP','Outcome'])
    
    myFile.writerows(result)
    data = pd.read_csv("yearBreakdown.csv")
    # Convert categorical variable to numeric
    #print(data.iloc[:,3])
    data=data[["Rdiff",
          "SRS","R_G","R","RBI","OBP","OPSP","RA","ERA","SV","HA","ER","ERAP","WHIP","Outcome"]].dropna(axis=0, how='any')
    # Split dataset in training and test datasets
    X_train, X_test = train_test_split(data, test_size=0.3, random_state=int(time.time()))
    # Instantiate the classifier
    gnb = GaussianNB()
    used_features =[
          "Rdiff",
          "SRS","R_G","R","RBI","OBP","OPSP","RA","ERA","SV","HA","ER","ERAP","WHIP"
          ]
    
    gnb.fit(
            X_train[used_features].values,
            X_train["Outcome"]
    )
    
    y_pred = gnb.predict(X_test[used_features])
    
    
    # Print results
    print("Number of mislabeled points out of a total {} points : {}, performance {:05.2f}%"
          .format(
              X_test.shape[0],
              (X_test["Outcome"] != y_pred).sum(),
              100*(1-(X_test["Outcome"] != y_pred).sum()/X_test.shape[0])
    ))
    
    
main()

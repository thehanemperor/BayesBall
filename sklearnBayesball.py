import csv
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

#Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import random
import sys

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

    team1=""
    team2=""
    
    if(len(sys.argv)==3):
        team1=sys.argv[1]
        team2=sys.argv[2]
        predicted_home_game_dataset = "SELECT id, Rdiff, SRS, R_G, R, RBI, OBP, OPSP, RA, ERA, SV, HA, ER, ERAP, WHIP FROM yearBreakdown WHERE home_team='" + team1 +"' LIMIT 1;"
        predicted_opponent_game_dataset = "SELECT id, Rdiff, SRS, R_G, R, RBI, OBP, OPSP, RA, ERA, SV, HA, ER, ERAP, WHIP FROM yearBreakdown WHERE home_team='"+ team2+"' LIMIT 1;"
       
        m.execute(predicted_home_game_dataset)
        predicted_game_dataset = m.fetchall()
        
        m.execute(predicted_opponent_game_dataset)
        predicted_game_dataset += m.fetchall()
        
        fpr = open("predictYearBreakdown.csv","w")
        pFile = csv.writer(fpr, lineterminator='\n')
        pFile.writerow(['id','Rdiff','SRS','R_G','R','RBI','OBP','OPSP','RA','ERA','SV','HA','ER','ERAP','WHIP'])
        pFile.writerows(predicted_game_dataset)
    
        return 

    yearBreakdown_dataset = "SELECT id, Rdiff, SRS, R_G, R, RBI, OBP, OPSP, RA, ERA, SV, HA, ER, ERAP, WHIP, opponent_Rdiff, opponent_SRS ,opponent_R_G ,opponent_R ,opponent_RBI, opponent_OBP ,opponent_OPSP ,opponent_RA,opponent_ERA ,opponent_SV ,opponent_HA, opponent_ER, opponent_ERAP,opponent_WHIP, Outcome FROM yearBreakdown;"
    m.execute(yearBreakdown_dataset)
    result = m.fetchall()
    
    fp = open("yearBreakdown2.csv","w")
    myFile = csv.writer(fp, lineterminator='\n')
    myFile.writerow(['id','Rdiff','SRS','R_G','R','RBI','OBP','OPSP','RA','ERA','SV','HA','ER','ERAP','WHIP', 'opponent_Rdiff', 'opponent_SRS' ,'opponent_R_G' ,'opponent_R' ,'opponent_RBI', 'opponent_OBP' ,'opponent_OPSP' ,'opponent_RA','opponent_ERA' ,'opponent_SV' ,'opponent_HA', 'opponent_ER', 'opponent_ERAP','opponent_WHIP','Outcome'])
    myFile.writerows(result)
    data = pd.read_csv("yearBreakdown2.csv")
    # Convert categorical variable to numeric
    #print(data.iloc[:,3])
    data=data[["Rdiff",
          "SRS","R_G","R","RBI","OBP","OPSP","RA","ERA","SV","HA","ER","ERAP","WHIP",'opponent_Rdiff', 'opponent_SRS' ,'opponent_R_G' ,'opponent_R' ,'opponent_RBI', 'opponent_OBP' ,'opponent_OPSP' ,'opponent_RA','opponent_ERA' ,'opponent_SV' ,'opponent_HA', 'opponent_ER', 'opponent_ERAP','opponent_WHIP',"Outcome"]].dropna(axis=0, how='any')
    # Split dataset in training and test datasets
    RunNaiveBayes(data)
    
    #RunLinearRegression(data)
    
    RunLogisticRegression(data)
    
    #RandomPredictor(data)
    

def RunNaiveBayes(data):
    print("Running Naive Bayes on Dataset\n")
    X_train, X_test = train_test_split(data, test_size=0.33, random_state=int(time.time()))
    # Instantiate the classifier
    gnb = GaussianNB()
    used_features =[
          "Rdiff",
          "SRS","R_G","R","RBI","OBP","OPSP","RA","ERA","SV","HA","ER","ERAP","WHIP",'opponent_Rdiff', 'opponent_SRS' ,'opponent_R_G' ,'opponent_R' ,'opponent_RBI', 'opponent_OBP' ,'opponent_OPSP' ,'opponent_RA','opponent_ERA' ,'opponent_SV' ,'opponent_HA', 'opponent_ER', 'opponent_ERAP','opponent_WHIP'
          ]
    
    gnb.fit(
            X_train[used_features].values,
            X_train["Outcome"]
    )
    
    y_pred = gnb.predict(X_test[used_features])
    
    
    # Print resultss
    print("Total Predicted: {}\nPredicted Correctly: {}\nPercentage Correct: {:05.2f}%"
          .format(
              X_test.shape[0],
              (X_test["Outcome"] == y_pred).sum(),
              100*((X_test["Outcome"] == y_pred).sum()/X_test.shape[0])
    ))
    print("\n")

def RunLinearRegression(data):
    
    plt.scatter(data.Rdiff, data.Outcome)
    plt.xlabel("Rdiff")
    plt.ylabel("Outcome")
    plt.show()
    
    
    print("Running Linear Regressions on Dataset\n")
    used_features = [
            "Rdiff",
            "SRS",
            "R_G",
            "R",
            "RBI",
            "OBP",
            "OPSP",
            "RA",
            "ERA",
            "SV",
            "HA",
            "ER",
            "ERAP",
            "WHIP",
            'opponent_Rdiff', 
            'opponent_SRS' ,
            'opponent_R_G' ,
            'opponent_R' ,
            'opponent_RBI', 
            'opponent_OBP' ,
            'opponent_OPSP' ,
            'opponent_RA',
            'opponent_ERA' ,
            'opponent_SV' ,
            'opponent_HA', 
            'opponent_ER', 
            'opponent_ERAP',
            'opponent_WHIP'
    ]
    
    F_train, F_test, C_train, C_test = train_test_split(data[used_features], data["Outcome"], test_size=0.33, random_state=int(time.time()))
    
    
    model = LinearRegression()
    model.fit(
            F_train,
            C_train
            )
    print(model.score(F_test, C_test))
    train_pred = model.predict(F_train)
    test_pred = model.predict(F_test)
    
    print("Results train: {:05.2f}".format((np.mean( (C_train - train_pred) **2) *100) ) ) 
    print("\n")
    print(F_train.shape)
    print(F_test.shape)
    print(C_train.shape)
    print(C_test.shape)
    
    #plt.scatter(model.predict(F_train), model.predict(F_train) - C_train, c='red', s=40, alpha=0.5)
    #plt.scatter(model.predict(F_train), (model.predict(F_test)) - C_test, c='green', s=40)
    
    #plt.scatter(model.predict(F_train), model.predict(F_train) - C_train, c='red', s=30, alpha=0.5)
    #plt.scatter((model.predict(F_train)[:,0]), model.predict(F_test) - C_test, c='green')
    #plt.scatter(C_test, model.predict(F_test))
    #plt.hlines(y=0, xmin=0,xmax=5)
    #plt.title("Training = Blue, Test - Green")
    #plt.ylabel('Residuals')
    
    
    
def RunLogisticRegression(data):
    print("Running Logistic Regression on Dataset\n")

    #Solver = Limited Memory BFGS - optimizes problem of mismatched # of features in Hessian matrix
    logR = LogisticRegression(max_iter=1500, random_state=0, solver='lbfgs',multi_class="multinomial")
    
    #Edit LogisticRegression() to have class weights attached to features
    X_train, X_test = train_test_split(data, test_size=0.33, random_state=int(time.time()))
    used_features = [
            "Rdiff",
            "SRS",
            "R_G",
            "R",
            "RBI",
            "OBP",
            "OPSP",
            "RA",
            "ERA",
            "SV",
            "HA",
            "ER",
            "ERAP",
            "WHIP",
            'opponent_Rdiff', 
            'opponent_SRS' ,
            'opponent_R_G' ,
            'opponent_R' ,
            'opponent_RBI', 
            'opponent_OBP' ,
            'opponent_OPSP' ,
            'opponent_RA',
            'opponent_ERA' ,
            'opponent_SV' ,
            'opponent_HA', 
            'opponent_ER', 
            'opponent_ERAP',
            'opponent_WHIP'
    ]
    
    logR.fit(X_train[used_features].values, X_train["Outcome"])
    prediction = logR.predict(X_test[used_features])
    
    
    print("Total Predicted: {}\nPredicted Correctly: {}\nPercentage Correct: {:05.2f}%"
          .format(prediction.size,
                  (X_test["Outcome"]== prediction).sum(),
                  100*(((X_test["Outcome"] == prediction).sum())/prediction.size)
                  ))
    print("\n")
    
def RandomPredictor(data):
    randomArray = []
    for i in range(data.size):
        randomArray.append(random.randint(0,1))
    
    print(randomArray)
    print("\nNumber correct of random algorithm: {:05.2f}%".format((100*(randomArray == data["Outcome"].values).sum())/randomArray.size) )
    
main()
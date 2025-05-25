############## Modules and Libraries ###########################
import sys
from datetime import datetime
try:
    import pandas as pd
    import pyfiglet
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score
    import matplotlib.pyplot as plt
################################################################

##################### Banner ###################################
    pf=pyfiglet.figlet_format("Restaurant Rating Predictor")
    print(pf,"\n Version 1.0")
################################################################

##################### Loading Data #############################
    data=pd.read_csv('Dataset .csv')
    data=data.dropna()
    print("[*] Dataset is Loaded Successfully!")
    print()

###################### Splitting ###############################
    X=data[['Locality','Cuisines','Average Cost for two','Votes']]
    y=data['Aggregate rating']

    X=pd.get_dummies(X)

    scale=StandardScaler()
    X[['Average Cost for two','Votes']]=scale.fit_transform(X[['Average Cost for two','Votes']])

###################### Train Test Split ########################
    X_train, X_test, y_train,y_test=train_test_split(X,y,test_size=0.2, train_size=0.8,random_state=42)

    model=RandomForestRegressor(n_estimators=100,random_state=42)
    model.fit(X_train,y_train)

    prediction=model.predict(X_test)

###################### Features and Importances #################
    importance=model.feature_importances_
    feature_names=X.columns

    feature_df=pd.DataFrame({'Criteria':feature_names,'Score':importance}).sort_values(by='Score',ascending=False)

###################### Output ####################################
    print("[*] Top 10 Most influential Features on Restaurant Rantings:")
    print(feature_df.head(10))
    print()

###################### Evaluation ################################
    mse=mean_squared_error(y_test,prediction)
    r2=r2_score(y_test,prediction)
    print("[?] Mean Square Error:",round(mse**0.5,4))
    print()
    print("[?] R2 Score:",round(r2,2))
    print()

###################### Plotting Graph #############################
    plt.figure(figsize=(10,6))
    plt.plot(feature_df.head(10)['Score'],feature_df.head(10)['Criteria'],marker='o',linestyle='-',color='red')
    plt.xlabel('Score')
    plt.ylabel('Criteria')
    plt.title("Top 10 Most influential Features on Restaurant Rantings")
    plt.tight_layout()
    plt.show()

except Exception or KeyboardInterrupt:
    print("[-] Something Went Wrong!")
    print("[-] Exited at:",str(datetime.now().strftime("%I:%M %p")),"On",str(datetime.now().strftime("%d %B %Y, %A")))
    sys.exit()











    

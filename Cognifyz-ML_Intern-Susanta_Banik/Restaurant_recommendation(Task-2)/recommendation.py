############## Modules ######################################################
import sys
from datetime import datetime, timedelta
try:
    import pandas as pd
    from sklearn.impute import SimpleImputer
    import os
    import pyfiglet
#############################################################################
    pf = pyfiglet.figlet_format("Restaurant Recommendation")
    print(pf,"\n version 1.0")
    print()
    inp=input("[+]Enter <Start> to Start or <Exit> to Stop: ")
    print()
    if inp=="Start" or inp=="start" or inp=="START":
        pass
    else:
        print("[-]Exited at:",str(datetime.now().strftime("%I:%M %p")),"On",str(datetime.now().strftime("%d %B %Y, %A")))
        sys.exit()
        
    # Load dataset
    df = pd.read_csv('Dataset .csv')  

    # Handle missing values
    imputer = SimpleImputer(strategy='most_frequent')
    df[['Cuisines', 'Locality Verbose', 'Price range', 'Aggregate rating']] = imputer.fit_transform(df[['Cuisines', 'Locality Verbose', 'Price range', 'Aggregate rating']])

    # Clean and format Cuisine
    df['Cuisines'] = df['Cuisines'].apply(lambda x: ','.join([c.strip().lower() for c in x.split(',')]))

    # Recommendation Function
    def dynamic_recommend(cuisine=None, price_range=None, top_rec=5):
        filtered = df
        if cuisine:
            filtered = filtered[filtered['Cuisines'].str.contains(cuisine.lower())]

        if price_range:
            filtered = filtered[filtered['Price range'].astype(str) == str(price_range)]

        top = filtered.sort_values(by='Aggregate rating', ascending=False).head(top_rec)
        return top[['Restaurant Name', 'Cuisines', 'Price range', 'Aggregate rating']]

    # Load or initialize preference log
    log_file = "preferences.csv"
    if os.path.exists(log_file):
        user_log = pd.read_csv(log_file)
    else:
        user_log = pd.DataFrame(columns=["Cuisines", "Price range", "Recommend"])

    # Auto-suggestion from history
    def get_most_common(column):
        if column in user_log.columns and not user_log.empty:
            return user_log[column].value_counts().idxmax()
        else:
            return None
    while True:
        suggested_cuisine = get_most_common("Cuisines")
        suggested_price = get_most_common("Price range")
        suggested_Recommend = get_most_common("Recommend")

        # --- USER INPUT ---
        print("[+] Welcome to the Personalized Restaurant Recommender!\n")

        # Cuisine input
        if suggested_cuisine:
            print(f"Most searched Items: {suggested_cuisine}")
            cuisine = input(f"Enter preferred Items : ").strip()
            if cuisine == "":
                cuisine = suggested_cuisine
        else:
            cuisine = input("Enter preferred Items (e.g., French, Indian): ").strip()

        # Price range input
        if suggested_price:
            print(f"Most searched price range: {suggested_price}")
            price_range = input(f"Enter price range (1 = Low, 2 = Medium, 3 = High, 4 = Highest): ").strip()
            if price_range == "":
                price_range = suggested_price
        else:
            price_range = input("Enter price range (1 = Low, 2 = Medium, 3 = High, 4 = Highest): ").strip()

        # suggested_Recommend input
        if suggested_Recommend:
            print(f"Most requested number of recommendations: {suggested_Recommend}")
            top_rec = input(f"How many recommendations? : ").strip()
            if top_rec == "":
                top_rec = int(suggested_Recommend)
            else:
                top_rec = int(top_rec)
        else:
            top_rec = input("How many recommendations? (Default is 5): ").strip()
            if top_rec.isdigit():
                top_rec = int(top_rec)
            else:
                top_rec = 5
        print()
        # Log user preference
        new_entry = pd.DataFrame([{
        "Cuisines": cuisine,
        "Price range": price_range,
        "Recommend": top_rec
        }])

        user_log = pd.concat([user_log, new_entry], ignore_index=True)
        user_log.to_csv(log_file, index=False)

        # Generate recommendations
        print("[*] Fetching top Recommended",cuisine,"restaurants (Price Range:",price_range,")...")
        print()
        results = dynamic_recommend(cuisine=cuisine, price_range=price_range, top_rec=top_rec)
        if not results.empty:
            print(results.to_string(index=False))
        else:
            print("[-] No matching restaurants found. Try different preferences.")
        print()
        print("[?] Tip: The more you use this, the smarter your suggestions become!")
        print()
        inp=input("[+]Enter <Continue> to Start or <Exit> to Stop: ")
        print()
        if inp=="continue" or inp=="Continue":
            pass
            print()
        else:
            print("[-]Exited at:",str(datetime.now().strftime("%I:%M %p")),"On",str(datetime.now().strftime("%d %B %Y, %A")))
            sys.exit()
except KeyboardInterrupt or Exception:
    print()
    print("[-]Something Went Wrong!")
    print("[-]Exited at:",str(datetime.now().strftime("%I:%M %p")),"On",str(datetime.now().strftime("%d %B %Y, %A")))
    print()
    sys.exit()
#########################################################################################################################################################################

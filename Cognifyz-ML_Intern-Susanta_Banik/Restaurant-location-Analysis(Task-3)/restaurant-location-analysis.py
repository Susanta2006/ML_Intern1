############## Modules and Libraries ###########################
import sys
from datetime import datetime
try:
    import pyfiglet
    import pandas as pd
    import folium
    from folium.plugins import MarkerCluster
    import seaborn as sns
    import matplotlib.pyplot as plt
#################################################################
##################### Banner ###################################
    pf=pyfiglet.figlet_format("Restaurant Location-based Analysis")
    print(pf,"\n Version 1.0")
    print()
################################################################

##################### Loading Data #############################
    df = pd.read_csv("Dataset .csv")
    df=df.dropna()
    print("[*] Dataset is Loaded Successfully!")
    print()
########## Drop rows with missing location or city/locality ##### 
    df = df.dropna(subset=['Latitude', 'Longitude', 'City', 'Locality'])

##################### Map Visualization ######################### 

    print("[+] Generating interactive map...")
    print()
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)

    for i, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Restaurant Name']} ({row['Aggregate rating']}) - {row['Cuisines']}"
        ).add_to(marker_cluster)

    m.save("restaurant_map.html")
    print("[*] Map saved as 'restaurant_map.html'")
    print()
##################### Group by City & Locality ##################

    grouped = df.groupby(['City', 'Locality']).agg({
        'Restaurant Name': 'count',
        'Aggregate rating': 'mean',
        'Price range': 'mean'
    }).rename(columns={
        'Restaurant Name': 'restaurant_count',
        'Aggregate rating': 'avg_rating',
        'Price range': 'avg_price_range'
    }).reset_index()

################## Cuisine Analysis by City #####################

    print("[*] Most Common Cuisine by City:")
    print()
    cuisine_mode = df.groupby('City')['Cuisines'].agg(lambda x: x.mode().iat[0] if not x.mode().empty else 'NO MATCH FOUND!')
    print(cuisine_mode.head(10))
    print()
################# Statistical Summary by City #####################

    city_stats = df.groupby('City').agg({
        'Aggregate rating': ['mean', 'max'],
        'Price range': ['mean', 'max']
    }).round(2)

    print("[?] Statistical Average Rating and Price Range by City:")
    print()
    print(city_stats.head(10))
    print()
################ Interesting Insights ############################

    # Highest rated restaurant(s)
    max_rating = df['Aggregate rating'].max()
    top_rated = df[df['Aggregate rating'] == max_rating]
    print("[*] Highest Rated Restaurant(s):")
    print()
    print(top_rated[['Restaurant Name', 'City', 'Locality', 'Aggregate rating']].head(10))
    print()

    # Most expensive restaurant(s)
    max_price = df['Price range'].max()
    most_expensive = df[df['Price range'] == max_price]
    print("[*] Most Expensive Restaurant(s):")
    print()
    print(most_expensive[['Restaurant Name', 'City', 'Locality', 'Price range', 'Aggregate rating']].head(10))
    print()
    
    # Top 10 locations with highest restaurant concentration Graphical
    top_localities = grouped.sort_values(by='restaurant_count', ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_localities, x='restaurant_count', y='Locality', hue='City')
    plt.title("Top 10 Localities by Number of Restaurants")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Locality")
    plt.tight_layout()
    plt.show()
    
except Exception or KeyboardInterrupt:
    print("[-] Something Went Wrong!")
    print("[-] Exited at:",str(datetime.now().strftime("%I:%M %p")),"On",str(datetime.now().strftime("%d %B %Y, %A")))
    sys.exit()




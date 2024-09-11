import streamlit as st
import seaborn as sns
import time
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


df = pd.read_csv("Data\Data_ready_for_streamlit_deploy")

df['pickup_date'] = pd.to_datetime(df['pickup_date'])
df['pickup_time'] = pd.to_timedelta(df['pickup_time'])

df['dropoff_date'] = pd.to_datetime(df['dropoff_date'])
df['dropoff_time'] = pd.to_timedelta(df['dropoff_time'])


st.markdown("<h1 style='text-align: center; color: white;'>Choose a category</h1>", unsafe_allow_html=True)
value = st.selectbox("",["Univariant Analysis","Bivariant Analysis"])

if value == "Univariant Analysis":
#============================================================ Average Distances of the travels
    
    st.markdown("<h1 style='text-align: center; color: white;'>Average Distances of the travels</h1>", unsafe_allow_html=True)
    fig2,ax1 =  plt.subplots()
    plt.figure(figsize=(10, 6))
    ax1.hist(df.trip_distance, bins=50, edgecolor='black')
    st.pyplot(fig2)
    

    
#============================================================ Payment types   
    st.markdown("<h1 style='text-align: center; color: white;'>Payment types </h1>", unsafe_allow_html=True)
    plt.figure(figsize=(10, 6))
    st.plotly_chart(px.histogram(df['payment_type']))
    
    
    
#============================================================ Tip_Amount based on the Payment of Customer

    st.markdown("<h1 style='text-align: center; color: white;'>Tip_Amount based on the Payment of Customer</h1>", unsafe_allow_html=True)
    plt.figure(figsize=(10, 6))
    st.plotly_chart(px.histogram(df, x='tip_amount',color='payment_type',nbins = 15))

    

#============================================================ Demand over the week


    st.markdown("<h1 style='text-align: center; color: white;'>Demand over the week</h1>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    df['day_of_week'] = df['pickup_date'].dt.day_name()
    plt.figure(figsize=(10, 6))
    sns.countplot(x='day_of_week', data=df, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],ax =ax)
    st.pyplot(fig)

    plt.figure(figsize=(8, 6))
    st.plotly_chart(px.pie( values = df.day_of_week.value_counts(normalize = True) *100,names =df.day_of_week.unique() , hole = 0.3,
       color_discrete_sequence=px.colors.sequential.RdBu))
    
    
#============================================================ 'The Busiest Month'  
    
    st.markdown("<h1 style='text-align: center; color: white;'>The Busiest Month</h1>", unsafe_allow_html=True)
    fig2,ax1 =  plt.subplots()
    plt.figure(figsize=(10, 6))
    ax1.hist(df.pickup_date.dt.month, bins=15, edgecolor='black')
    plt.xlabel('Month')
    plt.ylabel('Frequent')
    plt.title('The Busiest Month')
    plt.xticks(range(1, 13))
    plt.grid(axis='y', alpha=0.5)
    st.pyplot(fig2)  

    
    
    
    
    
    
#============================================================ Demand By Location

    st.markdown("<h1 style='text-align: center; color: white;'>Taxi Demand by Location over the year</h1>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(50, 8))
    sns.countplot(x='pick_up_location', data=df, ax=ax)
    ax.set_xlabel('Pick-Up Locations')
    ax.set_ylabel('Number of Trips')
    plt.xticks(rotation=90)

    st.pyplot(fig)


#============================================================ The Top 10 Frequent pick_up_locations    

    Top_pick_up = df.pick_up_location.value_counts(normalize = True ,ascending = False ).head(10).keys()
    Percentage = df.pick_up_location.value_counts(normalize = True ,ascending = False ).head(10).tolist()
    
    mapping = dict(zip(Percentage, Top_pick_up))
    
    dfx = pd.DataFrame()
    dfx["X"] = Top_pick_up
    dfx["Y"] = Percentage
    
#========================   
    fig = px.bar(dfx, x='X', y='Y', title="The Most Frequent Pick-Up Locations")

    # Update layout and axis titles
    fig.update_xaxes(title_text="Areas", tickangle=90)
    fig.update_yaxes(title_text="Percentage")
    fig.update_layout(
        title=dict(
            text="The Top 10 Frequent Pick-Up Locations",
            font=dict(size=24)
        ),
        xaxis_title=dict(
            text="Percentage of the Trips",
            font=dict(size=18)
        ),
        yaxis_title=dict(
            text="Areas",
            font=dict(size=18)
        )
    )

    st.plotly_chart(fig)
        
#============================================================ Demand By Location      
    fig, axs = plt.subplots(1, 2, figsize=(20, 6))
    
    st.markdown("<h1 style='text-align: center; color: white;'>Fare amount Vs Pick up locations </h1>", unsafe_allow_html=True)
    # First subplot: Bar plot
    df.groupby('pick_up_location').fare_amount.mean().sort_values().head(15).plot(kind='bar', ax=axs[0])
    axs[0].set_xlabel('Pick-Up Location')
    axs[0].set_ylabel('Average Fare Amount')
    axs[0].set_title('Average Fare Amount by Pick-Up Location')

   
    
    # Second subplot: Pie chart
    
    axs[1].pie(df.groupby('pick_up_location').fare_amount.mean().sort_values().head(15),
           labels=df.groupby('pick_up_location').fare_amount.mean().sort_values().head(15).keys(),
           autopct='%1.1f%%',
           startangle=180)

    axs[1].axis('equal')
    plt.tight_layout()
    st.pyplot(fig)
    
    
    
    
#============================================================ The Top 10 Frequent Drop_Off_locations

    st.markdown("<h1 style='text-align: center; color: white;'>The Top 10 Frequent Drop_Off_locations </h1>", unsafe_allow_html=True)
    
    labels_drop_off = df.drop_of_location.value_counts(normalize = True ,ascending = False ).head(10).keys()

    ValuesOfDropOff = df.drop_of_location.value_counts(normalize = True ,ascending = False ).head(10).tolist()

    mapping = dict(zip(ValuesOfDropOff, labels_drop_off))

    dfx_drop = pd.DataFrame()
    dfx_drop["x"] = ValuesOfDropOff
    dfx_drop["y"] = labels_drop_off


#===============

    fig = px.bar(dfx_drop, x='x', y='y', title="The Most Frequent Pick-Up Locations")

    # Update layout and axis titles
    fig.update_xaxes(title_text="Areas", tickangle=90)
    fig.update_yaxes(title_text="Percentage")
    fig.update_layout(
        title=dict(
            text="The Top 10 Frequent Drop_Off_locations",
            font=dict(size=24)
        ),
        xaxis_title=dict(
            text="Percentage of the Trips",
            font=dict(size=18)
        ),
        yaxis_title=dict(
            text="Areas",
            font=dict(size=18)
        )
    )

    st.plotly_chart(fig)  

#===============


    
    plt.figure(figsize=(12, 6))
    
    df['drop_of_location'].value_counts().sort_values(ascending=False).head(15).plot(kind='bar')

    # Set titles and labels
    plt.title('Top 15 Drop-Off Locations')
    plt.xlabel('Drop-Off Location')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability


    st.pyplot(plt)


elif value == "Bivariant Analysis":
    
    
#============================================================ Fare amount versus Trip distance

    # Plotting correlation between trip distance and fare amount
    st.markdown("<h1 style='text-align: center; color: white;'>Fare amount versus Trip distance </h1>", unsafe_allow_html=True)
    fig, ax =  plt.subplots(figsize=(18, 6))
    sns.scatterplot(x='trip_distance', y='fare_amount', data=df, ax =ax)
    plt.xlabel('Trip Distance (miles)')
    plt.ylabel('Fare Amount ($)')
    st.pyplot(fig)

    

#============================================================ Correlation graph
    st.markdown("<h1 style='text-align: center; color: white;'>Correlation graph</h1>", unsafe_allow_html=True)

    df3 = df.select_dtypes('float','int')
    df3.drop(columns = ["mta_tax","tolls_amount"],axis =1, inplace = True)

    num_cols = df3.select_dtypes('float','int')
#========================    
    fig, ax = plt.subplots(figsize=(18, 6))
    sns.heatmap(num_cols.corr(), annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5 , ax= ax)
    st.pyplot(fig)



#============================================================ fare amount over the months   

    df['pickup_date'] = pd.to_datetime(df['pickup_date'])

    df['month'] = df['pickup_date'].dt.to_period('M').dt.to_timestamp()

    st.markdown("<h1 style='text-align: center; color: white;'>Fare Amount Over the Months</h1>", unsafe_allow_html=True)

  
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=df['month'], y=df['fare_amount'], marker='o', linestyle='-', ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Fare Amount')
    ax.set_title('Fare Amount Over Time')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust layout to prevent clipping of labels
    plt.tight_layout()
  
    st.pyplot(fig)
    plt.clf()

#============================================================ Tip amount over Time

#    st.markdown("<h1 style='text-align: center; color: white;'> Tip amount over Time </h1>", unsafe_allow_html=True)
    
#    df['pickup_date'] = pd.to_datetime(df['pickup_date'])
  
# #   df['month'] = df['pickup_date'].dt.to_period('M').dt.to_timestamp()

#    # Create the plot
# #   fig, ax = plt.subplots(figsize=(15, 6))

    # Create a line plot with Seaborn
# #   sns.lineplot(x=df['month'], y=df['tip_amount'], marker='o', linestyle='-', ax=ax)

    # Set titles and labels
#  #  ax.set_title('Monthly Tip Amounts')
#  #  ax.set_xlabel('Month')
#  #  ax.set_ylabel('Tip Amount')

    # Rotate x-axis labels for better readability
#  #  plt.xticks(rotation=45, ha='right')

    # Adjust layout to prevent clipping of labels
#  #  plt.tight_layout()

#  #  st.pyplot(fig)
## #   plt.clf()

#============================================================ Average tip amount per month


    st.markdown("<h1 style='text-align: center; color: white;'> Average Tip amount over Time</h1>", unsafe_allow_html=True)

    df['pickup_date'] = pd.to_datetime(df['pickup_date'])

    # Create 'month' column as Period and then convert to Timestamp for plotting
    df['month'] = df['pickup_date'].dt.to_period('M')

    # Calculate average tip amount per month
    monthly_avg_tips = df.groupby('month')['tip_amount'].mean().reset_index()

    # Convert 'month' back to datetime for plotting
    monthly_avg_tips['month'] = monthly_avg_tips['month'].dt.to_timestamp()


    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.lineplot(x='month', y='tip_amount', data=monthly_avg_tips, marker='o', linestyle='-', ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Tip Amount')
   

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    # Adjust layout to prevent clipping of labels
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Optionally, if you want to clear the plot after displaying:
    plt.clf()



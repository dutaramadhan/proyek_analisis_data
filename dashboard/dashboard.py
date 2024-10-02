import streamlit as st
import pandas as pd
import matplotlib.pylab as plt
import datetime

all_df = pd.read_csv('https://raw.githubusercontent.com/dutaramadhan/proyek_analisis_data/refs/heads/main/dashboard/all_df.csv')
all_df['Datetime'] = pd.to_datetime(all_df['Datetime'])

parameter_dict = {
    'PM10 (Particulate Matter Diameter 10)': 'PM10',
    'PM2.5 (Particulate Matter Diameter 2.5)': 'PM2.5',
    'SO2 (Sulfur Dioxide)': 'SO2',
    'NO2 (Nitrogen Dioxide)': 'NO2',
    'CO (Carbon Monoxide)': 'CO',
    'O3 (Ozone)': 'O3',
    'Temperature': 'TEMP',
    'Pressure': 'PRES',
    'Dew Point': 'DEWP',
    'Rainfall': 'RAIN',
    'Wind Direction': 'wd',
    'Wind Speed': 'WSPM'
}

def plot_informations_daily(all_df, city, day, parameter_familiar):
    parameter = parameter_dict[parameter_familiar]

    start_of_day = pd.to_datetime(day).normalize()
    end_of_day = start_of_day + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    filtered_df = all_df[(all_df['station'] == city) & 
                          (all_df['Datetime'] >= start_of_day) & 
                          (all_df['Datetime'] <= end_of_day)]

    if not filtered_df.empty:
        st.subheader(f'Average {parameter_familiar} Levels in {city} on {day}')
        
        if parameter == 'wd':
            st.bar_chart(filtered_df['wd'].value_counts())
        else:
            avg_value = filtered_df[parameter].mean()
            st.metric(label=parameter_familiar, value=avg_value)
            st.line_chart(filtered_df[['Datetime', parameter]].set_index('Datetime')) 
    else:
        st.write("No data available for the selected filters.")

def plot_informations_overtime(all_df, city, date, parameter_familiar):
    parameter = parameter_dict[parameter_familiar]

    filtered_df = all_df[(all_df['station'] == city) & 
                          (all_df['Datetime'] >= pd.to_datetime(date[0])) & 
                          (all_df['Datetime'] <= pd.to_datetime(date[1]))]

    if not filtered_df.empty:
        st.subheader(f'{parameter_familiar} Levels in {city} Over Time per Day')
        filtered_df['Date'] = filtered_df['Datetime'].dt.date
        daily_avg = filtered_df.groupby('Date')[parameter].mean().reset_index()

        if parameter == 'wd':
            st.bar_chart(filtered_df['wd'].value_counts())
        else:
            st.line_chart(daily_avg.set_index('Date')[parameter])
    else:
        st.write("No data available for the selected filters.")


def plot_highest_pollutant(pollutant):
    df = all_df.groupby(['station']).agg({pollutant: 'mean'}).sort_values(by=pollutant, ascending=False).reset_index()
    
    plt.figure(figsize=(10, 6))
    colors = ['red' if x == df[pollutant].max() else 'pink' for x in df[pollutant]]
    plt.bar(df['station'], df[pollutant], color=colors)
    plt.title(f'Average {pollutant} Levels by Station')
    plt.xlabel('Stations')
    plt.ylabel('Average Concentration (µg/m³)')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def plot_weekday_weekend(pollutant):
    all_df['dayofweek'] = all_df['Datetime'].dt.dayofweek
    all_df['is_weekend'] = all_df['dayofweek'].apply(lambda x: 1 if x>=5 else 0)
    weekday_vs_weekend = all_df.groupby(['station', 'is_weekend'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().reset_index()
    grouped_data = weekday_vs_weekend.pivot(index='station', columns='is_weekend', values=pollutant)

    plt.figure(figsize=(10, 6))
    grouped_data.plot(kind='bar', color=['yellow', 'blue'], alpha=0.7)
    plt.title(f'Average {pollutant} Levels on Weekdays vs Weekends by Station')
    plt.xlabel('Stations')
    plt.ylabel('Average Concentration (µg/m³)')
    plt.xticks(rotation=45)
    plt.legend(['Weekday', 'Weekend'])
    st.pyplot(plt)


st.title('Air Quality Dashboard')
st.write("This dashboard aims to provide Air Quality Information on 12 station")

with st.container():
    st.subheader('About')
    st.write("This dashboard utilizes the Air Quality Dataset, which is accessible via this [link](https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view). This dataset contains air quality data from 12 stations over the time range of March 1, 2013, to February 28, 2017.")
    st.write(all_df.head(50))
    st.write('\n')

with st.container():
    st.subheader('Daily Information')
    st.write("You can access the daily information of this Air Quality Information.")
    day = st.date_input(label='Select Date', min_value=datetime.date(2013, 3, 1),max_value=datetime.date(2017, 2, 28), value=datetime.date(2017, 2, 28), key='daily_date')
    city = st.selectbox(label = "Select City", options = ('Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'), key = 'daily_city')
    parameter_familiar = st.selectbox(label = "Select Parameter", options = list(parameter_dict.keys()),key = 'daily_parameter')
    plot_informations_daily(all_df, city, day, parameter_familiar)
    st.write('\n')

with st.container():
    st.subheader('Information Overtime')
    st.write("You can access the overtime information of this Air Quality Information.")
    date = st.date_input(label='Select Date Range', value=(datetime.date(2013, 3, 1), datetime.date(2017, 2, 28)), min_value=datetime.date(2013, 3, 1),max_value=datetime.date(2017, 2, 28), key='overtime_date')
    city = st.selectbox(label = "Select City", options = ('Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'), key = 'overtime_city')
    parameter_familiar = st.selectbox(label = "Select Parameter", options = list(parameter_dict.keys()),key = 'overtime_parameter'
    )
    plot_informations_overtime(all_df, city, date, parameter_familiar)
    st.write('\n')

with st.container():
    st.subheader('City with the Highest Average Pollutant Level')
    st.write('This section visualize the station that has recorded the highest average levels of pollutants across different types, specifically focusing on PM2.5, PM10, SO2, NO2, CO, O3. This section visualize insights into which location is most affected by air pollution.')
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    
    with tab1:
        plot_highest_pollutant("PM2.5")
    with tab2:
        plot_highest_pollutant("PM10")
    with tab3:
        plot_highest_pollutant("SO2")
    with tab4:
        plot_highest_pollutant("NO2")
    with tab5:
        plot_highest_pollutant("CO")
    with tab6:
        plot_highest_pollutant("O3")
    
    st.write('From the chart obtained highest average concentration for each pollutant is held by different regions. The highest average concentration of PM2.5 is in Dongsi, PM10 in Gucheng, SO2 in Nongzhanguan, NO2 in Wanliu, CO in Wanshouxigong, and O3 in Dingling. However, there is one region that consistently ranks in the top five for the highest pollutant concentrations, which is Nongzhanguan. This indicates that Nongzhanguan may have issues related to air quality that require greater attention from the authorities.\n')

with st.container():
    st.subheader('Average Pollutant Level on Weekday vs Weekend')
    st.write('This section visualize comparison of average pollutant level on each cities between weekday and weekend.')
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    
    with tab1:
        plot_weekday_weekend("PM2.5")
    with tab2:
        plot_weekday_weekend("PM10")
    with tab3:
        plot_weekday_weekend("SO2")
    with tab4:
        plot_weekday_weekend("NO2")
    with tab5:
        plot_weekday_weekend("CO")
    with tab6:
        plot_weekday_weekend("O3")
    
    st.write('From the chart obtained that the average concentration of each pollutant is consistently higher on weekends compared to weekdays in every region. This is understandable as it may be due to increased human activities, such as recreation and transportation, which tend to be more intensive on weekends. These activities can potentially raise pollutant emissions into the air, impacting air quality. However, monitoring and evaluation should continue, especially if there are industries that illegally operate on weekends, which could further increase pollutant levels.\n')
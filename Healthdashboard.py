import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Public Health Dashboard",layout="wide", page_icon=":chart_with_upwards_trend:")
st.sidebar.title('🔍 Filters')
st.title(" 	:bar_chart: Public Health Surveillance Dashboard")

tabs = st.tabs(["🏠 Home", "📊 Data Overview", "📈 Visualizations", "🔍 Insights","📖 Reference"])
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)


with tabs[0]:
    st.header("Introduction")
    st.write("""The ubiquitous and openly accessible information produced by the public on the Internet 
             has sparked an increasing interest in developing digital public health surveillance (DPHS) systems.
             Shakeri Hossein A. et al.[1]
             """)
   
    st.write("### Team members:")
    st.markdown("- Claire Abu  \n- Yuhang Yu  \n- Agyei Osei Duodu")
    

with tabs[1]:
    st.header("About the data")
    st.write("""
               This dataset was compiled by Dr. Zahra Shakeri and her research team in 2021 for the publication “Digital Public Health Surveillance: A Systematic Scoping Review”. It consists of 755 records and contains comprehensive information related to published studies. This includes details on demographics, surveillance aspects, methodology, and evaluation, making it a valuable asset for research in the domain of digital public health surveillance.
            """)
    st.write("### Key Performance Indicators")
    st.markdown("- Country  \n- Platform  \n- Surveillance Evaluation \n- Health Event Under Surveillance \n- Surveillance Objective \n- Analysis Methods \n- Data Source")





with tabs[2]:
    # Streamlit app layout
    #Read file
    fl = st.file_uploader(" :file_folder: Upload a file", type=(["csv","xlsx"]))
    #Handle no file exception:
    if fl is not None:
        df = pd.read_excel(fl, engine="openpyxl")
        st.write(f"Loaded file: {fl.name}")

    else:
        default_path = "Public Health Surveillance.xlsx"
        default_filename = r"Public Health Surveillance.xlsx"
        df = pd.read_excel(default_path)
        st.write(f"No file uploaded. Using default: {default_filename}")

    st.divider()
    mt1,mt2,mt3 = st.columns([0.3,0.35,0.35])

    # Select relevant columns for analysis
    selected_columns = [
        'Title',
        'Year of Publication',
        'Authors\'s country #1',
        'Platform #1',
        'Health Event Under Surveillance',
        'Surveillance Objective',
        'Surveillance Type',
        'Objective-sub',
        'Finding',
        'Analysis Method #1','Analysis Method #2', 'Analysis Method #3',
        'Analysis Method #4','Analysis Method #5', 'Data Source','Surveillance Evaluation'
    ]
    df_selected = df[selected_columns]

    # Convert 'Year of Publication' to string to avoid dtype mismatch in filtering
    df_selected['Year of Publication'] = df_selected['Year of Publication'].astype(str)

    # Create multi-select filters
    years = st.sidebar.multiselect('Select Year(s) of Publication', sorted(df_selected['Year of Publication'].dropna().unique()))
    countries = st.sidebar.multiselect('Select Country(ies)', sorted(df_selected['Authors\'s country #1'].dropna().unique()))
    health_events = st.sidebar.multiselect('Select Health Event(s)', sorted(df_selected['Health Event Under Surveillance'].dropna().unique()))
    platforms = st.sidebar.multiselect('Select Platform(s)', sorted(df_selected['Platform #1'].dropna().unique()))
    analysis_methods = st.sidebar.multiselect('Select Analysis Method(s)', sorted(df_selected['Analysis Method #1'].dropna().unique()))

    # Filter data based on user selections
    filtered_df = df_selected.copy()
    if years:
        filtered_df = filtered_df[filtered_df['Year of Publication'].isin(years)]
    if countries:
        filtered_df = filtered_df[filtered_df['Authors\'s country #1'].isin(countries)]
    if health_events:
        filtered_df = filtered_df[filtered_df['Health Event Under Surveillance'].isin(health_events)]
    if platforms:
        filtered_df = filtered_df[filtered_df['Platform #1'].isin(platforms)]
    if analysis_methods:
        filtered_df = filtered_df[filtered_df['Analysis Method #1'].isin(analysis_methods)]
    

    # Display total studies count
    view1,view2,view3,view4= st.columns([0.25,0.25,0.25,0.25]) # For displaying metric cards
    
    total_rows = len(filtered_df)
    with view1:
        st.metric(label="Total Studies Matching Filters", value=total_rows)
    health_event_counts = filtered_df['Health Event Under Surveillance'].value_counts().sum()
    with view2:
        st.metric(label="Total Surveillance",value=health_event_counts)
    most_used_platform = filtered_df['Platform #1'].value_counts().idxmax()
    most_used_platform_count=filtered_df['Platform #1'].value_counts().max()
    with view3:
        st.metric(label="Most used platform",value=most_used_platform)
    with view4:
        st.metric(label="Coount of most used",value=most_used_platform_count)
    st.divider()
    # Visualization: Count of studies per platform
    col1,col2 = st.columns([0.5,0.5])
    col3,col4 = st.columns([0.5,0.5])
    col5,col6 = st.columns([0.5,0.5]) # Yuhan charts
    col7,col8 = st.columns([0.5,0.5]) # Clair charts

    if not filtered_df.empty:
        platforms_count = filtered_df['Platform #1'].value_counts().reset_index()
        platforms_count.columns = ['Platform', 'Number of Studies']
        # Comparative Analysis: Count of studies per country
        country_counts = filtered_df['Authors\'s country #1'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Number of Studies']

        
        # Display charts
        # Bar Chart: Number of studies per country
        with col1:
            st.subheader("Comparison of Health Surveillance by Country")
            fig_country_bar = px.bar(country_counts, x = "Country", 
                        y = "Number of Studies", 
                        color="Country",
                        template = "seaborn")
            st.plotly_chart(fig_country_bar,use_container_width=True)

        # Create Bar Chart
        with col2:
            st.subheader("Public Health Surveillance Platforms Count")
            fig_pie = px.pie(
                platforms_count,
                names='Platform',
                values='Number of Studies',
                color='Platform')
            st.plotly_chart(fig_pie,use_container_width=True)
        
        # Create Pie Chart
        with col3:
            st.subheader("Distribution of Surveillance Platforms")
            fig_bar = px.bar(
                platforms_count,
                x='Number of Studies',
                y='Platform',
                orientation='h',
                labels={'x': 'Platforms', 'y': 'Number of Studies'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_bar,use_container_width=True)
            view_osei1,dwn_osei1 = st.columns([0.5,0.5])
            with view_osei1:
                dropdown=st.expander("View Data")
                dropdown.write(platforms_count)
            with dwn_osei1:
                st.download_button("Get a copy of the Data", data=platforms_count.to_csv().encode(),file_name="healthsurveillance_bar.csv", mime="text.csv")
    
        with col4:
            treemap_data = filtered_df.groupby(["Authors's country #1","Health Event Under Surveillance"]).size().reset_index(name="Count")
            # Create a treemap
            st.header("Health Surveillance by Country")
            fig_treemap = px.treemap(
                treemap_data, 
                path=["Authors's country #1", "Health Event Under Surveillance"],  # Hierarchical structure (Country → Health Event)
                values="Count", 
                title="",
                color="Count",
                color_continuous_scale="Blues"  # Adjust color scheme as needed
            )
            st.plotly_chart(fig_treemap,use_container_width=True)
            view_osei2,dwn_osei2 = st.columns([0.5,0.5])
            with view_osei2:
                dropdown=st.expander("View Data")
                dropdown.write(treemap_data)
            with dwn_osei2:
                st.download_button("Get a copy of the Data", data=treemap_data.to_csv().encode(),file_name="healthsurveillance_treemap.csv", mime="text.csv")
        with col5:
            st.subheader("Proportion of Data Sources in years")
            source_counts = filtered_df['Data Source'].value_counts()
            top_10_sources = source_counts.head(10)
            others_sum = source_counts[10:].sum()
            final_counts = pd.concat([top_10_sources, pd.Series({'Others': others_sum})])
            
            fig_yuhan1 = px.pie(
            values=final_counts.values,
            names=final_counts.index,
            labels={'names': 'Data Source', 'values': 'Count'}
            )
            fig_yuhan1.update_layout(
                legend_title="Data Sources",
                showlegend=True
            )
            st.plotly_chart(fig_yuhan1,use_container_width=True)
            view_yuhan1,dwn_yuhan1 = st.columns([0.5,0.5])
            with view_yuhan1:
                dropdown=st.expander("View Data")
                dropdown.write(final_counts)
            with dwn_yuhan1:
                st.download_button("Get a copy of the Data", data=final_counts.to_csv().encode(),file_name="healthsurveillance_ypie.csv", mime="text.csv")
        
        with col6:
            st.header(f"📊 Trend of {analysis_methods} Over Time")
            df["Year of Publication"] = df["Year of Publication"].astype(str)
            analysis_method_col = "Analysis Method #1"
            trend_data = filtered_df.groupby(["Year of Publication", analysis_method_col]).size().reset_index(name="Count")

 
            fig_Yuhan2 = px.line(
                trend_data, 
                x="Year of Publication", 
                y="Count", 
                color=analysis_method_col,
                labels={"Count": "Number of Publications", "Year of Publication": "Year"}
            )
            
            fig_Yuhan2.update_layout(
                legend_title="Analysis Method",
                xaxis_title="Year",
                yaxis_title="Number of Publications"
            )
            st.plotly_chart(fig_Yuhan2,use_container_width=True)
            view_yuhan2, dwn_yuhan2 = st.columns([0.5,0.5])
            with view_yuhan2:
                dropdown=st.expander("View Data")
                dropdown.write(trend_data)
            with dwn_yuhan2:
                st.download_button("Get a copy of the Data", data=trend_data.to_csv().encode(),file_name="healthsurveillance_line.csv", mime="text.csv")

        with col7:
           
            health_event_col = 'Health Event Under Surveillance' 
            objective_col = 'Surveillance Objective'
            st.header("")
            #new df
            #df_counts = filtered_df.groupby(['Health Event Under Surveillance', 'Surveillance Objective']).size().reset_index(name='count') # Calculate the proportions 
            #f_counts['proportion'] = df_counts.groupby('Health Event Under Surveillance')['count'].transform(lambda x: x / x.sum()) 
            # Step 1: Calculate the count of each combination
            df_counts = filtered_df.groupby(['Health Event Under Surveillance', 'Surveillance Objective']).size().reset_index(name='count')

            # Step 2: Calculate the total count per Health Event
            df_counts['total'] = df_counts.groupby('Health Event Under Surveillance')['count'].transform('sum')

            # Step 3: Normalize the counts by dividing by the total count for each health event
            df_counts['proportion'] = df_counts['count'] / df_counts['total']

            # Step 4: Calculate the proportion of 'Infodemiology' for each 'Health Event Under Surveillance'
            infodemiology_proportion = df_counts[df_counts['Surveillance Objective'] == 'Infodemiology'] \
                .groupby('Health Event Under Surveillance')['proportion'].sum().reset_index()

            # Step 5: Sort the health events by the proportion of 'Infodemiology'
            infodemiology_proportion = infodemiology_proportion.sort_values('proportion', ascending=False)

            # Step 6: Create a custom order for 'Health Event Under Surveillance' based on the sorted proportions
            custom_order = infodemiology_proportion['Health Event Under Surveillance'].tolist()

            fig_claire1 = px.bar(
                df_counts, 
                x=df_counts['proportion'],
                y=health_event_col,
                color=objective_col,
                labels={health_event_col: "Health Event", objective_col: "Surveillance Objective"},
                category_orders={"Health Event Under Surveillance": custom_order},
                title="Proportion of Objectives per Health Event",
                barmode="stack" # Normalizes the bar heights to show proportions
            )
            fig_claire1.update_layout(
                xaxis_title="Proportion",
                yaxis_title="Health Event",
                legend_title="Surveillance Objective"
            )
            st.plotly_chart(fig_claire1, use_container_width=True)
            view_claire1,dwn_claire1 = st.columns([0.5,0.5]) 
            
            with view_claire1:
                dropdown=st.expander("View Data")
                dropdown.write(health_event_col)
           
                    
                

        with col8:
            
            pie_data = filtered_df.groupby(["Surveillance Evaluation", "Surveillance Objective"]).size().reset_index(name="Count")
            if pie_data.empty:
                st.warning("No data available for the selected filters. Please adjust the filters.")
            else:
            # Create a Sunburst Chart (better than a pie chart for two categorical variables)
                fig_claire2 = px.sunburst(
                    pie_data, 
                    path=["Surveillance Objective","Surveillance Evaluation"],  # Hierarchy
                    values="Count",  
                    title="Distribution of Surveillance Evaluation & Objective",
                    height=500
                )
            
                fig_claire2.update_traces(textinfo="label+percent entry")  # Show labels & percentages
                st.plotly_chart(fig_claire2, use_container_width=True)
                view_claire2,dwn_claire2 = st.columns([0.5,0.5]) 
                with view_claire2:
                    dropdown=st.expander("View Data")
                    dropdown.write(pie_data)
                with dwn_claire2:
                    st.download_button("Get a copy of the Data", data=pie_data.to_csv().encode(),file_name="healthsurveillance_sunburst.csv", mime="text.csv")



                            
    else:
        st.warning("No data available for the selected filters. Please adjust your selections.")

    # Display filtered data as a table
    st.write("### Filtered Data")
    st.dataframe(filtered_df)
    _,_,dwn_df = st.columns([0.3,0.3,0.3]) # For viewing data and download buttons
    with dwn_df:
        st.download_button("Get a copy of the Raw Data", data=filtered_df.to_csv().encode(),file_name="healthsurveillance.csv", mime="text.csv")
        
with tabs[3]:
    st.write("### Key Insights")
    st.write("##### Which Country has the highest health event Surveillance?")
    st.markdown("""
    1. United States of America has the largest health event under surveillance among the countries in the study. \n
    2. Behavioral Risk Factors and Communicable diseases are the most predominant of all health events under study. This is confirmed by the fact that USA has well-funded public health agencies (CDC, NIH, FDA) dedicated to surveillance. The Centers for Disease Control and Prevention (CDC) runs major behavioral risk and infectious disease surveillance programs.
    The USA allocates large budgets for disease monitoring, prevention, and intervention.
    3. The Platform widely used is Twitter. This might be due to its real-time data, large user base, and ability to detect emerging health trends quickly based on user sentiments. \n
    """)
with tabs[4]:
    st.header("References:")
    st.write("""Shakeri Hossein A. et al. Z., Kline, A., Sultana, M.  
             Digital public health surveillance: a systematic scoping review. 
             npj Digit. Med. 4, 41 (2021). https://doi.org/10.1038/s41746-021-00407-6
            """)


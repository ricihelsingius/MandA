import pandas as pd
import plotly.express as px

# Load the CSV file into a DataFrame
data = pd.read_csv('acquisitions_update_2021.csv')

# Filter out rows where Acquisition Year is not a number
data_filtered = data[data['Acquisition Year'].apply(lambda x: x.isnumeric())]
data_filtered['Acquisition Year'] = data_filtered['Acquisition Year'].astype(int)

# Group by Parent Company and Acquisition Year to count the number of acquisitions in each year
grouped_data = data_filtered.groupby(['Parent Company', 'Acquisition Year']).size().reset_index(name='Acquisitions Count')

# Create the interactive Plotly chart
fig = px.line(grouped_data, x='Acquisition Year', y='Acquisitions Count', color='Parent Company',
              title='Timeline of Acquisitions by Parent Companies', 
              labels={'Acquisition Year': 'Year', 'Acquisitions Count': 'Number of Acquisitions'},
              markers=True)

# Show the plot
fig.show()

fig.write_html("m&a.html")

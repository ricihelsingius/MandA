import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the CSV file into a DataFrame
data = pd.read_csv('acquisitions_update_2021.csv')

# Data validation
# Check for missing values
missing_data = data.isnull().sum()
print("Missing data count:\n", missing_data)

# Check for duplicate rows
duplicate_rows = data[data.duplicated()]
if not duplicate_rows.empty:
    print("Duplicate rows detected!\n", duplicate_rows)
    data.drop_duplicates(inplace=True)

# Drop rows where Acquisition Year is not a number
data_filtered = data[data['Acquisition Year'].apply(lambda x: str(x).isnumeric())]
data_filtered.loc[:, 'Acquisition Year'] = data_filtered['Acquisition Year'].astype(int)

# Descriptive statistics
print(data_filtered.describe())

# Group by Parent Company and Acquisition Year to count the number of acquisitions in each year
grouped_data = data_filtered.groupby(['Parent Company', 'Acquisition Year']).size().reset_index(name='Acquisitions Count')

# Create the interactive Plotly chart with toggle buttons for different views
fig = go.Figure()

# Add scatter (line) and bar traces for each parent company
for parent in grouped_data['Parent Company'].unique():
    parent_data = grouped_data[grouped_data['Parent Company'] == parent]

    # Line traces
    fig.add_trace(go.Scatter(x=parent_data['Acquisition Year'], 
                             y=parent_data['Acquisitions Count'], 
                             mode='lines+markers',
                             name=parent,
                             marker=dict(size=8),
                             visible=True))
    
    # Bar traces
    fig.add_trace(go.Bar(x=parent_data['Acquisition Year'], 
                         y=parent_data['Acquisitions Count'], 
                         name=parent,
                         visible=False))

# Update layout for toggling between line and stacked bar views
fig.update_layout(title='Timeline of Acquisitions by Parent Companies',
                  xaxis_title='Year',
                  yaxis_title='Number of Acquisitions',
                  updatemenus=[
                      dict(
                          type="buttons",
                          showactive=True,
                          buttons=[
                              dict(label="Line",
                                   method="update",
                                   args=[{"visible": [True, False]*len(grouped_data['Parent Company'].unique()), "barmode": "relative"}]),
                              dict(label="Bar",
                                   method="update",
                                   args=[{"visible": [False, True]*len(grouped_data['Parent Company'].unique()), "barmode": "stack"}])
                          ]
                      )
                  ])

# Customize legend
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

# Show the plot
fig.show()


# Save as interactive HTML
fig.write_html("interactive_m&a.html")

# Save processed data
grouped_data.to_csv('processed_acquisitions_data.csv', index=False)

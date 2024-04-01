import streamlit as st
import pandas as pd
from logic import get_upcoming_odds, calculate_events, create_arbitrage_df

# Set page title and favicon
st.set_page_config(page_title='Sports Betting Arbitrage', page_icon=':moneybag:')

# Add a title and description with styling
st.markdown("""
    <h1 style='text-align: center;'>Sports Betting Arbitrage</h1>
    <p style='text-align: center;'>Find arbitrage opportunities across different bookmakers.</p>
""", unsafe_allow_html=True)

# Add a sidebar for filters and options
st.sidebar.title('Options')
BET_SIZE = st.sidebar.number_input('Bet Size (USD)', min_value=1, value=100, step=10)

# Add a button to fetch and calculate arbitrage opportunities
if st.button('Find Arbitrage Opportunities'):
    try:
        # Fetch upcoming odds from the API
        odds_response = get_upcoming_odds()
        
        # Calculate arbitrage opportunities
        arbitrage_events = calculate_events(odds_response, BET_SIZE)
        
        if len(arbitrage_events) > 0:
            # Create a DataFrame to store the arbitrage data
            dataframe, MAX_OUTCOMES, ARBITRAGE_EVENTS_COUNT = create_arbitrage_df(arbitrage_events)
            
            # Write the arbitrage data to the DataFrame
            # write_data_to_excel(arbitrage_events, dataframe)
            
            # # Format the Excel file
            # format_excel(MAX_OUTCOMES, ARBITRAGE_EVENTS_COUNT)
            
            # Set column widths
            column_widths = [10, 15, 15] + [20] * (len(dataframe.columns) - 3)
            pd.set_option('display.max_colwidth', None)
            for i, width in enumerate(column_widths):
                pd.set_option(f'display.column_width.{i}', width)
            
            # Apply custom CSS styles to the table
            st.markdown("""
                <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #f2f2f2;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Apply hover effect to table rows
            st.markdown("""
                <style>
                tbody tr:hover {
                    background-color: #f5f5f5;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Alternate row colors
            st.markdown("""
                <style>
                tbody tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Display the arbitrage data in a styled table
            styled_table = dataframe.style.background_gradient(cmap='YlGn', subset=['Expected Earnings'])
            st.write(styled_table)
            
            # Provide a download link for the Excel file
            with open('upcoming_events_bets.xlsx', 'rb') as f:
                excel_data = f.read()
            st.download_button(label='Download Excel File', data=excel_data, file_name='upcoming_events_bets.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        else:
            st.warning('No arbitrage opportunities found.')
    except (IndexError, KeyError):
        st.warning('No games available or invalid data structure.')

# Add a footer
st.markdown("""
    <hr>
    <p style='text-align: center;'>Powered by Streamlit | &copy; 2024 Developed by Mikeo Skinner</p>
""", unsafe_allow_html=True)
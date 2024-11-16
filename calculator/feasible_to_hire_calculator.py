import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from parameters.age_group_assumption import age_group_mapping
from parameters.channel_assumption import hiring_channels, channel_population
def predict_unemployment_rates(historical_data):
    """
    Predict unemployment rates for each age group
    """
    try:
        # Create a copy
        df = historical_data.copy()
        print(df.head())
        
        # Verify required columns exist
        required_columns = ['Period', 'Year', 'Age Group', 'Unemployment_Rate']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        # Extract month from Period (M01, M02, etc.)
        df['Month'] = df['Period'].str.extract('M(\d+)').astype(int)
        
        # Create Date column
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01')
        
        # Print debug info
        print("Columns in dataframe:", df.columns.tolist())
        print("First few rows of Month column:", df['Month'].head())
        
        predictions_by_age = {}
        age_groups = df['Age Group'].unique()
        
        for age_group in age_groups:
            age_data = df[df['Age Group'] == age_group].copy()
            
            # Sort by date
            age_data = age_data.sort_values('Date')
            
            # Prepare regression data
            X = (age_data['Year'] + age_data['Month']/12).values.reshape(-1, 1)
            y = age_data['Unemployment_Rate'].values
            
            # Fit model
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate future dates
            last_date = age_data['Date'].max()
            future_dates = pd.date_range(start=last_date, periods=121, freq='M')[1:]
            future_X = (future_dates.year + future_dates.month/12).values.reshape(-1, 1)
            
            # Predict
            future_predictions = model.predict(future_X)
            future_predictions = np.maximum(future_predictions, 0)
            
            predictions_by_age[age_group] = pd.DataFrame({
                'Date': future_dates,
                'Predicted_Rate': future_predictions
            })
        
        return predictions_by_age
        
    except Exception as e:
        print(f"Error in predict_unemployment_rates: {str(e)}")
        raise

def get_feasible_hires_by_year(channel_population, hiring_channels, predictions_by_age, age_group_mapping):
    """
    Calculate feasible hires considering both unemployed and employed job seekers
    
    Parameters:
    -----------
    channel_population: dict
        Population data by channel
    hiring_channels: dict
        Qualification rates by channel
    predictions_by_age: dict
        Predicted unemployment rates by age group
    age_group_mapping: dict
        Mapping between channel age groups and prediction age groups
    """
    years = range(2024, 2034)
    feasible_hires = pd.DataFrame(index=years, columns=['Feasible_Hires'])
    
    # Job seeking rates by employment status
    employed_job_seeking_rate = 0.15  # 15% of employed people seek jobs annually
    
    for year in years:
        total_feasible = 0
        for channel, data in channel_population.items():
            for age_group, distribution in data['distribution'].items():
                base_pool = data['total_pool'] * distribution
                mapped_age_group = age_group_mapping[age_group]
                
                if mapped_age_group in predictions_by_age:
                    # Get unemployment rate for this age group and year
                    unemployment_rate = predictions_by_age[mapped_age_group].loc[
                        predictions_by_age[mapped_age_group]['Date'].dt.year == year, 
                        'Predicted_Rate'
                    ].iloc[0] / 100
                    
                    # Calculate total job seekers
                    unemployed_seekers = base_pool * unemployment_rate
                    employed_seekers = base_pool * (1 - unemployment_rate) * employed_job_seeking_rate
                    total_seekers = unemployed_seekers + employed_seekers
                    
                    # Apply qualification rate
                    qualified_rate = hiring_channels[channel][age_group]['qualified_rate']
                    feasible_hires_channel = total_seekers * qualified_rate
                    
                    total_feasible += feasible_hires_channel
        
        feasible_hires.loc[year, 'Feasible_Hires'] = total_feasible
    
    return feasible_hires

def get_feasible_hires_by_channel(historical_data):
    """
    Calculate feasible hires broken down by channel
    
    Parameters:
    historical_data: DataFrame with unemployment data
    
    Returns:
    dict with feasible hires by year and channel
    """
    predictions_by_age = predict_unemployment_rates(historical_data)
    years = range(2024, 2034)
    feasible_by_year_channel = {year: {} for year in years}
    
    for year in years:
        for channel, data in channel_population.items():
            total_feasible = 0
            for age_group, distribution in data['distribution'].items():
                base_pool = data['total_pool'] * distribution
                mapped_age_group = age_group_mapping[age_group]
                
                if mapped_age_group in predictions_by_age:
                    pred_rate = predictions_by_age[mapped_age_group].loc[
                        predictions_by_age[mapped_age_group]['Date'].dt.year == year, 
                        'Predicted_Rate'
                    ].iloc[0] / 100
                    
                    qualified_rate = hiring_channels[channel][age_group]['qualified_rate']
                    feasible_hires = base_pool * pred_rate * qualified_rate
                    total_feasible += feasible_hires
            
            feasible_by_year_channel[year][channel] = total_feasible
    
    return feasible_by_year_channel
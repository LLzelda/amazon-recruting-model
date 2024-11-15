import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression

# Channel population data
channel_population = {
    'Industry': {
        'total_pool': 1_000_000,  # Domestic workforce in relevant industry
        'distribution': {
            '16 to 19 years': 0.00,  # Almost none
            '20 to 24 years': 0.10,  # 10% of industry workforce
            '25 to 34 years': 0.35,  # 35% of industry workforce
            '35 to 44 years': 0.30,  # 30% of industry workforce
            '45 to 54 years': 0.15,  # 15% of industry workforce
            '55 years and over': 0.10  # 10% of industry workforce
        }
    },
    'Student': {
        'total_pool': 200_000,  # Annual graduates in relevant fields
        'distribution': {
            '16 to 19 years': 0.05,  # High school/early college
            '20 to 24 years': 0.60,  # Bachelor's graduates
            '25 to 34 years': 0.30,  # Master's/PhD students
            '35 to 44 years': 0.04,  # Career changers
            '45 to 54 years': 0.007,  # Rare cases
            '55 years and over': 0.003  # Very rare cases
        }
    },
    'International': {
        'total_pool': 500_000,  # Potential international candidates
        'distribution': {
            '16 to 19 years': 0.02,  # International students
            '20 to 24 years': 0.25,  # Fresh graduates
            '25 to 34 years': 0.40,  # Early career
            '35 to 44 years': 0.20,  # Mid career
            '45 to 54 years': 0.10,  # Senior level
            '55 years and over': 0.03  # Expert level
        }
    }
}

# Hiring channels qualification rates
hiring_channels = {
    'Industry': {
        '16 to 19 years': {'qualified_rate': 0.0},
        '20 to 24 years': {'qualified_rate': 0.15},
        '25 to 34 years': {'qualified_rate': 0.45},
        '35 to 44 years': {'qualified_rate': 0.60},
        '45 to 54 years': {'qualified_rate': 0.55},
        '55 years and over': {'qualified_rate': 0.40}
    },
    'Student': {
        '16 to 19 years': {'qualified_rate': 0.10},
        '20 to 24 years': {'qualified_rate': 0.35},
        '25 to 34 years': {'qualified_rate': 0.25},
        '35 to 44 years': {'qualified_rate': 0.05},
        '45 to 54 years': {'qualified_rate': 0.02},
        '55 years and over': {'qualified_rate': 0.01}
    },
    'International': {
        '16 to 19 years': {'qualified_rate': 0.05},
        '20 to 24 years': {'qualified_rate': 0.30},
        '25 to 34 years': {'qualified_rate': 0.50},
        '35 to 44 years': {'qualified_rate': 0.45},
        '45 to 54 years': {'qualified_rate': 0.35},
        '55 years and over': {'qualified_rate': 0.20}
    }
}

# Age group mapping
age_group_mapping = {
    '16 to 19 years': '16-19',
    '20 to 24 years': '20-24',
    '25 to 34 years': '25-34',
    '35 to 44 years': '35-44',
    '45 to 54 years': '45-54',
    '55 years and over': '55+'
}

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
    Calculate feasible hires for each year from 2024 to 2033
    
    Parameters:
    channel_population: dict, population data by channel
    hiring_channels: dict, qualification rates by channel and age group
    predictions_by_age: dict, unemployment rate predictions by age group
    age_group_mapping: dict, mapping between age group formats
    
    Returns:
    DataFrame with columns: Year, Feasible_Hires
    """
    years = range(2024, 2034)
    feasible_hires = pd.DataFrame(index=years, columns=['Feasible_Hires'])
    
    for year in years:
        total_feasible = 0
        for channel, data in channel_population.items():
            for age_group, distribution in data['distribution'].items():
                base_pool = data['total_pool'] * distribution
                mapped_age_group = age_group_mapping[age_group]
                
                if mapped_age_group in predictions_by_age:
                    pred_rate = predictions_by_age[mapped_age_group].loc[
                        predictions_by_age[mapped_age_group]['Date'].dt.year == year, 
                        'Predicted_Rate'
                    ].iloc[0] / 100
                    
                    qualified_rate = hiring_channels[channel][age_group]['qualified_rate']
                    feasible_hires.loc[year, 'Feasible_Hires'] = base_pool * pred_rate * qualified_rate
                    total_feasible += feasible_hires.loc[year, 'Feasible_Hires']
        
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
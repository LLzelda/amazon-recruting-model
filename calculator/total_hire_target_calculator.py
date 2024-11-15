import numpy as np
import pandas as pd

# Starting Employee Numbers (2023)
starting_employees = {
    'Amazon_US': 1_100_000,
    'Amazon_International': 264_000,
    'AWS': 136_000
}

# Growth Rates
growth_rates = {
    'Amazon_US': {'lower': 0.02, 'median': 0.035, 'upper': 0.05},
    'Amazon_International': {'lower': 0.05, 'median': 0.075, 'upper': 0.10},
    'AWS': {'lower': 0.10, 'median': 0.15, 'upper': 0.2}
}

# Tech ratio progression over years
tech_ratio_progression = {
    'Amazon_US': {
        2023: 0.28,  # Starting at 28%
        2028: 0.32,  # Increase to 32% by 2028
        2033: 0.35   # Increase to 35% by 2033
    },
    'Amazon_International': {
        2023: 0.25,  # Starting at 25%
        2028: 0.30,  # Increase to 30% by 2028
        2033: 0.33   # Increase to 33% by 2033
    },
    'AWS': {
        2023: 0.95,  # Starting at 95%
        2028: 0.96,  # Slight increase to 96% by 2028
        2033: 0.97   # Slight increase to 97% by 2033
    }
}

def get_tech_ratio(year, sector):
    """Calculate tech ratio for a given year using linear interpolation"""
    progression = tech_ratio_progression[sector]
    if year in progression:
        return progression[year]
    
    # Find the surrounding years
    years = sorted(progression.keys())
    for i in range(len(years)-1):
        if years[i] <= year <= years[i+1]:
            # Linear interpolation
            ratio = (year - years[i]) / (years[i+1] - years[i])
            return progression[years[i]] + ratio * (progression[years[i+1]] - progression[years[i]])
    return progression[years[-1]]  # Return last value if beyond range

def project_employees(starting_number, rates, sector):
    """Project both total and technical employees"""
    years = np.arange(2023, 2034)
    total_projections = {'lower': [], 'median': [], 'upper': []}
    tech_projections = {'tech_lower': [], 'tech_median': [], 'tech_upper': []}
    
    # Initialize first year
    for scenario in ['lower', 'median', 'upper']:
        total_projections[scenario].append(starting_number)
        tech_projections[f'tech_{scenario}'].append(
            starting_number * get_tech_ratio(2023, sector)
        )
    
    # Project future years
    for year in years[1:]:
        for scenario in ['lower', 'median', 'upper']:
            # Calculate total employees
            prev_total = total_projections[scenario][-1]
            new_total = prev_total * (1 + rates[scenario])
            total_projections[scenario].append(new_total)
            
            # Calculate tech employees with progressive ratio
            tech_ratio = get_tech_ratio(year, sector)
            tech_projections[f'tech_{scenario}'].append(new_total * tech_ratio)
    
    return {**total_projections, **tech_projections}

def calculate_projections():
    """Calculate all projections and return DataFrame"""
    years = np.arange(2023, 2034)
    df = pd.DataFrame({'Year': years})
    
    # Project for each sector
    for sector in starting_employees.keys():
        projections = project_employees(
            starting_employees[sector],
            growth_rates[sector],
            sector
        )
        
        # Add projections to dataframe
        for scenario in ['lower', 'median', 'upper']:
            df[f'{sector}_{scenario}'] = projections[scenario]
            df[f'{sector}_tech_{scenario}'] = projections[f'tech_{scenario}']

    # Calculate total tech employees across all sectors
    df['tech_total_lower'] = df[[f'{sector}_tech_lower' for sector in starting_employees.keys()]].sum(axis=1)
    df['tech_total_median'] = df[[f'{sector}_tech_median' for sector in starting_employees.keys()]].sum(axis=1)
    df['tech_total_upper'] = df[[f'{sector}_tech_upper' for sector in starting_employees.keys()]].sum(axis=1)
    
    return df

def get_annual_hiring_needs(df, scenario='median'):
    """Calculate annual technical hiring needs based on growth and replacement"""
    hiring_needs = pd.DataFrame()
    hiring_needs['Year'] = df['Year'][1:]  # Start from 2024
    
    # Calculate new hires needed for growth
    tech_total = df[f'tech_total_{scenario}']
    hiring_needs['New_Hires_Growth'] = tech_total.diff()[1:]
    
    # Calculate replacement hires (assume 10% annual turnover)
    hiring_needs['Replacement_Hires'] = tech_total[1:] * 0.10
    
    # Calculate total hiring needs
    hiring_needs['Total_Hires'] = hiring_needs['New_Hires_Growth'] + hiring_needs['Replacement_Hires']
    
    return hiring_needs
import sys
import pandas as pd
sys.path.append('..')  # Add parent directory to Python path

from parameters.age_group_assumption import (
    workforce_by_age_group,
    attrition_rates_by_age_group
)
from calculator.total_hire_target_calculator import calculate_projections
from parameters.age_group_assumption import compensation_by_age_group, productivity_by_age_group
from parameters.retention_assumption import (
    RETENTION_COST_RATE,
    HIRING_COST_RATE,
    TRAINING_MONTHS,
    ROI_THRESHOLD,
    RETAINABLE_RATE
)

##Nov.21 update##
from parameters.year_assumption import attrition_rates_by_year #dynamic yearly attrition rates (2023-2033)

def calculate_detailed_attrition(scenario='median'):
    # Get employee projections using existing function
    projections_df = calculate_projections()
    
    # Initialize results DataFrame
    results = pd.DataFrame()
    results['Year'] = projections_df['Year']
    results['Total_Tech_Employees'] = projections_df[f'tech_total_{scenario}']
    
    # Calculate attrition for each age group
    for age_group in workforce_by_age_group.keys():
        # Get the percentage of workforce in this age group
        workforce_percent = workforce_by_age_group[age_group]
        # Get the attrition rate for this age group
        attrition_rate = attrition_rates_by_age_group[age_group]
        
        # Calculate employees in this age group
        employees_in_group = results['Total_Tech_Employees'] * workforce_percent
        results[f'Employees_{age_group}'] = employees_in_group.round(0)
        
        # Calculate attrition for this age group
        attrition = employees_in_group * attrition_rate
        results[f'Attrition_{age_group}'] = attrition.round(0)

        # Calculate retention cost using total compensation from salary_assumption
        total_comp = compensation_by_age_group[age_group]
        retention_cost = employees_in_group * total_comp * RETENTION_COST_RATE
        results[f'Retention_Cost_{age_group}'] = retention_cost.round(0)
    
    # Calculate total attrition
    attrition_columns = [col for col in results.columns if col.startswith('Attrition_')]
    results['Total_Attrition'] = results[attrition_columns].sum(axis=1).round(0)
    
    # Calculate overall attrition rate
    results['Overall_Attrition_Rate'] = (
        results['Total_Attrition'] / results['Total_Tech_Employees']
    ).round(4)

    # Calculate total retention cost
    retention_cost_columns = [col for col in results.columns if col.startswith('Retention_Cost_')]
    results['Total_Retention_Cost'] = results[retention_cost_columns].sum(axis=1).round(0)
    
    # Calculate average retention cost per employee
    results['Average_Retention_Cost_Per_Employee'] = (
        results['Total_Retention_Cost'] / results['Total_Tech_Employees']
    ).round(0)
    
    return results



##Nov.21 update##
def calculate_detailed_attrition_with_yearly_rates(scenario='median'):
    projections_df = calculate_projections()
    results = pd.DataFrame()
    results['Year'] = projections_df['Year']
    results['Total_Tech_Employees'] = projections_df[f'tech_total_{scenario}']
    

    for age_group in workforce_by_age_group.keys():
        workforce_percent = workforce_by_age_group[age_group]
        employees_in_group = results['Total_Tech_Employees'] * workforce_percent
        results[f'Employees_{age_group}'] = employees_in_group.round(0)
        results[f'Attrition_{age_group}'] = results.apply(
            lambda row: row[f'Employees_{age_group}'] * attrition_rates_by_year[row['Year']],
            axis=1
        ).round(0)
        
        total_comp = compensation_by_age_group[age_group]
        retention_cost = employees_in_group * total_comp * RETENTION_COST_RATE
        results[f'Retention_Cost_{age_group}'] = retention_cost.round(0)
    

    attrition_columns = [col for col in results.columns if col.startswith('Attrition_')]
    results['Total_Attrition'] = results[attrition_columns].sum(axis=1).round(0)
    
    results['Overall_Attrition_Rate'] = (
        results['Total_Attrition'] / results['Total_Tech_Employees']
    ).round(4)

    retention_cost_columns = [col for col in results.columns if col.startswith('Retention_Cost_')]
    results['Total_Retention_Cost'] = results[retention_cost_columns].sum(axis=1).round(0)
    
    results['Average_Retention_Cost_Per_Employee'] = (
        results['Total_Retention_Cost'] / results['Total_Tech_Employees']
    ).round(0)
    
    return results



def analyze_retention_worth():
    """Analyze the retention investment value for each age group"""
    
    analysis_results = pd.DataFrame()
    analysis_results['Age_Group'] = workforce_by_age_group.keys()
    
    for age_group in workforce_by_age_group.keys():
        productivity_value = productivity_by_age_group[age_group]
        attrition_rate = attrition_rates_by_age_group[age_group]
        total_comp = compensation_by_age_group[age_group]
        
        # Calculate total potential loss
        hiring_cost = total_comp * HIRING_COST_RATE
        productivity_loss_during_training = (productivity_value * (TRAINING_MONTHS/12))
        total_potential_loss = (productivity_value * attrition_rate) + \
                             (hiring_cost * attrition_rate) + \
                             (productivity_loss_during_training * attrition_rate)
        
        retention_cost = total_comp * RETENTION_COST_RATE
        roi = (total_potential_loss - retention_cost) / retention_cost
        
        # Add to results DataFrame
        analysis_results.loc[analysis_results['Age_Group'] == age_group, 'Annual_Productivity'] = productivity_value
        analysis_results.loc[analysis_results['Age_Group'] == age_group, 'Attrition_Rate'] = f"{attrition_rate:.1%}"
        analysis_results.loc[analysis_results['Age_Group'] == age_group, 'Retention_Cost'] = retention_cost
        analysis_results.loc[analysis_results['Age_Group'] == age_group, 'Potential_Loss'] = total_potential_loss
        analysis_results.loc[analysis_results['Age_Group'] == age_group, 'ROI'] = f"{roi:.1%}"
        analysis_results.loc[analysis_results['Age_Group'] == age_group, 'Worth_Retention'] = roi > ROI_THRESHOLD
        
    return analysis_results

def calculate_retainable_employees(scenario='median'):
    """Calculate the number of employees worth retaining by age group"""
    # Get overall employee projections
    projections = calculate_detailed_attrition(scenario)
    
    # Identify which age groups are worth retention efforts
    retention_worth = analyze_retention_worth()
    worth_retention_groups = retention_worth[retention_worth['Worth_Retention'] == True]['Age_Group'].tolist()
    
    # Create results DataFrame
    results = pd.DataFrame()
    results['Year'] = projections['Year']
    
    # Calculate retainable employees for each worth-retaining age group
    for age_group in worth_retention_groups:
        employees_in_group = projections[f'Employees_{age_group}']
        attrition_count = projections[f'Attrition_{age_group}']
        
        # Use RETAINABLE_RATE instead of hard-coded 0.5
        retainable_employees = (attrition_count * RETAINABLE_RATE).round(0)
        results[f'Retainable_{age_group}'] = retainable_employees
    
    # Calculate total retainable employees
    retainable_columns = [col for col in results.columns if col.startswith('Retainable_')]
    results['Total_Retainable'] = results[retainable_columns].sum(axis=1).round(0)
    
    return results

# Amazon Technical Recruiting Model

## Project Overview
This model predicts and analyzes Amazon's technical talent needs, feasible hiring targets, and talent gaps for 2024-2033. The model incorporates:

- Growth projections across business sectors (Amazon US, International, AWS)
- Evolution of technical talent ratios
- Age-based productivity and attrition analysis
- Retention ROI optimization
- Multi-channel hiring feasibility assessment

## Key Findings

### Technical Workforce Projections
- 2023 Baseline: 503,200 technical employees
- 2033 Projections (Base Case):
  - Amazon US: 543,081
  - Amazon International: 179,557
  - AWS: 533,690
  - Total: 1,256,328

### Annual Hiring Needs (including attrition)
- 2024: 155,307 
- 2028: 212,693
- 2033: 310,109

### Talent Gap Analysis
- Talent gaps emerge from 2025
- Gap widens to 177,368 by 2033
- 10-year cumulative gap: 756,300
- Total economic impact: $3.1B (Net Cost)

## Calculation Formulas

#### 1. Technical Workforce Projection
$$
Tech \ Employees_{year} = Tech \ Employees_{year-1} * (1 + Growth \ Rate) 
$$

#### 2. Net Hiring Target
$$
Net \ Target \ Hires = Base \ Target \ Hires + Attrition - Retainable
$$

#### 3. Hiring Feasibility
$$
Feasible \ Hires = Σ(Candidate \ Pool_{channel} * Qualification \ Rate_{channel})
$$

#### 4. Detailed Attrition
$$
Attrition_{age \ group,year} = Employees_{age \ group,year} × Attrition\ Rate_{age \ group,year}
$$

#### 5. Total Potential Loss
$$
Loss_{age \ group,year} = Attrition_{age \ group,year} × (P_{age \ group,year} + H_{age \ group,year} + P_{age \ group,year} × \frac{T_m}{12})
$$

Where:
- $P_{age}$ = Productivity value for age group
- $A_{age}$ = Attrition rate for age group
- $H_{age}$ = Hiring cost (Compensation × Hiring cost rate)
- $T_m$ = Training months

#### 6. Retention ROI by Age Group
$$
ROI_{age} = \frac{Loss_{age} - (C_{age} × R_r)}{C_{age} × R_r}
$$

Where:
- $C_{age}$ = Total compensation for age group
- $R_r$ = Retention cost rate

#### 8. Retainable Employees
$$
Retainable_{age} = Attrition_{age} × Retainable\ Rate
$$

## Technical Requirements

- Python 3.13
- For other Python versions, reinstall dependencies from requirements.txt:
  - matplotlib
  - pandas
  - scikit-learn

## Project Structure
- **calculators/**: Contains Python scripts for calculations like total hiring targets and retention analysis.
- **parameters/**: Assumptions such as sector growth and age group assumptions.
- **analysis/**: Jupyter notebooks with detailed analysis and visualizations.
- **data/**: Raw data used in the analysis.
- **result/**: Output and processed results.

## Key Model Assumptions

### Business Growth Rates
- Amazon US: 2%-5%
- Amazon International: 5%-10%
- AWS: 10%-20%

### Technical Talent Ratios
- Amazon US: 28%(2023) → 35%(2033)
- Amazon International: 25%(2023) → 33%(2033)
- AWS: 95%(2023) → 97%(2033)

### Age Group Productivity
- 16-19 years: $150,000 (Entry level)
- 20-24 years: $280,000 (Junior level)
- 25-34 years: $420,000 (Mid-level)
- 35-44 years: $580,000 (Senior level)
- 45-54 years: $750,000 (Principal level)
- 55+ years: $850,000 (Distinguished level)

### Retention Analysis
- Analysis shows highest ROI for retention investments in 16-19 age group and lowest in 55+ age group
- Expected to recover 50% of potential attrition
- Average retention cost per employee: $58,470

## Model Components

### Hiring Target Calculator
- Projects workforce needs based on growth and replacement
- Accounts for sector-specific growth rates
- Incorporates technical talent ratio progression

### Feasibility Calculator
- Analyzes hiring channel capacity
- Considers age group unemployment rates
- Evaluates qualification rates by channel

### Retention Calculator
- Calculates detailed attrition by age group
- Analyzes retention costs and ROI
- Projects retention program effectiveness

## Future Development

### Optimization & Improvement
1. Add hiring channel mix adjustment strategy
2. Add regional talent supply analysis
3. Add additional channel to increase hiring feasibility (e.g. bootcamp or apprenticeship.)
4. Add dynamic retention strategy but not constant conversion rate
5. Consider age group distribution change over time
6. Consider salary growth over time
7. Build for robust assumptions for growth and attrition


## Data Sources

- Amazon Annual Reports
- Bureau of Labor Statistics (BLS) unemployment data
- Weekly hiring distribution data provided by Allen

## License

This project is proprietary and confidential.

## Contact

For questions or suggestions, please contact the project maintainers.


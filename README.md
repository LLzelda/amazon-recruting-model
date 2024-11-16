# Amazon Technical Recruiting Model

## Project Overview
This model predicts and analyzes Amazon's technical talent needs, feasible hiring targets, and talent gaps for 2024-2033. The model incorporates:

- Growth projections across business sectors (Amazon US, International, AWS)
- Evolution of technical talent ratios
- Productivity contributions by age groups
- Attrition and retention analysis
- Feasibility assessment of hiring channels

## Key Findings

### Technical Workforce Projections
- 2023 Baseline: 503,200 technical employees
- 2033 Projections (Base Case):
  - Amazon US: 543,081
  - Amazon International: 179,557
  - AWS: 533,690
  - Total: 1,256,328

### Annual Hiring Needs (Base Case)
- 2024: 102,426
- 2028: 149,859
- 2033: 239,126

### Talent Gap Analysis
- Talent gaps expected to emerge from 2029
- Gap widens to 224,480 by 2033
- 10-year cumulative gap: 931,775

## Technical Requirements

- Python 3.13
- For other Python versions, reinstall dependencies from requirements.txt:
  - matplotlib
  - pandas
  - scikit-learn

## Project Structure
amazon-recruiting-model/
├── calculator/
│   ├── total_hire_target_calculator.py     # Total hiring target calculations
│   ├── feasible_to_hire_calculator.py      # Feasibility calculations
│   └── retention_calculator.py             # Retention analysis
├── parameters/
│   ├── sector_assumption.py                # Sector growth assumptions
│   └── age_group_assumption.py             # Age group assumptions
├── notebook/
│   ├── total_hire_target.ipynb            # Hiring target analysis
│   ├── feasible_to_hire.ipynb             # Hiring feasibility analysis
│   └── annual_tech_hire_gap.ipynb         # Talent gap analysis
├── result/
│   ├── annual_tech_hire_gap.ipynb         # Gap analysis results
│   └── retention_analysis.ipynb           # Retention analysis results
├── data/
│   └── bls_unemployment_by_age_group.csv   # Unemployment rate data
└── requirements.txt

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
- Analysis shows highest ROI for retention investments in 25-44 age group
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

1. Optimize hiring channel mix strategy
2. Enhance regional talent supply analysis
3. Develop retention ROI optimization model
4. Add compensation competitiveness module

## Data Sources

- Amazon Annual Reports
- Bureau of Labor Statistics (BLS) unemployment data
- Industry talent mobility studies
- Internal workforce analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## License

This project is proprietary and confidential.

## Contact

For questions or suggestions, please contact the project maintainers.


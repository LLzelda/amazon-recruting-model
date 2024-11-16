# Age group mapping
age_group_mapping = {
    '16 to 19 years': '16-19',
    '20 to 24 years': '20-24',
    '25 to 34 years': '25-34',
    '35 to 44 years': '35-44',
    '45 to 54 years': '45-54',
    '55 years and over': '55+'
}

# Annual attrition rates for Software Engineers by age group
attrition_rates_by_age_group = {
    '16 to 19 years': 0.35,  # 35% - High mobility, internship conversions or seeking first job
    '20 to 24 years': 0.28,  # 28% - Frequent job changes for growth and compensation
    '25 to 34 years': 0.20,  # 20% - Career growth phase, still seeking opportunities
    '35 to 44 years': 0.12,  # 12% - More stable, but still mobile for right opportunities
    '45 to 54 years': 0.08,  # 8%  - Career stability phase, less voluntary movement
    '55 years and over': 0.05  # 5% - Very stable, mainly retirement or special opportunities
}

# Workforce distribution by age group (percentages)
workforce_by_age_group = {
    '16 to 19 years': 0.02,  # 2%
    '20 to 24 years': 0.15,  # 15%
    '25 to 34 years': 0.45,  # 45%
    '35 to 44 years': 0.25,  # 25%
    '45 to 54 years': 0.10,  # 10%
    '55 years and over': 0.03  # 3%
}

# Annual productivity value per employee by age group (USD)
# These values represent estimated revenue generation/value creation per employee
productivity_by_age_group = {
    '16 to 19 years': 150_000,    # Entry level contribution
                                  # - Basic coding tasks
                                  # - Learning phase
                                  # - Requires supervision
    
    '20 to 24 years': 280_000,    # Junior level contribution
                                  # - Independent feature development
                                  # - Bug fixes
                                  # - Small project ownership
    
    '25 to 34 years': 420_000,    # Mid-level contribution
                                  # - Full project ownership
                                  # - Technical leadership
                                  # - Mentoring juniors
    
    '35 to 44 years': 580_000,    # Senior level contribution
                                  # - Complex system design
                                  # - Strategic technical decisions
                                  # - Team multiplier effect
    
    '45 to 54 years': 750_000,    # Principal level contribution
                                  # - Architectural decisions
                                  # - Organization-wide impact
                                  # - Innovation leadership
    
    '55 years and over': 850_000  # Distinguished level contribution
                                  # - Strategic technical vision
                                  # - Industry influence
                                  # - Transformational projects
}

compensation_by_age_group = {
    '16 to 19 years': 95_000,
    '20 to 24 years': 190_000,
    '25 to 34 years': 260_000,
    '35 to 44 years': 340_000,
    '45 to 54 years': 445_000,
    '55 years and over': 515_000
}
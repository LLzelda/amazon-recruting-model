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


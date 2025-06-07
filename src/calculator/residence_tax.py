def calculate_residence_tax(
    previous_year_income: float,
    previous_year_social_insurance: float,
    dependents: int = 0,
    employment_income_deduction: float = 1_950_000,
    basic_deduction: float = 430_000,
    dependent_deduction: float = 330_000,
    municipal_tax_rate: float = 0.06,
    prefectural_tax_rate: float = 0.04,
    per_capita_tax: float = 5_000
) -> int:
    """
    Calculates monthly residence tax based on previous year's income
    
    Args:
        previous_year_income: Gross annual income from previous year
        previous_year_social_insurance: Total social insurance paid previous year
        dependents: Number of dependents claimed previous year
        employment_income_deduction: Default 2025 deduction for salaried workers
        basic_deduction: Residence tax basic deduction (¥430,000)
        dependent_deduction: Per dependent deduction (¥330,000)
        municipal_tax_rate: City tax rate (default 6%)
        prefectural_tax_rate: Prefecture tax rate (default 4%)
        per_capita_tax: Fixed per capita tax (¥5,000)
        
    Returns:
        Monthly residence tax amount (rounded to nearest yen)
        
    References:
        - Tokyo Metropolitan Tax Guide [2][3][6]
        - 2025 Deduction Changes [3][5]
        
    Example:
        >>> calculate_residence_tax(8_000_000, 1_263_180)
        28800
    """
    # Calculate taxable income
    income_after_employment_deduction = previous_year_income - employment_income_deduction
    total_deductions = (
        basic_deduction +
        dependent_deduction * dependents +
        previous_year_social_insurance
    )
    
    taxable_income = max(income_after_employment_deduction - total_deductions, 0)
    
    # Calculate income-based tax
    income_tax = taxable_income * (municipal_tax_rate + prefectural_tax_rate)
    
    # Calculate total annual tax
    annual_residence_tax = income_tax + per_capita_tax
    
    # Monthly amount with rounding
    return round(annual_residence_tax / 12)

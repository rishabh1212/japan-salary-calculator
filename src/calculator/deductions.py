def calculate_health_insurance(
    monthly_salary: float, 
    rate: float = 0.0967,
    employee_share: float = 0.5,
    lower_cap: float = 58_000,
    upper_cap: float = 1_390_000
) -> float:
    """
    Calculates monthly health insurance premium for employees in Ibaraki Prefecture
    
    Args:
        monthly_salary: Gross monthly salary before deductions
        rate: Total insurance rate (employer + employee) [default: 2025 Ibaraki rate]
        employee_share: Employee's portion of premium [default: 50%]
        cap: Maximum insured monthly salary [default: 2025 Ibaraki cap]
        
    Returns:
        Employee's monthly health insurance premium
        
    Raises:
        ValueError: If input salary is negative
        
    Reference:
        - Ibaraki Health Insurance Association: https://www.accompany-sr.jp/info/20250228183709.html
        - MHLW Standard Rates: https://www.mhlw.go.jp/content/12601000/001183530.pdf
    
    Example:
        >>> calculate_health_insurance(847_938)
        40998.0
    """
    if monthly_salary < 0:
        raise ValueError("Salary cannot be negative")

    # Calculate total premium (employer + employee)
    insured_salary = min(monthly_salary, upper_cap) if monthly_salary >= lower_cap else 0
    total_premium = insured_salary * rate

    # Return employee's share
    return round(total_premium * employee_share, 0)


def calculate_pension_insurance(
    monthly_salary: float,
    rate: float = 0.183,
    employee_share: float = 0.5,
    cap: float = 650_000
) -> float:
    """
    Calculates monthly pension insurance premium for employees in Japan
    
    Args:
        monthly_salary: Gross monthly salary before deductions
        rate: Total insurance rate (employer + employee) [default: 2025 rate]
        employee_share: Employee's portion of premium [default: 50%]
        cap: Maximum insured monthly salary [default: 2025 cap]
        
    Returns:
        Employee's monthly pension premium rounded to nearest yen
        
    Raises:
        ValueError: If input salary is negative
        
    References:
        - Pension Insurance Rates: https://www.mhlw.go.jp/content/12601000/001183530.pdf
        - Cap Regulations: https://www.nenkin.go.jp/oshirase/taisetu/2020/202009/20200901.html
        
    Examples:
        >>> calculate_pension_insurance(847_938)
        59475.0
        >>> calculate_pension_insurance(500_000)
        45750.0
    """
    if monthly_salary < 0:
        raise ValueError("Salary cannot be negative")
    
    # Apply monthly salary cap
    insured_salary = min(monthly_salary, cap)
    
    # Calculate total premium and employee's share
    total_premium = insured_salary * rate
    employee_contribution = total_premium * employee_share
    
    return round(employee_contribution, 0)

def calculate_employment_insurance(
    monthly_salary: float,
    rate: float = 0.0055,
    round_half_down: bool = True
) -> int:
    """
    Calculates monthly employment insurance premium for employees in Japan
    
    Args:
        monthly_salary: Gross monthly salary before deductions
        rate: Insurance rate [default: 2025 general business rate 0.55%]
        round_half_down: Use traditional financial rounding (50 sen truncation)
        
    Returns:
        Rounded premium amount (employee's share)
        
    Raises:
        ValueError: If salary is negative
        
    References:
        - MHLW 2025 Rates: https://www.mhlw.go.jp/content/001401966.pdf
        - Rounding Rules: https://www.yayoi-kk.co.jp/lawinfo/detail/20250314/
        
    Examples:
        >>> calculate_employment_insurance(847_938)
        4664
        >>> calculate_employment_insurance(500_000)
        2750
    """
    if monthly_salary < 0:
        raise ValueError("Salary cannot be negative")
    
    raw_premium = monthly_salary * rate
    
    if round_half_down:
        # Traditional Japanese financial rounding (50銭以下切り捨て)
        integer_part = int(raw_premium)
        decimal_part = raw_premium - integer_part
        return integer_part + (1 if decimal_part > 0.5 else 0)
    
    return round(raw_premium)


def calculate_japan_income_tax(
    monthly_gross: float,
    dependents: int = 0,
    health_insurance: float = 41_126,
    pension: float = 59_475,
    employment_insurance: float = 4_664,
    employment_income_deduction: float = 1_950_000,
    basic_deduction: float = 480_000,
    dependent_deduction: float = 380_000,
) -> int:
    """
    Calculate monthly Japanese income tax (所得税) including the Reconstruction Special Tax.
    
    Args:
        monthly_gross: Total monthly gross income (sum of all taxable salary components).
        dependents: Number of dependents (for deduction). Default is 1, as on your payslip.
        health_insurance: Monthly health insurance deduction (default from payslip).
        pension: Monthly pension insurance deduction (default from payslip).
        employment_insurance: Monthly employment insurance deduction (default from payslip).
        employment_income_deduction: Annual employment income deduction (default: 1,950,000 yen for annual income > 8.5M).
        basic_deduction: Annual basic deduction (default: 480,000 yen for high income).
        dependent_deduction: Annual deduction per dependent (default: 380,000 yen).
        
    Returns:
        Monthly income tax (rounded to nearest yen).
        
    References:
        - Tax brackets: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
        - Reconstruction Special Tax: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
        - Deduction details: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
        - Payslip example: See attached PDF [1]
    """
    # Step 1: Calculate annual gross income
    annual_gross = monthly_gross * 12

    # Step 2: Calculate total annual deductions
    total_social_insurance = (health_insurance + pension + employment_insurance) * 12
    total_deductions = (
        employment_income_deduction +
        basic_deduction +
        dependent_deduction * dependents +
        total_social_insurance
    )

    # Step 3: Calculate taxable income (truncate to nearest 1,000 yen)
    taxable_income = annual_gross - total_deductions
    taxable_income = int(taxable_income // 1000 * 1000)

    # Step 4: Apply 2025 progressive tax brackets
    brackets = [
        (1_949_000, 0.05, 0),
        (3_299_000, 0.10, 97_500),
        (6_949_000, 0.20, 427_500),
        (8_999_000, 0.23, 636_000),
        (17_999_000, 0.33, 1_536_000),
        (39_999_000, 0.40, 2_796_000),
        (float('inf'), 0.45, 4_796_000),
    ]
    for upper, rate, deduction in brackets:
        if taxable_income <= upper:
            base_tax = taxable_income * rate - deduction
            break

    # Step 5: Add Reconstruction Special Income Tax (2.1%)
    total_tax = base_tax * 1.021

    # Step 6: Monthly withholding (rounded)
    monthly_tax = int(round(total_tax / 12))

    return monthly_tax


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



def calculate_net_salary(monthly_gross: float, 
                        previous_year_income: float = None) -> dict:
    """
    Calculates monthly net salary with detailed breakdown
    """
    if not previous_year_income:
        previous_year_income = monthly_gross * 12  # Default to current income
    
    deductions = {
        'health_insurance': calculate_health_insurance(monthly_gross),
        'pension': calculate_pension_insurance(monthly_gross),
        'employment_insurance': calculate_employment_insurance(monthly_gross),
        'income_tax': calculate_japan_income_tax(monthly_gross),
        'resident_tax': calculate_residence_tax(previous_year_income, calculate_pension_insurance(monthly_gross))
    }
    
    total_deductions = sum(deductions.values())
    net_salary = monthly_gross - total_deductions
    
    return {
        'gross': monthly_gross,
        'deductions': deductions,
        'net_salary': net_salary,
        'retention_rate': net_salary / monthly_gross
    }

# Example usage for ¥1,000,000/month
if __name__ == "__main__":
    monthly_gross_salary = 847_938
    result = calculate_net_salary(monthly_gross_salary, previous_year_income=None)
    print(f"Net Salary for ¥{monthly_gross_salary:,}: ¥{result['net_salary']:,}")
    print(f"Detailed Deductions: {result['deductions']}")

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

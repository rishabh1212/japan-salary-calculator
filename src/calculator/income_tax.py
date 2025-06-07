
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

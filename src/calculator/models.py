# src/calculator/models.py
from pydantic import BaseModel, Field, validator
from typing import Optional

class SocialInsuranceInput(BaseModel):
    monthly_salary: float = Field(..., gt=0, description="Gross monthly salary in JPY")
    prefecture: str = Field("ibaraki", description="Resident prefecture for insurance rates")
    dependents: int = Field(0, ge=0, description="Number of dependents")

class TaxCalculationInput(SocialInsuranceInput):
    previous_year_income: Optional[float] = Field(None, description="Previous year's income for residence tax")
    municipal_tax_rate: float = Field(0.06, description="Municipal tax rate")
    prefectural_tax_rate: float = Field(0.04, description="Prefectural tax rate")

class DeductionResult(BaseModel):
    health_insurance: float
    pension_insurance: float
    employment_insurance: float
    income_tax: float
    resident_tax: float

    @validator('*')
    def validate_non_negative(cls, value):
        if value < 0:
            raise ValueError("Deductions cannot be negative")
        return value

class NetSalaryResult(DeductionResult):
    gross_salary: float
    net_salary: float
    retention_rate: float

    class Config:
        json_schema_extra = {
            "example": {
                "gross_salary": 847938,
                "net_salary": 646438,
                "retention_rate": 0.763
            }
        }

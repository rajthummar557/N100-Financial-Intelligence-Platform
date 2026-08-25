import pytest
from src.etl.normaliser import normalize_year,normalize_ticker

@pytest.mark.parametrize(
    "input_value,expected",
    [
         ("Mar-23", "2023-03"),
        ("Mar 23", "2023-03"),
        ("March-2023", "2023-03"),
        ("2023", "2023-03"),
        ("FY23", "2023-03"),
        ("Dec-22", "2022-12"),
        ("Jun-23", "2023-06"),
        ("2023-03", "2023-03"),
        ("March-20", "2020-03"),
        ("Jan-24", "2024-01"),
        ("Feb-24", "2024-02"),
        ("Apr-24", "2024-04"),
        ("May-24", "2024-05"),
        ("Jul-24", "2024-07"),
        ("Aug-24", "2024-08"),
        ("Sep-24", "2024-09"),
        ("Oct-24", "2024-10"),
        ("Nov-24", "2024-11"),
        ("  Mar-23  ", "2023-03"),
        ("garbage", "PARSE_ERROR")
    ],
)
def test_normalize_year(input_value,expected):
    assert normalize_year(input_value)==expected

@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("tcs", "TCS"),
        ("TCS", "TCS"),
        (" tcs ", "TCS"),
        ("Tcs", "TCS"),
        ("reliance", "RELIANCE"),
        (" reliance ", "RELIANCE"),
        ("bajaj-auto", "BAJAJ-AUTO"),
        ("BAJAJ-AUTO", "BAJAJ-AUTO"),
        ("M&M", "M&M"),
        ("m&m", "M&M"),
        ("adaniensol", "ADANIENSOL"),
        (" ADANIENT ", "ADANIENT"),
        ("hdfc-bank", "HDFC-BANK"),
        ("  infosys  ", "INFOSYS"),
        ("itc", "ITC"),
    ],
)
def test_normalize_ticker(input_value, expected):
    assert normalize_ticker(input_value) == expected
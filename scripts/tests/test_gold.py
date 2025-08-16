import pytest
from scripts.gold_enricher import mascarar_cpf

def test_mascarar_cpf_completo():
    cpf = "123.456.789-00"
    resultado = mascarar_cpf(cpf)
    assert resultado == "123.***.***-00"

def test_mascarar_cpf_incompleto():
    cpf = "123456789"
    resultado = mascarar_cpf(cpf)
    assert resultado == "123.***.***-**"

def test_mascarar_cpf_none():
    resultado = mascarar_cpf(None)
    assert resultado == "None.***.***-**"

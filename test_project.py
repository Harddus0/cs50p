from project import filename_add_extension, filter, get_quantities_index, get_composition_index
from unittest.mock import patch
import pandas as pd


def test_filename_add_extension():
    assert filename_add_extension("   sinapi   ") == "sinapi.xlsx"
    assert filename_add_extension("sinapi") == "sinapi.xlsx"
    assert filename_add_extension("sinapi.xlsx") == "sinapi.xlsx"


def test_filter():
    d = {'COLUMN 1': [0, 1, 2, 3], 'DESCRICAO DA COMPOSICAO': ["one", "two", "two three",  "three four"]}
    df = pd.DataFrame.from_dict(d)
    assert filter(keywords=["one"], df=df)['DESCRICAO DA COMPOSICAO'].to_list() == ["one"]
    assert filter(keywords=["two"], df=df)['DESCRICAO DA COMPOSICAO'].to_list() == ["two", "two three"]
    assert filter(keywords=["three four"], df=df)['DESCRICAO DA COMPOSICAO'].to_list() == ["three four"]
    assert filter(keywords=["five"], df=df)['DESCRICAO DA COMPOSICAO'].to_list() == []


def test_get_quantities_index_valid():
    budget_cols = ['Col1', 'Col2', 'Col3']
    
    with patch('builtins.input', return_value='1'):
        result = get_quantities_index(budget_cols)
        assert result == 1
    with patch('builtins.input', side_effect=['5', '1']):
        result = get_quantities_index(budget_cols)
        assert result == 1


def test_get_composition_index_valid():
    budget_cols = ['Col1', 'Col2', 'Col3']
    
    with patch('builtins.input', return_value='2'):
        result = get_composition_index(budget_cols)
        assert result == 2
    with patch('builtins.input', side_effect=['4', '2']):
        result = get_composition_index(budget_cols)
        assert result == 2

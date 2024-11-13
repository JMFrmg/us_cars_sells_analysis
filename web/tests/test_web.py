from streamlit.testing.v1 import AppTest
import datetime


def test_title():
    at = AppTest.from_file("app.py").run()
    assert "Ventes de voitures aux Etats-Unis" in at.markdown[0].value


def test_initial_columns():
    at = AppTest.from_file("app.py").run()
    columns_nb = 15
    assert at.dataframe[0].value.shape[1] == columns_nb

def test_initial_rows():
    at = AppTest.from_file("app.py").run()
    rows_nb = 548399
    assert at.dataframe[0].value.shape[0] == rows_nb

def test_ascending_sort():
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value("Prix de vente").run()
    assert at.dataframe[0].value["prix_de_vente"].is_monotonic_increasing

def test_descending_sort():
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value("Prix de vente").run()
    at.selectbox[1].set_value(False).run()
    assert at.dataframe[0].value["prix_de_vente"].iloc[::-1].is_monotonic_increasing


def test_date_filter():
    at = AppTest.from_file("app.py").run()
    filter_begin = datetime.date(2015, 3, 1)
    filter_end = datetime.date(2015, 3, 31)
    at.date_input[0].set_value((filter_begin, filter_end)).run()
    date_array = at.dataframe[0].value["date_de_vente"]
    min_date = date_array.min()
    max_date = date_array.max()
    assert (min_date.date() >= filter_begin) and (max_date.date() <= filter_end)

def test_marque_filter():
    at = AppTest.from_file("app.py").run()
    filter_text = "bmw"
    at.text_input[1].set_value(filter_text).run()
    maker_array = at.dataframe[0].value["marque_du_véhicule"]
    assert maker_array.astype(str).str.contains(filter_text).all()

def test_multi_filter():
    at = AppTest.from_file("app.py").run()
    filter_maker = "bmw"
    filter_modele = "M5"
    at.text_input[1].set_value(filter_maker).run()
    at.text_input[2].set_value(filter_modele).run()
    maker_array = at.dataframe[0].value["marque_du_véhicule"]
    modele_array = at.dataframe[0].value["modèle_du_véhicule"]
    is_maker_correct = maker_array.astype(str).str.contains(filter_maker).all()
    is_control_correct = modele_array.astype(str).str.contains(filter_modele).all()
    assert is_maker_correct and is_control_correct

def test_add_filter():
    at = AppTest.from_file("app.py").run()
    at.multiselect[0].select("kilomètres").run()
    min_value, max_value = 40000, 100000
    at.slider[1].set_range(40000, 100000).run()
    km_array = at.dataframe[0].value["kilomètres"]
    assert (km_array.max() >= min_value) and (km_array.min() <= max_value)

def test_groupby_numeric():
    at = AppTest.from_file("app.py").run()
    at.selectbox[2].set_value("marque_du_véhicule").run()
    at.multiselect[1].select("prix_de_vente").run()
    at.selectbox[3].set_value("mean").run()
    is_maker_unique = at.dataframe[0].value.index.is_unique
    is_maker_index = at.dataframe[0].value.index.name == "marque_du_véhicule"
    assert is_maker_unique and is_maker_index

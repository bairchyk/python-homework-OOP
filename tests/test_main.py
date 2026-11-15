import pytest
from _pytest.capture import CaptureFixture

from main import Category, Product


@pytest.fixture
def test_product() -> list[Product]:
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    return [product1, product2, product3]


@pytest.fixture(autouse=True)
def reset_counters() -> None:
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def test_category(test_product: list[Product]) -> Category:
    return Category(
        "Смартфоны",
        "Смартфоны для коммуникации и удобства жизни",
        test_product,
    )


def test_init_product1(test_product: list[Product]) -> None:
    assert test_product[0].name == "Samsung Galaxy S23 Ultra"
    assert test_product[0].description == "256GB, Серый цвет, 200MP камера"
    assert test_product[0].price == 180000.0
    assert test_product[0].quantity == 5


def test_init_category(test_category: Category, test_product: list[Product]) -> None:
    assert test_category.name == "Смартфоны"
    assert test_category.description == "Смартфоны для коммуникации и удобства жизни"
    expected = (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"
    )
    assert test_category.products == expected


def test_product_count(test_category: Category) -> None:
    assert Category.product_count == 3


def test_category_count(test_category: Category) -> None:
    Category("Телевизоры", "Описание телевизоров", [])

    assert Category.category_count == 2


def test_price_getter() -> None:
    product = Product("Телефон", "Смартфон", 5000.0, 5)

    assert product.price == 5000.0


def test_price_setter_positive() -> None:
    product = Product("Телефон", "Смартфон", 5000.0, 5)

    product.price = 7000.0

    assert product.price == 7000.0


def test_price_setter_negative() -> None:
    product = Product("Телефон", "Смартфон", 5000.0, 5)

    product.price = -1000.0

    assert product.price == 5000.0


def test_price_setter_message(capsys: pytest.CaptureFixture[str]) -> None:
    product = Product("Телефон", "Смартфон", 5000.0, 5)

    product.price = -1000.0

    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"


def test_products_getter() -> None:
    product = Product("Телефон", "Смартфон", 5000.0, 5)
    category = Category("Электроника", "Техника", [product])

    assert category.products == "Телефон, 5000.0 руб. Остаток: 5 шт.\n"


def test_add_product() -> None:
    category = Category("Электроника", "Техника", [])
    product = Product("Телефон", "Смартфон", 5000.0, 5)

    before_count = Category.product_count

    category.add_product(product)

    assert Category.product_count == before_count + 1
    assert category.products == "Телефон, 5000.0 руб. Остаток: 5 шт.\n"

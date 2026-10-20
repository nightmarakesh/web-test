from pages.search_page import SearchPage


def test_search_returns_expected_products(driver):
    """Цель: найти MacBook. Ожидаются MacBook, MacBook Air и MacBook Pro."""
    page = SearchPage(driver)
    page.open()
    page.search("MacBook")

    actual_names = page.get_product_names()
    expected_names = ["MacBook", "MacBook Air", "MacBook Pro"]

    assert sorted(actual_names) == sorted(expected_names), (
        f"Ожидались товары: {expected_names}. Получены: {actual_names}"
    )

def test_search_without_results(driver):
    """Цель: найти отсутствующий товар. Ожидаются сообщение и отсутствие товаров."""
    page = SearchPage(driver)
    page.open()
    page.search("selenium_no_such_product_826491")

    actual_message = page.get_empty_message()
    expected_message = "Нет товаров, которые соответствуют критериям поиска."

    assert actual_message == expected_message, (
        f"Ожидалось сообщение: {expected_message!r}. Получено: {actual_message!r}"
    )

    product_count = page.get_product_count()

    assert product_count == 0, (
        f"Ожидалось отсутствие товаров, но найдено: {product_count}"
    )
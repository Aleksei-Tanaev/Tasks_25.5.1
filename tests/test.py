import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from settings import email, password


def test_list(testing):
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    try:
        mail = WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
    except RuntimeError:
        pytest.driver.quit()

    # Вводим email
    mail.send_keys(email)

    try:
        passw = WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "pass"))
        )
    except RuntimeError:
        pytest.driver.quit()

    # Вводим пароль
    passw.send_keys(password)
    # нажимаем кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    pytest.driver.implicitly_wait(10)
    # переходим на страницу своих питомцев
    pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')

    # получаем количество питомцев из статистики
    total_pets = int(pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split()[2])
    # получаем список из имени, породы и возраста питомцев
    my_pets_all = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets table tbody tr')
    # получаем список фото питомцев
    images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
    # получаем список имен питомцев
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    # получаем список пород питомцев
    species = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-of-type(2)')
    # получаем список возрастов питомцев
    ages = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-of-type(3)')

    # сравниваем количество питомцев из статистики и таблицы
    assert total_pets == len(my_pets_all)

    # проверяем наличие фотографий
    try:
        count = 0
        for i in range(len(images)):
            if images[i].get_attribute('src') != '':
                count += 1

        if len(my_pets_all) % 2 == 1:
            assert count >= len(my_pets_all)//2+1
        elif len(my_pets_all) % 2 == 0:
            assert count >= len(my_pets_all)//2
        print('Фотографии есть у большей части питомцев')
    except AssertionError:
        print('\n', 'Фотографии присутствуют у менее половины количества питомцев')

    # проверяем наличие имен у питомцев
    try:
        for i in range(len(names)):
            assert names[i].text != ''
        print('У всех животных есть имя')
    except AssertionError:
        print('Имеются животные без имени')

    # проверяем наличие породы у питомцев
    try:
        for i in range(len(species)):
            assert species[i].text != ''
        print('У всех животных есть порода')
    except AssertionError:
        print('Имеются животные беcпородные')

    # проверяем указание возраста у питомцев
    try:
        for i in range(len(ages)):
            assert ages[i].text != ''
        print('У всех животных указан возраст')
    except AssertionError:
        print('Имеются животные без возраста')

    # проверяем уникальность имен
    try:
        name_list = []
        for i in names:
            name_list.append(i.text)
        name_list.sort()
        for i in range(len(name_list)):
            if i < len(name_list) - 1:
                assert name_list[i] != name_list[i+1]
        print("Животных с одинаковыми именами нет")
    except AssertionError:
        print('Есть животные с одинаковыми именами')

    # проверяем уникальность животных
    my_pets_all_list = []
    for i in range(len(my_pets_all)):
        my_pets_all_list.append(str(my_pets_all[i].text))
    my_pets_all_list.sort()

    try:
        for i in range(len(my_pets_all_list)):
            if i < len(my_pets_all_list) - 1:
                assert my_pets_all_list[i] != my_pets_all_list[i + 1]
        print('Повторных животных нет')
    except AssertionError:
        print('Есть одинаковые животные')

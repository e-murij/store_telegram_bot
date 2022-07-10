# store_telegram_bot
telegram бот, имитирующий простейшее управление магазином  

## Интерфейс
1. Возможность просмотреть информацию о магазине, настройки и приступить к выбору товара  

![MarineGEO circle logo](interface_screen/Screenshot_1.png "MarineGEO logo")  

2. Просмотр информации о магазине, возможность вернуться на стартовую страницу  

![MarineGEO circle logo](interface_screen/Screenshot_2.png "MarineGEO logo")  

3. Выбор категории продукта в нижнем меню, выбор продукта и добавление его в заказ в инлайн меню  

![MarineGEO circle logo](interface_screen/Screenshot_3.png "MarineGEO logo")  

4. Просмотр информации по товарам в заказе, возможность переходить между позициями заказа и изменять количество единиц товара, возможность оформить заказ  

![MarineGEO circle logo](interface_screen/Screenshot_4.png "MarineGEO logo")

5. Заказ отпрален на склад, выведена информация о заказе  

![MarineGEO circle logo](interface_screen/Screenshot_5.png "MarineGEO logo")  

## Запуск проекта
1. Клонировать репозиторий
2. В директории store_telegram_bot\setttings заполнить файл .env.template и переименовать его в .env
3. Для создания тестовой базы данных и наполнения ее данными можно запустить скрипт store_telegram_bot\data_base\create_and_fill_DB.py
4. Запустить скрипт store_telegram_bot\telegram_bot.py
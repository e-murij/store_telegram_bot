from setttings.messages import MESSAGES
from setttings import config
from handlers.handler import Handler
from data_base import servises


class HandlerAllTextCommands(Handler):
    """ Класс обрабатывает текстовые сообщения от нажатия на кнопки """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_info(self, message):
        """ Обрабатывает нажатие на кнопоку 'О магазине'. """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.info_menu()
                              )

    def pressed_btn_settings(self, message):
        """ Обрабатывает нажатие на кнопоку 'Настройки'. """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.settings_menu()
                              )

    def pressed_btn_back(self, message):
        """ Обрабатывает нажатие на кнопку 'Назад'."""
        self.bot.send_message(message.chat.id, "Вы вернулись к стартовому меню",
                              reply_markup=self.keyboards.start_menu()
                              )

    def pressed_btn_category(self, message):
        """ Обрабатывает нажатие на кнопку 'Выбрать товар'. Выбор категории товаров. """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keyboards.remove_menu()
                              )
        self.bot.send_message(message.chat.id, "Выберите категорию товара",
                              reply_markup=self.keyboards.category_menu()
                              )

    def pressed_btn_product(self, message, product):
        """ Обрабатывает  нажатие на кнопку 'Выбрать товар'. Выбор товара из категории """
        self.bot.send_message(message.chat.id, 'Категория ' +
                              config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product])
                              )
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keyboards.category_menu()
                              )

    def pressed_btn_order(self, message):
        """ Обрабатывает нажатие на кнопку 'Заказ'."""
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_up(self, message):
        """ Обработвает нажатие кнопки увеличения количества определенного товара в заказе """
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_douwn(self, message):
        """ Обработывает нажатие кнопки уменьшения количества определенного товара в заказе """
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """ Обработывает нажатие кнопки удаления товарной позиции заказа """
        count = self.BD.select_all_product_id()
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            quantity_product = self.BD.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            self.BD.delete_order(count[self.step])
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
            if self.step > 0:
                self.step -= 1
        count = self.BD.select_all_product_id()
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keyboards.category_menu()
                                  )

    def pressed_btn_back_step(self, message):
        """ Обрабтывает нажатие кнопки перемещения к более ранним товарным позициям заказа """
        if self.step > 0:
            self.step -= 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        """ Обработывает нажатие кнопки перемещения к более поздним товарным позициям заказа """
        if self.step < self.BD.count_rows_order()-1:
            self.step += 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apply(self, message):
        """ Обрабатывает нажатие на кнопку 'Оформить заказ'. """
        self.bot.send_message(message.chat.id,
                              MESSAGES['apply'].format(
                                  servises.get_total_coast(self.BD),
                                  servises.get_total_quantity(self.BD)),
                              parse_mode="HTML",
                              reply_markup=self.keyboards.category_menu())
        self.BD.delete_all_order()

    def send_message_order(self, product_id, quantity, message):
        """ Отправляет ответ пользователю при выполнении различных действий с заказом"""
        self.bot.send_message(message.chat.id,MESSAGES['order_number'].format(self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(product_id),
                                     self.BD.select_single_product_title(product_id),
                                     self.BD.select_single_product_price(product_id),
                                     self.BD.select_order_quantity(product_id)
                                     ),
                              parse_mode="HTML",
                              reply_markup=self.keyboards.orders_menu(self.step, quantity)
                              )

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # основные меню
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            # категории товаров
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            # заказ
            if message.text == config.KEYBOARD['ORDER']:
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keyboards.category_menu()
                                          )

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_douwn(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_btn_apply(message)
            # иные нажатия и ввод данных пользователем
            else:
                self.bot.send_message(message.chat.id, message.text)


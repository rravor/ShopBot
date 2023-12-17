from aiogram.fsm.state import StatesGroup, State


class AddProduct(StatesGroup):
    data = State()


class AddUser(StatesGroup):
    enter_name = State()
    enter_username = State()
    enter_phone_number = State()
    enter_email = State()
    enter_address = State()


class DeleteProduct(StatesGroup):
    id = State()


class UpdateProduct(StatesGroup):
    id = State()
    data = State()


class CheckProduct(StatesGroup):
    id = State()


class UpdateUser(StatesGroup):
    id = State()
    data = State()


class CheckProductCategory(StatesGroup):
    id = State()


class CheckProudctBrend(StatesGroup):
    id = State()


class GetExcelFile(StatesGroup):
    file = State()
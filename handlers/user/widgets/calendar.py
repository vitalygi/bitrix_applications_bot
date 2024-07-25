from contextlib import suppress
from datetime import date, timedelta
from typing import Dict, List

from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, CallbackQuery
from babel.dates import get_day_names, get_month_names

from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Calendar, CalendarScope, ManagedCalendar, Button,
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView, CalendarMonthView,
    CalendarScopeView, CalendarYearsView,
    DATE_TEXT, TODAY_TEXT, CalendarConfig, BEARING_DATE, CalendarUserConfig, CALLBACK_PREV_YEAR, CALLBACK_NEXT_YEAR,
    empty_button, month_begin, next_month_begin, CALLBACK_PREV_MONTH, CALLBACK_NEXT_MONTH,
)
from aiogram_dialog.widgets.text import Const, Format, Text

from keyboard.utils import application_back_markup_with_action
from routers.create_application_fabric import ApplicationAction
from states.user.create_application import ApplicationStatesGroup
from handlers.utils.user_utils import date_selected

from handlers.utils.utils import mark_message_to_del


class CalendarState(StatesGroup):
    DEFAULT = State()
    MAIN = State()
    CUSTOM = State()


SELECTED_DAYS_KEY = "selected_dates"


class CustomCalendarDaysView(CalendarDaysView):

    async def _render_pager(
            self,
            config: CalendarUserConfig,
            offset: date,
            data: Dict,
            manager: DialogManager,
    ) -> List[InlineKeyboardButton]:
        curr_month = offset.month
        next_month = (curr_month % 12) + 1
        prev_month = (curr_month - 2) % 12 + 1
        prev_end = month_begin(offset) - timedelta(1)
        prev_begin = month_begin(prev_end)
        next_begin = next_month_begin(offset)
        if (
                prev_end < self.config.min_date and
                next_begin > self.config.max_date
        ):
            return []

        prev_month_data = {
            "month": prev_month,
            "date": prev_begin,
            "data": data,
        }
        curr_month_data = {
            "month": curr_month,
            "date": BEARING_DATE.replace(month=curr_month),
            "data": data,
        }
        next_month_data = {
            "month": next_month,
            "date": next_begin,
            "data": data,
        }
        if prev_end < self.config.min_date:
            prev_button = empty_button()
        else:
            prev_button = InlineKeyboardButton(
                text=await self.prev_month_text.render_text(
                    prev_month_data, manager,
                ),
                callback_data=self.callback_generator(CALLBACK_PREV_MONTH),
            )
        if next_begin > self.config.max_date:
            next_button = empty_button()
        else:
            next_button = InlineKeyboardButton(
                text=await self.next_month_text.render_text(
                    next_month_data, manager,
                ),
                callback_data=self.callback_generator(CALLBACK_NEXT_MONTH),
            )

        return [prev_button, next_button]


class CustomCalendarMonthView(CalendarMonthView):
    async def _render_pager(
            self,
            config: CalendarUserConfig,
            offset: date,
            data: Dict,
            manager: DialogManager,
    ) -> List[InlineKeyboardButton]:
        curr_year = offset.year
        next_year = curr_year + 1
        prev_year = curr_year - 1

        if curr_year not in range(
                self.config.min_date.year, self.config.max_date.year,
        ):
            return []

        prev_year_data = {
            "year": prev_year,
            "date": max(
                BEARING_DATE.replace(year=prev_year),
                self.config.min_date,
            ),
            "data": data,
        }
        curr_year_data = {
            "year": curr_year,
            "date": BEARING_DATE.replace(year=curr_year),
            "data": data,
        }
        next_year_data = {
            "year": next_year,
            "date": min(
                BEARING_DATE.replace(year=next_year),
                self.config.max_date,
            ),
            "data": data,
        }
        if prev_year < self.config.min_date.year:
            prev_button = empty_button()
        else:
            prev_button = InlineKeyboardButton(
                text=await self.prev_year_text.render_text(
                    prev_year_data, manager,
                ),
                callback_data=self.callback_generator(CALLBACK_PREV_YEAR),
            )
        if next_year > self.config.max_date.year:
            next_button = empty_button()
        else:
            next_button = InlineKeyboardButton(
                text=await self.next_year_text.render_text(
                    next_year_data, manager,
                ),
                callback_data=self.callback_generator(CALLBACK_NEXT_YEAR),
            )
        return [prev_button, next_button]


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_day_names(
            width="short", context='stand-alone', locale=locale,
        )[selected_date.weekday()].title()


class MarkedDay(Text):
    def __init__(self, mark: str, other: Text):
        super().__init__()
        self.mark = mark
        self.other = other

    async def _render_text(self, data, manager: DialogManager) -> str:
        current_date: date = data["date"]
        serial_date = current_date.isoformat()
        selected = manager.dialog_data.get(SELECTED_DAYS_KEY, [])

        if serial_date in selected:
            return "✅"

        return await self.other.render_text(data, manager)


3


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            'wide', context='stand-alone', locale=locale,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CustomCalendarDaysView(
                self._item_callback_data,
                date_text=MarkedDay("🔴", DATE_TEXT),
                today_text=MarkedDay("⭕", TODAY_TEXT),
                header_text="~~~~~ " + Month() + " ~~~~~",
                weekday_text=WeekDay(),
                next_month_text=Month() + " >>",
                prev_month_text="<< " + Month(),
                config=CalendarConfig()
            ),
            CalendarScope.MONTHS: CustomCalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                header_text="~~~~~ " + Format("{date:%Y}") + " ~~~~~",
                this_month_text="[" + Month() + "]",
                config=CalendarConfig()
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
                config=CalendarConfig()
            ),
        }


def check_date(selected, current, start_data):
    if len(selected) == 0:
        return True
    selected.sort()

    return True


async def on_date_selected(
        callback: ChatEvent,
        widget: ManagedCalendar,
        manager: DialogManager,
        clicked_date: date, /,
):
    selected = manager.dialog_data.setdefault(SELECTED_DAYS_KEY, [])
    serial_date = clicked_date.isoformat()
    if serial_date in selected:
        selected.sort()
        index = [x for x in range(0, len(selected)) if selected[x] == serial_date][0]
        if index == 0 or index == (len(selected) - 1):
            selected.remove(serial_date)
    elif len(selected)==0:
        selected.append(serial_date)


async def selection_getter(dialog_manager, **_):
    selected = dialog_manager.dialog_data.get(SELECTED_DAYS_KEY, [])
    selected_to_print = []
    for day in selected:
        str_date = date.fromisoformat(day)
        selected_to_print.append(str_date.strftime('%d.%m.%y'))
    return {
        "selected": "\n".join(sorted(selected_to_print)),
    }


async def back_clicked(callback: CallbackQuery, button: Button,
                       manager: DialogManager):
    message = callback.message
    state = manager.middleware_data['state']
    with suppress(Exception):
        await callback.message.delete()
    await mark_message_to_del(await message.answer('Введите сумму:',
                                                   reply_markup=application_back_markup_with_action(
                                                       ApplicationAction.enter_comments)), state)
    await state.set_state(ApplicationStatesGroup.enter_amount)
    await manager.done()


async def dates_selected_clicked(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    selected = manager.dialog_data.get('selected_dates', [])
    if len(selected) == 0:
        pass
    else:
        state = manager.middleware_data['state']
        selected.sort()
        await date_selected(callback, state, selected[0])
        await manager.done()


CALENDAR_BACK_BUTTON = Button(
    text=Const("Назад"), id="back_button", on_click=back_clicked
)

BOOK_BUTTON = Button(
    text=Const("Далее"), id="next", on_click=dates_selected_clicked
)

calendar_dialog = Dialog(
    Window(
        Format("\nВы выбрали:\n{selected}", when=F["selected"]),
        Format("\nВыберите дату оплаты", when=~F["selected"]),
        CustomCalendar(
            id="cal",
            on_click=on_date_selected,
        ),
        BOOK_BUTTON,
        CALENDAR_BACK_BUTTON,
        getter=selection_getter,
        state=CalendarState.MAIN,
    ),
)

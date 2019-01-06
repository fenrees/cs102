import datetime as datetime
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    # перебираем друзей создаем список дат
    friends = [User(**i) for i in get_friends(user_id, 'bdate')]
        # сегодняшняя дата
        current_date = datetime.date(datetime.now())
        #создаем список возрастов приятелей(каркас)
        age_list = []
        for person in friends:
            # др друга перменная
            bday = person.bdate
            try:
                # прогоняем у пользователя дату месяц и число рождения
                bd = datetime.strptime(bday, "%d.%m.%Y")
            #если нет то юзер проходит мимо
            except (ValueError, TypeError):
                pass
            else:
               #считает возраст пользователя считая данный год - год рождения вычитая данный месяц и день если они меньше даты рождения
                age = current_date.year - bd.year - ((current_date.month, current_date.day) < (bd.month, bd.day))
                age_list.append(age)
        if age_list:
        return float(median(age_list))

from collections import Counter
import datetime
import plotly
from typing import List, Tuple
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    # считает количество повторяющихся дат сообщений 1.09 1.10 1.11 и тд
    c = Counter()
    for message in messages:
        date = fromtimestamp(message.date)
        c[date] += 1
    # * выводит перменные по отдельности из списка
    # zip возвращает кортеж на каждой интерации, на выходе список  потому что list но так кортеж будет (интератор - класс, генерирующий последовательность значений)
    # будет ([дата, кол-во сообщений в эту дату с этим челом])
    result = list(zip(*c.most_common()))
    return tuple((sorted(result[0]), [c[date] for date in sorted(result[0])]))


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [plotly.graph_objs.Scatter(x=dates, y=freq)]
    plotly.plotly.plot(data)
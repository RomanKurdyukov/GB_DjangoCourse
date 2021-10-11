from django import template
import datetime

register = template.Library()


@register.simple_tag
def monthname():
    dt = datetime.datetime.today()
    ru = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня', 7: 'июля',
          8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}
    return ru[dt.month]

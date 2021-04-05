import datetime


def is_valid_date_and_time(value):
    """
    Checking input data
    :param value-> string:
    :return <class 'datetime.datetime'> or False:

    """
    if not isinstance(value, str):
        return False
    list_of_numb = value.split(".")
    if len(list_of_numb) != 5:
        return False
    day = int(list_of_numb[0])
    month = int(list_of_numb[1])
    year = int(list_of_numb[2])
    hour = int(list_of_numb[3])
    minutes = int(list_of_numb[4])
    try:
        date_time = datetime.datetime(year, month, day, hour, minutes)
        return date_time
    except ValueError:
        return False


if __name__ == '__main__':
    print(is_valid_date_and_time("5.10.2009.10.00"))

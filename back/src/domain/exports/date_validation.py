from datetime import *


def date_validation(datefrom, dateto):
    format = "%m-%Y-%d"
    res = True
    try:
        res = bool(datetime.strptime(datefrom, format))
        res_1 = bool(datetime.strptime(dateto, format))
    except ValueError:
        res = None
        res_1 = None
    return (res, res_1)


def validation_2(datefrom, dateto):
    d = datefrom.split("-")
    d_2 = dateto.split("-")
    if (
        len(d[0]) != 4
        or len(d[1]) != 2
        or len(d[2]) != 2
        or len(d_2[0]) != 4
        or len(d_2[1]) != 2
        or len(d_2[2]) != 2
    ):
        return None
    else:
        return (datefrom, dateto)


print(validation_2("2022-04-21", "2022-06-23"))

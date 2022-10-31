def first(list, prediace):
    try:
        return next(el for el in list if prediace(el))
    except:
        return None
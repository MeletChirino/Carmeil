sign = '''Best regards
Jhon Doe
My companie
Phone: 07 06 05 04 03 02
'''
def message():
    return F'''Estimado cliente {name},
Lamentamos informarle que su pedid #{id_pedido} no podra ser enviado antes de la fecha {fecha}. Lamentamos mucho los inconvenientes. Gracias por su preferencia.
'''

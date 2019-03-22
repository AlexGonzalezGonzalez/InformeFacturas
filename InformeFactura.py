import os

from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer, Paragraph, Table, TableStyle)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from sqlite3 import dbapi2




try:
    detalleFactura = []
    facturas = []

    bbdd = dbapi2.connect("facturaDB.db")
    cursor = bbdd.cursor()

    #cursor.execute("create table clientes (codc text, nomc text, direccion text)")
    #cursor.execute("create table facturas (numf number, codc text, codp text, cantidad number)")
    #cursor.execute("create table productos (codp text, descripcion text, precio number)")

    #cursor.execute("""insert into clientes values('111a','Quique','O Rosal')""")
    #cursor.execute("""insert into clientes values('222b','Alejandro','Cangas')""")

    #cursor.execute("""insert into facturas values('0001','111a','0101','3')""")
    #cursor.execute("""insert into facturas values('0001','111a','0102','5')""")
    #cursor.execute("""insert into facturas values('0001','111a','0103','1')""")

    #cursor.execute("""insert into productos values('0101','Tizas','9')""")
    #cursor.execute("""insert into productos values('0102','Rotuladores','5')""")
    #cursor.execute("""insert into productos values('0103','Borradores','4')""")
    #bbdd.commit()



    cursorConsultaNumFacturas = cursor.execute("select numf from facturas group by numf")

    listaFacturas = list()

    for numF in cursorConsultaNumFacturas:
        if numF[0] not in listaFacturas:
            listaFacturas.append(numF[0])

        for numF in listaFacturas:
            codc = None
            consultaFactura = None
            cursorConsultaFactura = cursor.execute("select codc from facturas where numf = ?", (int(numF),))
            codc = cursorConsultaFactura.fetchone()[0]
            # Primera linea de la factura.
            detalleFactura.append(['Codigo Cliente: ', codc, '', 'Numero Factura: ', numF])

            cursorConsultaFactura = cursor.execute("select nomc, direccion from clientes where codc = '" + str(codc) + "'")
            registroCliente = cursorConsultaFactura.fetchone()

            detalleFactura.append(['Nombre', registroCliente[0], '', '', ''])
            detalleFactura.append(['Direccion', registroCliente[1], '', '', ''])

            cursorConsultaDetalle = cursor.execute("select codp, cantidad from facturas where numf = ?", (int(numF),))
            listaConsultaDetalleFactura = []

        for elementoFac in cursorConsultaDetalle:
            listaConsultaDetalleFactura.append([elementoFac[0], elementoFac[1]])

        for elemento in listaConsultaDetalleFactura:
            cursorConsultaProducto = cursor.execute("select descripcion, precio from productos where codp = '" +
            str(elemento[0]) + "'")
            registroProducto = cursorConsultaProducto.fetchone()

            detalleFactura.append(
            [elemento[0], registroProducto[0], elemento[1], registroProducto[1], elemento[1] * registroProducto[1]])

    facturas.append(list(detalleFactura))
    detalleFactura.clear()

except(dbapi2.DatabaseError):
    print("Error en la base de datos")

finally:
    print("Cerrando cursor y conexion de la base de datos")
    cursor.close()
    bbdd.close()

doc = SimpleDocTemplate("TableFacturas.pdf", pagesize=A4)
guion = []

for factura in facturas:
    tabla = Table(factura, colWidths=80, rowHeights=30)
    tabla.setStyle(TableStyle([
    ('TEXTCOLOR', (0, 0), (-1, 2), colors.blue),
    ('TEXTCOLOR', (0, 4), (-1, -1), colors.green),
    ('ALIGN',(2,5),(-1,-1),'RIGHT'),
    ('BACKGROUND', (0, 4), (-1, -1), colors.lightcyan),
    ('BOX', (0, 4), (-1, -2), 1, colors.black),
    ('BOX', (0, 0), (-1, 2), 1, colors.black),
    ('INNERGRID', (0, 3), (-1, -2), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    guion.append(tabla)

doc.build(guion)
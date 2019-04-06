#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import sqlite3

BD = "facturas.sqlite3"

@click.group()
def crud():
    pass

@crud.command()
@click.argument("razonsocial")
@click.argument("rfc")
def c_cliente(razonsocial, rfc):
    """ Inserta un registro en la tabla Cliente """
    # Se arma una tupla con los campos
    print(razonsocial)
    print(rfc)
    campos = (razonsocial, rfc)
    # Se realiza la conexión a la base de datos
    conn = sqlite3.connect(BD)
    # Se obtiene un cursor o indice a la base de datos
    cur = conn.cursor()
    # Se ejecuta la consulta SQL colocando un símbolo ? para cada valor de cada
    # campo para evitar inyección SQL. Es la recomendación que hace el módulo
    # sqlite3.
    cur.execute("insert into Cliente values (null, ?, ?)", campos)
    # Se ejecuta un commit para indicar que la inserción se ejecute como una
    # operación atómica.
    conn.commit()
    # Se cierra la base de datos
    conn.close()
    # Se muestra un mensaje al usuario
    print("Se ha insertado el registro {} en la tabla Cliente".format(campos))

@crud.command()
def r_cliente():
    """ Imprime la lista de registros de la tabla Cliente """
    # Se realiza la conexión a la base de datos y with la cierra en automático
    with sqlite3.connect(BD) as conn:
        # Se obtiene un cursor o indice a la base de datos
        cur = conn.cursor()
        # Se ejecuta la consulta SQL colocando un símbolo ? para cada valor de
        # cada campo para evitar inyección SQL. Es la recomendación que hace el
        # módulo sqlite3.
        cur.execute("select * from Cliente")
        # Se obtiene la lista de campos y se agrega como primer posición en la
        # lista de resultados.
        res = [[r[0] for r in cur.description]]
        # Se obtiene la lista de resultados de la consulta SQL
        res += cur.fetchall()

    # Se obtiene el ancho máximo de cada columna
    anchos = [[len(str(c)) for c in f] for f in res]
    anchos = [max(f) for f in zip(*anchos)]
    # Se imprime la tabla de resultados
    for fila in res:
        # Se remplaza los campos vaciós por cademas vacías.
        fila = [c if c != None else "" for c in fila]
        # A cada campo se agrega el valor del ancho
        fila = tuple(zip(fila, anchos))
        # A cada campo se le dá formato
        fila = ["{:{}}".format(*c) for c in fila]
        # Se fusionan los campos en una cadena y se imprimen
        print(" | ".join(fila))

@crud.command()
@click.argument("idcliente")
@click.argument("campo")
@click.argument("valor")
def u_cliente(idcliente, campo, valor):
    """ Actualiza los datos de un Cliente """
    # Se realiza la conexión a la base de datos
    with sqlite3.connect(BD) as conn:
        # Se obtiene un cursor o indice a la base de datos
        cur = conn.cursor()
        # Se crea la consulta SQL
        sql = "update Cliente set {}=? where idCliente=?".format(campo)
        # Se crea la tupla de valores
        valores = (valor, idcliente)
        # Se ejecuta la consulta SQL agregando los valores de forma segura
        cur.execute(sql, valores)
        # Se ejecuta un commit para indicar a la BD que la actualización se
        # ejecute como una operación atómica.
        conn.commit()

    # Se muestra un mensaje al usuario
    print("Se ha actualizado el registro {} en la tabla Autor".format(idcliente))


@crud.command()
@click.argument("idcliente")
def d_cliente(idcliente):
    """ Elimina un registro de un CLiente """
    # Se realiza la conexión a la base de datos
    with sqlite3.connect(BD) as conn:
        # Se obtiene un cursor o indice a la base de datos
        cur = conn.cursor()
        # Se crea la consulta SQL
        sql = "delete from Cliente where idCliente=?"
        # Se crea la tupla de valores
        valores = (idcliente,)
        # Se ejecuta la consulta SQL agregando los valores de forma segura
        cur.execute(sql, valores)
        # Se ejecuta un commit para indicar a la BD que la aliminación se
        # ejecute como una operación atómica.
        conn.commit()

    # Se muestra un mensaje al usuario
    print("Se ha eliminado el registro {} en la tabla Autor".format(idcliente))


if __name__ == '__main__':
    crud()

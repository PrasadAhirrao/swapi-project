"""

pip install pymysql
pip install cryptography


# if you want to create new user and want to grant to root permissions to him

CREATE USER adam@localhost IDENTIFIED BY 'qwerty@123';
GRANT ALL PRIVILEGES ON *.* TO adam WITH GRANT OPTION;
SHOW GRANTS FOR adam;

"""

import yaml
import toml
import pymysql
from typing import List


def get_db_conn():

    filepath = "settings/secrets.yaml"
    with open(filepath, "r") as foo:
        doc = yaml.load(foo, Loader=yaml.FullLoader)
        connection_ = pymysql.connect(**doc)
        return connection_


def get_db_conn_toml():

    toml_path = "settings/secrets.toml"

    with open(toml_path, "r") as foo:
        config = toml.load(foo)
        dbconfig = config.get("mysqldb")
        connection_ = pymysql.connect(**dbconfig)
        return connection_


def insert_resource(
        table_name: str,
        primary_key_: str,
        primary_value: int,
        columns_: List,
        values: List
):
    """

    Args:
        table_name (str):
        primary_key_ (str):
        primary_value (int):
        columns_ (list):
        values (list):

    Returns:
        number of records inserted in DB table
    """

    column_names = ", ".join(columns_)
    value_fields = ", ".join(values)

    column_names.rstrip(", ")
    value_fields.rstrip(", ")

    value_fields = ""
    for value in values:
        if isinstance(value, str):
            value_fields = value_fields + '''"''' + value + '''"''' + ''', '''
        elif isinstance(value, int):
            value_fields = value_fields + str(value) + ''','''

    value_fields = value_fields.rstrip(""", """)

    result = None
    with get_db_conn() as conn:
        cursor = conn.cursor()
        sql_magic = f"""insert into starwarsDB.{table_name} ({primary_key_}, {column_names}) values ({primary_value}, {value_fields});"""
        result = cursor.execute(sql_magic)
        conn.commit()
    return result


if __name__ == "__main__":
    yaml_conn = get_db_conn()
    toml_conn = get_db_conn_toml()


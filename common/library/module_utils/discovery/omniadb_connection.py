# Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# pylint: disable=import-error,no-name-in-module,line-too-long

"""
Database connection utilities for Omnia discovery modules.
"""
import sys
import psycopg2 as pg
from psycopg2.extras import DictCursor
from cryptography.fernet import Fernet


KEY_FILE_PATH = "/opt/omnia/.postgres/.postgres_pass.key"
PASS_FILE_PATH = "/opt/omnia/.postgres/.encrypted_pwd"

with open(KEY_FILE_PATH, "rb") as passfile:
    key = passfile.read()
fernet = Fernet(key)

with open(PASS_FILE_PATH, "rb") as datafile:
    encrypted_file_data = datafile.read()
decrypted_pwd = fernet.decrypt(encrypted_file_data).decode()


def create_connection():
    """
    Create a database connection to the omniadb.

    This function establishes a connection to the omniadb database using the provided password.
    It reads the encrypted password from a file,
        decrypts it using the provided key, and connects to the database.

    Parameters:
        None

    Returns:
        conn (psycopg2.extensions.connection): The database connection.
    """
    # Create database connection
    conn = pg.connect(
        database="omniadb",
        user="postgres",
        password=decrypted_pwd,
        host="localhost",
        port="5432",
    )
    conn.autocommit = True
    return conn


def create_connection_xcatdb():
    """
    Create a database connection to the xcatdb.

    This function establishes a connection to the xcatdb database using the provided password.
    It reads the encrypted password from a file,
        decrypts it using the provided key, and connects to the database.

    Parameters:
        None

    Returns:
        conn (psycopg2.extensions.connection): The database connection.
    """
    # Create database connection
    conn = pg.connect(
        database="xcatdb",
        user="postgres",
        password=decrypted_pwd,
        host="localhost",
        port="5432",
    )
    conn.autocommit = True
    return conn


def insert_node_info(
    service_tag,
    node,
    hostname,
    admin_mac,
    admin_ip,
    bmc_ip,
    group_name,
    role,
    cluster_name,
    parent,
    location_id,
    architecture,
    discovery_mechanism,
    bmc_mode,
    switch_ip,
    switch_name,
    switch_port,
):

    """
    Inserts node information into the cluster.nodeinfo table.

    Parameters:
        service_tag (str): The service tag of the node.
        node (str): The node name.
        hostname (str): The hostname of the node.
        admin_mac (str): The MAC address of the admin interface.
        admin_ip (Union[str, None]): The IP address of the admin interface.
        bmc_ip (Union[str, None]): The IP address of the BMC.
        group_name (str): The group the node belongs to.
        role (str): The role of the node.
        cluster_name (str): The name of the cluster.
        parent (str): The parent node service tag.
        location_id (str): The location ID of the node.
        architecture (str): The architecture of the node.
        discovery_mechanism (str): The mechanism used to discover the node.
        bmc_mode (str): The mode of the BMC.
        switch_ip (Union[str, None]): The IP address of the switch.
        switch_name (str): The name of the switch.
        switch_port (str): The port of the switch.

    Returns:
        None
    """
    conn = create_connection()
    cursor = conn.cursor()

    sql = """INSERT INTO cluster.nodeinfo(
                service_tag, node, hostname, admin_mac, admin_ip, bmc_ip, group_name, role, cluster_name, parent, location_id, architecture,
                discovery_mechanism, bmc_mode, switch_ip, switch_name, switch_port)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    params = (
        service_tag,
        node,
        hostname,
        admin_mac,
        str(admin_ip) if admin_ip else None,
        str(bmc_ip) if bmc_ip else None,
        group_name,
        role,
        cluster_name,
        parent,
        location_id,
        architecture,
        discovery_mechanism,
        bmc_mode,
        str(switch_ip) if switch_ip else None,
        switch_name,
        switch_port,
    )

    cursor.execute(sql, params)
    conn.commit()
    conn.close()


def insert_switch_info(switch_name, switch_ip, group):
    """
    Inserts switch details into the cluster.switchinfo table.

    Parameters:
        switch_name (str): The name of the switch.
        switch_ip (str): The IP address of the switch.

    Returns:
        None
    """
    conn = create_connection()
    cursor = conn.cursor()
    # Insert switch details to cluster.switchinfo table
    sql = """INSERT INTO cluster.switchinfo(switch_name,switch_ip, group_name) VALUES (%s,%s,%s)"""
    params = (switch_name, switch_ip, group)
    cursor.execute(sql, params)

    return (f"Inserted switch_ip: {switch_ip} with switch_name: "
            f"{switch_name} into cluster.switchinfo table")


def get_data_from_db(db="omniadb", table_name="cluster.nodeinfo", filter_dict=None):
    """
    Retrieves data from the database based on the provided filter.

    Parameters:
        db (str): The name of the database.
        table_name (str): The name of the table.
        filter_dict (dict): A dictionary containing the filter conditions.
            The keys of the dictionary are the column names and the values are the filter values.

    Returns:
        list: The result of the query.

    Raises:
        Exception: If the database query fails.
    """
    conn = get_db_connection(db)
    cursor = conn.cursor(cursor_factory=DictCursor)
    if filter_dict is None:
        filter_dict = {}
    filter_query, params = create_filter_query(filter_dict)

    query = f"SELECT * FROM {table_name} WHERE true{filter_query}"

    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as ex:
        sys.exit(f"Failed to fetch data from the database: {ex}")


def create_filter_query(filter_dict):
    """
    Creates the query and parameters for filtering.

    Parameters:
        filter_dict (dict): A dictionary containing the filter conditions.

    Returns:
        tuple: A tuple containing the filter query and the parameters.
    """
    filter_query = ""
    params = []

    for col, val in filter_dict.items():
        if col == "role":
            filter_query += f" AND {col} ~* %s"
            params.append(f".*{val}.*")
        else:
            filter_query += f" AND {col}=%s"
            params.append(val)

    return filter_query, params


def get_db_connection(db):
    """
    Returns the database connection.

    Parameters:
        db (str): The name of the database.

    Returns:
        psycopg2.extensions.connection: The database connection.

    Raises:
        Exception: If the database connection fails.
    """
    if db == "omniadb":
        conn = create_connection()
    elif db == "xcatdb":
        conn = create_connection_xcatdb()
    else:
        sys.exit(f"Invalid database: {db}")

    return conn


def execute_select_query(query, db="omniadb", params=None):
    """
    Executes a user-provided query on the given database and returns the result.

    Parameters:
        query (str): The SQL query to execute.
        db (str): The database name, default is 'omniadb'.
        params (tuple, optional): Parameters for the query to prevent SQL injection.

    Returns:
        list: Query result as a list of dictionaries.

    Raises:
        Exception: If the query execution fails.
    """
    conn = get_db_connection(db)
    cursor = conn.cursor(cursor_factory=DictCursor)

    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(row) for row in result]  # Convert to list of dicts
    except Exception as ex:
        sys.exit(f"Failed to execute query: {ex}")

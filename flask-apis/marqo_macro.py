"""Defined Macros to Operate VectorDB-related Operations
"""


import os


VECTOR_DB_IP = os.getenv("VECTOR_DB_IP")
VECTOR_DB_PORT = os.getenv("VECTOR_DB_PORT")

assert VECTOR_DB_IP is not None, "`VECTOR_DB_IP` Environment Variable is `None`."
assert VECTOR_DB_PORT is not None, "`VECTOR_DB_PORT` Environment Variable is `None`."

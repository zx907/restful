# AsIs wrapper can return a string representation of wrapped object with getquoted() func
import re
import psycopg2
from psycopg2.extensions import adapt, register_adapter, AsIs

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def adapt_point(point):
    x = adapt(point.x).getquoted()
    y = adapt(point.y).getquoted()
    return AsIs("'(%s, %s)'" % (x, y))

register_adapter(Point, adapt_point)

def cast_point(value, cur):
    if value is None:
        return None

    m = re.match(r"\(([^)]+),([^)]+)\)", value)
    if m:
        return Point(float(m.group(1)), float(m.group(2)))
    else:
        raise InterruptedError("bad point representation: %r" % value)

def register_point_type(engine):
    register_adapter(Point, adapt_point)
    rs = engine.execute("SELECT NULL::point")
    point_oid = rs.cursor.description[0][1]
    POINT = psycopg2.extensions.new_type((point_oid,), "POINT", cast_point)
    psycopg2.extensions.register_type(POINT)
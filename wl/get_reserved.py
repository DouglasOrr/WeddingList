"""List out the reserved items, as a CSV.
"""

from . import util


with util.UsingConn(util.connect()) as conn, util.UsingCursor(conn) as cursor:
    cursor.execute("""
    SELECT claim.email, claim.name, item.id as item_id, item.title as item
    FROM claim LEFT JOIN item ON claim.item_id=item.id
    ORDER BY claim.email
    """)
    print(','.join(cursor.column_names))
    for row in cursor:
        print(','.join('"{}"'.format(col) for col in row))

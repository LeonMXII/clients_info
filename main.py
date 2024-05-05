import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(20) not null,
            last_name VARCHAR(20) not null ,
            email VARCHAR(40) not null,
            phone_number VARCHAR(50) not null
        );
        """)
        conn.commit()

def add_clint(conn, id, name, last_name, email, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(id, name, last_name, email, phone_number) VALUES(%s, %s, %s, %s, %s);
        """, (id, name, last_name, email, phone_number))
        conn.commit()
#
def add_phone_number(conn, id, add_phone):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO client(id, phone_number) VALUES(%s, %s);
                """, (id, add_phone))
        conn.commit()
#
def change_client(conn, id, name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        if name is not None:
            cur.execute("""
                UPDATE client SET name=%s WHERE id=%s;
            """, (name, id))
        if last_name is not None:
            cur.execute("""
                UPDATE client SET last_name=%s WHERE id=%s;
            """, (last_name, id))
        if email is not None:
            cur.execute("""
                UPDATE client SET email=%s WHERE id=%s;
            """, (email, id))
        if phone_number is not None:
            cur.execute("""
                UPDATE client SET phone_number=%s WHERE id=%s;
            """, (phone_number, id))
            conn.commit()

def delete_phone_number(conn, id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client WHERE id=%s or phone_number=%s;
        """, (id, phone_number))
        conn.commit()
#
def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client WHERE id=%s;
        """, (id,))
        conn.commit()
#
def find_client(conn, name, last_name, email, phone_number):
    with conn.cursor() as cur:
        if name is not None:
            cur.execute("""
                SELECT * FROM client WHERE name=%s;
            """, (name,))
            print(cur.fetchone())
        if last_name is not None:
            cur.execute("""
                SELECT * FROM client WHERE last_name=%s;
            """, (last_name,))
            print(cur.fetchone())
        if email is not None:
            cur.execute("""
                SELECT * FROM client WHERE email=%s;
            """, (email,))
            print(cur.fetchone())
        if phone_number is not None:
            cur.execute("""
                SELECT * FROM client WHERE phone_number=%s;
            """, (phone_number,))
            print(cur.fetchone())
#
with psycopg2.connect(database='clients', user='postgres', password='pass') as conn:
    create_db(conn)
    add_clint(conn, 1, 'Mark ', 'Zuckerberg', 'MarkZucker@gmail.com', '+15556667777')
    add_clint(conn, 2, 'Mark ', 'Zuckerberg', 'MarkZucker@gmail.com', '+15556667777')
    add_phone_number(conn, 1,'+15554447876')
    change_client(conn, 2, 'Elon', 'Musk', 'ElonMusk@gmail.com', '+19999999999')
    delete_phone_number(conn, 1, '+15556667777')
    delete_client(conn,2)
    find_client(conn, 'Mark')

conn.close()


import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE phone;
            DROP TABLE client;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                name VARCHAR(20) not null,
                last_name VARCHAR(20) not null ,
                email VARCHAR(40) not null);
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
            phone_id SERIAL PRIMARY KEY,
            phone_number VARCHAR(50) not null,
            client_id INTEGER NOT NULL REFERENCES client(id));
        """)
        conn.commit()

def add_clint(conn, id, name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(id, name, last_name, email) VALUES(%s, %s, %s, %s);
        """, (id, name, last_name, email))
        conn.commit()

def add_phone_number(conn, phone_id, phone_number, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(phone_id, phone_number, client_id) VALUES(%s, %s, %s);
        """, (phone_id, phone_number, client_id))
        conn.commit()

def change_client(conn, id, name=None, last_name=None, email=None):
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
            conn.commit()

def delete_phone_number(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE client_id=%s or phone_number=%s;
        """, (client_id, phone_number))
        conn.commit()

def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client WHERE id=%s;
        """, (id,))
        conn.commit()

def find_client(conn, name='%', last_name='%', email='%'):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM client WHERE name LIKE %s;
        """, (name,))
        print(cur.fetchone())
        cur.execute("""
            SELECT * FROM client WHERE last_name LIKE %s;
        """, (last_name,))
        print(cur.fetchone())
        cur.execute("""
            SELECT * FROM client WHERE email LIKE %s;
        """, (email,))
        print(cur.fetchone())

if __name__ == '__main__':
    with psycopg2.connect(database='clients', user='postgres', password='pass') as conn:
        create_db(conn)
        add_clint(conn, 1, 'Mark', 'Zuckerberg', 'MarkZucker@gmail.com')
        add_clint(conn, 2, '4 ', '5', '6')
        add_phone_number(conn, 1,'+15554447876', 1)
        change_client(conn, 2, 'Elon', 'Musk', 'ElonMusk@gmail.com')
        add_phone_number(conn, 2, '+15556667777', 2)
        # delete_phone_number(conn, 1, '+15554447876')
        # delete_client(conn,2)
        find_client(conn, 'Mark', 'Musk', 'MarkZucker@gmail.com')
conn.close()







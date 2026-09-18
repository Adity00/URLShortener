from database.connection import pool
from psycopg.errors import UniqueViolation

def create_url(short_code, url, user_id, expires_at=None):
    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO urls (shortcode, url, expires_at, user_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (short_code, url, expires_at, user_id)
                )

        return True

    except UniqueViolation:
        print("Collison:",short_code)
        return False

def get_url_stats(shortcode, user_id):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT  url, clicks, expires_at
                FROM urls
                WHERE shortcode = %s
                AND user_id = %s
                """,
                (shortcode, user_id)
            )
            row = cursor.fetchone()
    if row is None:
        return None

    return{
        'url': row[0],
        'clicks': row[1],
        'expires_at':row[2]
    }     

def get_url_and_increment_clicks(shortcode):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE urls
                SET clicks = clicks + 1
                WHERE shortcode = %s
                AND (
                        expires_at is NULL 
                        OR
                        expires_at > CURRENT_TIMESTAMP    
                    )
                RETURNING url, expires_at   
                """,
                (shortcode,)
            )

            row = cursor.fetchone()

            if row is not None:
                return {
                    'status':'success',
                    'url':row[0],
                    'expires_at':row[1]
                }
            
            cursor.execute(
                """
                SELECT expires_at
                FROM urls
                WHERE shortcode = %s
                """,
                (shortcode,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                'status':'expired'
            }

def create_user(email, password_hash):
    try:    
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users(email, password_hash)
                    VALUES(%s,%s)
                    """,
                    (email, password_hash)
                )

        return True
            
    except UniqueViolation:
        return False

def get_user_by_email(email):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                'id':row[0],
                'email':row[1],
                'password_hash':row[2]
            }
            
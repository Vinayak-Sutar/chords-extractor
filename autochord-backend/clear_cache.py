"""
Clear the chord cache in PostgreSQL database.
"""

from database import init_connection_pool, get_connection, return_connection


def clear_cache():
    """Clear all cached chords from the database."""
    print("🗑️  Clearing chord cache...")

    if not init_connection_pool():
        print("❌ Could not connect to database")
        return False

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Delete all rows
        cursor.execute("DELETE FROM chord_cache")
        count = cursor.rowcount

        conn.commit()
        print(f"✅ Cleared {count} cached songs")
        return True

    except Exception as e:
        print(f"❌ Error clearing cache: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            return_connection(conn)


if __name__ == "__main__":
    clear_cache()

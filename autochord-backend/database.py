"""
Database module for chord caching system.

This module handles all PostgreSQL database operations including:
- Connection management
- CRUD operations for chord cache
- Database initialization
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'chords_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Connection pool - maintains multiple database connections for efficiency
connection_pool = None


def init_connection_pool():
    """
    Initialize the PostgreSQL connection pool.

    Connection pooling allows reusing database connections instead of
    creating new ones for each request, which is much more efficient.
    """
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,  # Minimum number of connections
            10,  # Maximum number of connections
            **DB_CONFIG
        )
        print("✅ Database connection pool created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating connection pool: {e}")
        return False


def get_connection():
    """Get a connection from the pool."""
    return connection_pool.getconn()


def return_connection(conn):
    """Return a connection to the pool."""
    connection_pool.putconn(conn)


def init_database():
    """
    Initialize the database schema.

    Creates the chord_cache table if it doesn't exist.
    This table stores:
    - youtube_id: Unique identifier from YouTube URL (PRIMARY KEY)
    - youtube_url: Full YouTube URL
    - title: Song title from YouTube
    - duration: Song length in seconds
    - beat_length: Duration of each beat in seconds
    - bpm: Beats per minute (tempo)
    - key: Musical key of the song (e.g., "C Major", "A Minor")
    - chords: JSON array of chord data [timestamp, timestamp, chord_name]
    - created_at: When the song was first processed
    - last_accessed: Last time this song was requested
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create table with proper schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chord_cache (
                youtube_id TEXT PRIMARY KEY,
                youtube_url TEXT NOT NULL,
                title TEXT,
                duration INTEGER,
                beat_length REAL NOT NULL,
                bpm REAL NOT NULL,
                key TEXT,
                chords JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create index on last_accessed for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_last_accessed 
            ON chord_cache(last_accessed DESC);
        """)

        conn.commit()
        print("✅ Database schema initialized successfully")
        return True

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            return_connection(conn)


def extract_youtube_id(url):
    """
    Extract YouTube video ID from URL.

    Examples:
    - https://www.youtube.com/watch?v=dQw4w9WgXcQ -> dQw4w9WgXcQ
    - https://youtu.be/dQw4w9WgXcQ -> dQw4w9WgXcQ
    """
    if 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    elif 'youtube.com/watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    return None


def get_cached_chords(youtube_url):
    """
    Retrieve cached chords for a YouTube URL.

    Returns:
    - dict: Chord data if found in cache
    - None: If not in cache

    Also updates the last_accessed timestamp to track popular songs.
    """
    youtube_id = extract_youtube_id(youtube_url)
    if not youtube_id:
        return None

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Fetch cached data
        cursor.execute("""
            SELECT * FROM chord_cache 
            WHERE youtube_id = %s
        """, (youtube_id,))

        result = cursor.fetchone()

        if result:
            # Update last_accessed timestamp
            cursor.execute("""
                UPDATE chord_cache 
                SET last_accessed = CURRENT_TIMESTAMP 
                WHERE youtube_id = %s
            """, (youtube_id,))
            conn.commit()

            print(f"✅ Cache HIT for {youtube_id}")
            return dict(result)

        print(f"⚠️  Cache MISS for {youtube_id}")
        return None

    except Exception as e:
        print(f"❌ Error fetching cached chords: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            return_connection(conn)


def save_chords_to_cache(youtube_url, title, duration, beat_length, bpm, key, chords):
    """
    Save extracted chords to the database cache.

    Parameters:
    - youtube_url: Full YouTube URL
    - title: Song title
    - duration: Song length in seconds
    - beat_length: Duration of each beat
    - bpm: Beats per minute
    - key: Musical key (e.g., "C Major")
    - chords: List of chord tuples [(start, end, chord_name), ...]

    Returns:
    - bool: True if saved successfully, False otherwise
    """
    youtube_id = extract_youtube_id(youtube_url)
    if not youtube_id:
        return False

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Convert chords list to JSON
        chords_json = json.dumps(chords)

        # Insert or update (upsert)
        cursor.execute("""
            INSERT INTO chord_cache 
            (youtube_id, youtube_url, title, duration, beat_length, bpm, key, chords)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (youtube_id) 
            DO UPDATE SET 
                title = EXCLUDED.title,
                duration = EXCLUDED.duration,
                beat_length = EXCLUDED.beat_length,
                bpm = EXCLUDED.bpm,
                key = EXCLUDED.key,
                chords = EXCLUDED.chords,
                last_accessed = CURRENT_TIMESTAMP
        """, (youtube_id, youtube_url, title, duration, beat_length, bpm, key, chords_json))

        conn.commit()
        print(f"✅ Chords cached for {youtube_id}")
        return True

    except Exception as e:
        print(f"❌ Error saving chords to cache: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            return_connection(conn)


def check_multiple_cached(youtube_ids):
    """
    Check cache status for multiple YouTube videos at once.

    Args:
        youtube_ids: List of YouTube video IDs

    Returns:
        dict: Mapping of youtube_id -> True/False for cache status
    """
    conn = None
    try:
        if not youtube_ids:
            return {}

        conn = get_connection()
        cursor = conn.cursor()

        # Use IN query for efficient batch lookup
        placeholders = ','.join(['%s'] * len(youtube_ids))
        query = f"SELECT youtube_id FROM chord_cache WHERE youtube_id IN ({placeholders})"
        cursor.execute(query, tuple(youtube_ids))

        # Get all cached IDs
        cached_ids = set(row[0] for row in cursor.fetchall())

        # Create result mapping
        result = {vid: (vid in cached_ids) for vid in youtube_ids}

        return result

    except Exception as e:
        print(f"❌ Error checking multiple cached videos: {e}")
        return {vid: False for vid in youtube_ids}
    finally:
        if conn:
            cursor.close()
            return_connection(conn)


def get_cache_stats():
    """
    Get statistics about the chord cache.

    Returns:
    - dict: Statistics including total songs, most popular songs, etc.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM chord_cache")
        total = cursor.fetchone()['total']

        # Get most accessed songs
        cursor.execute("""
            SELECT youtube_id, title, youtube_url, last_accessed
            FROM chord_cache
            ORDER BY last_accessed DESC
            LIMIT 10
        """)
        popular_songs = cursor.fetchall()

        return {
            'total_cached_songs': total,
            'popular_songs': [dict(song) for song in popular_songs]
        }

    except Exception as e:
        print(f"❌ Error getting cache stats: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            return_connection(conn)

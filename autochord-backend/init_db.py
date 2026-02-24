"""
Database initialization script.

This script:
1. Tests the database connection
2. Creates the chord_cache table
3. Shows cache statistics

Run this after setting up your .env file with the correct password.
"""

from database import init_connection_pool, init_database, get_cache_stats


def main():
    print("=" * 60)
    print("🎵 Chord Extractor - Database Initialization")
    print("=" * 60)

    # Step 1: Initialize connection pool
    print("\n1️⃣  Testing database connection...")
    if not init_connection_pool():
        print("\n❌ Failed to connect to database!")
        print("\nPlease check:")
        print("  • PostgreSQL is running: sudo systemctl status postgresql")
        print("  • Database exists: sudo -u postgres psql -c '\\l'")
        print("  • .env file has correct password")
        return False

    # Step 2: Create tables
    print("\n2️⃣  Creating database schema...")
    if not init_database():
        print("\n❌ Failed to create database schema!")
        return False

    # Step 3: Show stats
    print("\n3️⃣  Checking cache statistics...")
    stats = get_cache_stats()
    if stats:
        print(f"\n📊 Cache Stats:")
        print(f"   Total cached songs: {stats['total_cached_songs']}")
        if stats['popular_songs']:
            print(f"\n   Most recent songs:")
            for i, song in enumerate(stats['popular_songs'][:5], 1):
                print(f"   {i}. {song['title'] or 'Unknown'}")

    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print("\nYou can now start the Flask server with:")
    print("  source venv/bin/activate && python app.py")

    return True


if __name__ == "__main__":
    main()

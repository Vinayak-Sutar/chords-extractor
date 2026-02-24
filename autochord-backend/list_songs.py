#!/usr/bin/env python3
"""List all cached songs from the database"""

from database import init_connection_pool, get_connection, return_connection

# Initialize connection pool
init_connection_pool()

# Get connection and query
conn = get_connection()
cursor = conn.cursor()

cursor.execute('''
    SELECT youtube_id, key, title, created_at 
    FROM chord_cache 
    ORDER BY created_at DESC;
''')

songs = cursor.fetchall()
cursor.close()
return_connection(conn)

# Display results
print(f'\n📊 Total cached songs: {len(songs)}\n')
print('=' * 80)
print(f'{"#":<4} {"YouTube ID":<15} {"Key":<5} {"Title":<40} {"Cached At"}')
print('=' * 80)

for i, (youtube_id, key, title, created_at) in enumerate(songs, 1):
    title_short = (
        title[:37] + '...') if title and len(title) > 40 else (title or 'N/A')
    cached_str = created_at.strftime('%Y-%m-%d %H:%M') if created_at else 'N/A'
    print(f'{i:<4} {youtube_id:<15} {key:<5} {title_short:<40} {cached_str}')

print('=' * 80)

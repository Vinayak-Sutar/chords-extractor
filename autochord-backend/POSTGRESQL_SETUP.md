# PostgreSQL Setup Guide

## 📚 What is PostgreSQL?

PostgreSQL (often called "Postgres") is a powerful, open-source relational database. We're using it to **cache chord extraction results** so we don't have to re-process the same songs multiple times.

### Why caching?

Extracting chords from a YouTube video takes time:

1. Download audio (~10-30 seconds)
2. Analyze with librosa and autochord (~20-60 seconds)
3. Detect musical key (~5 seconds)

With caching, **second request for same song = instant response!** ⚡

---

## 🔧 Setup Steps

### Step 1: Set PostgreSQL Password

We need to set a password for the `postgres` user:

```bash
# Set password (for local dev, 'postgres' is fine)
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

### Step 2: Update .env File

Edit `/home/vinayak/FILES/code/chords-project/autochord-backend/.env`:

```bash
cd /home/vinayak/FILES/code/chords-project/autochord-backend
nano .env
```

Change this line:

```
DB_PASSWORD=your_postgres_password_here
```

To:

```
DB_PASSWORD=postgres
```

(Or whatever password you set in Step 1)

Save with `Ctrl+O`, exit with `Ctrl+X`.

### Step 3: Initialize Database

Run the initialization script:

```bash
cd /home/vinayak/FILES/code/chords-project/autochord-backend
source venv/bin/activate
python init_db.py
```

This will:

- Test database connection
- Create the `chord_cache` table
- Show cache statistics

---

## 🗄️ Database Schema

Our `chord_cache` table stores:

| Column          | Type               | Description                                       |
| --------------- | ------------------ | ------------------------------------------------- |
| `youtube_id`    | TEXT (PRIMARY KEY) | Video ID from URL (e.g., "dQw4w9WgXcQ")           |
| `youtube_url`   | TEXT               | Full YouTube URL                                  |
| `title`         | TEXT               | Song title from YouTube                           |
| `duration`      | INTEGER            | Song length in seconds                            |
| `beat_length`   | REAL               | Duration of each beat in seconds                  |
| `bpm`           | REAL               | Tempo (beats per minute)                          |
| `key`           | TEXT               | Musical key (e.g., "C Major", "A Minor")          |
| `chords`        | JSONB              | Array of chord data: `[[start, end, chord], ...]` |
| `created_at`    | TIMESTAMP          | When first extracted                              |
| `last_accessed` | TIMESTAMP          | Last time requested                               |

**Why JSONB?** PostgreSQL's JSONB type is efficient for storing JSON data and allows querying inside the JSON structure.

---

## 🔄 How Caching Works

### First Request (Cache MISS):

```
User requests song → Check DB → Not found → Extract chords → Save to DB → Return result
                        ↓
                   [2-3 minutes]
```

### Second Request (Cache HIT):

```
User requests song → Check DB → Found! → Return from DB
                        ↓
                   [<1 second] ⚡
```

---

## 🎼 Key Detection

We use **music21** library to detect the musical key:

### How it works:

1. **Parse chords**: Convert chord names (like "Cmaj7") into actual notes
2. **Analyze notes**: Count frequency of each note (C, D, E, etc.)
3. **Algorithm**: Use Krumhansl-Schmuckler algorithm to find best key

### Example:

```
Chords: C, Am, F, G
Notes: C, E, G, A, C, F, G, B
Analysis: Lots of C, E, G → Probably C Major!
Result: "C Major"
```

---

## 🚀 Starting the Server

Once setup is complete:

```bash
cd /home/vinayak/FILES/code/chords-project/autochord-backend
source venv/bin/activate
python app.py
```

You'll see:

```
============================================================
🎸 Starting Chord Extractor Backend...
============================================================

📊 Initializing database connection...
✅ Database connected!
✅ Database schema initialized successfully
   Cached songs: 0

📡 Server running on http://127.0.0.1:5000
✅ CORS enabled for frontend
============================================================
```

---

## 🔍 Testing

### Test database initialization:

```bash
python init_db.py
```

### Test API endpoints:

**Health check:**

```bash
curl http://localhost:5000/health
```

**Cache stats:**

```bash
curl http://localhost:5000/cache/stats
```

---

## 🐛 Troubleshooting

### "Connection refused"

- PostgreSQL not running: `sudo systemctl start postgresql`
- Check status: `sudo systemctl status postgresql`

### "Authentication failed"

- Wrong password in `.env` file
- Password not set: Run Step 1 again

### "Database does not exist"

- Run: `sudo -u postgres psql -c "CREATE DATABASE chords_db;"`

### "music21 warnings about numpy"

- Expected! music21 wants newer numpy, but TensorFlow needs 1.23.5
- Key detection still works, just ignore warnings

---

## 📊 Viewing Database

Connect to PostgreSQL:

```bash
sudo -u postgres psql -d chords_db
```

Useful commands:

```sql
-- List all tables
\dt

-- View all cached songs
SELECT youtube_id, title, key, bpm, last_accessed FROM chord_cache;

-- Count cached songs
SELECT COUNT(*) FROM chord_cache;

-- Most popular songs
SELECT title, last_accessed FROM chord_cache ORDER BY last_accessed DESC LIMIT 5;

-- Exit
\q
```

---

## 🎯 Next Steps

After setup:

1. Update frontend to display the `key` field
2. Show BPM in the UI
3. Add a "cached" indicator
4. Maybe add a cache management page

Happy coding! 🎵

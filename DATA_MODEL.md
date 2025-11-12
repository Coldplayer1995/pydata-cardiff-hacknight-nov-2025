┌─────────────────────────┐
│   CHARACTERS            │
│─────────────────────────│
│ id (PK)                 │
│ name                    │
│ normalized_name         │
│ gender                  │
└─────────────────────────┘
         ▲
         │
         │ character_id (FK)
         │
┌─────────────────────────┐
│   SCRIPT_LINES          │◄─── CENTRAL HUB TABLE
│─────────────────────────│
│ id (PK)                 │
│ episode_id (FK) ────────┼──┐
│ character_id (FK)      │  │
│ location_id (FK) ───────┼──┼──┐
│ number                  │  │  │
│ raw_text                │  │  │
│ timestamp_in_ms         │  │  │
│ speaking_line (bool)    │  │  │
│ spoken_words            │  │  │
│ word_count              │  │  │
└─────────────────────────┘  │  │
         │                   │  │
         │ episode_id (FK)    │  │
         │                     │  │
┌─────────────────────────┐  │  │
│   EPISODES               │◄─┘  │
│─────────────────────────│     │
│ id (PK)                 │     │
│ title                   │     │
│ season                  │     │
│ imdb_rating             │     │
│ original_air_date       │     │
│ us_viewers_in_millions  │     │
└─────────────────────────┘     │
                                │
                                │ location_id (FK)
                                │
┌─────────────────────────┐     │
│   LOCATIONS             │◄────┘
│─────────────────────────│
│ id (PK)                 │
│ name                    │
│ normalized_name         │
└─────────────────────────┘
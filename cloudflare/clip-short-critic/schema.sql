PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS critiques (
  id TEXT PRIMARY KEY,
  video_sha256 TEXT NOT NULL,
  model TEXT NOT NULL,
  provider TEXT NOT NULL,
  effort TEXT NOT NULL,
  decision TEXT NOT NULL,
  editorial_score REAL,
  request_id TEXT,
  r2_key TEXT,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_critiques_video ON critiques(video_sha256);

CREATE TABLE IF NOT EXISTS critique_findings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  critique_id TEXT NOT NULL REFERENCES critiques(id) ON DELETE CASCADE,
  timestamp_sec REAL,
  severity TEXT NOT NULL,
  category TEXT NOT NULL,
  evidence TEXT NOT NULL,
  explanation TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_findings_critique ON critique_findings(critique_id);

CREATE TABLE IF NOT EXISTS edit_trajectories (
  id TEXT PRIMARY KEY,
  video_id TEXT NOT NULL,
  query_id TEXT NOT NULL,
  action_id TEXT NOT NULL,
  features_json TEXT NOT NULL,
  label INTEGER NOT NULL CHECK(label BETWEEN 0 AND 4),
  label_provenance TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_trajectories_query ON edit_trajectories(query_id);

CREATE TABLE IF NOT EXISTS preference_labels (
  id TEXT PRIMARY KEY,
  query_id TEXT NOT NULL,
  winner_action_id TEXT NOT NULL,
  loser_action_id TEXT NOT NULL,
  reviewer_id TEXT NOT NULL,
  note TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assets (
  key TEXT PRIMARY KEY,
  sha256 TEXT NOT NULL,
  content_type TEXT,
  size INTEGER NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
  school_id TEXT PRIMARY KEY,
  full_name TEXT NOT NULL,
  class_name TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS teachers (
  telegram_id INTEGER PRIMARY KEY,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'teacher'
);
CREATE TABLE IF NOT EXISTS subjects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  school_id TEXT NOT NULL,
  subject_id INTEGER NOT NULL,
  teacher_id INTEGER NOT NULL,
  score_date TEXT NOT NULL,
  readiness INTEGER NOT NULL,
  understanding INTEGER NOT NULL,
  independent_work INTEGER NOT NULL,
  activity INTEGER NOT NULL,
  assessment INTEGER NOT NULL,
  note TEXT DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(school_id, subject_id, score_date),
  FOREIGN KEY(student_id) REFERENCES students(school_id)
);

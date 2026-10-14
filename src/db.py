"""SQLite storage for the pricing tool. Stdlib only."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "pricing.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    sku TEXT PRIMARY KEY,
    ean TEXT,
    name TEXT NOT NULL,
    own_price REAL,
    shop_url TEXT,
    image_url TEXT,
    active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS shop_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    price REAL NOT NULL,
    scraped_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_shop_prices_sku ON shop_prices(sku, scraped_at);
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL REFERENCES products(sku),
    marketplace TEXT NOT NULL,
    url TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    UNIQUE (sku, marketplace)
);
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    price REAL,
    currency TEXT DEFAULT 'EUR',
    available INTEGER,
    source TEXT,
    error TEXT,
    scraped_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_snapshots_match ON snapshots(match_id, scraped_at);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    """Add columns introduced after the first schema. Snapshots are never rewritten."""
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(products)")}
    if "shop_url" not in cols:
        conn.execute("ALTER TABLE products ADD COLUMN shop_url TEXT")
    if "image_url" not in cols:
        conn.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
    if "active" not in cols:
        conn.execute("ALTER TABLE products ADD COLUMN active INTEGER NOT NULL DEFAULT 1")
    conn.commit()


def sync_from_csv(conn: sqlite3.Connection) -> None:
    """Upsert products.csv and matches.csv into the DB (CSVs are the source of truth
    for the catalog; snapshots are only ever appended).

    Rows that leave the CSVs stay in the database with active=0 so their history
    remains, and the daily scrape stops requesting them.
    A previously scraped own_price is kept until the shop page is read again.
    """
    conn.execute("UPDATE products SET active=0")
    conn.execute("UPDATE matches SET active=0")
    with open(ROOT / "products.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row.get("sku"):
                continue
            own = float(row["own_price_eur"]) if row.get("own_price_eur") else None
            conn.execute(
                "INSERT INTO products (sku, ean, name, own_price, shop_url, image_url, active) "
                "VALUES (?,?,?,?,?,?,1) "
                "ON CONFLICT(sku) DO UPDATE SET ean=excluded.ean, name=excluded.name, "
                "own_price=COALESCE(products.own_price, excluded.own_price), "
                "shop_url=excluded.shop_url, "
                "image_url=COALESCE(excluded.image_url, products.image_url), active=1",
                (
                    row["sku"].strip(),
                    (row.get("ean") or "").strip() or None,
                    row["name"].strip(),
                    own,
                    (row.get("shop_url") or "").strip() or None,
                    (row.get("image_url") or "").strip() or None,
                ),
            )
    matches_file = ROOT / "matches.csv"
    if matches_file.exists():
        with open(matches_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("url"):
                    continue
                conn.execute(
                    "INSERT INTO matches (sku, marketplace, url, active) VALUES (?,?,?,1) "
                    "ON CONFLICT(sku, marketplace) DO UPDATE SET url=excluded.url, active=1",
                    (row["sku"].strip(), row["marketplace"].strip().lower(), row["url"].strip()),
                )
    conn.commit()


def record_shop_price(conn, sku, price, image_url=None):
    """Store the price read from the own shop page, once per calendar day."""
    conn.execute(
        "UPDATE products SET own_price=?, image_url=COALESCE(?, image_url) WHERE sku=?",
        (price, image_url, sku),
    )
    row = conn.execute(
        "SELECT id FROM shop_prices WHERE sku=? AND date(scraped_at)=date('now')",
        (sku,),
    ).fetchone()
    if row:
        conn.execute("UPDATE shop_prices SET price=? WHERE id=?", (price, row["id"]))
    else:
        conn.execute("INSERT INTO shop_prices (sku, price) VALUES (?,?)", (sku, price))
    conn.commit()


def active_matches(conn: sqlite3.Connection):
    return conn.execute(
        "SELECT m.id, m.sku, m.marketplace, m.url, p.name FROM matches m "
        "JOIN products p ON p.sku = m.sku WHERE m.active = 1 ORDER BY m.sku"
    ).fetchall()


def add_snapshot(conn, match_id, price, currency, available, source, error=None):
    conn.execute(
        "INSERT INTO snapshots (match_id, price, currency, available, source, error) "
        "VALUES (?,?,?,?,?,?)",
        (match_id, price, currency, available, source, error),
    )
    conn.commit()

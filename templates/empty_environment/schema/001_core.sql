PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    node_type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    status TEXT NOT NULL DEFAULT 'candidate',
    owner TEXT,
    confidence REAL,
    source_path TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS edges (
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    rationale TEXT,
    confidence REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_id, target_id, edge_type),
    FOREIGN KEY (source_id) REFERENCES nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS external_refs (
    id INTEGER PRIMARY KEY,
    node_id TEXT NOT NULL,
    system TEXT NOT NULL,
    ref_type TEXT NOT NULL,
    external_id TEXT NOT NULL,
    role TEXT NOT NULL,
    url TEXT,
    authority_level TEXT NOT NULL DEFAULT 'reference',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    selected_option TEXT,
    rationale TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    decided_by TEXT,
    decided_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decision_options (
    decision_id TEXT NOT NULL,
    option_key TEXT NOT NULL,
    description TEXT NOT NULL,
    pros TEXT,
    cons TEXT,
    PRIMARY KEY (decision_id, option_key),
    FOREIGN KEY (decision_id) REFERENCES decisions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activity_policies (
    id TEXT PRIMARY KEY,
    activity_id TEXT NOT NULL,
    trigger_key TEXT NOT NULL,
    trigger_value TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    rationale TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'normal',
    FOREIGN KEY (activity_id) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS run_log (
    id INTEGER PRIMARY KEY,
    run_type TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE IF NOT EXISTS nodes_fts USING fts5(
    id UNINDEXED,
    node_type UNINDEXED,
    title,
    body,
    content='nodes',
    content_rowid='rowid'
);

CREATE TRIGGER IF NOT EXISTS nodes_ai AFTER INSERT ON nodes BEGIN
    INSERT INTO nodes_fts(rowid, id, node_type, title, body)
    VALUES (new.rowid, new.id, new.node_type, new.title, new.body);
END;

CREATE TRIGGER IF NOT EXISTS nodes_ad AFTER DELETE ON nodes BEGIN
    INSERT INTO nodes_fts(nodes_fts, rowid, id, node_type, title, body)
    VALUES ('delete', old.rowid, old.id, old.node_type, old.title, old.body);
END;

CREATE TRIGGER IF NOT EXISTS nodes_au AFTER UPDATE ON nodes BEGIN
    INSERT INTO nodes_fts(nodes_fts, rowid, id, node_type, title, body)
    VALUES ('delete', old.rowid, old.id, old.node_type, old.title, old.body);
    INSERT INTO nodes_fts(rowid, id, node_type, title, body)
    VALUES (new.rowid, new.id, new.node_type, new.title, new.body);
END;

CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(node_type);
CREATE INDEX IF NOT EXISTS idx_nodes_status ON nodes(status);
CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);
CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(edge_type);
CREATE INDEX IF NOT EXISTS idx_external_refs_node ON external_refs(node_id);

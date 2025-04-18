CREATE TABLE violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_poursuite TEXT,
    business_id TEXT,
    date TEXT,
    description TEXT,
    adresse TEXT,
    date_jugement TEXT,
    etablissement TEXT,
    montant REAL,
    proprietaire TEXT,
    ville TEXT,
    statut TEXT,
    date_statut TEXT,
    categorie TEXT
);

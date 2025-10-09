#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Costruzione dell'indice dei materiali (Attuario Knowledge Base)
Analizza PDF, PPT, R-script e audio (placeholder)
e aggiorna automaticamente materials_index.csv
"""

import os
import csv
import datetime
from pathlib import Path

# === Percorso base del progetto ===
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "01_raw_materials"

# === Mapping automatico delle materie (basato sui nomi cartella) ===
MATERIE = {
    "01_modelli_matematici_mercati_finanziari": "Modelli matematici per i mercati finanziari",
    "02_rischio_finanziario_assicurativo": "Gestione del rischio finanziario e assicurativo",
    "03_modelli_analisi_economica": "Modelli matematici per l’analisi economica",
    "04_analisi_dati_spaziali": "Analisi dei dati spaziali per le applicazioni",
    "05_statistica_assicurazioni": "Statistica per le assicurazioni",
    "06_tecniche_attuariali": "Tecniche attuariali per le assicurazioni",
    "07_modelli_stocastici_derivati": "Modelli stocastici e contratti derivati",
    "08_machine_learning_finanza": "Machine Learning per la finanza",
    "09_diritto_tributario_finanziario": "Diritto tributario e delle attività finanziarie",
    "10_piani_strategici": "Simulazione di piani strategici",
}

# === Tipi di file ammessi ===
ESTENSIONI = {
    ".pdf": "lezione_pdf",
    ".ppt": "slide",
    ".pptx": "slide",
    ".r": "script_R",
    ".py": "script_Python",
    ".mp3": "audio",
    ".wav": "audio",
}

# === File CSV di output ===
INDEX_FILE = BASE_DIR / "materials_index.csv"

def scan_materials():
    """Scansiona la cartella 01_raw_materials e restituisce i metadati"""
    records = []
    for root, _, files in os.walk(RAW_DIR):
        for f in files:
            ext = Path(f).suffix.lower()
            if ext not in ESTENSIONI:
                continue
            full_path = Path(root) / f
            materia_key = Path(root).parts[-1]
            materia = MATERIE.get(materia_key, "N/A")
            tipo = ESTENSIONI.get(ext, "altro")
            record = {
                "file_name": f,
                "materia": materia,
                "tipo": tipo,
                "path": str(full_path.relative_to(BASE_DIR)),
                "dimensione_kb": round(full_path.stat().st_size / 1024, 1),
                "estratto_il": datetime.date.today().isoformat(),
            }
            records.append(record)
    return records

def save_index(records):
    """Scrive l'indice in formato CSV"""
    with open(INDEX_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["file_name", "materia", "tipo", "path", "dimensione_kb", "estratto_il"],
        )
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    data = scan_materials()
    save_index(data)
    print(f"✅ Creato indice con {len(data)} materiali in {INDEX_FILE}")

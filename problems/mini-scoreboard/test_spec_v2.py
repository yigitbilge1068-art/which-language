"""
mini-scoreboard (Enterprise Edition) SPEC QA & Test Senaryolari
Ogrenci: [Utkuhan Akar] ([251478036])
Test Kapsami: Happy Path + Edge Cases + Data Security + V1 Tests
"""
import subprocess
import os
import shutil

def run_cmd(args):
    result = subprocess.run(["python", "miniscore.py"] + args, capture_output=True, text=True)
    return result.stdout.strip()

def setup_function():
    if os.path.exists(".miniscore"):
        shutil.rmtree(".miniscore")

# --- 1. CORE SYSTEM TESTS ---
def test_init_creates_system():
    run_cmd(["init"])
    assert os.path.exists(".miniscore/matches.dat")

def test_init_already_exists():
    run_cmd(["init"])
    assert "Already initialized" in run_cmd(["init"])

# --- 2. HAPPY PATH TESTS ---
def test_add_match_success():
    run_cmd(["init"])
    output = run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "Galatasaray", "2", "Fenerbahce", "1"])
    assert "Added match #1" in output
    assert "GALATASARAY 2 - 1 FENERBAHCE on 2026-03-16" in output

# --- 3. DEFENSIVE PROGRAMMING TESTS ---
def test_security_prevent_delimiter_injection():
    run_cmd(["init"])
    output = run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "Galatasaray|A", "2", "FB", "1"])
    assert "Error: The '|' character is reserved" in output

def test_validation_prevent_invalid_score_type():
    run_cmd(["init"])
    output = run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "GS", "iki", "FB", "1"])
    assert "Error: Scores must be positive numbers" in output

def test_validation_prevent_ghost_teams():
    run_cmd(["init"])
    output = run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "   ", "2", "FB", "1"])
    assert "Error: Team names cannot be empty" in output

def test_validation_prevent_clone_match():
    run_cmd(["init"])
    output = run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "GS", "2", "GS", "1"])
    assert "Error: A team cannot play against itself" in output

# --- 4. V1 IMPLEMENTATION TESTS (Artik PASSED olacaklar!) ---
def test_history_empty_and_filled():
    run_cmd(["init"])
    assert "History is empty." in run_cmd(["history"])
    run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "GS", "2", "FB", "1"])
    assert "MATCH HISTORY" in run_cmd(["history"])
    assert "GS 2 - 1 FB" in run_cmd(["history"])

def test_team_filter():
    run_cmd(["init"])
    run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "GS", "2", "FB", "1"])
    run_cmd(["add-match", "SuperLig", "W2", "2026-03-23", "BJK", "3", "TS", "0"])
    
    output_gs = run_cmd(["team", "GS"])
    assert "MATCHES FOR GS" in output_gs
    assert "FB" in output_gs
    assert "BJK" not in output_gs

def test_stats_bonus():
    run_cmd(["init"])
    assert "No stats available" in run_cmd(["stats"])
    run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "GS", "2", "FB", "1"]) # 3 Gol
    run_cmd(["add-match", "SuperLig", "W2", "2026-03-23", "BJK", "3", "TS", "0"]) # 3 Gol
    output = run_cmd(["stats"])
    assert "Total Matches: 2" in output
    assert "Total Goals Scored: 6" in output

# --- 5. FUTURE TDD TESTS (V2/V3 icin Kirmizi kalacak) ---
def test_standings_future_logic():
    run_cmd(["init"])
    assert "will be implemented" in run_cmd(["standings"])
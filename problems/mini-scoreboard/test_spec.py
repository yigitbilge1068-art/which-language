"""
mini-scoreboard (Enterprise Edition) SPEC QA & Test Senaryolari
Ogrenci: [Utkuhan Akar] ([251478036])
Test Kapsami: Happy Path + Edge Cases + Data Security + TDD Future Tests
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

def test_validation_strict_date_format():
    run_cmd(["init"])
    output = run_cmd(["add-match", "SuperLig", "W1", "Bahar2026", "GS", "2", "FB", "1"])
    assert "Error: Date must be strictly in YYYY-MM-DD format" in output

def test_validation_max_length_limit():
    run_cmd(["init"])
    long_team = "A" * 35
    output = run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", long_team, "2", "FB", "1"])
    assert "Error: Inputs cannot exceed 30 characters" in output

def test_security_missing_file_after_init():
    run_cmd(["init"])
    os.remove(".miniscore/matches.dat")
    output = run_cmd(["add-match", "SuperLig", "W1", "2026-03-16", "GS", "2", "FB", "1"])
    assert "Not initialized or files missing" in output

def test_unknown_command():
    run_cmd(["init"])
    assert "Unknown command" in run_cmd(["hack_system"])

# --- 4. FUTURE IMPLEMENTATION TESTS (TDD) ---
# DİKKAT: Bu testler V0 aşamasında bilerek başarısız (FAILED) olacaktır.
# Gerçek kodlar yazıldığında testler geçecektir.

def test_standings_future_logic():
    run_cmd(["init"])
    assert "No matches played yet" in run_cmd(["standings"]) 

def test_history_future_logic():
    run_cmd(["init"])
    assert "History is empty" in run_cmd(["history", "SuperLig"])

def test_stats_future_logic():
    run_cmd(["init"])
    assert "No stats available" in run_cmd(["stats"])
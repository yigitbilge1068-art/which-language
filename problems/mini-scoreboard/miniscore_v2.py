"""
mini-scoreboard V1 — Enterprise Architecture Edition
Ogrenci: [Utkuhan Akar] ([251478036])

--- V1 GOREV LİSTESİ (TASK LIST) ---
[x] Task 1: ID uretimindeki teknik borcu kapat (while dongusu ile guvenli ID bul).
[x] Task 2: 'history' komutunu while dongusu kullanarak implemente et.
[x] Task 3: 'team' komutunu while dongusu ve filtreleme ile implemente et.
[x] Bonus Task: AI Codex kullanarak 'stats' komutunu implemente et.
------------------------------------
"""
import sys
import os

# --- SABITLER (CONSTANTS) ---
DIR_NAME = ".miniscore"
DB_FILE = ".miniscore/matches.dat"
DELIMITER = "|"

CMD_INDEX = 1
MIN_ARGS_PROGRAM = 2
MIN_ARGS_ADD_MATCH = 9
MAX_STRING_LENGTH = 30

def is_initialized():
    return os.path.exists(DIR_NAME) and os.path.exists(DB_FILE)

def get_not_implemented_msg(cmd_name):
    return "Command '" + cmd_name + "' will be implemented in future weeks."

def execute_init():
    if is_initialized(): return "Already initialized"
    if not os.path.exists(DIR_NAME): os.mkdir(DIR_NAME)
    file = open(DB_FILE, "w", encoding="utf-8")
    file.close()
    return "Initialized empty miniscore in " + DIR_NAME + "/"

def execute_add_match(league, week, date, team_a, score_a, team_b, score_b):
    if not is_initialized(): return "Not initialized or files missing. Run: python miniscore.py init"
    
    # Validation Rules
    if len(league) > MAX_STRING_LENGTH or len(week) > MAX_STRING_LENGTH or len(team_a) > MAX_STRING_LENGTH or len(team_b) > MAX_STRING_LENGTH: return "Error: Inputs cannot exceed 30 characters."
    if DELIMITER in league or DELIMITER in week or DELIMITER in date or DELIMITER in team_a or DELIMITER in team_b: return "Error: The '|' character is reserved."
    if not score_a.isdigit() or not score_b.isdigit(): return "Error: Scores must be positive numbers."
    team_a, team_b = team_a.strip().upper().replace("\n", ""), team_b.strip().upper().replace("\n", "")
    league, week = league.strip().replace("\n", ""), week.strip().replace("\n", "")
    if team_a == "" or team_b == "": return "Error: Team names cannot be empty or just spaces."
    if team_a == team_b: return "Error: A team cannot play against itself."
    if len(date) != 10 or date[4] != "-" or date[7] != "-": return "Error: Date must be strictly in YYYY-MM-DD format."
    if not date[:4].isdigit() or not date[5:7].isdigit() or not date[8:].isdigit(): return "Error: Date must contain valid numbers."

    # V1 TASK 1: WHILE DONGUSU ILE GUYENLI ID URETIMI
    new_id = 1
    read_file = open(DB_FILE, "r", encoding="utf-8")
    line = read_file.readline()
    while line:
        if line.strip(): # Bos satirlari atla (Fragile ID sorununu cozduk!)
            parts = line.strip().split(DELIMITER)
            if parts[0].isdigit():
                new_id = int(parts[0]) + 1
        line = read_file.readline()
    read_file.close()
    
    write_file = open(DB_FILE, "a", encoding="utf-8")
    line_to_write = str(new_id) + "|" + league + "|" + week + "|" + date + "|" + team_a + "|" + score_a + "|" + team_b + "|" + score_b + "\n"
    write_file.write(line_to_write)
    write_file.close()
    
    return "Added match #" + str(new_id) + ": [" + league + " - " + week + "] " + team_a + " " + score_a + " - " + score_b + " " + team_b + " on " + date

# V1 TASK 2: HISTORY KOMUTU
def execute_history():
    if not is_initialized(): return "Not initialized."
    file = open(DB_FILE, "r", encoding="utf-8")
    line = file.readline()
    
    result = "--- MATCH HISTORY ---\n"
    has_matches = False
    while line:
        if line.strip():
            parts = line.strip().split(DELIMITER)
            result += "[" + parts[0] + "] " + parts[2] + " " + parts[4] + " " + parts[5] + " - " + parts[7] + " " + parts[6] + " (" + parts[3] + ")\n"
            has_matches = True
        line = file.readline()
    file.close()
    
    if not has_matches: return "History is empty."
    return result.strip()

# V1 TASK 3: TEAM KOMUTU (Filtreleme)
def execute_team(target_team):
    if not is_initialized(): return "Not initialized."
    target_team = target_team.strip().upper()
    file = open(DB_FILE, "r", encoding="utf-8")
    line = file.readline()
    
    result = "--- MATCHES FOR " + target_team + " ---\n"
    found = False
    while line:
        if line.strip():
            parts = line.strip().split(DELIMITER)
            if parts[4] == target_team or parts[6] == target_team:
                result += "[" + parts[1] + " - " + parts[2] + "] " + parts[4] + " " + parts[5] + " - " + parts[7] + " " + parts[6] + " (" + parts[3] + ")\n"
                found = True
        line = file.readline()
    file.close()
    
    if not found: return "No matches found for " + target_team + "."
    return result.strip()

# BONUS TASK: STATS KOMUTU
def execute_stats():
    if not is_initialized(): return "Not initialized."
    file = open(DB_FILE, "r", encoding="utf-8")
    line = file.readline()
    
    total_matches = 0
    total_goals = 0
    
    while line:
        if line.strip():
            parts = line.strip().split(DELIMITER)
            total_matches += 1
            total_goals += int(parts[5]) + int(parts[7])
        line = file.readline()
    file.close()
    
    if total_matches == 0: return "No stats available."
    return "Total Matches: " + str(total_matches) + " | Total Goals Scored: " + str(total_goals)

# --- ROUTER ---
if len(sys.argv) < MIN_ARGS_PROGRAM:
    print("Usage: python miniscore.py <command> [args]")
else:
    command = sys.argv[CMD_INDEX].lower()
    
    if command == "init":
        print(execute_init())
    elif command == "add-match":
        if len(sys.argv) != MIN_ARGS_ADD_MATCH:
            print("Usage: python miniscore.py add-match <League> <Week> <Date> <TeamA> <ScoreA> <TeamB> <ScoreB>")
        else:
            print(execute_add_match(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]))
    elif command == "history":
        print(execute_history())
    elif command == "team":
        if len(sys.argv) < 3:
            print("Usage: python miniscore.py team <TeamName>")
        else:
            print(execute_team(sys.argv[2]))
    elif command == "stats":
        print(execute_stats())
    elif command == "standings" or command == "h2h" or command == "delete-match" or command == "edit-match" or command == "reset":
        print(get_not_implemented_msg(command))
    else:
        print("Unknown command: " + command)
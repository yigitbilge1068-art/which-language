"""
mini-scoreboard v0 — Enterprise Architecture Edition
Ogrenci: [Utkuhan Akar] ([251478036])

Mimari Kararlar (Architectural Decisions):
  - KISITLAMALARA UYULDU: Dongu (for/while) ve Liste ([]) KULLANILMADI.
  - DEFENSIVE PROGRAMMING: Delimiter Injection, Max Length, Ghost Teams, Clone Teams ve Newline Zehirlenmesi engellendi.
  - DRY & No Magic Numbers uygulandi. UTF-8 standardi getirildi.
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

# --- YARDIMCI FONKSIYONLAR (DRY) ---
def is_initialized():
    """Sistemin hem klasor hem de dosya bazinda saglam olup olmadigini dogrular."""
    return os.path.exists(DIR_NAME) and os.path.exists(DB_FILE)

def get_not_implemented_msg(cmd_name):
    return "Command '" + cmd_name + "' will be implemented in future weeks."

# --- ANA KOMUTLAR ---
def execute_init():
    if is_initialized():
        return "Already initialized"
    
    if not os.path.exists(DIR_NAME):
        os.mkdir(DIR_NAME)
        
    file = open(DB_FILE, "w", encoding="utf-8")
    file.close()
    return "Initialized empty miniscore in " + DIR_NAME + "/"

def execute_add_match(league, week, date, team_a, score_a, team_b, score_b):
    if not is_initialized():
        return "Not initialized or files missing. Run: python miniscore.py init"
    
    # 1. SAVUNMA: UZUNLUK KONTROLU
    if len(league) > MAX_STRING_LENGTH or len(week) > MAX_STRING_LENGTH or len(team_a) > MAX_STRING_LENGTH or len(team_b) > MAX_STRING_LENGTH:
        return "Error: Inputs cannot exceed 30 characters."
    
    # 2. SAVUNMA: DELIMITER INJECTION KORUMASI
    if DELIMITER in league or DELIMITER in week or DELIMITER in date or DELIMITER in team_a or DELIMITER in team_b:
        return "Error: The '|' character is reserved and cannot be used in inputs."
    
    # 3. SAVUNMA: VERI TIPI DOGRULAMASI
    if not score_a.isdigit() or not score_b.isdigit():
        return "Error: Scores must be positive numbers."
        
    # 4. SAVUNMA: BOSLUK VE SATIR SONU (NEWLINE) TEMIZLIGI
    team_a = team_a.strip().upper().replace("\n", "").replace("\r", "")
    team_b = team_b.strip().upper().replace("\n", "").replace("\r", "")
    league = league.strip().replace("\n", "").replace("\r", "")
    week = week.strip().replace("\n", "").replace("\r", "")
    
    # 5. SAVUNMA: HAYALET TAKIM KORUMASI
    if team_a == "" or team_b == "":
        return "Error: Team names cannot be empty or just spaces."
        
    # 6. SAVUNMA: KLON MAC KORUMASI
    if team_a == team_b:
        return "Error: A team cannot play against itself."
        
    # 7. SAVUNMA: KUSURSUZ TARIH FORMATI KONTROLU (YYYY-MM-DD)
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        return "Error: Date must be strictly in YYYY-MM-DD format."
    if not date[:4].isdigit() or not date[5:7].isdigit() or not date[8:].isdigit():
        return "Error: Date must contain valid numbers (e.g., 2026-03-16)."

    # --- DOSYAYA YAZMA ISLEMI (UTF-8) ---
    read_file = open(DB_FILE, "r", encoding="utf-8")
    content = read_file.read()
    read_file.close()
    
    new_id = content.count("\n") + 1
    
    write_file = open(DB_FILE, "a", encoding="utf-8")
    line = str(new_id) + "|" + league + "|" + week + "|" + date + "|" + team_a + "|" + score_a + "|" + team_b + "|" + score_b + "\n"
    write_file.write(line)
    write_file.close()
    
    return "Added match #" + str(new_id) + ": [" + league + " - " + week + "] " + team_a + " " + score_a + " - " + score_b + " " + team_b + " on " + date

# --- ROUTER (YONLENDIRICI) ---
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
            
    elif command == "standings" or command == "history" or command == "team" or command == "h2h" or command == "stats" or command == "delete-match" or command == "edit-match" or command == "reset":
        print(get_not_implemented_msg(command))
        
    else:
        print("Unknown command: " + command)
import sys
import os
from datetime import datetime

# ==========================================
# V2 GÖREVLERİ (TASKS):
# 1. 'add' komutunda kayıtlara otomatik tarih/saat damgası eklemek.
# 2. 'total/summary' komutu ile liste kullanmadan toplam bakiyeyi hesaplamak.
# 3. Dosya yokken list/total komutlarında çökmeyi önleyen Hata Yönetimi.
# ==========================================

FILE_PATH = ".minibudget/ledger.dat"

def ensure_dir():
    if not os.path.exists(".minibudget"):
        os.makedirs(".minibudget")

def add_transaction(txn_type, amount, desc):
    ensure_dir()
    
    # ID hesaplama (Liste yasak olduğu için while ile satır sayıyoruz)
    txn_id = 1
    if os.path.exists(FILE_PATH):
        f_in = open(FILE_PATH, "r")
        line = f_in.readline()
        while line:
            txn_id += 1
            line = f_in.readline()
        f_in.close()

    # Görev 1: Otomatik Tarih Damgası
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    f = open(FILE_PATH, "a")
    # Format: id | type | amount | category | date
    f.write(str(txn_id) + "|" + txn_type + "|" + amount + "|" + desc + "|" + date_str + "\n")
    f.close()
    
    print("Added transaction #" + str(txn_id) + ": " + txn_type + " " + amount + " for " + desc)

def list_transactions():
    # Görev 3: Dosya Kontrolü (Hata Yönetimi)
    if not os.path.exists(FILE_PATH):
        print("No transactions found.")
        return
    
    f = open(FILE_PATH, "r")
    line = f.readline()
    if not line:
        print("No transactions found.")
        f.close()
        return
        
    while line:
        print(line.strip().replace("|", " - "))
        line = f.readline()
    f.close()

def show_total():
    # Görev 2 & 3: Toplam Hesaplama ve Hata Yönetimi
    if not os.path.exists(FILE_PATH):
        print("Total Income: 0.0")
        print("Total Expense: 0.0")
        print("Net Balance: 0.0")
        return
    
    f = open(FILE_PATH, "r")
    total_income = 0.0
    total_expense = 0.0
    line = f.readline()
    
    while line:
        parts = line.split("|")
        # Spec formatına göre type index 1, amount index 2'dir
        if len(parts) >= 3:
            try:
                txn_type = parts[1].strip()
                amount_val = float(parts[2].strip())
                
                if txn_type == "INCOME":
                    total_income += amount_val
                elif txn_type == "EXPENSE":
                    total_expense += amount_val
            except ValueError:
                pass 
        line = f.readline()
    f.close()
    
    net_balance = total_income - total_expense
    print("Total Income: " + str(total_income))
    print("Total Expense: " + str(total_expense))
    print("Net Balance: " + str(net_balance))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solution_v2.py [init/add/list/total/summary]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        if os.path.exists(".minibudget"):
            print("Already initialized")
        else:
            ensure_dir()
            open(FILE_PATH, "w").close()
            
    elif command == "add":
        if len(sys.argv) < 5:
            print("Usage: python solution_v2.py add <type> <amount> <category>")
        else:
            txn_type = sys.argv[2]
            if txn_type not in ["INCOME", "EXPENSE"]:
                print("Error: Type must be INCOME or EXPENSE")
            else:
                amount = sys.argv[3]
                try:
                    float(amount) # Sayısal doğrulama
                    desc = ""
                    i = 4
                    while i < len(sys.argv): # While döngüsü ile açıklama birleştirme
                        desc += sys.argv[i] + " "
                        i += 1
                    add_transaction(txn_type, amount, desc.strip())
                except ValueError:
                    print("Error: Amount must be a valid number")
                    
    elif command == "list":
        list_transactions()
        
    elif command == "total" or command == "summary":
        show_total()
        
    else:
        print("Unknown command: " + command)

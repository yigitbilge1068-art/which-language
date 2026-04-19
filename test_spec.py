"""
mini-budget SPEC test senaryolari
Ogrenci: Yiğit Bilge (251478059)
Proje: mini-budget
Versiyon: V2
"""
import subprocess
import os
import shutil
from datetime import datetime

# --- Yardimci Fonksiyon ---
def run_cmd(args):
    """Komutu calistir, stdout dondur."""
    # V2 guncellemesi: Artik solution_v2.py dosyasini test ediyor
    result = subprocess.run(
        ["python", "solution_v2.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def setup_function():
    """Her testten once temiz baslangic saglar."""
    if os.path.exists(".minibudget"):
        shutil.rmtree(".minibudget")

# --- init testleri ---
def test_init_creates_directory():
    output = run_cmd(["init"])
    assert os.path.exists(".minibudget"), ".minibudget dizini olusturulmali"
    assert os.path.exists(".minibudget/ledger.dat"), "ledger.dat dosyasi olusturulmali"

def test_init_already_exists():
    run_cmd(["init"])
    output = run_cmd(["init"])
    assert "Already initialized" in output

# --- add testleri ---
def test_add_income_success():
    run_cmd(["init"])
    output = run_cmd(["add", "INCOME", "500.0", "Harclik"])
    assert "Added transaction" in output
    assert "INCOME" in output

def test_add_expense_success():
    run_cmd(["init"])
    run_cmd(["add", "INCOME", "500.0", "Harclik"])
    output = run_cmd(["add", "EXPENSE", "120.0", "Yemek"])
    assert "Added transaction" in output
    assert "EXPENSE" in output

def test_add_invalid_type():
    run_cmd(["init"])
    output = run_cmd(["add", "MAGIC", "100.0", "Test"])
    assert "Error: Type must be INCOME or EXPENSE" in output

# --- list testleri ---
def test_list_empty():
    run_cmd(["init"])
    output = run_cmd(["list"])
    assert "No transactions found" in output

def test_list_shows_transactions():
    run_cmd(["init"])
    run_cmd(["add", "INCOME", "500.0", "Harclik"])
    output = run_cmd(["list"])
    assert "500.0" in output
    assert "Harclik" in output

# --- summary testleri ---
def test_summary_calculates_correctly():
    run_cmd(["init"])
    run_cmd(["add", "INCOME", "500.0", "Harclik"])
    run_cmd(["add", "EXPENSE", "100.0", "Fatura"])
    output = run_cmd(["summary"])
    assert "500.0" in output
    assert "100.0" in output

# --- hata testleri ---
def test_command_before_init():
    output = run_cmd(["add", "INCOME", "500.0", "Harclik"])
    assert "Not initialized" in output or "No transactions" in output

def test_unknown_command():
    run_cmd(["init"])
    output = run_cmd(["uc"])
    assert "Unknown command" in output


# ==========================================
# V2 YENI TEST SENARYOLARI
# ==========================================

def test_v2_timestamp_added_automatically():
    """Görev 1: Sistemin otomatik tarih/saat atadigini test eder."""
    run_cmd(["init"])
    run_cmd(["add", "INCOME", "500.0", "Burs"])
    output = run_cmd(["list"])
    
    current_year = str(datetime.now().year)
    assert current_year in output, "V2 Hatasi: Listelemede otomatik yil (zaman damgasi) bulunamadi."

def test_v2_total_command():
    """Görev 2: Yeni total komutunun hatasiz calistigini test eder."""
    run_cmd(["init"])
    run_cmd(["add", "INCOME", "1000.0", "Maas"])
    run_cmd(["add", "EXPENSE", "250.0", "Market"])
    
    output = run_cmd(["total"])
    assert output != "", "V2 Hatasi: Total komutu hicbir ciktı vermiyor."
    assert "Unknown command" not in output, "V2 Hatasi: Total komutu sisteme tanitilmamis."

def test_v2_safe_execution_without_file():
    """Görev 3: Dosya ve klasor yokken programin cokmedigini test eder."""
    output_list = run_cmd(["list"])
    output_total = run_cmd(["total"])
    
    # Program cokerse output bostur veya hata mesaji basar. Biz kibar bir donus bekliyoruz.
    assert "No transactions found" in output_list or "Not initialized" in output_list, "V2 Hatasi: list komutu klasor yokken coktu."
    assert "Total Balance: 0.0" in output_total or "Not initialized" in output_total or "0" in output_total, "V2 Hatasi: total komutu klasor yokken coktu."

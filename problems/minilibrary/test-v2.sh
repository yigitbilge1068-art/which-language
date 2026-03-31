#!/usr/bin/env bash
set -e

PASS_COUNT=0
FAIL_COUNT=0

fail() {
  echo "FAIL: $1"
  FAIL_COUNT=$((FAIL_COUNT+1))
}

pass() {
  echo "PASS: $1"
  PASS_COUNT=$((PASS_COUNT+1))
}

cleanup() {
  cd "$(dirname "$0")"
  rm -rf testrepo
}

# Build if needed
cd "$(dirname "$0")"

if [ -f Makefile ] || [ -f makefile ]; then
  make -s 2>/dev/null || true
fi
if [ -f build.sh ]; then
  bash build.sh 2>/dev/null || true
fi
chmod +x minilibrary 2>/dev/null || true

######################################
# Setup
######################################

cleanup
mkdir testrepo
cd testrepo

######################################
# Test 1: init creates requests.dat
######################################

if ../minilibrary init 2>&1 | grep -q "Initialized" && [ -f .minilibrary/books.dat ] && [ -f .minilibrary/requests.dat ]; then
  pass "init creates books.dat and requests.dat"
else
  fail "init creates books.dat and requests.dat"
fi

######################################
# Test 2: request new book (1/3)
######################################

OUTPUT=$(../minilibrary request "Clean Code" "Robert C. Martin" 2>&1)
if echo "$OUTPUT" | grep -q "Request recorded" && echo "$OUTPUT" | grep -q "1/3"; then
  pass "request new book shows 1/3"
else
  fail "request new book shows 1/3 (got: $OUTPUT)"
fi

######################################
# Test 3: request increment (2/3)
######################################

OUTPUT=$(../minilibrary request "Clean Code" "Robert C. Martin" 2>&1)
if echo "$OUTPUT" | grep -q "2/3"; then
  pass "request increment shows 2/3"
else
  fail "request increment shows 2/3 (got: $OUTPUT)"
fi

######################################
# Test 4: request triggers order (3/3)
######################################

OUTPUT=$(../minilibrary request "Clean Code" "Robert C. Martin" 2>&1)
if echo "$OUTPUT" | grep -q "Order placed"; then
  pass "request triggers order at 3/3"
else
  fail "request triggers order at 3/3 (got: $OUTPUT)"
fi

######################################
# Test 5: request existing book
######################################

../minilibrary add "Dune" "Frank Herbert" > /dev/null 2>&1
OUTPUT=$(../minilibrary request "Dune" "Frank Herbert" 2>&1)
if echo "$OUTPUT" | grep -q "already exists"; then
  pass "request existing book shows error"
else
  fail "request existing book shows error (got: $OUTPUT)"
fi

######################################
# Test 6: listrequests empty
######################################

rm -rf .minilibrary
../minilibrary init > /dev/null 2>&1
OUTPUT=$(../minilibrary listrequests 2>&1)
if echo "$OUTPUT" | grep -q "No pending requests"; then
  pass "listrequests empty"
else
  fail "listrequests empty (got: $OUTPUT)"
fi

######################################
# Test 7: listrequests shows requests
######################################

../minilibrary request "Clean Code" "Robert C. Martin" > /dev/null 2>&1
OUTPUT=$(../minilibrary listrequests 2>&1)
if echo "$OUTPUT" | grep -q "Clean Code" && echo "$OUTPUT" | grep -q "1/3"; then
  pass "listrequests shows pending requests"
else
  fail "listrequests shows pending requests (got: $OUTPUT)"
fi

######################################
# Test 8: listrequests multiple
######################################

../minilibrary request "The Pragmatic Programmer" "David Thomas" > /dev/null 2>&1
OUTPUT=$(../minilibrary listrequests 2>&1)
if echo "$OUTPUT" | grep -q "Clean Code" && echo "$OUTPUT" | grep -q "The Pragmatic Programmer"; then
  pass "listrequests shows multiple requests"
else
  fail "listrequests shows multiple requests (got: $OUTPUT)"
fi

######################################
# Test 9: request removed after order
######################################

../minilibrary request "Clean Code" "Robert C. Martin" > /dev/null 2>&1
../minilibrary request "Clean Code" "Robert C. Martin" > /dev/null 2>&1
OUTPUT=$(../minilibrary listrequests 2>&1)
if echo "$OUTPUT" | grep -q "Clean Code"; then
  fail "request removed from list after order placed"
else
  pass "request removed from list after order placed"
fi

######################################
# Test 10: v1 commands still work (add + list)
######################################

../minilibrary add "The Little Prince" "Antoine de Saint-Exupery" > /dev/null 2>&1
OUTPUT=$(../minilibrary list 2>&1)
if echo "$OUTPUT" | grep -q "The Little Prince" && echo "$OUTPUT" | grep -q "AVAILABLE"; then
  pass "v1 add and list still work"
else
  fail "v1 add and list still work (got: $OUTPUT)"
fi

######################################
# Test 11: v1 borrow still works
######################################

OUTPUT=$(../minilibrary borrow 1 2>&1)
if echo "$OUTPUT" | grep -q "borrowed" && echo "$OUTPUT" | grep -q "Due date"; then
  pass "v1 borrow still works"
else
  fail "v1 borrow still works (got: $OUTPUT)"
fi

######################################
# Test 12: v1 return still works
######################################

OUTPUT=$(../minilibrary return 1 2>&1)
if echo "$OUTPUT" | grep -q "returned"; then
  pass "v1 return still works"
else
  fail "v1 return still works (got: $OUTPUT)"
fi

######################################
# Test 13: v1 delete still works
######################################

OUTPUT=$(../minilibrary delete 1 2>&1)
if echo "$OUTPUT" | grep -q "Deleted"; then
  pass "v1 delete still works"
else
  fail "v1 delete still works (got: $OUTPUT)"
fi

######################################
# Test 14: request before init
######################################

rm -rf .minilibrary
OUTPUT=$(../minilibrary request "Some Book" "Some Author" 2>&1)
if echo "$OUTPUT" | grep -q "Not initialized"; then
  pass "request before init shows error"
else
  fail "request before init shows error (got: $OUTPUT)"
fi

######################################
# Test 15: listrequests before init
######################################

OUTPUT=$(../minilibrary listrequests 2>&1)
if echo "$OUTPUT" | grep -q "Not initialized"; then
  pass "listrequests before init shows error"
else
  fail "listrequests before init shows error (got: $OUTPUT)"
fi

######################################
# Cleanup & Summary
######################################

cd ..
rm -rf testrepo

echo ""
echo "========================"
echo "PASSED: $PASS_COUNT"
echo "FAILED: $FAIL_COUNT"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo "========================"

if [ "$FAIL_COUNT" -eq 0 ]; then
  echo "ALL TESTS PASSED"
  exit 0
else
  exit 1
fi

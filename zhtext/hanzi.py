def is_hanzi(c):
  return ord(c) >= 0x4e00 and ord(c) <= 0x9fff

def count_hanzi(s):
  result = 0
  for c in s:
    if is_hanzi(c):
      result += 1
  return result

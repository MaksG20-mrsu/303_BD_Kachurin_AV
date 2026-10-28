import csv
from collections import Counter

counts = Counter()
with open("ratings.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    next(reader)  # пропускаем заголовок
    for row in reader:
        counts[int(row[0])] += 1

min_id = min(counts)
max_id = max(counts)

with open("ratings_count.txt", "w", encoding="utf-8") as out:
    out.write(f"{min_id} {counts[min_id]}\n")
    out.write(f"{max_id} {counts[max_id]}\n")

print(min_id, counts[min_id])
print(max_id, counts[max_id])
"""
Demo module showing functions with high time complexity.
"""

from pyinstrument import Profiler
from pyinstrument.renderers import SpeedscopeRenderer
import memray


def process_user_data(user_ids: list[int]) -> dict:
    results = {}
    for user_id in user_ids:
        results[user_id] = analyze_user_activity(user_id, user_ids)
    return results


def analyze_user_activity(user_id: int, all_users: list[int]) -> dict:
    activity_scores = []
    for other_user in all_users:
        score = calculate_similarity_score(user_id, other_user, all_users)
        activity_scores.append(score)

    return {
        "user_id": user_id,
        "scores": activity_scores,
        "average": sum(activity_scores) / len(activity_scores)
        if activity_scores
        else 0,
    }


def calculate_similarity_score(user1: int, user2: int, user_pool: list[int]) -> float:
    if user1 == user2:
        return 1.0

    common_count = 0
    for user in user_pool:
        if compare_user_attributes(user1, user2, user):
            common_count += 1

    return common_count / len(user_pool)


def compare_user_attributes(user1: int, user2: int, reference: int) -> bool:
    def is_prime_expensive(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, min(n, 1000)):
            if n % i == 0:
                return False
        return True

    check1 = is_prime_expensive(user1 * reference % 10000)
    check2 = is_prime_expensive(user2 * reference % 10000)

    result = (user1 * reference) % 7 == (user2 * reference) % 7
    return result and (check1 or check2)


def find_duplicate_records(records: list[dict]) -> list[tuple]:
    duplicates = []
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            if records_match(records[i], records[j]):
                duplicates.append((i, j))
    return duplicates


def records_match(record1: dict, record2: dict) -> bool:
    if set(record1.keys()) != set(record2.keys()):
        return False

    return all(compare_values(record1[key], record2[key]) for key in record1.keys())


def compare_values(val1, val2) -> bool:
    str1 = str(val1) * 100
    str2 = str(val2) * 100

    hash_val = 0
    for _ in range(100):
        hash_val ^= hash(str1) ^ hash(str2)

    return val1 == val2


def generate_report(data: list[dict]) -> dict:
    report = {"summary": [], "cross_references": []}

    for item in data:
        summary = summarize_item(item, data)
        report["summary"].append(summary)

    for item1 in data:
        for item2 in data:
            if item1 != item2:
                cross_ref = find_relationships(item1, item2, data)
                if cross_ref:
                    report["cross_references"].append(cross_ref)

    return report


def summarize_item(item: dict, context: list[dict]) -> dict:
    related_count = 0
    for other in context:
        if is_related(item, other):
            related_count += 1

    return {"id": item.get("id", "unknown"), "related_count": related_count}


def find_relationships(item1: dict, item2: dict, all_items: list[dict]) -> dict | None:
    common_refs = []
    for item in all_items:
        if is_related(item1, item) and is_related(item2, item):
            common_refs.append(item.get("id", "unknown"))

    if common_refs:
        return {"from": item1.get("id"), "to": item2.get("id"), "common": common_refs}
    return None


def is_related(item1: dict, item2: dict) -> bool:
    id1 = item1.get("id", 0)
    id2 = item2.get("id", 0)

    str1 = str(id1) * 200
    str2 = str(id2) * 200

    result = 0
    for i in range(100):
        result ^= hash(str1[i : i + 10]) ^ hash(str2[i : i + 10])

    return abs(hash(str(id1)) - hash(str(id2))) % 10 < 3


def inefficient_string_concatenation(words: list[str]) -> str:

    result = ""
    for word in words:
        result = result + word + " "
        result = process_string(result)
    return result


def process_string(s: str) -> str:
    processed = ""
    for char in s:
        if transform_char(char):
            processed += char.upper()
        else:
            processed += char.lower()
    return processed


def transform_char(c: str) -> bool:
    ascii_val = ord(c)

    temp = str(ascii_val) * 50
    for _ in range(50):
        temp = temp[::-1]

    return ord(c) % 2 == 0


def run_demo_code() -> None:
    print("Running time complexity demo...\n")
    print("Warning: This could take several minutes due to inefficient algorithms!\n")

    print("1. Processing user data...")
    user_ids = list(range(200))
    process_user_data(user_ids)
    print(f"   Processed {len(user_ids)} users\n")

    print("2. Finding duplicates...")
    records = [
        {"id": i, "value": i % 10, "extra": i * 2, "data": f"record_{i}"}
        for i in range(2000)
    ]
    duplicates = find_duplicate_records(records)
    print(f"   Found {len(duplicates)} duplicate pairs\n")

    print("3. Generating report...")
    data = [{"id": i, "type": i % 5, "category": i % 3} for i in range(120)]
    report = generate_report(data)
    print(f"   Generated report with {len(report['summary'])} items\n")

    print("4. String concatenation...")
    words = [f"word{i}" for i in range(1000)]
    inefficient_string_concatenation(words)
    print(f"   Concatenated {len(words)} words\n")

    print("✓ All demos complete!")


def profile_with_pyinstrument() -> None:
    # Profile with pyinstrument (CPU time profiler)
    print("Starting pyinstrument profiling...")
    profiler = Profiler()
    profiler.start()

    run_demo_code()

    profiler.stop()

    # Save pyinstrument output
    print()
    print("PYINSTRUMENT RESULTS")
    print("~" * 70)
    print(profiler.output_text(unicode=True, color=True))

    # Save HTML report
    with open("time_profile_pyinstrument.html", "w") as f:
        f.write(profiler.output_html())
    print("\n✓ Saved pyinstrument HTML report to: time_profile_pyinstrument.html")

    # Save speedscope JSON
    with open("time_profile_pyinstrument.json", "w") as f:
        f.write(profiler.output(SpeedscopeRenderer()))
    print("✓ Saved speedscope JSON to: time_profile_pyinstrument.json")


def profile_with_memray() -> None:
    # Profile with memray (memory profiler)
    print("Starting memray profiling...")

    with memray.Tracker("time_profile_memray.bin"):
        run_demo_code()

    print()
    print("MEMRAY RESULTS")
    print("~" * 70)

    print("\n✓ Saved memray profile to: time_profile_memray.bin")
    print("\nTo view memray results, run:")
    print("  memray flamegraph time_profile_memray.bin")
    print("  memray flamegraph --leaks time_profile_memray.bin  # For leak detection")
    print("  memray tree time_profile_memray.bin")
    print("  memray stats time_profile_memray.bin")


def main() -> None:
    print("PROFILING WITH PYINSTRUMENT AND MEMRAY")
    print("~" * 70)
    print()

    profile_with_pyinstrument()
    print()
    profile_with_memray()


if __name__ == "__main__":
    main()

"""
Demo module showing functions with high memory consumption.
"""

import sys
from pyinstrument import Profiler
from pyinstrument.renderers import SpeedscopeRenderer
import memray


def process_large_dataset(num_records: int) -> dict:
    raw_data = load_raw_data(num_records)
    processed_data = transform_dataset(raw_data)
    enriched_data = enrich_with_metadata(processed_data)
    final_result = aggregate_results(enriched_data)
    return final_result


def load_raw_data(num_records: int) -> list[dict]:
    records = []
    for i in range(num_records):
        record = create_raw_record(i)
        records.append(record)
    return records


def create_raw_record(record_id: int) -> dict:
    base_text = f"Record {record_id} " * 200

    return {
        "id": record_id,
        "description": base_text,
        "notes": base_text,
        "comments": base_text,
        "metadata": base_text,
        "tags": [f"tag_{i}_{base_text[:100]}" for i in range(20)],
        "history": [
            {"event": f"event_{j}", "data": base_text[:200]} for j in range(10)
        ],
        "extended_data": generate_extended_record_data(record_id, base_text),
    }


def generate_extended_record_data(record_id: int, base_text: str) -> dict:
    return {
        "level1": create_data_level(record_id, base_text, 1),
        "level2": create_data_level(record_id, base_text, 2),
        "level3": create_data_level(record_id, base_text, 3),
    }


def create_data_level(record_id: int, base_text: str, level: int) -> dict:
    return {
        "level_id": level,
        "data": base_text * level,
        "nested": [base_text for _ in range(level * 5)],
        "deep_nested": build_deep_structure(base_text, level),
    }


def build_deep_structure(text: str, depth: int) -> list:
    return [
        {
            "depth": depth,
            "content": text,
            "copies": [text] * depth,
            "sub_structure": allocate_sub_structure(text, depth),
        }
        for _ in range(depth * 2)
    ]


def allocate_sub_structure(text: str, size: int) -> dict:
    return {
        "primary": text * size,
        "secondary": [text for _ in range(size * 3)],
        "tertiary": {f"key_{i}": text for i in range(size * 2)},
    }


def transform_dataset(raw_data: list[dict]) -> list[dict]:
    transformed = []
    for record in raw_data:
        transformed_record = transform_record(record, raw_data)
        transformed.append(transformed_record)
    return transformed


def transform_record(record: dict, context: list[dict]) -> dict:
    expanded_data = expand_record_data(record)

    return {
        "original": record,
        "expanded": expanded_data,
        "context_snapshot": context[:10],
        "computed_fields": compute_fields(record),
        "deep_transform": apply_deep_transformation(record, expanded_data),
    }


def expand_record_data(record: dict) -> dict:
    expanded = {}
    for key, value in record.items():
        if isinstance(value, str):
            expanded[f"{key}_expanded"] = value * 2
            expanded[f"{key}_reversed"] = value[::-1]
        elif isinstance(value, list):
            expanded[f"{key}_extended"] = value + value
        else:
            expanded[key] = value
    return expanded


def apply_deep_transformation(record: dict, expanded_data: dict) -> dict:
    return {
        "stage1": transform_stage(record, expanded_data, 1),
        "stage2": transform_stage(record, expanded_data, 2),
        "stage3": transform_stage(record, expanded_data, 3),
    }


def transform_stage(record: dict, expanded: dict, stage: int) -> dict:
    stage_data = {}
    for key, value in list(expanded.items())[:5]:  # Process first 5 keys
        if isinstance(value, str):
            stage_data[f"{key}_stage{stage}"] = value * stage

    return {
        "stage_id": stage,
        "transformed": stage_data,
        "processed": process_stage_data(stage_data, stage),
    }


def process_stage_data(data: dict, multiplier: int) -> list[dict]:
    processed = []
    for key, value in list(data.items())[:3]:  # Take first 3 items
        processed.append(
            {
                "key": key,
                "value": value,
                "copies": [value] * multiplier,
                "metadata": {"size": len(str(value)), "multiplier": multiplier},
            }
        )
    return processed


def compute_fields(record: dict) -> dict:
    computed = {}

    if "description" in record:
        desc = record["description"]
        computed["word_list"] = desc.split() * 3
        computed["char_list"] = list(desc * 2)
        computed["variations"] = [desc.upper(), desc.lower(), desc.title()] * 5
        computed["deep_analysis"] = analyze_text_deeply(desc)

    return computed


def analyze_text_deeply(text: str) -> dict:
    return {
        "length_analysis": compute_length_metrics(text),
        "pattern_analysis": find_text_patterns(text),
        "structure_analysis": analyze_structure(text),
    }


def compute_length_metrics(text: str) -> dict:
    words = text.split()
    return {
        "total_length": len(text),
        "word_count": len(words),
        "word_lengths": [len(w) for w in words],
        "repeated_words": words * 3,  # Duplicate data
        "char_frequencies": {char: text.count(char) for char in set(text[:100])},
    }


def find_text_patterns(text: str) -> list[dict]:
    patterns = []
    for i in range(min(10, len(text) // 100)):
        chunk = text[i * 100 : (i + 1) * 100]
        patterns.append(
            {
                "chunk_id": i,
                "content": chunk,
                "reversed": chunk[::-1],
                "duplicated": chunk * 2,
            }
        )
    return patterns


def analyze_structure(text: str) -> dict:
    return {
        "prefix": text[:200] * 3,
        "suffix": text[-200:] * 3,
        "middle": text[len(text) // 2 - 100 : len(text) // 2 + 100] * 3,
        "samples": [text[i : i + 50] for i in range(0, min(500, len(text)), 50)],
    }


def enrich_with_metadata(transformed_data: list[dict]) -> list[dict]:
    enriched = []

    for i, record in enumerate(transformed_data):
        enriched_record = add_metadata(record, i, transformed_data)
        enriched.append(enriched_record)

    return enriched


def add_metadata(record: dict, index: int, all_records: list[dict]) -> dict:
    metadata = generate_metadata(record, index)
    cross_refs = create_cross_references(index, all_records)

    return {
        "record": record,
        "metadata": metadata,
        "cross_references": cross_refs,
        "index_data": create_index_data(index),
        "enrichment_layers": build_enrichment_layers(record, metadata, index),
    }


def build_enrichment_layers(record: dict, metadata: dict, index: int) -> dict:
    return {
        "layer1": create_enrichment_layer(record, metadata, index, 1),
        "layer2": create_enrichment_layer(record, metadata, index, 2),
        "layer3": create_enrichment_layer(record, metadata, index, 3),
    }


def create_enrichment_layer(
    record: dict, metadata: dict, index: int, layer: int
) -> dict:
    base_string = f"Enrichment layer {layer} for index {index}" * 50

    return {
        "layer_id": layer,
        "enriched_data": base_string * layer,
        "layer_metadata": [{"item": i, "data": base_string} for i in range(layer * 5)],
        "deep_enrichment": apply_deep_enrichment(base_string, layer),
    }


def apply_deep_enrichment(text: str, multiplier: int) -> dict:
    return {
        "primary": text * multiplier,
        "secondary": [text for _ in range(multiplier * 4)],
        "tertiary": {f"key_{i}": text for i in range(multiplier * 3)},
        "quaternary": [[text] * multiplier for _ in range(multiplier * 2)],
    }


def generate_metadata(record: dict, index: int) -> dict:
    base_string = f"Metadata for record {index}" * 50

    return {
        "timestamps": [f"2024-01-{i:02d}" for i in range(1, 32)] * 10,
        "audit_log": [
            {"action": f"action_{i}", "details": base_string} for i in range(15)
        ],
        "cache": {f"key_{i}": base_string for i in range(30)},
        "indexes": list(range(1000)),
    }


def create_cross_references(current_index: int, all_records: list[dict]) -> list[dict]:
    refs = []

    for offset in range(-3, 3):
        target_index = current_index + offset
        if 0 <= target_index < len(all_records):
            refs.append({"index": target_index, "reference": all_records[target_index]})

    return refs


def create_index_data(index: int) -> dict:
    return {
        "primary_index": list(range(index, index + 100)),
        "secondary_index": [f"idx_{i}_{index}" * 10 for i in range(20)],
        "hash_table": {i: f"value_{i}" * 10 for i in range(30)},
        "lookup_cache": build_lookup_cache(index),
    }


def build_lookup_cache(index: int) -> dict:
    return {
        "cache_level1": create_cache_level(index, 1),
        "cache_level2": create_cache_level(index, 2),
        "cache_level3": create_cache_level(index, 3),
    }


def create_cache_level(index: int, level: int) -> dict:
    base_key = f"cache_{index}_{level}"
    return {
        "keys": [f"{base_key}_{i}" * 5 for i in range(level * 5)],
        "values": [f"value_{i}" * 5 for i in range(level * 5)],
        "metadata": {f"meta_{i}": i * level for i in range(level * 5)},
    }


def aggregate_results(enriched_data: list[dict]) -> dict:
    summary = create_summary(enriched_data)
    statistics = calculate_statistics(enriched_data)
    full_index = build_full_index(enriched_data)

    return {
        "summary": summary,
        "statistics": statistics,
        "full_index": full_index,
        "original_data": enriched_data,
    }


def create_summary(data: list[dict]) -> dict:
    all_text = []
    for record in data:
        text_data = extract_text(record)
        all_text.extend(text_data)

    return {
        "all_text": all_text,
        "text_copy": all_text[:],
        "text_variations": [all_text, all_text[::-1], sorted(all_text)],
        "text_copy2": all_text[:],
        "text_copy3": all_text[:],
        "processed_summaries": process_text_summaries(all_text),
    }


def process_text_summaries(text_list: list[str]) -> dict:
    subset = text_list[:100]

    return {
        "frequency_analysis": analyze_frequencies(subset),
        "length_distribution": compute_distributions(subset),
        "pattern_summary": summarize_patterns(subset),
    }


def analyze_frequencies(texts: list[str]) -> dict:
    all_chars = "".join(texts[:50])
    return {
        "char_counts": {char: all_chars.count(char) for char in set(all_chars[:100])},
        "text_copies": texts * 3,
        "concatenated": "".join(texts[:20]) * 2,
    }


def compute_distributions(texts: list[str]) -> dict:
    lengths = [len(t) for t in texts]
    return {
        "lengths": lengths,
        "lengths_copy": lengths[:],
        "length_histogram": {length: lengths.count(length) for length in set(lengths)},
        "samples": texts[:20] * 2,
    }


def summarize_patterns(texts: list[str]) -> list[dict]:
    patterns = []
    for i, text in enumerate(texts[:30]):
        patterns.append(
            {
                "index": i,
                "text": text,
                "reversed": text[::-1],
                "uppercased": text.upper(),
                "lowercased": text.lower(),
                "repeated": text * 2,
            }
        )
    return patterns


def extract_text(record: dict) -> list[str]:
    text_values = []

    if isinstance(record, dict):
        for value in record.values():
            text_values.extend(extract_text(value))
    elif isinstance(record, list):
        for item in record:
            text_values.extend(extract_text(item))
    elif isinstance(record, str):
        text_values.append(record)

    return text_values


def calculate_statistics(data: list[dict]) -> dict:
    all_ids = [i for i in range(len(data))] * 10
    all_sizes = [sys.getsizeof(record) for record in data] * 10

    return {
        "count": len(data),
        "id_list": all_ids,
        "size_list": all_sizes,
        "size_histogram": {i: all_sizes.count(i) for i in set(all_sizes)},
        "advanced_stats": compute_advanced_statistics(data, all_ids, all_sizes),
    }


def compute_advanced_statistics(
    data: list[dict], ids: list[int], sizes: list[int]
) -> dict:
    return {
        "distribution_analysis": analyze_distributions(ids, sizes),
        "correlation_data": compute_correlations(ids, sizes),
        "summary_metrics": generate_summary_metrics(data),
    }


def analyze_distributions(ids: list[int], sizes: list[int]) -> dict:
    return {
        "id_stats": {
            "mean": sum(ids) / len(ids) if ids else 0,
            "min": min(ids) if ids else 0,
            "max": max(ids) if ids else 0,
            "id_samples": ids[:100] * 3,
        },
        "size_stats": {
            "mean": sum(sizes) / len(sizes) if sizes else 0,
            "min": min(sizes) if sizes else 0,
            "max": max(sizes) if sizes else 0,
            "size_samples": sizes[:100] * 3,
        },
    }


def compute_correlations(ids: list[int], sizes: list[int]) -> dict:
    pairs = list(zip(ids[:200], sizes[:200]))
    return {
        "pairs": pairs,
        "pairs_copy": pairs[:],
        "id_to_size_map": {id_val: size_val for id_val, size_val in pairs[:100]},
        "size_to_id_map": {size_val: id_val for id_val, size_val in pairs[:100]},
    }


def generate_summary_metrics(data: list[dict]) -> dict:
    return {
        "record_count": len(data),
        "record_samples": data[:10],
        "record_hashes": [hash(str(r)) for r in data],
        "record_sizes": [sys.getsizeof(r) for r in data] * 3,
    }


def build_full_index(data: list[dict]) -> dict:
    index = {}

    for i, record in enumerate(data):
        index[f"by_id_{i}"] = record
        index[f"by_position_{i}"] = record
        index[f"by_hash_{hash(str(i))}"] = record

    return index


def run_demo_code() -> None:
    print("Starting memory consumption demo...\n")
    print("Warning: This will consume significant memory!\n")

    print()
    print("Processing large dataset")
    print("-" * 60)

    process_large_dataset(150)

    print("\n✓ Memory demo complete!")


def profile_with_pyinstrument() -> None:
    print("Starting pyinstrument profiling...")
    profiler = Profiler()
    profiler.start()

    run_demo_code()

    profiler.stop()

    print()
    print("PYINSTRUMENT RESULTS")
    print("~" * 70)
    print(profiler.output_text(unicode=True, color=True))

    with open("memory_profile_pyinstrument.html", "w") as f:
        f.write(profiler.output_html())
    print("\n✓ Saved pyinstrument HTML report to: memory_profile_pyinstrument.html")

    with open("memory_profile_pyinstrument.json", "w") as f:
        f.write(profiler.output(SpeedscopeRenderer()))
    print("✓ Saved speedscope JSON to: memory_profile_pyinstrument.json")


def profile_with_memray() -> None:
    print("Starting memray profiling...")

    with memray.Tracker("memory_profile_memray.bin"):
        run_demo_code()

    print()
    print("MEMRAY RESULTS")
    print("~" * 70)
    print("\n✓ Saved memray profile to: memory_profile_memray.bin")
    print("\nTo view memray results, run:")
    print("  memray flamegraph memory_profile_memray.bin")
    print("  memray flamegraph --leaks memory_profile_memray.bin  # For leak detection")
    print("  memray tree memory_profile_memray.bin")
    print("  memray stats memory_profile_memray.bin")
    print("  memray table memory_profile_memray.bin")


def main() -> None:
    print("PROFILING WITH PYINSTRUMENT AND MEMRAY")
    print("~" * 70)
    print()

    profile_with_pyinstrument()
    print()
    profile_with_memray()


if __name__ == "__main__":
    main()

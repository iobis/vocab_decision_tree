
from flat_files_to_svg import flat_files_to_elk_with_wrapping

flat_files_to_elk_with_wrapping("nodes.csv", "edges.csv", "elk_input.json")
print("✅ ELK input JSON written to elk_input.json")


import csv
import json
import textwrap
import subprocess
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom as minidom

def flat_files_to_elk_with_wrapping(nodes_csv, edges_csv, elk_input_json,
                                     max_chars_per_line=30, font_size=20, line_height=28, padding=20):
    char_width = int(font_size * 0.6)
    nodes = []
    node_id_map = {}

    with open(nodes_csv, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node_id = row["id"]
            node_id_map[node_id] = node_id  # identity map
            label = row.get("label", row["id"])
            category = str(row.get("category", "")).strip()
            shape = row.get("shape", "rectangle")
            color = row.get("color", "#ffffcc")
            wrapped_lines = []
            for para in label.split("\n"):
                wrapped_lines.extend(textwrap.wrap(para, width=max_chars_per_line))
            lines = wrapped_lines or [""]
            max_line_len = max(len(line) for line in lines)
            width = max(char_width * max_line_len + padding, 100)
            height = line_height * len(lines) + padding
            node = {
                "id": node_id,
                "width": width,
                "height": height,
                "labels": [{
                    "text": label,
                    "layoutOptions": {
                "elk.category": category,
                        "elk.label.position": "CENTER"
                    }
                }],
                "layoutOptions": {
                    "elk.shape": shape,
                    "elk.fillColor": color,
                    "elk.category": category
                }


            }
            nodes.append(node)

    edges = []
    with open(edges_csv, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source = node_id_map[row["source_id"]]
            target = node_id_map[row["target_id"]]
            edge = {
                "id": f"e-{source[2:]}-{target[2:]}",
                "sources": [source],
                "targets": [target]
            }
            edges.append(edge)

    elk_json = {
        "id": "root",
        "layoutOptions": {
            "elk.algorithm": "layered",
            "elk.direction": "DOWN"
        },
        "children": nodes,
        "edges": edges
    }

    with open(elk_input_json, "w") as f:
        json.dump(elk_json, f, indent=2)

def run_elk_layout(elk_input_json, elk_output_json, elk_jar_path="elkjs.jar"):
    result = subprocess.run([
        "java", "-jar", elk_jar_path,
        "-i", elk_input_json,
        "-o", elk_output_json
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ELK layout failed: {result.stderr}")

def elk_json_to_svg(elk_output_json, svg_output_path, max_chars_per_line=30, font_size=20, line_height=28, padding=20):
    char_width = int(font_size * 0.6)
    with open(elk_output_json, "r") as f:
        elk_data = json.load(f)

    def get_fill_color(node):
        return node.get("layoutOptions", {}).get("elk.fillColor", "#ffffcc")

    svg = Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(int(elk_data["width"])),
        "height": str(int(elk_data["height"])),
        "viewBox": f"0 0 {int(elk_data['width'])} {int(elk_data['height'])}",
        "fill": "none"
    })

    SubElement(svg, "rect", {
        "width": str(int(elk_data["width"])),
        "height": str(int(elk_data["height"])),
        "fill": "#F5F5F5"
    })

    frame = SubElement(svg, "g", {"id": "Frame 58"})
    SubElement(frame, "rect", {
        "width": str(int(elk_data["width"])),
        "height": str(int(elk_data["height"])),
        "fill": "#F2EEE6"
    })

    for node in elk_data["children"]:
        node_id = node["id"]
        x, y = int(node["x"]), int(node["y"])
        def get_node_style(node):
            category_colors = {
                "Pre-determined": "#cce5ff",
                "Suggestion": "#d4edda",
                "Optional": "#fff3cd",
                "Text Only": "none",
                "Action": "#e0e0ff",
                "Recommendation": "#ffe0e0",
                "Guideline": "#e0f0ff",
                "Example": "#e6e6e6",
                "Strongly recommended": "#fff59d",
                "Negative Result": "#ef9a9a",
                "Directions": "#d1c4e9",
                "Legend": "#f5f5f5",
                "Data Attribute": "#fce4ec",
                "Vocab Term": "#ffe0b2",
                "Root": "#d7ccc8"
            }

            ellipse_categories = {"Pre-determined", "Suggestion", "Optional"}
            layout = node.get("layoutOptions", {})
            category = layout.get("elk.category", "").strip()
            fill = category_colors.get(category, "#f8f9fa")
            shape = "ellipse" if category in ellipse_categories else "none" if category == "Text Only" else "rectangle"
            return shape, fill


        label = node["labels"][0]["text"]
        wrapped_lines = []
        for para in label.split("\n"):
            wrapped_lines.extend(textwrap.wrap(para, width=max_chars_per_line))
        lines = wrapped_lines or [""]
        max_line_len = max(len(line) for line in lines)
        width = max(char_width * max_line_len + padding, 100)
        height = line_height * len(lines) + padding
        center_x = width // 2
        center_y = height // 2
        g_node = SubElement(frame, "g", {"id": node_id})
        shape, fill = get_node_style(node)
        if shape == "ellipse":
            SubElement(g_node, "ellipse", {
                "cx": str(center_x + x),
                "cy": str(center_y + y),
                "rx": str(width / 2),
                "ry": str(height / 2),
                "fill": fill,
                "stroke": "#000000"
            })
        elif shape != "none":
            SubElement(g_node, "rect", {
                "width": str(width),
                "height": str(height),
                "transform": f"translate({x} {y})",
                "fill": fill,
                "stroke": "#000000"
            })
        for i, line in enumerate(lines):
            line_y = center_y + i * line_height - ((len(lines) - 1) * line_height // 2)
            SubElement(g_node, "text", {
                "x": str(center_x),
                "y": str(line_y),
                "transform": f"translate({x} {y})",
                "font-family": "Arial",
                "font-size": str(font_size),
                "fill": "black",
                "text-anchor": "middle",
                "dominant-baseline": "middle"
            }).text = line

    for edge in elk_data["edges"]:
        g_edge = SubElement(frame, "g", {"id": edge["id"]})
        for section in edge.get("sections", []):
            points = [section["startPoint"]] + section.get("bendPoints", []) + [section["endPoint"]]
            d = " ".join(
                f"{'M' if i == 0 else 'L'}{int(pt['x'])} {int(pt['y'])}"
                for i, pt in enumerate(points)
            )
            SubElement(g_edge, "path", {
                "d": d,
                "stroke": "#4D5B80",
                "stroke-opacity": "0.75",
                "stroke-width": "3",
                "stroke-miterlimit": "0",
                "stroke-linecap": "round",
                "stroke-linejoin": "bevel"
            })

    pretty_svg = minidom.parseString(tostring(svg)).toprettyxml(indent="  ")
    with open(svg_output_path, "w") as f:
        f.write(pretty_svg)

def flat_files_to_svg(nodes_csv, edges_csv, svg_output_path, elk_jar_path="elkjs.jar"):
    elk_input = "elk_input.json"
    elk_output = "elk_output.json"
    flat_files_to_elk_with_wrapping(nodes_csv, edges_csv, elk_input)
    run_elk_layout(elk_input, elk_output, elk_jar_path)
    elk_json_to_svg(elk_output, svg_output_path)

if __name__ == "__main__":
    flat_files_to_svg(
        nodes_csv="nodes.csv",             # input: your node definitions
        edges_csv="edges.csv",             # input: your edge definitions
        svg_output_path="flowchart.svg",   # output: final SVG written here
        elk_jar_path="elkjs.jar"           # path to your local ELK .jar
    )

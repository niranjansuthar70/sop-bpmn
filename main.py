# main.py
import docx
from src.parser import SimpleSOPParser
from src.renderer import BPMNRenderer

def read_docx(file_path):
    doc = docx.Document(file_path)
    return [p.text for p in doc.paragraphs if p.text.strip()]

def main():
    # 1. Input
    print("Reading SOP...")
    lines = read_docx("C:\\Users\\NIRANJAN\\Desktop\\job_hunt_2025\\Kiagentic\\input_sop.docx")
    print(f"Read lines :{lines}")

    # 2. Parse
    print("Parsing Logic...")
    parser = SimpleSOPParser()
    graph = parser.parse(lines)

    # 3. Generate
    print("Generating BPMN...")
    renderer = BPMNRenderer()
    xml_content = renderer.render(graph)

    # 4. Output
    with open("output.bpmn", "w") as f:
        f.write(xml_content)
    print("Done! Saved to output.bpmn")

if __name__ == "__main__":
    main()
from lxml import etree

class BPMNRenderer:
    def __init__(self):
        # BPMN 2.0 Namespaces
        self.NS_MAP = {
            "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
            "dc": "http://www.omg.org/spec/DD/20100524/DC",
            "di": "http://www.omg.org/spec/DD/20100524/DI",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }

    def render(self, graph) -> str:
        # 1. Create Root Element
        definitions = etree.Element(
            f"{{{self.NS_MAP['bpmn']}}}definitions",
            nsmap=self.NS_MAP,
            id="Definitions_1",
            targetNamespace="http://bpmn.io/schema/bpmn"
        )

        # 2. Create Process Element (The Logic)
        process = etree.SubElement(definitions, f"{{{self.NS_MAP['bpmn']}}}process", id="Process_1", isExecutable="false")

        # 3. Create Diagram Element (The Visuals)
        diagram = etree.SubElement(definitions, f"{{{self.NS_MAP['bpmndi']}}}BPMNDiagram", id="BPMNDiagram_1")
        plane = etree.SubElement(diagram, f"{{{self.NS_MAP['bpmndi']}}}BPMNPlane", id="BPMNPlane_1", bpmnElement="Process_1")

        # --- A. GENERATE LOGIC ELEMENTS (NODES) ---
        for node in graph.nodes:
            tag_name = "task" # default
            if node.type == "start": tag_name = "startEvent"
            elif node.type == "end": tag_name = "endEvent"
            elif node.type == "gateway": tag_name = "exclusiveGateway"
            
            # Create the element: <bpmn:task id="..." name="...">
            element = etree.SubElement(process, f"{{{self.NS_MAP['bpmn']}}}{tag_name}", id=node.id, name=node.name)

        # --- B. GENERATE LOGIC CONNECTIONS (EDGES) ---
        for edge in graph.edges:
            # Create the flow: <bpmn:sequenceFlow id="..." sourceRef="..." targetRef="...">
            flow = etree.SubElement(
                process, 
                f"{{{self.NS_MAP['bpmn']}}}sequenceFlow", 
                id=edge.id, 
                sourceRef=edge.source, 
                targetRef=edge.target
            )
            if edge.label:
                flow.set("name", edge.label)

            # Link nodes to this flow (BPMN requires nodes to know their incoming/outgoing flows)
            # Note: For a simple prototype, explicit incoming/outgoing tags inside nodes are often optional 
            # in some viewers, but strict BPMN requires them. We'll skip adding <incoming> tags to nodes 
            # to keep the prototype simple, as bpmn.io handles this gracefully.

        # --- C. GENERATE VISUAL SHAPES (DI) ---
        current_x = 150
        y_pos = 100
        
        # Dictionary to store coordinates for edge calculation later
        node_coords = {}

        for node in graph.nodes:
            # Determine size based on type
            width = 36 if node.type in ["start", "end"] else (50 if node.type == "gateway" else 100)
            height = 36 if node.type in ["start", "end"] else (50 if node.type == "gateway" else 80)
            
            # Store center points for edge drawing
            node_coords[node.id] = {"x": current_x + (width/2), "y": y_pos + (height/2)}

            # Create Shape Wrapper
            shape = etree.SubElement(plane, f"{{{self.NS_MAP['bpmndi']}}}BPMNShape", id=f"{node.id}_di", bpmnElement=node.id)
            
            # Define Bounds
            etree.SubElement(shape, f"{{{self.NS_MAP['dc']}}}Bounds", x=str(current_x), y=str(y_pos), width=str(width), height=str(height))
            
            # Add Label tag (essential for viewing names)
            label = etree.SubElement(shape, f"{{{self.NS_MAP['bpmndi']}}}BPMNLabel")
            
            # Increment X for next element (Simple layout strategy)
            current_x += 160

        # --- D. GENERATE VISUAL EDGES (DI) ---
        for edge in graph.edges:
            edge_shape = etree.SubElement(plane, f"{{{self.NS_MAP['bpmndi']}}}BPMNEdge", id=f"{edge.id}_di", bpmnElement=edge.id)
            
            # Get coordinates
            start = node_coords.get(edge.source, {"x": 0, "y": 0})
            end = node_coords.get(edge.target, {"x": 0, "y": 0})

            # Draw generic waypoint line (Start -> End)
            etree.SubElement(edge_shape, f"{{{self.NS_MAP['di']}}}waypoint", x=str(int(start['x'])), y=str(int(start['y'])))
            etree.SubElement(edge_shape, f"{{{self.NS_MAP['di']}}}waypoint", x=str(int(end['x'])), y=str(int(end['y'])))

        return etree.tostring(definitions, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
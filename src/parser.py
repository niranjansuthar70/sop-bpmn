# src/parser.py
import re
from .models import ProcessGraph, Node

class SimpleSOPParser:
    def parse(self, text_lines):
        graph = ProcessGraph()
        
        # 1. Create a generic Start Event
        start_node = Node("Start", node_type="start")
        graph.add_node(start_node)
        
        last_node = start_node
        last_gateway = None  # To remember where "If" statements branch from

        for line in text_lines:
            clean_line = line.strip()
            if not clean_line: continue

            # Remove numbering (e.g., "1. " or "2.")
            clean_text = re.sub(r'^\d+\.?\s*', '', clean_line)

            # --- LOGIC DETECTION ---
            
            # Case A: Conditional Flow ("If yes...", "If no...")
            if clean_text.lower().startswith("if "):
                # Parse logic: "If yes, do X"
                condition_part, action_part = clean_text.split(',', 1)
                condition_label = condition_part.replace("If ", "").strip() # "yes"
                
                # Create the task for the action
                new_node = Node(action_part.strip(), node_type="task")
                graph.add_node(new_node)
                
                # Connect from the LAST GATEWAY, not the previous line
                if last_gateway:
                    graph.add_edge(last_gateway, new_node, label=condition_label)
                
                # Update last_node (so next steps continue from here if linear)
                last_node = new_node

            # Case B: Gateway / Decision ("Check if...", "Is it...")
            elif "?" in clean_text or clean_text.lower().startswith("check"):
                new_node = Node(clean_text, node_type="gateway")
                graph.add_node(new_node)
                
                # Connect previous step to this gateway
                graph.add_edge(last_node, new_node)
                
                # Set markers
                last_node = new_node
                last_gateway = new_node # Remember this for upcoming "If"s

            # Case C: Standard Task
            else:
                new_node = Node(clean_text, node_type="task")
                graph.add_node(new_node)
                graph.add_edge(last_node, new_node)
                last_node = new_node

        # 2. Add End Event
        end_node = Node("End", node_type="end")
        graph.add_node(end_node)
        graph.add_edge(last_node, end_node)

        return graph
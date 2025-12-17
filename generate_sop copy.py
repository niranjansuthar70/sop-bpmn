import docx

# Create a new valid Word document
doc = docx.Document()

# Add your specific content
lines = [
    "1. Receive customer support email.",
    "2. Check if the issue is billing-related.",
    "3. If yes, assign to Billing Queue.",
    "4. If no, assign to General Support Queue.",
    "5. Send acknowledgment email to customer.",
    "6. Close the triage step."
]

for line in lines:
    doc.add_paragraph(line)

# Save it to the correct path
file_path = "input_sop.docx" 
doc.save(file_path)

print(f"Successfully created a valid Word doc at: {file_path}")
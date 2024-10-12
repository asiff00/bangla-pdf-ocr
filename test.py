from bangla_pdf_ocr import process_pdf

path = "bangla_pdf_ocr\data\Freedom Fight.pdf"
output_file = "Extracted_text.txt"
extracted_text = process_pdf(path, output_file)

print(f"Text extracted and saved to: {output_file}")

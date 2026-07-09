import fitz  # PyMuPDF
import os

PDF_FOLDER = "data/pdfs"
OUTPUT_FOLDER = "data/processed"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text

def extract_all():
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    
    if not pdf_files:
        print("No PDFs found in", PDF_FOLDER)
        return
    
    for filename in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, filename)
        print(f"Extracting: {filename}...")
        text = extract_text_from_pdf(pdf_path)
        
        output_filename = filename.replace(".pdf", ".txt")
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"Saved: {output_filename} ({len(text):,} characters)")

if __name__ == "__main__":
    extract_all()
    print("\nAll PDFs extracted successfully.")
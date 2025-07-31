import os
import hashlib
from PyPDF2 import PdfReader
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_test_pdf(filepath, text):
    """Cria um PDF de teste com o texto especificado."""
    c = canvas.Canvas(filepath, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()


def calculate_file_hash(filepath, hash_algorithm='sha256'):
    """Calcula o hash de um arquivo."""
    hasher = hashlib.sha256() if hash_algorithm == 'sha256' else hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)  # Ler em blocos de 8KB
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def extract_text_from_pdf(pdf_path):
    """Extrai texto de um arquivo PDF."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Erro ao extrair texto do PDF {pdf_path}: {e}")
    return text


def extract_text_from_docx(docx_path):
    """Extrai texto de um arquivo DOCX."""
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Erro ao extrair texto do DOCX {docx_path}: {e}")
    return text


def find_duplicates(folder_path):
    """Encontra PDFs duplicados e DOCXs que são duplicatas de PDFs."""
    pdf_contents = {}
    docx_contents = {}
    duplicates = {"pdf_duplicates": [], "docx_pdf_duplicates": [], "docx_duplicates": []}

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filename.lower().endswith(".pdf"):
                file_content = extract_text_from_pdf(filepath)

                # Comparar PDFs por conteúdo de texto
                found_duplicate = False
                for existing_pdf_path, existing_pdf_content in pdf_contents.items():
                    if file_content.strip() == existing_pdf_content.strip() and file_content.strip() != "":
                        duplicates["pdf_duplicates"].append((filepath, existing_pdf_path))
                        found_duplicate = True
                        break
                if not found_duplicate:
                    pdf_contents[filepath] = file_content

            elif filename.lower().endswith(".docx"):
                file_content = extract_text_from_docx(filepath)
                docx_contents[filepath] = file_content

    # Comparar DOCX com PDFs
    for docx_path, docx_text in docx_contents.items():
        for pdf_path, pdf_text in pdf_contents.items():
            if docx_text.strip() == pdf_text.strip() and docx_text.strip() != "":
                duplicates["docx_pdf_duplicates"].append((docx_path, pdf_path))

    # Encontrar DOCXs duplicados de DOCXs
    docx_only_contents = {}
    for docx_path, docx_text in docx_contents.items():
        is_docx_pdf_duplicate = False  # Inicializa a variável para cada DOCX
        for dup_docx_path, _ in duplicates["docx_pdf_duplicates"]:
            if docx_path == dup_docx_path:
                is_docx_pdf_duplicate = True
                break
        if not is_docx_pdf_duplicate:
            found_duplicate = False
            for existing_docx_path, existing_docx_content in docx_only_contents.items():
                if docx_text.strip() == existing_docx_content.strip() and docx_text.strip() != "":
                    duplicates["docx_duplicates"].append((docx_path, existing_docx_path))
                    found_duplicate = True
                    break
            if not found_duplicate:
                docx_only_contents[docx_path] = docx_text

    return duplicates


def delete_duplicates(duplicates):
    """Deleta arquivos duplicados com base nas regras especificadas."""
    deleted_files = []

    # Regra 1: PDFs duplicados - manter apenas uma cópia
    for dup_pdf_path, original_pdf_path in duplicates["pdf_duplicates"]:
        if os.path.exists(dup_pdf_path):
            os.remove(dup_pdf_path)
            deleted_files.append(dup_pdf_path)
            print(f"Deletado PDF duplicado: {dup_pdf_path} (original: {original_pdf_path})")

    # Regra 2: DOCX duplicado de um PDF - apagar o DOCX
    for docx_path, pdf_path in duplicates["docx_pdf_duplicates"]:
        if os.path.exists(docx_path):
            os.remove(docx_path)
            deleted_files.append(docx_path)
            print(f"Deletado DOCX duplicado de PDF: {docx_path} (PDF original: {pdf_path})")

    # Regra 3: DOCXs duplicados de DOCXs - apagar apenas 1
    for dup_docx_path, original_docx_path in duplicates["docx_duplicates"]:
        if os.path.exists(dup_docx_path):
            os.remove(dup_docx_path)
            deleted_files.append(dup_docx_path)
            print(f"Deletado DOCX duplicado: {dup_docx_path} (original: {original_docx_path})")

    return deleted_files


if __name__ == "__main__":
    test_folder = ".\\arquivos"

    print(f"Verificando duplicatas na pasta: {test_folder}")
    found_duplicates = find_duplicates(test_folder)

    if found_duplicates["pdf_duplicates"]:
        print("\nPDFs duplicados encontrados:")
        for dup_pdf, original_pdf in found_duplicates["pdf_duplicates"]:
            print(f"- '{dup_pdf}' é uma duplicata de '{original_pdf}'")
    else:
        print("\nNenhum PDF duplicado encontrado.")

    if found_duplicates["docx_pdf_duplicates"]:
        print("\nDOCXs que são duplicatas de PDFs encontrados:")
        for docx_file, pdf_file in found_duplicates["docx_pdf_duplicates"]:
            print(f"- '{docx_file}' tem o mesmo conteúdo que '{pdf_file}'")
    else:
        print("\nNenhum DOCX com conteúdo de PDF duplicado encontrado.")

    if found_duplicates["docx_duplicates"]:
        print("\nDOCXs duplicados encontrados:")
        for dup_docx, original_docx in found_duplicates["docx_duplicates"]:
            print(f"- '{dup_docx}' é uma duplicata de '{original_docx}'")
    else:
        print("\nNenhum DOCX duplicado encontrado (apenas DOCX).")

    if found_duplicates["pdf_duplicates"] or found_duplicates["docx_pdf_duplicates"] or found_duplicates[
        "docx_duplicates"]:
        user_confirm = input("\nDesja deletar os arquivos duplicados encontrados? (s/n): ")
        if user_confirm.lower() == "s":
            deleted_files = delete_duplicates(found_duplicates)
            if deleted_files:
                print("\nArquivos deletados:")
                for f in deleted_files:
                    print(f"- {f}")
            else:
                print("Nenhum arquivo foi deletado.")
        else:
            print("Nenhum arquivo foi deletado.")
    else:
        print("Nenhuma duplicata encontrada para deletar.")

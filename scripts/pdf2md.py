import pymupdf4llm

file_path = r"Глава 7. Формы __ 1С_Предприятие 8.3.8. Документация.pdf"

md_text = pymupdf4llm.to_markdown(file_path)

with open(f"{file_path.split(".")[0]}.txt", "w", encoding="utf-8") as file:
    file.write(md_text)

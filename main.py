from src.code_reviewer.splitters import XMLMetadataSplitter


with open("Информация.xml", encoding="utf-8") as file:
    text = file.read()

splitter = XMLMetadataSplitter()

chunks = splitter.split_text(text)

print(chunks)

from src.code_reviewer.splitters import BSLCodeSplitter

splitter = BSLCodeSplitter()

with open("Информация.os", encoding="utf-8") as file:
    text = file.read()
    print(text)

docs = splitter.split_text(text)

print(docs)
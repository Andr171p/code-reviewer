from langchain_community.document_loaders import UnstructuredXMLLoader

loader = UnstructuredXMLLoader(
    "Информация.xml",
)

docs = loader.load()

print(docs)

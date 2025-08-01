from __future__ import annotations

from typing import Any

from abc import ABC, abstractmethod

from xml.etree import ElementTree as ET

from ..base import BaseTextSplitter, BaseChunk
from .constants import METADATA_TYPES

NAMESPACES: dict[str, str] = {
    "md": "http://v8.1c.ru/8.1/metadata"
}


class XMLChunk(BaseChunk):
    type: str
    name: str
    content: str
    metadata: dict[str, Any]

    def to_text(self) -> str:
        return f"""\
        """


class XMLMetadataHandler(ABC):
    def __init__(self, next_handler: XMLMetadataHandler | None = None) -> None:
        self._next_handler = next_handler

    def set_next(self, handler: XMLMetadataHandler) -> XMLMetadataHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(
            self, element: ET.Element, chunks: list[XMLChunk], **kwargs
    ) -> list[XMLChunk]:
        if self._next_handler:
            return self._next_handler.handle(element, chunks, **kwargs)
        return chunks


class MetadataObjectHandler(XMLMetadataHandler):
    def handle(
            self, element: ET.Element, chunks: list[XMLChunk], **kwargs
    ) -> list[XMLChunk]:
        handled_chunks: list[XMLChunk] = []
        if element.tag.endswith("}MetaDataObject") or element.tag == "MetaDataObject":
            for child in element:
                processed_chunks = self._process_element(child, chunks)
                handled_chunks.extend(processed_chunks)
            return handled_chunks
        return super().handle(element, chunks, **kwargs)

    @staticmethod
    def _process_element(element: ET.Element, chunks: list[XMLChunk]) -> list[XMLChunk]:
        for metadata_type in METADATA_TYPES:
            if (
                    element.tag.endswith(f"}}{metadata_type}") or
                    element.tag == metadata_type
            ):
                name = element.get("name")
                uuid = element.get("uuid")
                chunks.append(XMLChunk(
                    type=metadata_type,
                    name=name,
                    content=ET.tostring(element, encoding="unicode"),
                    metadata={
                        "uuid": uuid, "object_type": metadata_type, "is_main_object": True
                    }
                ))
            return chunks


class AttributeHandler(XMLMetadataHandler):
    def handle(
            self, element: ET.Element, chunks: list[XMLChunk], **kwargs
    ) -> list[XMLChunk]:
        handled_chunks: list[XMLChunk] = []
        if any(tag in element.tag for tag in ["Catalog", "Document", "Enum"]):
            for attr in element.findall(".//md:Attribute", NAMESPACES):
                processed_chunks = self._process_attribute(attr, element, chunks)
                handled_chunks.extend(processed_chunks)
            return handled_chunks
        return super().handle(element, chunks, **kwargs)

    @staticmethod
    def _process_attribute(
            attribute: ET.Element, parent: ET.Element, chunks: list[XMLChunk]
    ) -> list[XMLChunk] | None:
        parent_name = parent.get("name", "unnamed")
        parent_type = parent.tag.split("}")[-1] if "}" in parent.tag else parent.tag
        attribute_name = attribute.get("name", "unnamed")
        chunks.append(XMLChunk(
            type=f"{parent_type}Attribute",
            name=f"{parent_name}.{attribute_name}",
            content=ET.tostring(attribute, encoding="unicode"),
            metadata={
                "parent_object": parent_name,
                "attribute_type": attribute.get("type", ""),
                "is_attribute": True
            }
        ))
        return chunks


class TabularSectionHandler(XMLMetadataHandler):
    def handle(
            self, element: ET.Element, chunks: list[XMLChunk], **kwargs
    ) -> list[XMLChunk]:
        handled_chunks: list[XMLChunk] = []
        if any(tag in element.tag for tag in ["Catalog", "Document"]):
            for tabular in element.findall(".//md:TabularSection", NAMESPACES):
                processed_chunks = self._process_tabular(tabular, element, chunks)
                handled_chunks.extend(processed_chunks)
                return handled_chunks
        return super().handle(element, chunks, **kwargs)

    @staticmethod
    def _process_tabular(
            tabular: ET.Element, parent: ET.Element, chunks: list[XMLChunk]
    ) -> list[XMLChunk]:
        parent_name = parent.get("name", "unnamed")
        parent_type = parent.tag.split("}")[-1] if "}" in parent.tag else parent.tag
        tab_name = tabular.get("name", "unnamed")
        chunks.append(XMLChunk(
            type=f"{parent_type}TabularSection",
            name=f"{parent_name}.{tab_name}",
            content=ET.tostring(tabular, encoding="unicode"),
            metadata={
                "parent_object": parent_name,
                "is_tabular": True
            }
        ))
        for attribute in tabular.findall(".//md:Attribute", NAMESPACES):
            attr_name = attribute.get("name", "unnamed")
            chunks.append(XMLChunk(
                type=f"{parent_type}TabularAttribute",
                name=f"{parent_name}.{tab_name}.{attr_name}",
                content=ET.tostring(attribute, encoding="unicode"),
                metadata={
                    "parent_tabular": tab_name,
                    "parent_object": parent_name,
                    "attribute_type": attribute.get("type", ""),
                    "is_tabular_attribute": True
                }
            ))
        return chunks


class FormsHandler(XMLMetadataHandler):
    def handle(
            self, element: ET.Element, chunks: list[XMLChunk], **kwargs
    ) -> list[XMLChunk]:
        handled_chunks: list[XMLChunk] = []
        if any(tag in element.tag for tag in ["Catalog", "Document"]):
            for form in element.findall(".//md:Form", NAMESPACES):
                processed_chunks = self._process_form(form, element, chunks)
                handled_chunks.extend(processed_chunks)
                return handled_chunks
        super().handle(element, chunks, **kwargs)

    @staticmethod
    def _process_form(
            form: ET.Element, parent: ET.Element, chunks: list[XMLChunk]
    ) -> list[XMLChunk]:
        parent_name = parent.get("name", "unnamed")
        parent_type = parent.tag.split("}")[-1] if "}" in parent.tag else parent.tag
        form_name = form.get("name", "unnamed")
        form_type = form.get("type", "")
        chunks.append(XMLChunk(
            type=f"{parent_type}Form",
            name=f"{parent_name}.{form_name}",
            content=ET.tostring(form, encoding="unicode"),
            metadata={
                "parent_object": parent_name,
                "form_type": form_type,
                "is_form": True
            }
        ))
        return chunks


class CommandsHandler(XMLMetadataHandler):
    def handle(
            self, element: ET.Element, chunks: list[XMLChunk], **kwargs
    ) -> list[XMLChunk]:
        handled_chunks: list[XMLChunk] = []
        if any(tag in element.tag for tag in ["Catalog", "Document"]):
            for cmd in element.findall(".//md:Command", NAMESPACES):
                processed_chunks = self._process_command(cmd, element, chunks)
                handled_chunks.extend(processed_chunks)
                return handled_chunks
        return super().handle(element, chunks, **kwargs)

    @staticmethod
    def _process_command(
            command: ET.Element, parent: ET.Element, chunks: list[XMLChunk]
    ) -> list[XMLChunk]:
        parent_name = parent.get("name", "unnamed")
        parent_type = parent.tag.split("}")[-1] if "}" in parent.tag else parent.tag
        command_name = command.get("name", "unnamed")
        chunks.append(XMLChunk(
            type=f"{parent_type}Command",
            name=f"{parent_name}.{command_name}",
            content=ET.tostring(command, encoding="unicode"),
            metadata={
                "parent_object": parent_name,
                "is_command": True
            }
        ))
        return chunks


class XMLMetadataSplitter(BaseTextSplitter[XMLChunk]):
    def __init__(self) -> None:
        self.handler_chain = (
            MetadataObjectHandler()
            .set_next(AttributeHandler())
            .set_next(TabularSectionHandler())
            .set_next(FormsHandler())
            .set_next(CommandsHandler())
        )

    def split_text(self, text: str) -> list[XMLChunk]:
        chunks: list[XMLChunk] = []
        root = ET.fromstring(text)
        return self.handler_chain.handle(root, chunks)

from typing import AnyStr

import re

BSL_PATTERNS: dict[str, re.Pattern[AnyStr]] = {
    "procedure": re.compile(
        r"^\s*(?:Процедура|Procedure)\s+([\wа-яА-Я]+)\s*(?:\(([^)]*)\))?\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "function": re.compile(
        r"^\s*(?:Функция|Function)\s+([\wа-яА-Я]+)\s*(?:\(([^)]*)\))?\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "end_procedure": re.compile(
        r"^\s*(?:КонецПроцедуры|EndProcedure)\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "end_function": re.compile(
        r"^\s*(?:КонецФункции|EndFunction)\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "region": re.compile(
        r"^\s*#Область\s+(.*?)\s*$",
        re.IGNORECASE | re.MULTILINE
    ),
    "end_region": re.compile(
        r"^\s*#КонецОбласти\s*$",
        re.IGNORECASE | re.MULTILINE
    )
}

METADATA_TYPES: list[str] = [
    "Catalog",
    "Document",
    "Enum",
    "Report",
    "DataProcessor",
    "InformationRegister",
    "AccumulationRegister",
    "ChartOfAccounts",
    "ChartOfCalculationTypes",
    "BusinessProcess",
    "Task",
    "ExchangePlan",
    "FilterCriteria",
    "Subsystem",
    "CommonModule",
    "SessionParameter",
    "Role",
    "Style",
    "XDTOPackage",
    "WebService",
    "EventSubscription",
    "SettingsStorage",
    "CommandGroup",
    "Form",
    "Template",
    "CommonPicture",
    "CommonAttribute",
    "CommonCommand",
    "CommonForm",
    "CommonTemplate"
]

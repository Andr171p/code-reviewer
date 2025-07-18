
ONEC_SEPARATORS: list[str] = [
    # Разделение по началу процедур/функций
    "\nПроцедура ",
    "\nФункция ",
    # Разделение по управляющим конструкциям
    "\nЕсли ",
    "\nИначеЕсли ",
    "\nИначе ",
    "\nКонецЕсли",
    "\nДля ",
    "\nЦикл ",
    "\nПока ",
    "\nПопытка ",
    "\nИсключение ",
    # Разделение по объявлениям переменных
    "\nПерем ",
    # Разделение по ключевым словам модуля
    "\n#Область ",
    "\n#КонецОбласти",
    # Разделение по комментариям
    "\n//",
    # Стандартные разделители
    "\n\n",
    "\n",
    " ",
    "",
]

CPP_SEPARATORS: list[str] = [
    # Split along class definitions
    "\nclass ",
    # Split along function definitions
    "\nvoid ",
    "\nint ",
    "\nfloat ",
    "\ndouble ",
    # Split along control flow statements
    "\nif ",
    "\nfor ",
    "\nwhile ",
    "\nswitch ",
    "\ncase ",
    # Split by the normal type of lines
    "\n\n",
    "\n",
    " ",
    "",
]

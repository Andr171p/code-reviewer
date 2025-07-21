content = """
<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config " xmlns: cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform " xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns: sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns: v8="http://v8.1c.ru/8.1/data/core " xmlns: v8ui="http://v8.1c.ru/8.1/data/ui" xmlns: web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns: win="http://v8.1c.ru/8.1/data/ui/colors/windows " xmlns: xen="http://v8.1c.ru/8.3/xcf/enums" xmlns: xpr="http://v8.1c.ru/8.3/xcf/predef" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable " xmlns: xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" версия="2.20">
<HTTPService uuid="0692d112-8445-4724-99b9-2eec4ce26de8">
<Свойства>
<Имя>Совместное использование</Имя>
<Синоним>
<v8: элемент >
<v8:lang>ru</v8:lang>
<v8:content>Совместное использование</v8:content>
</v8:item>
</Синоним>
<Комментарий/>
<RootURL>сотрудничество</RootURL>
<Повторное использование сессий>Использовать</Повторное использование сессий>
<SessionMaxAge>60</SessionMaxAge>
</Свойства>
<дочерние объекты>
<Шаблон URL-адреса uuid="e4c45fda-95ec-4775-981f-5dd464d025f9">
<Свойства>
<Имя>Версия интерфейса</Имя>
<Синоним>
<v8: элемент >
<v8:lang>ru</v8:lang>
<v8:content>Версия интерфейса</v8:content>
</v8:item>
</Синоним>
<Комментарий/>
<Шаблон>/версия</Шаблон>
</Свойства>
<дочерние объекты>
<Метод uuid="5490e087-ecde-4123-8381-83f6d3bdf861">
<Свойства>
<Имя>Получить</Имя>
<Синоним>
<v8: элемент >
<v8:lang>ru</v8:lang>
<v8:content>GET</v8:content>
</v8:item>
</Синоним>
<Комментарий/>
<HTTPMethod>GET</HTTPMethod>
<Обработчик>ВерсияИнтерфейсаGET</Обработчик>
</Свойства>
</Метод>
</ChildObjects>
</URLTemplate>
<Шаблон URL-адреса uuid="d5776118-49c7-473e-a252-0aa65df51a71">
<Свойства>
<Имя>СпискиИзмененийСинхронизируемыхОбъектов</Имя>
<Синоним>
<v8: элемент >
<v8:lang>ru</v8:lang>
<v8:content>Списки изменений синхронизируемых объектов</v8:content>
</v8:item>
</Синоним>
<Комментарий/>
<Шаблон>/v1/change-records-snapshots</Шаблон>
</Свойства>
<дочерние объекты>
<Метод uuid="784693da-bff9-47aa-b71d-5aeab18961d5">
<Свойства>
<Имя>ПОСТ</Имя>
<Синоним>
<v8: элемент >
<v8:lang>ru</v8:lang>
<v8:content>POST</v8:content>
</v8:item>
</Синоним>
<Комментарий/>
<HTTPMethod>POST</HTTPMethod>
<Обработчик>СпискиИзмененийСинхронизируемыхОбъектовPOST</Обработчик>
</Properties>
</Method>
</ChildObjects>
</URLTemplate>
<URLTemplate uuid="faf80d78-f858-46ce-b2eb-6d7201803dd0">
<Properties>
<Name>СписокИзмененийСинхронизируемыхОбъектов</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>Список изменений синхронизируемых объектов</v8:content>
</v8:item>
</Synonym>
<Comment/>
<Template>/v1/change-records-snapshots/{snapshot-id}</Template>
</Properties>
<ChildObjects>
<Method uuid="42d23029-13d9-4583-a433-0e6bd61fe1d7">
<Properties>
<Name>GET</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>GET</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>GET</HTTPMethod>
<Handler>СписокИзмененийСинхронизируемыхОбъектовGET</Handler>
</Properties>
</Method>
<Method uuid="641247a9-7167-47cd-a7b2-a96f5075b875">
<Properties>
<Name>DELETE</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>DELETE</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>DELETE</HTTPMethod>
<Handler>СписокИзмененийСинхронизируемыхОбъектовDELETE</Handler>
</Properties>
</Method>
</ChildObjects>
</URLTemplate>
<URLTemplate uuid="42251adc-d736-4942-92cc-2b54da83da2d">
<Properties>
<Name>НастройкиПриложения</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>Настройки приложения</v8:content>
</v8:item>
</Synonym>
<Comment/>
<Template>/v1/app-config</Template>
</Properties>
<ChildObjects>
<Method uuid="31e23ca5-06f6-4f7b-8628-1ffc9b8a516e">
<Properties>
<Name>GET</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>GET</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>GET</HTTPMethod>
<Handler>НастройкиПриложенияGET</Handler>
</Properties>
</Method>
</ChildObjects>
</URLTemplate>
<URLTemplate uuid="8b7529b9-0edf-495d-856f-dbb39a35c3b9">
<Properties>
<Name>НастройкиСовместногоИспользования</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>Настройки совместного использования</v8:content>
</v8:item>
</Synonym>
<Comment/>
<Template>/v1/application-links/{app-id}</Template>
</Properties>
<ChildObjects>
<Method uuid="4df8558f-9ff6-4ef8-a3ca-ea51037dfb1f">
<Properties>
<Name>GET</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>GET</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>GET</HTTPMethod>
<Handler>НастройкиСовместногоИспользованияGET</Handler>
</Properties>
</Method>
<Method uuid="c2e70d9b-c9ff-43ec-afb0-7f1719e6724c">
<Properties>
<Name>PUT</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>PUT</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>PUT</HTTPMethod>
<Handler>НастройкиСовместногоИспользованияPUT</Handler>
</Properties>
</Method>
</ChildObjects>
</URLTemplate>
<URLTemplate uuid="bf6bf684-57fb-4f23-a92b-8bd0a5823940">
<Properties>
<Name>УчетнаяПолитика</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>Учетная политика</v8:content>
</v8:item>
</Synonym>
<Comment/>
<Template>/v1/accounting-policy</Template>
</Properties>
<ChildObjects>
<Method uuid="ca3e3a1d-b950-41cf-be07-7e26a1e52ff0">
<Properties>
<Name>GET</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>GET</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>GET</HTTPMethod>
<Handler>УчетнаяПолитикаGET</Handler>
</Properties>
</Method>
</ChildObjects>
</URLTemplate>
<URLTemplate uuid="8e197231-36b1-4711-8f32-ea470fb31894">
<Properties>
<Name>ДанныеПубличныхИдентификаторов</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>Данные публичных идентификаторов</v8:content>
</v8:item>
</Synonym>
<Comment/>
<Template>/v1/external-data</Template>
</Properties>
<ChildObjects>
<Method uuid="2200b93a-a0a8-4d2b-9278-57ff295cf37a">
<Properties>
<Name>POST</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>POST</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>POST</HTTPMethod>
<Handler>ДанныеПубличныхИдентификаторовPOST</Handler>
</Properties>
</Method>
</ChildObjects>
</URLTemplate>
<URLTemplate uuid="945edd21-2ac1-48b4-a127-6c522baf738d">
<Properties>
<Name>СозданиеОрганизации</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>Создание организации</v8:content>
</v8:item>
</Synonym>
<Comment/>
<Template>/v1/setup-organization</Template>
</Properties>
<ChildObjects>
<Method uuid="3fd83bd6-9baa-402a-b6d6-efd2861dd2a8">
<Properties>
<Name>PUT</Name>
<Synonym>
<v8:item>
<v8:lang>ru</v8:lang>
<v8:content>PUT</v8:content>
</v8:item>
</Synonym>
<Comment/>
<HTTPMethod>PUT</HTTPMethod>
<Handler>СозданиеОрганизацииPUT</Handler>
</Properties>
</Method>
</ChildObjects>
</URLTemplate>
</ChildObjects>
</HTTPService>
</MetaDataObject>
"""
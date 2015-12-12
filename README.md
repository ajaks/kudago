Тестовое задание для KudaGo

usage:
    `python manage.py import xmlFeed ./importer/tests/test.xml --events 93492 93822  --places 16767 10777 -c -s`

где:

    `xmlFeed` название парсера
    
    `./test.xml` путь до файла с данными
    
    `--events  93492 93822` доп параметр. Позволяет задать список конкретных событий на импорт
    
    `--places  93492 93822` доп параметр. Позволяет задать список конкретных мест на импорт
    
    `-c` или `--clean` запускает только парсер без маппера
    
    `-s` или `--silent` выключает логи
    

Идея исполнения такова:
kudagoM/ - некая уже существующая джанговская апликуха с модельками
importer/ - непосредственно маппер c management коммандой на импорт
    parsers/ - base и наследуемые от него парсеры различных источников
    mapper.py - непосредственно маппер.

Я считаю, что мапперу должно быть глубоко фиолетово какой источник данных использовать. Он просто берет на вход словарь и раскладывает его по моделькам.
Сам же парсер, оперируя готовыми методами из base(с добавлением специфичных свистелок для конкретного источника данных) подготавливает тот самый словарь.
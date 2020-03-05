# Pytlik

Aby vám Pytlík (už jsem z něj odstranil všechny šablony) fungoval, musíte si nainstalovat Django a zařídit databázi na svém počítači.
Nyní trochu podrobněji.

Django:
1. docela stačí zadat si do příkazového řádku následující pokyn: pip install django.
2. Až si stáhnete zde přiložené soubory, otevřete si složku je obsahující v příkazovém řádku a zadejte do něj pokyn: python manage.py runserver
3. Pokud bude vše v pořádku, měl by vám příkazový řádek odpovědět url adresou. Když ji zadáte do prohlížeče, vyskočí vám současná podona Pytlíka.
   Ale ještě před tím si zařiďe databázi.
  
Databáze:
1.Běte na tuto stránku: https://mariadb.com/downloads/ a stáhněte si nástroj na práci s databázemi.
2. Vytvořte si databázi Pytlik, namapujte ji na port 3306 a zadejte si heslo pouhazkouska 
   (tohoto procesu se nijak nebojte. V průběhu instalace a vytváření databáze se vás aplikace na všechno explicitně zeptá).
3. Až budete mít prázdnou databázi Pytlik, spusťte v ní soubor pytlik.sql

A pak už by vám mělo fungovat veškeré nic, které zatím máme.
Kdo by měl s čímkoliv problém, nechť mě kontaktuje.

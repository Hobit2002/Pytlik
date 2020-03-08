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
2. Otevřte si aplikaci HeidiSQL a vytvořte si "nové okno", přístupé údaje do tohoto okna nechť jsou následující
uživatel:root
heslo: pouhazkouska
Jakmile se vám okno vytvoří, klikněte pravým tlačítkem na lachtana (asi se jmenuje Mario) a ve vyskočivší nabídce zaklikněte, že chcete vytvořit nový objekt, což následněte rozvinete na databázi jménem pytlik.
3. Až budete mít prázdnou databázi Pytlik, klikněte na tlačítko Soubor (horní lišta úplně vlevo) a vyberte, že chcete "Run SQL file". 
   Program se vás zeptá, která složka to má být a vy vyberete pytlik.sql. 
   Nejspíše žádnou změnu neuvidíte, ale když okno opustíte a pak se do něj zase vrátíte, úspěch by se měl dostavit.

A pak už by vám mělo fungovat veškeré nic, které zatím máme.
Kdo by měl s čímkoliv problém, nechť mě kontaktuje.

#!/usr/bin/env python
# -*- coding: utf-8 -+-
import sys
import os
import re
import json
import glob2
import tempfile
import xlsxwriter
from io import BytesIO

usage = """\
usage: parser.py source_file output_file

    source_filename - path to pdf file to extract information
    output_file - path to xlsx file to store an output information
"""
DIV = "; "

FETCH_PARAMS = "Параметри запиту"

OBJECT_ADDRESS = "Адреса / Місцезнаходження"
OBJECT_KOD = "Кадастровий номер земельної ділянки"


REGISTRY1 = "ВІДОМОСТІ З ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО"

REGISTRY1_1 = "Актуальна інформація про об’єкт нерухомого майна"

REGISTRY1_1_1 = "Реєстраційний номер об’єкта нерухомого майна"
REGISTRY1_1_2 = "Об’єкт нерухомого майна"
REGISTRY1_1_3 = "Площа"
REGISTRY1_1_4 = "Кадастровий номер"
REGISTRY1_1_5 = "Цільове призначення"
REGISTRY1_1_6 = "Адреса"
REGISTRY1_1_7 = "Земельні ділянки місця розташування"

REGISTRY1_2 = "Актуальна інформація про право власності"

REGISTRY1_2_1 = "Номер запису про право власності"
REGISTRY1_2_2 = "Дата, час державної реєстрації"
REGISTRY1_2_3 = "Державний реєстратор"
REGISTRY1_2_4 = "Підстава виникнення права власності"
REGISTRY1_2_5 = "Підстава внесення запису"
REGISTRY1_2_6 = "Форма власності"
REGISTRY1_2_7 = "Розмір частки"
REGISTRY1_2_8 = "Власники"
REGISTRY1_2_9 = "Додаткові відомості"
REGISTRY1_2_10 = 'Актуальна інформація про реєстрацію іншого речового права'

REGISTRY1_3 = "Актуальна інформація про державну реєстрацію іпотеки"

REGISTRY1_3_1 = "Номер запису про іпотеку"
REGISTRY1_3_2 = "Дата, час державної реєстрації"
REGISTRY1_3_3 = "Державний реєстратор"
REGISTRY1_3_4 = "Підстава виникнення іпотеки"
REGISTRY1_3_5 = "Підстава внесення запису"
REGISTRY1_3_6 = "Відомості про основне зобов’язання"
REGISTRY1_3_7 = "Відомості про суб’єктів"
REGISTRY1_3_8 = "Додаткові відомості про іпотеку"
REGISTRY1_3_9 = "Відомості про об’єкт іпотеки"


REGISTRY1_4 = "Актуальна інформація про державну реєстрацію обтяжень"

REGISTRY1_4_1 = "Номер запису про обтяження"
REGISTRY1_4_2 = "Дата, час державної реєстрації"
REGISTRY1_4_3 = "Державний реєстратор"
REGISTRY1_4_4 = "Підстава виникнення обтяження"
REGISTRY1_4_5 = "Підстава внесення запису"
REGISTRY1_4_6 = "Вид обтяження"
REGISTRY1_4_7 = "Відомості про суб’єктів обтяження"
REGISTRY1_4_8 = "Відомості про реєстрацію до 01.01.2013р."
REGISTRY1_4_9 = "Додаткові відомості про обтяження"
REGISTRY1_4_10 = "Відомості про об’єкт обтяження"


REGISTRY2 = "ВІДОМОСТІ З РЕЄСТРУ ПРАВ ВЛАСНОСТІ НА НЕРУХОМЕ МАЙНО"

REGISTRY2_1 = "ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА"

REGISTRY2_1_1 = "Реєстраційний номер майна"
REGISTRY2_1_2 = "Тип майна"
REGISTRY2_1_3 = "Адреса нерухомого майна"
REGISTRY2_1_4 = "Інформація"
REGISTRY2_1_5 = "Номер запису"

REGISTRY2_2 = "ВІДОМОСТІ ПРО ПРАВА ВЛАСНОСТІ"

REGISTRY2_2_1 = "Дата прийняття рішення про державну реєстрацію"
REGISTRY2_2_2 = "Дата внесення запису"
REGISTRY2_2_3 = "ПІБ"
REGISTRY2_2_4 = "Форма власності"
REGISTRY2_2_5 = "Частка власності"
REGISTRY2_2_6 = "Підстава виникнення права власності"


REGISTRY3 = "ВІДОМОСТІ З ЄДИНОГО РЕЄСТРУ ЗАБОРОН ВІДЧУЖЕННЯ ОБ’ЄКТІВ НЕРУХОМОГО МАЙНА"


REGISTRY3_1 = "ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ ДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО"

REGISTRY3_1_1 = "Номер запису про обтяження"
REGISTRY3_1_2 = "Дата перенесення"
REGISTRY3_1_3 = "Запис"

REGISTRY3_2 = "Інформація"

REGISTRY3_2_1 = "Тип обтяження"
REGISTRY3_2_2 = "Реєстраційний номер обтяження"
REGISTRY3_2_3 = "Зареєстровано"
REGISTRY3_2_4 = "Підстава обтяження"
REGISTRY3_2_5 = "Об’єкт обтяження" 
REGISTRY3_2_6 = "Власник"
REGISTRY3_2_7 = "Заявник"
REGISTRY3_2_8 = "Додаткові дані"


REGISTRY4 = "ВІДОМОСТІ З ДЕРЖАВНОГО РЕЄСТРУ ІПОТЕК"

REGISTRY4_1 = "ВІДОМОСТІ ПРО ІПОТЕКУ"

REGISTRY4_1_1 = "Реєстраційний номер обтяження"
REGISTRY4_1_2 = "Тип обтяження"
REGISTRY4_1_3 = "Зареєстровано"
REGISTRY4_1_4 = "Підстава обтяження"
REGISTRY4_1_5 = "Об’єкт обтяження"
REGISTRY4_1_6 = "Іпотекодержатель"
REGISTRY4_1_7 = "Іпотекодавець"
REGISTRY4_1_8 = "Розмір основного зобов’язання"
REGISTRY4_1_9 = "Строк виконання"
REGISTRY4_1_10 = "Заставна"
REGISTRY4_1_11 = "Додаткові дані"
REGISTRY4_1_12 = "Майновий поручитель"
REGISTRY4_1_13 = "Боржник"


REGISTRY4_2 = "ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ ДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО"

REGISTRY4_2_1 = "Номер запису про іпотеку"
REGISTRY4_2_2 = "Дата перенесення"
REGISTRY4_2_3 = "Запис"




GROUP_OBJECT1 = (
	(0,
	 r'(Реєстраційний номер\nоб’єкта нерухомого\nмайна:\n.*?(?=Актуальна інформація про об’єкт нерухомого майна|$))'),
)

GROUP_OBJECT2 = (
	(0,
	 r'(ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА\n.*?(?=ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА|$))'),
)
GROUP_OBJECT2_2 = (
	(0,
	 r'(Дата прийняття рішення\nпро державну\nреєстрацію:\n.*?(?=Дата прийняття рішення\nпро державну\nреєстрацію:\n|$))'),
)

GROUP_OBJECT3 = (
	(0,
	 r'(Тип обтяження:.*?(?=Тип обтяження|$))'),
)
GROUP_OBJECT3_2 = (
	(0,
	 r'(Тип обтяження:.*?(?=Тип обтяження|ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ|$))'),
)

GROUP_OBJECT3_1 = (
	(0,
	 r'(Номер запису про\nобтяження:.*?(?=Номер запису про\nобтяження|ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ|$))'),
)

GROUP_OBJECT4 = (
	(0,
	 r'(Реєстраційний номер\nобтяження:.*?(?=Реєстраційний номер\nобтяження|$))'),
)

GROUP_OBJECT4_1 = (
	(0,
	 r'(Реєстраційний номер\n.*?(?=ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ|Реєстраційний номер|$))'),
)

GROUP_OBJECT4_2 = (
	(0,
	 r'(Номер запису про\nіпотеку:.*?(?=ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ|Номер запису про\nіпотеку|$))'),
)

GROUP_ALL = (
	(FETCH_PARAMS,r'Параметри запиту(.*?)ВІДОМОСТІ'),
	(REGISTRY1,
	 r'ВІДОМОСТІ\nЗ ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО\n(.*?)ВІДОМОСТІ'),
	(REGISTRY2,
	 r'ВІДОМОСТІ\nЗ РЕЄСТРУ ПРАВ ВЛАСНОСТІ НА НЕРУХОМЕ МАЙНО\n(.*?)ВІДОМОСТІ\nЗ ЄДИНОГО РЕЄСТРУ'),
	(REGISTRY3,
	 r'ВІДОМОСТІ\nЗ ЄДИНОГО РЕЄСТРУ ЗАБОРОН ВІДЧУЖЕННЯ ОБ’ЄКТІВ НЕРУХОМОГО МАЙНА\n(.*?)ВІДОМОСТІ'),
	(REGISTRY4,
	 r'ВІДОМОСТІ\nЗ ДЕРЖАВНОГО РЕЄСТРУ ІПОТЕК\n(.*?)$'),
)

GROUP_OBJECT = (
	(OBJECT_ADDRESS,
	 r'Адреса /\nМісцезнаходження:\n(.*?)$'),
	(OBJECT_KOD,
	 r'Кадастровий номер\nземельної ділянки:\n(\d{10}:\d{2}:\d{3}:\d{4})'),
)

GROUP_REG1 = (
	(REGISTRY1_1,
	 r'(Реєстраційний номер\nоб’єкта нерухомого\nмайна:\n.*?(?=Реєстраційний|$|Актуальна|відсутні))'),
	(REGISTRY1_2,
	 r'(Номер запису про право(?:\n| )власності:.*?(?=Номер запису про право(?:\n| )власності|$|Актуальна інформація про державну реєстрацію іпотеки|Відомості про реєстрацію іншого речового права відсутні))'),
	(REGISTRY1_3,
	 r'(Номер запису про(?:\n| )іпотек(?:у|и):.*?\n(?=Номер запису|$|Актуальна|відсутні))'),
	(REGISTRY1_4,
	 r'(Номер запису про(?:\n| )обтяження:.*?(?:\n|)(?=$|Номер запису про(?:\n| )обтяження:|ВІДОМОСТІ|Актуальна|відсутні))'),
)

GROUP_REG1_1 = (
	(REGISTRY1_1_1,
	 r'Реєстраційний номер\nоб’єкта нерухомого\nмайна:\n(\d{8,14})\n'),
	(REGISTRY1_1_2,
	 r'Об’єкт нерухомого\nмайна:\n(.*Ні|.*Так|.*\n(?=Адреса:))'),
	(REGISTRY1_1_3,r'Площа:(.*?)\n'),
	(REGISTRY1_1_4,
	 r'Кадастровий номер:(\d{10}:\d{2}:\d{3}:\d{4})\n'),
	(REGISTRY1_1_5,
	 r'Цільове призначення:\n(.*)\nАдреса'),
	(REGISTRY1_1_6,r'Адреса:(.*?)\n(?:Актуальна інформація|Земельні|Додаткові|Відомості|$)'),
	(REGISTRY1_1_7,
     r'Земельні ділянки місця.*розташування:\n(.*?)($|Актуальна)'),
)

GROUP_REG1_2 = (
	(REGISTRY1_2_1,r'Номер запису про право(?:\n| )власності:.*?(\d{4,12})'),
	(REGISTRY1_2_2,r'Дата, час державної\nреєстрації:\n(.*? .*?)\n'),
	(REGISTRY1_2_3,r'Державний реєстратор:(.*?)\nПідстава'),
	(REGISTRY1_2_4,r'Підстава виникнення\nправа власності:(.*?)\nПідстава внесення'),
	(REGISTRY1_2_5,r'Підстава внесення\nзапису:\n(.*?)\nФорма власності'),
	(REGISTRY1_2_6,r'Форма власності:(.*?)\n'),
	(REGISTRY1_2_7,r'Розмір частки:(.*?)\n'),
	(REGISTRY1_2_8,r'Власники:(.*?)\n(Номер запису про право|Актуальна|Додаткові|Відомості|$)'),
	(REGISTRY1_2_9,r'Додаткові відомості:(.*?)\n(Актуальна|Додаткові|Відомості|$)'),
	(REGISTRY1_2_10,r'Актуальна інформація про реєстрацію іншого речового права\n(.*?)(Актуальна|Додаткові|$)'),

)

GROUP_REG1_3 = (
	(REGISTRY1_3_1,r'Номер запису про(?:\n| )іпотеку:(.*?)\n'),
	(REGISTRY1_3_2,r'Дата, час державної\nреєстрації:\n(.*? .*?)\n'),
	(REGISTRY1_3_3,r'Державний реєстратор:(.*?)\nПідстава'),
	(REGISTRY1_3_4,r'Підстава виникнення\nіпотеки:(.*?)\nПідстава внесення'),
	(REGISTRY1_3_5,r'Підстава внесення\nзапису:\n(.*?)\nВідомості'),
	(REGISTRY1_3_6,r'Відомості про основне\nзобов’язання:\n(.*?)\nВідомості'),
	(REGISTRY1_3_7,r'Відомості про суб’єктів:(.*?)\n(Додаткові.*?:|Відомості.*?(?:.|)|Адреса.*?:|Зміст,|Опис.*?)'),
	(REGISTRY1_3_8,r'Опис предмета іпотеки:(.*?)(?:Актуальна|Додаткові|Відомості|$)'),
	(REGISTRY1_3_9,r'Відомості про об’єкт\nнерухомого майна\n(.*?)(?:Актуальна|Додаткові|Відомості|ВІДОМОСТІ|$)'),
)
GROUP_REG1_4 = (
	(REGISTRY1_4_1,r'Номер запису про(?:\n| )обтяження:(?:\n| )(.*?)\n'),
	(REGISTRY1_4_2,r'Дата, час державної\nреєстрації:\n(.*? .*?)\n'),
	(REGISTRY1_4_3,r'Державний реєстратор: (.*?)\nПідстава'),
	(REGISTRY1_4_4,r'Підстава виникнення\nобтяження:\n(.*?)\nПідстава внесення'),
	(REGISTRY1_4_5,r'Підстава внесення\nзапису:\n(.*?)\n(Відомості|Вид|Форма)'),
	(REGISTRY1_4_6,r'Вид обтяження: (.*?)\n(Відомості|$)'),
	(REGISTRY1_4_7,r'Відомості про суб’єктів\nобтяження:(.*?)($|Зміст,|ВІДОМОСТІ|Відомості|Вид|Опис)'),
	(REGISTRY1_4_8,r'Відомості про реєстрацію\nдо 01.01.2013р.:\n(.*?)(Відомості|Актуальна|Зміст|$)'),
	(REGISTRY1_4_9,r'(?:Опис предмета\nобтяження|Зміст, характеристика\nобтяження):(.*?)(?:Актуальна|Додаткові|Відомості|ВІДОМОСТІ|$)'),
	(REGISTRY1_4_10,r'Відомості про об’єкт\nнерухомого майна\n(.*?)(?:Актуальна|Додаткові|Відомості|ВІДОМОСТІ|$)'),
)

GROUP_REG2 = (
	(REGISTRY2_1,
	 r'ВІДОМОСТІ ПРО ОБ’ЄКТ НЕРУХОМОГО МАЙНА\n(.*?)\nВІДОМОСТІ'),
	(REGISTRY2_2,
	 r'ВІДОМОСТІ ПРО ПРАВА ВЛАСНОСТІ\n(.*?)$'),
)

GROUP_REG2_1 = (
	(REGISTRY2_1_1,
	 r'Реєстраційний номер\nмайна:\n(\d{8,14})\n'),
	(REGISTRY2_1_2,
	 r'Тип майна:(.*?)\nАдреса'),
	(REGISTRY2_1_3,r'Адреса нерухомого\nмайна:[\n|\s](.*?\d{1,5})\n'),
	(REGISTRY2_1_4,
	 r'Адреса нерухомого\nмайна:[\n|\s].*?\d{1,5}.*\n(Загальна площа.*)\nНомер запису:'),
	(REGISTRY2_1_5,r'Номер запису: (.*?)(\n|ВІДОМОСТІ|$)'),
)

GROUP_REG2_2 = (
	(REGISTRY2_2_1,
	 r'Дата прийняття рішення\nпро державну\nреєстрацію:\n(.*?)\n'),
	(REGISTRY2_2_2,
	 r'Дата внесення запису: (.*?)\n'),
	(REGISTRY2_2_3,r'(?:Назва|ПІБ): (.*?)\n(?:Форма власності|ВІДОМОСТІ|$)'),
	(REGISTRY2_2_4,
	 r'Форма власності: (.*?)\n'),
	(REGISTRY2_2_5,r'Частка власності: (.*?)\n'),
	(REGISTRY2_2_6,r'Підстава виникнення\nправа власності:\n(.*?)(Відомості|ВІДОМОСТІ ПРО ІНШІ|$)'),
)

GROUP_REG3 = (
	(REGISTRY3_1,
	 r'ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ\nДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО\n(.*?)$'),
	(REGISTRY3_2,
	 r'(Тип обтяження:.*?)(?=ВІДМІТКА|$|Актуальна|відсутні)'),
)

GROUP_REG3_1 = (
	(REGISTRY3_1_1,
	 r'Номер запису про\nобтяження:\n(.*?)\nДата перенесення'),
	(REGISTRY3_1_2,
	 r'Дата перенесення: (.*?)(?:\n|ВІДОМОСТІ|$)'),
	(REGISTRY3_1_3,r'Дата перенесення:.*?\n(.*?)(?:ВІДОМОСТІ|$)'),
)

GROUP_REG3_2 = (
	(REGISTRY3_2_1,
	 r'Тип обтяження:(.*?)\n(Реєстраційний)'),
	(REGISTRY3_2_2,
	 r'Реєстраційний номер\nобтяження:\n(.*?)\nЗареєстровано'),
	(REGISTRY3_2_3,r'Зареєстровано:(?:.|..)(.*?)\nПідстава обтяження'),
	(REGISTRY3_2_4,r'Підстава обтяження:(.*?)\nОб’єкт обтяження'),
	(REGISTRY3_2_5,r'Об’єкт обтяження: (.*?)\n(?:Власник)'),
	(REGISTRY3_2_6,r'Власник: (.*?)\n(?:Заявник|Обтяжувач|Додаткові)'),
	(REGISTRY3_2_7,r'Заявник: (.*?)(ВІДОМОСТІ|$)'),
	(REGISTRY3_2_8,r'Додаткові дані:(.*?)\n(ВІДМІТКА|$)'),
)

GROUP_REG4 = (
	(REGISTRY4_1,
	 r'(Реєстраційний номер.*?)(?:\nВІДМІТКА|$)'),
	(REGISTRY4_2,
	 r'ВІДМІТКА ПРО ПЕРЕНЕСЕННЯ ЗАПИСУ\nДО ДЕРЖАВНОГО РЕЄСТРУ РЕЧОВИХ ПРАВ НА НЕРУХОМЕ МАЙНО\n(.*?)(?:Реєстраційний номер\nобтяження|$)'),
)

GROUP_REG4_1 = (
	(REGISTRY4_1_1,
	 r'Реєстраційний номер\nобтяження:\n(.*?)\n'),
	(REGISTRY4_1_2,
	 r'Тип обтяження: (.*?)\nЗареєстровано'),
	(REGISTRY4_1_3,r'Зареєстровано:(?:.|..)(.*?)\nПідстава обтяження'),
	(REGISTRY4_1_4,
	 r'Підстава обтяження: (.*?)\nОб’єкт'),
	(REGISTRY4_1_5,
	 r'Об’єкт обтяження: (.*?)\n(?:Іпотекодержатель)'),
	(REGISTRY4_1_6,r'Іпотекодержатель: (.*?)\n(?:Іпотекодавець|Майновий|Боржник|Розмір)'),
	(REGISTRY4_1_7,
	 r'Іпотекодавець: (.*?)\n(?:Боржник|Розмір)'),
	(REGISTRY4_1_8,
	 r'Розмір основного\nзобов’язання:\n(.*?)\nСтрок'),
	(REGISTRY4_1_9,r'Строк виконання: (.*?)\n'),
	(REGISTRY4_1_10,
	 r'Заставна: (.*?)(?:Додаткові|$)'),
	(REGISTRY4_1_11,
	 r'Додаткові дані: (.*?)$'),
	(REGISTRY4_1_12,
	 r'Майновий поручитель: (.*?)(?:Розмір основного|Боржник|Додаткові|$)'),
	(REGISTRY4_1_13,
	 r'Боржник за основним\nзобов’язанням:(?:\n| )(.*?)(?:Додаткові|Розмір|Строк|Заставна|$)'),
)

GROUP_REG4_2 = (
	(REGISTRY4_2_1,
	 r'Номер запису про\nіпотеку:(.*?)\nДата перенесення'),
	(REGISTRY4_2_2,
	 r'Дата перенесення:(?:.|..)(.*?)(?:\n|ВІДОМОСТІ|$)'),
	(REGISTRY4_2_3,r'Дата перенесення:.*?\n(.*?)(?:ВІДОМОСТІ ПРО ІПОТЕКУ|$)'),
)


def separate(data,GROUP_PARAMS):

	"""simple extraction in format of dictionary

	"""
	dic = {}
	for group in GROUP_PARAMS:
		for param1,param2 in [group]:
			p = re.search(param2,data,re.U|re.S)
			dic[param1] = p.group(1) if p else "None"
	return dic

def second_lvl_extraction(data,GROUP_PARAMS):

	""" returns a dictionary
			key - keyword for a group
			value - list of matches

	"""
	dic = {}
	for group in GROUP_PARAMS:
		for param1,param2 in [group]:
			p = re.findall(param2,data,re.U|re.S)
			dic[param1] = p if p else []
	return dic

def first_lvl_extraction(data,GROUP_PARAMS):
	
	"""returns a simple list of matches

	"""
	p = re.findall(GROUP_PARAMS[0][1],data,re.U|re.S)
	return p

def shorten(p):
	p1 = re.search(r'(?:Т(?:ОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ|овариство з обмеженою відповідальністю)|товариство з обмеженою відповідальністю) (.*?\d{8})',
				p,re.U|re.I|re.S)
	if p1:
		return "TOB " + p1.group(1).replace(' код ЄДРПОУ:','')

	p2 = re.search(r'(?:П(?:УБЛІЧНЕ АКЦІОНЕРНЕ ТОВАРИСТВО|ублічне акціонерне товариство|ублічне Акціонерне Товариство)|публічне акціонерне товариство) (.*?\d{8})',
				p,re.U|re.I|re.S)

	if p2:
		return "ПАТ " + p2.group(1).replace(' код ЄДРПОУ:','')

	p3 = re.search(r'(?:А(?:КЦІОНЕРНО-КОМЕРЦІЙНИЙ БАНК|кціонерно-комерційний банк)|акціонерно-комерційний банк) (.*?\d{8})',
				p,re.U|re.I|re.S)
	if p3:
		return "АКБ " + p3.group(1).replace(' код ЄДРПОУ:','')

	p4 = re.search(r'(?:П(?:РИВАТНЕ АКЦІОНЕРНЕ ТОВАРИСТВО|риватне акціонерне товариство|риватне Акціонерне Товариство)|приватне акціонерне товариство) (.*?\d{8})',
				p,re.U|re.I|re.S)
	if p4:
		return "ПрАТ " + p4.group(1).replace(' код ЄДРПОУ:','')

	p5 = re.compile(r'(?:А(?:КЦІОНЕРНА КОМПАНІЯ З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ|кціонерна компанія з обмеженою відповідальністю)|акціонерна компанія з обмеженою відповідальністю)')
	if p5:
		return (p5.sub("АК з ОВ ",p))

	p6 = re.compile(r'(?:В(?:ІДКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО|ідкрите акціонерне товариство|ідкрите Акціонерне Товариство)|відкрите акціонерне товариство)')
	if p6:
		return (p6.sub("ВАТ ",p))

	p7 = re.compile(r'(?:З(?:АКРИТЕ АКЦІОНЕРНЕ ТОВАРИСТВО|акрите акціонерне товариство|акрите Акціонерне Товариство)|закрите акціонерне товариство)')
	if p7:
		return (p7.sub("ЗАТ ",p))

	p8 = re.compile(r'(?:Т(?:ОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ|овариство з обмеженою відповідальністю)|товариство з обмеженою відповідальністю)')
	if p8:
		return (p8.sub("TOB ",p))

	p9 = re.search(r'(?:А(?:КЦІОНЕРНИЙ БАНК|кціонерний банк|кціонерний Банк)|акціонерний банк) (.*?\d{8})',
				p,re.U|re.I|re.S)
	if p9:
		return "АБ " + p9.group(1).replace(' код ЄДРПОУ:','')

	p10 = re.compile(r'(?:А(?:КЦІОНЕРНИЙ БАНК|кціонерний банк|кціонерний Банк)|акціонерний банк)')
	if p10:
		return (p10.sub("АБ ",p))

	p11 = re.search(r'(?:П(?:риватне підприємство|риватне підприємство|риватне Підприємство)|приватне підприємство) (.*?\d{8})',
				p,re.U|re.I|re.S)
	if p11:
		return "ПП " + p11.group(1).replace(' код ЄДРПОУ:','')

	p12 = re.compile(r'(?:П(?:риватне підприємство|риватне підприємство|риватне Підприємство)|приватне підприємство)')
	if p12:
		return (p12.sub("ПП ",p))

	p13 = re.search(r'(?:К(?:омпанія з управління активами|омпанія з управління активами|омпанія З Управління Активами)|компанія з управління активами|КОМПАНІЯ З УПРАВЛІННЯ АКТИВАМИ) (.*?\d{8})',
				p,re.U|re.I|re.S)
	if p13:
		return "КУА " + p13.group(1).replace(' код ЄДРПОУ:','')

	p14 = re.compile(r'(?:К(?:омпанія з управління активами|омпанія з управління активами|омпанія З Управління Активами)|компанія з управління активами|КОМПАНІЯ З УПРАВЛІННЯ АКТИВАМИ)')
	if p14:
		return (p14.sub("КУА ",p))

	p15 = re.search(r'(?:ПАЙОВИЙ ЗАКРИТИЙ НЕДИВЕРСИФІКОВАНИЙ ВЕНЧУРНИЙ ІНВЕСТИЦІЙНИЙ ФОНД|пайовий закритий недиверсифікований венчурний інвестиційний фонд) (.*?\d{8})',
				p,re.U|re.I|re.S)
	if p15:
		return "ПЗНВІФ " + p15.group(1).replace(' код ЄДРПОУ:','')

	p16 = re.compile(r'(?:ПАЙОВИЙ ЗАКРИТИЙ НЕДИВЕРСИФІКОВАНИЙ ВЕНЧУРНИЙ ІНВЕСТИЦІЙНИЙ ФОНД|пайовий закритий недиверсифікований венчурний інвестиційний фонд)')
	if p16:
		return (p16.sub("ПЗНВІФ ",p))
	
	return p

def recieve_value(lst):

	"""applies a rule to the value and returns its string representation

	"""
	result = ""
	for elem in lst:
		elem = list(elem)
		if elem[0] != 'None' and elem[0] != '':
			elem[0] = elem[0].replace('\n',' ')
			for param in elem[1]:
				if param == 's':
					result = elem[0].split(',')[0]
				elif param == 'x':
					p = re.compile(r'(, (?:О|о)б\'єкт житлової нерухомості)(?:\: Ні|)')
					result += p.sub('',elem[0])
				elif param == 'r':
					p = re.compile(r'((?:З|з)агальна площа \(кв\.м\))|(((?:З|з)агальна площа))')
					result += p.sub('Заг.пл.',elem[0])
					p = re.compile(r'((?:Ж|ж)итлова площа \(кв\.м\))|(((?:Ж|ж)итлова(?:.*?)площа))')
					result = p.sub('Житл.пл.',result)
					p = re.compile(r'((?:З|з)агальна вартість нерухомого майна(?:.*)\(грн\))')
					result = p.sub('Вартість (грн)',result)
					p = re.compile(r'((?:Т|т)ехнічний опис майна: (?:К|к)ількість кімнат(?:| )(?:- |— |-|—))|((?:К|к)ількість кімнат (?:- |— |-|—))')
					result = p.sub('Кімнат: ',result)
					p = re.compile(r'((?:З|з)агальною площею)|(загальною площею)')
					result = p.sub('Заг.пл.:',result)
					p = re.compile(r'((?:Ж|ж)итловою площею)|((?:Ж|ж)итловою плоею)|(житловою площею)')
					result = p.sub('Житл.пл.:',result)
				elif param == 't':
					result += elem[0][:10]
				elif param == 'k':
					p = re.search(r'Іпотекодавець:(.*?)(?:|^.)(?:Іпотекодержатель|Майновий поручитель|Боржник за основним|Боржник|$)',
									elem[0],re.U|re.S)
					if p:
						result += shorten(p.group(1))
				elif param == 'd':
					p = re.search(r'(.*?)(?:, адреса:)',
									elem[0],re.U|re.S)
					if p:
						result += p.group(1)
					p = re.compile(r'((?:З|з)агальною площею)|(загальною площею)')
					result = p.sub('Заг.пл.:',result)
					p = re.compile(r'((?:Ж|ж)итловою площею)|((?:Ж|ж)итловою плоею)|(житловою площею)')
					result = p.sub('Житл.пл.:',result)
				elif param == 'a':
					result += REGISTRY4_1_8 + ": " + elem[0]
				elif param == 'z':
					result += REGISTRY4_1_10 + ": " + elem[0]
				elif param == 'p':
					result += REGISTRY4_1_9 + ": " + elem[0]
				elif param == 'b':
					result += REGISTRY4_1_13 + ": " + elem[0]
				elif param == 'f':
					#rule 'f' should goes last,to be processed as it needs to
					result += shorten(elem[0])
					return result
				elif param == 'q':
					p = re.search(r'Іпотекодержатель:(.*?)(?:|^.)(?:Іпотекодавець|Майновий поручитель|Боржник за основним|Боржник|$)',
									elem[0],re.U|re.S)
					if p:
						result += shorten(p.group(1))
				elif param == 'e':
					p = re.search(r'Майновий поручитель:(.*?)(?:|^.)(?:Іпотекодавець|Іпотекодержатель|Боржник за основним|Боржник|$)',
									elem[0],re.U|re.S)
					if p:
						result += shorten(p.group(1)) + DIV
					p = re.search(r'(Боржник.*?)(?:Майновий|Заявник|$)',elem[0],re.U|re.S)
					if p:
						p1 = re.compile(r'Т(?:ОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ|овариство з обмеженою відповідальністю)')
						tmp = p1.sub('ТОВ ',p.group(1))
						p1 = re.compile(r'(?!\d{8})(, адреса.*?)(?=Боржник|$)')
						tmp = p1.sub(' ',tmp)
						result += tmp
				elif param == 'h':
					p = re.match(r'(.*?),(?:| )серія та номер',elem[0],re.U|re.S)
					if p:
						result += p.group(1)
					else:
						result += elem[0]
				elif param == 'g':
					p = re.compile(r'(?:Г|г)рив(?:ня|ень)')
					result = p.sub('грн ',elem[0])
				elif param == 'w':
					p = re.compile(r'(?:С|с)трок виконання основного зобов’язання')
					result = p.sub('Строк виконання',elem[0])
				elif param == 'i':
					p = re.compile(r'правочин, в якому встановлено основне зобов’язання')
					result = p.sub('правочин',elem[0])
				elif param == 'c':
					p = re.search(r'(Боржник.*?)(?:Заявник|$)',elem[0],re.U|re.S)
					if p:
						p1 = re.compile(r'Т(?:ОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ|овариство з обмеженою відповідальністю)')
						tmp = p1.sub('ТОВ ',p.group(1))
						p1 = re.compile(r'(?!\d{8})(, адреса.*?)(?=Боржник|$)')
						tmp = p1.sub(' ',tmp)
						result += tmp
				elif param == 'y':
					p = re.search(r'Обтяжувач:(.*?)(?:|^.)(?:Особа, майно/права|Боржник|Боржник за основним|Особа, в інтересах|Опис предмета|$)',
									elem[0],re.U|re.S)
					if p:
						result += shorten(p.group(1))
				elif param == 'u':
					p = re.search(r'Особа, майно/права якої обтяжуються:(.*?)(?:|^.)(?:Обтяжувач|Боржник|Боржник за основним|Особа, в інтересах|Опис предмета|$)',
									elem[0],re.U|re.S)
					if p:
						result += shorten(p.group(1))
					p = re.compile(r'(Особа, майно/права якої обтяжуються: )')
					result = p.sub('',result)
				elif param == 'v':
					p = re.compile(r'(?:Іпотекодавець):(.*?)(?=Іпотекодержатель|Майновий поручитель|Особа|Боржник|Боржник за основним|Заявник|$)')
					tmp = p.sub('',elem[0])
					p = re.compile(r'(?:Іпотекодержатель):(.*?)(?=Іпотекодавець|Майновий поручитель|Особа|Боржник|Боржник за основним|Заявник|$)')
					tmp = p.sub('',tmp)
					p = re.compile(r'(?:Боржник|Боржник за основним зобов\’язанням):(.*?)(?=Іпотекодавець|Майновий поручитель|Особа|Іпотекодержатель|Заявник|$)')
					tmp = p.sub('',tmp)
					p = re.compile(r'(?:Майновий поручитель):(.*?)(?=Іпотекодавець|Іпотекодержатель|Особа|Боржник|Боржник за основним|Заявник|$)')
					result += p.sub('',tmp)
				elif param == 'j':
					p = re.compile(r'(?:Обтяжувач):(.*?)(?=Особа|Боржник|Боржник за основним|Заявник|$)')
					tmp = p.sub('',elem[0])
					p = re.compile(r'(?:Боржник|Боржник за основним зобов\’язанням):(.*?)(?=Обтяжувач|Особа|Заявник|$)')
					tmp = p.sub('',tmp)
					p = re.compile(r'(?:Особа, майно/права якої обтяжуються):(.*?)(?=Особа|Обтяжувач|Боржник за основним|Боржник|Заявник|$)')
					result += p.sub('',tmp)
				else:
					result += elem[0]
				elem[0] = result
			result += '' if not result.strip(' ') else DIV
	return result.strip().strip(DIV)

def first_part(text):
	#first level separation
	data = separate(text,GROUP_ALL) 
	#gets params of qwerty
	data[FETCH_PARAMS] = separate(data[FETCH_PARAMS],GROUP_OBJECT)
	#gets all possible records for each group in 'data' dictionary
	groups = [(REGISTRY1,GROUP_OBJECT1),(REGISTRY2,GROUP_OBJECT2),
			  (REGISTRY3,GROUP_OBJECT3),(REGISTRY4,GROUP_OBJECT4)
	]
	for group in groups:
		data[group[0]] = first_lvl_extraction(data[group[0]],group[1])
	#first level extractions for each group in 'data' dictionary
	dic = {
		REGISTRY1: [GROUP_REG1,[(REGISTRY1_1,GROUP_REG1_1),(REGISTRY1_2,GROUP_REG1_2),
				    (REGISTRY1_3,GROUP_REG1_3),(REGISTRY1_4,GROUP_REG1_4)]],
		REGISTRY2: [GROUP_REG2,[(REGISTRY2_1,GROUP_REG2_1),(REGISTRY2_2,GROUP_REG2_2)]],
		REGISTRY3: [GROUP_REG3,[(REGISTRY3_1,GROUP_REG3_1),(REGISTRY3_2,GROUP_REG3_2)]],
		REGISTRY4: [GROUP_REG4,[(REGISTRY4_1,GROUP_REG4_1),(REGISTRY4_2,GROUP_REG4_2)]],
	}
	for key in dic.keys():
		for i in range(len(data[key])):
			data[key][i] = second_lvl_extraction(data[key][i],dic[key][0]) 
			groups = dic[key][1]
			for group in groups:
				#special fields that need preprocess extractions
				if group[0] == REGISTRY2_2:
					data[key][i][group[0]] = \
						first_lvl_extraction(data[key][i][group[0]][0],
												GROUP_OBJECT2_2)	
			
				if group[0] == REGISTRY4_2 and key == REGISTRY4:
					if data[key][i][group[0]]:
						data[key][i][group[0]] = \
						first_lvl_extraction(data[key][i][group[0]][0],
												GROUP_OBJECT4_2)
				if group[0] == REGISTRY4_1 and key == REGISTRY4:
					if data[key][i][group[0]]:
						data[key][i][group[0]] = \
						first_lvl_extraction(data[key][i][group[0]][0],
												GROUP_OBJECT4_1)
				if group[0] == REGISTRY3_2 and key == REGISTRY3:
					if data[key][i][group[0]]:
						data[key][i][group[0]] = \
						first_lvl_extraction(data[key][i][group[0]][0],
												GROUP_OBJECT3_2)
				if group[0] == REGISTRY3_1 and key == REGISTRY3:
					if data[key][i][group[0]]:
						data[key][i][group[0]] = \
						first_lvl_extraction(data[key][i][group[0]][0],
												GROUP_OBJECT3_1)


				####
				for y in range(len(data[key][i][group[0]])):
					data[key][i][group[0]][y] = \
					separate(data[key][i][group[0]][y],group[1])
	return data

def second_part(check):
	#second part 
	#first table
	check1 = [[],[]]
	for i in range(len(check[REGISTRY1])):
		for y in range(len(check[REGISTRY1][i][REGISTRY1_2])):
			dic = {}
			dic['Параметри запиту'] = \
					check[REGISTRY1][i][REGISTRY1_1][0][REGISTRY1_1_6].replace('\n',' ')
			#a dictionary of lists of tuples containing fields of record and rule to process those strings
			fields = {
					'Характеристики нерухомості': [(check[REGISTRY1][i][REGISTRY1_1][0][REGISTRY1_1_2],'x'),
													 (check[REGISTRY1][i][REGISTRY1_1][0][REGISTRY1_1_3],'r'),
													 (check[REGISTRY1][i][REGISTRY1_1][0][REGISTRY1_1_5],'o'),
													 (check[REGISTRY1][i][REGISTRY1_1][0][REGISTRY1_1_7],'o'),
													 (check[REGISTRY1][i][REGISTRY1_2][y][REGISTRY1_2_10],'o')],
					'Дата регистрации': [(check[REGISTRY1][i][REGISTRY1_2][y][REGISTRY1_2_2],'t'),],
					'Підстава власності': [(check[REGISTRY1][i][REGISTRY1_2][y][REGISTRY1_2_4],'h'),],
					'Форма власності': [(check[REGISTRY1][i][REGISTRY1_2][y][REGISTRY1_2_6],'o'),],
					'Частка': [(check[REGISTRY1][i][REGISTRY1_2][y][REGISTRY1_2_7],'o'),],
					'Власник': [(check[REGISTRY1][i][REGISTRY1_2][y][REGISTRY1_2_8],'f'),],
			}
			for key in fields:
				dic[key] = recieve_value(fields[key])
			check1[0].append(dic)
	if check[REGISTRY2]:
		for i in range(len(check[REGISTRY2])):
			for y in range(len(check[REGISTRY2][i][REGISTRY2_2])):
				dic = {}
				dic['Параметри запиту'] = \
					check[REGISTRY2][i][REGISTRY2_1][0][REGISTRY2_1_3].replace('\n',' ')
				fields = {
						'Характеристики нерухомості': [(check[REGISTRY2][i][REGISTRY2_1][0][REGISTRY2_1_2],'o'),
					 								   (check[REGISTRY2][i][REGISTRY2_1][0][REGISTRY2_1_4],'r'),],
						'Дата регистрации': [(check[REGISTRY2][i][REGISTRY2_2][y][REGISTRY2_2_1],'o'),],
						'Підстава власності': [(check[REGISTRY2][i][REGISTRY2_2][y][REGISTRY2_2_6],'hs'),],
						'Форма власності': [(check[REGISTRY2][i][REGISTRY2_2][y][REGISTRY2_2_4],'o'),],
						'Частка': [(check[REGISTRY2][i][REGISTRY2_2][y][REGISTRY2_2_5],'o'),],
						'Власник': [(check[REGISTRY2][i][REGISTRY2_2][y][REGISTRY2_2_3],'f'),],
				}
				for key in fields:
					dic[key] = recieve_value(fields[key])
				check1[0].append(dic)
	#second table
	for i in range(len(check[REGISTRY1])):
		for y in range(len(check[REGISTRY1][i][REGISTRY1_3])):
			dic = {}
			dic['Параметри запиту'] = \
					check[REGISTRY1][i][REGISTRY1_1][0][REGISTRY1_1_6].replace('\n',' ')
			fields = {
					'Дата регистрации': [(check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_2],'t'),],
					'Причина обтяження': [(check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_4],'h'),],
					'Деталі': [(check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_6],'hgwi'),
							   (check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_8],'r'),
							   (check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_9],'m'),],
					"Суб'єкти обтяження": [(check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_7],'v'),],
					'Заявник': [(check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_7],'q'),],
					'Власник': [(check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_7],'k'),],
					'Поручитель': [(check[REGISTRY1][i][REGISTRY1_3][y][REGISTRY1_3_7],'e'),],
			}
			for key in fields:
				dic[key] = recieve_value(fields[key])
			check1[1].append(dic)

		for y in range(len(check[REGISTRY1][i][REGISTRY1_4])): 
			dic = {}
			dic['Параметри запиту'] = \
					check[REGISTRY1][i][REGISTRY1_1][0][REGISTRY1_1_6].replace('\n',' ')
			fields = {
					'Дата регистрации': [(check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_2],'t'),],
					'Причина обтяження': [(check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_4],'h'),],
					'Деталі': [(check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_6],'h'),
							   (check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_9],'r'),
							   (check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_10],'l'),],
					"Суб'єкти обтяження": [(check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_7],'j'),],
					'Заявник': [(check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_7],'y'),],
					'Власник': [(check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_7],'u'),],
					'Поручитель': [(check[REGISTRY1][i][REGISTRY1_4][y][REGISTRY1_4_7],'c'),],
			}
			for key in fields:
				dic[key] = recieve_value(fields[key])
			check1[1].append(dic)
	if check[REGISTRY3]:
		for i in range(len(check[REGISTRY3])):
			for y in range(len(check[REGISTRY3][i][REGISTRY3_2])):
				dic = {}
				dic['Параметри запиту'] = ''
				fields = {
						'Дата регистрации': [(check[REGISTRY3][i][REGISTRY3_2][y][REGISTRY3_2_3],'t'),],
						'Причина обтяження': [(check[REGISTRY3][i][REGISTRY3_2][y][REGISTRY3_2_4],'h'),],
						'Деталі': [(check[REGISTRY3][i][REGISTRY3_2][y][REGISTRY3_2_5],'d'),
								   (check[REGISTRY3][i][REGISTRY3_2][y][REGISTRY3_2_1],'o'),],
						"Суб'єкти обтяження": [('','o'),],
						'Заявник': [(check[REGISTRY3][i][REGISTRY3_2][y][REGISTRY3_2_7],'f'),],
						'Власник': [(check[REGISTRY3][i][REGISTRY3_2][y][REGISTRY3_2_6],'f'),],
						'Поручитель': [('','o'),],
				}
				for key in fields:
					dic[key] = recieve_value(fields[key])
				check1[1].append(dic)
		for i in range(len(check[REGISTRY3])):
			for y in range(len(check[REGISTRY3][i][REGISTRY3_1])):
				dic = {}
				dic['Параметри запиту'] = ''
				fields = {
						'Дата регистрации': [(check[REGISTRY3][i][REGISTRY3_1][y][REGISTRY3_1_2],'t'),],
						'Причина обтяження': [('','o'),],
						'Деталі': [(check[REGISTRY3][i][REGISTRY3_1][y][REGISTRY3_1_3],'o'),],
						"Суб'єкти обтяження": [('','o'),],
						'Заявник': [('','o'),],
						'Власник': [('','o'),],
						'Поручитель': [('','o'),],
				}
				for key in fields:
					dic[key] = recieve_value(fields[key])
				check1[1].append(dic)

	if check[REGISTRY4]:
		for i in range(len(check[REGISTRY4])):
			for y in range(len(check[REGISTRY4][i][REGISTRY4_1])):
				dic = {}
				dic['Параметри запиту'] = ''
				fields = {
						'Дата регистрации': [(check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_3],'t'),],
						'Причина обтяження': [(check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_4],'h'),],
						'Деталі': [(check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_5],'d'),
								   (check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_2],'o'),
								   (check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_8],'ag'),
								   (check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_10],'z'),
								   (check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_9],'p'),
								   (check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_11],'o'),],		   
						"Суб'єкти обтяження": [('','o'),],
						'Заявник': [(check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_6],'f'),],
						'Власник': [(check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_7],'f'),],
						'Поручитель': [(check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_12],'o'),
									   (check[REGISTRY4][i][REGISTRY4_1][y][REGISTRY4_1_13],'b'),],
				}
				for key in fields:
					dic[key] = recieve_value(fields[key])
				check1[1].append(dic)
		for i in range(len(check[REGISTRY4])):
			for y in range(len(check[REGISTRY4][i][REGISTRY4_2])):
				dic = {}
				dic['Параметри запиту'] = ''
				fields = {
						'Дата регистрации': [(check[REGISTRY4][i][REGISTRY4_2][y][REGISTRY4_2_2],'t'),],
						'Причина обтяження': [('','o'),],
						'Деталі': [(check[REGISTRY4][i][REGISTRY4_2][y][REGISTRY4_2_3],'o'),],
						"Суб'єкти обтяження": [('','o'),],
						'Заявник': [('','o'),],
						'Власник': [('','o'),],
						'Поручитель': [('','o'),],
				}
				for key in fields:
					dic[key] = recieve_value(fields[key])
				check1[1].append(dic)
	return check1

def convert_one(fname):
	output_file = tempfile.mktemp(prefix="yes_i_know_you_deprecated")

	"""
	pdftotext - is installed poppler-utils package for PDF to text conversion;

	keys:
		-raw   Keep the text in content stream order;
		-nopgbrk  Don’t insert page breaks between  pages.
	""" 
	os.system('pdftotext -raw -nopgbrk "{0}" "{1}"'.format(
		fname, output_file))

	with open(output_file, 'rb') as f:
		# converted text from pdf file
		text = f.read().decode('utf-8')

	os.unlink(output_file)

	# deletes junk
	text = re.sub(r'стор. \d{1,3} з \d{1,3}|(?:RRP|REP)-.*?\n|  ', '' ,text) 

	check = first_part(text)
	check1 = second_part(check)

	return check1, fname


def convert_many(infile):
	to_export = convert_one(infile)
	output_file = BytesIO()

	workbook = xlsxwriter.Workbook(output_file, {'in_memory': True})
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': True})

	worksheet.write_row(0, 0, [
		u'Назва файлу',
		u'Параметри запиту',
		u'Дата регистрации',
		u'Власник',
		u'Характеристики нерухомості',
		u'Підстава власності',
		u'Форма власності',
		u'Частка',
		u'Дата обтяження',
		u'Причина обтяження',
		u'Деталі',
		u'Заявник/Обтяжувач/Іпотекодержатель',
		u'Власник/Іпотекодавець',
		u'Поручитель/Боржник',
		u"Iншi суб'єкти обтяження",], bold
	)

	row = 1

	check1,fname = to_export[0],to_export[1]
	for item in check1[0]:
		worksheet.write(row,0, fname.rsplit('/')[-1])
		worksheet.write(row,1, item['Параметри запиту'])
		names = ['Дата регистрации','Власник',
			 'Характеристики нерухомості','Підстава власності',
			 'Форма власності','Частка',
		]
		worksheet.write_row(
			row, 2,
			map(lambda x: item[x], names))
		row += 1

	for item in check1[1]:
		worksheet.write(row, 0, fname.rsplit('/')[-1])
		worksheet.write(row, 1, item['Параметри запиту'])
		names = ['Дата регистрации','Причина обтяження','Деталі',
			 'Заявник','Власник','Поручитель',"Суб'єкти обтяження",
		]
		worksheet.write_row(
			row, 8,
			map(lambda x: item[x], names))
		row += 1


	workbook.close()
	output_file.seek(0)
	return output_file

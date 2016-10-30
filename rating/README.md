Есть два скрипта:

1. convert_csv_to_json.py    -  принимает csv таблицу с какими-нибудь результатами и json список со всеми студентами. Создаёт json с описанием баллов каждого студента в формате для следующего скрипта
2. build_table.py    -  принимает config результирующей таблицы, включающий в себя описание полей и веса для итоговых баллов по каждому направлению. Также принимает папку с json-ами результатов работ в определённом формате (например папка students_tasks). Создаёт git markdown file.

Использование первого шага необязательно для второго шага, нужные json-ы можно руками создавать.

У скриптов есть параметр -h для показа небольшой подсказки по параметрам.

Примеры использования (нужные файлы уже есть в текущей папке):

1. python convert_csv_to_json.py --all-students all_students.json --input industry_hw0/industry_hw0.csv --output industry_hw0.json
2. python build_table.py --students students_tasks/ --config rating_config.json --output table.md

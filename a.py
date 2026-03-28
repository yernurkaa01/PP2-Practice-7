import psycopg2  # модуль для работы с PostgreSQL
import csv       # модуль для чтения CSV файлов

conn = psycopg2.connect(  # подключаемся к базе данных
    "postgresql://neondb_owner:npg_KD85rTMSdqAk@ep-old-mode-am43uefr-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

cur = conn.cursor()  # создаём курсор для выполнения SQL-запросов

print("\n--- PHONEBOOK MENU ---")  # меню
print("1. Add from console")
print("2. Add from CSV")
print("3. Update phone")
print("4. Delete user")
print("5. Show all")

choice = input("Choose option (1-5): ")  # выбор пользователя

# 1️⃣ INSERT
if choice == "1":
    name = input("Enter name: ")   # ввод имени
    phone = input("Enter phone: ") # ввод телефона
    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",  # SQL запрос
        (name, phone)  # значения подставляются безопасно
    )
    print("✅ Added!")

# 2️⃣ CSV
elif choice == "2":
    try:
        with open("data.csv") as f:  # открываем CSV файл
            reader = csv.reader(f)   # читаем построчно
            for row in reader:       # перебираем строки
                cur.execute(
                    "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                    row  # вставляем данные из CSV
                )
        print("✅ CSV inserted!")
    except FileNotFoundError:  # если файла нет
        print("❌ data.csv not found")

# 3️⃣ UPDATE
elif choice == "3":
    name = input("Enter name to update: ")   # имя для поиска
    new_phone = input("Enter new phone: ")  # новый номер
    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE username=%s",  # обновление
        (new_phone, name)
    )
    print("✅ Updated!")

# 4️⃣ DELETE
elif choice == "4":
    name = input("Enter name to delete: ")  # имя для удаления
    cur.execute(
        "DELETE FROM phonebook WHERE username=%s",  # удаление
        (name,)  # кортеж из одного элемента
    )
    print("✅ Deleted!")

# 5️⃣ SELECT
elif choice == "5":
    cur.execute("SELECT * FROM phonebook")  # получаем все записи
    rows = cur.fetchall()  # забираем результат
    print("\n📋 PhoneBook:")
    for row in rows:  # выводим каждую строку
        print(row)

else:
    print("❌ Invalid choice")  # если неправильный ввод

conn.commit()  # сохраняем изменения в базе
conn.close()   # закрываем соединение
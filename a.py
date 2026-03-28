import psycopg2
import csv

conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_KD85rTMSdqAk@ep-old-mode-am43uefr-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

cur = conn.cursor()

print("\n--- PHONEBOOK MENU ---")
print("1. Add from console")
print("2. Add from CSV")
print("3. Update phone")
print("4. Delete user")
print("5. Show all")

choice = input("Choose option (1-5): ")

# 1️⃣ INSERT
if choice == "1":
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
        (name, phone)
    )
    print("✅ Added!")

# 2️⃣ CSV
elif choice == "2":
    try:
        with open("data.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                    row
                )
        print("✅ CSV inserted!")
    except FileNotFoundError:
        print("❌ data.csv not found")

# 3️⃣ UPDATE
elif choice == "3":
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")
    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE username=%s",
        (new_phone, name)
    )
    print("✅ Updated!")

# 4️⃣ DELETE
elif choice == "4":
    name = input("Enter name to delete: ")
    cur.execute(
        "DELETE FROM phonebook WHERE username=%s",
        (name,)
    )
    print("✅ Deleted!")

# 5️⃣ SELECT
elif choice == "5":
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    print("\n📋 PhoneBook:")
    for row in rows:
        print(row)

else:
    print("❌ Invalid choice")

conn.commit()
conn.close()
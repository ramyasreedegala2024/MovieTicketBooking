import mysql.connector

for port in [3306, 3307]:
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=port,
            user="root",
            password="YOUR_PASSWORD"  # replace with what you think it is
        )

        print(f"Connected on port {port}")

        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")

        print("Databases:")
        for db in cursor.fetchall():
            print(db)

        conn.close()

    except Exception as e:
        print(f"Port {port} -> {e}")
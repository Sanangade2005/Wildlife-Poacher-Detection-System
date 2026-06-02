import psycopg2

def test_connection(password):
    try:
        conn = psycopg2.connect(
            dbname="poacher_db",
            user="postgres",
            password=password,
            host="127.0.0.1",
            port="5432"
        )
        print(f"SUCCESS: Connected with password '{password}'")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED: Could not connect with password '{password}'. Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing 'bala1234'...")
    if test_connection("bala1234"):
        exit(0)
        
    print("\nTesting 'bala123' (User mentioned this first)...")
    if test_connection("bala123"):
        exit(0)
        
    print("\nAll attempts failed.")

import os
import shutil
import subprocess

# Your apps
APPS = ['accounts', 'products', 'orders', 'dashboard']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def delete_migrations():
    print("\n🔹 Deleting migration files...")
    for app in APPS:
        path = os.path.join(BASE_DIR, app, 'migrations')

        if os.path.exists(path):
            for file in os.listdir(path):
                file_path = os.path.join(path, file)

                if file == '__init__.py':
                    continue

                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted folder: {file_path}")


def delete_pycache():
    print("\n🔹 Deleting __pycache__...")
    for root, dirs, files in os.walk(BASE_DIR):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))


def run(cmd):
    print(f"\n⚙️ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("❌ Failed")
        exit()


def migrate_in_order():
    print("\n🔹 Running migrations in correct order...")

    # Core Django
    run("python manage.py migrate contenttypes")
    run("python manage.py migrate auth")

    # 🔥 Your custom user FIRST
    run("python manage.py makemigrations accounts")
    run("python manage.py migrate accounts")

    # Django admin AFTER user
    run("python manage.py migrate admin")

    # Other apps
    run("python manage.py makemigrations products")
    run("python manage.py migrate products")

    run("python manage.py makemigrations orders")
    run("python manage.py migrate orders")

    run("python manage.py makemigrations dashboard")
    run("python manage.py migrate dashboard")

    # Final sync
    run("python manage.py migrate")


def main():
    delete_migrations()
    delete_pycache()
    migrate_in_order()

    print("\n✅ Project reset & migrated successfully!")


if __name__ == "__main__":
    main()
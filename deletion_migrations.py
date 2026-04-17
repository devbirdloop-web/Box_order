import os
import shutil

# Add your apps here
APPS = ['accounts', 'orders', 'products', 'dashboard']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def delete_migration_files():
    print("\n🔹 Deleting migration files...")
    for app in APPS:
        migrations_path = os.path.join(BASE_DIR, app, 'migrations')

        if os.path.exists(migrations_path):
            for file in os.listdir(migrations_path):
                file_path = os.path.join(migrations_path, file)

                if file == '__init__.py':
                    continue

                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"Deleted folder: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


def delete_pycache(base_path):
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted __pycache__: {dir_path}")
                except Exception as e:
                    print(f"Error deleting {dir_path}: {e}")


def delete_pyc_files(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted .pyc file: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


def clean_project():
    delete_migration_files()
    print("\n🔹 Deleting __pycache__ folders...")
    delete_pycache(BASE_DIR)

    print("\n🔹 Deleting .pyc files...")
    delete_pyc_files(BASE_DIR)

    print("\n✅ Project cleaned successfully!")


if __name__ == "__main__":
    clean_project()
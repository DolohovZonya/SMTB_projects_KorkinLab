import pandas as pd
import csv

def process_files():
    try:
        df1 = pd.read_csv('repeats_in_scope_2.07_no_dup.csv')
        print("Первый файл успешно прочитан")
    except FileNotFoundError:
        print("Ошибка: Первый файл не найден")
        return
    except Exception as e:
        print(f"Ошибка при чтении первого файла: {e}")
        return

    try:
        df2 = pd.read_csv('proteins_from_repeats_db.csv')
        print("Второй файл успешно прочитан")
    except FileNotFoundError:
        print("Ошибка: Второй файл не найден")
        return
    except Exception as e:
        print(f"Ошибка при чтении второго файла: {e}")
        return

    pdb_ids = df2.iloc[:, 1].unique()
    print(f"Найдено {len(pdb_ids)} уникальных PDB ID")

    sf_dict = {}
    for _, row in df1.iterrows():
        pdb_id = row['pdb_id']
        sf_value = row['sf']
        
        # Извлекаем только числовую часть из SF=48670
        if isinstance(sf_value, str) and 'SF=' in sf_value:
            sf_number = sf_value.split('SF=')[1]
            sf_dict[pdb_id] = sf_number


    sf_values = set()
    
    for pdb_id in pdb_ids:
        if pdb_id in sf_dict:
            sf_values.add(sf_dict[pdb_id])
            print(f"Для {pdb_id} найден SF: {sf_dict[pdb_id]}")
        else:
            print(f"Для {pdb_id} SF значение не найдено")


    try:
        with open('sf_values.txt', 'w') as f:
            for sf_value in sorted(sf_values):
                f.write(f"{sf_value}\n")
        print(f"Успешно записано {len(sf_values)} уникальных SF значений в файл sf_values.txt")
        
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

if __name__ == "__main__":
    process_files()
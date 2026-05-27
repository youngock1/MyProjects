import sqlite3
import json


def to_dict(all_tasks, completed, deleted) -> dict:
	data = {
		'all': all_tasks,
		'completed': completed,
		'deleted': deleted
	}
	return data 


def save_to_file(data) -> bool:
	# Запись данных  в файл в формате JSON
	try:
		with open("data/tasks.json", "w", encoding="utf-8") as file:
			json.dump(data, file, indent=4, ensure_ascii=False)
			print("Данные успешно записаны.")
			return True
	except Exception as error:
		print(f"Произошла ошибка: {error}.")
		return False


def get_data_from_file() -> set:
	try:
		with open("data/tasks.json", "r", encoding="utf-8") as file:
			# Загружаем данные из файла
			data = json.load(file)

		return (data['all'], data['completed'], data['deleted']) if data else None
	except Exception as error:
		print(f"Произошла ошибка: {error}.")
		return None



class Database_Tasks:

	def __init__(self) -> None:
		self.connection = sqlite3.Connection('data/task.db')
		self.cursor = self.connection.cursor()

		if not get_data_from_file():
			data = to_dict(0, 0, 0)
			save_to_file(data)





	def create_table(self) -> bool:
		try:
			self.cursor.execute("""
					CREATE TABLE IF NOT EXISTS tasks (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						name TEXT,
						desscriiption TEXT,
						deadline TEXT
						)
				""")
			print("Таблица создана.")
			return True 
		except Exception as error:
			print(f"Произошла ошибка: {error}.")

		return False


	def create_task(self, name, description, deadline) -> bool:
		try:
			self.cursor.execute("INSERT INTO tasks (name, desscriiption, deadline) VALUES (?, ?, ?)",
							(name, description, deadline))
			self.connection.commit()

			return True
		except Exception as error:
			print(f"Произошла ошибка: {error}.")

		return False


	def read_task(self, task_id) -> set:
		try:
			task = self.cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
			return task
		except Exception as error:
			print(f"Произошла ошибка: {error}.")

		return ()


	def update_task(self, task_id, name, description, deadline) -> bool:
		try:
			self.cursor.execute("UPDATE tasks SET name = (?) WHERE id= (?)", (name, task_id))
			self.cursor.execute("UPDATE tasks SET desscriiption = (?) WHERE id= (?)", (description, task_id))
			self.cursor.execute("UPDATE tasks SET deadline = (?) WHERE id= (?)", (deadline, task_id))
			self.connection.commit()
			return True 

		except Exception as error:
			print(f"Произошла ошибка: {error}.")

		return False


	def delete_task(self, task_id) -> bool:
		try:
			self.cursor.execute("DELETE FROM tasks WHERE id = (?)",
								(task_id,))
			self.connection.commit()
			data = get_data_from_file()
			new_data = to_dict(data[0], data[1], data[2]+1)
			save_to_file(new_data)
			return True
		except Exception as error:
			print(f"Произошла ошибка: {error}.")

		return False


	def check_deadlines(self) -> None:
		try:
			time_task_list = self.cursor.execute("SELECT deadlines FROM tasks").fetchall()
			time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
			for time_task in time_task_list:
				print(f'Просрочена: {time_task}' if time_now > time_task[0] else f'Время ещё есть: {time_task}')
		except Exception as error:
			print(f"Произошла ошибка: {error}.")


	def complete_task(self, task_id) -> bool:
		try:
			self.cursor.execute("DELETE FROM tasks WHERE id = (?)",
								(task_id,))
			self.connection.commit()
			data = get_data_from_file()
			new_data = to_dict(data[0], data[1]+1, data[2])
			save_to_file(new_data)
		except Exception as error:
			print(f"Произошла ошибка: {error}.")
			return False


	def save_all_tasks(self) -> None:
		try:
			all_tasks = len(self.cursor.execute("SELECT * FROM tasks").fetchall())
			data = get_data_from_file()
			new_data = to_dict(all_tasks+data[1]+data[2], data[1], data[2])
			save_to_file(new_data)
		except Exception as error:
			print(f"Произошла ошибка: {error}.")


	def get_all_tasks(self) -> list:
		try:
			tasks = self.cursor.execute("SELECT * FROM tasks").fetchall()

			return tasks
		except Exception as error:
			print(f"Произошла ошибка: {error}.")


def main_loop():
	tasker = Database_Tasks()
	tasker.create_table()
	tasker.save_all_tasks()

	command = input("Введите команду:\t").lower().split()
	try:

		while command[0] != 'exit':

			if command[0] == 'add':
				name = input("Введите название:\t").lower().strip()
				description = input("Введите описание:\t").lower().strip()
				deadline = input("Введите дедлайн:(Ex: 01-01-2020 15:00)\t").lower().strip()
				if not name or not deadline or not deadline:
					print(f"Данных не хватает. :(")
				if tasker.create_task(name, description, deadline):
					print("Задача успешно добавлена.")
					tasker.save_all_tasks()
			elif command[0] == 'read':
				task_id = input("Введите ID задачи:\t").lower().strip()
				if not task_id:
					print("Данных не хватает. :(")
				print(tasker.read_task(task_id))
			elif command[0] == 'update':
				name = input("Введите название:\t").lower().strip()
				description = input("Введите описание:\t").lower().strip()
				deadline = input("Введите дедлайн:(Ex: 01-01-2020 15:00)\t").lower().strip()
				task_id = cinput("Введите ID задачи:\t").lower().strip()
				if not name or not description or not deadline or not task_id:
					print("Данных не хватает. :(") 
				if tasker.update_task(task_id, name, description, deadline):
					print("Задача успешно обновлена.")
			elif command[0] == 'delete':
				task_id = input("Введите ID задачи:\t").lower().strip()
				if not task_id:
					print("Данных не хватает. :(")
				if tasker.delete_task(task_id):
					print("Задача успешно удалена.")
			elif command[0] == 'complete':
				task_id = input("Введите ID задачи:\t").lower().strip()
				if not task_id:
					print("Данных не хватает. :(")
				if tasker.complete_task(task_id):
					print("Задача успешно выполнена.")
			elif command[0] == 'stats':
				data = get_data_from_file()
				print(f"Всего задач:     {data[0]} шт.\n"
					  f"Выполнено задач: {data[1]} шт.\n"
					  f"Удалено задач:   {data[2]} шт.")
			elif command[0] == 'all':
				data = tasker.get_all_tasks()
				if data:
					for task in data:
						print(f"ID: {task[0]}\tName: {task[1]}")
				else:
					print("Текущих задач нет.")

			command = input("Введите команду:\t").lower().split()
	except Exception as error:
		print(f"Произошла ошибка: {error}.")


if __name__ == '__main__':
	main_loop()
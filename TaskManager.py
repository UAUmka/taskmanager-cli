import json
import os
from colorama import Fore, Back, Style
from datetime import datetime


def task_load():
	if os.path.exists("task.json"):
		with open("task.json", "r", encoding = "utf-8") as f:
			return json.load(f)

def task_save(data):
	with open("task.json", "w", encoding = "utf-8") as f:
		json.dump(data, f, indent = 2, ensure_ascii = False)

class TaskManager:
	def __init__(self):
		self.commands = {
			"menu": [
				f"[1] Переглянути завдання",
				f"[2] Додати завдання",
				f"[3] Редагувати завдання",
				f"[4] Позначити як виконане",
				f"[5] Фільтрація",
				f"[6] Пошук по ключовому слову",
				f"[7] {Fore.CYAN}Експорт у .txt{Style.RESET_ALL}",
				f"[8] {Fore.RED}Видалення завдань{Style.RESET_ALL}",
				f"[0] Вийти"
			],
			"command": {
				"1": self.task_view,
				"2": self.tasks_add,
				"3": self.task_edit,
				"4": self.mark_done,
				"5": self.task_sorting,
				"6": self.task_search,
				"7": self.export_to_txt,
				"8": self.task_delete,
				"0": self.quit
			}
		}
		self.tasks = task_load() or []

	def no_task(self):
		if not self.tasks:
			print("\nСписок порожний!\n")
			return

	def task_lists(self):
		result = [self.format_task(task, i) for i, task in enumerate(self.tasks, start = 1)]
		return "\n".join(result)

	def format_task(self, task, index):
		status = "✅" if task['done'] else ""
		color = Fore.RED if task['priority'] == "high" else Fore.CYAN
		return f"{status} {color}{index}. [{task['data']}] {task['title']}{Style.RESET_ALL}"

	def priority_task(self, priority):
		priorities = {'1': "high", '2': "medium"}
		return priorities.get(priority, None)

	def number_task(self, index):
		if index.isdigit():
			i = int(index) - 1
			len_task = (0 <= i < len(self.tasks))
		else:
			print("\n❌ Введіть число.\n")
		return i, len_task

	def task_view(self):
		print(
			f"\nПриоритет завдань: [{Fore.RED}Важливі{Style.RESET_ALL}], [{Fore.CYAN}Меньш важливі{Style.RESET_ALL}]\n"
			"Виконані завдання: ✅\n"
		)
		self.no_task()
		lists = self.task_lists()
		print(lists)

	def tasks_add(self):
		while True:
			add = input("Завдання: ")
			setting = input("Оберить приоритет: [1] високий, [2] середній: ")

			priority = self.priority_task(setting)
			data = datetime.now().strftime("%d.%m.%Y %H:%M")

			self.tasks.append({"title": add, "priority": priority, "done": False, "data": data})
			task_save(self.tasks)

			quit = input("Хочете додати ще завдання? [1] так, [0] ні: ")
			if quit == '0':
				break

	def task_edit(self):
		self.no_task()
		self.task_view()
		index = input("Введіть номер завдання, яке відредагувати: ")
		i, len_task = self.number_task(index)

		if len_task:
			title_edit = input("Введіть новий текаст: ")
			self.tasks[i]['title'] = title_edit
			task_save(self.tasks)
			print(f"\n✅ Завдання відредаговано.")
		else:
			print("\n❌ Невірний номер.")

	def mark_done(self):
		self.task_view()
		index = input("Введіть номер завдання, яке виконано: ")
		i, len_task = self.number_task(index)

		if len_task:
			self.tasks[i]['done'] = True
			task_save(self.tasks)
			print(f"\n✅ Завдання '{self.tasks[i]['title']}' позначено як виконане.")
		else:
			print("\n❌ Невірний номер.")

	def task_sorting(self):
		self.no_task()
		sort_in = input("[1] Сортувати по приоритету, [2] Сортувати по виконаному/не виконаному: ")
		sorted_task = []
		if sort_in == '1':
			choice = input("Сортувати по приоритету: [1] високий, [2] середній: ")
			priority = self.priority_task(choice)
			sorted_task = [task for task in self.tasks if task['priority'] == priority]
		elif sort_in == '2':
			choice = input("Сортувати по: [1] виконано, [2] не виконано: ")
			done = choice == '1'
			sorted_task = [task for task in self.tasks if task['done'] == done]
		else:
			print("\n❌ Невірний номер.")

		print(f"\n🔎 Знайдено {len(sorted_task)} завдань:")
		for i, task in enumerate(sorted_task, start = 1):
			print(self.format_task(task, i))

	def task_search(self):
		self.no_task()
		key = input("Введіть ключове слово для пошуку: ").lower()
		found = [task for task in self.tasks if key in task['title'].lower()]

		if found:
			print("\n🔎 Знайдено {len(found)} завдань:")
			for i, task in enumerate(found, start = 1):
				print(self.format_task(task, i))
		else:
			print("\n❌ Нічого не знайдено.")

	def export_to_txt(self):
		filename = input("Введіть назву файлу (без розширення): ") + ".txt"
		with open(filename, "w", encoding = "utf-8") as f:
			for i, task in enumerate(self.tasks, start = 1):
				priority = "високий" if task['priority'] == "high" else "середній"
				status = "Виконано" if task['done'] else "Не виконано"
				f.write(f"{i}. [{task['data']}] {task['title']} | Пріоритет: {priority} | Статус: {status}\n")
			print(f"\n📁 Завдання експортовано у файл: {filename}")

	def task_delete(self):
		self.no_task()
		self.task_view()
		index = input("Введіть номер завдання, яке потрібно видалити: ")
		i, len_task = self.number_task(index)

		if len_task:
			delete = input("Підтвердити видаленя? [1] так, [0] ні: ")
			if delete == '1':
				del self.tasks[i]
				task_save(self.tasks)
				print("\n❌ Завдання видалено.")
		else:
			print("\n❌ Невірний номер.")

	def quit(self):
		exit(0)

	def run(self):
		if self.tasks:
			self.task_view()

		while True:
			for menu in self.commands['menu']:
				print(menu)
			command = input("> ")
			if command in self.commands['command']:
				self.commands['command'][command]()
			else:
				print("\n❌ Невірна команда. Спробуйте ще раз.")


def main():
	app = TaskManager()
	app.run()

if __name__ == '__main__':
	main()
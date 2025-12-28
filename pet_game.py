import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import tempfile
import os
import sys
from pathlib import Path


class UniversalCodeTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Универсальный Код-Терминал")
        self.root.geometry("1000x700")

        # Поддерживаемые языки и их команды
        self.languages = {
            "Python": {"ext": ".py", "cmd": ["python", "{file}"]},
            "Python 3": {"ext": ".py", "cmd": ["python3", "{file}"]},
            "JavaScript (Node)": {"ext": ".js", "cmd": ["node", "{file}"]},
            "C": {"ext": ".c", "cmd": ["gcc", "{file}", "-o", "{file_noext}", "&&", "./{file_noext}"]},
            "C++": {"ext": ".cpp", "cmd": ["g++", "{file}", "-o", "{file_noext}", "&&", "./{file_noext}"]},
            "Java": {"ext": ".java", "cmd": ["javac", "{file}", "&&", "java", "{class_name}"]},
            "Ruby": {"ext": ".rb", "cmd": ["ruby", "{file}"]},
            "PHP": {"ext": ".php", "cmd": ["php", "{file}"]},
            "Go": {"ext": ".go", "cmd": ["go", "run", "{file}"]},
            "Rust": {"ext": ".rs", "cmd": ["rustc", "{file}", "&&", "./{file_noext}"]},
            "Bash/Shell": {"ext": ".sh", "cmd": ["bash", "{file}"]},
            "Perl": {"ext": ".pl", "cmd": ["perl", "{file}"]},
            "C# (Mono)": {"ext": ".cs", "cmd": ["mcs", "{file}", "&&", "mono", "{file_noext}.exe"]},
            "TypeScript": {"ext": ".ts", "cmd": ["ts-node", "{file}"]},
            "Lua": {"ext": ".lua", "cmd": ["lua", "{file}"]},
            "Swift": {"ext": ".swift", "cmd": ["swift", "{file}"]},
        }

        # Текущий выбранный язык
        self.current_language = "Python"

        # Создаем интерфейс
        self.setup_ui()

    def setup_ui(self):
        # Стиль
        style = ttk.Style()
        style.theme_use('clam')

        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2b2b2b')
        top_frame.pack(fill='x', padx=10, pady=10)

        # Выбор языка
        tk.Label(top_frame, text="Язык:", bg='#2b2b2b', fg='white',
                 font=('Arial', 10)).pack(side='left', padx=5)

        self.language_var = tk.StringVar(value=self.current_language)
        self.language_menu = ttk.Combobox(
            top_frame,
            textvariable=self.language_var,
            values=list(self.languages.keys()),
            width=20,
            state='readonly'
        )
        self.language_menu.pack(side='left', padx=5)
        self.language_menu.bind('<<ComboboxSelected>>', self.on_language_change)

        # Кнопка информации о языке
        ttk.Button(
            top_frame,
            text="ℹ️ Инфо",
            command=self.show_language_info,
            width=10
        ).pack(side='left', padx=5)

        # Кнопки управления
        button_frame = tk.Frame(top_frame, bg='#2b2b2b')
        button_frame.pack(side='right')

        ttk.Button(
            button_frame,
            text="▶ Запустить",
            command=self.run_code,
            style='Run.TButton'
        ).pack(side='left', padx=2)

        ttk.Button(
            button_frame,
            text="🧹 Очистить",
            command=self.clear_output,
        ).pack(side='left', padx=2)

        ttk.Button(
            button_frame,
            text="💾 Сохранить код",
            command=self.save_code,
        ).pack(side='left', padx=2)

        ttk.Button(
            button_frame,
            text="📂 Загрузить код",
            command=self.load_code,
        ).pack(side='left', padx=2)

        # Создаем стиль для кнопки запуска
        style.configure('Run.TButton', foreground='green', font=('Arial', 10, 'bold'))

        # Панель редактора кода
        editor_frame = tk.LabelFrame(self.root, text="✏️ Редактор кода",
                                     font=('Arial', 11, 'bold'))
        editor_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Редактор кода с нумерацией строк
        self.code_text = scrolledtext.ScrolledText(
            editor_frame,
            font=('Courier New', 12),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white',
            wrap='none',
            undo=True
        )
        self.code_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Вставить пример кода
        self.insert_example_code()

        # Настройка подсветки синтаксиса
        self.setup_syntax_highlighting()

        # Панель вывода
        output_frame = tk.LabelFrame(self.root, text="📊 Вывод программы",
                                     font=('Arial', 11, 'bold'))
        output_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Терминал вывода
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            font=('Courier New', 11),
            bg='black',
            fg='#00ff00',
            height=10,
            state='normal'
        )
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Статус бар
        self.status_bar = tk.Label(
            self.root,
            text=f"Готов | Язык: {self.current_language}",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#2b2b2b',
            fg='white'
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def insert_example_code(self):
        """Вставить пример кода для выбранного языка"""
        examples = {
            "Python": '''# Простой калькулятор на Python
def calculator():
    print("🧮 Калькулятор")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")

    choice = input("Выберите операцию (1-4): ")
    num1 = float(input("Первое число: "))
    num2 = float(input("Второе число: "))

    if choice == '1':
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
    elif choice == '2':
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
    elif choice == '3':
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
    elif choice == '4':
        if num2 != 0:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
        else:
            print("Ошибка: деление на ноль!")
    else:
        print("Неверный выбор!")

if __name__ == "__main__":
    calculator()''',

            "JavaScript (Node)": '''// Приветствие на JavaScript
console.log("👋 Привет из Node.js!");
console.log("Вот пример работы:");

function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log("Первые 10 чисел Фибоначчи:");
for (let i = 0; i < 10; i++) {
    console.log(`F(${i}) = ${fibonacci(i)}`);
}

// Работа с массивом
const fruits = ["🍎 Яблоко", "🍌 Банан", "🍊 Апельсин", "🍓 Клубника"];
console.log("\\nМои любимые фрукты:");
fruits.forEach(fruit => console.log(fruit));''',

            "C": '''/* Программа на C - проверка числа */
#include <stdio.h>

int main() {
    printf("🔢 Проверка числа\\n");

    int number;
    printf("Введите число: ");
    scanf("%d", &number);

    printf("\\nАнализ числа %d:\\n", number);

    if (number > 0) {
        printf("- Число положительное\\n");
    } else if (number < 0) {
        printf("- Число отрицательное\\n");
    } else {
        printf("- Это ноль\\n");
    }

    if (number % 2 == 0) {
        printf("- Число четное\\n");
    } else {
        printf("- Число нечетное\\n");
    }

    return 0;
}''',

            "Java": '''// Простой класс на Java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("☕ Hello from Java!");
        System.out.println("Аргументы командной строки:");

        if (args.length > 0) {
            for (int i = 0; i < args.length; i++) {
                System.out.println("  args[" + i + "] = " + args[i]);
            }
        } else {
            System.out.println("  (аргументы не переданы)");
        }

        // Пример вычисления факториала
        int number = 5;
        long factorial = calculateFactorial(number);
        System.out.println("\\nФакториал " + number + " = " + factorial);
    }

    public static long calculateFactorial(int n) {
        if (n <= 1) return 1;
        return n * calculateFactorial(n - 1);
    }
}''',

            "HTML/JavaScript": '''<!-- Простая HTML страница с JS -->
<!DOCTYPE html>
<html>
<head>
    <title>Моя страница</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ Мой первый сайт</h1>
        <p id="demo">Нажмите кнопку чтобы изменить этот текст.</p>
        <button onclick="changeText()">Нажми меня!</button>
        <button onclick="showTime()">Показать время</button>
    </div>

    <script>
        function changeText() {
            document.getElementById("demo").innerHTML = 
                "🎉 Текст изменен! " + new Date().toLocaleTimeString();
        }

        function showTime() {
            alert("Текущее время: " + new Date().toLocaleTimeString());
        }

        console.log("Страница загружена!");
    </script>
</body>
</html>'''
        }

        # Получаем пример для текущего языка или Python по умолчанию
        example = examples.get(self.current_language, examples["Python"])
        self.code_text.insert('1.0', example)

    def setup_syntax_highlighting(self):
        """Настройка цветов для разных языков"""
        # Теги для подсветки (базовые)
        self.code_text.tag_configure("keyword", foreground="#569CD6")
        self.code_text.tag_configure("string", foreground="#CE9178")
        self.code_text.tag_configure("comment", foreground="#608B4E")
        self.code_text.tag_configure("number", foreground="#B5CEA8")
        self.code_text.tag_configure("function", foreground="#DCDCAA")

        # Привязка события для динамической подсветки
        self.code_text.bind('<KeyRelease>', self.highlight_syntax)

    def highlight_syntax(self, event=None):
        """Простая подсветка синтаксиса"""
        # Очищаем все теги
        for tag in ["keyword", "string", "comment", "number", "function"]:
            self.code_text.tag_remove(tag, "1.0", tk.END)

        # Получаем весь текст
        content = self.code_text.get("1.0", tk.END)

        # Простая подсветка для Python (можно расширить для других языков)
        if self.current_language in ["Python", "Python 3"]:
            keywords = ["def", "class", "if", "else", "elif", "while",
                        "for", "in", "import", "from", "as", "return",
                        "try", "except", "finally", "with", "lambda"]

            lines = content.split('\n')
            line_num = 1

            for line in lines:
                # Комментарии
                if '#' in line:
                    start = line.find('#')
                    self.code_text.tag_add("comment",
                                           f"{line_num}.{start}",
                                           f"{line_num}.{len(line)}")

                # Ключевые слова
                for keyword in keywords:
                    idx = 0
                    while idx < len(line):
                        idx = line.find(keyword, idx)
                        if idx == -1:
                            break
                        # Проверяем, что это отдельное слово
                        if (idx == 0 or not line[idx - 1].isalnum()) and \
                                (idx + len(keyword) == len(line) or not line[idx + len(keyword)].isalnum()):
                            self.code_text.tag_add("keyword",
                                                   f"{line_num}.{idx}",
                                                   f"{line_num}.{idx + len(keyword)}")
                        idx += len(keyword)

                line_num += 1

    def on_language_change(self, event):
        """Обработка смены языка"""
        self.current_language = self.language_var.get()
        self.status_bar.config(text=f"Язык изменен на: {self.current_language}")

        # Очищаем и вставляем новый пример
        self.code_text.delete('1.0', tk.END)
        self.insert_example_code()

    def show_language_info(self):
        """Показать информацию о выбранном языке"""
        lang = self.current_language
        info = {
            "Python": "• Интерпретируемый язык\n• Динамическая типизация\n• Отличный для начинающих",
            "JavaScript (Node)": "• Язык для веба\n• Выполняется в Node.js\n• Асинхронное программирование",
            "C": "• Компилируемый язык\n• Статическая типизация\n• Высокая производительность",
            "Java": "• Кроссплатформенный\n• Виртуальная машина JVM\n• Объектно-ориентированный",
            "C++": "• Наследник C\n• ООП + низкоуровневые возможности\n• Высокая скорость",
            "HTML/JavaScript": "• Веб-технологии\n• HTML - разметка\n• JS - интерактивность"
        }

        messagebox.showinfo(
            f"Информация: {lang}",
            info.get(lang, "Информация об этом языке скоро будет добавлена!")
        )

    def run_code(self):
        """Запуск кода"""
        code = self.code_text.get('1.0', tk.END).strip()

        if not code:
            messagebox.showwarning("Пустой код", "Пожалуйста, введите код для выполнения")
            return

        # Очищаем вывод
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', f"🚀 Запуск {self.current_language}...\n{'=' * 50}\n")

        # Обновляем статус
        self.status_bar.config(text="Выполняется...")
        self.root.update()

        try:
            # Создаем временный файл
            with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix=self.languages[self.current_language]["ext"],
                    delete=False,
                    encoding='utf-8'
            ) as f:
                f.write(code)
                temp_file = f.name

            # Получаем команду для выполнения
            lang_info = self.languages[self.current_language]
            cmd_template = lang_info["cmd"]

            # Заменяем плейсхолдеры
            file_noext = os.path.splitext(temp_file)[0]
            class_name = os.path.splitext(os.path.basename(temp_file))[0]

            cmd = []
            for part in cmd_template:
                part = part.replace("{file}", temp_file)
                part = part.replace("{file_noext}", file_noext)
                part = part.replace("{class_name}", class_name)
                cmd.append(part)

            # Если команда содержит &&, разбиваем на несколько
            if "&&" in cmd:
                # Упрощенная обработка нескольких команд
                full_cmd = " ".join(cmd)
                result = subprocess.run(
                    full_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

            # Выводим результат
            if result.stdout:
                self.output_text.insert(tk.END, "✅ ВЫВОД:\n")
                self.output_text.insert(tk.END, result.stdout)

            if result.stderr:
                self.output_text.insert(tk.END, "\n❌ ОШИБКИ:\n")
                self.output_text.insert(tk.END, result.stderr)

            self.output_text.insert(tk.END, f"\n{'=' * 50}\n")
            self.output_text.insert(tk.END, f"💡 Код завершился с кодом возврата: {result.returncode}")

        except subprocess.TimeoutExpired:
            self.output_text.insert(tk.END, "\n⏰ ТАЙМАУТ: Программа выполнялась слишком долго (более 30 секунд)")
        except FileNotFoundError as e:
            self.output_text.insert(tk.END, f"\n❌ ОШИБКА: {e}")
            self.output_text.insert(tk.END,
                                    "\n⚠️  Убедитесь, что компилятор/интерпретатор установлен и добавлен в PATH")
        except Exception as e:
            self.output_text.insert(tk.END, f"\n❌ НЕИЗВЕСТНАЯ ОШИБКА: {e}")
        finally:
            # Удаляем временный файл
            if 'temp_file' in locals() and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                    # Удаляем скомпилированные файлы если есть
                    if self.current_language in ["C", "C++", "Rust"]:
                        exe_file = file_noext
                        if os.path.exists(exe_file):
                            os.unlink(exe_file)
                        if os.path.exists(exe_file + ".exe"):
                            os.unlink(exe_file + ".exe")
                except:
                    pass

            # Обновляем статус
            self.status_bar.config(text=f"Готов | Язык: {self.current_language}")

    def clear_output(self):
        """Очистить область вывода"""
        self.output_text.delete('1.0', tk.END)

    def save_code(self):
        """Сохранить код в файл"""
        from tkinter import filedialog

        code = self.code_text.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("Пустой код", "Нет кода для сохранения")
            return

        # Предлагаем расширение по умолчанию
        default_ext = self.languages[self.current_language]["ext"]
        filename = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=[
                (f"{self.current_language} файлы", f"*{default_ext}"),
                ("Все файлы", "*.*")
            ]
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                messagebox.showinfo("Успех", f"Код сохранен в:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

    def load_code(self):
        """Загрузить код из файла"""
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            filetypes=[
                ("Все файлы", "*.*"),
                ("Python", "*.py"),
                ("JavaScript", "*.js"),
                ("C/C++", "*.c;*.cpp;*.h"),
                ("Java", "*.java"),
                ("HTML", "*.html;*.htm"),
            ]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()

                self.code_text.delete('1.0', tk.END)
                self.code_text.insert('1.0', code)

                # Пытаемся определить язык по расширению
                ext = os.path.splitext(filename)[1].lower()
                ext_to_lang = {
                    '.py': 'Python',
                    '.js': 'JavaScript (Node)',
                    '.c': 'C',
                    '.cpp': 'C++',
                    '.java': 'Java',
                    '.html': 'HTML/JavaScript',
                    '.htm': 'HTML/JavaScript',
                    '.rb': 'Ruby',
                    '.php': 'PHP',
                    '.go': 'Go',
                    '.rs': 'Rust',
                    '.sh': 'Bash/Shell',
                    '.pl': 'Perl',
                    '.cs': 'C# (Mono)',
                    '.ts': 'TypeScript',
                    '.lua': 'Lua',
                    '.swift': 'Swift'
                }

                if ext in ext_to_lang and ext_to_lang[ext] in self.languages:
                    self.current_language = ext_to_lang[ext]
                    self.language_var.set(self.current_language)

                messagebox.showinfo("Успех", f"Код загружен из:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")


def main():
    """Запуск приложения"""
    root = tk.Tk()

    # Устанавливаем иконку (если есть)
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass

    # Создаем приложение
    app = UniversalCodeTerminal(root)

    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Запускаем главный цикл
    root.mainloop()


if __name__ == "__main__":
    main()
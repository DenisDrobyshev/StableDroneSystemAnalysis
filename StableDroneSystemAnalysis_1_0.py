import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib import rcParams

class ModernDroneSystemAnalysis:
    """
    Современный интерфейс для анализа устойчивости динамической системы БПЛА
    с красивым UI/UX дизайном
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🛩️ Анализ устойчивости системы БПЛА")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f5f6fa')
        
        # Настройка стилей
        self.setup_styles()
        self.setup_parameters()
        self.setup_ui()
        
    def setup_styles(self):
        """Настройка современных стилей для интерфейса"""
        self.style = ttk.Style()
        self.style.theme_use('clam')  
        
        # Современная цветовая схема
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71', 
            'accent': '#e74c3c',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'background': '#f5f6fa',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }
        
        # Настройка стилей ttk
        self.style.configure('Modern.TFrame', background=self.colors['background'])
        self.style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)
        self.style.configure('Title.TLabel', background=self.colors['background'], 
                           font=('Segoe UI', 16, 'bold'), foreground=self.colors['dark'])
        self.style.configure('Subtitle.TLabel', background=self.colors['background'],
                           font=('Segoe UI', 12), foreground=self.colors['dark'])
        self.style.configure('Modern.TButton',
                     font=('Segoe UI', 10, 'bold'),
                     background=self.colors['primary'],
                     foreground=self.colors['dark'],  
                     borderwidth=0,
                     padding=(10, 5))

        self.style.configure('Accent.TButton',
                     font=('Segoe UI', 10, 'bold'),
                     background=self.colors['secondary'],
                     foreground=self.colors['dark'],  
                     borderwidth=0,
                     padding=(10, 5))
        
        self.style.configure('Modern.TLabelframe', background=self.colors['background'],
                           font=('Segoe UI', 11, 'bold'))
        self.style.configure('Modern.TLabelframe.Label', background=self.colors['background'],
                           font=('Segoe UI', 11, 'bold'), foreground=self.colors['dark'])
        
        # Настройка matplotlib для современных графиков
        plt.style.use('seaborn-v0_8-whitegrid')
        rcParams['font.family'] = 'Segoe UI'
        rcParams['axes.titleweight'] = 'bold'
        rcParams['axes.labelsize'] = 12
        
    def setup_parameters(self):
        """Инициализация параметров системы"""
        # Основные параметры
        self.t0 = 0.0
        self.t_k = 50.0
        self.n = 2000
        self.dt = self.t_k / self.n
        
        # Параметры системы
        self.mass = 1.0
        self.damping_coef = 2.5
        self.stiffness_coef = 4.0
        self.control_coef = 1.0
        
        # Начальные условия
        self.a1_0 = 0.5
        self.a2_0 = 0.0
        
        # Управляющие воздействия
        self.u_functions = [
            ("🔄 Без управления", self.u_zero),
            ("📈 Плавное нарастание", self.u_smooth_ramp),
            ("🌊 Синусоидальное", self.u_sine),
            ("⚡ Постоянное", self.u_constant),
            ("🎯 Импульсное", self.u_smooth_pulse),
            ("📊 Ступенчатое", self.u_step),
            ("🛡️ Стабилизирующее", self.u_stabilizing),
        ]
        
        # Методы интегрирования
        self.integration_methods = [
            ("📐 Эйлер", self.euler_integration),
            ("🎯 Рунге-Кутта 4", self.rk4_integration)
        ]
    
    def u_zero(self, t):
        return 0.0
    
    def u_smooth_ramp(self, t):
        return min(1.0, 0.2 * t)
    
    def u_sine(self, t):
        return 0.5 * np.sin(0.5 * t)
    
    def u_constant(self, t):
        return 0.3
    
    def u_smooth_pulse(self, t):
        if 10 < t < 20:
            return 0.8 * (1 + np.sin(0.5 * (t - 10)))
        return 0.0
    
    def u_step(self, t):
        return 0.4 if t > 15 else 0.0
    
    def u_stabilizing(self, t):
        return -0.1 * t if t < 10 else 0.1
    
    def system_equations(self, a1, a2, u):
        """Корректные уравнения системы дрона"""
        da1_dt = a2
        da2_dt = (u - self.damping_coef * a2 - self.stiffness_coef * a1) / self.mass
        return da1_dt, da2_dt
    
    def euler_integration(self, u_func):
        """Интегрирование методом Эйлера"""
        t = np.linspace(self.t0, self.t_k, self.n + 1)
        a1 = np.zeros(self.n + 1)
        a2 = np.zeros(self.n + 1)
        u_vals = np.zeros(self.n + 1)
        
        a1[0] = self.a1_0
        a2[0] = self.a2_0
        u_vals[0] = u_func(self.t0)
        
        for i in range(self.n):
            current_u = u_func(t[i])
            da1_dt, da2_dt = self.system_equations(a1[i], a2[i], current_u)
            
            a1[i + 1] = a1[i] + da1_dt * self.dt
            a2[i + 1] = a2[i] + da2_dt * self.dt
            u_vals[i + 1] = u_func(t[i + 1])
        
        return t, a1, a2, u_vals
    
    def rk4_integration(self, u_func):
        """Интегрирование методом Рунге-Кутты 4-го порядка"""
        t = np.linspace(self.t0, self.t_k, self.n + 1)
        a1 = np.zeros(self.n + 1)
        a2 = np.zeros(self.n + 1)
        u_vals = np.zeros(self.n + 1)
        
        a1[0] = self.a1_0
        a2[0] = self.a2_0
        u_vals[0] = u_func(self.t0)
        
        for i in range(self.n):
            current_t = t[i]
            current_u = u_func(current_t)
            
            k1_a1, k1_a2 = self.system_equations(a1[i], a2[i], current_u)
            k2_a1, k2_a2 = self.system_equations(
                a1[i] + 0.5 * self.dt * k1_a1,
                a2[i] + 0.5 * self.dt * k1_a2,
                u_func(current_t + 0.5 * self.dt)
            )
            k3_a1, k3_a2 = self.system_equations(
                a1[i] + 0.5 * self.dt * k2_a1,
                a2[i] + 0.5 * self.dt * k2_a2,
                u_func(current_t + 0.5 * self.dt)
            )
            k4_a1, k4_a2 = self.system_equations(
                a1[i] + self.dt * k3_a1,
                a2[i] + self.dt * k3_a2,
                u_func(current_t + self.dt)
            )
            
            a1[i + 1] = a1[i] + (self.dt / 6.0) * (k1_a1 + 2*k2_a1 + 2*k3_a1 + k4_a1)
            a2[i + 1] = a2[i] + (self.dt / 6.0) * (k1_a2 + 2*k2_a2 + 2*k3_a2 + k4_a2)
            u_vals[i + 1] = u_func(t[i + 1])
        
        return t, a1, a2, u_vals
    
    def analyze_stability(self, a1, a2):
        """Анализ устойчивости системы"""
        a1_final = a1[-1]
        a2_final = a2[-1]
        
        zero_crossings_a1 = np.where(np.diff(np.sign(a1)))[0]
        has_oscillations = len(zero_crossings_a1) > 2
        
        # Вычисление собственных чисел
        a_coef = 1.0
        b_coef = self.damping_coef / self.mass
        c_coef = self.stiffness_coef / self.mass
        
        discriminant = b_coef**2 - 4*a_coef*c_coef
        
        if discriminant >= 0:
            lambda1 = (-b_coef + np.sqrt(discriminant)) / (2*a_coef)
            lambda2 = (-b_coef - np.sqrt(discriminant)) / (2*a_coef)
            eigen_type = "Вещественные"
        else:
            real_part = -b_coef / (2*a_coef)
            imag_part = np.sqrt(-discriminant) / (2*a_coef)
            lambda1 = complex(real_part, imag_part)
            lambda2 = complex(real_part, -imag_part)
            eigen_type = "Комплексные"
        
        # Определение типа устойчивости
        if has_oscillations:
            if abs(a1_final) < 0.05 and abs(a2_final) < 0.05:
                stability = "✅ Устойчивые колебания"
                color = self.colors['success']
                icon = "🔄"
            else:
                stability = "⚠️ Неустойчивые колебания"
                color = self.colors['warning']
                icon = "⚡"
        else:
            if abs(a1_final) < 0.05 and abs(a2_final) < 0.05:
                stability = "✅ Апериодическая устойчивость"
                color = self.colors['success']
                icon = "✅"
            elif abs(a1_final) < 1.0:
                stability = "⚠️ Ограниченная устойчивость"
                color = self.colors['warning']
                icon = "📊"
            else:
                stability = "❌ Расходящаяся система"
                color = self.colors['danger']
                icon = "❌"
        
        additional_info = f"""
{icon} {stability}

📊 Собственные числа: {lambda1:.3f}, {lambda2:.3f}
🎯 Тип: {eigen_type}
📈 Колебания: {'Да' if has_oscillations else 'Нет'}
🎯 Конечные значения: a1={a1_final:.3f}, a2={a2_final:.3f}
        """.strip()
        
        return stability, color, additional_info
    
    def create_card(self, parent, title, padding=10):
        """Создание карточки с тенью"""
        card = ttk.Frame(parent, style='Card.TFrame', padding=padding)
        
        if title:
            title_label = ttk.Label(card, text=title, font=('Segoe UI', 11, 'bold'),
                                  foreground=self.colors['dark'], background='white')
            title_label.pack(anchor='w', pady=(0, 10))
        
        return card
    
    def setup_ui(self):
        """Создание современного пользовательского интерфейса"""
        # Главный контейнер
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок приложения
        header_frame = ttk.Frame(main_container, style='Modern.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
                               text="🛩️ Анализ устойчивости системы БПЛА",
                               font=('Segoe UI', 24, 'bold'),
                               foreground=self.colors['dark'],
                               background=self.colors['background'])
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(header_frame,
                                 text="Моделирование динамики и анализ устойчивости",
                                 font=('Segoe UI', 12),
                                 foreground=self.colors['primary'],
                                 background=self.colors['background'])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=(5, 0))
        
        # Основное содержимое - две колонки
        content_frame = ttk.Frame(main_container, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая колонка - управление
        left_column = ttk.Frame(content_frame, style='Modern.TFrame', width=400)
        left_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_column.pack_propagate(False)
        
        # Правая колонка - графики
        right_column = ttk.Frame(content_frame, style='Modern.TFrame')
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Карточка управления моделированием
        control_card = self.create_card(left_column, "🎮 Управление моделированием")
        control_card.pack(fill=tk.X, pady=(0, 15))
        
        # Выбор типа управления
        ttk.Label(control_card, text="Тип управления:", 
                 font=('Segoe UI', 10, 'bold'),
                 background='white').pack(anchor='w', pady=(5, 2))
        
        self.u_var = tk.StringVar()
        self.u_combobox = ttk.Combobox(control_card, textvariable=self.u_var, 
                                       values=[name for name, _ in self.u_functions],
                                       state="readonly", 
                                       font=('Segoe UI', 10),
                                       height=15)
        self.u_combobox.current(0)
        self.u_combobox.pack(fill=tk.X, pady=(0, 10))
        
        # Выбор метода интегрирования
        ttk.Label(control_card, text="Метод интегрирования:",
                 font=('Segoe UI', 10, 'bold'),
                 background='white').pack(anchor='w', pady=(5, 2))
        
        self.method_var = tk.StringVar()
        self.method_combobox = ttk.Combobox(control_card, textvariable=self.method_var,
                                            values=[name for name, _ in self.integration_methods],
                                            state="readonly",
                                            font=('Segoe UI', 10))
        self.method_combobox.current(1)
        self.method_combobox.pack(fill=tk.X, pady=(0, 15))
        
        # Кнопки управления
        button_frame = ttk.Frame(control_card, style='Card.TFrame')
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="🚀 Запустить моделирование", 
                  command=self.run_simulation, style='Accent.TButton').pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="📊 Сравнить все", 
                  command=self.compare_all, style='Modern.TButton').pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="📈 Анализ устойчивости", 
                  command=self.stability_analysis, style='Modern.TButton').pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="💾 Экспорт данных", 
                  command=self.export_data, style='Modern.TButton').pack(fill=tk.X, pady=2)
        
        # Карточка параметров системы
        params_card = self.create_card(left_column, "⚙️ Параметры системы")
        params_card.pack(fill=tk.X, pady=(0, 15))
        
        # Параметры в сетке
        params_grid = ttk.Frame(params_card, style='Card.TFrame')
        params_grid.pack(fill=tk.X)
        
        parameters = [
            ("Масса (m)", "mass", self.mass),
            ("Демпфирование (c)", "damping_coef", self.damping_coef),
            ("Жесткость (k)", "stiffness_coef", self.stiffness_coef),
            ("Нач. положение (a1₀)", "a1_0", self.a1_0),
        ]
        
        self.param_vars = {}
        for i, (label, param_name, default_value) in enumerate(parameters):
            ttk.Label(params_grid, text=label, background='white',
                     font=('Segoe UI', 9)).grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            
            var = tk.DoubleVar(value=default_value)
            self.param_vars[param_name] = var
            
            entry = ttk.Entry(params_grid, textvariable=var, font=('Segoe UI', 9),
                             width=15)
            entry.grid(row=i, column=1, sticky=tk.EW, pady=5, padx=(0, 10))
            
            # Информационная кнопка
            info_btn = ttk.Button(params_grid, text="ℹ️", width=3,
                                 command=lambda p=param_name: self.show_param_info(p))
            info_btn.grid(row=i, column=2, padx=(0, 5))
        
        params_grid.columnconfigure(1, weight=1)
        
        ttk.Button(params_card, text="🔄 Применить параметры", 
                  command=self.apply_parameters, style='Modern.TButton').pack(fill=tk.X, pady=(10, 0))
        
        # Карточка информации о системе
        info_card = self.create_card(left_column, "📊 Информация о системе")
        info_card.pack(fill=tk.X, pady=(0, 15))
        
        self.info_text = tk.Text(info_card, height=8, wrap=tk.WORD, 
                                font=('Segoe UI', 9),
                                bg='white', relief='flat',
                                padx=10, pady=10)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.insert(tk.END, "Запустите моделирование для получения информации...")
        self.info_text.config(state=tk.DISABLED)
        
        # Область графиков
        graphs_card = self.create_card(right_column, "📈 Визуализация динамики системы")
        graphs_card.pack(fill=tk.BOTH, expand=True)
        
        # Создание современных графиков
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        self.fig.set_facecolor('#f8f9fa')
        
        # Настройка стилей графиков
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.set_facecolor('#ffffff')
            ax.grid(True, alpha=0.3, color='#e0e0e0')
            ax.spines['bottom'].set_color('#cccccc')
            ax.spines['top'].set_color('#cccccc') 
            ax.spines['right'].set_color('#cccccc')
            ax.spines['left'].set_color('#cccccc')
        
        self.ax1.set_xlabel('Время, с', fontsize=11, fontweight='bold')
        self.ax1.set_ylabel('a1(t) - Положение, м', fontsize=11, fontweight='bold')
        
        self.ax2.set_xlabel('Время, с', fontsize=11, fontweight='bold')
        self.ax2.set_ylabel('a2(t) - Скорость, м/с', fontsize=11, fontweight='bold')
        
        self.ax3.set_xlabel('Время, с', fontsize=11, fontweight='bold')
        self.ax3.set_ylabel('u(t) - Управление, Н', fontsize=11, fontweight='bold')
        
        self.ax4.set_xlabel('a1 - Положение, м', fontsize=11, fontweight='bold')
        self.ax4.set_ylabel('a2 - Скорость, м/с', fontsize=11, fontweight='bold')
        
        self.canvas = FigureCanvasTkAgg(self.fig, graphs_card)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Статус бар
        status_frame = ttk.Frame(main_container, style='Modern.TFrame', height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="🟢 Готов к моделированию")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var,
                              font=('Segoe UI', 9),
                              background=self.colors['dark'],
                              foreground='white',
                              anchor=tk.W,
                              padding=(10, 5))
        status_bar.pack(fill=tk.BOTH)
        
        # Запуск первоначального моделирования
        self.run_simulation()
    
    def show_param_info(self, param_name):
        """Показать информацию о параметре"""
        info_mapping = {
            'mass': "Масса дрона [кг]. Влияет на инерционность системы.",
            'damping_coef': "Коэффициент демпфирования [Н·с/м]. Определяет затухание колебаний.", 
            'stiffness_coef': "Коэффициент жесткости [Н/м]. Определяет упругие свойства системы.",
            'a1_0': "Начальное положение [м]. Начальное отклонение от положения равновесия."
        }
        
        messagebox.showinfo("Информация о параметре", 
                          info_mapping.get(param_name, "Информация отсутствует"))
    
    def apply_parameters(self):
        """Применение новых параметров системы"""
        try:
            self.mass = max(0.1, self.param_vars['mass'].get())
            self.damping_coef = max(0.0, self.param_vars['damping_coef'].get())
            self.stiffness_coef = max(0.0, self.param_vars['stiffness_coef'].get())
            self.a1_0 = self.param_vars['a1_0'].get()
            
            self.status_var.set("✅ Параметры применены успешно")
            self.run_simulation()
        except Exception as e:
            self.status_var.set(f"❌ Ошибка в параметрах: {str(e)}")
    
    def run_simulation(self):
        """Запуск моделирования с современной визуализацией"""
        try:
            self.status_var.set("🔄 Выполняется моделирование...")
            self.root.update()
            
            # Очистка графиков
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.clear()
                ax.grid(True, alpha=0.3, color='#e0e0e0')
                ax.set_facecolor('#ffffff')
            
            # Получение выбранных параметров
            u_name = self.u_var.get()
            u_func = dict(self.u_functions)[u_name]
            
            method_name = self.method_var.get()
            method_func = dict(self.integration_methods)[method_name]
            
            # Выполнение моделирования
            t, a1, a2, u_vals = method_func(u_func)
            
            # Анализ устойчивости
            stability, color, additional_info = self.analyze_stability(a1, a2)
            
            # Современное оформление графиков
            self.ax1.plot(t, a1, color=self.colors['primary'], linewidth=2.5, label='a1(t)')
            self.ax1.fill_between(t, a1, alpha=0.3, color=self.colors['primary'])
            self.ax1.set_title(f'📊 Положение системы', fontsize=12, fontweight='bold', pad=15)
            self.ax1.legend(framealpha=0.9, facecolor='white')
            
            self.ax2.plot(t, a2, color=self.colors['secondary'], linewidth=2.5, label='a2(t)')
            self.ax2.fill_between(t, a2, alpha=0.3, color=self.colors['secondary'])
            self.ax2.set_title('🎯 Скорость системы', fontsize=12, fontweight='bold', pad=15)
            self.ax2.legend(framealpha=0.9, facecolor='white')
            
            self.ax3.plot(t, u_vals, color=self.colors['accent'], linewidth=2.5, label='u(t)')
            self.ax3.fill_between(t, u_vals, alpha=0.3, color=self.colors['accent'])
            self.ax3.set_title(f'🎮 Управляющее воздействие: {u_name.split(" ", 1)[-1]}', 
                             fontsize=12, fontweight='bold', pad=15)
            self.ax3.legend(framealpha=0.9, facecolor='white')
            
            # Фазовый портрет с градиентом
            points = np.array([a1, a2]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            
            from matplotlib.collections import LineCollection
            lc = LineCollection(segments, cmap='viridis', linewidth=2, alpha=0.8)
            lc.set_array(np.linspace(0, 1, len(segments)))
            self.ax4.add_collection(lc)
            
            self.ax4.plot(a1[0], a2[0], 'o', markersize=10, 
                         color=self.colors['success'], label='Начало', markeredgecolor='white', markeredgewidth=2)
            self.ax4.plot(a1[-1], a2[-1], 's', markersize=10, 
                         color=self.colors['danger'], label='Конец', markeredgecolor='white', markeredgewidth=2)
            self.ax4.set_title('🔄 Фазовый портрет системы', fontsize=12, fontweight='bold', pad=15)
            self.ax4.legend(framealpha=0.9, facecolor='white')
            
            # Обновление информации
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"""📋 РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ

{additional_info}

📊 Параметры моделирования:
• Метод: {method_name}
• Управление: {u_name}
• Время: {self.t_k} с
• Шаг: {self.dt:.3f} с
• Точек: {self.n}

⚙️ Параметры системы:
• Масса: {self.mass} кг
• Демпфирование: {self.damping_coef} Н·с/м  
• Жесткость: {self.stiffness_coef} Н/м
""")
            self.info_text.config(state=tk.DISABLED)
            
            # Обновление canvas
            self.fig.tight_layout()
            self.canvas.draw()
            
            self.status_var.set(f"✅ Моделирование завершено: {stability}")
            
        except Exception as e:
            self.status_var.set(f"❌ Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"Произошла ошибка при моделировании:\n{str(e)}")
    
    def compare_all(self):
        """Сравнение всех управляющих воздействий с современной визуализацией"""
        try:
            self.status_var.set("🔄 Выполняется сравнение всех управлений...")
            self.root.update()
            
            # Очистка графиков
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.clear()
                ax.grid(True, alpha=0.3, color='#e0e0e0')
                ax.set_facecolor('#ffffff')
            
            colors = plt.cm.Set3(np.linspace(0, 1, len(self.u_functions)))
            
            # Получение выбранного метода
            method_name = self.method_var.get()
            method_func = dict(self.integration_methods)[method_name]
            
            # Моделирование для всех управлений
            for idx, (u_name, u_func) in enumerate(self.u_functions):
                t, a1, a2, u_vals = method_func(u_func)
                stability, _, _ = self.analyze_stability(a1, a2)
                
                label = u_name.split(" ", 1)[-1]
                
                self.ax1.plot(t, a1, color=colors[idx], linewidth=2, label=label, alpha=0.8)
                self.ax2.plot(t, a2, color=colors[idx], linewidth=2, alpha=0.8, label=label)
                self.ax3.plot(t, u_vals, color=colors[idx], linewidth=2, alpha=0.8, label=label)
                self.ax4.plot(a1, a2, color=colors[idx], linewidth=1.5, alpha=0.7, label=label)
            
            # Настройка графиков сравнения
            self.ax1.set_title('📊 Сравнение: Положение системы', fontsize=12, fontweight='bold', pad=15)
            self.ax1.set_ylabel('a1(t) - Положение, м')
            self.ax1.legend(fontsize=9, framealpha=0.9, facecolor='white')
            
            self.ax2.set_title('🎯 Сравнение: Скорость системы', fontsize=12, fontweight='bold', pad=15)
            self.ax2.set_ylabel('a2(t) - Скорость, м/с')
            self.ax2.legend(fontsize=9, framealpha=0.9, facecolor='white')
            
            self.ax3.set_title('🎮 Сравнение: Управляющие воздействия', fontsize=12, fontweight='bold', pad=15)
            self.ax3.set_ylabel('u(t) - Управление, Н')
            self.ax3.legend(fontsize=9, framealpha=0.9, facecolor='white')
            
            self.ax4.set_title('🔄 Сравнение: Фазовые портреты', fontsize=12, fontweight='bold', pad=15)
            self.ax4.set_xlabel('a1 - Положение, м')
            self.ax4.set_ylabel('a2 - Скорость, м/с')
            self.ax4.legend(fontsize=9, framealpha=0.9, facecolor='white')
            
            # Обновление информации
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"""📊 СРАВНЕНИЕ УПРАВЛЕНИЙ

🔄 Выполнено сравнение {len(self.u_functions)} типов управления

🎯 Метод интегрирования: {method_name}
📈 Время моделирования: {self.t_k} с
⚙️ Количество точек: {self.n}

💡 Для детального анализа выберите конкретный тип управления
""")
            self.info_text.config(state=tk.DISABLED)
            
            # Обновление canvas
            self.fig.tight_layout()
            self.canvas.draw()
            
            self.status_var.set("✅ Сравнение всех управлений завершено")
            
        except Exception as e:
            self.status_var.set(f"❌ Ошибка при сравнении: {str(e)}")
            messagebox.showerror("Ошибка", f"Ошибка при сравнении:\n{str(e)}")
    
    def stability_analysis(self):
        """Углубленный анализ устойчивости системы"""
        try:
            # Создаем современное окно для анализа
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("📈 Анализ устойчивости системы")
            analysis_window.geometry("700x500")
            analysis_window.configure(bg=self.colors['background'])
            analysis_window.resizable(True, True)
            
            # Центрирование окна
            analysis_window.transient(self.root)
            analysis_window.grab_set()
            
            # Заголовок
            title_frame = ttk.Frame(analysis_window, style='Modern.TFrame')
            title_frame.pack(fill=tk.X, padx=20, pady=20)
            
            ttk.Label(title_frame, 
                     text="📈 Анализ устойчивости системы",
                     font=('Segoe UI', 18, 'bold'),
                     foreground=self.colors['dark'],
                     background=self.colors['background']).pack()
            
            # Содержимое анализа
            content_frame = ttk.Frame(analysis_window, style='Modern.TFrame')
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            # Вычисляем собственные числа
            a_coef = 1.0
            b_coef = self.damping_coef / self.mass
            c_coef = self.stiffness_coef / self.mass
            
            discriminant = b_coef**2 - 4*a_coef*c_coef
            
            if discriminant >= 0:
                lambda1 = (-b_coef + np.sqrt(discriminant)) / (2*a_coef)
                lambda2 = (-b_coef - np.sqrt(discriminant)) / (2*a_coef)
                eigen_type = "Вещественные"
                stability = "✅ Устойчива" if (lambda1 < 0 and lambda2 < 0) else "❌ Неустойчива"
                stability_color = self.colors['success'] if (lambda1 < 0 and lambda2 < 0) else self.colors['danger']
            else:
                real_part = -b_coef / (2*a_coef)
                imag_part = np.sqrt(-discriminant) / (2*a_coef)
                lambda1 = complex(real_part, imag_part)
                lambda2 = complex(real_part, -imag_part)
                eigen_type = "Комплексные"
                stability = "✅ Устойчива" if real_part < 0 else "❌ Неустойчива"
                stability_color = self.colors['success'] if real_part < 0 else self.colors['danger']
            
            # Текст анализа
            analysis_text = f"""
🔍 АНАЛИЗ УСТОЙЧИВОСТИ СИСТЕМЫ

📋 Параметры системы:
• Масса (m): {self.mass} кг
• Демпфирование (c): {self.damping_coef} Н·с/м  
• Жесткость (k): {self.stiffness_coef} Н/м

📐 Характеристическое уравнение:
λ² + {b_coef:.3f}λ + {c_coef:.3f} = 0

🎯 Собственные числа:
λ₁ = {lambda1:.3f}
λ₂ = {lambda2:.3f}
📊 Тип: {eigen_type}

📈 Дискриминант: {discriminant:.3f}

🎯 РЕЗУЛЬТАТ: {stability}

💡 Критерии устойчивости:
• Система устойчива, если действительные части всех собственных чисел отрицательны
• В данном случае: {f"Re(λ₁)={lambda1.real:.3f}, Re(λ₂)={lambda2.real:.3f}" if eigen_type == "Комплексные" 
                        else f"λ₁={lambda1:.3f}, λ₂={lambda2:.3f}"}

🛠️ Рекомендации:
• Для повышения устойчивости увеличьте демпфирование
• Оптимальное демпфирование: критическое (дискриминант = 0)
• Избегайте отрицательных значений жесткости
"""
            
            text_widget = tk.Text(content_frame, wrap=tk.WORD, padx=20, pady=20,
                                 font=('Segoe UI', 10),
                                 bg='white', relief='flat')
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, analysis_text)
            
            # Подсветка результата
            text_widget.tag_configure("result", foreground=stability_color, font=('Segoe UI', 11, 'bold'))
            start_idx = analysis_text.find("🎯 РЕЗУЛЬТАТ:")
            line_start = analysis_text.count('\n', 0, start_idx) + 1
            text_widget.tag_add("result", f"{line_start}.0", f"{line_start}.end")
            
            text_widget.config(state=tk.DISABLED)
            
            # Кнопка закрытия
            button_frame = ttk.Frame(analysis_window, style='Modern.TFrame')
            button_frame.pack(fill=tk.X, padx=20, pady=10)
            
            ttk.Button(button_frame, text="Закрыть", 
                      command=analysis_window.destroy,
                      style='Modern.TButton').pack(side=tk.RIGHT)
            
            self.status_var.set("✅ Анализ устойчивости завершен")
            
        except Exception as e:
            self.status_var.set(f"❌ Ошибка анализа: {str(e)}")
            messagebox.showerror("Ошибка", f"Ошибка при анализе устойчивости:\n{str(e)}")
    
    def export_data(self):
        """Экспорт данных моделирования"""
        try:
            messagebox.showinfo("Экспорт данных", 
                              "Функция экспорта данных будет реализована в следующей версии")
            self.status_var.set("💾 Экспорт данных (в разработке)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте:\n{str(e)}")

def main():
    """Основная функция запуска приложения"""
    try:
        root = tk.Tk()
        
        # Установка иконки (если есть)
        try:
            root.iconbitmap("drone_icon.ico")
        except:
            pass
            
        app = ModernDroneSystemAnalysis(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")

if __name__ == "__main__":
    main()
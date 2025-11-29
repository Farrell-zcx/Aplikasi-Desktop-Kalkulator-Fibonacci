import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
from fibonacci_logic import FibonacciAnalyzer

# Konfigurasi Tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FibonacciApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analisis Kompleksitas: Fibonacci")
        self.geometry("1100x750")
        
        self.analyzer = FibonacciAnalyzer()
        self.is_running = False
        
        # Layout Grid Utama
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Fibonacci\nAnalyzer Pro", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_calculator = ctk.CTkButton(self.sidebar_frame, text="Kalkulator", command=self.show_calculator)
        self.btn_calculator.grid(row=1, column=0, padx=20, pady=10)

        self.btn_analysis = ctk.CTkButton(self.sidebar_frame, text="Analisis Grafik", command=self.show_analysis)
        self.btn_analysis.grid(row=2, column=0, padx=20, pady=10)

        self.lbl_credit = ctk.CTkLabel(self.sidebar_frame, text="Tubes Analisis\nKompleksitas", font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_credit.grid(row=5, column=0, padx=20, pady=20)

        # Frame Kalkulator 
        self.frame_calculator = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_calculator_ui()

        # Frame Analisis
        self.frame_analysis = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_analysis_ui()

        # Tampilkan default
        self.show_calculator()

    def show_calculator(self):
        self.frame_analysis.grid_forget()
        self.frame_calculator.grid(row=0, column=1, sticky="nsew")

    def show_analysis(self):
        self.frame_calculator.grid_forget()
        self.frame_analysis.grid(row=0, column=1, sticky="nsew")

    # === LOGIKA KALKULATOR ===
    def setup_calculator_ui(self):
        self.frame_calculator.grid_columnconfigure(0, weight=1)
        
        # Header
        lbl_title = ctk.CTkLabel(self.frame_calculator, text="Kalkulator Perbandingan", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input
        self.entry_n = ctk.CTkEntry(self.frame_calculator, placeholder_text="Masukkan N (misal: 30)", width=200)
        self.entry_n.grid(row=1, column=0, padx=20, pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self.frame_calculator, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=10)
        
        btn_run = ctk.CTkButton(btn_frame, text="Hitung (Bandingkan)", command=self.run_single_calculation, width=200, height=40)
        btn_run.pack()

        # Hasil Container
        self.res_frame = ctk.CTkFrame(self.frame_calculator)
        self.res_frame.grid(row=3, column=0, padx=40, pady=20, sticky="ew")
        self.res_frame.grid_columnconfigure((0, 1), weight=1)

        # Hasil Iteratif
        lbl_iter_title = ctk.CTkLabel(self.res_frame, text="ITERATIF O(n)", font=ctk.CTkFont(weight="bold", size=16), text_color="#4CC9F0")
        lbl_iter_title.grid(row=0, column=0, padx=10, pady=(10, 5))
        self.lbl_result_iter = ctk.CTkLabel(self.res_frame, text="-", font=ctk.CTkFont(size=14))
        self.lbl_result_iter.grid(row=1, column=0, padx=10, pady=(0, 10))
        self.lbl_time_iter = ctk.CTkLabel(self.res_frame, text="Waktu: -", font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_time_iter.grid(row=2, column=0, padx=10, pady=(0, 10))

        # Hasil Rekursif
        lbl_rec_title = ctk.CTkLabel(self.res_frame, text="REKURSIF O(2^n)", font=ctk.CTkFont(weight="bold", size=16), text_color="#F72585")
        lbl_rec_title.grid(row=0, column=1, padx=10, pady=(10, 5))
        self.lbl_result_rec = ctk.CTkLabel(self.res_frame, text="-", font=ctk.CTkFont(size=14))
        self.lbl_result_rec.grid(row=1, column=1, padx=10, pady=(0, 10))
        self.lbl_time_rec = ctk.CTkLabel(self.res_frame, text="Waktu: -", font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_time_rec.grid(row=2, column=1, padx=10, pady=(0, 10))

        self.lbl_note = ctk.CTkLabel(self.frame_calculator, text="⚠️ Peringatan: N > 40 pada Rekursif Naif bisa menyebabkan aplikasi hang.", text_color="#FF5555")
        self.lbl_note.grid(row=4, column=0, padx=20, pady=20)

    def run_single_calculation(self):
        try:
            n = int(self.entry_n.get())
        except ValueError:
            self.lbl_result_iter.configure(text="Error")
            return

        if n > 40:
            confirm = messagebox.askyesno("Peringatan Keras", "Menghitung Rekursif Naif untuk N > 40 akan memakan waktu SANGAT LAMA (bisa menit/jam). Yakin ingin lanjut?")
            if not confirm:
                return

        self.lbl_result_iter.configure(text="Menghitung...")
        self.lbl_result_rec.configure(text="Menghitung...")
        self.lbl_time_iter.configure(text="Waktu: ...")
        self.lbl_time_rec.configure(text="Waktu: ...")

        threading.Thread(target=self._calculate_thread, args=(n,), daemon=True).start()

    def _calculate_thread(self, n):
        # 1. Iteratif (Cepat)
        val_i, time_i = self.analyzer.measure_time(self.analyzer.iterative, n)
        self.lbl_result_iter.configure(text=f"Hasil: {val_i}")
        self.lbl_time_iter.configure(text=f"{time_i:.8f} detik")

        # 2. Rekursif
        # Kita izinkan user mencoba N=50 jika mereka memaksa, tapi risikonya ditanggung user (app freeze)
        val_r, time_r = self.analyzer.measure_time(self.analyzer.recursive_naive, n)
        self.lbl_result_rec.configure(text=f"Hasil: {val_r}")
        self.lbl_time_rec.configure(text=f"{time_r:.8f} detik")

    # === LOGIKA ANALISIS & GRAFIK ===
    def setup_analysis_ui(self):
        self.frame_analysis.grid_columnconfigure(0, weight=1)
        self.frame_analysis.grid_rowconfigure(3, weight=1)

        # Header
        lbl_title = ctk.CTkLabel(self.frame_analysis, text="Grafik Analisis Kompleksitas", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.grid(row=0, column=0, padx=20, pady=(10, 5))

        # Controls Panel
        ctrl_frame = ctk.CTkFrame(self.frame_analysis)
        ctrl_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        # Input Ranges
        grid_ctrl = ctk.CTkFrame(ctrl_frame, fg_color="transparent")
        grid_ctrl.pack(pady=10)

        ctk.CTkLabel(grid_ctrl, text="Max N (Rekursif):").grid(row=0, column=0, padx=5)
        self.entry_max_rec = ctk.CTkEntry(grid_ctrl, width=60)
        self.entry_max_rec.insert(0, "32")
        self.entry_max_rec.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(grid_ctrl, text="Max N (Iteratif):").grid(row=0, column=2, padx=5)
        self.entry_max_iter = ctk.CTkEntry(grid_ctrl, width=80)
        self.entry_max_iter.insert(0, "1000")
        self.entry_max_iter.grid(row=0, column=3, padx=5)

        # Options
        self.check_log_scale = ctk.CTkCheckBox(grid_ctrl, text="Gunakan Skala Logaritmik (Y-Axis)")
        self.check_log_scale.grid(row=0, column=4, padx=20)
        self.check_log_scale.select() # Default on biar grafik bagus

        self.btn_benchmark = ctk.CTkButton(ctrl_frame, text="MULAI ANALISIS", command=self.run_benchmark, fg_color="#2CC985", hover_color="#229965")
        self.btn_benchmark.pack(pady=(0, 10))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.frame_analysis, orientation="horizontal")
        self.progress_bar.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        # Area Grafik
        self.plot_frame = ctk.CTkFrame(self.frame_analysis, fg_color="transparent")
        self.plot_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

    def run_benchmark(self):
        if self.is_running: return
        
        try:
            max_rec = int(self.entry_max_rec.get())
            max_iter = int(self.entry_max_iter.get())
        except ValueError:
            return

        if max_rec > 40:
            confirm = messagebox.askyesno("Konfirmasi", "Max N Rekursif > 40 akan memakan waktu sangat lama. Lanjutkan?")
            if not confirm: return

        self.is_running = True
        self.btn_benchmark.configure(state="disabled", text="Sedang Berjalan...")
        self.progress_bar.set(0)
        
        threading.Thread(target=self._benchmark_thread, args=(max_rec, max_iter), daemon=True).start()

    def _benchmark_thread(self, max_rec, max_iter):
        x_rec, y_rec = [], []
        x_iter, y_iter = [], []

        # 1. Benchmark Rekursif
        # Kita batasi loop agar progress bar update
        for n in range(1, max_rec + 1):
            _, t = self.analyzer.measure_time(self.analyzer.recursive_naive, n)
            x_rec.append(n)
            y_rec.append(t)
            # Update progress (50% pertama untuk rekursif)
            prog = (n / max_rec) * 0.5
            self.after(0, lambda p=prog: self.progress_bar.set(p))

        # 2. Benchmark Iteratif
        step = 1 if max_iter < 100 else max_iter // 50
        count = 0
        total_steps = (max_iter - 1) // step + 1
        
        for n in range(1, max_iter + 1, step):
            _, t = self.analyzer.measure_time(self.analyzer.iterative, n)
            x_iter.append(n)
            y_iter.append(t)
            count += 1
            # Update progress (50% sisanya untuk iteratif)
            prog = 0.5 + (count / total_steps) * 0.5
            self.after(0, lambda p=prog: self.progress_bar.set(p))

        # Selesai
        self.after(0, lambda: self._update_graph(x_rec, y_rec, x_iter, y_iter))
        self.is_running = False

    def _update_graph(self, x_rec, y_rec, x_iter, y_iter):
        self.btn_benchmark.configure(state="normal", text="MULAI ANALISIS")
        self.progress_bar.set(1)

        # Bersihkan frame lama
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Buat Figure Matplotlib
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Plot Data
        ax.plot(x_rec, y_rec, marker='o', markersize=4, label='Rekursif Naif O(2^n)', color='#F72585')
        ax.plot(x_iter, y_iter, label='Iteratif O(n)', color='#4CC9F0', linestyle='--', linewidth=2)

        # Konfigurasi Grafik
        ax.set_title("Perbandingan Kompleksitas Waktu", fontsize=12)
        ax.set_xlabel("Ukuran Input (N)")
        ax.set_ylabel("Waktu Eksekusi (detik)")
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()

        # Log Scale Option
        if self.check_log_scale.get():
            ax.set_yscale('log')
            ax.set_ylabel("Waktu (detik) - Skala Log")

        # Embed ke Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = FibonacciApp()
    app.mainloop()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def nim_bisection_method(nim_last_digit, interval_lower, interval_upper, tolerance=1e-6):
    """
    Menyelesaikan persamaan non-linear f(x) = x^3 - 5x + C menggunakan metode Biseksi.

    Args:
        nim_last_digit (int): Digit terakhir NIM, digunakan sebagai konstanta C.
        interval_lower (float): Batas bawah interval pencarian.
        interval_upper (float): Batas atas interval pencarian.
        tolerance (float): Toleransi galat relatif untuk menghentikan iterasi.
    
    Returns:
        tuple: (akar yang ditemukan, jumlah iterasi)
    """
    # Definisikan fungsi f(x)
    def f(x):
        return x**3 - 5*x + nim_last_digit

    a = interval_lower
    b = interval_upper
    
    # Periksa apakah ada akar dalam interval
    if f(a) * f(b) >= 0:
        print("Peringatan: Fungsi memiliki tanda yang sama di batas interval. Menggunakan interval valid [-3, -2].")
        a = -3.0
        b = -2.0

    iter_data = []
    x_mid_prev = 0
    iteration = 0
    relative_error = float('inf')

    print("Iterasi dimulai...")
    
    while relative_error > tolerance:
        iteration += 1
        x_mid = (a + b) / 2
        
        if iteration > 1:
            relative_error = abs((x_mid - x_mid_prev) / x_mid) * 100
        
        fx_mid = f(x_mid)
        iter_data.append([iteration, a, b, x_mid, fx_mid, relative_error])

        if f(a) * fx_mid < 0:
            b = x_mid
        else:
            a = x_mid
        
        x_mid_prev = x_mid
    
    df = pd.DataFrame(iter_data, columns=['Iterasi', 'a', 'b', 'x_mid', 'f(x_mid)', 'Error (%)'])
    pd.set_option('display.max_rows', None)
    pd.set_option('display.precision', 6)
    print(df.to_string(index=False))
    print("\nIterasi selesai.")

    final_root = x_mid
    return final_root, iteration

# --- Program Utama ---
nim_last_digit = 7
nim_last_two_digits = 67
interval_upper_bound = nim_last_two_digits / 10.0
interval_lower_bound = 0.0

# Bagian baru: Meminta input toleransi dari pengguna
try:
    user_tolerance = float(input("Masukkan toleransi error (misal, 0.01 untuk 0.01%): "))
except ValueError:
    print("Input tidak valid. Menggunakan toleransi default 0.01%.")
    user_tolerance = 0.01

root, iterations = nim_bisection_method(nim_last_digit, interval_lower_bound, interval_upper_bound, user_tolerance)

# Tampilkan hasil akhir
if root is not None:
    print(f"\nAKAR DITEMUKAN: {root:.6f}")
    print(f"Jumlah iterasi: {iterations}")

    # --- Bagian Grafik ---
    fig, ax = plt.subplots(figsize=(8, 6))

    x_vals_plot = np.linspace(-2, 2, 400)
    y_vals_plot = x_vals_plot**3 - 5*x_vals_plot + nim_last_digit
    ax.plot(x_vals_plot, y_vals_plot, label=f'$f(x) = x^3 - 5x + {nim_last_digit}$')

    ax.axhline(0, color='black', linewidth=0.5)
    
    ax.plot(root, 0, 'ro', markersize=8, label=f'Akar ≈ {root:.4f}')

    ax.set_title(f'Grafik $f(x) = x^3 - 5x + {nim_last_digit}$ dan Posisi Akar')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True)
    plt.show()

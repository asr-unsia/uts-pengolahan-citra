import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt


# Fungsi untuk membaca gambar dan mengonversi ke grayscale
def read_and_convert_image(filepath):
    """
    Membaca gambar dari file dan mengonversinya ke bentuk grayscale.

    Parameters:
    filepath (str): Lokasi file gambar.

    Returns:
    tuple: Gambar asli dan gambar grayscale.
    """
    # Membaca gambar dari jalur yang diberikan
    image = iio.imread(filepath)

    # Jika gambar berwarna (3 channel), konversi ke grayscale
    if len(image.shape) == 3:
        # Menggunakan bobot untuk konversi RGB ke grayscale
        gray_image = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
    else:
        # Jika sudah grayscale, kembalikan gambar tanpa perubahan
        gray_image = image

    return image, gray_image


# Fungsi untuk melakukan histogram equalization
def histogram_equalization(img):
    """
    Menerapkan histogram equalization untuk meningkatkan kontras citra.

    Parameters:
    img (numpy.ndarray): Citra grayscale input.

    Returns:
    numpy.ndarray: Citra setelah histogram equalization.
    """
    # Menghitung histogram citra
    hist, _ = np.histogram(img.flatten(), 256, [0, 256])

    # Menghitung cumulative distribution function (CDF)
    cdf = hist.cumsum()

    # Masking nilai CDF yang sama dengan nol
    cdf_m = np.ma.masked_equal(cdf, 0)

    # Normalisasi CDF
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())

    # Mengisi nilai yang ter-mask dengan nol
    cdf = np.ma.filled(cdf_m, 0).astype("uint8")

    # Menerapkan CDF ke citra untuk mendapatkan citra yang telah di-equalize
    img_equalized = cdf[img.astype("uint8")]
    return img_equalized


# Fungsi untuk meningkatkan kontras citra
def contrast_stretching(img, contrast_level):
    """
    Menerapkan peningkatan kontras pada citra dengan level tertentu.

    Parameters:
    img (numpy.ndarray): Citra grayscale input.
    contrast_level (float): Level kontras.

    Returns:
    numpy.ndarray: Citra dengan kontras yang sudah ditingkatkan.
    """
    # Normalisasi nilai piksel ke rentang [0, 1]
    image_normalized = img / 255.0

    # Menerapkan peningkatan kontras dengan mengalikan dengan faktor
    image_contrast = np.clip(image_normalized * contrast_level, 0, 1)

    # Mengembalikan citra ke rentang piksel [0, 255]
    return (image_contrast * 255).astype("uint8")


# Fungsi untuk memproses dan menampilkan hasil histogram equalization
def histogram_result(img_path, title):
    """
    Memproses citra dengan histogram equalization,
    kemudian menampilkan hasilnya.

    Parameters:
    img_path (str): Lokasi file gambar.
    title (str): Judul untuk hasil yang ditampilkan.
    """
    print("=" * 100)
    print(title.upper())
    print("-" * 100)

    # Membaca dan mengonversi gambar
    image, gray_image = read_and_convert_image(img_path)

    # Menerapkan histogram equalization pada citra grayscale
    equalized_image = histogram_equalization(gray_image)

    # Menampilkan citra asli, citra grayscale, citra setelah histogram equalization, dan citra dengan peningkatan kontras
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(image)
    plt.title("Citra Asli")
    plt.axis("off")  # Menyembunyikan sumbu

    plt.subplot(1, 3, 2)
    plt.imshow(gray_image, cmap="gray")
    plt.title("Citra Grayscale")
    plt.axis("off")  # Menyembunyikan sumbu

    plt.subplot(1, 3, 3)
    plt.imshow(equalized_image, cmap="gray")
    plt.title("Citra Setelah Histogram Equalization")
    plt.axis("off")  # Menyembunyikan sumbu

    plt.tight_layout()  # Mengatur tata letak subplot agar lebih rapi
    plt.show()  # Menampilkan semua subplot

    print("=" * 100)


# Fungsi untuk memproses dan menampilkan hasil histogram dan contrast
def histogram_and_contrast_result(img_path, contrast_level, title):
    """
    Memproses citra dengan histogram equalization dan peningkatan kontras,
    kemudian menampilkan hasilnya.

    Parameters:
    img_path (str): Lokasi file gambar.
    contrast_level (float): Level kontras.
    title (str): Judul untuk hasil yang ditampilkan.
    """
    print("=" * 100)
    print(title.upper())
    print("-" * 100)

    # Membaca dan mengonversi gambar
    image, gray_image = read_and_convert_image(img_path)

    # Menerapkan histogram equalization pada citra grayscale
    equalized_image = histogram_equalization(gray_image)

    # Menerapkan peningkatan kontras dengan level sesuai parameter input
    contrast_image = contrast_stretching(gray_image, contrast_level)

    # Menampilkan citra asli, citra grayscale, citra setelah histogram equalization, dan citra dengan peningkatan kontras
    plt.figure(figsize=(10, 5))

    plt.subplot(2, 2, 1)
    plt.imshow(image)
    plt.title("Citra Asli")
    plt.axis("off")  # Menyembunyikan sumbu

    plt.subplot(2, 2, 2)
    plt.imshow(gray_image, cmap="gray")
    plt.title("Citra Grayscale")
    plt.axis("off")  # Menyembunyikan sumbu

    plt.subplot(2, 2, 3)
    plt.imshow(equalized_image, cmap="gray")
    plt.title("Citra Setelah Histogram Equalization")
    plt.axis("off")  # Menyembunyikan sumbu

    plt.subplot(2, 2, 4)
    plt.imshow(contrast_image, cmap="gray")
    plt.title("Citra Setelah Peningkatan Kontras (Level 1.5)")
    plt.axis("off")  # Menyembunyikan sumbu

    plt.tight_layout()  # Mengatur tata letak subplot agar lebih rapi
    plt.show()  # Menampilkan semua subplot

    print("=" * 100)


# Percobaan 1 - Histogram Equalization
histogram_result("image.png", "Percobaan 1 - Histogram Equalization")
# Percobaan 2 - Histogram Equalization
histogram_result("GO48R.png", "Percobaan 2 - Histogram Equalization")

print("\n")

# Percobaan 1 - Histogram Equalization & Contrast Stretching
histogram_and_contrast_result(
    "image.png", 1.5, "Percobaan 1 - Histogram Equalization & Contrast Stretching"
)
# Percobaan 2 - Histogram Equalization & Contrast Stretching
histogram_and_contrast_result(
    "GO48R.png", 1.5, "Percobaan 2 - Histogram Equalization & Contrast Stretching"
)

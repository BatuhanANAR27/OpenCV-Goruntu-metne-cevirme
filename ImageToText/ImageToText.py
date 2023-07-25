import cv2
import pytesseract

# Tesseract OCR için tesseract.exe'nin yolunu belirtmeniz gerekebilir.
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\batuh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Görüntüyü yükle
    image = cv2.imread(image_path)
    # Görüntüyü gri tonlamaya dönüştür
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Gürültüyü azaltmak için Gaussian bulanıklaştırma uygula
    blurred = cv2.GaussianBlur(gray, (1,1), 0)

    # Görüntüdeki kenarları tespit etmek için Canny kenar tespiti uygula
    edges = cv2.Canny(gray, threshold1=30, threshold2=150)

    # Kontürleri bul
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    extracted_texts = []
    roi_coordinates = []  # ROI koordinatlarını saklamak için bir liste oluştur

    for i, contour in enumerate(contours):
        # Kontur alanını hesapla
        area = cv2.contourArea(contour)
        # Küçük alanları filtrele
        if area > 1000:
            # ROI'yi dikdörtgen içine al
            x, y, w, h = cv2.boundingRect(contour)
            roi = image[y:y+h, x:x+w]

            # ROI'yi OCR ile metne çevir
            text = pytesseract.image_to_string(roi, lang='tur')
            extracted_texts.append(text)

            # ROI'nin çevresine bir dikdörtgen çiz
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Koordinatları ve numaraları yazdır
            text_to_display = f"({x}, {y}) - Width: {w}, Height: {h} - {i+1}"
            cv2.putText(image, text_to_display, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Bulunan ROI'nin koordinatlarını roi_coordinates listesine ekle
            roi_coordinates.append((x, y, w, h))

    # Görüntü üzerindeki tüm dikdörtgenleri, koordinatları ve numaraları görselleştir
    cv2.imshow("Detected ROIs", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return extracted_texts, roi_coordinates  # ROI koordinatlarını çıktı olarak döndür

# Görüntü yolu
image_path = 'rapor8.jpeg'

extracted_texts, roi_coordinates = extract_text_from_image(image_path)
for text in extracted_texts:
    print(text)

print("ROI Koordinatları:")
print(roi_coordinates)

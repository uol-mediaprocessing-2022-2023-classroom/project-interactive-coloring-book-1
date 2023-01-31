import cv2
import numpy as np
import cv2 as cv
import numpy
from PIL import Image
from matplotlib import pyplot as plt
from skimage import segmentation
from skimage.color import label2rgb


# erstellt pixel matrix in Größe des Bildes: 0 = unbenutzt, 1 = benutzt
def createPixelList(size_x_1, size_y_1):
    pixel_list = numpy.zeros((size_x_1, size_y_1))
    return pixel_list


# erstellt pixel matrix in Größe des Bildes: 0 = unbenutzt, 1 = benutzt
def createZonePixelList(size_x_1, size_y_1):
    zone_pixel_list = numpy.zeros((size_x_1, size_y_1))
    return zone_pixel_list


# überprüft Nachbarn des Pixels
def checkNeighbour(x, y, pixel_matrix, pixel_zone_matrix, pixel_colour, colour_of_zone, size_x, size_y, index_of_zone,
                   colour_toleranz):
    # erstellt Array der Zone [x,y]
    zone = []
    # erstellt Warteschlangenarray [x,y]
    queue_to_check = [[x, y]]
    # hakt Pixel ab, dass er einer Zone hinzugefügt wurde
    pixel_matrix[x, y] = True
    # trägt dem Pixel seine Zone als Integer ein
    pixel_zone_matrix[x, y] = index_of_zone

    # solange ein Pixel in der Warteschlange ist
    while len(queue_to_check) >= 1:
        # übernimmt ersten Pixel aus der Warteschlange, entfernt diesen dort und fügt Zone hinzu
        x_to_check = queue_to_check[0][0]
        y_to_check = queue_to_check[0][1]
        queue_to_check.pop(0)
        zone.append([x_to_check, y_to_check])

        # prüft von-Neumann-Nachbarn oben
        if y_to_check != 0 and not pixel_matrix[x_to_check, y_to_check - 1]:
            # nehme Farbe des zu prüfenden Pixels und schaue, ob diese im Toleranz Bereich zur Zone liegt
            colour = pixel_colour[x_to_check, y_to_check - 1]
            if colour_of_zone[0] + colour_toleranz >= colour[0] >= colour_of_zone[0] - colour_toleranz and \
                    colour_of_zone[1] + colour_toleranz >= colour[1] >= \
                    colour_of_zone[1] - colour_toleranz and colour_of_zone[2] + colour_toleranz >= colour[2] >= \
                    colour_of_zone[2] - colour_toleranz:
                # füge Pixel zur Warteschlange hinzu, trage ihn als Zone zugewiesen ein und trage Zonen index ein
                queue_to_check.append([x_to_check, y_to_check - 1])
                pixel_matrix[x_to_check, y_to_check - 1] = True
                pixel_zone_matrix[x_to_check, y_to_check - 1] = index_of_zone
        # prüft von-Neumann-Nachbarn rechts
        if x_to_check + 1 < size_x and not pixel_matrix[x_to_check + 1, y_to_check]:
            # nehme Farbe des zu prüfenden Pixels und schaue, ob diese im Toleranz Bereich zur Zone liegt
            colour = pixel_colour[x_to_check + 1, y_to_check]
            if colour_of_zone[0] + colour_toleranz >= colour[0] >= colour_of_zone[0] - colour_toleranz and \
                    colour_of_zone[1] + colour_toleranz >= colour[1] >= \
                    colour_of_zone[1] - colour_toleranz and colour_of_zone[2] + colour_toleranz >= colour[2] >= \
                    colour_of_zone[2] - colour_toleranz:
                # füge Pixel zur Warteschlange hinzu, trage ihn als Zone zugewiesen ein und trage Zonen index ein
                queue_to_check.append([x_to_check + 1, y_to_check])
                pixel_matrix[x_to_check + 1, y_to_check] = True
                pixel_zone_matrix[x_to_check + 1, y_to_check] = index_of_zone
        # prüft von-Neumann-Nachbarn unten
        if y_to_check + 1 < size_y and not pixel_matrix[x_to_check, y_to_check + 1]:
            # nehme Farbe des zu prüfenden Pixels und schaue, ob diese im Toleranz Bereich zur Zone liegt
            colour = pixel_colour[x_to_check, y_to_check + 1]
            if colour_of_zone[0] + colour_toleranz >= colour[0] >= colour_of_zone[0] - colour_toleranz and \
                    colour_of_zone[1] + colour_toleranz >= colour[1] >= \
                    colour_of_zone[1] - colour_toleranz and colour_of_zone[2] + colour_toleranz >= colour[2] >= \
                    colour_of_zone[2] - colour_toleranz:
                # füge Pixel zur Warteschlange hinzu, trage ihn als Zone zugewiesen ein und trage Zonen index ein
                queue_to_check.append([x_to_check, y_to_check + 1])
                pixel_matrix[x_to_check, y_to_check + 1] = True
                pixel_zone_matrix[x_to_check, y_to_check + 1] = index_of_zone
        # prüft von-Neumann-Nachbarn links
        if x_to_check != 0 and not pixel_matrix[x_to_check - 1, y_to_check]:
            # nehme Farbe des zu prüfenden Pixels und schaue, ob diese im Toleranz Bereich zur Zone liegt
            colour = pixel_colour[x_to_check - 1, y_to_check]
            if colour_of_zone[0] + colour_toleranz >= colour[0] >= colour_of_zone[0] - colour_toleranz and \
                    colour_of_zone[1] + colour_toleranz >= colour[1] >= \
                    colour_of_zone[1] - colour_toleranz and colour_of_zone[2] + colour_toleranz >= colour[2] >= \
                    colour_of_zone[2] - colour_toleranz:
                # füge Pixel zur Warteschlange hinzu, trage ihn als Zone zugewiesen ein und trage Zonen index ein
                queue_to_check.append([x_to_check - 1, y_to_check])
                pixel_matrix[x_to_check - 1, y_to_check] = True
                pixel_zone_matrix[x_to_check - 1, y_to_check] = index_of_zone
    return zone, pixel_matrix, pixel_zone_matrix


'''
    wendet k-Means auf das übergebene Bild an, was das Bild in eine festgelegte Anzahl von Farben einteilt

    Parameters
    ----------
    img : numpy.ndarray
        Das zu bearbeitende Bild als numpy.ndarray
    blur_kernel_size : int
        Die Grösse die der Kernel für das Blurren mit dem Gaussfilter haben soll
        
    Returns
    -------
    result_img : numpy.ndarray
        Das mit kmeans bearbeitete Bild wird als numpy.ndarray in BGR zurückgegeben
'''


def k_means(img, blur_kernel_size, k):
    # das Bild wird geblurrt, zur besseren Weiterverarbeitung
    img = cv2.GaussianBlur(img, (blur_kernel_size, blur_kernel_size), 0)

    # dasd Bildarray wird umgeformt und zu float32 konvertiert (ist durch cv2 unit8)
    tmp_img = img.reshape((-1, 3))
    tmp_img = np.float32(tmp_img)

    # die Kriterien und die Anzahl der Farben für kmeans werden definiert und kmeans dann angewendet
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    ret, label, center = cv.kmeans(tmp_img, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    # das Bildarray wird wieder zurück in uint8 konvertiert und wieder in die ursprüngliche Form umgeformt
    center = np.uint8(center)
    res = center[label.flatten()]
    result_img = res.reshape(img.shape)

    # das Resultat wird zurückgegeben
    return result_img


'''
    Findet alle Zonen in einem Bild die kleiner sind, als der übergegebene Schwellenwert und übertragt diese Zonen
    an gleicher Stelle in ein zweites gleich grösses Bild in der angegebenen Farbe
    
    Anmerkung: Für unsere Zwecke wäre es zwar sinnvoller gewesen direkt ein Binary oder Grayscale Bild zu erstellen,
    anstatt ein schwarz-weiss Bild, das trotzdem in RGB codiert ist. Jedoch funktioniert die CheckNeighbour-Methode
    nur mit RGB-Bildern und um diese nicht extra umschreiben zu müssen, wird das Bild in RGB erstellt und dann 
    umgewandelt

    Parameters
    ----------
    img1 : PIL.Image.Image
        Das erste Bild in denen die Zonen gesucht werden soll
    img2 : PIL.Image.Image
        Das zweite Bild in denen die Zonen übertragen werden sollen
    size_x
        die Breite der Bilder
    size_y 
        die Höhe der Bilder
    zone_size_threshold
        der Schwellenwert für die Zonengrösse
    color_code
        der Farbcode für die Färbung der Zellen

    Returns
    -------
    img_2 : PI.Image.Image
        das zweite Bild wird mit den neu übertragen Zonen zurückgegeben
'''


def find_zones_and_color_them(img1, img2, size_x, size_y, zone_size_threshold, color_code):
    # Spielraum der Farbe
    colour_toleranz = 0

    # lädt Matrix mit Pixel Farben
    pixel_colour = img1.load()

    # erstellt eine Liste für alle Zonen, die erkannt werden
    zone_list = []

    # erstellt boolean Matrix in größe des Bildes um erkannte Pixel abzuhaken
    pixel_matrix = createPixelList(size_x, size_y)

    # erstellt integer Matrix in größe des Bildes, um Zone des Pixels einzutragen
    pixel_zone_matrix = createZonePixelList(size_x, size_y)

    # Zonen Index, um den verschiedenen Pixeln eine Zone zuzuweisen
    index_of_zone = 0

    # gehe Pixel für Pixel des Bildes durch
    for x in range(0, size_x):
        for y in range(0, size_y):
            # wenn der Pixel zu keiner Zone gehört, suche alle Pixel, die aneinander liegen und dieselbe Farbe haben
            if not pixel_matrix[x, y]:
                colour_of_zone = pixel_colour[x, y]
                zone, pixel_matrix, pixel_zone_matrix = checkNeighbour(x, y, pixel_matrix, pixel_zone_matrix,
                                                                       pixel_colour, colour_of_zone, size_x, size_y,
                                                                       index_of_zone, colour_toleranz)
                zone_list.append(zone)

                # erhöht Zonen Index nach erkannter Zone
                index_of_zone = index_of_zone + 1

    # Array zur Speicherung der Zonen die kleiner als zoneSizeThreshold sind
    zone_list_small = []

    # fügt zone_list_small die Zonen zu, die kleiner als zoneSizeThreshold sind
    for p in range(0, len(zone_list)):
        if len(zone_list[p]) < zone_size_threshold:
            zone_list_small.append(zone_list[p])

    # die Zonen die kleiner als der Threshold sind, werden als weisse Zonen an den gleichen Koordinaten,
    # die sie im Ursprungs-Bild haben, in das RGB-Bild übertragen
    for p in range(0, len(zone_list_small)):
        for q in range(0, len(zone_list_small[p])):
            img2.putpixel((zone_list_small[p][q][0], zone_list_small[p][q][1]), color_code)

    return img2


'''
    Erstellt eine Maske des Bildes zur Weiterbearbeitung mit SLIC.
    Alle Bereiche die grösser als der Threshold sind werden maskiert, damit SLIC diese nicht beachtet
    Zudem werden Löcher in der Maske geschlossen die kleiner als 1000px sind

    Parameters
    ----------
    img : numpy.ndarray
        Das zu bearbeitende Bild als numpy.ndarray
    zone_size_threshold : int
        Der Schwellenwert den die Zonen unterbieten müssen, um nicht maskiert zu werden

    Returns
    -------
    result_mask : numpy.ndarray
        Die erstellte Maske wird als numpy.ndarray in Grayscale zurückgegeben
'''


def create_mask(img, zone_size_threshold):
    # das numpy.ndarray wird zu PIL.Image.Image umgewandelt
    img = Image.fromarray(img)
    # breite und höhe des Bildes
    size_x, size_y = img.size
    # erstellt ein komplett schwarzes RGB-Bild als PIL.Image.Image, welches die gleiche Grösse hat, wie unser Bild
    mask = Image.new("RGB", (size_x, size_y), (0, 0, 0))
    # Erstellung der Maske
    mask = find_zones_and_color_them(img, mask, size_x, size_y, zone_size_threshold, (255, 255, 255))
    # Abspeicherung des Bildes zu Testzwecken
    mask.save("pictures/testResults/testMask.png")

    # Umwandlung des PIL.Image.Image zu numpy.ndarray zur Weiterverarbeitung
    result_mask = np.array(mask)
    # Umwandlung des numpy.array von rgb in grayscale
    result_mask = rgb2gray(result_mask)

    # Schliessen von Löchern in der Maske
    result_closed_mask = find_zones_and_color_them(mask, mask, size_x, size_y, 1000, (0, 0, 0))
    # Umwandlung des PIL.Image.Image zu numpy.ndarray zur Weiterverarbeitung
    result_closed_mask = np.array(result_closed_mask)
    # Umwandlung des numpy.array von rgb in grayscale
    result_closed_mask = rgb2gray(result_closed_mask)

    # Abspeicherung des Bildes zu Testzwecken
    cv2.imwrite("pictures/testResults/testClosedMask.png", result_closed_mask)


    # das Resultat wird zurückgegeben (zurzeit zu Testzwecken die Maske mit und ohne LÖcher) (TODO: Ändern)
    return result_mask, result_closed_mask


'''
    Quelle: https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
    Wandelt ein rgb-numpy array in grayscale um
    
    Parameters
    ---------
    
    rgb : numpy.ndarray
        das Bild das umgewandelt werden als numpy.ndarray in rgb
    
    Returns
    -------
    
    gray : numpy.ndarray
        das umgewandelte Bild als numpy.ndarray in grayscale
'''
def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


'''
    Wendet mit Hilfe einer Maske SLIC auf das zu bearbeitende Bild an.
    Die Maske sorgt dafür, das SLIC nur auf relevante Teile angewandt wird
    und nicht auf grosse einfarbige Segmente des Bildes.
    SLIC sorgt dafür, dass das Bild in Superpixel aufgeteilt wird

    Parameters
    ----------
    img : numpy.ndarray
        Das zu bearbeitende Bild als numpy.ndarray in BGR
    mask : numpy.ndarray
        Die Maske die verwendet werden soll als numpy.ndarray in Grayscale
        
    Returns
    -------
    result_img : PIL.Image.Image
        Der unmaskierte Teil des Bildes der mit SLIC bearbeitet wurde, wird als PIL.Image.Image zurückgegeben
'''


def mask_slic(img, mask, slic_segments):
    # opencv benutzt standardmässig BGR, wir brauchen nun aber RGB: Daher wird das Bild nun in RGB konvertiert
    tmp_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # SLIC wird auf den unmaskierten Teil des Bildes angewandt und das Bild wird in Superpixel segmentiert
    m_slic = segmentation.slic(tmp_img, n_segments=slic_segments, mask=mask, compactness=1)

    # die durchschnittliche Farbe eines Superpixel wird nun verwendet um diesen Superpixel auszufüllen
    tmp_img = label2rgb(m_slic, tmp_img, kind='avg')

    # wandelt das numpy.ndarray zu PIL.Image.Image um (Grund: für die Weiterverarbeitung wird eine Image Datei und
    # kein Array benötigt)
    result_img = Image.fromarray(tmp_img, 'RGB')

    # Abspeicherung des Bildes zu Testzwecken
    result_img.save("pictures/testResults/testSLIC.png")

    # das Resultat wird zurückgegeben
    return result_img


'''
    Quelle: https://www.geeksforgeeks.org/create-transparent-png-image-with-python-pillow/
    Legt das durch SLIC erstellte Bild, welches durch die Maske nur ein Ausschnitt des gesamten Bildes ist, über
    das mit kMeans erstellte Bild, um wieder ein vollständiges Bild zu erhalten

    Parameters
    ----------
    foreground : PIL.Image.Image
        Der von SLIC bearbeitete Ausschnitt des Bildes der über das von kMeans erstellte Bild gelegt wird, als 
        PIL.Image.Image
    background : numpy.ndarray
        Das von kMeans erstellte Bild, auf das der Ausschnit gelegt wird, als numpy.ndarray

    Returns
    -------
    result_img : PIL.Image.Image
        Das zusammengefügte Bild als PIL.Image.Image
'''


def combine_mask_slic_and_kmeans(foreground, background):
    # konvertiert den Vordergrund zur RGBA
    foreground_rgba = foreground.convert("RGBA")

    # das Bild wird in eine eindimensionale Sequenz von Pixeln gewandelt
    datas = foreground_rgba.getdata()

    new_data = []

    # findet anhand des RGBA-Wertes schwarze Farbe, und speichert diese dann anstatt schwarz als transparent ab
    # andere Farben bleiben unverändert
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    # die eindimensionale Sequenz von Pixeln wird wieder in ein Bild umgewandelt
    foreground_rgba.putdata(new_data)

    # der Hintergrund ist in BGR und muss in RGB umgewandelt
    background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)

    # der Hintergrund wird von numpy.ndarray in PIL.Image.Image umgewandelt
    background = Image.fromarray(background)

    # Fügt den Vordergrund auf den Hintergrund ein
    # fängt bei den Koordinaten (0,0) an
    background.paste(foreground_rgba, (0, 0), mask=foreground_rgba)

    result_img = background

    # Abspeicherung des Bildes zu Testzwecken
    result_img.save("pictures/testResults/testSLICandKCombined.png")

    # das Resultat wird zurückgegeben
    return result_img


# Main Methode
def main():
    img = cv.imread('pictures/wild.jpg')

    # Variablen defininiere, für Schwierigkeitsgrad ggf. ändern
    first_blur = 17
    second_blur = 11
    zone_size_threshold = 75000
    slic_segments = 1000
    k = 12

    # Bild in Farbbereiche aufteilen
    k_means_img = k_means(img, first_blur, k)

    # Abspeicherung des Bildes
    cv.imwrite("pictures/testResults/testKMeans.png", k_means_img)

    # erstellt eine Maske für SLIC
    mask, closed_mask = create_mask(k_means_img, zone_size_threshold)

    # superpixel erstellen
    slic_img = mask_slic(k_means_img, mask, slic_segments)

    # Kombinierung der von SLIC und k-means erstellten Bilder
    img = combine_mask_slic_and_kmeans(slic_img, k_means_img)

    # PIL.Image.Image in numpy.ndarray umwandeln
    img = numpy.array(img)

    # numpy.ndarray wird von RGB in BGR umgewandelt
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # kombinierte Bild noch einmal in die Farbbereiche aufteilen
    result = k_means(img, second_blur, k)

    # Abspeicherung des Bildes
    cv.imwrite("pictures/wildResult.jpg", result)


    # superpixel erstellen
    slic_img = mask_slic(k_means_img, closed_mask, slic_segments)

    # Kombinierung der von SLIC und k-means erstellten Bilder
    img = combine_mask_slic_and_kmeans(slic_img, k_means_img)

    # PIL.Image.Image in numpy.ndarray umwandeln
    img = numpy.array(img)

    # numpy.ndarray wird von RGB in BGR umgewandelt
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # kombinierte Bild noch einmal in die Farbbereiche aufteilen
    result = k_means(img, second_blur, k)

    # Abspeicherung des Bildes
    cv.imwrite("pictures/wildResult1.jpg", result)


if __name__ == "__main__":
    main()

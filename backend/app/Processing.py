import cv2
import numpy as np
import cv2 as cv
import numpy
from PIL import Image
from skimage import segmentation
import matplotlib.image as mpimg
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

def kMeans(img, blurKernel):
    img = cv2.GaussianBlur(img, (blurKernel, blurKernel), 0)

    Z = img.reshape((-1, 3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 12
    ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    img = res.reshape((img.shape))
    return img

# Main Methode
def main():

    img = cv.imread('mountains.jpg')

    img = kMeans(img, 17)

    cv.imwrite("testK1.png", img)


    # Spielraum der farbe
    colour_toleranz = 0

    # liest kmeans Bild ein und lädt Matrix mit Pixel Farben
    img = Image.fromarray(img)
    pixel_colour = img.load()

    # erstellt eine Liste für alle Zonen, die erkannt werden
    zone_list = []

    # breite und höhe des Bildes
    size_x, size_y = img.size

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

    zone_list_small = []


    for p in range(0, len(zone_list)):
        if 50 < len(zone_list[p]) < 50000:
            zone_list_small.append(zone_list[p])

    mask = Image.new("1", (size_x, size_y), 0)

    for p in range(0, len(zone_list_small)):
        for l in range(0, len(zone_list_small[p])):
            mask.putpixel((zone_list_small[p][l][0], zone_list_small[p][l][1]), 1)

    mask.save("testMask.png")

    img = cv2.imread("testMask.png", cv2.IMREAD_UNCHANGED)

    mask = img
    kernel = np.ones((5, 5), np.uint8)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    print(opening.shape)

    cv2.imwrite("testClosedMask.png", closing)

    img = mpimg.imread('testK1.png')

    print(img.shape)

    mask = mpimg.imread('testClosedMask.png')

    print(mask.shape)

    m_slic = segmentation.slic(img, n_segments=1000, mask=mask, compactness=1)

    src = label2rgb(m_slic, img, kind='avg')

    mpimg.imsave("testSLIC.png", src)



if __name__ == "__main__":
    main()



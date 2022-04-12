import PIL as pil
from PIL import Image
from PIL import ImageTk 


def nbrCol(matrice):
    return(len(matrice[0]))


def nbrLig(matrice):
    return len(matrice)


def saving(matPix, filename):
    #sauvegarde l'image contenue dans matpix dans le fichier filename
	#utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad = pil.Image.open(filename)
    mat = [[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat


def creerQRC():
    qRCode = [[1 for i in range(25)] for i in range(25)]
    # création des carrées pleins
    y = - 1
    for i in range(0, 7):
        x = 0
        y += 1
        for j in range(0, 7):
            qRCode[y][x] = 0
            x += 1
    y = -1
    for i in range(0, 7):
        x = 18
        y += 1
        for j in range(0, 7):
            qRCode[y][x] = 0
            x += 1
    y = 17
    for i in range(0, 7):
        x = 0
        y += 1
        for j in range(0, 7):
            qRCode[y][x] = 0
            x += 1
    # création des lignes en poitillés
    for i in range(6, 18, 2):
        qRCode[6][i] = 0
    for i in range(6, 18, 2):
        qRCode[i][6] = 0
    # création des lignes blanche intra-carrées
    for i in range(1, 6):
        # ligne du haut
        qRCode[1][i] = 1
    for i in range(1, 6):
        #ligne de gauche
        qRCode[i][1] = 1
    for i in range(1, 6):
        # ligne de droite
        qRCode[i][5] = 1
    for i in range(1, 6):
        # ligne du bas
        qRCode[5][i] = 1
    # Deuxième carré lignes blanches
    for i in range(19, 24):
        # ligne du haut
        qRCode[1][i] = 1
    for i in range(1, 6):
        # ligne de gauche
        qRCode[i][19] = 1
    for i in range(1, 6):
        # ligne de droite
        qRCode[i][23] = 1
    for i in range(19, 24):
        # ligne du bas
        qRCode[5][i] = 1
    # Troisième carré lignes blanches
    for i in range(1, 6):
        # ligne du haut
        qRCode[19][i] = 1
    for i in range(19, 24):
        # ligne de gauche 
        qRCode[i][1] = 1
    for i in range(19, 24):
        # ligne de droite
        qRCode[i][5] = 1
    for i in range(1, 6):
        # ligne du bas
        qRCode[23][i] = 1
    return qRCode


def rotationQRC(matrice):
    matrice1 = [[1 for i in range(25)] for j in range(25)]
    for i in range(25):
        ligne = []
        for j in range(25):
            ligne.append(matrice[j][i])
        ligne.reverse()
        matrice1[i] = ligne
    return matrice1

def extraireCoin(matrice, taillecoin):
    """Fonction qui prend une matrice de pixel et qui en sort les 4 coins sous forme de liste."""
    coinGaucheHaut = [[matrice[i][j] for i in range(0, taillecoin)] for j in range(0, taillecoin)]
    coinDroitHaut = [[matrice[i][j] for i in range(0, taillecoin)] for j in range(len(matrice) - taillecoin, len(matrice))]
    coinGaucheBas = [[matrice[i][j] for i in range(len(matrice) - taillecoin, len(matrice))] for j in range(0, taillecoin)]
    return (coinGaucheHaut, coinDroitHaut, coinGaucheBas)

def verifQRC(matrice):
    """Fonction qui compare les coins d'une matrice de pixels et qui les compare à un QRCODE.
    Si la matrice est bien un QRcode, elle le tourne pour qu'il puisse être dans le bon sens."""
    averif = extraireCoin(matrice, 7)
    temoin = extraireCoin(creerQRC(), 7)
    while averif != temoin:
        matrice = rotationQRC(matrice)
        averif = extraireCoin(matrice, 7)
    return matrice


def verifLignesQRC(matrice):
    check = True
    for i in range(6, 18):
        if matrice[6][i] != (i % 2):
            check = False
    for i in range(6, 18):
        if matrice[i][6] != (i % 2):
            check = False
    return check


def correctionHamming(bits):
    print(bits, "bit avant correction")
    # calcul bits de controle
    p1 = bits[0] ^ bits[1] ^ bits[2]
    p2 = bits[0] ^ bits[2] ^ bits[3]
    p3 = bits[1] ^ bits[2] ^ bits[3]
    # position erreur
    num = int(p1 != bits[4]) + int(p2 != bits[5]) * 2 + int(p3 != bits[6]) * 4
    print(num, "num")
    if num == 3:
        bits[0] = int(not bits[0])
    if num == 5:
        bits[1] = int(not bits[1])
    if num == 6:
        bits[2] = int(not bits[2])
    if num == 7:
        bits[3] = int(not bits[3])
    print(bits, "bit après correction")
    return bits[:4]


def filtre(matrice):
    """Fonction qui vérifie le filtre et son type et qui applique ce filtre au pixel du QRC"""
    # filtre = matrice[23][8] << 1 | matrice[22][8]
    filtre = 4
    matriceFiltre = [[0 for j in range(0, 14)] for i in range(0, 16)]
    if filtre == 0:
        print("filtre de type 0")
        return matrice
    elif filtre == 1:
        print("filtre de type 1")
        for i in range(0, 16):
            for j in range(0, 14):
                if (i + j) % 2 == 1:
                    matriceFiltre[i][j] = 1
    elif filtre == 2:
        print("filtre de type 2")
        for i in range(0, 16):
            for j in range(0, 14):
                if i % 2 == 1:
                    matriceFiltre[i][j] = 1
    elif filtre == 3:
        print("filtre de type 3")
        for i in range(0, 16):
            for j in range(0, 14):
                if j % 2 == 1:
                    matriceFiltre[i][j] = int(not matriceFiltre[i][j])
    for i in range(len(matriceFiltre)):
        for j in range(len(matriceFiltre[0])):
            x1, y1 = len(matrice[0]) - 1, len(matrice) - 1
            x2, y2 = len(matriceFiltre[0]) - 1, len(matriceFiltre) - 1
            matrice[y1 - i][x1 - j] = matrice[y1 - i][x1 - j] ^ matriceFiltre[y2 - i][x2 - j]
    print("filtre {filtre} appliqué".format(filtre=filtre))
    saving(matriceFiltre, "filtre{filtre}.png".format(filtre=filtre))
    return matrice


def HammingRead(matrice):
    """Fonction qui prend une matrice de pixels et la lit en effectuant la vérification via le code de Hamming."""
    filtre(matrice)
    donnees = []
    bloc = []
    etage = 0
    while len(donnees) < 32:
        for i in range(0, 28):
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            else:
                y = len(matrice) - 2 - etage * 2
            x = (len(matrice) - 1) - (i // 2)
            bit = matrice[y][x]
            bloc.append(bit)
            if len(bloc) == 7:
                # bloc = correctionHamming(bloc)
                donnees.extend(bloc)
                bloc = []
        etage += 1
        for i in range(0, 28):
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            else:
                y = len(matrice) - 2 - etage * 2
            x = 11 + (i // 2)
            bit = matrice[y][x]
            bloc.append(bit)
            if len(bloc) == 7:
                # bloc = correctionHamming(bloc)
                donnees.extend(bloc)
                bloc = []
        etage += 1
    print(donnees)
    return donnees


def to_ascii(data:list):
    """Fonction qui prend une liste de bits et qui les convertit en caractères ascii."""
    ascii = ""
    resultat = ""
    for i in range(0, len(data)):
        ascii += str(data[i])
        if len(ascii) == 8:
            resultat += chr(int(ascii, 2))
            ascii = ""
    return resultat

print(to_ascii(HammingRead(loading("qr_code_damier_ascii.png"))))
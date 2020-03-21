import time

from IPython.core.display import clear_output


def tulosta_tila(tila):
    """
    Tämä funktio luo tulostettavan pelilaudan.
    """
    tuloste = ''
    tuloste += '+---+---+---+\n'
    for i in range(3):
        for j in range(3):
            laatta = tila[i * 3 + j]
            tuloste += '| {} '.format(' ' if laatta == 0 else laatta)
        tuloste += '|\n'
        tuloste += '+---+---+---+\n'
    return tuloste


def ratkaise_lailliset_liikkeet(sijainti):
    """
    Tämä funktio ratkaisee lailliset liikkeet tyhjälle laatalle.
    """
    liikkeet = [1, -1, 3, -3]
    lailliset_liikkeet = []
    for liike in liikkeet:
        if 0 <= sijainti + liike < 9:
            if liike == 1 and (sijainti == 2 or sijainti == 5 or sijainti == 8):
                continue
            if liike == -1 and (sijainti == 0 or sijainti == 3 or sijainti == 6):
                continue
            lailliset_liikkeet.append(liike)
    return lailliset_liikkeet


def generoi_uudet_lailliset_tilat(tila):
    """
    Tämä funktio generoi seuraavat lailliset tilat nykyisestä tilasta.
    """
    tyhjä_laatta = tila.index(0)  # tyhjä ruutu
    lailliset_liikkeet = ratkaise_lailliset_liikkeet(tyhjä_laatta)
    uudet_tilat = []
    for liike in lailliset_liikkeet:
        uusi_tila = copy.deepcopy(tila)
        (uusi_tila[tyhjä_laatta + liike], uusi_tila[tyhjä_laatta]) = (
        uusi_tila[tyhjä_laatta], uusi_tila[tyhjä_laatta + liike])
        uudet_tilat.append(uusi_tila)
    return uudet_tilat


def laske_heuristinen_arvo(tila, tavoitetila, heuristinen_funktio):
    """
    Tämä funktio valitsee arviointifunktioksi joko hamming-etäisyyden 'hamming', city-block-etäisyyden 'city-block' tai euklidisen etäisyyden 'euklidinen'.
    """
    if heuristinen_funktio == 'hamming':
        return laske_hamming_etäisyys(tila, tavoitetila)
    elif heuristinen_funktio == 'city-block':
        return laske_city_block_etäisyys(tila, tavoitetila)
    elif heuristinen_funktio == 'euklidinen':
        return laske_euklidinen_etäisyys(tila, tavoitetila)
    else:
        print('Vaihtoehdot ovat \'hamming\' ,\'city-block\' tai \'euklidinen\'')


def järjestä_avoin_lista(avoin_lista, f_arvot):
    """
    Tässä funktiossa järjestetään avoin lista f-arvojen perusteella
    """
    f_arvot_tmp = []
    for tila, polku in avoin_lista:
        f_arvot_tmp.append(f_arvot[string(tila)])
    return [x for y, x in sorted(zip(f_arvot_tmp, avoin_lista))]


def string(lista):
    """
    Tämä funktio muuttaa listan stringiksi.
    """
    return ''.join(list(map(str, lista)))


def a_tähti(alkutila, tavoitetila, heuristinen_funktio):
    """
    Tämä funktio ratkaisee pelin käyttämällä A-tähti-hakualgoritmia.
    """
    avoin_lista = []
    suljettu_lista = []
    polku = []
    g_arvot = {}
    f_arvot = {}
    g_arvot[string(alkutila)] = 0
    f_arvot[string(alkutila)] = g_arvot[string(alkutila)] + laske_heuristinen_arvo(alkutila, tavoitetila,
                                                                                   heuristinen_funktio)
    tila = [alkutila, polku]
    avoin_lista.append(tila)
    while len(avoin_lista) != 0:
        avoin_lista = järjestä_avoin_lista(avoin_lista, f_arvot)
        tila, polku = avoin_lista.pop(0)
        if tila == tavoitetila:
            uusi_polku = polku + [tila]
            return uusi_polku, suljettu_lista
        suljettu_lista.append(tila)
        uudet_tilat = generoi_uudet_lailliset_tilat(tila)
        for uusi_tila in uudet_tilat:
            alustava_g_arvo = g_arvot[string(tila)] + 1
            if uusi_tila in suljettu_lista and alustava_g_arvo >= g_arvot[string(uusi_tila)]:
                continue
            if uusi_tila not in suljettu_lista or alustava_g_arvo < g_arvot[string(uusi_tila)]:
                uusi_polku = polku + [tila]
                g_arvot[string(uusi_tila)] = alustava_g_arvo
                f_arvot[string(uusi_tila)] = g_arvot[string(uusi_tila)] + laske_heuristinen_arvo(uusi_tila, tavoitetila,
                                                                                                 heuristinen_funktio)
                if uusi_tila not in avoin_lista:
                    avoin_lista.append([uusi_tila, uusi_polku])
    print('Ratkaisua ei löytynyt!')


def ratkaise_peli(alkutila, tavoitetila, arviointifunktio):
    """
    Tämä funktio luo ratkaisun käytetyllä arviointifunktiolla, kun alkutila ja tavoitetila ovat tiedossa.
    """
    polku, suljettu_lista = a_tähti(alkutila, tavoitetila, arviointifunktio)
    for tila in polku:
        clear_output(wait=True)
        print('Alkutila:\n' + tulosta_tila(alkutila))
        print('\nRatkaisu alkutilalle A*-hakualgoritmilla {}-etäisyys arviointifunktiota apuna käyttäen:\n\n'.format(
            arviointifunktio) + tulosta_tila(tila))
        time.sleep(1)
    print('Ratkaisu sisältää {} liikettä, jonka löytämiseksi tutkittiin yhteensä {} tilaa.'.format(len(polku) - 1,
                                                                                                   len(suljettu_lista)))

def laske_euklidinen_etäisyys(tila, tavoitetila):
    """
    Tämä funktio laskee euklidisen etäisyyden tilalle tavoitetilasta.
    """
    # Alustetaan muuttuja euklidinen_arvo arvolla 0
    euklidinen_arvo = 0
    # Käydään silmukassa läpi laatan arvot 1-8
    for laatan_arvo in range(1, 9):
        # Selvitetään tilalle ja tavoitetilalle, missä kohtaa matriisia laatan arvo on (esim. tila_x viittaa tilan laatan arvon vaakasuuntaiseen koordinaattiin)
        (tila_x, tila_y) = (tila.index(laatan_arvo) // 3, tila.index(laatan_arvo) % 3)
        (tavoitetila_x, tavoitetila_y) = (tavoitetila.index(laatan_arvo) // 3, tavoitetila.index(laatan_arvo) % 3)
        # Lasketaan jokaiselle laatalle neliöity vaakasuuntainen ja pystysuuntainen etäisyys ja lisätään niiden summan neliöjuuri muuttujaan euklidinen_arvo
        euklidinen_arvo += ((tavoitetila_x - tila_x)**2 + (tavoitetila_y - tila_y)**2)**0.5
    # Palautetaan lopuksi muuttuja euklidinen_arvo
    return euklidinen_arvo


def laske_hamming_etäisyys(tila, tavoitetila):
    """
    Tämä funktio laskee hamming-etäisyyden tilalle tavoitetilasta.
    """
    # -------- TÄHÄN SINUN KOODI --------
    # Alusta muuttuja hamming_arvo arvolla 0

    # Käy silmukassa läpi laatan arvot 1-8

    # Selvitä tilalle ja tavoitetilalle, missä kohtaa LISTAA laatan arvo on (esim. tila_indeksi viittaa tilan laatan arvon indeksiin listassa. Vihje: .index())

    # Jos tilan laatan arvon indeksi on eri kuin tavoitetilan vastaavan laatan arvon indeksi

    # Kasvata muuttujan hamming_arvo arvoa 1:llä

    # Palauta lopuksi muuttuja hamming_arvo

    # -----------------------------------


def laske_city_block_etäisyys(tila, tavoitetila):
    """
    Tämä funktio laskee city-block-etäisyyden tilalle tavoitetilasta.
    """
    # -------- TÄHÄN SINUN KOODISI --------
    # Alusta muuttuja city_block_arvo arvolla 0

    # Käy silmukassa läpi laatan arvot 1-8

    # Selvitä tilalle ja tavoitetilalle, missä kohtaa MATRIISIA laatan arvo on (esim. tila_x viittaa tilan laatan arvon vaakasuuntaiseen koordinaattiin)

    # Laske jokaiselle laatalle vaakasuuntainen ja pystysuuntainen itseisarvoistettu etäisyys ja lisää ne muuttujaan city-block_arvo

    # Palauta lopuksi muuttuja city_block_arvo

    # -------------------------------------


if __name__ == '__main__':
    # Määritetään kuvan 2 alkutila ja tavoitetila
    alkutila = [7, 2, 3, 1, 0, 6, 5, 8, 4]
    tavoitetila = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # Tarkistetaan, että funktio laske_euklidinen_etäisyys() palauttaa oikean arvon
    print('Euklidinen-etäisyys alkutilalle on: {}'.format(laske_euklidinen_etäisyys(alkutila, tavoitetila)))
    # Ratkaistaan peli alkutilalle arviointifunktion ollessa euklidinen-etäisyys.
    ratkaise_peli(alkutila, tavoitetila, 'euklidinen')
    # Tarkistetaan, että funktio laske_hamming_etäisyys() palauttaa oikean arvon
    print('Hamming-etäisyys alkutilalle on: {}'.format(laske_hamming_etäisyys(alkutila, tavoitetila)))
    # Ratkaistaan peli alkutilalle arviointifunktion ollessa hamming-etäisyys.
    ratkaise_peli(alkutila, tavoitetila, 'hamming')
    # Tarkistetaan, että funktio laske_city_block_etäisyys() palauttaa oikean arvon
    print('City-block-etäisyys alkutilalle on: {}'.format(laske_city_block_etäisyys(alkutila, tavoitetila)))
    # Ratkaistaan peli alkutilalle arviointifunktion ollessa city-block-etäisyys.
    ratkaise_peli(alkutila, tavoitetila, 'city-block')
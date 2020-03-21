import copy


def paimen_saaressa(saari):
    """
    Tässä funktiossa tarkistetaan onko paimen saaressa vai mantereella. Jos paimen on saaressa, palautetaan totuusarvo True.
    Muussa tapauksessa palautetaan totuusarvo False.
    """
    if 'P' in saari:
        return True
    return False


def objektit_saaressa(objektit, manner):
    """
    Tässä funktiossa selvitetään objektit saaressa, kun tiedossa on mitä objekteja on mantereella.
    Poistetaan kaikista peliin osallistuvista objekteista mantereen objektit, jolloin saadaan saaressa olevat objektit.
    """
    return [objekti for objekti in objektit if objekti not in manner]


def laillinen_tila(objektit, manner):
    """
    Tässä funktiossa tarkistetaan, onko toteutettavasta liikkeestä aiheutunut tila laillinen molemmilla puolin meritietä.
    Jos liike on laiton, palautetaan totuusarvo False. Muussa tapauksessa palautetaan totuusarvo True.
    """
    saari = objektit_saaressa(objektit, manner)
    # Jos paimen on saaressa, (susi ja lammas) tai (lammas ja kaali) ei saa olla mantereella.
    if paimen_saaressa(saari):
        if ('S' in manner and 'L' in manner) or ('L' in manner and 'K' in manner):
            return False
        return True
    # Jos paimen on mantereella, (susi ja lammas) tai (lammas ja kaali) ei saa olla saaressa.
    else:
        if ('S' in saari and 'L' in saari) or ('L' in saari and 'K' in saari):
            return False
        return True


def generoi_uudet_lailliset_mantereet(objektit, manner):
    """
    Tässä funktiossa generoidaan uudet lailliset tilat mantereelle.
    """
    manner = copy.deepcopy(manner)
    uudet_mantereet = []  # alustetaan uudet_mantereet lista
    saari = objektit_saaressa(objektit, manner)
    if paimen_saaressa(saari):
        saari.remove('P')  # vähintään paimen liikkuu pois saaresta mantereelle
        manner.extend('P')
        if laillinen_tila(objektit, manner):
            uudet_mantereet.extend(sorted(manner))
        for objekti in saari:
            manner_tmp = manner + [objekti]
            if laillinen_tila(objektit, manner_tmp):
                uudet_mantereet.extend(sorted(manner_tmp))
    else:
        manner.remove('P')  # vähintään paimen liikkuu pois mantereelta saareen
        saari.extend('P')
        if laillinen_tila(objektit, manner):
            uudet_mantereet.extend(sorted(manner))
        manner_tmp = copy.deepcopy(manner)
        for objekti in manner:
            manner_tmp.remove(objekti)
            if laillinen_tila(objektit, manner_tmp):
                uudet_mantereet.extend(sorted(manner_tmp))
            manner_tmp.extend(objekti)
    return uudet_mantereet


def tulosta_liikkeet(objektit, polku):
    """
    Tässä funktiossa tulostetaan tehdyt liikkeet, kun valmis polku on löydetty.
    """
    print('     Manner' + ' ' * 23 + 'Vene' + ' ' * 28 + 'Saari')
    for i, manner in enumerate(polku):
        saari = objektit_saaressa(objektit, manner)
        if paimen_saaressa(saari):
            print('     {}'.format(manner) + ' ' * (61 - len(str(manner))) + '{}'.format(saari))
            if i < len(polku) - 1:
                vene = [x for x in saari if x not in objektit_saaressa(objektit, polku[i + 1])]
                print('{}.   '.format(i + 1) + ' ' * 27 + '<-{}'.format(vene))
        else:
            print('     {}'.format(manner) + ' ' * (61 - len(str(manner))) + '{}'.format(saari))
            if i < len(polku) - 1:
                vene = [x for x in manner if x not in polku[i + 1]]
                print('{}.   '.format(i + 1) + ' ' * 29 + '{}->'.format(vene))


def syvyyshaku(objektit, manner):
    """
    Tässä funktiossa etsitään ongelman ratkaiseva polku käyttämällä syvyyshakua (engl. depth-first-search).
    """
    tavoitetila = []
    polku = [manner]
    # -------- TÄHÄN SINUN KOODI --------
    # 1. Alusta kaksi tyhjää listaa: avoin_lista ja suljettu_lista
    avoin_lista = []
    suljettu_lista = []
    # 2. Määritetään muuttuja alkutila, joka on lista, joka koostuu kahdesta muusta listasta manner ja polku
    alkutila = [manner, polku]
    # 3. Lisää alkutila avoimeen listaan
    avoin_lista.append(alkutila)
    # 4. Käy läpi avointa listaa niin kauan, kunnes se on tyhjä (Vihje: while loop)
    while avoin_lista:
        # 4.A Valitaan avoimen listan viimeinen alkio
        manner, polku = avoin_lista.pop()
        # 4.B Jos muuttuja manner ei ole jo ennestään suljetussa listassa
        if manner not in suljettu_lista:
            # 4.B.a Lisää muuttuja manner suljettuun listaan
            suljettu_lista.append(manner)
            # 4.B.b Tarkasta onko manner sama kuin tavoitetila
            if manner == tavoitetila:
                # 4.B.b.i Jos näin on, palauta muuttuja polku
                return polku
            # 4.B.c Generoidaan muuttuja uudet_mantereet käyttämällä apufunktiota generoi_uudet_lailliset_mantereet(objektit, manner)
            uudet_mantereet = generoi_uudet_lailliset_mantereet(objektit, manner)
            # 4.B.d Käydään läpi silmukassa muuttujan uudet_mantereet alkiot yksi kerrallaan käyttämällä alkiosta nimeä uusi_manner
            for uusi_manner in uudet_mantereet:
                # 4.B.d.i Selvitetään muuttuja uusi_polku lisäämällä listaan polku muuttuja uusi_manner
                polku.append(uusi_manner)
                uusi_polku = polku
                # 4.B.d.ii Lisätään listaan avoin_lista uusi tila, joka koostuu läpikäytävästä uudesta mantereesta sekä listasta uusi_polku
                avoin_lista.extend([uusi_manner, uusi_polku])

    # 5. Tulostetaan virheilmoitus, kun avoin lista on tyhjä ja ratkaisua ei löytynyt
    print('Ratkaisua ei löytynyt')
# -----------------------------------

if __name__ == '__main__':
    objektit = sorted(['S', 'L', 'K', 'P'])
    # sorted() komento huolehtii, että susi, lammas, kaali ja paimen ovat listassa aakkosjärjestyksessä
    saari = sorted([])
    manner = copy.deepcopy(objektit)
    print('Alkutilanteessa mantereella on {} ja saaressa on {}'.format(manner, saari))
    syvyyshaku_polku = syvyyshaku(objektit, manner)
    tulosta_liikkeet(objektit, syvyyshaku_polku)
#    leveyshaku_polku = leveyshaku(objektit, manner)
#    tulosta_liikkeet(objektit, leveyshaku_polku)

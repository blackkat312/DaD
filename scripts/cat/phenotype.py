from .genotype import *
from random import choice, randint
from scripts.cat.breed_functions import find_my_breed

class Phenotype():

    def __init__(self, genotype):
        self.length = ""

        self.highwhite = ""
        self.fade = ""
        self.colour = ""
        self.silvergold = ""
        self.tabtype = ""
        self.tabby = ""
        self.tortie = ""
        self.point = ""
        self.lowwhite = ""
        self.karpati = ""
        self.specwhite = ""

        self.eartype = ""
        self.tailtype = ""
        self.bobtailnr = 0
        self.pawtype = ""
        self.furtype = []

        self.vitiligo = ""

        self.genotype = genotype

    def FurtypeFinder(self):
        furtype = []

        if self.genotype.lykoi[0] == "ly":
            furtype.append("sparse")

        if self.genotype.wirehair[0] == "Wh" and self.genotype.ruhr != ["Hrbd", "hrbd"]:
            if len(furtype)>0:
                furtype.append(", ")
            else:
                furtype.append("wiry")

        if self.genotype.laperm[0] == "Lp" or self.genotype.cornish[0] == "r" or self.genotype.urals[0] == "ru" or self.genotype.tenn[0] == "tr" or self.genotype.fleece[0] == "fc" or self.genotype.sedesp[0] == "Se" or self.genotype.sedesp[0] == "re" or self.genotype.ruhr == ["Hrbd", "hrbd"]:
            if len(furtype)>0:
                furtype.append(", ")

            if self.genotype.ruhr[0] == "Hrbd" and self.genotype.ruhrmod == ["hi", "ha"]:
                furtype.append("patchy ")

            if self.genotype.ruhr[0] != "Hrbd":
                furtype.append("rexed")
            else:
                furtype.append("brush-coated")

        if self.genotype.satin[0] == "st" or self.genotype.tenn[0] == "tr":
            furtype.append(" satin")
        elif self.genotype.glitter[0] == "gl" and self.genotype.agouti[0] != "a":
            furtype.append(" shiny")

        if len(furtype)>0:
            furtype.append(" fur")

        if self.genotype.ruhr[1] == "Hrbd" or (self.genotype.ruhr == ["Hrbd", "hrbd"] and self.genotype.ruhrmod[0] == "ha") or self.genotype.sedesp == ["hr", "hr"]:
            self.length = "hairless"
            furtype = []
        elif self.genotype.sedesp[0] == "hr":
            self.length = 'fur-pointed'
        elif self.genotype.furLength[0] == "l":
            self.length = "longhaired"
        else:
            self.length = "shorthaired"

        if(len(furtype)==0):
            furtype.append("")
        self.furtype = furtype
    def MainColourFinder(self):
        colour = ""
        tortie = ""

        if('o' not in self.genotype.sexgene):
            if(self.genotype.dilute[0] == "d"):
                if(self.genotype.pinkdilute[0] == "dp"):
                    colour += "ivory"
                else:
                    colour += "cream"

                if(self.genotype.dilutemd[0] == "Dm"):
                    colour += " apricot"
            else:
                if(self.genotype.pinkdilute[0] == "dp"):
                    colour += "honey"
                else:
                    colour += "red"
        else:
            if(self.genotype.dilute[0] == "d"):
                if(self.genotype.eumelanin[0] == "B"):
                    if(self.genotype.pinkdilute[0] == "dp"):
                        colour += "platinum"
                    else:
                        colour += "blue"
                elif(self.genotype.eumelanin[0] == "b"):
                    if(self.genotype.pinkdilute[0] == "dp"):
                        colour += "lavender"
                    else:
                        colour += "lilac"
                else:
                    if(self.genotype.pinkdilute[0] == "dp"):
                        colour += "beige"
                    else:
                        colour += "fawn"

                if(self.genotype.dilutemd[0] == "Dm"):
                    colour += " caramel"
            else:
                if(self.genotype.pinkdilute[0] == "dp"):
                    if(self.genotype.eumelanin[0] == "B"):
                        colour += "dove"
                    elif(self.genotype.eumelanin[0] == "b"):
                        colour += "champagne"
                    else:
                        colour += "buff"
                else:
                    if(self.genotype.eumelanin[0] == "B"):
                        colour += "black"
                    elif(self.genotype.eumelanin[0] == "b"):
                        colour += "chocolate"
                    else:
                        colour += "cinnamon"

        if 'O' in self.genotype.sexgene and 'o' in self.genotype.sexgene:
            tortie = "tortie "



        self.colour = colour
        if(tortie != "" and self.genotype.brindledbi):
            tortie = "brindled bicolour "
        self.tortie = tortie


    def WhiteFinder(self):
        if self.genotype.white[1] in ["ws", 'wt'] or 'NoDBE' not in self.genotype.pax3:
            if(self.tortie != "" and self.tortie != 'brindled bicolour '):
                self.tortie = "calico "
            elif (self.tortie == "" or self.genotype.whitegrade > 2):
                self.highwhite = "white and "

        elif(self.genotype.white[0] in ['ws', 'wt'] and self.genotype.whitegrade > 2):
            if(self.tortie != "" and self.tortie != 'brindled bicolour ' and self.genotype.whitegrade > 4):
                self.tortie = "calico "
            else:
                self.lowwhite = "and white "


        if(self.genotype.white[0] == "wg"):
            self.specwhite = "white gloves"
        elif(self.genotype.white[0] == 'wt' or self.genotype.white[1] == 'wt'):
            self.specwhite = "a white dorsal stripe"

    def PointFinder(self):
        self.point = ""

        if(self.genotype.pointgene[0] == 'cb'):
            if(self.genotype.pointgene[1] == 'cs'):
                self.point = "mink "
            elif(self.genotype.pointgene[1] == 'cm'):
                self.point = "burmocha "
            elif (self.genotype.pointgene[1] == 'c'):
                self.point = "sepia-albino "
            else:
                self.point = "sepia "
        elif(self.genotype.pointgene[0] == 'cs'):
            if(self.genotype.pointgene[1] == 'cm'):
                self.point = "siamocha "
            elif (self.genotype.pointgene[1] == 'c'):
                self.point = "point-albino "
            else:
                self.point = "point "
        elif(self.genotype.pointgene[0] == 'cm'):
            if (self.genotype.pointgene[1] == 'c'):
                self.point = "mocha-albino "
            else:
                self.point = "mocha "

        if(self.point != ''):
            if(self.colour == 'red'):
                self.colour = 'flame'
            elif(self.colour == 'black'):
                if(self.point == "sepia " or self.point == "burmocha " or self.point == "mocha " or self.point == "mocha-albino "):
                    self.colour = 'sable'
                else:
                    self.colour = 'seal'


    def ExtFinder(self):
        if('o' in self.genotype.sexgene):
            if(self.genotype.ext[0] == 'ec'):
                if(self.colour == ''):
                    self.tortie = " " + self.tortie
                self.colour = 'agouti carnelian'
                if(self.genotype.agouti[0] == 'a'):
                    self.colour = "non" + self.colour
                if(self.genotype.dilute[0] == 'd' or self.genotype.pinkdilute[0] == 'dp'):
                    self.colour = "light " + self.colour

            elif(self.genotype.ext[0] == 'er'):
                self.colour += ' russet'
            elif(self.genotype.ext[0] == 'ea'):
                if(self.genotype.dilute[0] == 'd' or self.genotype.pinkdilute[0] == 'dp'):
                    self.colour += " light"
                self.colour += ' amber'
    def KarpFadeFinder(self):
        self.karpati = ""
        self.fade = ""

        if(self.genotype.karp[0] == 'K'):
            self.karpati = "karpati "
        if(self.genotype.white[0] == 'wsal'):
            self.karpati += "salmiak "

        if(self.genotype.bleach[0] == "lb"):
            self.fade = "bleached "
        elif(self.genotype.ghosting[0] == "Gh"):
            self.fade = "faded "
    def SolidWhite(self, pattern=None):
        if(self.genotype.white[0] == "W" or self.genotype.pointgene[0] == "c" or (self.genotype.brindledbi and 'o' not in self.genotype.sexgene)) or ('DBEalt' not in self.genotype.pax3 and 'NoDBE' not in self.genotype.pax3):
            self.highwhite = ""
            self.fade = ""
            if(self.genotype.pointgene[0] == "c"):
                self.colour = "albino"
            else:
                self.colour = "white"
            self.silvergold = ""
            self.tabtype = ""
            self.tabby = ""
            self.tortie = ""
            self.point = ""
            self.lowwhite = ""
            self.highwhite = ""
            self.karpati = ""
            self.specwhite = ""
            self.vitiligo = ""
    def SilverGoldFinder(self):
        self.silvergold = ""

        if((self.genotype.agouti[0] == 'a' or self.genotype.ext[0] == 'Eg') and 'o' in self.genotype.sexgene):
            if(self.genotype.silver[0] == 'I'):
                if(self.genotype.wbsum > 13):
                    self.silvergold = 'masked silver '
                else:
                    if(self.genotype.wbsum > 9):
                        self.silvergold = 'light '
                    self.silvergold += 'smoke '
        else:
            if(self.genotype.silver[0] == 'I'):
                if(self.genotype.corin[0] in ['sg', 'sh'] or (self.genotype.ext[0] != 'ec' and self.genotype.ext[1] == 'ec')):
                    self.silvergold = 'bimetallic '
                elif(self.genotype.corin[0] == 'fg'):
                    self.silvergold = 'silver copper '
                elif ('o' not in self.genotype.sexgene):
                    self.silvergold = 'cameo '
                else:
                    self.silvergold = 'silver '
            elif(self.genotype.corin[0] == 'sg' or self.genotype.wbsum > 11):
                self.silvergold = 'golden '
            elif(self.genotype.corin[0] == 'sh'):
                self.silvergold = 'sunshine '
            elif(self.genotype.corin[0] == 'fg'):
                self.silvergold = 'flaxen gold '

    def TabbyFinder(self):
        self.tabby = ""
        self.tabtype = ""

        if (self.genotype.ext[0] == 'Eg' and 'o' in self.genotype.sexgene and self.genotype.agouti[0] != 'a'):
            self.tabtype += 'grizzled '
        if (self.genotype.agouti == ['Apb', 'Apb'] and 'o' in self.genotype.sexgene):
            self.tabtype += 'twilight '
        elif (self.genotype.agouti[0] == 'Apb' and 'o' in self.genotype.sexgene):
            self.tabtype += 'charcoal '

        if(self.tabtype == ' '):
            self.tabtype = ''

        def FindPattern():
            if(self.genotype.ticked[0] != 'ta' or self.genotype.wbsum > 13):
                if(self.genotype.wbsum > 13):
                    self.tabby = 'chinchilla'
                elif(self.genotype.ticked[1] == 'Ta' or not self.genotype.breakthrough):
                    if (self.genotype.wbsum > 11):
                        self.tabby = 'shaded'
                    elif(self.genotype.ticksum > 7):
                        self.tabby = 'agouti'
                    else:
                        self.tabby = 'ticked'
                else:
                    if(self.genotype.mack[0] == 'mc'):
                        self.tabby = 'ghost-patterned'
                    elif(self.genotype.spotsum > 5):
                        self.tabby = 'servaline'
                    else:
                        if(self.genotype.spotsum > 2):
                            self.tabby = 'broken '
                        self.tabby += 'pinstripe'
            elif(self.genotype.mack[0] == 'mc'):
                self.tabby = 'classic'
            elif(self.genotype.spotsum > 5):
                self.tabby = 'spotted'
            else:
                if(self.genotype.spotsum > 2):
                    self.tabby = 'broken '
                self.tabby += 'mackerel'

            if(self.tabby != "" and (self.genotype.bengsum > 3 or self.genotype.soksum > 5)):
                if(self.genotype.bengsum > 3):
                    if(self.tabby == "spotted"):
                        self.tabby = "rosetted"
                    elif(self.tabby == "broken mackerel"):
                        self.tabby = "broken braided"
                    elif(self.tabby == "mackerel"):
                        self.tabby = "braided"
                    elif(self.tabby == "classic"):
                        self.tabby = "marbled"

                    elif(self.tabby == "servaline"):
                        self.tabby += "-rosetted"
                    elif('pinstripe' in self.tabby):
                        self.tabby += "-braided"
                    elif(self.tabby == "ghost-patterned"):
                        self.tabby = "ghost marble"
                elif(self.tabby == 'classic'):
                    self.tabby = 'sokoke'

        if('o' not in self.genotype.sexgene or self.genotype.agouti[0] != 'a' or self.tabtype != '' or ('smoke' in self.silvergold and self.length == 'shorthaired') or self.genotype.ext[0] not in ['Eg', 'E']):
            FindPattern()

        if(self.tortie != '' and self.tabby != '' and self.tortie != "brindled bicolour "):
            if(self.tortie == 'calico '):
                self.tortie = ' caliby '
            else:
                self.tortie = ' torbie '
        elif(self.tabby != ''  and self.point != ''):
            if(self.point == 'mink '):
                self.tabby += ' mynx '
                self.point = ''
            elif(self.point == 'sepia '):
                self.tabby += ' synx '
                self.point = ''
            else:
                self.tabby += ' lynx '
        elif(self.tabby != ''):
            self.tabby += ' tabby '

    def EarFinder(self):
        self.eartype = ""

        if(self.genotype.fold[0] == 'Fd'):
            self.eartype += 'folded'
            if(self.genotype.curl[0] == 'Cu'):
                self.eartype += ' back'
            self.eartype += ' ears'
        elif(self.genotype.curl[0] == 'Cu'):
            self.eartype = 'curled back ears'

    def LegFinder(self):
        self.pawtype = ""

        if(self.genotype.munch[0] == 'Mk'):
            self.pawtype = "short legs"

        if(self.genotype.poly[0] == 'Pd'):
            if(self.pawtype != ""):
                self.pawtype += ", "

            self.pawtype += 'extra toes'

    def TailFinder(self):
        self.tailtype = "a "

        if(self.genotype.manx[0] != 'M' or (self.genotype.manxtype != 'rumpy' and self.genotype.manxtype != 'stumpy' and self.genotype.manxtype != 'riser')):
            if(self.genotype.kab[0] == 'kab' or self.genotype.toybob[1] == 'Tb' or self.genotype.kub[0] == 'Kub' or self.genotype.jbob[0] == 'jb'):
                self.tailtype += 'stubby, pom-pom '
                self.bobtailnr = 2
            else:
                if(self.genotype.jbob[1] == 'jb' or self.genotype.toybob[0] == 'Tb'):
                    self.tailtype += 'kinked, '
                if(self.genotype.manx[0] == 'Ab' or self.genotype.toybob[0] == 'Tb' or self.genotype.jbob[1] == 'jb' or (self.genotype.manx[0] == 'M' and self.genotype.manxtype == 'stubby')):
                    self.tailtype += "short "
                    self.bobtailnr = 3
                    if self.genotype.manx[0] == 'Ab' and (self.genotype.manxtype == 'rumpy' or self.genotype.manxtype == 'riser'):
                        self.bobtailnr = 2
                    elif (self.genotype.manxtype == 'long' or self.genotype.manxtype == 'most') or (self.genotype.manx[0] == 'M' and self.genotype.manxtype == 'stubby'):
                        self.bobtailnr = 4
                elif(self.genotype.manx[0] == 'M' and self.genotype.manxtype == 'most'):
                    self.tailtype += 'somewhat shortened '
                    self.bobtailnr = 5

                if(self.genotype.ring[0] == 'rt'):
                    self.tailtype = 'curled ' + self.tailtype
        elif(self.genotype.manx[0] == 'M'):
            if(self.genotype.manxtype == 'stumpy'):
                self.tailtype += 'stubby '
                self.bobtailnr = 3
            elif(self.genotype.manxtype == 'riser'):
                self.tailtype += 'stubby, barely visible '
                self.bobtailnr = 1
            elif(self.genotype.manxtype == 'rumpy'):
                self.tailtype = 'no '
                self.bobtailnr = 1

        if self.tailtype == 'a ':
            self.tailtype = ''

        if(self.tailtype != ''):
            self.tailtype += "tail"

    def PhenotypeOutput(self, gender=None, sex=None, pattern=None):
        self.FurtypeFinder()
        self.MainColourFinder()
        self.PointFinder()
        self.ExtFinder()
        self.KarpFadeFinder()
        self.WhiteFinder()
        self.SilverGoldFinder()
        self.TabbyFinder()

        self.EarFinder()
        self.TailFinder()
        self.LegFinder()

        if (self.genotype.vitiligo):
            self.vitiligo = 'vitiligo'
        self.SolidWhite(pattern=pattern)

        if(self.genotype.chimera and not self.genotype.chimerapattern):
            self.genotype.chimerapattern = self.ChooseTortiePattern('chim')

        eyes = ""

        furtype = ""
        for i in self.furtype:
            furtype += i

        if(self.genotype.lefteye == self.genotype.righteye):
            eyes = "insertleft eyes"
        else:
            eyes = "one insertleft eye, and one insertright eye"

        if(self.genotype.extraeye):
            eyes = eyes.replace(" one insertleft eye, and one insertright eye ", " one insertleft eye, one insertright eye ")
            eyes += ", and insertsectoral sectoral heterochromia"

        withword = self.specwhite
        if (self.eartype !="" or self.tailtype!="" or self.pawtype!="" or furtype!="" or self.vitiligo != ""):
            withword += ", " + self.vitiligo + ", " + furtype + ", " + self.eartype + ", " + self.tailtype + ", " + self.pawtype
            while(withword[0] == ","):
                withword = withword[2:]
            while(withword[(len(withword)-2)] == ","):
                withword = withword[:(len(withword)-2)]
            nochange = False
            while(nochange == False):
                withword = withword.replace(", , ", ", ")
                if(withword == withword.replace(", , ", ", ")):
                    nochange = True

        if(withword != ""):
            if ", " in withword:
                if "insertright" in eyes:
                    withword += ", "
                else:
                    withword += ", and "
            else:
                if "insertright" in eyes:
                    withword += ", "
                else:
                    withword += " and "
        else:
            if ", and insertsectoral sectoral" in eyes and "one insertleft eye, one insertright eye" not in eyes:
                eyes = eyes.replace(", and insertsectoral sectoral", "and insertsectoral sectoral")
            elif "one insertleft eye, and one insertright eye" in eyes and ", and insertsectoral sectoral" not in eyes:
                eyes = eyes.replace("one insertleft eye, and one insertright eye", "one insertleft eye and one insertright eye")

        eyes = eyes.replace("insertleft", self.genotype.lefteye)
        eyes = eyes.replace("insertright", self.genotype.righteye)
        eyes = eyes.replace("insertsectoral", self.genotype.extraeyecolour)
        withword = " with " + withword + eyes.lower()

        sextext = " "
        if not sex or (sex and sex != "intersex"):  # everything else
            sextext = " "
        elif sex == "intersex":  # specifying jic though
            sextext = sex + " "

        if not gender:
            gendera = "cat"
        elif gender == "molly" or gender == "trans molly":
            gendera = "molly"
        elif gender == "tom" or gender == "trans tom":
            gendera = "tom"
        else:
            gendera = "cat"

        if self.genotype.chimera:
            gendera = "chimera " + gendera

        gendera = sextext + gendera

        error_genders = ["intersex molly", "intersex tom", "chimera molly", "chimera tom"]
        for x in error_genders:
            if x in gendera and "trans" not in gender:
                gendera = "this should not appear"
                break

        breed = find_my_breed(self.genotype, self, self.genotype.odds)
        if breed:
            breed = " " + breed + " "

        if self.genotype.pointgene == ['C', 'c'] and ("albino" in self.genotype.lefteyetype or "albino" in self.genotype.righteyetype or (self.genotype.extraeye and "albino" in self.genotype.extraeyetype)):
            outputs = "a " + self.length + " albinistic " + self.highwhite + self.fade + self.colour + " " + self.silvergold + self.tabtype + self.tabby + self.tortie + self.point + self.lowwhite + self.karpati + breed + gendera + withword
        else:
            outputs = "a " + self.length + " " + self.highwhite + self.fade + self.colour + " " + self.silvergold + self.tabtype + self.tabby + self.tortie + self.point + self.lowwhite + self.karpati + breed + gendera + withword

        while "  " in outputs:
            outputs = outputs.replace("  ", " ")

        return outputs

    def GetTabbySprite(self, special = None):
        pattern = ""

        if(special == 'redbar'):
            if(self.genotype.mack[0] == "mc"):
                pattern = 'redbarc'
            else:
                pattern = 'redbar'
        elif(self.genotype.wbtype == 'chinchilla' or self.genotype.ticked[1] == "Ta" or ((not self.genotype.breakthrough or self.genotype.mack[0] == "mc") and self.genotype.ticked[0] == "Ta")):
            if(self.genotype.ticktype == "agouti" or self.genotype.wbtype == 'chinchilla'):
                pattern = 'agouti'
            elif(self.genotype.ticktype == 'reduced barring'):
                if(self.genotype.mack[0] == "mc"):
                    pattern = 'redbarc'
                else:
                    pattern = 'redbar'
            else:
                if(self.genotype.mack[0] == "mc"):
                    pattern = 'fullbarc'
                else:
                    pattern = 'fullbar'
        elif(self.genotype.ticked[0] == "Ta"):
            if(self.genotype.bengtype == "normal markings"):
                if(self.genotype.spottype == "broken stripes"):
                    pattern = 'brokenpins'
                elif(self.genotype.spotsum < 6):
                    pattern = 'pinstripe'
                else:
                    pattern = 'servaline'
            else:
                if(self.genotype.spottype == "broken stripes"):
                    pattern = 'brokenpinsbraid'
                elif(self.genotype.spotsum < 6):
                    pattern = 'pinsbraided'
                else:
                    pattern = 'leopard'
        elif(self.genotype.mack[0] == "mc"):
            if(self.genotype.bengtype == "normal markings"):
                pattern = 'classic'
            else:
                pattern = 'marbled'
        else:
            if(self.genotype.bengtype == "normal markings"):
                if(self.genotype.spottype == "broken stripes"):
                    pattern = 'brokenmack'
                elif(self.genotype.spotsum < 6):
                    pattern = 'mackerel'
                else:
                    pattern = 'spotted'
            else:
                if(self.genotype.spottype == "broken stripes"):
                    pattern = 'brokenbraid'
                elif(self.genotype.spotsum < 6):
                    pattern = 'braided'
                else:
                    pattern = 'rosetted'


        return pattern

    def ChooseTortiePattern(self, spec=None):
        tortie_patterns = [
            'ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE',
            'MINIMALFOUR', 'HALF', 'OREO', 'SWOOP', 'MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN',
            'STREAMSTRIKE', 'ORIOLE', 'CHIMERA', 'DAUB', 'EMBER', 'BLANKET', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL',
            'SAFI', 'SMUDGED', 'DAPPLENIGHT', 'STREAK', 'MASK', 'CHEST', 'ARMTAIL', 'GRUMPYFACE', 'BRIE', 'BELOVED',
            'BODY', 'SHILOH', 'FRECKLED', 'HEARTBEAT',
            # Mink's
            'MINKANY', 'MINKTUXEDO', 'MINKVAN', 'MINKANYTWO', 'MINKSAVANNAH', 'MINKPEBBLESHINE', 'MINKBROKEN',
            'MINKLIGHTTUXEDO', 'MINKLIGHTSONG', 'MINKBLACKSTAR', 'MINKPIEBALD', 'MINKCURVED', 'MINKPETAL',
            'MINKSHIBAINU', 'MINKOWL', 'MINKTIP', 'MINKFANCY', 'MINKFRECKLES', 'MINKRINGTAIL', 'MINKHALFFACE',
            'MINKPANTSTWO', 'MINKGOATEE', 'MINKMITAINE', 'MINKBROKENBLAZE', 'MINKTAIL', 'MINKPRINCE', 'MINKUNDERS',
            'MINKFAROFA', 'MINKMISTER', 'MINKTOPCOVER', 'MINKAPRON', 'MINKCAPSADDLE', 'MINKMASKMANTLE', 'MINKSQUEAKS',
            'MINKSTAR', 'MINKSKUNK', 'MINKHALFWHITE', 'MINKAPPALOOSA', 'MINKDAPPLEPAW', 'MINKHEART', 'MINKLILTWO',
            'MINKGLASS', 'MINKMOORISH', 'MINKMAO', 'MINKWINGS', 'MINKWOODPECKER', 'MINKBOOTS', 'MINKMISS', 'MINKCOW',
            'MINKCOWTWO', 'MINKBUB', 'MINKBOWTIE', 'MINKREVERSEHEART', 'MINKSPARROW', 'MINKVEST', 'MINKLOVEBUG',
            'MINKTRIXIE', 'MINKSAMMY', 'MINKSHOOTINGSTAR', 'MINKREVERSEEYE', 'MINKFRONT', 'MINKBLOSSOMSTEP',
            'MINKPEBBLE', 'MINKTAILTWO', 'MINKBUDDY', 'MINKBULLSEYE', 'MINKFINN', 'MINKDIGIT', 'MINKKROPKA',
            'MINKFCONE', 'MINKMIA', 'MINKSCAR', 'MINKBUSTER', 'MINKHAWKBLAZE', 'MINKCAKE', 'MINKPRINCESS', 'MINKDOUGIE',
            'MINKEXTRA'
        ]

        chosen = choice(tortie_patterns)

        return chosen


    def SpriteInfo(self, moons):
        self.maincolour = ""
        self.mainunders = []
        self.spritecolour = ""
        self.caramel = ""
        self.tortpattern = ""
        self.patchmain = ""
        self.patchunders = []
        self.patchcolour = ""

        if self.genotype.pointgene[0] == "c":
            self.spritecolour = "albino"
            self.maincolour = self.spritecolour
        elif self.genotype.white[0] == "W" or ('DBEalt' not in self.genotype.pax3 and 'NoDBE' not in self.genotype.pax3) or (self.genotype.brindledbi and (('o' not in self.genotype.sexgene) or (self.genotype.ext[0] == 'ea' and ((moons > 11 and self.genotype.agouti[0] != 'a') or (moons > 23))) or (self.genotype.ext[0] == 'er' and moons > 23 and 'O' not in self.genotype.sexgene) or (self.genotype.ext[0] == 'ec' and (self.genotype.agouti[0] != 'a' or moons > 5)))):
            self.spritecolour = "white"
            self.maincolour = self.spritecolour
        elif('o' not in self.genotype.sexgene and self.genotype.silver[0] == 'I' and self.genotype.specialred == 'merle'):
            if self.genotype.tortiepattern is not None:
                self.tortpattern = self.genotype.tortiepattern
                main = self.FindRed(self.genotype, moons, 'merle')
                self.maincolour = main[0]
                self.spritecolour = main[1]
                self.mainunders = [main[2], main[3]]
                main = self.FindRed(self.genotype, moons)
                self.patchmain = main[0]
                self.patchcolour = main[1]
                self.patchunders = [main[2], main[3]]
            else:
                self.tortpattern = self.ChooseTortiePattern()
                main = self.FindRed(self.genotype, moons, 'merle')
                self.maincolour = main[0]
                self.spritecolour = main[1]
                self.mainunders = [main[2], main[3]]
                main = self.FindRed(self.genotype, moons)
                self.patchmain = main[0]
                self.patchcolour = main[1]
                self.patchunders = [main[2], main[3]]

                self.genotype.tortiepattern = self.tortpattern
        elif('o' not in self.genotype.sexgene and self.genotype.specialred == 'blue-tipped'):
            self.tortpattern = 'BLUE-TIPPED'
            main = self.FindRed(self.genotype, moons)
            self.maincolour = main[0]
            self.spritecolour = main[1]
            self.mainunders = [main[2], main[3]]
            main = self.FindRed(self.genotype, moons, 'blue-tipped')
            self.patchmain = main[0]
            self.patchcolour = main[1]
            self.patchunders = [main[2], main[3]]

            self.genotype.tortiepattern = self.tortpattern
        elif ('o' not in self.genotype.sexgene) or (self.genotype.ext[0] == 'ea' and ((moons > 11 and self.genotype.agouti[0] != 'a') or (moons > 23))) or (self.genotype.ext[0] == 'er' and moons > 23 and 'O' not in self.genotype.sexgene) or (self.genotype.ext[0] == 'ec' and moons > 0 and (self.genotype.agouti[0] != 'a' or moons > 5)):
            main = self.FindRed(self.genotype, moons, special=self.genotype.ext[0])
            self.maincolour = main[0]
            self.spritecolour = main[1]
            self.mainunders = [main[2], main[3]]
        elif('O' not in self.genotype.sexgene):
            main = self.FindBlack(self.genotype, moons)
            self.maincolour = main[0]
            self.spritecolour = main[1]
            self.mainunders = [main[2], main[3]]
        else:
            if self.genotype.tortiepattern is not None:
                self.tortpattern = self.genotype.tortiepattern
            else:
                lowlist = [
                    'MINKBROKENBLAZE', 'MINKLIGHTTUXEDO', 'MINKLILTWO', 'MINKREVERSEEYE', 'MINKREVERSEHEART', 'MINKTIP',
                    'MINKTUXEDO', 'MINKSAVANNAH', 'MINKFANCY', 'MINKSQUEAKS', 'MINKSTAR', 'MINKMISS', 'MINKBOWTIE',
                    'MINKFCONE', 'MINKMIA', 'MINKPRINCESS', 'MINKDOUGIE', 'MINKEXTRA', 'MINKMITAINE', 'MINKWOODPECKER',
                    'MINKDAPPLEPAW', 'MINKOWL'
                ]
                medlist = [
                    'MINKRINGTAIL', 'MINKUNDERS', 'MINKFAROFA', 'MINKFRONT', 'MINKBLOSSOMSTEP', 'MINKDIGIT',
                    'MINKHAWKBLAZE', 'MINKSKUNK', 'MINKTOPCOVER', 'MINKVEST', 'MINKANY', 'MINKSHIBAINU', 'MINKSPARROW',
                    'MINKMISTER', 'MINKTRIXIE', 'MINKWINGS', 'MINKMAO', 'MINKMASKMANTLE', 'MINKPANTSTWO', 'MINKBUB',
                    'MINKBULLSEYE', 'MINKSCAR'
                ]
                highlist = [
                    'MINKANYTWO', 'MINKPEBBLESHINE', 'MINKBROKEN', 'MINKPIEBALD', 'MINKFRECKLES', 'MINKHALFFACE',
                    'MINKGOATEE', 'MINKPRINCE', 'MINKCAPSADDLE', 'MINKGLASS', 'MINKCOWTWO', 'MINKSAMMY', 'MINKBUSTER',
                    'MINKCAKE', 'MINKVAN', 'MINKLIGHTSONG', 'MINKLOVEBUG', 'MINKCURVED', 'MINKFINN', 'MINKTAIL',
                    'MINKAPRON', 'MINKHALFWHITE', 'MINKAPPALOOSA', 'MINKHEART', 'MINKMOORISH', 'MINKPEBBLE', 'MINKCOW',
                    'MINKSHOOTINGSTAR', 'MINKTAILTWO', 'MINKBUDDY', 'MINKKROPKA', 'MINKBLACKSTAR', 'MINKPETAL',
                    'MINKBOOTS'
                ]
                mink = False
                patterntype = "error"

                self.tortpattern = self.ChooseTortiePattern()
                if "MINK" in self.tortpattern:
                    mink = True
                    if self.tortpattern in lowlist:
                        patterntype = "low"
                    elif self.tortpattern in medlist:
                        patterntype = "med"
                    elif self.tortpattern in highlist:
                        patterntype = "high"
                    else:
                        print(f"ERROR: cat has an unknown tortie patch: {self.tortpattern}")

                if ((not mink or (mink and patterntype == "low")) and randint(1, 10) == 1) or (mink and patterntype in ["med", "error"] and randint(1, 2) == 1) or ((self.tortpattern == "BODY" or (mink and patterntype == "high")) and randint(1, 10) != 1):
                    self.tortpattern = 'rev'+self.tortpattern

                self.genotype.tortiepattern = self.tortpattern

            if 'rev' in self.tortpattern:
                if(self.genotype.brindledbi):
                    self.maincolour = "white"
                    self.spritecolour = "white"
                else:
                    main = self.FindRed(self.genotype, moons)
                    self.maincolour = main[0]
                    self.spritecolour = main[1]
                    self.mainunders = [main[2], main[3]]
                main = self.FindBlack(self.genotype, moons, self.genotype.ext[0])
                self.patchmain = main[0]
                self.patchcolour = main[1]
                self.patchunders = [main[2], main[3]]
            else:
                main = self.FindBlack(self.genotype, moons)
                self.maincolour = main[0]
                self.spritecolour = main[1]
                self.mainunders = [main[2], main[3]]
                if(self.genotype.brindledbi):
                    self.patchmain = "white"
                    self.patchcolour = "white"
                else:
                    main = self.FindRed(self.genotype, moons)
                    self.patchmain = main[0]
                    self.patchcolour = main[1]
                    self.patchunders = [main[2], main[3]]

    def FindEumUnders(self, genes, wideband, rufousing):
        if(genes.dilute[0] == "d"):
            if(genes.pinkdilute[0] == "dp"):
                colour = "ivory"
            else:
                colour = "cream"
        else:
            if(genes.pinkdilute[0] == "dp"):
                colour = "honey"
            else:
                colour = "red"


        if wideband in ["chinchilla", "shaded"]:
            colour = "lightbasecolours0"
        elif rufousing != "rufoused":
            colour = colour + "low" + wideband + "0"
        else:
            colour = colour + "medium" + wideband + "0"

        return colour

    def GetSilverUnders(self, wideband):
        if wideband == "low":
           return 20
        elif wideband == "medium":
            return 40
        elif wideband == "high":
            return 60
        elif wideband == "shaded":
            return 80
        else:
            return 100
    def GetRedUnders(self, wideband):
        if wideband == "low":
           return 20
        elif wideband == "medium":
            return 30
        elif wideband == "high":
            return 40
        elif wideband == "shaded":
            return 50
        else:
            return 60
    def FindBlack(self, genes, moons, special=None):
        unders_colour = ""
        unders_opacity = 0
        if special=='er':
            return self.FindRed(genes, moons, special)
        else:
            if genes.eumelanin[0] == "bl":
                if genes.dilutemd[0] == 'Dm':
                    self.caramel = 'caramel'

                if genes.dilute[0] == "d":
                    if(genes.pinkdilute[0] == "dp"):
                        colour = "beige"
                    else:
                        colour = "fawn"
                else:
                    if(genes.pinkdilute[0] == "dp"):
                        colour = "buff"
                    else:
                        colour = "cinnamon"
                        self.caramel = ""
            elif genes.eumelanin[0] == "b":
                if genes.dilutemd[0] == 'Dm':
                    self.caramel = 'caramel'

                if genes.dilute[0] == "d":
                    if(genes.pinkdilute[0] == "dp"):
                        colour = "lavender"
                    else:
                        colour = "lilac"
                else:
                    if(genes.pinkdilute[0] == "dp"):
                        colour = "champagne"
                    else:
                        colour = "chocolate"
                        self.caramel = ""
            else:
                if(genes.dilutemd[0] == 'Dm'):
                    self.caramel = 'caramel'

                if(genes.dilute[0] == "d"):
                    if(genes.pinkdilute[0] == "dp"):
                        colour = "platinum"
                    else:
                        colour = "blue"
                else:
                    if(genes.pinkdilute[0] == "dp"):
                        colour = "dove"
                    else:
                        colour = "black"
                        self.caramel = ""

            maincolour = colour

            rufousing = ""
            banding = ""

            if ('masked' in self.silvergold and genes.wbsum > 15) or (genes.agouti[0] != "a" and genes.ext[0] != "Eg") or (genes.ext[0] not in ['Eg', 'E']):
                if genes.silver[0] == "I" or genes.brindledbi or (moons < 3 and genes.karp[0] == "K"):
                    rufousing = "silver"
                elif genes.pointgene[0] != "C" or genes.agouti[0] == "Apb":
                    rufousing = "low"
                else:
                    rufousing = genes.ruftype

                if genes.corin[0] == "sg" or genes.wbtype == "chinchilla":
                    banding = "chinchilla"
                elif genes.wbtype == "shaded" or genes.corin[0] == "sh" or genes.corin[0] == "fg" or genes.ext[0] == 'ec' or (genes.ext[0] == 'ea' and moons > 3):
                    banding = "shaded"
                else:
                    banding = genes.wbtype

                if rufousing == "silver":
                    unders_colour = "lightbasecolours0"
                    unders_opacity = self.GetSilverUnders(banding)
                else:
                    unders_colour = self.FindEumUnders(genes, banding, rufousing)
                    unders_opacity = 33

                colour = colour + rufousing + banding + "0"




            return [maincolour, colour, unders_colour, unders_opacity]
    def FindRed(self, genes, moons, special = None):
        unders_colour = 'lightbasecolours0'
        unders_opacity = 0
        maincolour = genes.ruftype
        if special == 'er':
            if(genes.eumelanin[0] == 'B'):
                maincolour = 'rufoused'
            elif(genes.eumelanin[0] == 'b'):
                maincolour = 'medium'
            else:
                maincolour = 'low'
        if(genes.dilute[0] == "d" or (genes.specialred == 'cameo' and genes.silver[0] == 'I') or special == 'merle'):
            if(genes.pinkdilute[0] == "dp"):
                if genes.dilutemd[0] == "Dm":
                    colour = "ivory-apricot"
                else:
                    colour = "ivory"
            else:
                if genes.dilutemd[0] == "Dm" and not(genes.specialred == 'cameo' or special == 'merle'):
                    colour = "apricot"
                else:
                    colour = "cream"
        else:
            if(genes.pinkdilute[0] == "dp"):
                if genes.dilutemd[0] == "Dm":
                    colour = "honey-apricot"
                else:
                    colour = "honey"
            else:
                colour = "red"

        maincolour += colour

        rufousing = ""
        banding = ""
        if genes.silver[0] == "I" and special != 'nosilver' or (moons < 3 and genes.karp[0] == "K"):
            rufousing = "silver"
        elif genes.pointgene[0] not in ["C", "cm"] or special=='low':
            rufousing = "low"
        else:
            rufousing = genes.ruftype

        if genes.corin[0] == "sg" or genes.wbtype == "chinchilla":
            banding = "chinchilla"
        elif genes.corin[0] == "sh" or genes.corin[0] == "fg" or genes.wbtype == "shaded":
            banding = "shaded"
        else:
            banding = genes.wbtype


        if colour == "apricot":
            if rufousing == "low":
                colour = "cream"
                rufousing = "medium"
            elif rufousing == "medium":
                colour = "cream"
                rufousing = "rufoused"
            else:
                colour = "red"
                rufousing = "low"
        elif colour == "honey-apricot":
            if rufousing == "low":
                colour = "honey"
                rufousing = "medium"
            elif rufousing == "medium":
                colour = "honey"
                rufousing = "rufoused"
            else:
                colour = "red"
                rufousing = "low"
        elif colour == "ivory-apricot":
            if rufousing == "low":
                colour = "ivory"
                rufousing = "medium"
            elif rufousing == "medium":
                colour = "ivory"
                rufousing = "rufoused"
            else:
                colour = "honey"
                rufousing = "low"

        if (genes.ext[0] == "ec" and genes.agouti[0] == "a" and 'o' in genes.sexgene):
            unders_opacity = 0
        elif rufousing == "silver" or (genes.ext[0] == "ec" and genes.agouti[0] != "a" and 'o' in genes.sexgene):
            unders_opacity = self.GetSilverUnders(banding)
        else:
            unders_opacity = self.GetRedUnders(banding)
        colour = colour + rufousing + banding + "0"

        if(genes.specialred in ['blue-red', 'cinnamon']) or special == 'blue-tipped':
            colour = colour.replace('cream', 'lilac')
            colour = colour.replace('red', 'blue')
            colour = colour.replace('honey', 'dove')
            colour = colour.replace('ivory', 'lavender')
            if(genes.specialred == 'cinnamon'):
                if('red' in maincolour):
                    maincolour = 'cinnamon'
                elif('cream' in maincolour or maincolour == 'apricot'):
                    maincolour = 'fawn'
                elif('honey' in maincolour):
                    maincolour = 'buff'
                elif('ivory' in maincolour):
                    maincolour = 'beige'

                if('apricot' in maincolour):
                    self.caramel = 'caramel'
            if rufousing != "silver":
                unders_colour = self.FindEumUnders(genes, banding, rufousing)
                unders_opacity = 33

        return [maincolour, colour, unders_colour, unders_opacity]

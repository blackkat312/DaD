from random import choice, randint, random
import json
from scripts.cat.breed_functions import breed_functions
from operator import xor
import math


class Genotype:
    def __init__(self, odds, ban_genes=True, spec=None):
        self.odds = odds
        self.ban_genes = ban_genes
        self.chimerapattern = None
        if spec != "chimera":
            self.chimera = False
        else:
            self.chimera = True if odds['chimera'] > 0 and randint(1, odds['chimera']) == 1 else False
        if self.chimera:
            self.chimerageno = Genotype(self.odds, self.ban_genes, 'chimera')
        else:
            self.chimerageno = None

        self.fevercoat = False

        self.furLength = ["", ""]
        self.longtype = 'long'
        self.eumelanin = ["", ""]
        self.sexgene = ["", ""]
        self.specialred = None
        self.tortiepattern = None
        self.pseudomerle = False
        self.merlepattern = None
        self.brindledbi = False
        self.sex = ["", ""]
        self.dilute = ["", ""]
        self.white = ["", ""]
        self.whitegrade = randint(1, 5)
        self.white_pattern = []
        self.vitiligo = False
        self.deaf = False
        self.pointgene = ["", ""]
        self.silver = ["", ""]
        self.agouti = ["", ""]
        self.mack = ["", ""]
        self.ticked = ["", ""]
        self.breakthrough = False

        self.wirehair = ["wh", "wh"]
        self.laperm = ["lp", "lp"]
        self.cornish = ["R", "R"]
        self.urals = ["Ru", "Ru"]
        self.tenn = ["Tr", "Tr"]
        self.fleece = ["Fc", "Fc"]
        self.sedesp = ["Hr", "Hr"]
        self.ruhr = ["hrbd", "hrbd"]
        self.ruhrmod = ""
        self.lykoi = ["Ly", "Ly"]

        self.pinkdilute = ["Dp", "Dp"]
        self.dilutemd = ["dm", "dm"]
        self.ext = ["E", "E"]
        self.corin = ["N", "N"]
        self.karp = ["k", "k"]
        self.bleach = ["Lb", "Lb"]
        self.ghosting = ["gh", "gh"]
        self.satin = ["St", "St"]
        self.glitter = ["Gl", "Gl"]

        self.curl = ["cu", "cu"]
        self.fold = ["fd", "fd"]
        self.manx = ["ab", "ab"]
        self.manxtype = choice(["long", "most", "most", "stubby", "stubby", "stubby", "stubby", "stubby", "stubby", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "riser", "riser", "riser", "riser", "riser", "riser", "riser", "riser", "riser", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy"])
        self.kab = ["Kab", "Kab"]
        self.toybob = ["tb", "tb"]
        self.jbob = ["Jb", "Jb"]
        self.kub = ["kub", "kub"]
        self.ring = ["Rt", "Rt"]
        self.munch = ["mk", "mk"]
        self.poly = ["pd", "pd"]
        self.pax3 = ["NoDBE", "NoDBE"]

        self.wideband = ""
        self.wbtype = ""
        self.wbsum = 0

        self.saturation = choice(odds['saturation'])

        self.rufousing = ""
        self.ruftype = ""
        self.rufsum = 0

        self.bengal = ""
        self.bengtype = ""
        self.bengsum = 0

        self.sokoke = ""
        self.soktype = ""
        self.soksum = 0

        self.spotted = ""
        self.spottype = ""
        self.spotsum = 0

        self.tickgenes = ""
        self.ticktype = ""
        self.ticksum = 0

        self.body_ranges = odds['body_ranges']
        self.height_ranges = odds['height_ranges']

        def getindexes(m, size):
            inds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            for i in range(0, size):
                for j in range(0, i+1):
                    inds[i] += m[j]

            return inds
        self.body_indexes = getindexes(self.body_ranges, 7)
        self.height_indexes = getindexes(self.height_ranges, 10)

        self.body_value = 0
        self.height_value = 0
        self.shoulder_height = 0
        self.body_label = ""
        self.height_label = ""

        self.refraction = False
        self.pigmentation = False

        self.lefteye = ""
        self.righteye = ""
        self.lefteyetype = "Error"
        self.righteyetype = "Error"

        self.extraeye = None
        self.extraeyetype = ""
        self.extraeyecolour = ""

        self.breeds = {}
        self.somatic = {}

    def __getitem__(self, name):
        return getattr(self, name)

    def fromJSON(self, jsonstring):
        try:
            self.fevercoat = jsonstring["fevercoat"]
        except:
            pass
        self.furLength = jsonstring["furLength"]
        self.eumelanin = jsonstring["eumelanin"]
        self.sexgene = jsonstring["sexgene"]
        self.tortiepattern = jsonstring["tortiepattern"]
        if self.tortiepattern and not isinstance(self.tortiepattern, list):
            self.tortiepattern = [self.tortiepattern]
        self.brindledbi = jsonstring["brindledbi"]

        self.specialred = jsonstring['specialred']

        self.merlepattern = jsonstring.get('merlepattern', None)
        try:
            self.pseudomerle = jsonstring['pseudomerle']
        except:
            pass

        self.chimera = jsonstring['chimera']
        self.chimerapattern = jsonstring['chimerapattern']
        if self.chimerapattern and not isinstance(self.chimerapattern, list):
            self.chimerapattern = [self.chimerapattern]
        if(jsonstring["chimerageno"]):
            self.chimerageno = Genotype(self.odds, self.ban_genes, 'chimera')
            self.chimerageno.fromJSON(jsonstring["chimerageno"])
        else:
            self.chimerageno = None
        self.longtype = jsonstring["longtype"]

        try:
            self.sex = jsonstring["sex"]
        except:
            self.sex = jsonstring["gender"]
        self.dilute = jsonstring["dilute"]
        self.white = jsonstring["white"]
        self.whitegrade = jsonstring["whitegrade"]
        self.vitiligo = jsonstring["vitiligo"]
        self.pointgene = jsonstring["pointgene"]
        self.silver = jsonstring["silver"]
        self.agouti = jsonstring["agouti"]
        self.mack = jsonstring["mack"]
        self.ticked = jsonstring["ticked"]
        self.breakthrough = jsonstring["breakthrough"]

        self.wirehair = jsonstring["wirehair"]
        self.laperm = jsonstring["laperm"]
        self.cornish = jsonstring["cornish"]
        self.urals = jsonstring["urals"]
        self.tenn = jsonstring["tenn"]
        self.fleece = jsonstring["fleece"]
        self.sedesp = jsonstring["sedesp"]
        self.ruhr = jsonstring["ruhr"]
        self.ruhrmod = jsonstring["ruhrmod"]
        self.lykoi = jsonstring["lykoi"]
    
        self.pinkdilute = jsonstring["pinkdilute"]
        self.dilutemd = jsonstring["dilutemd"]
        self.ext = jsonstring["ext"]
        self.corin = jsonstring["corin"]
        self.karp = jsonstring["karp"]
        self.bleach = jsonstring["bleach"]
        self.ghosting = jsonstring["ghosting"]
        self.satin = jsonstring["satin"]
        self.glitter = jsonstring["glitter"]
    
        self.curl = jsonstring["curl"]
        self.fold = jsonstring["fold"]
        self.manx = jsonstring["manx"]
        self.manxtype = jsonstring["manxtype"]
        self.kab = jsonstring["kab"]
        self.toybob = jsonstring["toybob"]
        self.jbob = jsonstring["jbob"]
        self.kub = jsonstring["kub"]
        self.ring = jsonstring["ring"]
        self.munch = jsonstring["munch"]
        self.poly = jsonstring["poly"]
        self.pax3 = jsonstring["pax3"]

        self.wideband = jsonstring["wideband"]

        try:
            self.saturation = jsonstring["saturation"]
        except:
            pass

        self.rufousing = jsonstring["rufousing"]

        self.bengal = jsonstring["bengal"]

        self.sokoke = jsonstring["sokoke"]

        self.spotted = jsonstring["spotted"]

        self.tickgenes = jsonstring["tickgenes"]

        self.refraction = jsonstring["refraction"]
        self.pigmentation = jsonstring["pigmentation"]

        self.lefteye = jsonstring["lefteye"]
        self.righteye = jsonstring["righteye"]
        self.lefteyetype = jsonstring["lefteyetype"]
        self.righteyetype = jsonstring["righteyetype"]
        
        self.extraeye = jsonstring["extraeye"]
        self.extraeyetype = jsonstring["extraeyetype"]
        self.extraeyecolour = jsonstring["extraeyecolour"]

        self.breeds = json.loads(jsonstring["breeds"])
        self.somatic = json.loads(jsonstring["somatic"])
        self.body_value = jsonstring["body_type"]
        self.height_value = jsonstring["height"]
        self.shoulder_height = jsonstring["shoulder_height"]
        self.body_label = jsonstring["body_type_label"]

        self.GeneSort()
        self.PolyEval()
        self.EyeColourName()

    def toJSON(self):
        chimgen = None

        if self.chimerageno:
            chimgen = self.chimerageno.toJSON()

        return {
            "fevercoat" : self.fevercoat,
            "furLength": self.furLength,
            "longtype": self.longtype,
            "eumelanin": self.eumelanin,
            "sexgene" : self.sexgene,
            "specialred" : self.specialred,
            "tortiepattern" : self.tortiepattern,
            "brindledbi" : self.brindledbi,

            "pseudomerle" : self.pseudomerle,
            "merlepattern" : self.merlepattern,
            "chimera" : self.chimera,
            "chimerapattern" : self.chimerapattern,
            "chimerageno" : chimgen,

            "sex": self.sex,
            "dilute": self.dilute,
            "white" : self.white,
            "whitegrade" : self.whitegrade,
            "vitiligo" : self.vitiligo,
            "pointgene" : self.pointgene,
            "silver" : self.silver,
            "agouti" : self.agouti,
            "mack" : self.mack,
            "ticked" : self.ticked,
            "breakthrough" : self.breakthrough,

            "wirehair" : self.wirehair,
            "laperm" : self.laperm,
            "cornish" : self.cornish,
            "urals" : self.urals,
            "tenn" : self.tenn,
            "fleece" : self.fleece,
            "sedesp" : self.sedesp,
            "ruhr" : self.ruhr,
            "ruhrmod" : self.ruhrmod,
            "lykoi" : self.lykoi,

            "pinkdilute" : self.pinkdilute,
            "dilutemd" : self.dilutemd,
            "ext" : self.ext,
            "corin" : self.corin,
            "karp" : self.karp,
            "bleach" : self.bleach,
            "ghosting" : self.ghosting,
            "satin" : self.satin,
            "glitter" : self.glitter,

            "curl" : self.curl,
            "fold" : self.fold,
            "manx" : self.manx,
            "manxtype" : self.manxtype,
            "kab" : self.kab,
            "toybob" : self.toybob,
            "jbob" : self.jbob,
            "kub" : self.kub,
            "ring" : self.ring,
            "munch" : self.munch,
            "poly" : self.poly,
            "pax3" : self.pax3,

            "wideband" : self.wideband,
            "saturation" : self.saturation,
            "rufousing" : self.rufousing,
            "bengal" : self.bengal,
            "sokoke" : self.sokoke,
            "spotted" : self.spotted,
            "tickgenes" : self.tickgenes,
            "refraction" :self.refraction,
            "pigmentation" : self.pigmentation,
            
            "lefteye" : self.lefteye,
            "righteye" : self.righteye,
            "lefteyetype" :self.lefteyetype,
            "righteyetype" : self.righteyetype,
            
            "extraeye" : self.extraeye,
            "extraeyetype" :self.extraeyetype,
            "extraeyecolour" : self.extraeyecolour,

            "body_type" : self.body_value,
            "body_type_label" : self.body_label,
            "height" : self.height_value,
            "shoulder_height" : self.shoulder_height,

            "breeds" : json.dumps(self.breeds),
            "somatic" : json.dumps(self.somatic)
        }

    def Generator(self, special=None):
        if self.chimera:
            par1 = Genotype(self.odds, self.ban_genes, 'chimera')
            par2 = Genotype(self.odds, self.ban_genes, 'chimera')
            par1.Generator()
            par2.Generator()
            self.KitGenerator(par1, par2)
            if self.munch[1] == 'Mk':
                self.munch[1] = "mk"
            if self.fold[1] == 'Fd':
                self.fold[1] = 'Fd'
            if self.manx[1] not in ['m', 'ab']:
                self.manx[1] = self.manx[1].lower()
            if 'NoDBE' not in self.pax3 and 'DBEalt' not in self.pax3:
                self.pax3[0] = 'DBEalt'
            if self.sexgene[0] == "Y":
                if randint(1, self.odds["red"]) == 1:
                    self.sexgene[0] = "O"
                else:
                    self.sexgene[0] = "o"

            return

        if self.odds["other_breed"] > 0 and randint(1, self.odds["other_breed"]) == 1:
            return self.BreedGenerator(special)
        
        if self.odds["vitiligo"] > 0 and randint(1, self.odds["vitiligo"]) == 1:
            self.vitiligo = True

        self.GenerateBody()

        # FUR LENGTH
        
        for i in range(2):
            if self.odds["longhair"] > 0 and randint(1, self.odds["longhair"]) > 3:
                self.furLength[i] = "l"
            else:
                self.furLength[i] = "L"

        # EUMELANIN

            if self.odds["cinnamon"] > 0 and randint(1, self.odds["cinnamon"]) == 1:
                self.eumelanin[i] = "bl"
            elif self.odds["chocolate"] > 0 and randint(1, self.odds["chocolate"]) == 1:
                self.eumelanin[i] = "b"
            else:
                self.eumelanin[i] = "B"

        # RED GENE

        self.sexgene = []
        if special == "fem":
            egg1 = "X"
            sperm1 = "X"
        elif special == "masc":
            egg1 = "X"
            sperm1 = "Y"
        else:
            if randint(1, self.odds['XXX/XXY']) == 1:
                egg1 = choice(["XX", "null"])
            else:
                egg1 = "X"

            if randint(1, self.odds['XXX/XXY']) == 1:
                sperm1 = choice(["XX", "XY", "YY", "null"])
            else:
                sperm1 = choice(["X", "Y"])

        while sperm1 == "Y" and egg1 == "null":
            sperm1 = choice(["X", "Y"])
            egg1 = choice(["XX", "null"])
        while (sperm1 == "YY" or sperm1 == "null") and egg1 == "null":
            sperm1 = choice(["XX", "XY", "YY", "null"])
            egg1 = choice(["XX", "null"])
        while sperm1 == "null" and egg1 == "null":
            sperm1 = choice(["XX", "XY", "YY", "null"])
            egg1 = choice(["XX", "null"])
            while (sperm1 == "YY" or sperm1 == "null") and egg1 == "null":
                sperm1 = choice(["XX", "XY", "YY", "null"])
                egg1 = choice(["XX", "null"])

        randnum = randint(1, 100)
        while sperm1 == "null" and egg1 == "X" and not ((randnum <= 37 and randint(1, 200) == 1) or not randnum <= 37):
            randnum = randint(1, 100)
            sperm1 = choice(["XX", "XY", "YY", "null"])

        randnum = randint(1, 100)
        while sperm1 == "X" and egg1 == "null" and not ((randnum <= 37 and randint(1, 200) == 1) or not randnum <= 37):
            randnum = randint(1, 100)
            sperm1 = choice(["X", "Y"])
            egg1 = choice(["XX", "null"])
            while sperm1 == "Y" and egg1 == "null":
                sperm1 = choice(["X", "Y"])
                egg1 = choice(["XX", "null"])

        for entry in egg1:
            self.sexgene.append(entry)
        for entry in sperm1:
            self.sexgene.append(entry)

        for i in range(1, 20):
            if "" in self.sexgene:
                self.sexgene.remove("")
            if "null" in self.sexgene:
                self.sexgene.remove("null")
            if "n" in self.sexgene:
                self.sexgene.remove("n")
            if "u" in self.sexgene:
                self.sexgene.remove("u")
            if "l" in self.sexgene:
                self.sexgene.remove("l")

        index = 0
        while index <= (len(self.sexgene) - 1):
            if self.sexgene[index] == "X":
                if randint(1, self.odds["red"]) == 1:
                    self.sexgene[index] = "O"
                else:
                    self.sexgene[index] = "o"
            index += 1

        if self.sexgene[0] == "Y":
            if randint(1, self.odds["red"]) == 1:
                self.sexgene = ["O"]
            else:
                self.sexgene = ["o"]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's first sexgene is Y in genotype.py Generator")
        if len(self.sexgene) > 4:
            self.sexgene = self.sexgene[:4]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's sexgene is longer than 4 in genotype.py Generator")
        if not self.sexgene:
            if randint(1, self.odds["red"]) == 1:
                self.sexgene = ["O"]
            else:
                self.sexgene = ["o"]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's sexgene is nothing in genotype.py Generator")

        if 'O' in self.sexgene and self.odds['brindled_bicolour'] > 0 and randint(1, self.odds['brindled_bicolour'])==1:
            self.brindledbi = True 
        if self.odds['pseudo_merle'] > 0 and randint(1, self.odds['pseudo_merle'])==1:
            self.pseudomerle = True

        if(random() < 0.05):
            self.specialred = choice(['cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'blue-red', 'blue-tipped', 'blue-tipped', 'blue-tipped', 'cinnamon'])

        # DILUTE

        for i in range(2):
            if self.odds["dilute"] > 0 and randint(1, self.odds["dilute"]) > 3:
                self.dilute[i] = "d"
            else:
                self.dilute[i] = "D"
        # WHITE
            if self.odds["birman gloving"] > 0 and randint(1, self.odds["birman gloving"]) == 1:
                self.white[i] = "wg"
            elif self.odds["thai white"] > 0 and randint(1, self.odds["thai white"]) == 1:
                self.white[i] = "wt"
            elif self.odds["salmiak"] > 0 and randint(1, self.odds["salmiak"]) == 1:
                self.white[i] = "wsal"
            elif self.odds["dominant white"] > 0 and randint(1, self.odds["dominant white"]) == 1:
                self.white[i] = "W"
            elif self.odds["white spotting"] > 0 and randint(1, self.odds["white spotting"]) > 3:
                self.white[i] = "ws"
            else:
                self.white[i] = "w"

        # ALBINO

            if self.odds["albino"] > 0 and randint(1, self.odds["albino"]) == 1 and not self.ban_genes:
                self.pointgene[i] = "c"
            elif self.odds["mocha"] > 0 and randint(1, self.odds["mocha"]) == 1:
                self.pointgene[i] = "cm"
            elif self.odds["sepia"] > 0 and randint(1, self.odds["sepia"]) == 1:
                self.pointgene[i] = "cb"
            elif self.odds["colourpoint"] > 0 and randint(1, self.odds["colourpoint"]) == 1:
                self.pointgene[i] = "cs"
            else:
                self.pointgene[i] = "C"

        # SILVER

            if self.odds["silver"] > 0 and randint(1, self.odds["silver"]) == 1:
                self.silver[i] = "I"
            else:
                self.silver[i] = "i"

        # AGOUTI

            if self.odds["charcoal"] > 0 and randint(1, self.odds["charcoal"]) == 1:
                self.agouti[i] = "Apb"
            elif self.odds["solid"] > 0 and randint(1, self.odds["solid"]) > 3:
                self.agouti[i] = "a"
            else:
                self.agouti[i] = "A"

        # MACKEREL
            if self.odds["blotched"] > 0 and randint(1, self.odds["blotched"]) == 1:
                self.mack[i] = "mc"
            else:
                self.mack[i] = "Mc"

        # TICKED
            if self.odds["ticked"] > 0 and randint(1, self.odds["ticked"]) == 1:
                self.ticked[i] = "Ta"
            else:
                self.ticked[i] = "ta"

        if self.odds["breakthrough"] > 0 and randint(1, self.odds["breakthrough"]) == 1:
            self.breakthrough = True

        # YORK, WIREHAIR, LAPERM, CORNISH, URAL, TENN, FLEECE

        for i in range(2):
            if self.odds["wirehair"] > 0 and randint(1, self.odds["wirehair"]) == 1:
                self.wirehair[i] = "Wh"
            if self.odds["laperm"] > 0 and randint(1, self.odds["laperm"]) == 1:
                self.laperm[i] = "Lp"
            if self.odds["cornish"] > 0 and randint(1, self.odds["cornish"]) == 1:
                self.cornish[i] = "r"
            if self.odds["urals"] > 0 and randint(1, self.odds["urals"]) == 1:
                self.urals[i] = "ru"
            if self.odds["tenn"] > 0 and randint(1, self.odds["tenn"]) == 1:
                self.tenn[i] = "tr"
            if self.odds["fleece"] > 0 and randint(1, self.odds["fleece"]) == 1:
                self.fleece[i] = "fc"


        #SELKIRK/DEVON/HAIRLESS

            if self.odds["canadian hairless"] > 0 and randint(1, self.odds["canadian hairless"]) == 1:
                self.sedesp[i] = "hr"
            elif self.odds["devon"] > 0 and randint(1, self.odds["devon"]) == 1:
                self.sedesp[i] = "re"
            elif self.odds["selkirk"] > 0 and randint(1, self.odds["selkirk"]) == 1:
                self.sedesp[i] = "Se"


        #ruhr + ruhrmod + lykoi
            if self.odds["russian hairless"] > 0 and randint(1, self.odds["russian hairless"]) == 1 and not self.ban_genes:
                self.ruhr[i] = "Hrbd"
            if self.odds["lykoi"] > 0 and randint(1, self.odds["lykoi"]) == 1 and not self.ban_genes:
                self.lykoi[i] = "ly"
        
        a = randint(1, 4)

        if a == 1:
            self.ruhrmod = ["hi", "hi"]
        elif a == 4:
            self.ruhrmod = ["ha", "ha"]
        else:
            self.ruhrmod = ["hi", "ha"]

        # pinkdilute + dilutemd

        for i in range(2):
            if self.odds["pink-eyed dilute"] > 0 and randint(1, self.odds["pink-eyed dilute"]) == 1 and not self.ban_genes:
                self.pinkdilute[i] = "dp"
            if self.odds["dilute modifier"] > 0 and randint(1, self.odds["dilute modifier"]) == 1:
                self.dilutemd[i] = "Dm"

        # ext

            if self.odds["grizzle"] > 0 and randint(1, self.odds["grizzle"]) == 1:
                self.ext[i] = "Eg"
            elif self.odds["carnelian"] > 0 and randint(1, self.odds["carnelian"]) == 1:
                self.ext[i] = "ec"
            elif self.odds["russet"] > 0 and randint(1, self.odds["russet"]) == 1:
                self.ext[i] = "er"
            elif self.odds["amber"] > 0 and randint(1, self.odds["amber"]) == 1:
                self.ext[i] = "ea"

        #sunshine

            if self.odds["sunshine"] > 0 and randint(1, self.odds["sunshine"]) == 1:
                self.corin[i] = "sh" #sunSHine
            elif self.odds["extreme sunshine"] > 0 and randint(1, self.odds["extreme sunshine"]) == 1:
                self.corin[i] = "sg" #Siberian Gold / extreme sunshine
            elif self.odds["copper"] > 0 and randint(1, self.odds["copper"]) == 1:
                self.corin[i] = "fg" #Flaxen Gold
            else:
                self.corin[i] = "N" #No

        # karp + bleach + ghosting + satin + glitter

            if self.odds["karpati"] > 0 and randint(1, self.odds["karpati"]) == 1:
                self.karp[i] = "K"
            if self.odds["bleaching"] > 0 and randint(1, self.odds["bleaching"]) == 1:
                self.bleach[i] = "lb"
            if self.odds["ghosting"] > 0 and randint(1, self.odds["ghosting"]) == 1:
                self.ghosting[i] = "Gh"
            if self.odds["satin"] > 0 and randint(1, self.odds["satin"]) == 1:
                self.satin[i] = "st"
            if self.odds["glitter"] > 0 and randint(1, self.odds["glitter"]) == 1:
                self.glitter[i] = "gl"

        # curl + fold

            if self.odds["curl"] > 0 and randint(1, self.odds["curl"]) == 1:
                self.curl[i] = "Cu"

        if self.odds["fold"] > 0 and randint(1, self.odds["fold"]) == 1 and not self.ban_genes:
            self.fold[0] = "Fd"

        #  manx + kab + toybob + jbob + kub + ring

        if self.odds["american bobtail"] > 0 and randint(1, self.odds["american bobtail"]) == 1:
            self.manx = ["Ab", "ab"]
        elif self.odds["manx"] > 0 and randint(1, self.odds["manx"]) == 1 and not self.ban_genes:
            self.manx = ["M", "m"]
        
        for i in range(2):
            if self.odds["karelian bobtail"] > 0 and randint(1, self.odds["karelian bobtail"]) == 1:
                self.kab[i] = "kab"
            if self.odds["toybob"] > 0 and randint(1, self.odds["toybob"]) == 1:
                self.toybob[i] = "Tb"
            if self.odds["kurilian bobtail"] > 0 and randint(1, self.odds["kurilian bobtail"]) == 1:
                self.kub[i] = "Kub"
            if self.odds["japanese bobtail"] > 0 and randint(1, self.odds["japanese bobtail"]) == 1:
                self.jbob[i] = "jb"
            if self.odds["ringtail"] > 0 and randint(1, self.odds["ringtail"]) == 1:
                self.ring[i] = "rt"
        
        # munch + poly + altai

        if self.odds["munchkin"] > 0 and randint(1, self.odds["munchkin"]) == 1 and not self.ban_genes:
            self.munch[0] = "Mk"

        for i in range(2):
            if self.odds["polydactyl"] > 0 and randint(1, self.odds["polydactyl"]) == 1:
                self.poly[i] = "Pd"
        
        if self.odds["DBE"] > 0 and randint(1, self.odds["DBE"] ** 2) == 1 and not self.ban_genes:
            self.pax3 = ['DBEalt', choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])]
        elif self.odds["DBE"] > 0 and randint(1, self.odds["DBE"]) == 1 and not self.ban_genes:
            self.pax3[0] = choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])

        widegenes = ["0", "0", "1", "1", "1", "2", "2"]
        genesspot = ["2", "1", "0"]

        self.wideband = ''
        self.rufousing = ''
        self.spotted = ''
        self.tickgenes = ''
        self.bengal = ''
        self.sokoke = ''
        self.refraction = ''
        self.pigmentation = ''
        
        for i in range(0, 8):
            self.wideband += choice(widegenes)
            self.wbsum += int(self.wideband[i])

        for i in range(0, 4):
            self.rufousing += choice(genesspot)
            self.rufsum += int(self.rufousing[i])

        for i in range(0, 4):
            self.spotted += choice(genesspot)
            self.spotsum += int(self.spotted[i])

        genesmild = ["2", "2", "1", "1", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0"]

        for i in range(0, 4):
            self.tickgenes += choice(genesmild)
            self.ticksum += int(self.tickgenes[i])

        for i in range(0, 4):
            self.bengal += choice(genesmild)
            self.bengsum += int(self.bengal[i])

        sokgenes = ["2", "2", "1", "1", "1", "0", "0", "0", "0"]

        for i in range(0, 4):
            self.sokoke += choice(sokgenes)
            self.soksum += int(self.sokoke[i])

        self.GeneSort()
        self.PolyEval()

        if self.odds['somatic_mutation'] > 0 and randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()

        self.EyeColourFinder()

    def AltGenerator(self, special=None):
        if self.chimera:
            par1 = Genotype(self.odds, self.ban_genes, 'chimera')
            par2 = Genotype(self.odds, self.ban_genes, 'chimera')
            par1.AltGenerator()
            par2.AltGenerator()
            self.KitGenerator(par1, par2)
            if self.munch[1] == 'Mk':
                self.munch[1] = "mk"
            if self.fold[1] == 'Fd':
                self.fold[1] = 'Fd'
            if self.manx[1] not in ['m', 'ab']:
                self.manx[1] = self.manx[1].lower()
            if 'NoDBE' not in self.pax3 and 'DBEalt' not in self.pax3:
                self.pax3[0] = 'DBEalt'
            if self.sexgene[0] == "Y":
                if randint(1, self.odds["red"]) == 1:
                    self.sexgene[0] = "O"
                else:
                    self.sexgene[0] = "o"

            return

        if self.odds["kittypet_breed"] > 0 and randint(1, self.odds["kittypet_breed"]) == 1:
            return self.BreedGenerator(special)

        if self.odds["vitiligo"] > 0 and randint(1, self.odds["vitiligo"]) == 1:
            self.vitiligo = True

        self.GenerateBody()

        # FUR LENGTH

        for i in range(2):
            if self.odds["longhair"] > 0 and randint(1, self.odds["longhair"]) > 3:
                self.furLength[i] = "l"
            else:
                self.furLength[i] = "L"

        # EUMELANIN

            if self.odds["cinnamon"] > 0 and (randint(1, round(self.odds["cinnamon"]/2)) == 1 or self.odds["cinnamon"] == 1):
                self.eumelanin[i] = "bl"
            elif self.odds["chocolate"] > 0 and (randint(1, round(self.odds["chocolate"]/2)) == 1 or self.odds["chocolate"] == 1):
                self.eumelanin[i] = "b"
            else:
                self.eumelanin[i] = "B"

        # RED GENE

        self.sexgene = []
        if special == "fem":
            if randint(1, self.odds['XXX/XXY']) == 1:
                egg1 = choice(["XX", "null"])
            else:
                egg1 = "X"

            if randint(1, self.odds['XXX/XXY']) == 1:
                sperm1 = choice(["XX", "null"])
            else:
                sperm1 = "X"
        elif special == "masc":
            if randint(1, self.odds['XXX/XXY']) == 1:
                egg1 = choice(["XX", "null"])
            else:
                egg1 = "X"

            if randint(1, self.odds['XXX/XXY']) == 1:
                sperm1 = choice(["XY", "YY"])
            else:
                sperm1 = "Y"
        else:
            if randint(1, self.odds['XXX/XXY']) == 1:
                egg1 = choice(["XX", "null"])
            else:
                egg1 = "X"

            if randint(1, self.odds['XXX/XXY']) == 1:
                sperm1 = choice(["XX", "XY", "YY", "null"])
            else:
                sperm1 = choice(["X", "Y"])

        while sperm1 == "Y" and egg1 == "null":
            sperm1 = choice(["X", "Y"])
            egg1 = choice(["XX", "null"])
        while (sperm1 == "YY" or sperm1 == "null") and egg1 == "null":
            sperm1 = choice(["XX", "XY", "YY", "null"])
            egg1 = choice(["XX", "null"])
        while sperm1 == "null" and egg1 == "null":
            sperm1 = choice(["XX", "XY", "YY", "null"])
            egg1 = choice(["XX", "null"])
            while (sperm1 == "YY" or sperm1 == "null") and egg1 == "null":
                sperm1 = choice(["XX", "XY", "YY", "null"])
                egg1 = choice(["XX", "null"])

        randnum = randint(1, 100)
        while sperm1 == "null" and egg1 == "X" and not ((randnum <= 37 and randint(1, 200) == 1) or not randnum <= 37):
            randnum = randint(1, 100)
            sperm1 = choice(["XX", "XY", "YY", "null"])

        randnum = randint(1, 100)
        while sperm1 == "X" and egg1 == "null" and not ((randnum <= 37 and randint(1, 200) == 1) or not randnum <= 37):
            randnum = randint(1, 100)
            sperm1 = choice(["X", "Y"])
            egg1 = choice(["XX", "null"])
            while sperm1 == "Y" and egg1 == "null":
                sperm1 = choice(["X", "Y"])
                egg1 = choice(["XX", "null"])

        for entry in egg1:
            self.sexgene.append(entry)
        for entry in sperm1:
            self.sexgene.append(entry)

        for i in range(1, 20):
            if "" in self.sexgene:
                self.sexgene.remove("")
            if "null" in self.sexgene:
                self.sexgene.remove("null")
            if "n" in self.sexgene:
                self.sexgene.remove("n")
            if "u" in self.sexgene:
                self.sexgene.remove("u")
            if "l" in self.sexgene:
                self.sexgene.remove("l")

        index = 0
        while index <= (len(self.sexgene) - 1):
            if self.sexgene[index] == "X":
                if randint(1, self.odds["red"]) == 1:
                    self.sexgene[index] = "O"
                else:
                    self.sexgene[index] = "o"
            index += 1

        if self.sexgene[0] == "Y":
            if randint(1, self.odds["red"]) == 1:
                self.sexgene = ["O"]
            else:
                self.sexgene = ["o"]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's first sexgene is Y in genotype.py AltGenerator")
        if len(self.sexgene) > 4:
            self.sexgene = self.sexgene[:4]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's sexgene is longer than 4 in genotype.py AltGenerator")
        if not self.sexgene:
            if randint(1, self.odds["red"]) == 1:
                self.sexgene = ["O"]
            else:
                self.sexgene = ["o"]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's sexgene is nothing in genotype.py AltGenerator")

        if 'O' in self.sexgene and self.odds['brindled_bicolour'] > 0 and randint(1, self.odds['brindled_bicolour'])==1:
            self.brindledbi = True 

        if self.odds['pseudo_merle'] > 0 and randint(1, self.odds['pseudo_merle'])==1:
            self.pseudomerle = True

        if(random() < 0.05):
            self.specialred = choice(['cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'blue-red', 'blue-tipped', 'blue-tipped', 'blue-tipped', 'cinnamon'])

        # DILUTE

        for i in range(2):
            if self.odds["dilute"] > 0 and randint(1, self.odds["dilute"]) > 3:
                self.dilute[i] = "d"
            else:
                self.dilute[i] = "D"

        # WHITE


            if self.odds["birman gloving"] > 0 and (randint(1, round(self.odds["birman gloving"]/2)) == 1 or self.odds["birman gloving"] == 1):
                self.white[i] = "wg"
            elif self.odds["thai white"] > 0 and (randint(1, round(self.odds["thai white"]/2)) == 1 or self.odds["thai white"] == 1):
                self.white[i] = "wt"
            elif self.odds["salmiak"] > 0 and (randint(1, round(self.odds["salmiak"]/2)) == 1 or self.odds["salmiak"] == 1):
                self.white[i] = "wsal"
            elif self.odds["dominant white"] > 0 and randint(1, self.odds["dominant white"]) == 1:
                self.white[i] = "W"
            elif self.odds["white spotting"] > 0 and randint(1, self.odds["white spotting"]) > 3:
                self.white[i] = "ws"
            else:
                self.white[i] = "w"

        # ALBINO

            if self.odds["albino"] > 0 and (randint(1, round(self.odds["albino"]/2)) == 1 or self.odds["albino"] == 1) and not self.ban_genes:
                self.pointgene[i] = "c"
            elif self.odds["mocha"] > 0 and (randint(1, round(self.odds["mocha"]/2)) == 1 or self.odds["mocha"] == 1):
                self.pointgene[i] = "cm"
            elif self.odds["sepia"] > 0 and (randint(1, round(self.odds["sepia"]/2)) == 1 or self.odds["sepia"] == 1):
                self.pointgene[i] = "cb"
            elif self.odds["colourpoint"] > 0 and (randint(1, round(self.odds["colourpoint"]/2)) == 1 or self.odds["colourpoint"] == 1):
                self.pointgene[i] = "cs"
            else:
                self.pointgene[i] = "C"

        # SILVER

            if self.odds["silver"] > 0 and randint(1, self.odds["silver"]) == 1:
                self.silver[i] = "I"
            else:
                self.silver[i] = "i"

        # AGOUTI

            if self.odds["charcoal"] > 0 and (randint(1, round(self.odds["charcoal"]/2)) == 1 or self.odds["charcoal"] == 1):
                self.agouti[i] = "Apb"
            elif self.odds["solid"] > 0 and randint(1, self.odds["solid"]) > 3:
                self.agouti[i] = "a"
            else:
                self.agouti[i] = "A"

        # MACKEREL
            if self.odds["blotched"] > 0 and randint(1, self.odds["blotched"]) == 1:
                self.mack[i] = "mc"
            else:
                self.mack[i] = "Mc"

        # TICKED
            if self.odds["ticked"] > 0 and randint(1, self.odds["ticked"]) == 1:
                self.ticked[i] = "Ta"
            else:
                self.ticked[i] = "ta"

        if self.odds["breakthrough"] > 0 and randint(1, self.odds["breakthrough"]) == 1:
            self.breakthrough = True

        # YORK, WIREHAIR, LAPERM, CORNISH, URAL, TENN, FLEECE

        for i in range(2):
            if self.odds["wirehair"] > 0 and (randint(1, round(self.odds["wirehair"]/2)) == 1 or self.odds["wirehair"] == 1):
                self.wirehair[i] = "Wh"
            if self.odds["laperm"] > 0 and (randint(1, round(self.odds["laperm"]/2)) == 1 or self.odds["laperm"] == 1):
                self.laperm[i] = "Lp"
            if self.odds["cornish"] > 0 and (randint(1, round(self.odds["cornish"]/2)) == 1 or self.odds["cornish"] == 1):
                self.cornish[i] = "r"
            if self.odds["urals"] > 0 and (randint(1, round(self.odds["urals"]/2)) == 1 or self.odds["urals"] == 1):
                self.urals[i] = "ru"
            if self.odds["tenn"] > 0 and (randint(1, round(self.odds["tenn"]/2)) == 1 or self.odds["tenn"] == 1):
                self.tenn[i] = "tr"
            if self.odds["fleece"] > 0 and (randint(1, round(self.odds["fleece"]/2)) == 1 or self.odds["fleece"] == 1):
                self.fleece[i] = "fc"


        #SELKIRK/DEVON/HAIRLESS

            if self.odds["canadian hairless"] > 0 and (randint(1, round(self.odds["canadian hairless"]/2)) == 1 or self.odds["canadian hairless"] == 1) and not self.ban_genes:
                self.sedesp[i] = "hr"
            elif self.odds["devon"] > 0 and (randint(1, round(self.odds["devon"]/2)) == 1 or self.odds["devon"] == 1):
                self.sedesp[i] = "re"
            elif self.odds["selkirk"] > 0 and (randint(1, round(self.odds["selkirk"]/2)) == 1 or self.odds["selkirk"] == 1):
                self.sedesp[i] = "Se"


        #ruhr + ruhrmod + lykoi
            if self.odds["russian hairless"] > 0 and (randint(1, round(self.odds["russian hairless"]/2)) == 1 or self.odds["russian hairless"] == 1) and not self.ban_genes:
                self.ruhr[i] = "Hrbd"
            if self.odds["lykoi"] > 0 and (randint(1, round(self.odds["lykoi"]/2)) == 1 or self.odds["lykoi"] == 1) and not self.ban_genes:
                self.lykoi[i] = "ly"
        
        a = randint(1, 4)

        if a == 1:
            self.ruhrmod = ["hi", "hi"]
        elif a == 4:
            self.ruhrmod = ["ha", "ha"]
        else:
            self.ruhrmod = ["hi", "ha"]

        # pinkdilute + dilutemd

        for i in range(2):
            if self.odds["pink-eyed dilute"] > 0 and (randint(1, round(self.odds["pink-eyed dilute"]/2)) == 1 or self.odds["pink-eyed dilute"] == 1) and not self.ban_genes:
                self.pinkdilute[i] = "dp"
            if self.odds["dilute modifier"] > 0 and (randint(1, round(self.odds["dilute modifier"]/2)) == 1 or self.odds["dilute modifier"] == 1):
                self.dilutemd[i] = "Dm"

        # ext

            if self.odds["grizzle"] > 0 and (randint(1, round(self.odds["grizzle"]/2)) == 1 or self.odds["grizzle"] == 1):
                self.ext[i] = "Eg"
            elif self.odds["carnelian"] > 0 and (randint(1, round(self.odds["carnelian"]/2)) == 1 or self.odds["carnelian"] == 1):
                self.ext[i] = "ec"
            elif self.odds["russet"] > 0 and (randint(1, round(self.odds["russet"]/2)) == 1 or self.odds["russet"] == 1):
                self.ext[i] = "er"
            elif self.odds["amber"] > 0 and (randint(1, round(self.odds["amber"]/2)) == 1 or self.odds["amber"] == 1):
                self.ext[i] = "ea"

        #sunshine

            if self.odds["sunshine"] > 0 and (randint(1, round(self.odds["sunshine"]/2)) == 1 or self.odds["sunshine"] == 1):
                self.corin[i] = "sh" #sunSHine
            elif self.odds["extreme sunshine"] > 0 and (randint(1, round(self.odds["extreme sunshine"]/2)) == 1 or self.odds["extreme sunshine"] == 1):
                self.corin[i] = "sg" #Siberian Gold / extreme sunshine
            elif self.odds["copper"] > 0 and (randint(1, round(self.odds["copper"]/2)) == 1 or self.odds["copper"] == 1):
                self.corin[i] = "fg" #Flaxen Gold
            else:
                self.corin[i] = "N" #No

        # karp + bleach + ghosting + satin + glitter

            if self.odds["karpati"] > 0 and (randint(1, round(self.odds["karpati"]/2)) == 1 or self.odds["karpati"] == 1):
                self.karp[i] = "K"
            if self.odds["bleaching"] > 0 and (randint(1, round(self.odds["bleaching"]/2)) == 1 or self.odds["bleaching"] == 1):
                self.bleach[i] = "lb"
            if self.odds["ghosting"] > 0 and (randint(1, round(self.odds["ghosting"]/2)) == 1 or self.odds["ghosting"] == 1):
                self.ghosting[i] = "Gh"
            if self.odds["satin"] > 0 and (randint(1, round(self.odds["satin"]/2)) == 1 or self.odds["satin"] == 1):
                self.satin[i] = "st"
            if self.odds["glitter"] > 0 and (randint(1, round(self.odds["glitter"]/2)) == 1 or self.odds["glitter"] == 1):
                self.glitter[i] = "gl"

        # curl + fold

            if self.odds["curl"] > 0 and (randint(1, round(self.odds["curl"]/2)) == 1 or self.odds["curl"] == 1):
                self.curl[i] = "Cu"

        if self.odds["fold"] > 0 and (randint(1, round(self.odds["fold"]/2)) == 1 or self.odds["fold"] == 1) and not self.ban_genes:
            self.fold[0] = "Fd"

        #  manx + kab + toybob + jbob + kub + ring

        if self.odds["american bobtail"] > 0 and (randint(1, round(self.odds["american bobtail"]/2)) == 1 or self.odds["american bobtail"] == 1):
            self.manx = ["Ab", "ab"]
        elif self.odds["manx"] > 0 and (randint(1, round(self.odds["manx"]/2)) == 1 or self.odds["manx"] == 1) and not self.ban_genes:
            self.manx = ["M", "m"]
        
        for i in range(2):
            if self.odds["karelian bobtail"] > 0 and (randint(1, round(self.odds["karelian bobtail"]/2)) == 1 or self.odds["karelian bobtail"] == 1):
                self.kab[i] = "kab"
            if self.odds["toybob"] > 0 and (randint(1, round(self.odds["toybob"]/2)) == 1 or self.odds["toybob"] == 1):
                self.toybob[i] = "Tb"
            if self.odds["kurilian bobtail"] > 0 and (randint(1, round(self.odds["kurilian bobtail"]/2)) == 1 or self.odds["kurilian bobtail"] == 1):
                self.kub[i] = "Kub"
            if self.odds["japanese bobtail"] > 0 and (randint(1, round(self.odds["japanese bobtail"]/2)) == 1 or self.odds["japanese bobtail"] == 1):
                self.jbob[i] = "jb"
            if self.odds["ringtail"] > 0 and (randint(1, round(self.odds["ringtail"]/2)) == 1 or self.odds["ringtail"] == 1):
                self.ring[i] = "rt"
        
        # munch + poly + altai

        if self.odds["munchkin"] > 0 and (randint(1, round(self.odds["munchkin"]/2)) == 1 or self.odds["munchkin"] == 1) and not self.ban_genes:
            self.munch[0] = "Mk"

        for i in range(2):
            if self.odds["polydactyl"] > 0 and (randint(1, round(self.odds["polydactyl"]/2)) == 1 or self.odds["polydactyl"] == 1):
                self.poly[i] = "Pd"
        
        if self.odds["DBE"] > 0 and (randint(1, round((self.odds["DBE"] ** 2)/2)) == 1 or self.odds["DBE"] == 1) and not self.ban_genes:
            self.pax3 = ['DBEalt', choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])]
        elif self.odds["DBE"] > 0 and (randint(1, round(self.odds["DBE"]/2)) == 1 or self.odds["DBE"] == 1) and not self.ban_genes:
            self.pax3[0] = choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])

        self.wideband = ''
        self.rufousing = ''
        self.spotted = ''
        self.tickgenes = ''
        self.bengal = ''
        self.sokoke = ''

        widegenes = ["0", "0", "1", "1", "1", "2", "2"]
        genesspot = ["2", "1", "0"]

        for i in range(0, 8):
            self.wideband += choice(widegenes)
            self.wbsum += int(self.wideband[i])

        for i in range(0, 4):
            self.rufousing += choice(genesspot)
            self.rufsum += int(self.rufousing[i])

        for i in range(0, 4):
            self.spotted += choice(genesspot)
            self.spotsum += int(self.spotted[i])

        genesmild = ["2", "2", "1", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0"]

        for i in range(0, 4):
            self.tickgenes += choice(genesmild)
            self.ticksum += int(self.tickgenes[i])

        for i in range(0, 4):
            self.bengal += choice(genesmild)
            self.bengsum += int(self.bengal[i])

        sokgenes = ["2", "2", "1", "1", "1", "0", "0", "0", "0"]

        for i in range(0, 4):
            self.sokoke += choice(sokgenes)
            self.soksum += int(self.sokoke[i])

        self.GeneSort()

        self.PolyEval()

        if randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()

        self.EyeColourFinder()

    def BreedGenerator(self, special=None):
        if self.chimera:
            self.chimerageno.Generator()

        common_breeds = [
            "Abyssinian", "American Burmese/Bombay", "American Curl", "American Shorthair", "Asian/Burmese",
            "Bengal", "Birman", "British", "Chartreux", "Cornish Rex", "Devon Rex", "Egyptian Mau",
            "Havana", "Japanese Bobtail", "Korat", "LaPerm", "Lykoi", "Maine Coon", "Manx", "Norwegian Forest cat",
            "Ocicat", "Oriental/Siamese", "Persian/Exotic", "Ragdoll", "Russian", "Selkirk Rex", "Siberian",
            "Singapura", "Sphynx", "Tonkinese", "Turkish"
        ]
        medium_breeds = [
            "American Bobtail", "Australian Mist", "Bambino", "Chausie", "Donskoy", "European Shorthair", "German Rex",
            "Highlander", "Khao Manee", "Kurilian Bobtail", "Mandalay/Burmese", "Munchkin", "Peterbald", "Pixie-Bob",
            "Ragamuffin", "Savannah", "Snowshoe", "Sokoke", "Thai", "Toybob", "Toyger"
        ]
        rare_breeds = [
            "Aphrodite", "Arabian Mau", "Brazilian Shorthair", "Cheetoh", "Ceylon", "Clippercat", "Foldex", "Gaelic Fold",
            "German Longhair", "Kanaani", "Karelian Bobtail", "Kinkalow", "Lambkin", "Lin-Qing Lion cat", "Mekong Bobtail",
            "Napoleon", "New Zealand", "Serengeti", "Skookum", "Tennessee Rex", "Ural Rex"
        ]

        selected_breed = choice(choice([rare_breeds, medium_breeds, medium_breeds, medium_breeds, medium_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds]))

        if self.ban_genes:
            while selected_breed in ["Lykoi", "Manx", "Sphynx", "Bambino", "Donskoy", "Munchkin", "Peterbald", "Foldex", "Gaelic Fold",
            "Kinkalow", "Lambkin", "Napoleon", "Skookum"]:
                selected_breed = choice(choice([rare_breeds, medium_breeds, medium_breeds, medium_breeds, medium_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds, common_breeds]))

        gen = breed_functions["generator"][selected_breed]

        self = gen(self, special)

        self.GeneSort()

        if self.body_value == 0:
            self.body_value = randint(self.body_indexes[2]+1, self.body_indexes[3])
        if self.height_value == 0:
            self.height_value = randint(self.height_indexes[3]+1, self.height_indexes[4])

        if self.odds['somatic_mutation'] > 0 and randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()

        self.PolyEval()
        self.EyeColourFinder()

    def KitGenerator(self, par1, par2=None, par3=None):
        try:
            par2 = par2.genotype
        except:
            par2 = par2
        if not par2:
            print("No second parent genotype given")
            par2 = Genotype(self.odds, self.ban_genes, 'no chimeras')
        if not par1:
            print("No first parent genotype given")
            par1 = Genotype(self.odds, self.ban_genes, 'no chimeras')

        threepars = False
        try:
            par3 = par3.genotype
        except:
            par3 = par3
            if par2 == par3:
                par3 = None


        for breed in par1.breeds:
            if par1.breeds[breed] >= 0.1:
                self.breeds[breed] = par1.breeds[breed] / 2
        for breed in par2.breeds:
            if par2.breeds[breed] >= 0.1:
                if self.breeds.get(breed, False):
                    self.breeds[breed] += par2.breeds[breed] / 2
                else:
                    self.breeds[breed] = par2.breeds[breed] / 2

        self.KitEyes(par1, par2)

        if self.chimera:
            if isinstance(par3, Genotype) and random() < 0.33:
                self.chimerageno.KitGenerator(par1, par3)
                threepars = True
            else:
                self.chimerageno.KitGenerator(par1, par2)
    
        if randint(1, 5) == 1:
            self.whitegrade = par1.whitegrade
        elif randint(1, 5) == 1:
            self.whitegrade = par2.whitegrade

        if self.odds["vitiligo"] <= 0:
            a = 0
        elif (par1.vitiligo and par2.vitiligo):
            a = randint(1, round((self.odds["vitiligo"]/4)))
        elif(par1.vitiligo or par2.vitiligo):
            a = randint(1, round((self.odds['vitiligo']/2)))
        else:
            a = randint(1, self.odds['vitiligo'])

        if(a == 1):
            self.vitiligo = True    

        if self.odds['pseudo_merle'] > 0 and randint(1, self.odds['pseudo_merle'])==1:
            self.pseudomerle = True


        self.furLength = [choice(par1.furLength), choice(par2.furLength)]
        
        self.eumelanin = [choice(par1.eumelanin), choice(par2.eumelanin)]

        #

        # SEXGENE

        #

        egglist1 = []
        egglist2 = []
        spermlist1 = []
        spermlist2 = []
        self.sexgene = []

        # deciding eggs and sperm
        if randint(1, self.odds['XXX/XXY']) == 1:
            egg1 = choice(["XX", "null"])
        else:
            egg1 = "X"
        if randint(1, self.odds['XXX/XXY']) == 1:
            egg2 = choice(["XX", "null"])
        else:
            egg2 = "X"
        if randint(1, self.odds['XXX/XXY']) == 1:
            sperm1 = choice(["XX", "XY", "YY", "null"])
        else:
            sperm1 = choice(["X", "Y"])
        if randint(1, self.odds['XXX/XXY']) == 1:
            sperm2 = choice(["XX", "XY", "YY", "null"])
        else:
            sperm2 = choice(["X", "Y"])

        while sperm1 == "Y" and sperm2 == "Y":
            sperm1 = choice(["X", "Y"])
            sperm2 = choice(["X", "Y"])
        while sperm1 == "Y" and (sperm2 == "YY" or sperm2 == "null"):
            sperm1 = choice(["X", "Y"])
            sperm2 = choice(["XX", "XY", "YY", "null"])
        while (sperm1 == "YY" or sperm1 == "null") and sperm2 == "Y":
            sperm1 = choice(["XX", "XY", "YY", "null"])
            sperm2 = choice(["X", "Y"])
        while (sperm1 == "YY" or sperm1 == "null") and (sperm2 == "YY" or sperm2 == "null"):
            sperm1 = choice(["XX", "XY", "YY", "null"])
            sperm2 = choice(["XX", "XY", "YY", "null"])

        while egg1 == "null" and egg2 == "null":
            egg1 = choice(["XX", "null"])
            egg2 = choice(["XX", "null"])

        while sperm1 == "Y" and egg1 == "null":
            sperm1 = choice(["X", "Y"])
            egg1 = choice(["XX", "null"])
            while sperm1 == "Y" and sperm2 == "Y":
                sperm1 = choice(["X", "Y"])
                sperm2 = choice(["X", "Y"])
            while sperm1 == "Y" and (sperm2 == "YY" or sperm2 == "null"):
                sperm1 = choice(["X", "Y"])
                sperm2 = choice(["XX", "XY", "YY", "null"])
            while (sperm1 == "YY" or sperm1 == "null") and sperm2 == "Y":
                sperm1 = choice(["XX", "XY", "YY", "null"])
                sperm2 = choice(["X", "Y"])
            while (sperm1 == "YY" or sperm1 == "null") and (sperm2 == "YY" or sperm2 == "null"):
                sperm1 = choice(["XX", "XY", "YY", "null"])
                sperm2 = choice(["XX", "XY", "YY", "null"])
            while egg1 == "null" and egg2 == "null":
                egg1 = choice(["XX", "null"])
                egg2 = choice(["XX", "null"])
        while (sperm1 == "YY" or sperm1 == "null") and egg1 == "null":
            sperm1 = choice(["XX", "XY", "YY", "null"])
            egg1 = choice(["XX", "null"])
            while sperm1 == "Y" and sperm2 == "Y":
                sperm1 = choice(["X", "Y"])
                sperm2 = choice(["X", "Y"])
            while sperm1 == "Y" and (sperm2 == "YY" or sperm2 == "null"):
                sperm1 = choice(["X", "Y"])
                sperm2 = choice(["XX", "XY", "YY", "null"])
            while (sperm1 == "YY" or sperm1 == "null") and sperm2 == "Y":
                sperm1 = choice(["XX", "XY", "YY", "null"])
                sperm2 = choice(["X", "Y"])
            while (sperm1 == "YY" or sperm1 == "null") and (sperm2 == "YY" or sperm2 == "null"):
                sperm1 = choice(["XX", "XY", "YY", "null"])
                sperm2 = choice(["XX", "XY", "YY", "null"])
            while egg1 == "null" and egg2 == "null":
                egg1 = choice(["XX", "null"])
                egg2 = choice(["XX", "null"])
        while sperm1 == "null" and egg1 == "null":
            sperm1 = choice(["XX", "XY", "YY", "null"])
            egg1 = choice(["XX", "null"])
            while (sperm1 == "YY" or sperm1 == "null") and egg1 == "null":
                sperm1 = choice(["XX", "XY", "YY", "null"])
                egg1 = choice(["XX", "null"])
            while sperm1 == "Y" and sperm2 == "Y":
                sperm1 = choice(["X", "Y"])
                sperm2 = choice(["X", "Y"])
            while sperm1 == "Y" and (sperm2 == "YY" or sperm2 == "null"):
                sperm1 = choice(["X", "Y"])
                sperm2 = choice(["XX", "XY", "YY", "null"])
            while (sperm1 == "YY" or sperm1 == "null") and sperm2 == "Y":
                sperm1 = choice(["XX", "XY", "YY", "null"])
                sperm2 = choice(["X", "Y"])
            while (sperm1 == "YY" or sperm1 == "null") and (sperm2 == "YY" or sperm2 == "null"):
                sperm1 = choice(["XX", "XY", "YY", "null"])
                sperm2 = choice(["XX", "XY", "YY", "null"])
            while egg1 == "null" and egg2 == "null":
                egg1 = choice(["XX", "null"])
                egg2 = choice(["XX", "null"])

        # setting inheritance
        if "Y" in par1.sexgene and "Y" in par2.sexgene:
            # par1
            if sperm1 == "X":
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist1.append(par1.sexgene[0])

            elif sperm1 == "XX":
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist1.append(par1.sexgene[0])

                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist1.append(par1.sexgene[0])

            elif sperm1 == "XY":
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist1.append(par1.sexgene[0])
                spermlist1.append("Y")

            elif sperm1 == "Y":
                spermlist1.append("Y")

            elif sperm1 == "YY":
                spermlist1.append("Y")
                spermlist1.append("Y")

            # par2
            if sperm2 == "X":
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])

            elif sperm2 == "XX":
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])

                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])

            elif sperm2 == "XY":
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])
                spermlist2.append("Y")

            elif sperm2 == "Y":
                spermlist2.append("Y")

            elif sperm2 == "YY":
                spermlist2.append("Y")
                spermlist2.append("Y")

            # getting rid of Y and YY cats
            if (sperm1 == "Y" or sperm1 == "YY") and sperm2 == "null":
                spermlist1 = []
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist1.append(par1.sexgene[0])
                if sperm1 == "YY":
                    spermlist1.append("Y")

            if sperm1 == "null" and (sperm2 == "Y" or sperm2 == "YY"):
                spermlist2 = []
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])
                if sperm2 == "YY":
                    spermlist2.append("Y")

            if (sperm1 == "Y" or sperm1 == "YY") and (sperm2 == "Y" or sperm2 == "YY"):
                spermlist1 = []
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist1.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist1.append(par1.sexgene[0])
                if sperm1 == "YY":
                    spermlist1.append("Y")

        elif "Y" not in par1.sexgene and "Y" not in par2.sexgene:
            # par1
            if "X" in egg1:
                egglist1.append(choice(par1.sexgene))
                if egg1 == "XX":
                    egglist1.append(choice(par1.sexgene))

            # par2
            if "X" in egg2:
                egglist2.append(choice(par2.sexgene))
                if egg2 == "XX":
                    egglist2.append(choice(par2.sexgene))

        elif "Y" not in par1.sexgene:
            # par1
            if "X" in egg1:
                egglist1.append(choice(par1.sexgene))
                if egg1 == "XX":
                    egglist1.append(choice(par1.sexgene))

            # par2
            if sperm2 == "X":
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])

            elif sperm2 == "XX":
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])

                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])

            elif sperm2 == "XY":
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])
                spermlist2.append("Y")

            elif sperm2 == "Y":
                spermlist2.append("Y")

            elif sperm2 == "YY":
                spermlist2.append("Y")
                spermlist2.append("Y")

            # getting rid of Y and YY cats
            if egg1 == "null" and (sperm2 == "Y" or sperm2 == "YY"):
                spermlist2 = []
                if len(par2.sexgene) == 3 and par2.sexgene[1] != "Y":
                    spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                elif len(par2.sexgene) == 4:
                    if par2.sexgene[2] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1]]))
                    elif par2.sexgene[3] == "Y":
                        spermlist2.append(choice([par2.sexgene[0], par2.sexgene[1], par2.sexgene[2]]))
                else:
                    spermlist2.append(par2.sexgene[0])
                if sperm2 == "YY":
                    spermlist2.append("Y")

        else:
            # par2
            if "X" in egg1:
                egglist1.append(choice(par2.sexgene))
                if egg1 == "XX":
                    egglist1.append(choice(par2.sexgene))

            # par1
            if sperm2 == "X":
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist2.append(par1.sexgene[0])

            elif sperm2 == "XX":
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist2.append(par1.sexgene[0])

                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist2.append(par1.sexgene[0])

            elif sperm2 == "XY":
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist2.append(par1.sexgene[0])
                spermlist2.append("Y")

            elif sperm2 == "Y":
                spermlist2.append("Y")

            elif sperm2 == "YY":
                spermlist2.append("Y")
                spermlist2.append("Y")

            # getting rid of Y and YY cats
            if egg1 == "null" and (sperm2 == "Y" or sperm2 == "YY"):
                spermlist2 = []
                if len(par1.sexgene) == 3 and par1.sexgene[1] != "Y":
                    spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                elif len(par1.sexgene) == 4:
                    if par1.sexgene[2] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1]]))
                    elif par1.sexgene[3] == "Y":
                        spermlist2.append(choice([par1.sexgene[0], par1.sexgene[1], par1.sexgene[2]]))
                else:
                    spermlist2.append(par1.sexgene[0])
                if sperm2 == "YY":
                    spermlist2.append("Y")

        # setting sexgene
        if "Y" in par1.sexgene and "Y" in par2.sexgene:
            for gene in spermlist1:
                self.sexgene.append(str(gene))
            for gene in spermlist2:
                self.sexgene.append(str(gene))
        elif "Y" not in par1.sexgene and "Y" not in par2.sexgene:
            for gene in egglist1:
                self.sexgene.append(str(gene))
            for gene in egglist2:
                self.sexgene.append(str(gene))
        else:
            for gene in egglist1:
                self.sexgene.append(str(gene))
            for gene in spermlist2:
                self.sexgene.append(str(gene))

        for i in range(1, 20):
            if "" in self.sexgene:
                self.sexgene.remove("")
            if "null" in self.sexgene:
                self.sexgene.remove("null")
            if "n" in self.sexgene:
                self.sexgene.remove("n")
            if "u" in self.sexgene:
                self.sexgene.remove("u")
            if "l" in self.sexgene:
                self.sexgene.remove("l")

        #

        # END SEXGENE

        #

        if 'O' in self.sexgene:
            if(par1.brindledbi and random() < 0.05):
                self.brindledbi = True
            elif(par2.brindledbi and random() < 0.05):
                self.brindledbi = True
            elif self.odds['brindled_bicolour'] > 0 and randint(1, self.odds['brindled_bicolour'])==1:
                self.brindledbi = True
        
        if(par1.specialred and random() < 0.1):
            self.specialred = par1.specialred
        elif(par2.specialred and random() < 0.1):
            self.specialred = par2.specialred
        elif(random() < 0.05):
            self.specialred = choice(['cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'blue-red', 'blue-tipped', 'blue-tipped', 'blue-tipped', 'cinnamon'])

        self.dilute = [choice(par1.dilute), choice(par2.dilute)]
        self.white = [choice(par1.white), choice(par2.white)]
        self.pointgene = [choice(par1.pointgene), choice(par2.pointgene)]

        self.silver = [choice(par1.silver), choice(par2.silver)]
        self.agouti = [choice(par1.agouti), choice(par2.agouti)]
        self.mack = [choice(par1.mack), choice(par2.mack)]
        self.ticked = [choice(par1.ticked), choice(par2.ticked)]

        if self.ticked[0] != self.ticked[1]:
            if(par1.breakthrough and random() < 0.25):
                self.breakthrough = par1.breakthrough
            elif(par2.breakthrough and random() < 0.25):
                self.breakthrough = par2.breakthrough
            elif self.odds["breakthrough"] > 0 and randint(1, self.odds["breakthrough"]) == 1:
                self.breakthrough = True

        self.wirehair = [choice(par1.wirehair), choice(par2.wirehair)]
        self.laperm = [choice(par1.laperm), choice(par2.laperm)]
        self.cornish = [choice(par1.cornish), choice(par2.cornish)]
        self.urals = [choice(par1.urals), choice(par2.urals)]
        self.tenn = [choice(par1.tenn), choice(par2.tenn)]
        self.fleece = [choice(par1.fleece), choice(par2.fleece)]
        self.sedesp = [choice(par1.sedesp), choice(par2.sedesp)]
        self.ruhr = [choice(par1.ruhr), choice(par2.ruhr)]
        self.ruhrmod = [choice(par1.ruhrmod), choice(par2.ruhrmod)]

        if(self.ruhrmod[0] == "ha"):
            x = self.ruhrmod[1]
            self.ruhrmod[1] = self.ruhrmod[0]
            self.ruhrmod[0] = x

        self.lykoi = [choice(par1.lykoi), choice(par2.lykoi)]

        self.pinkdilute = [choice(par1.pinkdilute), choice(par2.pinkdilute)]
        self.dilutemd = [choice(par1.dilutemd), choice(par2.dilutemd)]
        self.ext = [choice(par1.ext), choice(par2.ext)]
        self.corin = [choice(par1.corin), choice(par2.corin)]

        self.karp = [choice(par1.karp), choice(par2.karp)]
        self.bleach = [choice(par1.bleach), choice(par2.bleach)]
        self.ghosting = [choice(par1.ghosting), choice(par2.ghosting)]
        self.satin = [choice(par1.satin), choice(par2.satin)]
        self.glitter = [choice(par1.glitter), choice(par2.glitter)]

        self.curl = [choice(par1.curl), choice(par2.curl)]
        self.fold = [choice(par1.fold), choice(par2.fold)]
        
        self.manx = [choice(par1.manx), choice(par2.manx)]
        self.kab = [choice(par1.kab), choice(par2.kab)]
        self.toybob = [choice(par1.toybob), choice(par2.toybob)]
        self.jbob = [choice(par1.jbob), choice(par2.jbob)]
        self.kub = [choice(par1.kub), choice(par2.kub)]
        self.ring = [choice(par1.ring), choice(par2.ring)]
        self.munch = [choice(par1.munch), choice(par2.munch)]
        self.poly = [choice(par1.poly), choice(par2.poly)]
        self.pax3 = [choice(par1.pax3), choice(par2.pax3)]

        if random() < 0.25:
            self.saturation = par1.saturation
        elif random() < 0.25:
            self.saturation = par2.saturation


        self.wideband = ""

        for i in range(8):
            tempwb = 0
            if par1.wideband[i] == "2" or (par1.wideband[i] == "1" and randint(1, 2) == 1):
                tempwb = tempwb+1
                self.wbsum +=1
            if par2.wideband[i] == "2" or (par2.wideband[i] == "1" and randint(1, 2) == 1):
                tempwb = tempwb+1
                self.wbsum +=1
            self.wideband += str(tempwb)
        
        self.rufousing = ""
        for i in range(4):
            tempruf = 0
            if par1.rufousing[i] == "2" or (par1.rufousing[i] == "1" and randint(1, 2) == 1):
                tempruf = tempruf+1
                self.rufsum +=1
            if par2.rufousing[i] == "2" or (par2.rufousing[i] == "1" and randint(1, 2) == 1):
                tempruf = tempruf+1
                self.rufsum +=1
            self.rufousing += str(tempruf)
        
        self.bengal = ""
        for i in range(4):
            tempbeng = 0
            if par1.bengal[i] == "2" or (par1.bengal[i] == "1" and randint(1, 2) == 1):
                tempbeng = tempbeng+1
                self.bengsum +=1
            if par2.bengal[i] == "2" or (par2.bengal[i] == "1" and randint(1, 2) == 1):
                tempbeng = tempbeng+1
                self.bengsum +=1
            self.bengal += str(tempbeng)
        
        self.sokoke = ""
        for i in range(4):
            tempsok = 0
            if par1.sokoke[i] == "2" or (par1.sokoke[i] == "1" and randint(1, 2) == 1):
                tempsok = tempsok+1
                self.soksum +=1
            if par2.sokoke[i] == "2" or (par2.sokoke[i] == "1" and randint(1, 2) == 1):
                tempsok = tempsok+1
                self.soksum +=1
            self.sokoke += str(tempsok)
        
        self.spotted = ""
        for i in range(4):
            tempspot = 0
            if par1.spotted[i] == "2" or (par1.spotted[i] == "1" and randint(1, 2) == 1):
                tempspot = tempspot+1
                self.spotsum +=1
            if par2.spotted[i] == "2" or (par2.spotted[i] == "1" and randint(1, 2) == 1):
                tempspot = tempspot+1
                self.spotsum +=1
            self.spotted += str(tempspot)
        
        self.tickgenes = ""
        for i in range(4):
            temptick = 0
            if par1.tickgenes[i] == "2" or (par1.tickgenes[i] == "1" and randint(1, 2) == 1):
                temptick = temptick+1
                self.ticksum +=1
            if par2.tickgenes[i] == "2" or (par2.tickgenes[i] == "1" and randint(1, 2) == 1):
                temptick = temptick+1
                self.ticksum +=1
            self.tickgenes += str(temptick)

        wobble = randint(1, int(sum(self.body_ranges) / 25))
        self.body_value = randint(min(par1.body_value-wobble, par2.body_value-wobble), max(par1.body_value+wobble, par2.body_value+wobble))

        wobble = randint(1, int(sum(self.height_ranges) / 25))
        self.height_value = randint(min(par1.height_value-wobble, par2.height_value-wobble), max(par1.height_value+wobble, par2.height_value+wobble))

        if self.body_value < 1:
            self.body_value = 1
        if self.body_value > sum(self.body_ranges):
            self.body_value = sum(self.body_ranges)

        if self.height_value < 1:
            self.height_value = 1
        if self.height_value > sum(self.height_ranges):
            self.height_value = sum(self.height_ranges)

        self.GeneSort()

        if self.odds['random_mutation'] > 0 and randint(1, self.odds['random_mutation']) == 1:
            self.Mutate()

        if self.sexgene[0] == "Y":
            self.sexgene = random.choice([[par1.sexgene[0]], [par2.sexgene[0]]])
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's first sexgene is Y in genotype.py KitGenerator")
        if len(self.sexgene) > 4:
            self.sexgene = self.sexgene[:4]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's sexgene is longer than 4 in genotype.py KitGenerator")
        if not self.sexgene:
            self.sexgene = [par1.sexgene[0]]
            print("NOPE NOPE NOPE NOPE NOPE NOPE NOPE cat's sexgene is nothing in genotype.py KitGenerator")

        if self.odds['somatic_mutation'] > 0 and randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()

        self.PolyEval()
        self.EyeColourFinder()

        return threepars

    def KitEyes(self, par1, par2):
        multipliers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        multipliers2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
        def maths(par, m):
            m[par-1] += 10
            for i in range(0, par-1):
                m[i] += 10 / 5 ** (par-i-1)

            for i in range(par, 11):
                m[i] += 10 / 5 ** (i-par+1)
            return m

        multipliers = maths(par1.refraction, multipliers)
        multipliers = maths(par2.refraction, multipliers)
        multipliers = maths(math.floor((int(par1.refraction) + int(par2.refraction))/2), multipliers)
        multipliers2 = maths(par1.pigmentation, multipliers2)
        multipliers2 = maths(par2.pigmentation, multipliers2)
        multipliers2 = maths(math.floor((int(par1.pigmentation) + int(par2.pigmentation))/2), multipliers2)

        x = sum(multipliers)
        x2 = sum(multipliers2)

        def getindexes(m):
            inds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            for i in range(0, 11):
                for j in range(0, i+1):
                    inds[i] += m[j]

            return inds
        indexes = getindexes(multipliers)
        indexes2 = getindexes(multipliers2)

        num = random() * x
        self.refraction = next((n for n in range(len(indexes)) if num < indexes[n])) + 1
        num = random() * x2
        self.pigmentation = next((n for n in range(len(indexes2)) if num < indexes2[n])) + 1

    def GenerateBody(self):
        x = sum(self.body_ranges)

        self.body_value = randint(1, x)

        x = sum(self.height_ranges)

        self.height_value = randint(1, x)

    def VerifyBody(self, body_types):
        for i in range(7):
            if i == 0:
                if self.body_label == body_types[0] and self.body_value >= self.body_indexes[0]:
                    self.body_value = randint(0, self.body_indexes[0]-1)
            else:
                if self.body_label == body_types[i] and (self.body_value >= self.body_indexes[i] or self.body_value < self.body_indexes[i-1]):
                    self.body_value = randint(self.body_indexes[i-1], self.body_indexes[i]-1)

    def VerifyHeight(self):
        height = self.shoulder_height
        if self.munch[0] == 'Mk':
            height *= 1.5
        height = round(height, 2)

        if height <= 5.00:
            height = 0
            if self.height_value >= self.height_indexes[0]:
                self.height_value = randint(0, self.height_indexes[0]-1)
            return
        elif height >= 16.00:
            height = 0
            if self.height_value < self.height_indexes[8]:
                self.height_value = randint(self.height_indexes[8], self.height_indexes[9]-1)
            return
        elif 6.01 > height > 5.00:
            if self.height_indexes[0] > self.height_value or self.height_value >= self.height_indexes[1]:
                self.height_value = randint(self.height_indexes[0], self.height_indexes[1]-1)
            return
        elif 7.51 > height > 6.00:
            if self.height_indexes[1] > self.height_value or self.height_value >= self.height_indexes[2]:
                self.height_value = randint(self.height_indexes[1], self.height_indexes[2]-1)
            return
        elif 9 > height > 7.50:
            if self.height_indexes[2] > self.height_value or self.height_value >= self.height_indexes[3]:
                self.height_value = randint(self.height_indexes[2], self.height_indexes[3]-1)
            return
        elif 11.01 > height > 8.99:
            if self.height_indexes[3] > self.height_value or self.height_value >= self.height_indexes[4]:
                self.height_value = randint(self.height_indexes[3], self.height_indexes[4]-1)
            return
        elif 12.51 > height > 11.00:
            if self.height_indexes[4] > self.height_value or self.height_value >= self.height_indexes[5]:
                self.height_value = randint(self.height_indexes[4], self.height_indexes[5]-1)
            return
        elif 14.01 > height > 12.50:
            if self.height_indexes[5] > self.height_value or self.height_value >= self.height_indexes[6]:
                self.height_value = randint(self.height_indexes[5], self.height_indexes[6]-1)
            return
        elif 15.00 > height > 14.00:
            if self.height_indexes[6] > self.height_value or self.height_value >= self.height_indexes[7]:
                self.height_value = randint(self.height_indexes[6], self.height_indexes[7]-1)
            return
        elif 16.00 > height > 14.99:
            if self.height_indexes[7] > self.height_value or self.height_value >= self.height_indexes[8]:
                self.height_value = randint(self.height_indexes[7], self.height_indexes[8]-1)
            return

    def PolyEval(self):
        wbtypes = ["low", "medium", "high", "shaded", "chinchilla"]
        ruftypes = ["low", "medium", "rufoused"]

        self.wbsum = 0
        self.rufsum = 0
        self.bengsum = 0
        self.soksum = 0
        self.spotsum = 0
        self.ticksum = 0
        
        if len(self.wideband) < 8:
            while len(self.wideband) < 8:
                self.wideband += '1'
        if len(self.rufousing) < 4:
            while len(self.rufousing) < 4:
                self.rufousing += '1'
        if len(self.bengal) < 4:
            while len(self.bengal) < 4:
                self.bengal += '1'
        if len(self.sokoke) < 4:
            while len(self.sokoke) < 4:
                self.sokoke += '1'
        if len(self.spotted) < 4:
            while len(self.spotted) < 4:
                self.spotted += '1'
        if len(self.tickgenes) < 4:
            while len(self.tickgenes) < 4:
                self.tickgenes += '1'

        for i in self.wideband:
            self.wbsum += int(i)
        for i in self.rufousing:
            self.rufsum += int(i)
        for i in self.bengal:
            self.bengsum += int(i)
        for i in self.sokoke:
            self.soksum += int(i)
        for i in self.spotted:
            self.spotsum += int(i)
        for i in self.tickgenes:
            self.ticksum += int(i)
        
        if self.wbsum < 6:
            self.wbtype = wbtypes[0]
        elif self.wbsum < 10:
            self.wbtype = wbtypes[1]
        elif self.wbsum < 12: 
            self.wbtype = wbtypes[2]
        elif self.wbsum < 14: 
            self.wbtype = wbtypes[3]
        else: 
            self.wbtype = wbtypes[4]

        if self.rufsum < 3: 
            self.ruftype = ruftypes[0]
        elif self.rufsum < 6: 
            self.ruftype = ruftypes[1]
        else:
            self.ruftype = ruftypes[2]

        spottypes = ["fully striped", "slightly broken", "broken stripes", "mostly broken", "spotted"]

        if self.spotsum < 1: 
            self.spottype = spottypes[0]
        elif self.spotsum < 3:
            self.spottype = spottypes[1]
        elif self.spotsum < 6:
            self.spottype = spottypes[2]
        elif self.spotsum < 8: 
            self.spottype = spottypes[3]
        else:
            self.spottype = spottypes[4]
        
        ticktypes = ["full barring", "reduced barring", "agouti"]

        if self.ticksum < 4: 
            self.ticktype = ticktypes[0]
        elif self.ticksum < 6:
            self.ticktype = ticktypes[1]
        else:
            self.ticktype = ticktypes[2]

        bengtypes = ["normal markings", "mild bengal", "full bengal"]

        if self.bengsum < 4: 
            self.bengtype = bengtypes[0]
        elif self.bengsum < 6:
            self.bengtype = bengtypes[1]
        else:
            self.bengtype = bengtypes[2]

        soktypes = ["normal markings", "mild fading", "full sokoke"]

        if self.soksum < 4: 
            self.soktype = soktypes[0]
        elif self.soksum < 6:
            self.soktype = soktypes[1]
        else:
            self.soktype = soktypes[2]

        body_types = ['snub-nosed', 'cobby', 'semi-cobby', 'intermediate', 'semi-oriental', 'oriental', 'wedge-faced']
        height_types = ['teacup', 'tiny', 'small', 'below average', 'average', 'above average', 'large', 'massive', 'giant', 'goliath']

        if self.body_label != '':
            self.VerifyBody(body_types)
        else:
            index = next((n for n in range(7) if self.body_value <= self.body_indexes[n]))
            self.body_label = body_types[index]

        if self.shoulder_height > 0:
            self.VerifyHeight()
        index = next((n for n in range(10) if self.height_value <= self.height_indexes[n]))
        self.height_label = height_types[index]

        if self.shoulder_height > 0:
            return

        if index == 0:
            self.shoulder_height = 5.00
        elif index == 1:
            value = self.height_value - self.height_indexes[index-1]
            step = (6-5.01) / self.height_ranges[index]
            self.shoulder_height = 5.01 + value * (random() * step)
        elif index == 2:
            value = self.height_value - self.height_indexes[index-1]
            step = (7.5-6.01) / self.height_ranges[index]
            self.shoulder_height = 6.01 + value * (random() * step)
        elif index == 3:
            value = self.height_value - self.height_indexes[index-1]
            step = (8.99-7.51) / self.height_ranges[index]
            self.shoulder_height = 7.51 + value * (random() * step)
        elif index == 4:
            value = self.height_value - self.height_indexes[index-1]
            step = (11-9) / self.height_ranges[index]
            self.shoulder_height = 9 + value * (random() * step)
        elif index == 5:
            value = self.height_value - self.height_indexes[index-1]
            step = (12.5-11.01) / self.height_ranges[index]
            self.shoulder_height = 11.01 + value * (random() * step)
        elif index == 6:
            value = self.height_value - self.height_indexes[index-1]
            step = (14-12.51) / self.height_ranges[index]
            self.shoulder_height = 12.51 + value * (random() * step)
        elif index == 7:
            value = self.height_value - self.height_indexes[index-1]
            step = (14.99-14.01) / self.height_ranges[index]
            self.shoulder_height = 14.01 + value * (random() * step)
        elif index == 8:
            value = self.height_value - self.height_indexes[index-1]
            step = (15.99-15.00) / self.height_ranges[index]
            self.shoulder_height = 15.00 + value * (random() * step)
        elif index == 9:
            self.shoulder_height = 16.00

        if self.munch[0] == 'Mk':
            self.shoulder_height /= 1.5
        self.shoulder_height = round(self.shoulder_height, 2)

    def GeneSort(self):

        for gene in ["furLength", "dilute", 'silver', 'mack', 'ticked',
                     'wirehair', 'laperm', 'cornish', 'urals', 'tenn', 'fleece', 'ruhr', 'lykoi',
                     'pinkdilute', 'dilutemd', 'karp', 'bleach', 'ghosting', 'satin', 'glitter',
                     'curl', 'fold', 'kab', 'toybob', 'jbob', 'kub', 'ring', 'munch', 'poly']:
            if self[gene][0] != self[gene][1] and self[gene][0].islower():
                self[gene][0], self[gene][1] = self[gene][1], self[gene][0]

        if self.eumelanin[0] == "bl":
            self.eumelanin[0] = self.eumelanin[1]
            self.eumelanin[1] = "bl"
        elif self.eumelanin[0] == "b" and self.eumelanin[1] != "bl":
            self.eumelanin[0] = self.eumelanin[1]
            self.eumelanin[1] = "b"

        index = 0
        while index < len(self.sexgene):
            if self.sexgene[index] == "Y":
                self.sexgene[index] = "y"
            index += 1

        self.sexgene.sort()

        index = 0
        while index < len(self.sexgene):
            if self.sexgene[index] == "y":
                self.sexgene[index] = "Y"
            index += 1

        if self.white[0] == "wsal":
            self.white[0] = self.white[1]
            self.white[1] = "wsal"
        elif self.white[0] == "wg" and self.white[1] != "wsal":
            self.white[0] = self.white[1]
            self.white[1] = "wg"
        elif self.white[0] == "w" and self.white[1] != "wg" and self.white[1] != "wsal":
            self.white[0] = self.white[1]
            self.white[1] = "w"
        elif self.white[0] == "wt" and self.white[1] != "wg" and self.white[1] != "w" and self.white[1] != "wsal":
            self.white[0] = self.white[1]
            self.white[1] = "wt"
        elif self.white[1] == "W":
            self.white[1] = self.white[0]
            self.white[0] = "W"

        if self.pointgene[0] == "c":
            self.pointgene[0] = self.pointgene[1]
            self.pointgene[1] = "c"
        elif self.pointgene[0] == "cm" and self.pointgene[1] != "c":
            self.pointgene[0] = self.pointgene[1]
            self.pointgene[1] = "cm"
        elif self.pointgene[0] == "cs" and self.pointgene[1] != "c" and self.pointgene[1] != "cm":
            self.pointgene[0] = self.pointgene[1]
            self.pointgene[1] = "cs"
        elif self.pointgene[1] == "C":
            self.pointgene[1] = self.pointgene[0]
            self.pointgene[0] = "C"

        if self.agouti[0] == "a":
            self.agouti[0] = self.agouti[1]
            self.agouti[1] = "a"
        elif self.agouti[0] == "Apb" and self.agouti[1] != "a":
            self.agouti[0] = self.agouti[1]
            self.agouti[1] = "Apb"

        if self.sedesp[0] == "re":
            self.sedesp[0] = self.sedesp[1]
            self.sedesp[1] = "re"
        elif self.sedesp[0] == "hr" and self.sedesp[1] != "re":
            self.sedesp[0] = self.sedesp[1]
            self.sedesp[1] = "hr"
        elif self.sedesp[1] == "Se":
            self.sedesp[1] = self.sedesp[0]
            self.sedesp[0] = "Se"

        if self.ext[0] == "ec":
            self.ext[0] = self.ext[1]
            self.ext[1] = "ec"
        elif self.ext[0] == "er" and self.ext[1] != "ec":
            self.ext[0] = self.ext[1]
            self.ext[1] = "er"
        elif self.ext[1] == "Eg":
            self.ext[1] = self.ext[0]
            self.ext[0] = "Eg"
        elif self.ext[1] == "E" and self.ext[0] != "Eg":
            self.ext[1] = self.ext[0]
            self.ext[0] = "E"

        if self.corin[0] == "sh":
            self.corin[0] = self.corin[1]
            self.corin[1] = "sh"
        elif self.corin[0] == "fg":
            self.corin[0] = self.corin[1]
            self.corin[1] = "fg"
        elif self.corin[0] == "sg":
            self.corin[0] = self.corin[1]
            self.corin[1] = "sg"

        if self.manx[1] == "M":
            self.manx[1] = self.manx[0]
            self.manx[0] = "M"
        elif self.manx[1] == "Ab":
            self.manx[1] = self.manx[0]
            self.manx[0] = "Ab"

        if self.pax3[0] == 'NoDBE':
            self.pax3[0] = self.pax3[1]
            self.pax3[1] = 'NoDBE'

    def EyeColourFinder(self):
        eyecolours = {
        "R1" : ["Citrine", "Golden Beryl", "Yellow", "Pale Golden", "Golden", "Amber", "Light Orange", "Orange", "Cinnabar", "Auburn", "Copper", "Ice Blue", "Pink"],
        "R2" : ["Pale Citrine", "Pale Yellow", "Lemon", "Deep Yellow", "Dull Golden", "Honey", "Pale Orange", "Burnt Orange", "Dark Orange", "Russet", "Dark Topaz", "Aquamarine", "Rose"],
        "R3" : ["Lemonade Yellow", "Straw Yellow", "Dandelion Yellow", "Banana Yellow", "Sunglow Yellow", "Copal", "Dull Orange", "Rust Orange", "Topaz", "Chocolate", "Burgundy", "Sky Blue", "Magenta"],
        "R4" : ["Light Celadon", "Pale Chartreuse", "Pear Green", "Brass Yellow", "Golden Green", "Butterscotch", "Dusty Orange", "Tawny", "Jasper", "Light Brown", "Earth", "Cyan", "Periwinkle"],
        "R5" : ["Light Jade", "Pale Lime", "Spring Bud", "Chartreuse", "Pale Hazel", "Yellow Hazel", "Golden Fluorite", "Beaver Brown", "Sienna", "Chestnut", "Umber", "Baby Blue", "Violet"],
        "R6" : ["Light Fluorite", "Mantis Green", "Spring Green", "Lime", "Green Tea", "Hazel", "Golden Brown", "Dark Copal", "Cinnamon", "Raw Umber", "Sepia", "Aqua", "Glass"],
        "R7" : ["Pale Emerald", "Apple Green", "Shamrock", "Lemon-Lime", "Peridot", "Antique Brass", "Dark Hazel", "Brown-Green", "Hazel Brown", "Bronze", "Bistre Brown", "Cerulean", "Moonstone"],
        "R8" : ["Malachite", "Olivine", "Pastel Green", "Bright Green", "Pistachio", "Dull Olive", "Murky Green", "Jungle Green", "Hemlock Green", "Thatch Green", "Muddy", "Ocean Blue", "Ice Blue"],
        "R9" : ["Pale Turquoise", "Mint", "Snake Green", "Dark Lime", "Fern Green", "Dull Green", "Dark Fern Green", "Olive", "Tumbleweed Green", "Bronze Olive", "Deep Bronze", "Teal", "Aquamarine"],
        "R10" : ["Turquoise", "Viridian", "Green Onion", "Leaf Green", "Green", "Sap Green", "Dark Leaf Green", "Forest Green", "Dark Peridot", "Seaweed Green", "Dark Olive", "Sapphire", "Sky Blue"],
        "R11" : ["Deep Turquoise", "Amazonite", "Pine Green", "Deep Leaf Green", "Jade", "Emerald", "Deep Green", "Deep Forest Green", "Dark Green", "Dark Moss Green", "Black Olive", "Azure", "Albino Azure"]
        }
        sectoralindex = randint(0, 74)
        het2index = randint(0, 99)
        blueindex = 1
        hetindex = 1
        dpnum = randint(1, 8)

        if not self.refraction:
            refgrade = choice([1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 11])
            piggrade = choice([1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 11])
            self.refraction = refgrade
            self.pigmentation = piggrade
        else:
            refgrade = self.refraction
            piggrade = self.pigmentation

        if self.dilute[0] == "d" or self.pointgene == ["cb", "cb"] or self.pointgene == ["cb", "c"] or self.pointgene == ["cb", "cm"]:
            if randint(1, 5) == 1:
                piggrade = piggrade - 1

        if (self.pinkdilute[0] == 'dp' and dpnum in [1, 2]) or self.pointgene == ["cb", "cs"]:
            piggrade = math.ceil(piggrade / 2)

        if piggrade == 0 or ((self.pointgene == ["cb", "cm"] or self.pointgene == ["cm", "cm"] or self.pointgene == ["cm", "c"]) and randint(1, 5) == 1):
            piggrade = 1

        if self.pinkdilute[0] == 'dp' and dpnum in [3, 4, 5, 6, 7]:
            piggrade = 1

        if self.pinkdilute[0] == 'dp':
            if refgrade == 11 and piggrade > 6:
                piggrade = 6
            elif refgrade in [9, 10] and piggrade > 7:
                piggrade = 7
            elif refgrade in [7, 8] and piggrade > 8:
                piggrade = 8
            elif refgrade in [1, 2, 3, 4, 5, 6] and piggrade > 9:
                piggrade = 9

        def RefTypeFind(x, piggrade):
            y = eyecolours['R' + str(x)][piggrade-1]

            return y
        
        def SecondaryRefTypeFind(x, piggrade):
            y = ""

            piggrade = "P" + str(piggrade)
            if piggrade == "P12":
                piggrade = "blue"
            elif piggrade == "P13":
                piggrade = "albino"
                    
            y += "R" + str(x) + " ; " + str(piggrade) + ""
            return y




        if self.white == ["w","w"] or self.white == ["w", "wg"] or self.white == ["wg", "wg"]:
            blueindex = randint(0, 99)
        elif self.white == ["ws","w"] or self.white == ["ws","wg"] or self.white == ["wt", "w"] or self.white == ["wt", "wg"]:
            blueindex = randint(0, 74)
        elif self.white == ["ws","ws"] or self.white == ["wt", "wt"] or self.white == ["ws", "wt"]:
            blueindex = randint(0, 24)
        elif self.pointgene == ["cb","cs"]:
            blueindex = randint(0, 7)
        elif self.white[0] == "W":
            blueindex = randint(0, 14)
            if randint(1, 4) == 1 and blueindex == 0:
                self.deaf = True
        if self.white == ["W","W"]:
            blueindex = randint(0, 2)
            if randint(1, 4) < 4 and blueindex == 0:
                self.deaf = True
        
        if self.pointgene[0] == "cs" or ((self.pointgene == ["cb","cm"] or self.pointgene == ["cm","cm"] or self.pointgene == ["cm","c"]) and randint(0, 4)==0):
            blueindex = 0


        if 'ws' not in self.white and 'wt' not in self.white:
            hetindex = randint(0, 74)
        elif self.white[0] in ['ws', 'wt'] and self.white[1] not in ['ws', 'wt']:
            hetindex = randint(0, 24)
        elif self.white[0] in ['ws', 'wt'] and self.white[1] in ['ws', 'wt']:
            hetindex = randint(0, 14)
        elif self.white[0] == "W":
            hetindex = randint(0, 9)
            if randint(1, 10) == 1 and hetindex == 0:
                self.deaf = True
        if self.white == ["W","W"]:
            hetindex = randint(0, 2)
            if randint(1, 8) == 1 and hetindex == 0:
                self.deaf = True

        if self.pax3[0] != 'NoDBE':
            if 'NoDBE' not in self.pax3:
                blueindex = 0
                if (self.pax3 == ['DBEalt', 'DBEalt'] and random() < 0.33) or self.pax3 != ['DBEalt', 'DBEalt']:
                    self.deaf = True
            elif 'DBEre' not in self.pax3 and random() >= 0.1:
                if random() < 0.33:
                    blueindex = 0
                else:
                    hetindex = 0
            elif 'DBEre' in self.pax3:
                blueindex = 0
                if random() < 0.33:
                    self.deaf = True

        if het2index == 0 and not ("c" in self.pointgene and self.pointgene[0] != "C") and blueindex != 0 and not (self.pointgene == ["C", "c"] and randint(1, 10) > 7):
            tempref = randint(1, 11)
            temppig = randint(1, 12)
            if randint(1, 2)==1:
                self.lefteye = RefTypeFind(tempref, temppig)
                self.righteye = RefTypeFind(refgrade, piggrade)

                self.lefteyetype = SecondaryRefTypeFind(tempref, temppig)
                self.righteyetype = SecondaryRefTypeFind(refgrade, piggrade)
            else:
                self.righteye = RefTypeFind(tempref, temppig)
                self.lefteye = RefTypeFind(refgrade, piggrade)

                self.lefteyetype = SecondaryRefTypeFind(refgrade, piggrade)
                self.righteyetype = SecondaryRefTypeFind(tempref, temppig)
        else:
            self.righteye = RefTypeFind(refgrade, piggrade)
            self.lefteye = RefTypeFind(refgrade, piggrade)

            self.lefteyetype = SecondaryRefTypeFind(refgrade, piggrade)
            self.righteyetype = SecondaryRefTypeFind(refgrade, piggrade)

            if(sectoralindex == 0):
                self.extraeye = 'sectoral' + str(randint(1, 6))
            a = [randint(1, 11), randint(1, 12)]
            if "c" in self.pointgene and self.pointgene[0] != "C" or (self.pointgene == ["C", "c"] and randint(1, 10) > 7):
                a[1] = 13
            self.extraeyecolour = RefTypeFind(a[0], a[1])
            self.extraeyetype = SecondaryRefTypeFind(a[0], a[1])


            if (self.pointgene == ["C", "c"] and randint(1, 10) > 7) or ("c" in self.pointgene and self.pointgene[0] != "C"):
                self.lefteye = RefTypeFind(refgrade, 13)
                self.righteye = RefTypeFind(refgrade, 13)

                self.lefteyetype = SecondaryRefTypeFind(refgrade, 13)
                self.righteyetype = SecondaryRefTypeFind(refgrade, 13)

                if het2index == 0:
                    tempref = randint(1, 11)
                    if randint(0, 1)==0:
                        self.lefteye = RefTypeFind(tempref, 13)
                        self.lefteyetype = SecondaryRefTypeFind(tempref, 13)
                    else:
                        self.righteye = RefTypeFind(tempref, 13)
                        self.righteyetype = SecondaryRefTypeFind(tempref, 13)
                elif self.extraeye:
                    self.extraeyecolour = RefTypeFind(a[0], 13)
                    self.extraeyetype = SecondaryRefTypeFind(a[0], 13)
            elif(blueindex == 0):
                self.lefteye = RefTypeFind(refgrade, 12)
                self.righteye = RefTypeFind(refgrade, 12)

                self.lefteyetype = SecondaryRefTypeFind(refgrade, 12)
                self.righteyetype = SecondaryRefTypeFind(refgrade, 12)

                if het2index == 0:
                    tempref = randint(1, 11)
                    if random() < 0.5:
                        self.lefteye = RefTypeFind(tempref, 12)
                        self.lefteyetype = SecondaryRefTypeFind(tempref, 12)
                    else:
                        self.righteye = RefTypeFind(tempref, 12)
                        self.righteyetype = SecondaryRefTypeFind(tempref, 12)
                elif self.extraeye:
                    self.extraeyecolour = RefTypeFind(a[0], 12)
                    self.extraeyetype = SecondaryRefTypeFind(a[0], 12)
            elif hetindex == 0:
                if random() < 0.5:
                    self.lefteye = RefTypeFind(refgrade, 12)
                    self.lefteyetype = SecondaryRefTypeFind(refgrade, 12)
                else:
                    self.righteye = RefTypeFind(refgrade, 12)
                    self.righteyetype = SecondaryRefTypeFind(refgrade, 12)

    def EyeColourName(self):

        eyecolours = {
        "R1" : ["Citrine", "Golden Beryl", "Yellow", "Pale Golden", "Golden", "Amber", "Light Orange", "Orange", "Cinnabar", "Auburn", "Copper", "Ice Blue", "Pink"],
        "R2" : ["Pale Citrine", "Pale Yellow", "Lemon", "Deep Yellow", "Dull Golden", "Honey", "Pale Orange", "Burnt Orange", "Dark Orange", "Russet", "Dark Topaz", "Aquamarine", "Rose"],
        "R3" : ["Lemonade Yellow", "Straw Yellow", "Dandelion Yellow", "Banana Yellow", "Sunglow Yellow", "Copal", "Dull Orange", "Rust Orange", "Topaz", "Chocolate", "Burgundy", "Sky Blue", "Magenta"],
        "R4" : ["Light Celadon", "Pale Chartreuse", "Pear Green", "Brass Yellow", "Golden Green", "Butterscotch", "Dusty Orange", "Tawny", "Jasper", "Light Brown", "Earth", "Cyan", "Periwinkle"],
        "R5" : ["Light Jade", "Pale Lime", "Spring Bud", "Chartreuse", "Pale Hazel", "Yellow Hazel", "Golden Fluorite", "Beaver Brown", "Sienna", "Chestnut", "Umber", "Baby Blue", "Violet"],
        "R6" : ["Light Fluorite", "Mantis Green", "Spring Green", "Lime", "Green Tea", "Hazel", "Golden Brown", "Dark Copal", "Cinnamon", "Raw Umber", "Sepia", "Aqua", "Glass"],
        "R7" : ["Pale Emerald", "Apple Green", "Shamrock", "Lemon-Lime", "Peridot", "Antique Brass", "Dark Hazel", "Brown-Green", "Hazel Brown", "Bronze", "Bistre Brown", "Cerulean", "Moonstone"],
        "R8" : ["Malachite", "Olivine", "Pastel Green", "Bright Green", "Pistachio", "Dull Olive", "Murky Green", "Jungle Green", "Hemlock Green", "Thatch Green", "Muddy", "Ocean Blue", "Ice Blue"],
        "R9" : ["Pale Turquoise", "Mint", "Snake Green", "Dark Lime", "Fern Green", "Dull Green", "Dark Fern Green", "Olive", "Tumbleweed Green", "Bronze Olive", "Deep Bronze", "Teal", "Aquamarine"],
        "R10" : ["Turquoise", "Viridian", "Green Onion", "Leaf Green", "Green", "Sap Green", "Dark Leaf Green", "Forest Green", "Dark Peridot", "Seaweed Green", "Dark Olive", "Sapphire", "Sky Blue"],
        "R11" : ["Deep Turquoise", "Amazonite", "Pine Green", "Deep Leaf Green", "Jade", "Emerald", "Deep Green", "Deep Forest Green", "Dark Green", "Dark Moss Green", "Black Olive", "Azure", "Albino Azure"]
        }

        def setup(eyestring):
            eye = eyestring.split(' ; ')
            ref = eye[0]
            pig = int(eye[1].replace("albino", '13').replace('blue', '12').replace('P', ''))
            return eyecolours[ref][pig-1]
        self.lefteye = setup(self.lefteyetype)
        self.righteye = setup(self.righteyetype)
        if self.extraeyecolour != '':
            self.extraeyecolour = setup(self.extraeyetype)

    def EyeConvert(self):
        refsum = 0
        pigsum = 0
        refgrade = 1
        piggrade = 1

        for i in self.refraction:
            refsum += int(i)
        for i in self.pigmentation:
            pigsum += int(i)

        if refsum == 0:
            refgrade = 1
        elif refsum <= 1:
            refgrade = 2
        elif refsum <= 3:
            refgrade = 3
        elif refsum <= 5:
            refgrade = 4
        elif refsum <= 7:
            refgrade = 5
        elif refsum <= 10:
            refgrade = 6
        elif refsum <= 12:
            refgrade = 7
        elif refsum <= 14:
            refgrade = 8
        elif refsum <= 16:
            refgrade = 9
        elif refsum < 18:
            refgrade = 10
        else:
            refgrade = 11

        if pigsum == 0:
            piggrade = 1
        elif pigsum <= 1:
            piggrade = 2
        elif pigsum <= 3:
            piggrade = 3
        elif pigsum <= 5:
            piggrade = 4
        elif pigsum <= 7:
            piggrade = 5
        elif pigsum <= 10:
            piggrade = 6
        elif pigsum <= 12:
            piggrade = 7
        elif pigsum <= 14:
            piggrade = 8
        elif pigsum <= 16:
            piggrade = 9
        elif pigsum < 18:
            piggrade = 10
        else:
            piggrade = 11

        self.refraction = refgrade
        self.pigmentation = piggrade

    def ShowGenes(self, filter=True):
        """
        TODO: add sectoral heterochromia
        """
        wht = str(self.white) + " (" + str(self.whitegrade) + ")"
        breakthroughstring = "breakthrough tabby"

        self.PolyEval()
        if self.specialred:
            self.Cat_Genes = [self.furLength, self.eumelanin, self.sexgene, self.specialred, self.dilute, wht,
                              self.pointgene, self.silver, self.agouti, self.mack, self.ticked]
        else:
            self.Cat_Genes = [self.furLength, self.eumelanin, self.sexgene, self.dilute, wht, self.pointgene,
                              self.silver, self.agouti, self.mack, self.ticked]
        if self.breakthrough:
            self.Cat_Genes.append(breakthroughstring)
        if self.breeds:
            self.Cat_Genes.append(self.breeds)
        self.Fur_Genes = [self.wirehair, self.laperm, self.cornish, self.urals, self.tenn, self.fleece, self.sedesp, self.ruhr, self.ruhrmod, self.lykoi]
        self.Other_Colour = [self.pinkdilute, self.dilutemd, self.ext, self.corin, self.karp, self.bleach, self.ghosting, self.satin, self.glitter]
        self.Body_Genes = [self.curl, self.fold, self.manx, self.manxtype, self.kab, self.toybob, self.jbob, self.kub, self.ring, self.munch, self.poly, self.pax3]
        self.Polygenes = ["Rufousing:", self.rufousing, self.ruftype, "Bengal:", self.bengal, self.bengtype, "Sokoke:", self.sokoke, self.soktype, "Spotted:", self.spotted, self.spottype, "Ticked:", self.tickgenes, self.ticktype]
        self.Polygenes2 = ["Wideband:", self.wideband, self.wbtype, "Refraction:", self.refraction, "Pigmentation:", self.pigmentation]

        return self.Cat_Genes, "Other Fur Genes:", self.Fur_Genes, "Other Color Genes:", self.Other_Colour, "Body Mutations:", self.Body_Genes, "Polygenes:", self.Polygenes, self.Polygenes2
    
    def Mutate(self):
        print("MUTATION!")
        wheremutation = ["body", "furtype", "furtype", "othercoat", "othercoat", "othercoat", "maincoat", "maincoat", "maincoat", "maincoat", "maincoat", "maincoat"]
        where = choice(wheremutation)

        if where == 'body':
            self.Bodymutation()
        elif where == 'furtype':
            self.FurTypemutation()
        elif where == 'othercoat':
            self.OtherCoatmutation()
        else:
            self.MainCoatmutation()

    def Bodymutation(self):
        whichgene = ["curl", "fold", "manx", "karel", "toybob", "japanese", "kuril", "ringtail", "munchkin",
                     "polydactyl", "polydactyl", "polydactyl", "polydactyl"]

        if self.ban_genes:
            for i in range(1, 20):
                whichgene.remove("fold")
                whichgene.remove("munchkin")

        which = choice(whichgene)

        if which == "curl":
            print(self.curl)
            # Gains the gene
            if self.curl[0] == 'cu':
                self.curl[0] = 'Cu'
            elif self.curl[1] == 'cu':
                self.curl[1] = 'Cu'
            # Loses the gene
            elif self.curl[1] == 'Cu':
                self.curl[1] = 'cu'
            elif self.curl[0] == 'Cu':
                self.curl[0] = 'cu'
            else:
                self.Mutate()
            print(self.curl)
        elif which == 'fold':
            print(self.fold)
            # Gains the gene
            if self.fold[0] == 'fd':
                self.fold[0] = 'Fd'
            elif self.fold[1] == 'fd':
                self.fold[1] = 'Fd'
            # Loses the gene
            elif self.fold[1] == 'Fd':
                self.fold[1] = 'fd'
            elif self.fold[0] == 'Fd':
                self.fold[0] = 'fd'
            else:
                self.Mutate()
            print(self.fold)
        elif which == 'manx':
            print(self.manx)
            if self.manx[0].lower() == "ab":
                # Gains the gene
                if self.manx[0] == 'ab':
                    self.manx[0] = 'Ab'
                elif self.manx[1] == 'ab':
                    self.manx[1] = 'Ab'
                # Loses the gene
                elif self.manx[1] == 'Ab':
                    self.manx[1] = 'ab'
                elif self.manx[0] == 'Ab':
                    self.manx[0] = 'ab'
                else:
                    self.Mutate()
            elif self.manx[0].lower() == "m":
                # Gains the gene
                if self.manx[0] == 'm':
                    self.manx[0] = 'M'
                elif self.manx[1] == 'm':
                    self.manx[1] = 'M'
                # Loses the gene
                elif self.manx[1] == 'M':
                    self.manx[1] = 'm'
                elif self.manx[0] == 'M':
                    self.manx[0] = 'm'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            if self.ban_genes:
                if self.manx == ["M", "M"]:
                    self.manx = ["M", "m"]
                elif self.manx == ["Ab", "Ab"]:
                    self.manx = ["Ab", "ab"]
            print(self.manx)
        elif which == 'karel':
            print(self.kab)
            # Gains the gene
            if self.kab[1] == 'Kab':
                self.kab[1] = 'kab'
            elif self.kab[0] == 'Kab':
                self.kab[0] = 'kab'
            # Loses the gene
            elif self.kab[0] == 'kab':
                self.kab[0] = 'Kab'
            elif self.kab[1] == 'kab':
                self.kab[1] = 'Kab'
            else:
                self.Mutate()
            print(self.kab)
        elif which == 'toybob':
            print(self.toybob)
            # Gains the gene
            if self.toybob[0] == 'tb':
                self.toybob[0] = 'Tb'
            elif self.toybob[1] == 'tb':
                self.toybob[1] = 'Tb'
            # Loses the gene
            elif self.toybob[1] == 'Tb':
                self.toybob[1] = 'tb'
            elif self.toybob[0] == 'Tb':
                self.toybob[0] = 'tb'
            else:
                self.Mutate()
            print(self.toybob)
        elif which == 'japanese':
            print(self.jbob)
            # Gains the gene
            if self.jbob[1] == 'Jb':
                self.jbob[1] = 'jb'
            elif self.jbob[0] == 'Jb':
                self.jbob[0] = 'jb'
            # Loses the gene
            elif self.jbob[0] == 'jb':
                self.jbob[0] = 'Jb'
            elif self.jbob[1] == 'jb':
                self.jbob[1] = 'Jb'
            else:
                self.Mutate()
            print(self.jbob)
        elif which == 'kuril':
            print(self.kub)
            # Gains the gene
            if self.kub[0] == 'kub':
                self.kub[0] = 'Kub'
            elif self.kub[1] == 'kub':
                self.kub[1] = 'Kub'
            # Loses the gene
            elif self.kub[1] == 'Kub':
                self.kub[1] = 'kub'
            elif self.kub[0] == 'Kub':
                self.kub[0] = 'kub'
            else:
                self.Mutate()
            print(self.kub)
        elif which == 'ringtail':
            print(self.ring)
            # Gains the gene
            if self.ring[1] == 'Rt':
                self.ring[1] = 'rt'
            elif self.ring[0] == 'Rt':
                self.ring[0] = 'rt'
            # Loses the gene
            elif self.ring[0] == 'rt':
                self.ring[0] = 'Rt'
            elif self.ring[1] == 'rt':
                self.ring[1] = 'Rt'
            else:
                self.Mutate()
            print(self.ring)
        elif which == 'munchkin':
            print(self.munch)
            # Gains the gene
            if self.munch[0] == 'mk':
                self.munch[0] = 'Mk'
            elif self.munch[1] == 'mk':
                self.munch[1] = 'Mk'
            # Loses the gene
            elif self.munch[1] == 'Mk':
                self.munch[1] = 'mk'
            elif self.munch[0] == 'Mk':
                self.munch[0] = 'mk'
            else:
                self.Mutate()
            print(self.munch)
        else:  # polydactyl
            print(self.poly)
            # Gains the gene
            if self.poly[0] == 'pd':
                self.poly[0] = 'Pd'
            elif self.poly[1] == 'pd':
                self.poly[1] = 'Pd'
            # Loses the gene
            elif self.poly[1] == 'Pd':
                self.poly[1] = 'pd'
            elif self.poly[0] == 'Pd':
                self.poly[0] = 'pd'
            else:
                self.Mutate()
            print(self.poly)
        
        print(which)
    
    def FurTypemutation(self):
        whichgene = ["wirehair", "laperm", "cornish", "urals", "tennessee", "fleecy", "sedesp", "sedesp", "sedesp",
                     "russian", "russian mod", "lykoi"]

        if self.ban_genes:
            for i in range(1, 20):
                whichgene.remove("russian")
                whichgene.remove("lykoi")

        which = choice(whichgene)

        if which == 'wirehair':
            print(self.wirehair)
            # Gains the gene
            if self.wirehair[0] == 'wh':
                self.wirehair[0] = 'Wh'
            elif self.wirehair[1] == 'wh':
                self.wirehair[1] = 'Wh'
            # Loses the gene
            elif self.wirehair[1] == 'Wh':
                self.wirehair[1] = 'wh'
            elif self.wirehair[0] == 'Wh':
                self.wirehair[0] = 'wh'
            else:
                self.Mutate()
            print(self.wirehair)
        elif which == 'laperm':
            print(self.laperm)
            # Gains the gene
            if self.laperm[0] == 'lp':
                self.laperm[0] = 'Lp'
            elif self.laperm[1] == 'lp':
                self.laperm[1] = 'Lp'
            # Loses the gene
            elif self.laperm[1] == 'Lp':
                self.laperm[1] = 'lp'
            elif self.laperm[0] == 'Lp':
                self.laperm[0] = 'lp'
            else:
                self.Mutate()
            print(self.laperm)
        elif which == 'cornish':
            print(self.cornish)
            # Gains the gene
            if self.cornish[1] == 'R':
                self.cornish[1] = 'r'
            elif self.cornish[0] == 'R':
                self.cornish[0] = 'r'
            # Loses the gene
            elif self.cornish[0] == 'r':
                self.cornish[0] = 'R'
            elif self.cornish[1] == 'r':
                self.cornish[1] = 'R'
            else:
                self.Mutate()
            print(self.cornish)
        elif which == 'urals':
            print(self.urals)
            # Gains the gene
            if self.urals[1] == 'Ru':
                self.urals[1] = 'ru'
            elif self.urals[0] == 'Ru':
                self.urals[0] = 'ru'
            # Loses the gene
            elif self.urals[0] == 'ru':
                self.urals[0] = 'Ru'
            elif self.urals[1] == 'ru':
                self.urals[1] = 'Ru'
            else:
                self.Mutate()
            print(self.urals)
        elif which == 'tennessee':
            print(self.tenn)
            # Gains the gene
            if self.tenn[1] == 'Tr':
                self.tenn[1] = 'tr'
            elif self.tenn[0] == 'Tr':
                self.tenn[0] = 'tr'
            # Loses the gene
            elif self.tenn[0] == 'tr':
                self.tenn[0] = 'Tr'
            elif self.tenn[1] == 'tr':
                self.tenn[1] = 'Tr'
            else:
                self.Mutate()
            print(self.tenn)
        elif which == 'fleecy':
            print(self.fleece)
            # Gains the gene
            if self.fleece[1] == 'Fc':
                self.fleece[1] = 'fc'
            elif self.fleece[0] == 'Fc':
                self.fleece[0] = 'fc'
            # Loses the gene
            elif self.fleece[0] == 'fc':
                self.fleece[0] = 'Fc'
            elif self.fleece[1] == 'fc':
                self.fleece[1] = 'Fc'
            else:
                self.Mutate()
            print(self.fleece)
        elif which == 'sedesp':
            print(self.sedesp)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.sedesp[0] != 're' and hell == 1:
                ### Selkirk ###
                if self.sedesp[1] == 'Se':
                    self.sedesp[1] = choice(['Hr', 'hr', 're'])
                elif self.sedesp[0] == 'Se':
                    if self.sedesp[1] == 'Hr':
                        self.sedesp[0] = 'Hr'
                    elif self.sedesp[1] == 'hr':
                        self.sedesp[0] = choice(['Hr', 'hr'])
                    elif self.sedesp[1] == 're':
                        self.sedesp[0] = choice(['Hr', 'hr', 're'])
                    else:
                        self.Mutate()
                ### Normal Coat ###
                elif self.sedesp[1] == 'Hr':
                    self.sedesp[1] = choice(['hr', 're'])
                elif self.sedesp[0] == 'Hr':
                    if self.sedesp[1] == 'hr':
                        self.sedesp[0] = 'hr'
                    elif self.sedesp[1] == 're':
                        self.sedesp[0] = choice(['hr', 're'])
                    else:
                        self.Mutate()
                ### Hairless ###
                elif self.sedesp[1] == 'hr':
                    self.sedesp[1] = 're'
                elif self.sedesp[0] == 'hr':
                    self.sedesp[0] = 're'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.sedesp[0] == 're' or hell == 2:
                ### Devon ###
                if self.sedesp[0] == 're':
                    self.sedesp[0] = choice(['Se', 'Hr', 'hr'])
                elif self.sedesp[1] == 're':
                    if self.sedesp[0] == 'Se':
                        self.sedesp[1] = choice(['Se', 'Hr', 'hr'])
                    elif self.sedesp[0] == 'Hr':
                        self.sedesp[1] = choice(['Hr', 'hr'])
                    elif self.sedesp[0] == 'hr':
                        self.sedesp[1] = 'hr'
                    else:
                        self.Mutate()
                ### Hairless ###
                elif self.sedesp[0] == 'hr':
                    self.sedesp[0] = choice(['Se', 'Hr'])
                elif self.sedesp[1] == 'hr':
                    if self.sedesp[0] == 'Se':
                        self.sedesp[1] = choice(['Se', 'Hr'])
                    elif self.sedesp[0] == 'Hr':
                        self.sedesp[1] = 'Hr'
                    else:
                        self.Mutate()
                ### Normal Coat ###
                elif self.sedesp[0] == 'Hr':
                    self.sedesp[0] = 'Se'
                elif self.sedesp[1] == 'Hr':
                    self.sedesp[1] = 'Se'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.sedesp)
        elif which == 'russian':
            print(self.ruhr)
            # Gains the gene
            if self.ruhr[0] == 'hrbd':
                self.ruhr[0] = 'Hrbd'
            elif self.ruhr[1] == 'hrbd':
                self.ruhr[1] = 'Hrbd'
            # Loses the gene
            elif self.ruhr[1] == 'Hrbd':
                self.ruhr[1] = 'hrbd'
            elif self.ruhr[0] == 'Hrbd':
                self.ruhr[0] = 'hrbd'
            else:
                self.Mutate()
            print(self.ruhr)
        elif which == 'russian mod':
            print(self.ruhrmod)
            # Gains the gene
            if self.ruhrmod[1] == 'hi':
                self.ruhrmod[1] = 'ha'
            elif self.ruhrmod[0] == 'hi':
                self.ruhrmod[0] = 'ha'
            # Loses the gene
            elif self.ruhrmod[0] == 'ha':
                self.ruhrmod[0] = 'hi'
            elif self.ruhrmod[1] == 'ha':
                self.ruhrmod[1] = 'hi'
            else:
                self.Mutate()
            print(self.ruhrmod)
        else:  # lykoi
            print(self.lykoi)
            # Gains the gene
            if self.lykoi[1] == 'Ly':
                self.lykoi[1] = 'ly'
            elif self.lykoi[0] == 'Ly':
                self.lykoi[0] = 'ly'
            # Loses the gene
            elif self.lykoi[0] == 'ly':
                self.lykoi[0] = 'Ly'
            elif self.lykoi[1] == 'ly':
                self.lykoi[1] = 'Ly'
            else:
                self.Mutate()
            print(self.lykoi)

        print(which)

    def OtherCoatmutation(self):
        whichgene = ["pinkdilute", "dilute mod", "extention", "corin", "karpati", "bleaching", "ghosting", "satin",
                     "glitter"]

        if self.ban_genes:
            for i in range(1, 20):
                whichgene.remove("pinkdilute")

        which = choice(whichgene)

        if which == 'pinkdilute':
            print(self.pinkdilute)
            # Gains the gene
            if self.pinkdilute[1] == 'Dp':
                self.pinkdilute[1] = 'dp'
            elif self.pinkdilute[0] == 'Dp':
                self.pinkdilute[0] = 'dp'
            # Loses the gene
            elif self.pinkdilute[0] == 'dp':
                self.pinkdilute[0] = 'Dp'
            elif self.pinkdilute[1] == 'dp':
                self.pinkdilute[1] = 'Dp'
            else:
                self.Mutate()
            print(self.pinkdilute)
        elif which == 'dilute mod':
            print(self.dilutemd)
            # Gains the gene
            if self.dilutemd[0] == 'dm':
                self.dilutemd[0] = 'Dm'
            elif self.dilutemd[1] == 'dm':
                self.dilutemd[1] = 'Dm'
            # Loses the gene
            elif self.dilutemd[1] == 'Dm':
                self.dilutemd[1] = 'dm'
            elif self.dilutemd[0] == 'Dm':
                self.dilutemd[0] = 'dm'
            else:
                self.Mutate()
            print(self.dilutemd)
        elif which == 'extention':
            print(self.ext)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.ext[0] != 'ec' and hell == 1:
                ### Chausie Grizzle ###
                if self.ext[1] == 'Eg':
                    self.ext[1] = choice(['E', 'ea', 'er', 'ec'])
                elif self.ext[0] == 'Eg':
                    if self.ext[1] == 'E':
                        self.ext[0] = 'E'
                    elif self.ext[1] == 'ea':
                        self.ext[0] = choice(['E', 'ea'])
                    elif self.ext[1] == 'er':
                        self.ext[0] = choice(['E', 'ea', 'er'])
                    elif self.ext[1] == 'ec':
                        self.ext[0] = choice(['E', 'ea', 'er', 'ec'])
                    else:
                        self.Mutate()
                ### Normal Coloration ###
                elif self.ext[1] == 'E':
                    self.ext[1] = choice(['ea', 'er', 'ec'])
                elif self.ext[0] == 'E':
                    if self.ext[1] == 'ea':
                        self.ext[0] = 'ea'
                    elif self.ext[1] == 'er':
                        self.ext[0] = choice(['ea', 'er'])
                    elif self.ext[1] == 'ec':
                        self.ext[0] = choice(['ea', 'er', 'ec'])
                    else:
                        self.Mutate()
                ### Amber ###
                elif self.ext[1] == 'ea':
                    self.ext[1] = choice(['er', 'ec'])
                elif self.ext[0] == 'ea':
                    if self.ext[1] == 'er':
                        self.ext[0] = 'er'
                    elif self.ext[1] == 'ec':
                        self.ext[0] = choice(['er', 'ec'])
                    else:
                        self.Mutate()
                ### Russet ###
                elif self.ext[1] == 'er':
                    self.ext[1] = 'ec'
                elif self.ext[0] == 'er':
                    self.ext[0] = 'ec'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.ext[0] == 'ec' or hell == 2:
                ### Carnelian ###
                if self.ext[0] == 'ec':
                    self.ext[0] = choice(['Eg', 'E', 'ea', 'er'])
                elif self.ext[1] == 'ec':
                    if self.ext[0] == 'Eg':
                        self.ext[1] = choice(['Eg', 'E', 'ea', 'er'])
                    elif self.ext[0] == 'E':
                        self.ext[1] = choice(['E', 'ea', 'er'])
                    elif self.ext[0] == 'ea':
                        self.ext[1] = choice(['ea', 'er'])
                    elif self.ext[0] == 'er':
                        self.ext[1] = 'er'
                    else:
                        self.Mutate()
                ### Russet ###
                elif self.ext[0] == 'er':
                    self.ext[0] = choice(['Eg', 'E', 'ea'])
                elif self.ext[1] == 'er':
                    if self.ext[0] == 'Eg':
                        self.ext[1] = choice(['Eg', 'E', 'ea'])
                    elif self.ext[0] == 'E':
                        self.ext[1] = choice(['E', 'ea'])
                    elif self.ext[0] == 'ea':
                        self.ext[1] = 'ea'
                    else:
                        self.Mutate()
                ### Amber ###
                elif self.ext[0] == 'ea':
                    self.ext[0] = choice(['Eg', 'E'])
                elif self.ext[1] == 'ea':
                    if self.ext[0] == 'Eg':
                        self.ext[1] = choice(['Eg', 'E'])
                    elif self.ext[0] == 'E':
                        self.ext[1] = 'E'
                    else:
                        self.Mutate()
                ### Normal Coloration ###
                elif self.ext[0] == 'E':
                    self.ext[0] = 'Eg'
                elif self.ext[1] == 'E':
                    self.ext[1] = 'Eg'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.ext)
        elif which == 'corin':
            print(self.corin)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.corin[0] != 'fg' and hell == 1:
                ### Normal Coloration ###
                if self.corin[1] == 'N':
                    self.corin[1] = choice(['sg', 'sh', 'fg'])
                elif self.corin[0] == 'N':
                    if self.corin[1] == 'sg':
                        self.corin[0] = 'sg'
                    elif self.corin[1] == 'sh':
                        self.corin[0] = choice(['sg', 'sh'])
                    elif self.corin[1] == 'fg':
                        self.corin[0] = choice(['sg', 'sh', 'fg'])
                    else:
                        self.Mutate()
                ### Siberian Gold ###
                elif self.corin[1] == 'sg':
                    self.corin[1] = choice(['sh', 'fg'])
                elif self.corin[0] == 'sg':
                    if self.corin[1] == 'sh':
                        self.corin[0] = 'sh'
                    elif self.corin[1] == 'fg':
                        self.corin[0] = choice(['sh', 'fg'])
                    else:
                        self.Mutate()
                ### Sunshine ###
                elif self.corin[1] == 'sh':
                    self.corin[1] = 'fg'
                elif self.corin[0] == 'sh':
                    self.corin[0] = 'fg'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.corin[0] == 'fg' or hell == 2:
                ### Flaxen Gold ###
                if self.corin[0] == 'fg':
                    self.corin[0] = choice(['N', 'sg', 'sh'])
                elif self.corin[1] == 'fg':
                    if self.corin[0] == 'N':
                        self.corin[1] = choice(['N', 'sg', 'sh'])
                    elif self.corin[0] == 'sg':
                        self.corin[1] = choice(['sg', 'sh'])
                    elif self.corin[0] == 'sh':
                        self.corin[1] = 'sh'
                    else:
                        self.Mutate()
                ### Sunshine ###
                elif self.corin[0] == 'sh':
                    self.corin[0] = choice(['N', 'sg'])
                elif self.corin[1] == 'sh':
                    if self.corin[0] == 'N':
                        self.corin[1] = choice(['N', 'sg'])
                    elif self.corin[0] == 'sg':
                        self.corin[1] = 'sg'
                    else:
                        self.Mutate()
                ### Siberian Gold ###
                elif self.corin[0] == 'sg':
                    self.corin[0] = 'N'
                elif self.corin[1] == 'sg':
                    self.corin[1] = 'N'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.corin)
        elif which == 'karpati':
            print(self.karp)
            # Gains the gene
            if self.karp[0] == 'k':
                self.karp[0] = 'K'
            elif self.karp[1] == 'k':
                self.karp[1] = 'K'
            # Loses the gene
            elif self.karp[1] == 'K':
                self.karp[1] = 'k'
            elif self.karp[0] == 'K':
                self.karp[0] = 'k'
            else:
                self.Mutate()
            print(self.karp)
        elif which == 'bleaching':
            print(self.bleach)
            # Gains the gene
            if self.bleach[1] == 'Lb':
                self.bleach[1] = 'lb'
            elif self.bleach[0] == 'Lb':
                self.bleach[0] = 'lb'
            # Loses the gene
            elif self.bleach[0] == 'lb':
                self.bleach[0] = 'Lb'
            elif self.bleach[1] == 'lb':
                self.bleach[1] = 'Lb'
            else:
                self.Mutate()
            print(self.bleach)
        elif which == 'ghosting':
            print(self.ghosting)
            # Gains the gene
            if self.ghosting[0] == 'gh':
                self.ghosting[0] = 'Gh'
            elif self.ghosting[1] == 'gh':
                self.ghosting[1] = 'Gh'
            # Loses the gene
            elif self.ghosting[1] == 'Gh':
                self.ghosting[1] = 'gh'
            elif self.ghosting[0] == 'Gh':
                self.ghosting[0] = 'gh'
            else:
                self.Mutate()
            print(self.ghosting)
        elif which == 'satin':
            print(self.satin)
            # Gains the gene
            if self.satin[1] == 'St':
                self.satin[1] = 'st'
            elif self.satin[0] == 'St':
                self.satin[0] = 'st'
            # Loses the gene
            elif self.satin[0] == 'st':
                self.satin[0] = 'St'
            elif self.satin[1] == 'st':
                self.satin[1] = 'St'
            else:
                self.Mutate()
            print(self.satin)
        else:  # glitter
            print(self.glitter)
            # Gains the gene
            if self.glitter[1] == 'Gl':
                self.glitter[1] = 'gl'
            elif self.glitter[0] == 'Gl':
                self.glitter[0] = 'gl'
            # Loses the gene
            elif self.glitter[0] == 'gl':
                self.glitter[0] = 'Gl'
            elif self.glitter[1] == 'gl':
                self.glitter[1] = 'Gl'
            else:
                self.Mutate()
            print(self.glitter)

        print(which)
    
    def MainCoatmutation(self):
        whichgene = ["furlength", "black", "red", "dilute", "white", "point", "silver", "agouti", "mackerel", "ticked",
                     "DBE"]

        which = choice(whichgene)

        if which == 'furlength':
            print(self.furLength)
            # Gains the gene
            if self.furLength[1] == 'L':
                self.furLength[1] = 'l'
            elif self.furLength[0] == 'L':
                self.furLength[0] = 'l'
            # Loses the gene
            elif self.furLength[0] == 'l':
                self.furLength[0] = 'L'
            elif self.furLength[1] == 'l':
                self.furLength[1] = 'L'
            else:
                self.Mutate()
            print(self.furLength)
        elif which == 'black':
            print(self.eumelanin)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.eumelanin[0] != 'bl' and hell == 1:
                ### Black ###
                if self.eumelanin[1] == 'B':
                    self.eumelanin[1] = choice(['b', 'bl'])
                elif self.eumelanin[0] == 'B':
                    if self.eumelanin[1] == 'b':
                        self.eumelanin[0] = 'b'
                    elif self.eumelanin[1] == 'bl':
                        self.eumelanin[0] = choice(['b', 'bl'])
                    else:
                        self.Mutate()
                ### Chocolate ###
                elif self.eumelanin[1] == 'b':
                    self.eumelanin[1] = 'bl'
                elif self.eumelanin[0] == 'b':
                    self.eumelanin[0] = 'bl'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.eumelanin[0] == 'bl' or hell == 2:
                ### Cinnamon ###
                if self.eumelanin[0] == 'bl':
                    self.eumelanin[0] = choice(['B', 'b'])
                elif self.eumelanin[1] == 'bl':
                    if self.eumelanin[0] == 'B':
                        self.eumelanin[1] = choice(['B', 'b'])
                    elif self.eumelanin[0] == 'b':
                        self.eumelanin[1] = 'b'
                    else:
                        self.Mutate()
                ### Chocolate ###
                elif self.eumelanin[0] == 'b':
                    self.eumelanin[0] = 'B'
                elif self.eumelanin[1] == 'b':
                    self.eumelanin[1] = 'B'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.eumelanin)
        elif which == 'red':
            print(self.sexgene)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if ("o" in self.sexgene and "O" in self.sexgene and hell == 1) or ("o" in self.sexgene and "O" not in self.sexgene):
                if self.sexgene[0] == "o":
                    self.sexgene[0] = "O"
                elif len(self.sexgene) > 1 and self.sexgene[1] == "o":
                    self.sexgene[1] = "O"
                elif len(self.sexgene) > 2 and self.sexgene[2] == "o":
                    self.sexgene[2] = "O"
                elif len(self.sexgene) > 3 and self.sexgene[3] == "o":
                    self.sexgene[3] = "O"
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif ("o" in self.sexgene and "O" in self.sexgene and hell == 2) or ("o" not in self.sexgene and "O" in self.sexgene):
                if len(self.sexgene) > 3 and self.sexgene[3] == "O":
                    self.sexgene[3] = "o"
                elif len(self.sexgene) > 2 and self.sexgene[2] == "O":
                    self.sexgene[2] = "o"
                elif len(self.sexgene) > 1 and self.sexgene[1] == "O":
                    self.sexgene[1] = "o"
                elif self.sexgene[0] == "O":
                    self.sexgene[0] = "o"
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.sexgene)
        elif which == 'dilute':
            print(self.dilute)
            # Gains the gene
            if self.dilute[1] == 'D':
                self.dilute[1] = 'd'
            elif self.dilute[0] == 'D':
                self.dilute[0] = 'd'
            # Loses the gene
            elif self.dilute[0] == 'd':
                self.dilute[0] = 'D'
            elif self.dilute[1] == 'd':
                self.dilute[1] = 'D'
            else:
                self.Mutate()
            print(self.dilute)
        elif which == 'white':
            print(self.white)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.white[0] != 'wsal' and hell == 1:
                ### Dominant White ###
                if self.white[1] == 'W':
                    self.white[1] = choice(['ws', 'wt', 'w', 'wg', 'wsal'])
                elif self.white[0] == 'W':
                    if self.white[1] == 'ws':
                        self.white[0] = 'ws'
                    elif self.white[1] == 'wt':
                        self.white[0] = choice(['ws', 'wt'])
                    elif self.white[1] == 'w':
                        self.white[0] = choice(['ws', 'wt', 'w'])
                    elif self.white[1] == 'wg':
                        self.white[0] = choice(['ws', 'wt', 'w', 'wg'])
                    elif self.white[1] == 'wsal':
                        self.white[0] = choice(['ws', 'wt', 'w', 'wg', 'wsal'])
                    else:
                        self.Mutate()
                ### White Spotting ###
                elif self.white[1] == 'ws':
                    self.white[1] = choice(['wt', 'w', 'wg', 'wsal'])
                elif self.white[0] == 'ws':
                    if self.white[1] == 'wt':
                        self.white[0] = 'wt'
                    elif self.white[1] == 'w':
                        self.white[0] = choice(['wt', 'w'])
                    elif self.white[1] == 'wg':
                        self.white[0] = choice(['wt', 'w', 'wg'])
                    elif self.white[1] == 'wsal':
                        self.white[0] = choice(['wt', 'w', 'wg', 'wsal'])
                    else:
                        self.Mutate()
                ### Thai White ###
                elif self.white[1] == 'wt':
                    self.white[1] = choice(['w', 'wg', 'wsal'])
                elif self.white[0] == 'wt':
                    if self.white[1] == 'w':
                        self.white[0] = 'w'
                    elif self.white[1] == 'wg':
                        self.white[0] = choice(['w', 'wg'])
                    elif self.white[1] == 'wsal':
                        self.white[0] = choice(['w', 'wg', 'wsal'])
                    else:
                        self.Mutate()
                ### No White ###
                elif self.white[1] == 'w':
                    self.white[1] = choice(['wg', 'wsal'])
                elif self.white[0] == 'w':
                    if self.white[1] == 'wg':
                        self.white[0] = 'wg'
                    elif self.white[1] == 'wsal':
                        self.white[0] = choice(['wg', 'wsal'])
                    else:
                        self.Mutate()
                ### Birman Gloving ###
                elif self.white[1] == 'wg':
                    self.white[1] = 'wsal'
                elif self.white[0] == 'wg':
                    self.white[0] = 'wsal'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.white[0] == 'wsal' or hell == 2:
                ### Salmiak ###
                if self.white[0] == 'wsal':
                    self.white[0] = choice(['W', 'ws', 'wt', 'w', 'wg'])
                elif self.white[1] == 'wsal':
                    if self.white[0] == 'W':
                        self.white[1] = choice(['W', 'ws', 'wt', 'w', 'wg'])
                    elif self.white[0] == 'ws':
                        self.white[1] = choice(['ws', 'wt', 'w', 'wg'])
                    elif self.white[0] == 'wt':
                        self.white[1] = choice(['wt', 'w', 'wg'])
                    elif self.white[0] == 'w':
                        self.white[1] = choice(['w', 'wg'])
                    elif self.white[0] == 'wg':
                        self.white[1] = 'wg'
                    else:
                        self.Mutate()
                ### Birman Gloving ###
                elif self.white[0] == 'wg':
                    self.white[0] = choice(['W', 'ws', 'wt', 'w'])
                elif self.white[1] == 'wg':
                    if self.white[0] == 'W':
                        self.white[1] = choice(['W', 'ws', 'wt', 'w'])
                    elif self.white[0] == 'ws':
                        self.white[1] = choice(['ws', 'wt', 'w'])
                    elif self.white[0] == 'wt':
                        self.white[1] = choice(['wt', 'w'])
                    elif self.white[0] == 'w':
                        self.white[1] = 'w'
                    else:
                        self.Mutate()
                ### No White ###
                elif self.white[0] == 'w':
                    self.white[0] = choice(['W', 'ws', 'wt'])
                elif self.white[1] == 'w':
                    if self.white[0] == 'W':
                        self.white[1] = choice(['W', 'ws', 'wt'])
                    elif self.white[0] == 'ws':
                        self.white[1] = choice(['ws', 'wt'])
                    elif self.white[0] == 'wt':
                        self.white[1] = 'wt'
                    else:
                        self.Mutate()
                ### Thai White ###
                elif self.white[0] == 'wt':
                    self.white[0] = choice(['W', 'ws'])
                elif self.white[1] == 'wt':
                    if self.white[0] == 'W':
                        self.white[1] = choice(['W', 'ws'])
                    elif self.white[0] == 'ws':
                        self.white[1] = 'ws'
                    else:
                        self.Mutate()
                ### White Spotting ###
                elif self.white[0] == 'ws':
                    self.white[0] = 'W'
                elif self.white[1] == 'ws':
                    self.white[1] = 'W'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.white)
        elif which == 'point':
            print(self.pointgene)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.pointgene[0] != 'c' and hell == 1:
                ### Normal Coloration ###
                if self.pointgene[1] == 'C':
                    self.pointgene[1] = choice(['cb', 'cs', 'cm', 'c'])
                elif self.pointgene[0] == 'C':
                    if self.pointgene[1] == 'cb':
                        self.pointgene[0] = 'cb'
                    elif self.pointgene[1] == 'cs':
                        self.pointgene[0] = choice(['cb', 'cs'])
                    elif self.pointgene[1] == 'cm':
                        self.pointgene[0] = choice(['cb', 'cs', 'cm'])
                    elif self.pointgene[1] == 'c':
                        self.pointgene[0] = choice(['cb', 'cs', 'cm', 'c'])
                    else:
                        self.Mutate()
                ### Sepia ###
                elif self.pointgene[1] == 'cb':
                    self.pointgene[1] = choice(['cs', 'cm', 'c'])
                elif self.pointgene[0] == 'cb':
                    if self.pointgene[1] == 'cs':
                        self.pointgene[0] = 'cs'
                    elif self.pointgene[1] == 'cm':
                        self.pointgene[0] = choice(['cs', 'cm'])
                    elif self.pointgene[1] == 'c':
                        self.pointgene[0] = choice(['cs', 'cm', 'c'])
                    else:
                        self.Mutate()
                ### Colorpoint ###
                elif self.pointgene[1] == 'cs':
                    self.pointgene[1] = choice(['cm', 'c'])
                elif self.pointgene[0] == 'cs':
                    if self.pointgene[1] == 'cm':
                        self.pointgene[0] = 'cm'
                    elif self.pointgene[1] == 'c':
                        self.pointgene[0] = choice(['cm', 'c'])
                    else:
                        self.Mutate()
                ### Mocha ###
                elif self.pointgene[1] == 'cm':
                    self.pointgene[1] = 'c'
                elif self.pointgene[0] == 'cm':
                    self.pointgene[0] = 'c'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.pointgene[0] == 'c' or hell == 2:
                ### Albino ###
                if self.pointgene[0] == 'c':
                    self.pointgene[0] = choice(['C', 'cb', 'cs', 'cm'])
                elif self.pointgene[1] == 'c':
                    if self.pointgene[0] == 'C':
                        self.pointgene[1] = choice(['C', 'cb', 'cs', 'cm'])
                    elif self.pointgene[0] == 'cb':
                        self.pointgene[1] = choice(['cb', 'cs', 'cm'])
                    elif self.pointgene[0] == 'cs':
                        self.pointgene[1] = choice(['cs', 'cm'])
                    elif self.pointgene[0] == 'cm':
                        self.pointgene[1] = 'cm'
                    else:
                        self.Mutate()
                ### Mocha ###
                elif self.pointgene[0] == 'cm':
                    self.pointgene[0] = choice(['C', 'cb', 'cs'])
                elif self.pointgene[1] == 'cm':
                    if self.pointgene[0] == 'C':
                        self.pointgene[1] = choice(['C', 'cb', 'cs'])
                    elif self.pointgene[0] == 'cb':
                        self.pointgene[1] = choice(['cb', 'cs'])
                    elif self.pointgene[0] == 'cs':
                        self.pointgene[1] = 'cs'
                    else:
                        self.Mutate()
                ### Colorpoint ###
                elif self.pointgene[0] == 'cs':
                    self.pointgene[0] = choice(['C', 'cb'])
                elif self.pointgene[1] == 'cs':
                    if self.pointgene[0] == 'C':
                        self.pointgene[1] = choice(['C', 'cb'])
                    elif self.pointgene[0] == 'cb':
                        self.pointgene[1] = 'cb'
                    else:
                        self.Mutate()
                ### Sepia ###
                elif self.pointgene[0] == 'cb':
                    self.pointgene[0] = 'C'
                elif self.pointgene[1] == 'cb':
                    self.pointgene[1] = 'C'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            if self.ban_genes:
                if self.pointgene[0] == 'c':
                    self.pointgene[0] = 'cm'
                if self.pointgene[1] == 'c':
                    self.pointgene[1] = 'cm'
            print(self.pointgene)
        elif which == 'silver':
            print(self.silver)
            # Gains the gene
            if self.silver[0] == 'i':
                self.silver[0] = 'I'
            elif self.silver[1] == 'i':
                self.silver[1] = 'I'
            # Loses the gene
            elif self.silver[1] == 'I':
                self.silver[1] = 'i'
            elif self.silver[0] == 'I':
                self.silver[0] = 'i'
            else:
                self.Mutate()
            print(self.silver)
        elif which == 'agouti':
            print(self.agouti)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.agouti[0] != 'a' and hell == 1:
                ### Agouti ###
                if self.agouti[1] == 'A':
                    self.agouti[1] = choice(['Apb', 'a'])
                elif self.agouti[0] == 'A':
                    if self.agouti[1] == 'Apb':
                        self.agouti[0] = 'Apb'
                    elif self.agouti[1] == 'a':
                        self.agouti[0] = choice(['Apb', 'a'])
                    else:
                        self.Mutate()
                ### Charcoal ###
                elif self.agouti[1] == 'Apb':
                    self.agouti[1] = 'a'
                elif self.agouti[0] == 'Apb':
                    self.agouti[0] = 'a'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.agouti[0] == 'a' or hell == 2:
                ### Solid ###
                if self.agouti[0] == 'a':
                    self.agouti[0] = choice(['A', 'Apb'])
                elif self.agouti[1] == 'a':
                    if self.agouti[0] == 'A':
                        self.agouti[1] = choice(['A', 'Apb'])
                    elif self.agouti[0] == 'Apb':
                        self.agouti[1] = 'Apb'
                    else:
                        self.Mutate()
                ### Charcoal ###
                elif self.agouti[0] == 'Apb':
                    self.agouti[0] = 'A'
                elif self.agouti[1] == 'Apb':
                    self.agouti[1] = 'A'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.agouti)
        elif which == 'mackerel':
            print(self.mack)
            # Gains the gene
            if self.mack[1] == 'Mc':
                self.mack[1] = 'mc'
            elif self.mack[0] == 'Mc':
                self.mack[0] = 'mc'
            # Loses the gene
            elif self.mack[0] == 'mc':
                self.mack[0] = 'Mc'
            elif self.mack[1] == 'mc':
                self.mack[1] = 'Mc'
            else:
                self.Mutate()
            print(self.mack)
        elif which == 'ticked':
            print(self.ticked)
            # Gains the gene
            if self.ticked[0] == 'ta':
                self.ticked[0] = 'Ta'
            elif self.ticked[1] == 'ta':
                self.ticked[1] = 'Ta'
            # Loses the gene
            elif self.ticked[1] == 'Ta':
                self.ticked[1] = 'ta'
            elif self.ticked[0] == 'Ta':
                self.ticked[0] = 'ta'
            else:
                self.Mutate()
            print(self.ticked)
        else:  # DBE
            print(self.pax3)
            hell = randint(1, 2)
            ###### Gains the gene ######
            if self.pax3[0] != 'NoDBE' and hell == 1:
                ### Altai ###
                if self.pax3[1] == 'DBEalt':
                    self.pax3[1] = choice(['DBEcel', 'DBEre', 'NoDBE'])
                elif self.pax3[0] == 'DBEalt':
                    if self.pax3[1] == 'DBEcel':
                        self.pax3[0] = 'DBEcel'
                    elif self.pax3[1] == 'DBEre':
                        self.pax3[0] = choice(['DBEcel', 'DBEre'])
                    elif self.pax3[1] == 'NoDBE':
                        self.pax3[0] = choice(['DBEcel', 'DBEre', 'NoDBE'])
                    else:
                        self.Mutate()
                ### Celestial ###
                elif self.pax3[1] == 'DBEcel':
                    self.pax3[1] = choice(['DBEre', 'NoDBE'])
                elif self.pax3[0] == 'DBEcel':
                    if self.pax3[1] == 'DBEre':
                        self.pax3[0] = 'DBEre'
                    elif self.pax3[1] == 'NoDBE':
                        self.pax3[0] = choice(['DBEre', 'NoDBE'])
                    else:
                        self.Mutate()
                ### Dutch Maine Coon ###
                elif self.pax3[1] == 'DBEre':
                    self.pax3[1] = 'NoDBE'
                elif self.pax3[0] == 'DBEre':
                    self.pax3[0] = 'NoDBE'
                else:
                    self.Mutate()
            ###### Loses the gene ######
            elif self.pax3[0] == 'NoDBE' or hell == 2:
                ### No DBE ###
                if self.pax3[0] == 'NoDBE':
                    self.pax3[0] = choice(['DBEalt', 'DBEcel', 'DBEre'])
                elif self.pax3[1] == 'NoDBE':
                    if self.pax3[0] == 'DBEalt':
                        self.pax3[1] = choice(['DBEalt', 'DBEcel', 'DBEre'])
                    elif self.pax3[0] == 'DBEcel':
                        self.pax3[1] = choice(['DBEcel', 'DBEre'])
                    elif self.pax3[0] == 'DBEre':
                        self.pax3[1] = 'DBEre'
                    else:
                        self.Mutate()
                ### Dutch Maine Coon ###
                elif self.pax3[0] == 'DBEre':
                    self.pax3[0] = choice(['DBEalt', 'DBEcel'])
                elif self.pax3[1] == 'DBEre':
                    if self.pax3[0] == 'DBEalt':
                        self.pax3[1] = choice(['DBEalt', 'DBEcel'])
                    elif self.pax3[0] == 'DBEcel':
                        self.pax3[1] = 'DBEcel'
                    else:
                        self.Mutate()
                ### Celestial ###
                elif self.pax3[0] == 'DBEcel':
                    self.pax3[0] = 'DBEalt'
                elif self.pax3[1] == 'DBEcel':
                    self.pax3[1] = 'DBEalt'
                else:
                    self.Mutate()
            else:
                self.Mutate()
            print(self.pax3)

        print(which)

    def GenerateSomatic(self):
        self.somatic["base"] = choice(['Somatic/leftface', 'Somatic/rightface', 'Somatic/tail',
                                    'underbelly1', 'right front bicolour2', 'left front bicolour2',
                                    'right back bicolour2', 'left back bicolour2'])

        possible_mutes = {
        "furtype" : ["wirehair", "laperm", "cornish", "urals", "tenn", "fleece", "sedesp"],
        "other" : ["pinkdilute", "ext", "corin", "karp"],
        "main" : ["eumelanin", "sexgene", "dilute", "white", "pointgene", "silver", "agouti"]
        }
        filtered_mutes = {
        "furtype" : ["wirehair", "laperm", "cornish", "urals", "tenn", "fleece", "sedesp"],
        "other" : ["pinkdilute", "ext", "corin", "karp"],
        "main" : ["eumelanin", "sexgene", "dilute", "white", "pointgene", "silver", "agouti"]
        }

        for gene in possible_mutes["furtype"]:
            if gene in ['wirehair', 'laperm', 'sedesp']:
                if self[gene][0] in ['Wh', 'Lp', 'Se', 'hr', 're']:
                    filtered_mutes["furtype"].remove(gene)
            try:
                if self[gene][0] in ['r', 'ru', 'tr', 'fc']:
                    filtered_mutes["furtype"].remove(gene)
                elif self[gene][1] in ['R', 'Ru', 'Tr', 'Fc']:
                    filtered_mutes["furtype"].remove(gene)
            except:
                continue
        for gene in possible_mutes["other"]:
            if gene == 'corin' and (self.agouti[0] == 'a' or self.ext[0] == 'Eg'):
                filtered_mutes["other"].remove(gene)
                continue
            elif gene in ['ext', 'karp', 'ghosting']:
                if self[gene][0] in ['Eg', 'K', 'Gh']:
                    filtered_mutes["other"].remove(gene)
                    continue
            if self[gene][0] in ['dp', 'ec', 'ea', 'er', 'sh', 'sg', 'fg', 'lb', 'st', 'gl']:
                filtered_mutes["other"].remove(gene)
            elif self[gene][1] in ['Dp', 'E', 'N', 'Lb', 'St', 'Gl']:
                filtered_mutes["other"].remove(gene)
        for gene in possible_mutes["main"]:
            if gene in ['mack', 'ticked', 'silver'] and (self.agouti[0] == 'a' or self.ext[0] == 'Eg'):
                filtered_mutes["main"].remove(gene)
                continue
            elif gene == 'agouti' and (self.ext[0] == 'Eg' or 'o' not in self.sexgene):
                filtered_mutes["main"].remove(gene)
                continue
            elif gene in ['white']:
                if self[gene][0] in ['W', 'ws', 'wt']:
                    filtered_mutes["main"].remove(gene)
                    continue
            if self[gene][0] in ['I', 'b', 'bl', 'd', 'wg', 'wsal', 'cs', 'cb', 'cm', 'c', 'Apb', 'a']:
                filtered_mutes["main"].remove(gene)
            elif self[gene][1] in ['B', 'D', 'w', 'C', 'A']:
                filtered_mutes["main"].remove(gene)

        if "eumelanin" in filtered_mutes["main"] and self.sexgene[0] != "o":
            filtered_mutes["main"].remove("eumelanin")

        whichgene = ['furtype', 'other', 'main', 'other', 'main', 'main']
        if self.white[0] == 'W' or (self.white[1] in ['ws', 'wt'] and self.whitegrade == 5):
            whichgene = ['furtype']
        for cate in ['furtype', 'other', 'main']:
            if len(filtered_mutes[cate]) == 0:
                while cate in whichgene:
                    whichgene.remove(cate)
        if len(whichgene) > 0:
            self.somatic["gene"] = choice(filtered_mutes[choice(whichgene)])
        else:
            self.somatic = {}
            return


        if self.white[1] in ['ws', 'wt'] and self.somatic["base"] not in ['Somatic/leftface', 'Somatic/rightface', 'Somatic/tail']:
            self.somatic["base"] = choice(['Somatic/leftface', 'Somatic/rightface', 'Somatic/tail'])
        if self.somatic["gene"] in possible_mutes["furtype"]:
            self.somatic["base"] = "Somatic/tail"

        alleles = {
            "wirehair" : ['Wh'],
            "laperm" : ['Lp'],
            "cornish" : ['r'],
            "urals" : ['ru'],
            "tenn" : ['tr'],
            "fleece" : ['fc'],
            "sedesp" : ['Se'],

            'pinkdilute' : ['dp'],
            "ext" : ['ec', 'er', 'ea'],
            "corin" : ['sh', 'sg', 'fg'],
            "karp" : ['K'],
            "bleach" : ['lb'],
            "ghosting" : ['Gh'],

            'eumelanin' : ['b', 'bl'],
            'sexgene' : ['O'],
            "dilute" : ['d'],
            "white" : ['W', 'wsal'],
            "pointgene" : ['cb', 'cs', 'cm', 'c'],
            "silver" : ['I'],
            "agouti" : ['a']
        }

        self.somatic["allele"] = choice(alleles[self.somatic['gene']])
        if self.somatic['gene'] == 'sexgene' and self.sexgene[0] == 'O':
            self.somatic["allele"] = 'o'

    def FormatSomatic(self):
        body = {
            "Somatic/leftface" : "face",
            "Somatic/rightface" : "face",
            "Somatic/tail" : 'tail',
            "underbelly1" : 'underbelly',
            'right front bicolour2' : 'front leg',
            'left front bicolour2' : 'front leg',
            'right back bicolour2' : 'back leg',
            'left back bicolour2' : 'back leg'
        }
        if not self.somatic.get('gene', False):
            return ""

        alleles = {
            "wirehair" : "Wirehair",
            "laperm" : "LaPerm rex",
            "cornish" : "Cornish rex",
            "urals" : "Urals rex",
            "tenn" : "Tennessee rex",
            "fleece" : "Fleecy cloud rexing",
            "sedesp" : "Selkirk rex/Canadian hairless/Devon rex",

            'pinkdilute' : "Pink-eyed dilution",
            "ext" : {
                'ec': 'Carnelian',
                'er' : 'Russet',
                'ea' : 'Amber'
            },
            "corin" : {
                'sh' : 'Sunshine',
                'sg' : 'Extreme sunshine',
                'fg' : 'Flaxen gold'},
            "karp" : 'Karpati',
            "bleach" : 'Bleaching',
            "ghosting" : 'Ghosting',

            'eumelanin' : {'b' : 'Chocolate', 'bl' : 'Cinnamon'},
            'sexgene' : {
                'O': 'Red',
                'o' : 'Black'
            },
            "dilute" : 'Dilution',
            "white" : {'W' : 'Dominant white', 'wsal' : 'Salmiak'},
            "pointgene" : {'cb' : 'Sepia', 'cs' : 'Colorpoint', 'cm' : 'Mocha', 'c' : 'Albino'},
            "silver" : "Inhibitor",
            "agouti" : "Solid"
        }

        converted_name = alleles[self.somatic['gene']]
        try:
            converted_name = converted_name.get(self.somatic['allele'])
        except:
            pass

        return "\n" + str(converted_name) + " gene mutated to \"" + str(self.somatic['allele']) + "\" on " + str(body.get(self.somatic['base']))






import pygame

import os

import ujson

from scripts.game_structure.game_essentials import game

class Sprites():
    cat_tints = {}
    white_patches_tints = {}

    def __init__(self, size=None):
        """Class that handles and hold all spritesheets. 
        Size is normall automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None
        
        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading White Patches Tints")
            
    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7):  # pos = ex. (2, 3), no single pixels
        """
        Divide sprites on a sprite-sheet into groups of sprites that are easily accessible.

        Parameters:
        spritesheet -- Name of spritesheet.
        pos -- (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites.
        name -- Name of group to make.
        
        Keyword Arguments
        sprites_x -- Number of sprites horizontally (default: 3)
        sprites_y -- Number of sprites vertically (default: 3)
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )
                except ValueError:
                    # Fallback for non-existent sprites
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite
                self.sprites[f'{name}{i}'] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50 # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and do a search for 'if width / 3 == height / 7:'")

        del width, height # unneeded

        for x in [
            'lineart', 'whitepatches', 'minkstorties', 'minkswhite', 'scars', 'missingscars', 'collars', 'bellcollars',
            'bowcollars', 'nyloncollars', 'shadersnewwhite', 'lineartdead', 'tortiepatchesmasks', 'medcatherbs',
            'lineartdf', 'lightingnew', 'fademask', 'fadestarclan', 'fadedarkforest',

            'flower_accessories', 'plant2_accessories', 'snake_accessories', 'smallAnimal_accessories',
            'deadInsect_accessories', 'aliveInsect_accessories', 'fruit_accessories', 'crafted_accessories',
            'tail2_accessories',
            
            'disabilityscars', 'disabilityaccs'

        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        for x in os.listdir("sprites/genemod/borders"):
            sprites.spritesheet("sprites/genemod/borders/"+x, 'genemod/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/Base Colours"):
            sprites.spritesheet("sprites/genemod/Base Colours/"+x, 'base/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/points"):
            sprites.spritesheet("sprites/genemod/points/"+x, x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/Tabby Bases"):
            sprites.spritesheet("sprites/genemod/Tabby Bases/"+x, 'Tabby/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/extra"):
            sprites.spritesheet("sprites/genemod/extra/"+x, 'Other/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/effects"):
            sprites.spritesheet("sprites/genemod/effects/"+x, 'Other/'+x.replace('.png', ""))
        
        
        for x in os.listdir("sprites/genemod/white"):
            sprites.spritesheet("sprites/genemod/white/"+x, 'White/'+x.replace('.png', ""))
            self.make_group('White/'+x.replace('.png', ""), (0, 0), x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/break white"):
            sprites.spritesheet("sprites/genemod/break white/"+x, 'Break/'+x.replace('.png', ""))
            self.make_group('Break/'+x.replace('.png', ""), (0, 0), 'break/'+x.replace('.png', ""))

        # ...idk what to call these

        self.make_group('genemod/normal border', (0, 0), 'normbord')
        self.make_group('genemod/foldborder', (0, 0), 'foldbord')
        self.make_group('genemod/curlborder', (0, 0), 'curlbord')
        self.make_group('genemod/foldlineart', (0, 0), 'foldlines')
        self.make_group('genemod/fold_curllineart', (0, 0), 'fold_curllines')
        self.make_group('genemod/curllineart', (0, 0), 'curllines')
        self.make_group('genemod/foldlineartdf', (0, 0), 'foldlineartdf')
        self.make_group('genemod/fold_curllineartdf', (0, 0), 'fold_curllineartdf')
        self.make_group('genemod/curllineartdf', (0, 0), 'curllineartdf')
        self.make_group('genemod/foldlineartdead', (0, 0), 'foldlineartdead')
        self.make_group('genemod/fold_curllineartdead', (0, 0), 'fold_curllineartdead')
        self.make_group('genemod/curllineartdead', (0, 0), 'curllineartdead')

        self.make_group('genemod/isolateears', (0, 0), 'isolateears')
        self.make_group('genemod/noears', (0, 0), 'noears')
        
        self.make_group('genemod/rexlines', (0, 0), 'rexlineart')
        self.make_group('genemod/rexlinesdead', (0, 0), 'rexlineartdead')
        self.make_group('genemod/rexlinesdf', (0, 0), 'rexlineartdf')
        self.make_group('genemod/rexborder', (0, 0), 'rexbord')

        for a, x in enumerate(range(1, 6)):
            self.make_group('genemod/bobtails', (a, 0), f'bobtail{x}')

        # genemod base colours

        self.make_group('base/bases', (0, 0), 'basecolours', sprites_x=6, sprites_y=4)
        self.make_group('base/lightbases', (0, 0), 'lightbasecolours', sprites_x=4, sprites_y=1)

        # genemod tabby bases

        for x in ["black", "blue", "dove", "platinum",
                  "chocolate", "lilac", "champagne", "lavender",
                  "cinnamon", "fawn", "buff", "beige",
                  "red", "unders_red", "cream", "unders_cream", "honey", "unders_honey", "ivory", "unders_ivory"]:
            for a, i in enumerate(['rufousedlow', 'rufousedmedium', 'rufousedhigh', 'rufousedshaded', 'rufousedchinchilla']):
                self.make_group('Tabby/'+x, (a, 0), f'{x}{i}')
            for a, i in enumerate(['mediumlow', 'mediummedium', 'mediumhigh', 'mediumshaded', 'mediumchinchilla']):
                self.make_group('Tabby/'+x, (a, 1), f'{x}{i}')
            for a, i in enumerate(['lowlow', 'lowmedium', 'lowhigh', 'lowshaded', 'lowchinchilla']):
                self.make_group('Tabby/'+x, (a, 2), f'{x}{i}')
            for a, i in enumerate(['silverlow', 'silvermedium', 'silverhigh', 'silvershaded', 'silverchinchilla']):
                self.make_group('Tabby/'+x, (a, 3), f'{x}{i}')
        for a, x in enumerate(['low', 'medium', 'high', 'shaded', 'chinchilla']):
            self.make_group('Tabby/shading', (a, 0), f'{x}shading')

        # genemod tabby patterns

        for a, i in enumerate(['mackerel', 'brokenmack', 'spotted', 'classic', 'fullbar']):
            self.make_group('Other/tabbypatterns', (a, 0), f'{i}')
        for a, i in enumerate(['braided', 'brokenbraid', 'rosetted', 'marbled', 'redbar']):
            self.make_group('Other/tabbypatterns', (a, 1), f'{i}')
        for a, i in enumerate(['pinstripe', 'brokenpins', 'servaline', 'fullbarc', 'agouti']):
            self.make_group('Other/tabbypatterns', (a, 2), f'{i}')
        for a, i in enumerate(['pinsbraided', 'brokenpinsbraid', 'leopard', 'redbarc', 'charcoal']):
            self.make_group('Other/tabbypatterns', (a, 3), f'{i}')
        
        #genemod point markings

        self.make_group('points_spring', (0, 0), 'pointsm')
        self.make_group('points_summer', (0, 0), 'pointsl')
        self.make_group('points_winter', (0, 0), 'pointsd')
        self.make_group('mocha_spring', (0, 0), 'mocham')
        self.make_group('mocha_summer', (0, 0), 'mochal')
        self.make_group('mocha_winter', (0, 0), 'mochad')

        #genemod karpati
        for a, x in enumerate(['hetkarpatiwinter', 'hetkarpatispring', 'hetkarpatisummer']):
            self.make_group('Other/karpati', (a, 0), x)
        for a, x in enumerate(['homokarpatiwinter', 'homokarpatispring', 'homokarpatisummer']):
            self.make_group('Other/karpati', (a, 1), x)

        #genemod effects
        self.make_group('Other/bimetal', (0, 0), 'bimetal')
        self.make_group('Other/ghosting', (0, 0), 'ghost')
        self.make_group('Other/tabbyghost', (0, 0), 'tabbyghost')
        self.make_group('Other/grizzle', (0, 0), 'grizzle')
        self.make_group('Other/smoke', (0, 0), 'smoke')
        self.make_group('Other/bleach', (0, 0), 'bleach')
        self.make_group('Other/lykoi', (0, 0), 'lykoi')
        self.make_group('Other/hairless', (0, 0), 'hairless')
        self.make_group('Other/donskoy', (0, 0), 'donskoy')
        self.make_group('Other/furpoint', (0, 0), 'furpoint')
        self.make_group('Other/caramel', (0, 0), 'caramel', 1, 1)
        self.make_group('Other/satin', (0, 0), 'satin', 1, 1)
        self.make_group('Other/salmiak', (0, 0), 'salmiak')


        #genemod extra
        self.make_group('Other/ears', (0, 0), 'ears')
        self.make_group('Other/albino_skin', (0, 0), 'albino')
        self.make_group('Other/noses', (0, 0), 'nose')
        self.make_group('Other/nose_colours', (0, 0), 'nosecolours', sprites_y=5)
        self.make_group('Other/paw_pads', (0, 0), 'pads')

        #genemod eyes

        for i, x in enumerate(['left', 'right', 'sectoral1', 'sectoral2', 'sectoral3', 'sectoral4', 'sectoral5', 'sectoral6']):
            self.make_group('Other/eyebase', (i, 0), x, sprites_y=6)
        
        for b, x in enumerate(['P11', 'P10', 'P9', 'P8', 'P7', 'P6', 'P5', 'P4', 'P3', 'P2', 'P1', 'blue', 'albino']):
            for a, y in enumerate(range(1, 12)):
                self.make_group('Other/eyes_full', (a, b), f'R{y} ; {x}/', sprites_y=6)

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        # white patches
        for a, i in enumerate(['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO',
            'MOON', 'PHANTOM', 'POWDER', 'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE']):
            self.make_group('whitepatches', (a, 0), f'{i}')
        for a, i in enumerate(['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 
            'LIGHTSONG', 'VITILIGO', 'BLACKSTAR', 'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL']):
            self.make_group('whitepatches', (a, 1), f'{i}')
        # ryos white patches
        for a, i in enumerate(['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO',
            'PAWS', 'MITAINE', 'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD']):
            self.make_group('whitepatches', (a, 2), f'{i}')
        for a, i in enumerate(['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY',
            'FAROFA', 'DAMIEN', 'MISTER', 'BELLY', 'TAILTIP', 'TOES', 'TOPCOVER']):
            self.make_group('whitepatches', (a, 3), f'{i}')
        for a, i in enumerate(
                ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW',
                'PANTS', 'REVERSEPANTS', 'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW']):
            self.make_group('whitepatches', (a, 4), f'{i}')
        # beejeans white patches + perrio's point marks, painted, and heart2 + anju's new marks + key's blackstar
        for a, i in enumerate(['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT',
            'MAO', 'LUNA', 'CHESTSPECK', 'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER']):
            self.make_group('whitepatches', (a, 5), f'{i}')
        # acorn's white patches + ryos' bub + fable lovebug + frankie trixie
        for a, i in enumerate(['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART',
            'SPARROW', 'VEST', 'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE']):
            self.make_group('whitepatches', (a, 6), f'{i}')
        # acorn's white patches: the sequel
        for a, i in enumerate(['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE',
            'FADEBELLY', 'FRONT', 'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS']):
            self.make_group('whitepatches', (a, 7), f'{i}')
        for a, i in enumerate(['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR',
            'BUSTER', 'SMOKEY', 'HAWKBLAZE', 'CAKE', 'ROSINA', 'PRINCESS']):
            self.make_group('whitepatches', (a, 8), f'{i}')
        for a, i in enumerate(['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']):
            self.make_group('whitepatches', (a, 9), i)

                                # minks white patches
        for a, i in enumerate(['MINKONE', 'MINKTWO', 'MINKTHREE', 'MINKFOUR', 'MINKREDTAIL', 'MINKDELILAH', 'MINKHALF', 'MINKSTREAK', 'MINKMASK', 'MINKSMOKE']):
            self.make_group('minkswhite', (a, 0), f'{i}')
        for a, i in enumerate(['MINKMINIMALONE', 'MINKMINIMALTWO', 'MINKMINIMALTHREE', 'MINKMINIMALFOUR', 'MINKOREO', 'MINKSWOOP', 'MINKCHIMERA', 'MINKCHEST', 'MINKARMTAIL', 'MINKGRUMPYFACE']):
            self.make_group('minkswhite', (a, 1), f'{i}')
        for a, i in enumerate(['MINKMOTTLED', 'MINKSIDEMASK', 'MINKEYEDOT', 'MINKBANDANA', 'MINKPACMAN', 'MINKSTREAMSTRIKE', 'MINKSMUDGED', 'MINKDAUB', 'MINKEMBER', 'MINKBRIE']):
            self.make_group('minkswhite', (a, 2), f'{i}')
        for a, i in enumerate(['MINKORIOLE', 'MINKROBIN', 'MINKBRINDLE', 'MINKPAIGE', 'MINKROSETAIL', 'MINKSAFI', 'MINKDAPPLENIGHT', 'MINKBLANKET', 'MINKBELOVED', 'MINKBODY']):
            self.make_group('minkswhite', (a, 3), f'{i}')
        for a, i in enumerate(['MINKSHILOH', 'MINKFRECKLED', 'MINKHEARTBEAT']):
            self.make_group('minkswhite', (a, 4), f'{i}')
            
        # new new torties
        for a, i in enumerate(['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE']):
            self.make_group('tortiepatchesmasks', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL', 'GRUMPYFACE']):
            self.make_group('tortiepatchesmasks', (a, 1), f"tortiemask{i}")
        for a, i in enumerate(['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE']):
            self.make_group('tortiepatchesmasks', (a, 2), f"tortiemask{i}")
        for a, i in enumerate(['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY']):
            self.make_group('tortiepatchesmasks', (a, 3), f"tortiemask{i}")
        for a, i in enumerate(['SHILOH', 'FRECKLED', 'HEARTBEAT']):
            self.make_group('tortiepatchesmasks', (a, 4), f"tortiemask{i}")

        for a, i in enumerate(['MINKFULLWHITE', 'MINKANY', 'MINKTUXEDO', 'MINKLITTLE', 'MINKCOLOURPOINT', 'MINKVAN', 'MINKANYTWO',
            'MINKMOON', 'MINKPHANTOM', 'MINKPOWDER', 'MINKBLEACHED', 'MINKSAVANNAH', 'MINKFADESPOTS', 'MINKPEBBLESHINE']):
            self.make_group('minkstorties', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['MINKEXTRA', 'MINKONEEAR', 'MINKBROKEN', 'MINKLIGHTTUXEDO', 'MINKBUZZARDFANG', 'MINKRAGDOLL',
            'MINKLIGHTSONG', 'MINKVITILIGO', 'MINKBLACKSTAR', 'MINKPIEBALD', 'MINKCURVED', 'MINKPETAL', 'MINKSHIBAINU', 'MINKOWL']):
            self.make_group('minkstorties', (a, 1), f"tortiemask{i}")
        for a, i in enumerate(['MINKTIP', 'MINKFANCY', 'MINKFRECKLES', 'MINKRINGTAIL', 'MINKHALFFACE', 'MINKPANTSTWO', 'MINKGOATEE', 'MINKVITILIGOTWO',
            'MINKPAWS', 'MINKMITAINE', 'MINKBROKENBLAZE', 'MINKSCOURGE', 'MINKDIVA', 'MINKBEARD']):
            self.make_group('minkstorties', (a, 2), f"tortiemask{i}")
        for a, i in enumerate(['MINKTAIL', 'MINKBLAZE', 'MINKPRINCE', 'MINKBIB', 'MINKVEE', 'MINKUNDERS', 'MINKHONEY',
            'MINKFAROFA', 'MINKDAMIEN', 'MINKMISTER', 'MINKBELLY', 'MINKTAILTIP', 'MINKTOES', 'MINKTOPCOVER']):
            self.make_group('minkstorties', (a, 3), f'tortiemask{i}')
        for a, i in enumerate(['MINKAPRON', 'MINKCAPSADDLE', 'MINKMASKMANTLE', 'MINKSQUEAKS', 'MINKSTAR', 'MINKTOESTAIL', 'MINKRAVENPAW',
                'MINKPANTS', 'MINKREVERSEPANTS', 'MINKSKUNK', 'MINKKARPATI', 'MINKHALFWHITE', 'MINKAPPALOOSA', 'MINKDAPPLEPAW']):
            self.make_group('minkstorties', (a, 4), f'tortiemask{i}')
        for a, i in enumerate(['MINKHEART', 'MINKLILTWO', 'MINKGLASS', 'MINKMOORISH', 'MINKSEPIAPOINT', 'MINKMINKPOINT', 'MINKSEALPOINT',
            'MINKMAO', 'MINKLUNA', 'MINKCHESTSPECK', 'MINKWINGS', 'MINKPAINTED', 'MINKHEARTTWO', 'MINKWOODPECKER']):
            self.make_group('minkstorties', (a, 5), f'tortiemask{i}')
        for a, i in enumerate(['MINKBOOTS', 'MINKMISS', 'MINKCOW', 'MINKCOWTWO', 'MINKBUB', 'MINKBOWTIE', 'MINKMUSTACHE', 'MINKREVERSEHEART',
            'MINKSPARROW', 'MINKVEST', 'MINKLOVEBUG', 'MINKTRIXIE', 'MINKSAMMY', 'MINKSPARKLE']):
            self.make_group('minkstorties', (a, 6), f'tortiemask{i}')
        for a, i in enumerate(['MINKRIGHTEAR', 'MINKLEFTEAR', 'MINKESTRELLA', 'MINKSHOOTINGSTAR', 'MINKEYESPOT', 'MINKREVERSEEYE',
            'MINKFADEBELLY', 'MINKFRONT', 'MINKBLOSSOMSTEP', 'MINKPEBBLE', 'MINKTAILTWO', 'MINKBUDDY', 'MINKBACKSPOT', 'MINKEYEBAGS']):
            self.make_group('minkstorties', (a, 7), f'tortiemask{i}')
        for a, i in enumerate(['MINKBULLSEYE', 'MINKFINN', 'MINKDIGIT', 'MINKKROPKA', 'MINKFCTWO', 'MINKFCONE', 'MINKMIA', 'MINKSCAR',
            'MINKBUSTER', 'MINKSMOKEY', 'MINKHAWKBLAZE', 'MINKCAKE', 'MINKROSINA', 'MINKPRINCESS']):
            self.make_group('minkstorties', (a, 8), f'tortiemask{i}')
        for a, i in enumerate(['MINKLOCKET', 'MINKBLAZEMASK', 'MINKTEARS', 'MINKDOUGIE']):
            self.make_group('minkstorties', (a, 9), 'tortiemask' + i)

        self.make_group('Other/blue-tipped', (0, 0), 'tortiemaskBLUE-TIPPED')

        self.load_scars()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """
        for a, i in enumerate(
                ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL",
                 "BRIDGE", "RIGHTBLIND", "LEFTBLIND", "BOTHBLIND", "BURNPAWS", "BURNTAIL"]):
            self.make_group('scars', (a, 0), f'scars{i}')
        for a, i in enumerate(
                ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE",
                 "FROSTFACE", "FROSTTAIL", "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"]):
            self.make_group('scars', (a, 1), f'scars{i}')
        for a, i in enumerate(
                ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE",
                 "LEGBITE", "NECKBITE", "FACE"]):
            self.make_group('scars', (a, 2), f'scars{i}')
        for a, i in enumerate(
                ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]):
            self.make_group('scars', (a, 3), f'scars{i}')

        # disability mod related
        for a, i in enumerate(
                ["RASH", "DECLAWED"]):
            self.make_group('disabilityscars', (a, 0), f'scars{i}')

        # missing parts
        for a, i in enumerate(
                ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]):
            self.make_group('missingscars', (a, 0), f'scars{i}')

            # Accessories
        for a, i in enumerate([
            "MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL"]):
            self.make_group('medcatherbs', (a, 0), f'acc_herbs{i}')
        for a, i in enumerate([
            "BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS"]):
            self.make_group('medcatherbs', (a, 1), f'acc_herbs{i}')
        for a, i in enumerate([
            "OAK LEAVES", "CATMINT", "MAPLE SEED", "JUNIPER"]):
            self.make_group('medcatherbs', (a, 3), f'acc_herbs{i}')
        self.make_group('medcatherbs', (5, 2), 'acc_herbsDRY HERBS')

        for a, i in enumerate([
            "RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]):
            self.make_group('medcatherbs', (a, 2), f'acc_wild{i}')
        for a, i in enumerate(["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"]):
            self.make_group('collars', (a, 0), f'collars{i}')
        for a, i in enumerate(["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"]):
            self.make_group('collars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINK", "PURPLE", "MULTI", "INDIGO"]):
            self.make_group('collars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL",
            "LIMEBELL"
        ]):
            self.make_group('bellcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"]):
            self.make_group('bellcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]):
            self.make_group('bellcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW",
            "LIMEBOW"
        ]):
            self.make_group('bowcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"]):
            self.make_group('bowcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]):
            self.make_group('bowcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON",
            "LIMENYLON"
        ]):
            self.make_group('nyloncollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"]):
            self.make_group('nyloncollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]):
            self.make_group('nyloncollars', (a, 2), f'collars{i}')

        # ohdan's accessories
        for a, i in enumerate([
            "DAISY", "DIANTHUS", "BLEEDING HEARTS", "FRANGIPANI", "BLUE GLORY", "CATNIP FLOWER", "BLANKET FLOWER", "ALLIUM", "LACELEAF", "PURPLE GLORY"]):
            self.make_group('flower_accessories', (a, 0), f'acc_flower{i}')
        for a, i in enumerate([
            "YELLOW PRIMROSE", "HESPERIS", "MARIGOLD", "WISTERIA"]):
            self.make_group('flower_accessories', (a, 1), f'acc_flower{i}')

        for a, i in enumerate([
            "CLOVER", "STICK", "PUMPKIN", "MOSS", "IVY", "ACORN", "MOSS PELT", "REEDS", "BAMBOO"]):
            self.make_group('plant2_accessories', (a, 0), f'acc_plant2{i}')

        for a, i in enumerate([
            "GRASS SNAKE", "BLUE RACER", "WESTERN COACHWHIP", "KINGSNAKE"]):
            self.make_group('snake_accessories', (a, 0), f'acc_snake{i}')

        for a, i in enumerate([
            "GRAY SQUIRREL", "RED SQUIRREL", "CRAB", "WHITE RABBIT", "BLACK RABBIT", "BROWN RABBIT", "INDIAN GIANT SQUIRREL", "FAWN RABBIT", "BROWN AND WHITE RABBIT", "BLACK AND WHITE RABBIT"]):
            self.make_group('smallAnimal_accessories', (a, 0), f'acc_smallAnimal{i}')
        for a, i in enumerate([
            "WHITE AND FAWN RABBIT", "BLACK VITILIGO RABBIT", "BROWN VITILIGO RABBIT", "FAWN VITILIGO RABBIT", "BLACKBIRD", "ROBIN", "JAY", "THRUSH", "CARDINAL", "MAGPIE"]):
            self.make_group('smallAnimal_accessories', (a, 1), f'acc_smallAnimal{i}')
        for a, i in enumerate([
            "CUBAN TROGON", "TAN RABBIT", "TAN AND WHITE RABBIT", "TAN VITILIGO RABBIT", "RAT", "WHITE MOUSE", "BLACK MOUSE", "GRAY MOUSE", "BROWN MOUSE", "GRAY RABBIT"]):
            self.make_group('smallAnimal_accessories', (a, 2), f'acc_smallAnimal{i}')
        for a, i in enumerate([
            "GRAY AND WHITE RABBIT", "GRAY VITILIGO RABBIT"]):
            self.make_group('smallAnimal_accessories', (a, 3), f'acc_smallAnimal{i}')

        for a, i in enumerate([
            "LUNAR MOTH", "ROSY MAPLE MOTH", "MONARCH BUTTERFLY", "DAPPLED MONARCH", "POLYPHEMUS MOTH", "MINT MOTH"]):
            self.make_group('deadInsect_accessories', (a, 0), f'acc_deadInsect{i}')

        for a, i in enumerate([
            "BROWN SNAIL", "RED SNAIL", "WORM", "BLUE SNAIL", "ZEBRA ISOPOD", "DUCKY ISOPOD", "DAIRY COW ISOPOD", "BEETLEJUICE ISOPOD", "BEE", "RED LADYBUG"]):
            self.make_group('aliveInsect_accessories', (a, 0), f'acc_aliveInsect{i}')
        for a, i in enumerate([
            "ORANGE LADYBUG", "YELLOW LADYBUG"]):
            self.make_group('aliveInsect_accessories', (a, 1), f'acc_aliveInsect{i}')

        for a, i in enumerate([
            "RASPBERRY", "BLACKBERRY", "GOLDEN RASPBERRY", "CHERRY", "YEW"]):
            self.make_group('fruit_accessories', (a, 0), f'acc_fruit{i}')

        for a, i in enumerate([
            "WILLOWBARK BAG", "CLAY DAISY POT", "CLAY AMANITA POT", "CLAY BROWNCAP POT", "BIRD SKULL", "LEAF BOW"]):
            self.make_group('crafted_accessories', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "SEAWEED", "DAISY CORSAGE"]):
            self.make_group('tail2_accessories', (a, 0), f'acc_tail2{i}')

        # dismod accessories
        for a, i in enumerate(["BALL", "MOUSE", "MOSSBLANKIE", "BONE"]):
            self.make_group('disabilityaccs', (a, 0), f'acc_dismod{i}')
        for a, i in enumerate(["AUTISMFLAG", "DISFLAG", "ZEBFLAG"]):
            self.make_group('disabilityaccs', (a, 1), f'acc_dismod{i}')

# CREATE INSTANCE
sprites = Sprites()

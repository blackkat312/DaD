import random

from scripts.cat.history import History
from scripts.conditions import get_amount_cat_for_one_medic, medical_cats_condition_fulfilled
from scripts.game_structure.game_essentials import game


# ---------------------------------------------------------------------------- #
#                              Scar Event Class                                #
# ---------------------------------------------------------------------------- #

class Scar_Events():
    """All events with a connection to conditions."""

    # scar pools
    bite_scars = [
        "CATBITE", "CATBITETWO"
    ]
    rat_scars = [
        "RATBITE", "TOE"
    ]
    beak_scars = [
        "BEAKCHEEK", "BEAKLOWER", "BEAKSIDE"
    ]
    canid_scars = [
        "LEGBITE", "NECKBITE", "TAILSCAR", "BRIGHTHEART"
    ]
    snake_scars = [
        "SNAKE", "SNAKETWO"
    ]
    claw_scars = [
        "ONE", "TWO", "SNOUT", "TAILSCAR", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "FACE", "BRIDGE", "HINDLEG",
        "BACK", "SCRATCHSIDE", "QUILLSCRATCH", "LEFTEAR", "RIGHTEAR", "FOUR", "BEAKSIDE", "QUILLSIDE"
    ]
    face_claw_scars = [
        "QUILLSCRATCH", "SNOUT", "CHEEK", "FACE", "BRIDGE"
    ]
    leg_scars = [
        "NOPAW", "TOETRAP", "MANLEG", "FOUR"
    ]
    tail_scars = [
        "TAILSCAR", "TAILBASE", "NOTAIL", "HALFTAIL", "MANTAIL"
    ]
    ear_scars = [
        "LEFTEAR", "RIGHTEAR", 'NOLEFTEAR', 'NORIGHTEAR'
    ]
    frostbite_scars = [
        "HALFTAIL", "NOTAIL", "NOPAW", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "FROSTFACE", "FROSTTAIL", "FROSTMITT",
        "FROSTSOCK",
    ]
    eye_scars = [
        "THREE", "RIGHTBLIND", "LEFTBLIND", "BOTHBLIND"
    ]
    burn_scars = [
        "BRIGHTHEART", "BURNPAWS", "BURNTAIL", "BURNBELLY", "BURNRUMP"
    ]
    quill_scars = [
        "QUILLCHUNK", "QUILLSCRATCH", "QUILLSIDE"
    ]
    head_scars = [
        "SNOUT", "CHEEK", "BRIDGE", "BEAKCHEEK"
    ]
    bone_scars = [
        "MANLEG", "TOETRAP", "FOUR"
    ]
    back_scars = [
        "TWO", "TAILBASE", "BACK"
    ]
    rash_scars = [
        "RASH"
    ]
    declawed_scars = [
        "DECLAWED"
    ]
    torn_pelt_scars = [
        "ONE", "TWO", "SNOUT", "TAILSCAR", "CHEEK", "TAILBASE", "BELLY", "FACE", "BRIDGE", "HINDLEG", "BACK",
        "SCRATCHSIDE", "QUILLSCRATCH", "FOUR", "BEAKSIDE", "QUILLSIDE", "BEAKCHEEK", "BEAKLOWER"
    ]

    scar_allowed = {
        "bite-wound": canid_scars,
        "cat-bite": bite_scars,
        "severe burn": burn_scars,
        "rat bite": rat_scars,
        "snake bite": snake_scars,
        "mangled tail": tail_scars,
        "mangled leg": leg_scars,
        "torn ear": ear_scars,
        "frostbite": frostbite_scars,
        "torn pelt": torn_pelt_scars,
        "damaged eyes": eye_scars,
        "quilled by porcupine": quill_scars,
        "claw-wound": claw_scars,
        "beak bite": beak_scars,
        "broken jaw": head_scars,
        "broken back": back_scars,
        "broken bone": bone_scars,
        "rash": rash_scars,
        "wrenched claws": declawed_scars
    }

    @staticmethod
    def handle_scars(cat, injury_name):
        """ 
        This function handles the scars
        """

        # If the injury can't give a scar, move return None, None
        if injury_name not in Scar_Events.scar_allowed:
            return None, None

        moons_with = game.clan.age - cat.injuries[injury_name]["moon_start"]
        chance = max(5 - moons_with, 1)

        amount_per_med = get_amount_cat_for_one_medic(game.clan)
        if medical_cats_condition_fulfilled(game.cat_class.all_cats.values(), amount_per_med):
            chance += 2
        if injury_name == "wrenched claws":
            chance = random.randint(0, 25)

        # if len(cat.pelt.scars) < 7 and random.randint(1, 2) == 1:
        if len(cat.pelt.scars) < 7:

            # move potential scar text into displayed scar text

            scar_pool = [i for i in Scar_Events.scar_allowed[injury_name] if i not in cat.pelt.scars]
            if 'NOPAW' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ['TOETRAP', 'RATBITE', "FROSTSOCK"]]
            if 'NOTAIL' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if
                             i not in ["HALFTAIL", "TAILBASE", "TAILSCAR", "MANTAIL", "BURNTAIL", "FROSTTAIL"]]
            if 'HALFTAIL' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ["TAILSCAR", "MANTAIL", "FROSTTAIL"]]
            if "BRIGHTHEART" in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ["RIGHTBLIND", "BOTHBLIND"]]
            if 'BOTHBLIND' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if
                             i not in ["THREE", "RIGHTBLIND", "LEFTBLIND", "BOTHBLIND", "BRIGHTHEART"]]
            if 'NOEAR' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if
                             i not in ["LEFTEAR", "RIGHTEAR", 'NOLEFTEAR', 'NORIGHTEAR', "FROSTFACE"]]
            if 'MANTAIL' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ["BURNTAIL", 'FROSTTAIL']]
            if 'BURNTAIL' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ["MANTAIL", 'FROSTTAIL']]
            if 'FROSTTAIL' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ["MANTAIL", 'BURNTAIL']]
            if 'NOLEFT' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ['LEFTEAR']]
            if 'NORIGHT' in cat.pelt.scars:
                scar_pool = [i for i in scar_pool if i not in ['RIGHTEAR']]

            # Extra check for disabling scars.
            """if random.randint(1, 3) > 1:
                condition_scars = {
                    "LEGBITE", "THREE", "NOPAW", "TOETRAP", "NOTAIL", "HALFTAIL", "MANLEG", "BRIGHTHEART", "NOLEFTEAR",
                    "NORIGHTEAR", "NOEAR", "LEFTBLIND", "RIGHTBLIND", "BOTHBLIND", "RATBITE", "DECLAWED", "RASH",
                    "MANTAIL", "NECKBITE", "THROAT", "SIDE"
                }

                scar_pool = list(set(scar_pool).difference(condition_scars))"""

            # If there are no new scars to give them, return None, None.
            if not scar_pool:
                return None, None

            # If we've reached this point, we can move forward with giving history.
            History.add_scar(cat,
                             f"m_c was scarred from an injury ({injury_name}).",
                             condition=injury_name)

            specialty = [random.choice(scar_pool)]
            if (specialty == ["LEFTEAR"] or specialty == ["RIGHTEAR"]) and injury_name == "claw-wound":
                print("print")
                face_claw_scar_pool = [i for i in Scar_Events.face_claw_scars if i not in cat.pelt.scars]
                specialty.append(random.choice(face_claw_scar_pool))

            # combining left/right variations into the both version
            if "NOLEFTEAR" in cat.pelt.scars and "NORIGHTEAR" in specialty:
                cat.pelt.scars.remove("NOLEFTEAR")
                specialty.remove("NORIGHTEAR")
                specialty.append("NOEAR")
            elif "NORIGHTEAR" in cat.pelt.scars and "NOLEFTEAR" in specialty:
                cat.pelt.scars.remove("NORIGHTEAR")
                specialty.remove("NOLEFTEAR")
                specialty.append("NOEAR")

            if "LEFTBLIND" in cat.pelt.scars and "RIGHTBLIND" in specialty:
                cat.pelt.scars.remove("LEFTBLIND")
                specialty.remove("RIGHTBLIND")
                specialty.append("BOTHBLIND")
            elif "RIGHTBLIND" in cat.pelt.scars and "LEFTBLIND" in specialty:
                cat.pelt.scars.remove("RIGHTBLIND")
                specialty.remove("LEFTBLIND")
                specialty.append("BOTHBLIND")

            for entry in specialty:
                cat.pelt.scars.append(entry)

            scar_gain_string = random.choice([
                "m_c's " + injury_name + " has healed, but {PRONOUN/m_c/subject}'ll always carry evidence of the incident on {PRONOUN/m_c/poss} pelt.",
                "m_c healed from {PRONOUN/m_c/poss} " + injury_name + " but will forever be marked by a scar.",
                "m_c's " + injury_name + " has healed, but the injury left {PRONOUN/m_c/object} scarred.",
            ])
            return scar_gain_string, specialty
        else:
            return None, None

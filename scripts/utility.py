# pylint: disable=line-too-long
"""

TODO: Docs


"""  # pylint: enable=line-too-long

from random import choice, choices, randint, random, sample
import re
import pygame

from scripts.cat.phenotype import Phenotype
from scripts.cat.genotype import Genotype

import ujson
import logging
from sys import exit as sys_exit
from typing import Dict


logger = logging.getLogger(__name__)
from scripts.game_structure import image_cache
from scripts.cat.history import History
from scripts.cat.names import names
from scripts.cat.pelts import Pelt
from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game, screen_x, screen_y


# ---------------------------------------------------------------------------- #
#                              Counting Cats                                   #
# ---------------------------------------------------------------------------- #

def get_alive_clan_queens(living_cats):
    living_kits = [cat for cat in living_cats if not (cat.dead or cat.outside) and cat.status in ["kitten", "newborn"]]

    queen_dict = {}
    for cat in living_kits.copy():
        parents = cat.get_parents()
        #Fetch parent object, only alive and not outside. 
        parents = [cat.fetch_cat(i) for i in parents if cat.fetch_cat(i) and not(cat.fetch_cat(i).dead or cat.fetch_cat(i).outside)]
        if not parents:
            continue
        
        if len(parents) == 1 or len(parents) > 2 or\
            all(i.gender == "tom" for i in parents) or\
            parents[0].gender == "molly":
            if parents[0].ID in queen_dict:
                queen_dict[parents[0].ID].append(cat)
                living_kits.remove(cat)
            else:
                queen_dict[parents[0].ID] = [cat]
                living_kits.remove(cat)
        elif len(parents) == 2:
            if parents[1].ID in queen_dict:
                queen_dict[parents[1].ID].append(cat)
                living_kits.remove(cat)
            else:
                queen_dict[parents[1].ID] = [cat]
                living_kits.remove(cat)
    return queen_dict, living_kits

def get_alive_kits(Cat):
    """
    returns a list of IDs for all living kittens in the clan
    """
    alive_kits = [i for i in Cat.all_cats.values() if
                  i.age in ['kitten', 'newborn'] and not i.dead and not i.outside]

    return alive_kits


def get_med_cats(Cat, working=True):
    """
    returns a list of all meds and med apps currently alive, in the clan, and able to work

    set working to False if you want all meds and med apps regardless of their work status
    """
    all_cats = Cat.all_cats.values()
    possible_med_cats = [i for i in all_cats if
                         i.status in ['medicine cat apprentice', 'medicine cat'] and not (i.dead or i.outside)]

    if working:
        possible_med_cats = [i for i in possible_med_cats if not i.not_working()]

    # Sort the cats by age before returning
    possible_med_cats = sorted(possible_med_cats, key=lambda cat: cat.moons, reverse=True)

    return possible_med_cats


def get_living_cat_count(Cat):
    """
    TODO: DOCS
    """
    count = 0
    for the_cat in Cat.all_cats.values():
        if the_cat.dead:
            continue
        count += 1
    return count


def get_living_clan_cat_count(Cat):
    """
    TODO: DOCS
    """
    count = 0
    for the_cat in Cat.all_cats.values():
        if the_cat.dead or the_cat.exiled or the_cat.outside:
            continue
        count += 1
    return count


def get_cats_same_age(cat, range=10):  # pylint: disable=redefined-builtin
    """Look for all cats in the Clan and returns a list of cats, which are in the same age range as the given cat."""
    cats = []
    for inter_cat in cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        if inter_cat.moons <= cat.moons + range and inter_cat.moons <= cat.moons - range:
            cats.append(inter_cat)

    return cats


def get_free_possible_mates(cat):
    """Returns a list of available cats, which are possible mates for the given cat."""
    cats = []
    for inter_cat in cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        if inter_cat.is_potential_mate(cat, for_love_interest=True):
            cats.append(inter_cat)
    return cats


# ---------------------------------------------------------------------------- #
#                          Handling Outside Factors                            #
# ---------------------------------------------------------------------------- #
def get_current_season():
    """
    function to handle the math for finding the Clan's current season
    :return: the Clan's current season
    """

    if game.config['lock_season']:
        game.clan.current_season = game.clan.starting_season
        return game.clan.starting_season

    modifiers = {
        "Newleaf": 0,
        "Greenleaf": 3,
        "Leaf-fall": 6,
        "Leaf-bare": 9
    }
    if(not game.clan):
        return "Newleaf"
    else: 
        index = game.clan.age % 12 + modifiers[game.clan.starting_season]

        if index > 11:
            index = index - 12

        game.clan.current_season = game.clan.seasons[index]

        return game.clan.current_season

def change_clan_reputation(difference):
    """
    will change the Clan's reputation with outsider cats according to the difference parameter.
    """
    game.clan.reputation += difference


def change_clan_relations(other_clan, difference):
    """
    will change the Clan's relation with other clans according to the difference parameter.
    """
    # grab the clan that has been indicated
    other_clan = other_clan
    # grab the relation value for that clan
    y = game.clan.all_clans.index(other_clan)
    clan_relations = int(game.clan.all_clans[y].relations)
    # change the value
    clan_relations += difference
    # making sure it doesn't exceed the bounds
    if clan_relations > 30:
        clan_relations = 30
    elif clan_relations < 0:
        clan_relations = 0
    # setting it in the Clan save
    game.clan.all_clans[y].relations = clan_relations

def create_new_cat(Cat,
                   Relationship,
                   new_name:bool=False,
                   loner:bool=False,
                   kittypet:bool=False,
                   kit:bool=False,
                   litter:bool=False,
                   other_clan:bool=None,
                   backstory:bool=None,
                   status:str=None,
                   age:int=None,
                   gender:str=None,
                   thought:str='Is looking around the camp with wonder',
                   alive:bool=True,
                   outside:bool=False,
                   parent1:str=None,
                   parent2:str=None,
                   extrapar:Genotype=None,
                   adoptive_parent:list=None
    ) -> list:
    """
    This function creates new cats and then returns a list of those cats
    :param Cat: pass the Cat class
    :params Relationship: pass the Relationship class
    :param new_name: set True if cat(s) is a loner/rogue receiving a new Clan name - default: False
    :param loner: set True if cat(s) is a loner or rogue - default: False
    :param kittypet: set True if cat(s) is a kittypet - default: False
    :param kit: set True if the cat is a lone kitten - default: False
    :param litter: set True if a litter of kittens needs to be generated - default: False
    :param other_clan: if new cat(s) are from a neighboring clan, set true
    :param backstory: a list of possible backstories.json for the new cat(s) - default: None
    :param status: set as the rank you want the new cat to have - default: None (will cause a random status to be picked)
    :param age: set the age of the new cat(s) - default: None (will be random or if kit/litter is true, will be kitten.
    :param gender: set the gender (BIRTH SEX) of the cat - default: None (will be random)
    :param thought: if you need to give a custom "welcome" thought, set it here
    :param alive: set this as False to generate the cat as already dead - default: True (alive)
    :param outside: set this as True to generate the cat as an outsider instead of as part of the Clan - default: False (Clan cat)
    :param parent1: Cat ID to set as the biological parent1
    :param parent2: Cat ID object to set as the biological parert2
    """
    accessory = None
    if isinstance(backstory, list):
        backstory = choice(backstory)

    if backstory in (
            BACKSTORIES["backstory_categories"]["former_clancat_backstories"] or BACKSTORIES["backstory_categories"]["otherclan_categories"]):
        other_clan = True

    created_cats = []

    if not litter:
        number_of_cats = 1
    else:
        number_of_cats = choices([2, 3, 4, 5], [5, 4, 1, 1], k=1)[0]
    
    
    if not isinstance(age, int):
        if status == "newborn":
            age = 0
        elif litter or kit:
            age = randint(1, 5)
        elif status in ('apprentice', 'medicine cat apprentice', 'mediator apprentice'):
            age = randint(6, 11)
        elif status == 'warrior':
            age = randint(23, 120)
        elif status == 'medicine cat':
            age = randint(23, 140)
        elif status == 'elder':
            age = randint(120, 130)
        else:
            age = randint(6, 120)
    
    # setting status
    if not status:
        if age == 0:
            status = "newborn"
        elif age < 6:
            status = "kitten"
        elif 6 <= age <= 11:
            status = "apprentice"
        elif age >= 12:
            status = "warrior"
        elif age >= 120:
            status = 'elder'

    # cat creation and naming time
    for index in range(number_of_cats):
        # setting gender
        if not gender:
            _gender = choice(['fem', 'masc'])
        else:
            _gender = gender

        # other Clan cats, apps, and kittens (kittens and apps get indoctrinated lmao no old names for them)
        if other_clan or kit or litter or age < 12 and not (loner or kittypet):
            new_cat = Cat(moons=age,
                          status=status,
                          gender=_gender,
                          backstory=backstory,
                          parent1=parent1,
                          parent2=parent2,
                          extrapar=extrapar)
            if adoptive_parent:
                new_cat.adoptive_parents = [adoptive_parent]
        else:
            # grab starting names and accs for loners/kittypets
            if kittypet:
                name = choice(names.names_dict["loner_names"])
                if choice([1, 2]) == 1:
                    accessory = choice(Pelt.collars)
            elif loner and choice([1, 2]) == 1:  # try to give name from full loner name list
                name = choice(names.names_dict["loner_names"])
            else:
                name = choice(
                    names.names_dict["normal_prefixes"])  # otherwise give name from prefix list (more nature-y names)

            # now we make the cats
            if new_name:  # these cats get new names
                if choice([1, 2]) == 1:  # adding suffix to OG name
                    spaces = name.count(" ")
                    if spaces > 0:
                        # make a list of the words within the name, then add the OG name back in the list
                        words = name.split(" ")
                        words.append(name)
                        new_prefix = choice(words)  # pick new prefix from that list
                        name = new_prefix
                    new_cat = Cat(moons=age,
                                  prefix=name,
                                  status=status,
                                  gender=_gender,
                                  backstory=backstory,
                                  parent1=parent1,
                                  parent2=parent2,
                                  kittypet=kittypet)
                else:  # completely new name
                    new_cat = Cat(moons=age,
                                  status=status,
                                  gender=_gender,
                                  backstory=backstory,
                                  parent1=parent1,
                                  parent2=parent2,
                                  kittypet=kittypet)
            # these cats keep their old names
            else:
                new_cat = Cat(moons=age,
                              prefix=name,
                              suffix="",
                              status=status,
                              gender=_gender,
                              backstory=backstory,
                              parent1=parent1,
                              parent2=parent2,
                              kittypet=kittypet)

        # give em a collar if they got one
        if accessory:
            new_cat.pelt.accessory = accessory

        # give apprentice aged cat a mentor
        if new_cat.age == 'adolescent':
            new_cat.update_mentor()

        # Remove disabling scars, if they generated.
        not_allowed = []
        for scar in new_cat.pelt.scars:
            if scar in not_allowed:
                new_cat.pelt.scars.remove(scar)

        # chance to give the new cat a permanent condition, higher chance for found kits and litters
        if game.clan.game_mode != 'classic':
            if kit or litter:
                chance = int(game.config["cat_generation"]["base_permanent_condition"] / 11.25)
            else:
                chance = game.config["cat_generation"]["base_permanent_condition"] + 10
            if not int(random() * chance):
                possible_conditions = []
                genetics_exclusive = ["excess testosterone", "aneuploidy", "testosterone deficiency", "chimerism",
                                      "mosaicism", "albinism", "ocular albinism", "manx syndrome"]
                for condition in PERMANENT:
                    if (kit or litter) and (PERMANENT[condition]['congenital'] not in ['always', 'sometimes']) or (condition in genetics_exclusive):
                        continue
                    # next part ensures that a kit won't get a condition that takes too long to reveal
                    age = new_cat.moons
                    leeway = 5 - (PERMANENT[condition]['moons_until'] + 1)
                    if age > leeway:
                        continue
                    possible_conditions.append(condition)
                    
                if possible_conditions:
                    chosen_condition = choice(possible_conditions)
                    born_with = False
                    if PERMANENT[chosen_condition]['congenital'] in ['always', 'sometimes']:
                        born_with = True

                    new_cat.get_permanent_condition(chosen_condition, born_with)

                    # assign scars
                    if chosen_condition in ['lost a leg', 'born without a leg'] and ('NOPAW') not in new_cat.pelt.scars:
                        new_cat.pelt.scars.append('NOPAW')
                    elif chosen_condition in ['lost their tail', 'born without a tail'] and ('NOTAIL') not in new_cat.pelt.scars:
                        new_cat.pelt.scars.append("NOTAIL")

        if outside:
            new_cat.outside = True
        if not alive:
            new_cat.die()

        # newbie thought
        new_cat.thought = thought

        # and they exist now
        created_cats.append(new_cat)
        game.clan.add_cat(new_cat)
        history = History()
        history.add_beginning(new_cat)

        # create relationships
        new_cat.create_relationships_new_cat()
        # Note - we always update inheritance after the cats are generated, to
        # allow us to add parents. 
        #new_cat.create_inheritance_new_cat() 

    return created_cats


def create_outside_cat(Cat, status, backstory, age=None, alive=True, thought=None, gender=None):
    """
        TODO: DOCS
        """
    suffix = ''
    if backstory in BACKSTORIES["backstory_categories"]["rogue_backstories"]:
        status = 'rogue'
    elif backstory in BACKSTORIES["backstory_categories"]["former_clancat_backstories"]:
        status = "former Clancat"
    if status == 'kittypet':
        name = choice(names.names_dict["loner_names"])
    elif status in ['loner', 'rogue']:
        name = choice(names.names_dict["loner_names"] +
                      names.names_dict["normal_prefixes"])
    elif status == 'former Clancat':
        name = choice(names.names_dict["normal_prefixes"])
        suffix = choice(names.names_dict["normal_suffixes"])
    else:
        name = choice(names.names_dict["loner_names"])
    new_cat = Cat(prefix=name,
                  suffix=suffix,
                  gender=gender,
                  status=status,
                  backstory=backstory,
                  kittypet=True if status == 'kittypet' else False)
    if status == 'kittypet':
        new_cat.pelt.accessory = choice(Pelt.collars)
    new_cat.outside = True

    if(age):
        new_cat.moons = age

    if not alive:
        new_cat.die()

    thought = "Wonders about those Clan cats they just met"
    new_cat.thought = thought

    # create relationships - only with outsiders
    # (this function will handle, that the cat only knows other outsiders)
    new_cat.create_relationships_new_cat()
    new_cat.create_inheritance_new_cat()

    game.clan.add_cat(new_cat)
    game.clan.add_to_outside(new_cat)
    name = str(name + suffix)

    #return new_cat
    return new_cat

# ---------------------------------------------------------------------------- #
#                             Cat Relationships                                #
# ---------------------------------------------------------------------------- #


def get_highest_romantic_relation(relationships, exclude_mate=False, potential_mate=False):
    """Returns the relationship with the highest romantic value."""
    max_love_value = 0
    current_max_relationship = None
    for rel in relationships:
        if rel.romantic_love < 0:
            continue
        if exclude_mate and rel.cat_from.ID in rel.cat_to.mate:
            continue
        if potential_mate and not rel.cat_to.is_potential_mate(rel.cat_from, for_love_interest=True):
            continue
        if rel.romantic_love > max_love_value:
            current_max_relationship = rel
            max_love_value = rel.romantic_love

    return current_max_relationship


def check_relationship_value(cat_from, cat_to, rel_value=None):
    """
    returns the value of the rel_value param given
    :param cat_from: the cat who is having the feelings
    :param cat_to: the cat that the feelings are directed towards
    :param rel_value: the relationship value that you're looking for,
    options are: romantic, platonic, dislike, admiration, comfortable, jealousy, trust
    """
    if cat_to.ID in cat_from.relationships:
        relationship = cat_from.relationships[cat_to.ID]
    else:
        relationship = cat_from.create_one_relationship(cat_to)

    if rel_value == "romantic":
        return relationship.romantic_love
    elif rel_value == "platonic":
        return relationship.platonic_like
    elif rel_value == "dislike":
        return relationship.dislike
    elif rel_value == "admiration":
        return relationship.admiration
    elif rel_value == "comfortable":
        return relationship.comfortable
    elif rel_value == "jealousy":
        return relationship.jealousy
    elif rel_value == "trust":
        return relationship.trust


def get_personality_compatibility(cat1, cat2):
    """Returns:
        True - if personalities have a positive compatibility
        False - if personalities have a negative compatibility
        None - if personalities have a neutral compatibility
    """
    personality1 = cat1.personality.trait
    personality2 = cat2.personality.trait

    if personality1 == personality2:
        if personality1 is None:
            return None
        return True

    lawfulness_diff = abs(cat1.personality.lawfulness - cat2.personality.lawfulness)
    sociability_diff = abs(cat1.personality.sociability - cat2.personality.sociability)
    aggression_diff = abs(cat1.personality.aggression - cat2.personality.aggression)
    stability_diff = abs(cat1.personality.stability - cat2.personality.stability)
    list_of_differences = [lawfulness_diff, sociability_diff, aggression_diff, stability_diff]

    running_total = 0
    for x in list_of_differences:
        if x <= 4:
            running_total += 1
        elif x >= 6:
            running_total -= 1

    if running_total >= 2:
        return True
    if running_total <= -2:
        return False

    return None


def get_cats_of_romantic_interest(cat):
    """Returns a list of cats, those cats are love interest of the given cat"""
    cats = []
    for inter_cat in cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue
        
        # Extra check to ensure they are potential mates
        if inter_cat.is_potential_mate(cat, for_love_interest=True) and cat.relationships[inter_cat.ID].romantic_love > 0:
            cats.append(inter_cat)
    return cats


def get_amount_of_cats_with_relation_value_towards(cat, value, all_cats):
    """
    Looks how many cats have the certain value 
    :param cat: cat in question
    :param value: value which has to be reached
    :param all_cats: list of cats which has to be checked
    """

    # collect all true or false if the value is reached for the cat or not
    # later count or sum can be used to get the amount of cats
    # this will be handled like this, because it is easier / shorter to check
    relation_dict = {
        "romantic_love": [],
        "platonic_like": [],
        "dislike": [],
        "admiration": [],
        "comfortable": [],
        "jealousy": [],
        "trust": []
    }

    for inter_cat in all_cats:
        if cat.ID in inter_cat.relationships:
            relation = inter_cat.relationships[cat.ID]
        else:
            continue

        relation_dict['romantic_love'].append(relation.romantic_love >= value)
        relation_dict['platonic_like'].append(relation.platonic_like >= value)
        relation_dict['dislike'].append(relation.dislike >= value)
        relation_dict['admiration'].append(relation.admiration >= value)
        relation_dict['comfortable'].append(relation.comfortable >= value)
        relation_dict['jealousy'].append(relation.jealousy >= value)
        relation_dict['trust'].append(relation.trust >= value)

    return_dict = {
        "romantic_love": sum(relation_dict['romantic_love']),
        "platonic_like": sum(relation_dict['platonic_like']),
        "dislike": sum(relation_dict['dislike']),
        "admiration": sum(relation_dict['admiration']),
        "comfortable": sum(relation_dict['comfortable']),
        "jealousy": sum(relation_dict['jealousy']),
        "trust": sum(relation_dict['trust'])
    }

    return return_dict


def change_relationship_values(cats_to: list,
                               cats_from: list,
                               romantic_love:int=0,
                               platonic_like:int=0,
                               dislike:int=0,
                               admiration:int=0,
                               comfortable:int=0,
                               jealousy:int=0,
                               trust:int=0,
                               auto_romance:bool=False,
                               log:str=None
                               ):
    """
    changes relationship values according to the parameters.

    cats_from - a list of cats for the cats whose rel values are being affected
    cats_to - a list of cat IDs for the cats who are the target of that rel value
            i.e. cats in cats_from lose respect towards the cats in cats_to
    auto_romance - if this is set to False (which is the default) then if the cat_from already has romantic value
            with cat_to then the platonic_like param value will also be used for the romantic_love param
            if you don't want this to happen, then set auto_romance to False
    log - string to add to relationship log. 

    use the relationship value params to indicate how much the values should change.
    
    This is just for test prints - DON'T DELETE - you can use this to test if relationships are changing
    changed = False
    if romantic_love == 0 and platonic_like == 0 and dislike == 0 and admiration == 0 and \
            comfortable == 0 and jealousy == 0 and trust == 0:
        changed = False
    else:
        changed = True"""

    # pick out the correct cats
    for single_cat_from in cats_from:
        for single_cat_to_ID in cats_to:
            single_cat_to = single_cat_from.fetch_cat(single_cat_to_ID)

            if single_cat_from == single_cat_to:
                continue
            
            if single_cat_to_ID not in single_cat_from.relationships:
                single_cat_from.create_one_relationship(single_cat_to)

            rel = single_cat_from.relationships[single_cat_to_ID]

            # here we just double-check that the cats are allowed to be romantic with each other
            if single_cat_from.is_potential_mate(single_cat_to, for_love_interest=True) or single_cat_to.ID in single_cat_from.mate:
                # if cat already has romantic feelings then automatically increase romantic feelings
                # when platonic feelings would increase
                if rel.romantic_love > 0 and auto_romance:
                    romantic_love = platonic_like

                # now gain the romance
                rel.romantic_love += romantic_love

            # gain other rel values
            rel.platonic_like += platonic_like
            rel.dislike += dislike
            rel.admiration += admiration
            rel.comfortable += comfortable
            rel.jealousy += jealousy
            rel.trust += trust

            '''# for testing purposes - DON'T DELETE - you can use this to test if relationships are changing
            print(str(kitty.name) + " gained relationship with " + str(rel.cat_to.name) + ": " +
                  "Romantic: " + str(romantic_love) +
                  " /Platonic: " + str(platonic_like) +
                  " /Dislike: " + str(dislike) +
                  " /Respect: " + str(admiration) +
                  " /Comfort: " + str(comfortable) +
                  " /Jealousy: " + str(jealousy) +
                  " /Trust: " + str(trust)) if changed else print("No relationship change")'''
                  
            if log and isinstance(log, str):
                rel.log.append(log)


# ---------------------------------------------------------------------------- #
#                               Text Adjust                                    #
# ---------------------------------------------------------------------------- #

def pronoun_repl(m, cat_pronouns_dict, raise_exception=False):
    """ Helper function for add_pronouns. If raise_exception is 
    False, any error in pronoun formatting will not raise an 
    exception, and will use a simple replacement "error" """
    
    # Add protection about the "insert" sometimes used
    if m.group(0) == "{insert}":
        return m.group(0)
    
    inner_details = m.group(1).split("/")
    
    try:
        d = cat_pronouns_dict[inner_details[1]][1]
        if inner_details[0].upper() == "PRONOUN":
            pro = d[inner_details[2]]
            if inner_details[-1] == "CAP":
                pro = pro.capitalize()
            return pro
        elif inner_details[0].upper() == "VERB":
            return inner_details[d["conju"] + 1]
        
        if raise_exception:
            raise KeyError(f"Pronoun tag: {m.group(1)} is not properly"
                           "indicated as a PRONOUN or VERB tag.")
        
        print("Failed to find pronoun:", m.group(1))
        return "error1"
    except (KeyError, IndexError) as e:
        if raise_exception:
            raise
        
        logger.exception("Failed to find pronoun: " + m.group(1))
        print("Failed to find pronoun:", m.group(1))
        return "error2"


def name_repl(m, cat_dict):
    ''' Name replacement '''
    return cat_dict[m.group(0)][0]


def process_text(text, cat_dict, raise_exception=False):
    """ Add the correct name and pronouns into a string. """
    adjust_text = re.sub(r"\{(.*?)\}", lambda x: pronoun_repl(x, cat_dict, raise_exception),
                                                              text)

    name_patterns = [r'(?<!\{)' + re.escape(l) + r'(?!\})' for l in cat_dict]
    adjust_text = re.sub("|".join(name_patterns), lambda x: name_repl(x, cat_dict), adjust_text)
    return adjust_text


def adjust_list_text(list_of_items):
    """
    returns the list in correct grammar format (i.e. item1, item2, item3 and item4)
    this works with any number of items
    :param list_of_items: the list of items you want converted
    :return: the new string
    """
    if len(list_of_items) == 1:
        insert = f"{list_of_items[0]}"
    elif len(list_of_items) == 2:
        insert = f"{list_of_items[0]} and {list_of_items[1]}"
    else:
        item_line = ", ".join(list_of_items[:-1])
        insert = f"{item_line}, and {list_of_items[-1]}"

    return insert


def adjust_prey_abbr(patrol_text):
    """
    checks for prey abbreviations and returns adjusted text
    """
    for abbr in PREY_LISTS["abbreviations"]:
        if abbr in patrol_text:
            chosen_list = PREY_LISTS["abbreviations"].get(abbr)
            chosen_list = PREY_LISTS[chosen_list]
            prey = choice(chosen_list)
            patrol_text = patrol_text.replace(abbr, prey)

    return patrol_text


def get_special_snippet_list(chosen_list, amount, sense_groups=None, return_string=True):
    """
    function to grab items from various lists in snippet_collections.json
    list options are:
    -prophecy_list - sense_groups = sight, sound, smell, emotional, touch
    -omen_list - sense_groups = sight, sound, smell, emotional, touch
    -clair_list  - sense_groups = sound, smell, emotional, touch, taste
    -dream_list (this list doesn't have sense_groups)
    -story_list (this list doesn't have sense_groups)
    :param chosen_list: pick which list you want to grab from
    :param amount: the amount of items you want the returned list to contain
    :param sense_groups: list which senses you want the snippets to correspond with:
     "touch", "sight", "emotional", "sound", "smell" are the options. Default is None, if left as this then all senses
     will be included (if the list doesn't have sense categories, then leave as None)
    :param return_string: if True then the function will format the snippet list with appropriate commas and 'ands'.
    This will work with any number of items. If set to True, then the function will return a string instead of a list.
    (i.e. ["hate", "fear", "dread"] becomes "hate, fear, and dread") - Default is True
    :return: a list of the chosen items from chosen_list or a formatted string if format is True
    """
    biome = game.clan.biome.casefold()

    # these lists don't get sense specific snippets, so is handled first
    if chosen_list in ["dream_list", "story_list"]:

        if chosen_list == 'story_list':  # story list has some biome specific things to collect
            snippets = SNIPPETS[chosen_list]['general']
            snippets.extend(SNIPPETS[chosen_list][biome])
        elif chosen_list == 'clair_list':  # the clair list also pulls from the dream list
            snippets = SNIPPETS[chosen_list]
            snippets.extend(SNIPPETS["dream_list"])
        else:  # the dream list just gets the one
            snippets = SNIPPETS[chosen_list]

    else:
        # if no sense groups were specified, use all of them
        if not sense_groups:
            if chosen_list == 'clair_list':
                sense_groups = ["taste", "sound", "smell", "emotional", "touch"]
            else:
                sense_groups = ["sight", "sound", "smell", "emotional", "touch"]

        # find the correct lists and compile them
        snippets = []
        for sense in sense_groups:
            snippet_group = SNIPPETS[chosen_list][sense]
            snippets.extend(snippet_group["general"])
            snippets.extend(snippet_group[biome])

    # now choose a unique snippet from each snip list
    unique_snippets = []
    for snip_list in snippets:
        unique_snippets.append(choice(snip_list))

    # pick out our final snippets
    final_snippets = sample(unique_snippets, k=amount)

    if return_string:
        text = adjust_list_text(final_snippets)
        return text
    else:
        return final_snippets


def find_special_list_types(text):
    """
    purely to identify which senses are being called for by a snippet abbreviation
    returns adjusted text, sense list, and list type
    """
    senses = []
    if "omen_list" in text:
        list_type = "omen_list"
    elif "prophecy_list" in text:
        list_type = "prophecy_list"
    elif "dream_list" in text:
        list_type = "dream_list"
    elif "clair_list" in text:
        list_type = "clair_list"
    elif "story_list" in text:
        list_type = "story_list"
    else:
        return text, None, None

    if "_sight" in text:
        senses.append("sight")
        text = text.replace("_sight", "")
    if "_sound" in text:
        senses.append("sound")
        text = text.replace("_sight", "")
    if "_smell" in text:
        text = text.replace("_smell", "")
        senses.append("smell")
    if "_emotional" in text:
        text = text.replace("_emotional", "")
        senses.append("emotional")
    if "_touch" in text:
        text = text.replace("_touch", "")
        senses.append("touch")
    if "_taste" in text:
        text = text.replace("_taste", "")
        senses.append("taste")

    return text, senses, list_type


def history_text_adjust(text,
                        other_clan_name,
                        clan,other_cat_rc=None):
    """
    we want to handle history text on its own because it needs to preserve the pronoun tags and cat abbreviations.
    this is so that future pronoun changes or name changes will continue to be reflected in history
    """
    if "o_c" in text:
        text = text.replace("o_c", other_clan_name)
    if "c_n" in text:
        text = text.replace("c_n", clan.name)
    if "r_c" in text and other_cat_rc:
        text = selective_replace(text, "r_c", str(other_cat_rc.name))
    return text

def selective_replace(text, pattern, replacement):
    i = 0
    while i < len(text):
        index = text.find(pattern, i)
        if index == -1:
            break
        start_brace = text.rfind('{', 0, index)
        end_brace = text.find('}', index)
        if start_brace != -1 and end_brace != -1 and start_brace < index < end_brace:
            i = index + len(pattern)
        else:
            text = text[:index] + replacement + text[index + len(pattern):]
            i = index + len(replacement)

    return text

def ongoing_event_text_adjust(Cat, text, clan=None, other_clan_name=None):
    """
    This function is for adjusting the text of ongoing events
    :param Cat: the cat class
    :param text: the text to be adjusted
    :param clan: the name of the clan
    :param other_clan_name: the other Clan's name if another Clan is involved
    """
    cat_dict = {}
    if "lead_name" in text:
        kitty = Cat.fetch_cat(game.clan.leader)
        cat_dict["lead_name"] = (str(kitty.name), choice(kitty.pronouns))
    if "dep_name" in text:
        kitty = Cat.fetch_cat(game.clan.deputy)
        cat_dict["dep_name"] = (str(kitty.name), choice(kitty.pronouns))
    if "med_name" in text:
        kitty = choice(get_med_cats(Cat, working=False))
        cat_dict["med_name"] = (str(kitty.name), choice(kitty.pronouns))

    if cat_dict:
        text = process_text(text, cat_dict)

    if other_clan_name:
        text = text.replace("o_c", other_clan_name)
    if clan:
        clan_name = str(clan.name)
    else:
        if game.clan is None:
            clan_name = game.switches["clan_list"][0]
        else:
            clan_name = str(game.clan.name)

    text = text.replace("c_n", clan_name + "Clan")

    return text


def event_text_adjust(Cat,
                      text,
                      cat,
                      other_cat=None,
                      other_clan_name=None,
                      new_cat=None,
                      clan=None,
                      murder_reveal=False,
                      victim=None):
    """
    This function takes the given text and returns it with the abbreviations replaced appropriately
    :param Cat: Always give the Cat class
    :param text: The text that needs to be changed
    :param cat: The cat taking the place of m_c
    :param other_cat: The cat taking the place of r_c
    :param other_clan_name: The other clan involved in the event
    :param new_cat: The cat taking the place of n_c
    :param clan: The player's Clan
    :param murder_reveal: Whether or not this event is a murder reveal
    :return: the adjusted text
    """

    cat_dict = {}

    if cat:
        cat_dict["m_c"] = (str(cat.name), choice(cat.pronouns))
        cat_dict["p_l"] = cat_dict["m_c"]
    if "acc_plural" in text:
        text = text.replace("acc_plural", str(ACC_DISPLAY[cat.pelt.accessory]["plural"]))
    if "acc_singular" in text:
        text = text.replace("acc_singular", str(ACC_DISPLAY[cat.pelt.accessory]["singular"]))

    if type(other_cat) == list:
        chosen_cat = choice(other_cat)
        if chosen_cat.pronouns:
            cat_dict["r_c"] = (str(chosen_cat.name), choice(chosen_cat.pronouns))
        else:
            cat_dict["r_c"] = (str(chosen_cat.name))
    elif other_cat:
        if other_cat.pronouns:
            cat_dict["r_c"] = (str(other_cat.name), choice(other_cat.pronouns))
        else:
            cat_dict["r_c"] = (str(other_cat.name))

    if new_cat:
        cat_dict["n_c_pre"] = (str(new_cat.name.prefix), None)
        cat_dict["n_c"] = (str(new_cat.name), choice(new_cat.pronouns))

    if other_clan_name:
        text = text.replace("o_c", other_clan_name)
    if clan:
        clan_name = str(clan.name)
    else:
        if game.clan is None:
            clan_name = game.switches["clan_list"][0]
        else:
            clan_name = str(game.clan.name)

    text = text.replace("c_n", clan_name + "Clan")

    if murder_reveal and victim:
        victim_cat = Cat.fetch_cat(victim)
        cat_dict["mur_c"] = (str(victim_cat.name), choice(victim_cat.pronouns))

    # Dreams and Omens
    text, senses, list_type = find_special_list_types(text)
    if list_type:
        chosen_items = get_special_snippet_list(list_type, randint(1, 3), sense_groups=senses)
        text = text.replace(list_type, chosen_items)

    adjust_text = process_text(text, cat_dict)

    return adjust_text


def leader_ceremony_text_adjust(Cat,
                                text,
                                leader,
                                life_giver=None,
                                virtue=None,
                                extra_lives=None, ):
    """
    used to adjust the text for leader ceremonies
    """
    replace_dict = {
        "m_c_star": (str(leader.name.prefix + "star"), choice(leader.pronouns)),
        "m_c": (str(leader.name.prefix + leader.name.suffix), choice(leader.pronouns)),
    }

    if life_giver:
        replace_dict["r_c"] = (str(Cat.fetch_cat(life_giver).name), choice(Cat.fetch_cat(life_giver).pronouns))

    text = process_text(text, replace_dict)

    if virtue:
        virtue = process_text(virtue, replace_dict)
        text = text.replace("[virtue]", virtue)

    if extra_lives:
        text = text.replace('[life_num]', str(extra_lives))

    text = text.replace("c_n", str(game.clan.name) + "Clan")

    return text


def ceremony_text_adjust(Cat,
                         text,
                         cat,
                         old_name=None,
                         dead_mentor=None,
                         mentor=None,
                         previous_alive_mentor=None,
                         random_honor=None,
                         living_parents=(),
                         dead_parents=()):
    clanname = str(game.clan.name + "Clan")

    random_honor = random_honor
    random_living_parent = None
    random_dead_parent = None

    adjust_text = text

    cat_dict = {
        "m_c": (str(cat.name), choice(cat.pronouns)) if cat else ("cat_placeholder", None),
        "(mentor)": (str(mentor.name), choice(mentor.pronouns)) if mentor else ("mentor_placeholder", None),
        "(deadmentor)": (str(dead_mentor.name), choice(dead_mentor.pronouns)) if dead_mentor else (
            "dead_mentor_name", None),
        "(previous_mentor)": (
            str(previous_alive_mentor.name), choice(previous_alive_mentor.pronouns)) if previous_alive_mentor else (
            "previous_mentor_name", None),
        "l_n": (str(game.clan.leader.name), choice(game.clan.leader.pronouns)) if game.clan.leader else (
            "leader_name", None),
        "c_n": (clanname, None),
    }
    
    if old_name:
        cat_dict["(old_name)"] = (old_name, None)

    if random_honor:
        cat_dict["r_h"] = (random_honor, None)

    if "p1" in adjust_text and "p2" in adjust_text and len(living_parents) >= 2:
        cat_dict["p1"] = (str(living_parents[0].name), choice(living_parents[0].pronouns))
        cat_dict["p2"] = (str(living_parents[1].name), choice(living_parents[1].pronouns))
    elif living_parents:
        random_living_parent = choice(living_parents)
        cat_dict["p1"] = (str(random_living_parent.name), choice(random_living_parent.pronouns))
        cat_dict["p2"] = (str(random_living_parent.name), choice(random_living_parent.pronouns))

    if "dead_par1" in adjust_text and "dead_par2" in adjust_text and len(dead_parents) >= 2:
        cat_dict["dead_par1"] = (str(dead_parents[0].name), choice(dead_parents[0].pronouns))
        cat_dict["dead_par2"] = (str(dead_parents[1].name), choice(dead_parents[1].pronouns))
    elif dead_parents:
        random_dead_parent = choice(dead_parents)
        cat_dict["dead_par1"] = (str(random_dead_parent.name), choice(random_dead_parent.pronouns))
        cat_dict["dead_par2"] = (str(random_dead_parent.name), choice(random_dead_parent.pronouns))

    adjust_text = process_text(adjust_text, cat_dict)

    return adjust_text, random_living_parent, random_dead_parent


def shorten_text_to_fit(name, length_limit, font_size=None, font_type="resources/fonts/NotoSans-Medium.ttf"):
    length_limit = length_limit//2 if not game.settings['fullscreen'] else length_limit
    # Set the font size based on fullscreen settings if not provided
    # Text box objects are named by their fullscreen text size so it's easier to do it this way
    if font_size is None:
        font_size = 30
    font_size = font_size//2 if not game.settings['fullscreen'] else font_size
    # Create the font object
    font = pygame.font.Font(font_type, font_size)
    
    # Add dynamic name lengths by checking the actual width of the text
    total_width = 0
    short_name = ''
    for index, character in enumerate(name):
        char_width = font.size(character)[0]
        ellipsis_width = font.size("...")[0]
        
        # Check if the current character is the last one and its width is less than or equal to ellipsis_width
        if index == len(name) - 1 and char_width <= ellipsis_width:
            short_name += character
        else:
            total_width += char_width
            if total_width + ellipsis_width > length_limit:
                break
            short_name += character

    # If the name was truncated, add '...'
    if len(short_name) < len(name):
        short_name += '...'

    return short_name

# ---------------------------------------------------------------------------- #
#                                    Sprites                                   #
# ---------------------------------------------------------------------------- #

def scale(rect):
    rect[0] = round(rect[0] / 1600 * screen_x) if rect[0] > 0 else rect[0]
    rect[1] = round(rect[1] / 1400 * screen_y) if rect[1] > 0 else rect[1]
    rect[2] = round(rect[2] / 1600 * screen_x) if rect[2] > 0 else rect[2]
    rect[3] = round(rect[3] / 1400 * screen_y) if rect[3] > 0 else rect[3]

    return rect


def scale_dimentions(dim):
    dim = list(dim)
    dim[0] = round(dim[0] / 1600 * screen_x) if dim[0] > 0 else dim[0]
    dim[1] = round(dim[1] / 1400 * screen_y) if dim[1] > 0 else dim[1]
    dim = tuple(dim)

    return dim


def update_sprite(cat):
    # First, check if the cat is faded.
    if cat.faded:
        # Don't update the sprite if the cat is faded.
        return

    # apply
    cat.sprite = generate_sprite(cat)
    # update class dictionary
    cat.all_cats[cat.ID] = cat


def generate_sprite(cat, life_state=None, scars_hidden=False, acc_hidden=False, always_living=False, 
                    no_not_working=False) -> pygame.Surface:
    """Generates the sprite for a cat, with optional arugments that will override certain things. 
        life_stage: sets the age life_stage of the cat, overriding the one set by it's age. Set to string. 
        scar_hidden: If True, doesn't display the cat's scars. If False, display cat scars. 
        acc_hidden: If True, hide the accessory. If false, show the accessory.
        always_living: If True, always show the cat with living lineart
        no_not_working: If true, never use the not_working lineart.
                        If false, use the cat.not_working() to determine the no_working art. 
        """
    
    if life_state is not None:
        age = life_state
    else:
        age = cat.age
    
    if always_living:
        dead = False
    else:
        dead = cat.dead
    
    # setting the cat_sprite (bc this makes things much easier)
    if not no_not_working and cat.not_working() and age != 'newborn' and game.config['cat_sprites']['sick_sprites']:
        if age in ['kitten', 'adolescent']:
            cat_sprite = str(19)
        else:
            cat_sprite = str(18)
    elif cat.pelt.paralyzed and age != 'newborn':
        if age in ['kitten', 'adolescent']:
            cat_sprite = str(17)
        else:
            if cat.pelt.length == 'long' or (cat.pelt.length == 'medium' and get_current_season() == 'Leaf-bare'):
                cat_sprite = str(16)
            else:
                cat_sprite = str(15)
    else:
        if age == 'elder' and not game.config['fun']['all_cats_are_newborn']:
            age = 'senior'
        
        if game.config['fun']['all_cats_are_newborn']:
            cat_sprite = str(cat.pelt.cat_sprites['newborn'])
        else:
            if cat.pelt.cat_sprites[age] < 9 and cat.pelt.cat_sprites[age] > 5 and (cat.pelt.length == 'medium' and get_current_season() == 'Leaf-bare') and cat.moons > 11:
                cat_sprite = str(cat.pelt.cat_sprites[age]+3)
            else:
                cat_sprite = str(cat.pelt.cat_sprites[age])

    new_sprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

    vitiligo = ['MOON', 'PHANTOM', 'POWDER', 'BLEACHED', 'VITILIGO', 'VITILIGOTWO', 'SMOKEY']

    try:
        solidcolours = {
            'black' : 0,
            'chocolate' : 1,
            'cinnamon' : 2,
            'lowred' : 3,
            'mediumred' : 4,
            'rufousedred' : 5,
            'blue' : 6,
            'lilac' : 7,
            'fawn' : 8,
            'lowcream' : 9,
            'mediumcream' : 10,
            'rufousedcream' : 11,
            'dove' : 12,
            'champagne' : 13,
            'buff' : 14,
            'lowhoney' : 15,
            'mediumhoney' : 16,
            'rufousedhoney' : 17,
            'platinum' : 18,
            'lavender' : 19,
            'beige' : 20,
            'lowivory' : 21,
            'mediumivory' : 22,
            'rufousedivory' : 23
        }

        stripecolourdict = {
                'rufousedapricot' : 'lowred',
                'mediumapricot' : 'rufousedcream',
                'lowapricot' : 'mediumcream',

                'rufousedhoney-apricot' : 'lowred',
                'mediumhoney-apricot' : 'rufousedhoney',
                'lowhoney-apricot' : 'mediumhoney',

                'rufousedivory-apricot' : 'lowhoney',
                'mediumivory-apricot' : 'rufousedivory',
                'lowivory-apricot' : 'mediumivory'
            }
        gensprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                
        def GenSprite(genotype, phenotype):
            phenotype.SpriteInfo(cat.moons)

            def CreateStripes(stripecolour, whichbase, coloursurface=None, pattern=None, special = None):
                stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                
                if not pattern and not special and 'solid' not in whichbase:
                    if('chinchilla' in whichbase):
                        stripebase.blit(sprites.sprites['chinchillashading' + cat_sprite], (0, 0))   
                    elif('shaded' in whichbase):
                        stripebase.blit(sprites.sprites['shadedshading' + cat_sprite], (0, 0))       
                    else:           
                        stripebase.blit(sprites.sprites[genotype.wbtype + 'shading' + cat_sprite], (0, 0))      

                if pattern:
                    stripebase.blit(sprites.sprites[pattern + cat_sprite], (0, 0))
                else:    
                    stripebase.blit(sprites.sprites[phenotype.GetTabbySprite() + cat_sprite], (0, 0))

                charc = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                if(genotype.agouti[0] == "Apb" and ('red' not in stripecolour and 'cream' not in stripecolour and 'honey' not in stripecolour and 'ivory' not in stripecolour and 'apricot' not in stripecolour)):
                    charc.blit(sprites.sprites['charcoal' + cat_sprite], (0, 0))
                
                if(genotype.agouti == ["Apb", "Apb"]):
                    charc.set_alpha(125)
                stripebase.blit(charc, (0, 0))

                if coloursurface:
                    stripebase.blit(coloursurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                elif 'basecolours' in stripecolour:
                    stripebase.blit(sprites.sprites[stripecolour], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                else:
                    surf = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                    surf.blit(sprites.sprites['basecolours'+ str(solidcolours.get(stripecolourdict.get(stripecolour, stripecolour)))], (0, 0))
                    if phenotype.caramel == 'caramel' and not ('red' in stripecolour or 'cream' in stripecolour or 'honey' in stripecolour or 'ivory' in stripecolour or 'apricot' in stripecolour):    
                        surf.blit(sprites.sprites['caramel0'], (0, 0))

                    stripebase.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                middle = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                if(genotype.soktype == "full sokoke" and not pattern):
                    middle.blit(stripebase, (0, 0))
                    stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                    middle.set_alpha(150)
                    stripebase.blit(middle, (0, 0))
                    middle = CreateStripes(stripecolour, whichbase, coloursurface, pattern=phenotype.GetTabbySprite(special='redbar'))
                    stripebase.blit(middle, (0, 0))
                elif(genotype.soktype == "mild fading" and not pattern):
                    middle.blit(stripebase, (0, 0))
                    stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                    middle.set_alpha(204)
                    stripebase.blit(middle, (0, 0))
                    middle = CreateStripes(stripecolour, whichbase, coloursurface, pattern=phenotype.GetTabbySprite(special='redbar'))
                    stripebase.blit(middle, (0, 0))
                return stripebase

            def MakeCat(whichmain, whichcolour, whichbase, special=None):
                if (genotype.white[0] == 'W' or genotype.pointgene[0] == 'c' or whichcolour == 'white' or genotype.white_pattern == ['full white']):
                    whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                    if(genotype.pointgene[0] == "c"):
                        whichmain.blit(sprites.sprites['albino' + cat_sprite], (0, 0))
                elif(whichcolour != whichbase):
                    if(genotype.pointgene[0] == "C"):
                        whichmain.blit(sprites.sprites[whichbase + cat_sprite], (0, 0))

                        if special !='copper' and cat.moons > 12 and (genotype.silver[0] == 'I' and genotype.sunshine[0] == 'fg' and (get_current_season() == 'Leaf-fall' or get_current_season() == 'Leaf-bare')):
                            sunshine = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            
                            colours = phenotype.FindRed(genotype, cat.moons, special='low')
                            sunshine = MakeCat(sunshine, colours[0], colours[1], special='copper')

                            sunshine.set_alpha(150)
                            whichmain.blit(sunshine, (0, 0))
                        
                        if("rufoused" in whichcolour or 'medium' in whichcolour or 'low' in whichcolour) and ('red' in whichbase or 'cream' in whichbase or 'honey' in whichbase or 'ivory' in whichbase):
                            if(genotype.ext[0] != "Eg" and (genotype.ext[0] == "ec" and genotype.agouti[0] != "a" and 'o' in genotype.sexgene)):
                                if("chinchilla" in whichbase):
                                    whichmain.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + "chinchilla" + cat_sprite], (0, 0))        
                                elif("shaded" in whichbase):
                                    whichmain.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + "shaded" + cat_sprite], (0, 0))        
                                else:
                                    whichmain.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + genotype.wbtype + cat_sprite], (0, 0))        
                            elif(not (genotype.ext[0] == "ec" and genotype.agouti[0] == "a" and 'o' in genotype.sexgene)):
                                whichmain.blit(sprites.sprites["unders_" + whichbase + cat_sprite], (0, 0))

                        if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                            whichmain.blit(sprites.sprites['caramel0'], (0, 0))

                        stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        stripebase.blit(CreateStripes(whichcolour, whichbase), (0, 0))

                        if((genotype.sunshine[0] != 'N' and genotype.wbtype == 'shaded') or genotype.wbtype == 'chinchilla'):
                            if not ("rufoused" in whichcolour or 'medium' in whichcolour or 'low' in whichcolour or genotype.wbtype == 'chinchilla'):
                                stripebase.blit(CreateStripes(phenotype.FindRed(genotype, cat.moons, special='red')[0], phenotype.FindRed(genotype, cat.moons, special='red')[1]), (0, 0))
                                whichmain.blit(stripebase, (0, 0))
                            stripebase = CreateStripes(whichcolour, whichbase)
                            stripebase.set_alpha(120)
                            whichmain.blit(stripebase, (0, 0))
                            stripebase = CreateStripes(whichcolour, whichbase, pattern='agouti')
                        elif(genotype.wbtype == 'shaded' or genotype.sunshine[0] != 'N'):
                            if not ("rufoused" in whichcolour or 'medium' in whichcolour or 'low' in whichcolour):
                                stripebase.blit(CreateStripes(phenotype.FindRed(genotype, cat.moons, special='red')[0], phenotype.FindRed(genotype, cat.moons, special='red')[1]), (0, 0))
                                whichmain.blit(stripebase, (0, 0))
                            stripebase = CreateStripes(whichcolour, whichbase)
                            stripebase.set_alpha(200)
                            whichmain.blit(stripebase, (0, 0))
                            stripebase = CreateStripes(whichcolour, whichbase, pattern='agouti')
                        
                        whichmain.blit(stripebase, (0, 0))
                    else:
                        #create base
                        colourbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        if(whichcolour == "black" and genotype.pointgene[0] == "cm"):
                            colourbase.blit(sprites.sprites[whichbase.replace("black", "cinnamon") + cat_sprite], (0, 0))
                        else:
                            colourbase.blit(sprites.sprites[whichbase + cat_sprite], (0, 0))
                        
                            if special !='copper' and cat.moons > 12 and (genotype.silver[0] == 'I' and genotype.sunshine[0] == 'fg' and (get_current_season() == 'Leaf-fall' or get_current_season() == 'Leaf-bare')):
                                sunshine = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                
                                colours = phenotype.FindRed(genotype, cat.moons, special='low')
                                sunshine = MakeCat(sunshine, colours[0], colours[1], special='copper')

                                sunshine.set_alpha(150)
                                colourbase.blit(sunshine, (0, 0))
                            
                            if special != 'nounders' and ("rufoused" in whichcolour or 'medium' in whichcolour or 'low' in whichcolour) and ('red' in whichbase or 'cream' in whichbase or 'honey' in whichbase or 'ivory' in whichbase):
                                if(genotype.ext[0] != "Eg" and (genotype.ext[0] == "ec" and genotype.agouti[0] != "a" and 'o' in genotype.sexgene) and ('red' in whichbase or 'cream' in whichbase or 'honey' in whichbase or 'ivory' in whichbase)):
                                    if("chinchilla" in whichbase):
                                        whichmain.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + "chinchilla" + cat_sprite], (0, 0))        
                                    elif("shaded" in whichbase):
                                        whichmain.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + "shaded" + cat_sprite], (0, 0))        
                                    else:
                                        whichmain.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + genotype.wbtype + cat_sprite], (0, 0))        
                                elif(not (genotype.ext[0] == "ec" and genotype.agouti[0] == "a" and 'o' in genotype.sexgene)):
                                    whichmain.blit(sprites.sprites["unders_" + whichbase + cat_sprite], (0, 0))
                            if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                colourbase.blit(sprites.sprites['caramel0'], (0, 0))


                            if((genotype.pointgene == ["cb", "cb"] and cat_sprite != "20") or (((("cb" in genotype.pointgene or genotype.pointgene[0] == "cm") and cat_sprite != "20") or genotype.pointgene == ["cb", "cb"]) and get_current_season() == 'Leaf-bare')):
                                colourbase.set_alpha(100)
                            elif((("cb" in genotype.pointgene or genotype.pointgene[0] == "cm") and cat_sprite != "20") or genotype.pointgene == ["cb", "cb"] or ((cat_sprite != "20" or ("cb" in genotype.pointgene or genotype.pointgene[0] == "cm")) and get_current_season() == 'Leaf-bare')):
                                colourbase.set_alpha(50)
                            elif(cat_sprite != "20" or ("cb" in genotype.pointgene or genotype.pointgene[0] == "cm")):
                                colourbase.set_alpha(15)
                            else:
                                colourbase.set_alpha(0)
                        
                        whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                        whichmain.blit(colourbase, (0, 0))

                        #add base stripes
                        stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        colour = whichcolour
                        coloursurface = None
                        
                        if("cm" in genotype.pointgene):
                            if(whichcolour == "black" and genotype.pointgene[0] == "cm"):
                                stripebase.blit(CreateStripes('lightbasecolours2', whichbase), (0, 0))
                                colour = 'lightbasecolours2'
                            else:
                                if("cb" in genotype.pointgene or genotype.pointgene[0] == "cm"):
                                    if(whichcolour == "black" and cat_sprite != "20"):
                                        stripebase.blit(CreateStripes('lightbasecolours2', whichbase), (0, 0))
                                        colour = 'lightbasecolours2'
                                    elif((whichcolour == "chocolate" and cat_sprite != "20") or whichcolour == "black"):
                                        stripebase.blit(CreateStripes('lightbasecolours1', whichbase), (0, 0))
                                        colour = 'lightbasecolours1'
                                    elif(whichcolour == "cinnamon" or whichcolour == "chocolate"):
                                        stripebase.blit(CreateStripes('lightbasecolours0', whichbase), (0, 0))
                                        colour = 'lightbasecolours0'
                                    else:
                                        pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                        pointbase.blit(sprites.sprites['basecolours'+ str(solidcolours.get(stripecolourdict.get(whichcolour, whichcolour)))], (0, 0))
                                        if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                            pointbase.blit(sprites.sprites['caramel0'], (0, 0))
                                        pointbase.set_alpha(204)
                                        pointbase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                        pointbase2.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                                        pointbase2.blit(pointbase, (0, 0))
                                        stripebase.blit(CreateStripes(whichcolour, whichbase, coloursurface=pointbase2), (0, 0))
                                        coloursurface = pointbase2
                                else:
                                    if(whichcolour == "black" and cat_sprite != "20"):
                                        stripebase.blit(CreateStripes('lightbasecolours1', whichbase), (0, 0))
                                        colour = 'lightbasecolours1'
                                    else:
                                        stripebase.blit(CreateStripes('lightbasecolours0', whichbase), (0, 0))
                                        colour = 'lightbasecolours0'
                        
                        else:
                            if(whichcolour == "black" and genotype.pointgene == ["cb", "cb"] and cat_sprite != "20"):
                                stripebase.blit(CreateStripes('lightbasecolours3', whichbase), (0, 0))
                                colour = 'lightbasecolours3'
                            elif(((whichcolour == "chocolate" and genotype.pointgene == ["cb", "cb"]) or (whichcolour == "black" and "cb" in genotype.pointgene)) and cat_sprite != "20" or (whichcolour == "black" and genotype.pointgene == ["cb", "cb"])):
                                stripebase.blit(CreateStripes('lightbasecolours2', whichbase), (0, 0))
                                colour = 'lightbasecolours2'
                            elif(((whichcolour == "cinnamon" and genotype.pointgene == ["cb", "cb"]) or (whichcolour == "chocolate" and "cb" in genotype.pointgene) or (whichcolour == "black" and genotype.pointgene == ["cs", "cs"])) and cat_sprite != "20" or ((whichcolour == "chocolate" and genotype.pointgene == ["cb", "cb"]) or (whichcolour == "black" and "cb" in genotype.pointgene))):
                                stripebase.blit(CreateStripes('lightbasecolours1', whichbase), (0, 0))
                                colour = 'lightbasecolours1'

                            elif(genotype.pointgene == ["cb", "cb"]):
                                pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                pointbase.blit(sprites.sprites['basecolours'+ str(solidcolours.get(stripecolourdict.get(whichcolour, whichcolour)))], (0, 0))
                                if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                    pointbase.blit(sprites.sprites['caramel0'], (0, 0))
                                pointbase.set_alpha(204)
                                pointbase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                pointbase2.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                                pointbase2.blit(pointbase, (0, 0))
                                stripebase.blit(CreateStripes(whichcolour, whichbase, coloursurface=pointbase2), (0, 0))
                                coloursurface = pointbase2
                            elif("cb" in genotype.pointgene):
                                pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                pointbase.blit(sprites.sprites['basecolours'+ str(solidcolours.get(stripecolourdict.get(whichcolour, whichcolour)))], (0, 0))
                                if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                    pointbase.blit(sprites.sprites['caramel0'], (0, 0))
                                if(genotype.eumelanin[0] == "bl"):
                                    pointbase.set_alpha(25)
                                else:
                                    pointbase.set_alpha(102)
                                pointbase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                pointbase2.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                                pointbase2.blit(pointbase, (0, 0))
                                stripebase.blit(CreateStripes(whichcolour, whichbase, coloursurface=pointbase2), (0, 0))
                                coloursurface = pointbase2
                            else:
                                stripebase.blit(CreateStripes('lightbasecolours0', whichbase), (0, 0))
                                colour = 'lightbasecolours0'
                        
                        if((genotype.sunshine[0] != 'N' and genotype.wbtype == 'shaded') or genotype.wbtype == 'chinchilla'):
                            stripebase.set_alpha(120)
                            whichmain.blit(stripebase, (0, 0))
                            stripebase = CreateStripes(colour, whichbase, coloursurface=coloursurface, pattern='agouti')
                        elif(genotype.wbtype == 'shaded' or genotype.sunshine[0] != 'N'):
                            stripebase.set_alpha(200)
                            whichmain.blit(stripebase, (0, 0))
                            stripebase = CreateStripes(colour, whichbase, coloursurface=coloursurface, pattern='agouti')

                        whichmain.blit(stripebase, (0, 0))

                        #mask base
                        colourbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        if(whichcolour == "black" and genotype.pointgene[0] == "cm"):
                            colourbase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            colourbase.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                            colourbase2.blit(sprites.sprites[whichbase.replace("black", "cinnamon") + cat_sprite], (0, 0))
                            colourbase2.set_alpha(150)
                            colourbase.blit(colourbase2, (0, 0))
                        else:
                            colourbase.blit(sprites.sprites[whichbase + cat_sprite], (0, 0))
                            if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                colourbase.blit(sprites.sprites['caramel0'], (0, 0))
                                
                            
                            if special !='copper' and cat.moons > 12 and (genotype.silver[0] == 'I' and genotype.sunshine[0] == 'fg' and (get_current_season() == 'Leaf-fall' or get_current_season() == 'Leaf-bare')):
                                sunshine = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                
                                colours = phenotype.FindRed(genotype, cat.moons, special='low')
                                sunshine = MakeCat(sunshine, colours[0], colours[1], special='copper')

                                sunshine.set_alpha(150)
                                colourbase.blit(sunshine, (0, 0))
                            
                            if special != 'nounders' and ("rufoused" in whichcolour or 'medium' in whichcolour or 'low' in whichcolour) and ('red' in whichbase or 'cream' in whichbase or 'honey' in whichbase or 'ivory' in whichbase):
                                if(genotype.ext[0] != "Eg" and (genotype.ext[0] == "ec" and genotype.agouti[0] != "a" and 'o' in genotype.sexgene)):
                                    if("chinchilla" in whichbase):
                                        colourbase.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + "chinchilla" + cat_sprite], (0, 0))        
                                    elif("shaded" in whichbase):
                                        colourbase.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + "shaded" + cat_sprite], (0, 0))        
                                    else:
                                        colourbase.blit(sprites.sprites["unders_" + stripecolourdict.get(whichcolour, whichcolour).replace('rufoused', '').replace('medium', '').replace('low', '')+ "silver" + genotype.wbtype + cat_sprite], (0, 0))        
                                elif(not (genotype.ext[0] == "ec" and genotype.agouti[0] == "a" and 'o' in genotype.sexgene)):
                                    colourbase.blit(sprites.sprites["unders_" + whichbase + cat_sprite], (0, 0))
                        pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        pointbase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        pointbase2.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                        if("cm" in genotype.pointgene):
                            if(whichcolour == "black" and genotype.pointgene[0] == "cm"):
                                pointbase.blit(colourbase, (0, 0))
                            else:
                                if((("cb" in genotype.pointgene or genotype.pointgene[0] == "cm") and cat_sprite != "20") or ((cat_sprite != "20" or ("cb" in genotype.pointgene or genotype.pointgene[0] == "cm")) and get_current_season() == "Leaf-bare")):
                                    colourbase.set_alpha(204)
                                elif(cat_sprite != "20" or ("cb" in genotype.pointgene or genotype.pointgene[0] == "cm")):
                                    colourbase.set_alpha(125)
                                else:
                                    colourbase.set_alpha(0)

                                pointbase2.blit(colourbase, (0, 0))

                                if(get_current_season() == "Greenleaf"):
                                    pointbase.blit(sprites.sprites['mochal' + cat_sprite], (0, 0))
                                    pointbase.blit(pointbase2, (0, 0), 
                                                special_flags=pygame.BLEND_RGBA_MULT)
                                elif(get_current_season() == "Leaf-bare"):
                                    pointbase.blit(sprites.sprites['mochad' + cat_sprite], (0, 0))
                                    pointbase.blit(pointbase2, (0, 0), 
                                                special_flags=pygame.BLEND_RGBA_MULT)
                                else:
                                    pointbase.blit(sprites.sprites['mocham' + cat_sprite], (0, 0))
                                    pointbase.blit(pointbase2, (0, 0), 
                                                special_flags=pygame.BLEND_RGBA_MULT)
                            
                                
                        else:
                            if((genotype.pointgene == ["cb", "cb"] and cat_sprite != "20") or ("cb" in genotype.pointgene and cat_sprite != "20" and get_current_season() == 'Leaf-bare')):
                                colourbase.set_alpha(180)
                            elif(("cb" in genotype.pointgene and cat_sprite != "20") or genotype.pointgene == ["cb", "cb"] or ((cat_sprite != "20" or "cb" in genotype.pointgene) and get_current_season() == 'Leaf-bare')):
                                colourbase.set_alpha(120)
                            elif(cat_sprite != "20" or "cb" in genotype.pointgene):
                                colourbase.set_alpha(50)
                            else:
                                colourbase.set_alpha(15)
                            
                            pointbase2.blit(colourbase, (0, 0))

                            if(get_current_season() == "Greenleaf"):
                                pointbase.blit(sprites.sprites['pointsl' + cat_sprite], (0, 0))
                                pointbase.blit(pointbase2, (0, 0), 
                                            special_flags=pygame.BLEND_RGBA_MULT)
                            elif(get_current_season() == "Leaf-bare"):
                                pointbase.blit(sprites.sprites['pointsd' + cat_sprite], (0, 0))
                                pointbase.blit(pointbase2, (0, 0), 
                                            special_flags=pygame.BLEND_RGBA_MULT)
                            else:
                                pointbase.blit(sprites.sprites['pointsm' + cat_sprite], (0, 0))
                                pointbase.blit(pointbase2, (0, 0), 
                                            special_flags=pygame.BLEND_RGBA_MULT)
                        
                            
                        #add mask stripes
                    
                        stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        stripebase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

                        if(whichcolour == "black" and genotype.pointgene[0] == "cm"):
                            colour = 'lightbasecolours2'
                        else:
                            colour = whichcolour
                
                        stripebase.blit(CreateStripes(colour, whichbase), (0, 0))


                        if(get_current_season() == "Greenleaf"):
                            stripebase2.blit(sprites.sprites['mochal' + cat_sprite], (0, 0))
                            stripebase2.blit(stripebase, (0, 0), 
                                        special_flags=pygame.BLEND_RGBA_MULT)
                        elif(get_current_season() == "Leaf-bare"):
                            stripebase2.blit(sprites.sprites['mochad' + cat_sprite], (0, 0))
                            stripebase2.blit(stripebase, (0, 0), 
                                        special_flags=pygame.BLEND_RGBA_MULT)
                        else:
                            stripebase2.blit(sprites.sprites['mocham' + cat_sprite], (0, 0))
                            stripebase2.blit(stripebase, (0, 0), 
                                        special_flags=pygame.BLEND_RGBA_MULT)

                        pointbase.blit(stripebase2, (0, 0))

                        whichmain.blit(pointbase, (0, 0))

                else:
                    if(genotype.pointgene[0] == "C"):
                        whichmain.blit(sprites.sprites['basecolours'+ str(solidcolours.get(stripecolourdict.get(whichcolour, whichcolour)))], (0, 0))
                        if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                            whichmain.blit(sprites.sprites['caramel0'], (0, 0))
                            
                        if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                            whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                        if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                            ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                            if(cat.moons < 4):
                                ghostingbase.set_alpha(150)
                            
                            whichmain.blit(ghostingbase, (0, 0))
                        if (genotype.silver[0] == 'I'):
                            whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))
                            if(phenotype.silvergold == ' light smoke '):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))



                        stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                    
                        stripebase.blit(CreateStripes(whichcolour, "solid"), (0, 0))
                        
                        whichmain.blit(stripebase, (0, 0))
                    elif("cm" in genotype.pointgene):
                        colour = None
                        coloursurface = None
                        if(whichcolour == "black" and genotype.pointgene[0] == "cm"):
                            whichmain.blit(sprites.sprites['lightbasecolours2'], (0, 0)) 
                            if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                    whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                            if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                if(cat.moons < 4):
                                    ghostingbase.set_alpha(150)
                                
                                whichmain.blit(ghostingbase, (0, 0))
                            if (genotype.silver[0] == 'I'):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))


                            stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        
                            stripebase.blit(CreateStripes('cinnamon', 'solid', pattern="fullbar"), (0, 0))
                            stripebase.set_alpha(150)

                            whichmain.blit(stripebase, (0, 0))
                        else:
                            stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                
                            if("cb" in genotype.pointgene or genotype.pointgene[0] == "cm"):
                                if(whichcolour == "black" and cat_sprite != "20"):
                                    whichmain.blit(sprites.sprites['lightbasecolours2'], (0, 0))
                                    colour = 'lightbasecolours2'
                                    if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                        whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                                    if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                        ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                        ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                        if(cat.moons < 4):
                                            ghostingbase.set_alpha(150)
                                        
                                        whichmain.blit(ghostingbase, (0, 0))
                                    if (genotype.silver[0] == 'I'):
                                        whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))

                                elif((whichcolour == "chocolate" and cat_sprite != "20") or whichcolour == "black"):
                                    whichmain.blit(sprites.sprites['lightbasecolours1'], (0, 0))
                                    colour = 'lightbasecolours1'

                                    if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                        whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                                    if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                        ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                        ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                        if(cat.moons < 4):
                                            ghostingbase.set_alpha(150)
                                        
                                        whichmain.blit(ghostingbase, (0, 0))
                                    if (genotype.silver[0] == 'I'):
                                        whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))
                                elif(whichcolour == "cinnamon" or whichcolour == "chocolate"):
                                    whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                                    colour = 'lightbasecolours0'
                                else:
                                    pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                    pointbase.blit(sprites.sprites['basecolours'+ str(solidcolours.get(whichcolour))], (0, 0))
                                    if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                        pointbase.blit(sprites.sprites['caramel0'], (0, 0))
                        
                                    pointbase.set_alpha(204)
                                    whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                                    whichmain.blit(pointbase, (0, 0))
                                    pointbase.blit(whichmain, (0, 0))
                                    coloursurface = pointbase
                                    

                                    if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                        whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                                    if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                        ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                        ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                        if(cat.moons < 4):
                                            ghostingbase.set_alpha(150)
                                        
                                        whichmain.blit(ghostingbase, (0, 0))
                                    if (genotype.silver[0] == 'I'):
                                        whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))
                            else:
                                if(whichcolour == "black" and cat_sprite != "20"):
                                    whichmain.blit(sprites.sprites['lightbasecolours1'], (0, 0))
                                    colour = 'lightbasecolours1'

                                    if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                        whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                                    if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                        ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                        ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                        if(cat.moons < 4):
                                            ghostingbase.set_alpha(150)
                                        
                                        whichmain.blit(ghostingbase, (0, 0))
                                    if (genotype.silver[0] == 'I'):
                                        whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))
                                else:
                                    whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                                    colour = 'lightbasecolours0'
                            
                            stripebase = CreateStripes(colour, 'solid', coloursurface=coloursurface)
                            whichmain.blit(stripebase, (0, 0))

                            pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            pointbase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            
                            pointbase2.blit(sprites.sprites['basecolours'+ str(solidcolours.get(whichcolour))], (0, 0))
                            if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                pointbase2.blit(sprites.sprites['caramel0'], (0, 0))
                        
                                    
                            if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                            if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                if(cat.moons < 4):
                                    ghostingbase.set_alpha(150)
                                
                                whichmain.blit(ghostingbase, (0, 0))
                            if (genotype.silver[0] == 'I'):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))


                            stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            stripebase.blit(CreateStripes(whichcolour, 'solid'), (0, 0))

                            pointbase2.blit(stripebase, (0, 0))

                            if(get_current_season() == "Greenleaf"):
                                pointbase.blit(sprites.sprites['mochal' + cat_sprite], (0, 0))
                                pointbase.blit(pointbase2, (0, 0), 
                                            special_flags=pygame.BLEND_RGBA_MULT)
                            elif(get_current_season() == "Leaf-bare"):
                                pointbase.blit(sprites.sprites['mochad' + cat_sprite], (0, 0))
                                pointbase.blit(pointbase2, (0, 0), 
                                            special_flags=pygame.BLEND_RGBA_MULT)
                            else:
                                pointbase.blit(sprites.sprites['mocham' + cat_sprite], (0, 0))
                                pointbase.blit(pointbase2, (0, 0), 
                                            special_flags=pygame.BLEND_RGBA_MULT)
                        
                            whichmain.blit(pointbase, (0, 0))        
                            
                    else:
                        colour = whichcolour
                        coloursurface = None
                        stripebase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        if(whichcolour == "black" and genotype.pointgene == ["cb", "cb"] and cat_sprite != "20"):
                            whichmain.blit(sprites.sprites['lightbasecolours3'], (0, 0)) 
                            colour = 'lightbasecolours3'

                            if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                            if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                if(cat.moons < 4):
                                    ghostingbase.set_alpha(150)
                                
                                whichmain.blit(ghostingbase, (0, 0))
                            if (genotype.silver[0] == 'I'):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))


                        elif(((whichcolour == "chocolate" and genotype.pointgene == ["cb", "cb"]) or (whichcolour == "black" and "cb" in genotype.pointgene)) and cat_sprite != "20" or (whichcolour == "black" and genotype.pointgene == ["cb", "cb"])):
                            whichmain.blit(sprites.sprites['lightbasecolours2'], (0, 0)) 
                            colour = 'lightbasecolours2'

                            if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                            if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                if(cat.moons < 4):
                                    ghostingbase.set_alpha(150)
                                
                                whichmain.blit(ghostingbase, (0, 0))
                            if (genotype.silver[0] == 'I'):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))

                        elif(((whichcolour == "cinnamon" and genotype.pointgene == ["cb", "cb"]) or (whichcolour == "chocolate" and "cb" in genotype.pointgene) or (whichcolour == "black" and genotype.pointgene == ["cs", "cs"])) and cat_sprite != "20" or ((whichcolour == "chocolate" and genotype.pointgene == ["cb", "cb"]) or (whichcolour == "black" and "cb" in genotype.pointgene))):
                            whichmain.blit(sprites.sprites['lightbasecolours1'], (0, 0))  
                            colour = 'lightbasecolours1'

                            if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                            if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                if(cat.moons < 4):
                                    ghostingbase.set_alpha(150)
                                
                                whichmain.blit(ghostingbase, (0, 0))
                            if (genotype.silver[0] == 'I'):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))

                        elif(genotype.pointgene == ["cb", "cb"]):
                            pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            pointbase.blit(sprites.sprites['basecolours'+ str(solidcolours.get(whichcolour))], (0, 0))
                            if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                pointbase.blit(sprites.sprites['caramel0'], (0, 0))
                        
                            pointbase.set_alpha(204)
                            whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                            whichmain.blit(pointbase, (0, 0))
                            pointbase.blit(whichmain, (0, 0)) 
                            coloursurface = pointbase

                            if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                            if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                if(cat.moons < 4):
                                    ghostingbase.set_alpha(150)
                                
                                whichmain.blit(ghostingbase, (0, 0))
                            if (genotype.silver[0] == 'I'):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))

                        elif("cb" in genotype.pointgene):
                            pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            pointbase.blit(sprites.sprites['basecolours'+ str(solidcolours.get(whichcolour))], (0, 0))
                            if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                pointbase.blit(sprites.sprites['caramel0'], (0, 0))
                        
                            if(genotype.eumelanin[0] == "bl"):
                                pointbase.set_alpha(25)
                            else:
                                pointbase.set_alpha(102)
                            whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                            whichmain.blit(pointbase, (0, 0))

                            coloursurface = whichmain

                            if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                                whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                            if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                                ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                                ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                                if(cat.moons < 4):
                                    ghostingbase.set_alpha(150)
                                
                                whichmain.blit(ghostingbase, (0, 0))
                            if (genotype.silver[0] == 'I'):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))

                        else:
                            whichmain.blit(sprites.sprites['lightbasecolours0'], (0, 0))
                            colour = 'lightbasecolours0'

                        stripebase = CreateStripes(colour, 'solid', coloursurface=coloursurface)

                        whichmain.blit(stripebase, (0, 0))

                        pointbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        pointbase2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            
                        pointbase2.blit(sprites.sprites['basecolours'+ str(solidcolours.get(whichcolour))], (0, 0))
                        if phenotype.caramel == 'caramel' and not ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):    
                                pointbase2.blit(sprites.sprites['caramel0'], (0, 0))
                        
                            
                        if(genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a'):
                            whichmain.blit(sprites.sprites['grizzle' + cat_sprite], (0, 0))
                        if genotype.ghosting[0] == 'Gh' or (genotype.silver[0] == 'I' and genotype.furLength[0] == 'l'):
                            ghostingbase = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                            ghostingbase.blit(sprites.sprites['ghost' + cat_sprite], (0, 0))
                            if(cat.moons < 4):
                                ghostingbase.set_alpha(150)
                            
                            whichmain.blit(ghostingbase, (0, 0))
                        if (genotype.silver[0] == 'I'):
                            whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))
                            if(phenotype.silvergold == ' light smoke '):
                                whichmain.blit(sprites.sprites['smoke' + cat_sprite], (0, 0))




                        stripebase = CreateStripes(whichcolour, "solid")
                        
                        pointbase2.blit(stripebase, (0, 0))
                        if(get_current_season() == "Greenleaf"):
                            pointbase.blit(sprites.sprites['pointsl' + cat_sprite], (0, 0))
                            pointbase.blit(pointbase2, (0, 0), 
                                        special_flags=pygame.BLEND_RGBA_MULT)
                        elif(get_current_season() == "Leaf-bare"):
                            pointbase.blit(sprites.sprites['pointsd' + cat_sprite], (0, 0))
                            pointbase.blit(pointbase2, (0, 0), 
                                        special_flags=pygame.BLEND_RGBA_MULT)
                        else:
                            pointbase.blit(sprites.sprites['pointsm' + cat_sprite], (0, 0))
                            pointbase.blit(pointbase2, (0, 0), 
                                        special_flags=pygame.BLEND_RGBA_MULT)
                    
                        whichmain.blit(pointbase, (0, 0))


                seasondict = {
                    'Greenleaf': 'summer',
                    'Leaf-bare': 'winter'
                }

                if(genotype.karp[0] == 'K'):
                    if(genotype.karp[1] == 'K'):
                        whichmain.blit(sprites.sprites['homokarpati'+ seasondict.get(get_current_season(), "spring") + cat_sprite], (0, 0))
                    else:
                        whichmain.blit(sprites.sprites['hetkarpati'+ seasondict.get(get_current_season(), "spring") + cat_sprite], (0, 0))
                


                pads = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                pads.blit(sprites.sprites['pads' + cat_sprite], (0, 0))

                pad_dict = {
                    'red' : 0,
                    'white' : 1,
                    'tabby' : 2,
                    'black' : 3,
                    'chocolate' : 4,
                    'cinnamon' : 5,
                    'blue' : 6,
                    'lilac' : 7,
                    'fawn' : 8,
                    'dove' : 9,
                    'champagne' : 10,
                    'buff' : 11,
                    'platinum' : 12,
                    'lavender' : 13,
                    'beige' : 14
                }

                if(genotype.white[0] == 'W' or genotype.pointgene[0] == 'c' or genotype.white_pattern == ['full white']):
                    pads.blit(sprites.sprites['nosecolours1'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                elif ('red' in whichcolour or 'cream' in whichcolour or 'honey' in whichcolour or 'ivory' in whichcolour or 'apricot' in whichcolour):
                    pads.blit(sprites.sprites['nosecolours0'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                else:
                    pads.blit(sprites.sprites['nosecolours' + str(pad_dict.get(whichcolour))], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                whichmain.blit(pads, (0, 0))
                
                return whichmain

            gensprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
            gensprite = MakeCat(gensprite, phenotype.maincolour, phenotype.spritecolour)
            
            if (genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a') and genotype.satin[0] != "st" and genotype.tenn[0] != 'tr' and not ('red' in phenotype.maincolour or 'cream' in phenotype.maincolour or 'honey' in phenotype.maincolour or 'ivory' in phenotype.maincolour or 'apricot' in phenotype.maincolour):    
                gensprite.blit(sprites.sprites['satin0'], (0, 0))
            elif (genotype.glitter[0] == 'gl' or genotype.ghosting[0] == 'Gh') and (genotype.agouti[0] != 'a' or ('red' in phenotype.maincolour or 'cream' in phenotype.maincolour or 'honey' in phenotype.maincolour or 'ivory' in phenotype.maincolour or 'apricot' in phenotype.maincolour)):    
                if genotype.satin[0] != "st" and genotype.tenn[0] != 'tr':    
                    gensprite.blit(sprites.sprites['satin0'], (0, 0))
                if(genotype.ghosting[0] == 'Gh'):
                    fading = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                    fading.blit(sprites.sprites['tabbyghost'+cat_sprite], (0, 0))
                    fading.set_alpha(50)
                    gensprite.blit(fading, (0, 0))
                    gensprite.blit(sprites.sprites['satin0'], (0, 0))

            
            if not ('red' in phenotype.maincolour or 'cream' in phenotype.maincolour or 'honey' in phenotype.maincolour or 'ivory' in phenotype.maincolour or 'apricot' in phenotype.maincolour) and (genotype.ext[0] != "Eg" and genotype.agouti[0] !='a' and (genotype.sunshine[0] == 'sg' or genotype.sunshine[0] == 'sh' or ('ec' in genotype.ext and genotype.ext[0] != "Eg") or (genotype.ext[0] == 'ea' and cat.moons > 6) or (genotype.silver[0] == 'i' and genotype.sunshine[0] == 'fg'))):
                sunshine = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                sunshine.blit(sprites.sprites['bimetal' + cat_sprite], (0, 0))

                colours = phenotype.FindRed(genotype, cat.moons, special='nosilver')
                underbelly = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                underbelly = MakeCat(underbelly, colours[0], colours[1], special='nounders')
                sunshine.blit(underbelly, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

                sunshine.set_alpha(100)
                gensprite.blit(sunshine, (0, 0))

            if(phenotype.patchmain != ""):
                tortpatches = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                tortpatches = MakeCat(tortpatches, phenotype.patchmain, phenotype.patchcolour)
                
                if phenotype.caramel == 'caramel' and not ('red' in phenotype.patchmain or 'cream' in phenotype.patchmain or 'honey' in phenotype.patchmain or 'ivory' in phenotype.patchmain or 'apricot' in phenotype.patchmain): 
                    tortpatches.blit(sprites.sprites['caramel0'], (0, 0))
                if (genotype.ext[0] == 'Eg' and genotype.agouti[0] != 'a') and genotype.satin[0] != "st" and genotype.tenn[0] != 'tr' and not ('red' in phenotype.patchmain or 'cream' in phenotype.patchmain or 'honey' in phenotype.patchmain or 'ivory' in phenotype.patchmain or 'apricot' in phenotype.patchmain): 
                    tortpatches.blit(sprites.sprites['satin0'], (0, 0))
                elif (genotype.glitter[0] == 'gl' or genotype.ghosting[0] == 'Gh') and (genotype.agouti[0] != 'a' or ('red' in phenotype.patchmain or 'cream' in phenotype.patchmain or 'honey' in phenotype.patchmain or 'ivory' in phenotype.patchmain or 'apricot' in phenotype.patchmain)):  
                    if genotype.satin[0] != "st" and genotype.tenn[0] != 'tr':    
                        tortpatches.blit(sprites.sprites['satin0'], (0, 0))
                    if(genotype.ghosting[0] == 'Gh'):
                        fading = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                        fading.blit(sprites.sprites['tabbyghost'+cat_sprite], (0, 0))
                        fading.set_alpha(50)
                        tortpatches.blit(fading, (0, 0))
                        tortpatches.blit(sprites.sprites['satin0'], (0, 0))

                if not ('red' in phenotype.patchmain or 'cream' in phenotype.patchmain or 'honey' in phenotype.patchmain or 'ivory' in phenotype.patchmain or 'apricot' in phenotype.patchmain) and (genotype.agouti[0] !='a' and (genotype.sunshine[0] == 'sg' or genotype.sunshine[0] == 'sh' or (genotype.ext[0] != 'Eg' and 'ec' in genotype.ext) or (genotype.ext[0] == 'ea' and cat.moons > 6) or (genotype.silver[0] == 'i' and genotype.sunshine[0] == 'fg'))):
                    sunshine = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                    sunshine.blit(sprites.sprites['bimetal' + cat_sprite], (0, 0))

                    colours = phenotype.FindRed(genotype, cat.moons, special='nosilver')
                    underbelly = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                    underbelly = MakeCat(underbelly, colours[0], colours[1], special='nounders')
                    sunshine.blit(underbelly, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

                    sunshine.set_alpha(100)
                    tortpatches.blit(sunshine, (0, 0))
                
                tortpatches2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                tortpatches2.blit(sprites.sprites['tortiemask' + phenotype.tortpattern.replace('rev', "") + cat_sprite], (0, 0))
                tortpatches2.blit(tortpatches, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                gensprite.blit(tortpatches2, (0, 0))    

            if genotype.satin[0] == "st" or genotype.tenn[0] == 'tr':
                gensprite.blit(sprites.sprites['satin0'], (0, 0))

            if (genotype.bleach[0] == "lb" and cat.moons > 3) or 'masked' in phenotype.silvergold:
                gensprite.blit(sprites.sprites['bleach' + cat_sprite], (0, 0))
            
            
            nose = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
            nose.blit(sprites.sprites['nose' + cat_sprite], (0, 0))

            nose_dict = {
                'red' : 0,
                'white' : 1,
                'tabby' : 2,
                'black' : 3,
                'chocolate' : 4,
                'cinnamon' : 5,
                'blue' : 6,
                'lilac' : 7,
                'fawn' : 8,
                'dove' : 9,
                'champagne' : 10,
                'buff' : 11,
                'platinum' : 12,
                'lavender' : 13,
                'beige' : 14
            }

            if(genotype.white[0] == 'W' or genotype.pointgene[0] == 'c'):
                nose.blit(sprites.sprites['nosecolours1'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            elif ((genotype.ext[0] == 'ea' and genotype.agouti[0] != 'a') or 'red' in phenotype.maincolour or 'cream' in phenotype.maincolour or 'honey' in phenotype.maincolour or 'ivory' in phenotype.maincolour or 'apricot' in phenotype.maincolour):
                nose.blit(sprites.sprites['nosecolours0'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            elif (phenotype.maincolour != phenotype.spritecolour and genotype.ext[0] != 'ea'):
                nose.blit(sprites.sprites['nosecolours2'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                nose.blit(sprites.sprites['nosecolours' + str(nose_dict.get(phenotype.maincolour))], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            gensprite.blit(nose, (0, 0))

            whitesprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

            if(genotype.white_pattern != 'No' and genotype.white_pattern):
                for x in genotype.white_pattern:
                    if('dorsal' not in x and 'break/' not in x and x not in vitiligo):
                        whitesprite.blit(sprites.sprites[x + cat_sprite], (0, 0))
            if(genotype.white_pattern != 'No' and genotype.white_pattern):
                for x in genotype.white_pattern:
                    if('break/' in x):
                        whitesprite.blit(sprites.sprites[x + cat_sprite], (0, 0))
            whitesprite.set_colorkey((0, 0, 255))
            nose.blit(sprites.sprites['pads' + cat_sprite], (0, 0))
            nose.blit(sprites.sprites['nose' + cat_sprite], (0, 0))
            nose.blit(sprites.sprites['nosecolours1'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            nose2 = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
            nose2.blit(whitesprite, (0, 0))

            if(genotype.vitiligo):
                for x in vitiligo:
                    if x in genotype.white_pattern:
                        nose2.blit(sprites.sprites[x + cat_sprite], (0, 0))
            nose2.blit(nose, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            gensprite.blit(whitesprite, (0, 0))
            if(genotype.vitiligo):
                for x in vitiligo:
                    if x in genotype.white_pattern:
                        gensprite.blit(sprites.sprites[x + cat_sprite], (0, 0))
            if genotype.white_pattern:
                if 'dorsal1' in genotype.white_pattern:
                    gensprite.blit(sprites.sprites['dorsal1' + cat_sprite], (0, 0))
                elif 'dorsal2' in genotype.white_pattern:
                    gensprite.blit(sprites.sprites['dorsal2' + cat_sprite], (0, 0))


            if(cat.genotype.sedesp == ['hr', 're']):
                gensprite.blit(sprites.sprites['furpoint' + cat_sprite], (0, 0))
                gensprite.blit(sprites.sprites['furpoint' + cat_sprite], (0, 0))
            elif(cat.pelt.length == 'hairless'):
                gensprite.blit(sprites.sprites['hairless' + cat_sprite], (0, 0))
                gensprite.blit(sprites.sprites['furpoint' + cat_sprite], (0, 0))
            elif('patchy ' in cat.phenotype.furtype):
                gensprite.blit(sprites.sprites['donskoy' + cat_sprite], (0, 0))

            if('sparse' in cat.phenotype.furtype):
                gensprite.blit(sprites.sprites['satin0'], (0, 0))
                gensprite.blit(sprites.sprites['satin0'], (0, 0))
                gensprite.blit(sprites.sprites['lykoi' + cat_sprite], (0, 0))

            gensprite.blit(nose2, (0, 0))


            if(genotype.fold[0] != 'Fd' or genotype.curl[0] == 'Cu'):
                gensprite.blit(sprites.sprites['ears' + cat_sprite], (0, 0))

            # draw eyes & scars1
            #eyes = sprites.sprites['eyes' + cat.pelt.eye_colour + cat_sprite].copy()
            #if cat.pelt.eye_colour2 != None:
            #    eyes.blit(sprites.sprites['eyes2' + cat.pelt.eye_colour2 + cat_sprite], (0, 0))
            #new_sprite.blit(eyes, (0, 0))

            if(int(cat_sprite) < 18):
                lefteye = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                righteye = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
                special = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

                lefteye.blit(sprites.sprites['left' + cat_sprite], (0, 0))
                righteye.blit(sprites.sprites['right' + cat_sprite], (0, 0))

                lefteye.blit(sprites.sprites[genotype.lefteyetype + "/" + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                righteye.blit(sprites.sprites[genotype.righteyetype + "/" + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                gensprite.blit(lefteye, (0, 0))
                gensprite.blit(righteye, (0, 0))

                if(genotype.extraeye):
                    special.blit(sprites.sprites[genotype.extraeye + cat_sprite], (0, 0))
                    special.blit(sprites.sprites[genotype.extraeyetype + "/" + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    gensprite.blit(special, (0, 0))
            
            return gensprite

        gensprite.blit(GenSprite(cat.genotype, cat.phenotype), (0, 0))

        if(cat.genotype.chimera):
            chimerapatches = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
            chimerapatches.blit(sprites.sprites['tortiemask' + cat.genotype.chimerapattern + cat_sprite], (0, 0))
            chimerapheno = Phenotype(cat.genotype.chimerageno)
            chimerapatches.blit(GenSprite(cat.genotype.chimerageno, chimerapheno), (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            gensprite.blit(chimerapatches, (0, 0))

        if not scars_hidden:
            for scar in cat.pelt.scars:
                if scar in cat.pelt.scars1:
                    gensprite.blit(sprites.sprites['scars' + scar + cat_sprite], (0, 0))
                if scar in cat.pelt.scars3:
                    gensprite.blit(sprites.sprites['scars' + scar + cat_sprite], (0, 0))

        # draw line art
        if game.settings['shaders'] and not dead:
            gensprite.blit(sprites.sprites['shaders' + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            gensprite.blit(sprites.sprites['lighting' + cat_sprite], (0, 0))

        # make sure colours are in the lines
        if('rexed' in cat.phenotype.furtype or 'wiry' in cat.phenotype.furtype):
            gensprite.blit(sprites.sprites['rexbord'+ cat_sprite], (0, 0))
            gensprite.blit(sprites.sprites['rexbord'+ cat_sprite], (0, 0))
        else:
            gensprite.blit(sprites.sprites['normbord'+ cat_sprite], (0, 0))
            gensprite.blit(sprites.sprites['normbord'+ cat_sprite], (0, 0))
        if(cat.genotype.fold[0] == 'Fd'):
            gensprite.blit(sprites.sprites['foldbord'+ cat_sprite], (0, 0))
            gensprite.blit(sprites.sprites['foldbord'+ cat_sprite], (0, 0))
        elif(cat.genotype.curl[0] == 'Cu'):
            gensprite.blit(sprites.sprites['curlbord'+ cat_sprite], (0, 0))
            gensprite.blit(sprites.sprites['curlbord'+ cat_sprite], (0, 0))
        
        gensprite.set_colorkey((0, 0, 255))

        new_sprite.blit(gensprite, (0, 0))

        lineart = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
        earlines = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
        bodylines = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

        if not dead:
            if(cat.genotype.fold[0] != 'Fd'):
                if(cat.genotype.curl[0] == 'Cu'):
                    earlines.blit(sprites.sprites['curllines' + cat_sprite], (0, 0))
                else:
                    earlines.blit(sprites.sprites['lines' + cat_sprite], (0, 0))
            elif(cat.genotype.curl[0] == 'Cu'):
                earlines.blit(sprites.sprites['fold_curllines' + cat_sprite], (0, 0))
            else:
                earlines.blit(sprites.sprites['foldlines' + cat_sprite], (0, 0))
        elif cat.df:
            if(cat.genotype.fold[0] != 'Fd'):
                if(cat.genotype.curl[0] == 'Cu'):
                    earlines.blit(sprites.sprites['curllineartdf' + cat_sprite], (0, 0))
                else:
                    earlines.blit(sprites.sprites['lineartdf' + cat_sprite], (0, 0))
            elif(cat.genotype.curl[0] == 'Cu'):
                earlines.blit(sprites.sprites['fold_curllineartdf' + cat_sprite], (0, 0))
            else:
                earlines.blit(sprites.sprites['foldlineartdf' + cat_sprite], (0, 0))
        elif dead:
            if(cat.genotype.fold[0] != 'Fd'):
                if(cat.genotype.curl[0] == 'Cu'):
                    earlines.blit(sprites.sprites['curllineartdead' + cat_sprite], (0, 0))
                else:
                    earlines.blit(sprites.sprites['lineartdead' + cat_sprite], (0, 0))
            elif(cat.genotype.curl[0] == 'Cu'):
                earlines.blit(sprites.sprites['fold_curllineartdead' + cat_sprite], (0, 0))
            else:
                earlines.blit(sprites.sprites['foldlineartdead' + cat_sprite], (0, 0))

        earlines.blit(sprites.sprites['isolateears' + cat_sprite], (0, 0))
        earlines.set_colorkey((0, 0, 255))

        lineart.blit(earlines, (0, 0))
        if('rexed' in cat.phenotype.furtype or 'wiry' in cat.phenotype.furtype):
            if not dead:
                bodylines.blit(sprites.sprites['rexlineart' + cat_sprite], (0, 0))
            elif cat.df:
                bodylines.blit(sprites.sprites['rexlineartdf' + cat_sprite], (0, 0))
            else:
                bodylines.blit(sprites.sprites['rexlineartdead' + cat_sprite], (0, 0))
        else:
            if not dead:
                bodylines.blit(sprites.sprites['lines' + cat_sprite], (0, 0))
            elif cat.df:
                bodylines.blit(sprites.sprites['lineartdf' + cat_sprite], (0, 0))
            else:
                bodylines.blit(sprites.sprites['lineartdead' + cat_sprite], (0, 0))
            
        bodylines.blit(sprites.sprites['noears' + cat_sprite], (0, 0))
        bodylines.set_colorkey((0, 0, 255))
        if cat_sprite != '20':
            lineart.blit(bodylines, (0, 0))
        new_sprite.blit(lineart, (0, 0))

        # draw skin and scars2
        blendmode = pygame.BLEND_RGBA_MIN

        gensprite = new_sprite
        if cat.phenotype.bobtailnr > 0:
            gensprite.blit(sprites.sprites['bobtail' + str(cat.phenotype.bobtailnr) + cat_sprite], (0, 0))
        gensprite.set_colorkey((0, 0, 255))
        new_sprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)
        new_sprite.blit(gensprite, (0, 0))

        if not scars_hidden:
            for scar in cat.pelt.scars:
                if scar in cat.pelt.scars2:
                    new_sprite.blit(sprites.sprites['scars' + scar + cat_sprite], (0, 0), special_flags=blendmode)

        # draw accessories
        if not acc_hidden:        
            if cat.pelt.accessory in cat.pelt.plant_accessories:
                new_sprite.blit(sprites.sprites['acc_herbs' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.wild_accessories:
                new_sprite.blit(sprites.sprites['acc_wild' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.collars:
                new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))

            elif cat.pelt.accessory in cat.pelt.flower_accessories:
                new_sprite.blit(sprites.sprites['acc_flower' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.plant2_accessories:
                new_sprite.blit(sprites.sprites['acc_plant2' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.snake_accessories:
                new_sprite.blit(sprites.sprites['acc_snake' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.smallAnimal_accessories:
                new_sprite.blit(sprites.sprites['acc_smallAnimal' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.deadInsect_accessories:
                new_sprite.blit(sprites.sprites['acc_deadInsect' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.aliveInsect_accessories:
                new_sprite.blit(sprites.sprites['acc_aliveInsect' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.fruit_accessories:
                new_sprite.blit(sprites.sprites['acc_fruit' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.crafted_accessories:
                new_sprite.blit(sprites.sprites['acc_crafted' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.tail2_accessories:
                new_sprite.blit(sprites.sprites['acc_tail2' + cat.pelt.accessory + cat_sprite], (0, 0))

            elif cat.pelt.accessory in cat.pelt.toy_accessories:
                new_sprite.blit(sprites.sprites['acc_toy' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.blankie_accessories:
                new_sprite.blit(sprites.sprites['acc_blankie' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.flag_accessories:
                new_sprite.blit(sprites.sprites['acc_flag' + cat.pelt.accessory + cat_sprite], (0, 0))

        # Apply fading fog
        if cat.pelt.opacity <= 97 and not cat.prevent_fading and game.clan.clan_settings["fading"] and dead:

            stage = "0"
            if 80 >= cat.pelt.opacity > 45:
                # Stage 1
                stage = "1"
            elif cat.pelt.opacity <= 45:
                # Stage 2
                stage = "2"

            new_sprite.blit(sprites.sprites['fademask' + stage + cat_sprite],
                            (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            if cat.df:
                temp = sprites.sprites['fadedf' + stage + cat_sprite].copy()
                temp.blit(new_sprite, (0, 0))
                new_sprite = temp
            else:
                temp = sprites.sprites['fadestarclan' + stage + cat_sprite].copy()
                temp.blit(new_sprite, (0, 0))
                new_sprite = temp

        # reverse, if assigned so
        if cat.pelt.reverse:
            new_sprite = pygame.transform.flip(new_sprite, True, False)

    except (TypeError, KeyError):
        logger.exception("Failed to load sprite")

        # Placeholder image
        new_sprite = image_cache.load_image(f"sprites/error_placeholder.png").convert_alpha()

    return new_sprite

def apply_opacity(surface, opacity):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            pixel = list(surface.get_at((x, y)))
            pixel[3] = int(pixel[3] * opacity / 100)
            surface.set_at((x, y), tuple(pixel))
    return surface


# ---------------------------------------------------------------------------- #
#                                     OTHER                                    #
# ---------------------------------------------------------------------------- #

def chunks(L, n):
    return [L[x: x + n] for x in range(0, len(L), n)]

def is_iterable(y):
    try:
        0 in y
    except TypeError:
        return False


def get_text_box_theme(theme_name=""):
    """Updates the name of the theme based on dark or light mode"""
    if game.settings['dark mode']:
        if theme_name == "":
            return "#default_dark"
        else:
            return theme_name + "_dark"
    else:
        if theme_name == "":
            return "#text_box"
        else:
            return theme_name
def get_button_theme():
    """Updates the name of the theme based on dark or light mode"""
    if game.settings['dark mode']:
        return "#allegiance_dark"
    else:
        return "#allegiance_light"


def quit(savesettings=False, clearevents=False):
    """
    Quits the game, avoids a bunch of repeated lines
    """
    if savesettings:
        game.save_settings()
    if clearevents:
        game.cur_events_list.clear()
    game.rpc.close_rpc.set()
    game.rpc.update_rpc.set()
    pygame.display.quit()
    pygame.quit()
    if game.rpc.is_alive():
        game.rpc.join(1)
    sys_exit()


PERMANENT = None
with open(f"resources/dicts/conditions/permanent_conditions.json", 'r') as read_file:
    PERMANENT = ujson.loads(read_file.read())

ACC_DISPLAY = None
with open(f"resources/dicts/acc_display.json", 'r') as read_file:
    ACC_DISPLAY = ujson.loads(read_file.read())

SNIPPETS = None
with open(f"resources/dicts/snippet_collections.json", 'r') as read_file:
    SNIPPETS = ujson.loads(read_file.read())

PREY_LISTS = None
with open(f"resources/dicts/prey_text_replacements.json", 'r') as read_file:
    PREY_LISTS = ujson.loads(read_file.read())

with open(f"resources/dicts/backstories.json", 'r') as read_file:
    BACKSTORIES = ujson.loads(read_file.read())

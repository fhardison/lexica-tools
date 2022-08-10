from pathlib import Path
from collections import namedtuple
import json


Lexica = namedtuple("Lexica", "AUTENREITH LSJ ABBOTT SHORT ROUSE")


ROOT = Path(__file__).parent
ABBOT = ROOT / Path('abbot-smith-gloss-list/gloss-dict.tab')
AUT = ROOT / Path("aut/dat/grc-aut-defs.dat")
LSJ = ROOT / Path("lsj/dat/grc-lsj-defs.dat")
SHORT_DEFS = ROOT / Path("ShortdefsforOKLemma_perseus.txt")
ROUSE = ROOT / Path("rouse_vocab/vocab.tab")


class Either():
    pass

class Right(Either):
    def __init__(self, value):
        self.value = value
    
    def bind(self, f):
        return f(self.value)
    
    def is_right():
        return True
    
    def __eq__(self, x):
        return self.value == x.value

class Left(Either):
    def __init__(self, value):
        self.value = value

    def bind(self, f):
        return self.value

    def is_right():
        return False
    
    def __eq__(self, x):
        return self.value == x.value


class Option():
    def is_nothing():
        pass


class Just(Option):
    def __init__(self, x):
        self.value = x
    
    def is_nothing(self):
        return False
    
    def __bool__(self):
        return True

    def bind(self, f):
        return f(self.value)
    
    def __eq__(self, x):
        if type(x) == Nothing:
            return False
        return self.value == x.value


class Nothing(Option):
    def __init__(self, value=None):
        self.value = value
    
    def is_nothing(self):
        return True
    
    def bind(self, f):
        return Nothing(self.value)
    
    def __bool__(self):
        return False
    
    def __eq__(self, x):
        return False



def load_tab(fpath):
    out = {}
    with open(fpath, 'r', encoding="UTF-8") as f:
        for line in f:
            l = line.strip()
            if l:
                parts = l.split('\t', maxsplit=1)
                if len(parts) > 1:
                    out[parts[0]] = parts[1] 
                else:
                    out[parts[0]] = '??'
    return out

def load_abbot():
    return load_tab(ABBOT)


def load_short_defs():
    return load_tab(SHORT_DEFS)

def load_rouse():
    return load_tab(ROUSE)
    #with open(ROUSE, encoding="UTF-8") as f:
    #    return json.load(f)
    

def load_alpheos(fpath):
    out = {}
    with open(fpath, 'r', encoding="UTF-8") as f:
        for line in f:
            l = line.replace('@', '').strip()
            if l:
                k, v = l.split('|', maxsplit=1)
                if not k in out:
                    out[k] = v
                else:
                    i = 1
                    while f"{k}{v}" not in out:
                        i += 1
                    out[f"{k}{i}"] = v
    return out


def load_aut():
    return load_alpheos(AUT)


def load_lsj():
    return load_alpheos(LSJ)


def get_from_dict(dict, x):
    if x in dict:
        return Just(dict[x])
    else:
        return Nothing()


DICT_MAPPINGS = {
    Lexica.AUTENREITH : load_aut,
    Lexica.LSJ : load_lsj,
    Lexica.SHORT: load_short_defs,
    Lexica.ABBOTT: load_abbot, 
    Lexica.ROUSE: load_rouse
}

NAME_MAPPINGS = {
    Lexica.AUTENREITH : "Aut",
    Lexica.LSJ : "LSJ",
    Lexica.SHORT: "ShortDefs",
    Lexica.ABBOTT: "A-S", 
    Lexica.ROUSE: "Rouse"
}


def load_dicts(targets, default=None, map_names=True):
    """Loads dictionaries specified in `targets` and creates a function that searches them in the order specified"""
    dicts = [(DICT_MAPPINGS[t](), t) for t in targets]
    def finder(x):
        for dict, t in dicts:
            if x in dict:
                if map_names:
                    return Right((dict[x], NAME_MAPPINGS[t]))
                else:
                    return Right((dict[x], t))
        return Left(default)
    return finder


def load_dicts_simple(targets, default=None, map_names=True):
    dicts = [(DICT_MAPPINGS[t](), t) for t in targets]
    def finder(x):
        for dict, t in dicts:
            if x in dict:
                if map_names:
                    return (dict[x], NAME_MAPPINGS[t])
                else:
                    return (dict[x], t)
        return default
    return finder

if __name__ == '__main__':
    ROUSE_DATA = load_rouse()
    assert ROUSE_DATA['ἄβατος'] == 'οὐ παρέχων ἑαυτὸν βαίνειν· οὗ μὴ πάρεστι βαίνειν.'
    print(ROUSE_DATA['ἀγρυπνῶ'])
    ABBOT_DATA = load_abbot()
    assert get_from_dict(ABBOT_DATA, 'ἔγερσις').value == 'a rousing | a rising'
    AUT_DATA = load_aut()
    assert get_from_dict(AUT_DATA, 'Σιδών').value == 'Sidon'
    LSJ_DATA = load_lsj()
    assert get_from_dict(LSJ_DATA, 'λοιγός').value == 'ruin, havoc'
    SHORT_DATA = load_short_defs()	
    assert get_from_dict(SHORT_DATA, 'Αἰνόπαρις').value == 'unlucky Paris'
    homeric2 = load_dicts([Lexica.AUTENREITH, Lexica.LSJ])
    assert homeric2('Σιδών') == Right(('Sidon', Lexica.AUTENREITH))
    print(homeric2('Σιδών').value)
    assert issubclass(Just, Option)
    assert issubclass(Nothing, Option)
    assert issubclass(Right, Either) 
    assert issubclass(Left, Either) 

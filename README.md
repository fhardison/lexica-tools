# Usage

The repo provides a simple API where the user selects the lexicons to be loaded and then is given a function that will do the glossing and return the first gloss found as well as a code showing which lexicon returned the result if no gloss is found a default result can be supplied. There are two version of this. One using an Either Monad and one that simply returns the glosses. 


The repo provides 5 different glossing options:

1. Autenrieth's homeric lexicon
2. LSJ
3. Abbott-Smith NT Greek lexicon
4. Short Defs from the Perseus Project
5. Greek to Greek deffinitions from Rouse's A Greek Boy at Home.

These options are stored in a named tuple named `Lexica`:

`Lexica.AUTENREITH, Lexica.LSJ, Lexica.ABBOTT, Lexica.SHORT, Lexica.ROUSE`

To create a glossing function use either `load_dicts_simple` or `load_dicts` (the monadic version) and supply it a list of the lexicons to check. The order of the lexicons in the list determines the order in which they are checked.


The return values is a tuple of the shape `(<deffinition found>, <lexicon>)`.

By default the `lexicon` value is a string, but you can also supply `map_names=False` to the load_dicts function and it will return the Lexica tuple value representing the lexicon in which the gloss/deff was found.


The following snippet creates a glossing function that tried Autenreith's lexicon first and then proceeds to check LSJ and the Perseus Short Defs. If it can't find anything, it returns a default value of "N/A".

```
glosser = load_dicts_simple([Lexica.AUTENREITH, Lexica.LSJ, Lexica.SHORT], default='N/A')

# print gloss/deff and lexicon code
result = glosser('καί') 
print(f"{result[0]} (found in {result[1]})")
```

The following snippet does the same thing but uses the monadic result:

```
glosser = load_dicts([Lexica.AUTENREITH, Lexica.LSJ, Lexica.SHORT], default='N/A')

res = glosser('NOT A GREEK WORD')

assert res == Left('N/A')

res2 = glosser('καί')

assert typeof(res2) == Right

# print deff
print(res2.value[0])

# print lexicon used
print(res2.value[1])
```

# Sources

## aut and lsj

Both the [aut](https://github.com/alpheios-project/aut) and [lsj](https://github.com/alpheios-project/lsj) repos (included here) are from the [Alpheios Project](https://github.com/alpheios-project) and  are based on data taken from the Perseus Project (<http://www.perseus.tufts.edu/>). 

The National Endowment for the Humanities provided support for entering these texts.

The Perseus data is released under a [CC BY-SA 4.0 license](https://github.com/PerseusDL/canonical-greekLit/blob/master/license.md)


## ShortdefsforOKLemma

The gloss data in `ShortdefsforOKLemma_perseus.txt` is taken from https://github.com/helmadik/shortdefs which contains data taken from Perseus (perseus.uchicago.edu/greek.html) and Logeion (https://logeion.uchicago.edu/lexidium).

## Rouse Vocab

The Greek to Greek definitions found in the Rouse vocabulary data are from Rouse's _A Greek Boy At Home_'s Vocabulary which can be found [here](https://github.com/fhardison/rouse-a-greek-boy-at-home)

# License

In order to comply with licensing of the source data, this work is also released under a [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Stopword list for collector utils
#

class StopWords():

# english stop words
    eng_stop_list = ["un", "da", "se", "ap", "el", "morreu", "en", "la", "que", "ll", "don", "ve", "de", "gt", "lt", "com", "ly", "co", "re", "rt", "http","a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"]

# spanish stop words
    span_stop_list = [ "un", "una" ,"unas" ,"unos" ,"uno" ,"sobre" ,"todo" ,"tambien" ,"tras" ,"otro" ,"algun" ,"alguno" ,"alguna" ,"algunos" ,"algunas" ,"ser" ,"es" ,"soy" ,"eres" ,"somos" ,"sois" ,"estoy" ,"esta" ,"estamos" ,"estais" ,"estan" ,"como" ,"en" ,"para" ,"atras" ,"porque" ,"porque" ,"estado" ,"estaba" ,"ante" ,"antes" ,"siendo" ,"ambos" ,"pero" ,"por" ,"poder" ,"puede" ,"puedo" ,"podemos" ,"podeis" ,"pueden" ,"fui" ,"fue" ,"fuimos" ,"fueron" ,"hacer" ,"hago" ,"hace" ,"hacemos" ,"haceis" ,"hacen" ,"cada" ,"fin" ,"incluso" ,"primero desde" ,"conseguir" ,"consigo" ,"consigue" ,"consigues" ,"conseguimos" ,"consiguen" ,"ir" ,"voy" ,"va" ,"vamos" ,"vais" ,"van" ,"vaya" ,"gueno" ,"ha" ,"tener" ,"tengo" ,"tiene" ,"tenemos" ,"teneis" ,"tienen" ,"el" ,"la" ,"lo" ,"las" ,"los" ,"su" ,"aqui" ,"mio" ,"tuyo" ,"ellos" ,"ellas" ,"nos" ,"nosotros" ,"vosotros" ,"vosotras" ,"si" ,"dentro" ,"solo" ,"solamente" ,"saber" ,"sabes" ,"sabe" ,"sabemos" ,"sabeis" ,"saben" ,"ultimo" ,"largo" ,"bastante" ,"haces" ,"muchos" ,"aquellos" ,"aquellas" ,"sus" ,"entonces" ,"tiempo" ,"verdad" ,"verdadero" ,"verdadera" ,"cierto" ,"ciertos" ,"cierta" ,"ciertas" ,"intentar" ,"intento" ,"intenta" ,"intentas" ,"intentamos" ,"intentais" ,"intentan" ,"dos" ,"bajo" ,"arriba" ,"encima" ,"usar" ,"uso" ,"usas" ,"usa" ,"usamos" ,"usais" ,"usan" ,"emplear" ,"empleo" ,"empleas" ,"emplean" ,"ampleamos" ,"empleais" ,"valor" ,"muy" ,"era" ,"eras" ,"eramos" ,"eran" ,"modo" ,"bien" ,"cual" ,"cuando" ,"donde" ,"mientras" ,"quien" ,"con" ,"entre" ,"sin" ,"trabajo" ,"trabajar" ,"trabajas" ,"trabaja" ,"trabajamos" ,"trabajais" ,"trabajan" ,"podria" ,"podrias" ,"podriamos" ,"podrian" ,"podriais","yo" ,"aquel"]

# italian stop words
    ital_stop_list=[ "a", "adesso", "ai", "al", "alla", "allo", "allora", "altre", "altri", "altro", "anche", "ancora", "avere", "aveva", "avevano", "ben", "buono", "che", "chi", "cinque", "comprare", "con", "consecutivi", "consecutivo", "cosa", "cui", "da", "del", "della", "dello", "dentro", "deve", "devo", "di", "doppio", "due", "e", "ecco", "fare", "fine", "fino", "fra", "gente", "giu", "ha", "hai", "hanno", "ho", "il", "indietro", "invece", "io", "la", "lavoro", "le", "lei", "lo", "loro", "lui", "lungo", "ma", "me", "meglio", "molta", "molti", "molto", "nei", "nella", "no", "noi", "nome", "nostro", "nove", "nuovi", "nuovo", "o", "oltre", "ora", "otto", "peggio", "pero", "persone", "piu", "poco", "primo", "promesso", "qua", "quarto", "quasi", "quattro", "quello", "questo", "qui", "quindi", "quinto", "rispetto", "sara", "secondo", "sei", "sembra", "sembrava", "senza", "sette", "sia", "siamo", "siete", "solo", "sono", "sopra", "soprattutto", "sotto", "stati", "stato", "stesso", "su", "subito", "sul", "sulla", "tanto", "te", "tempo", "terzo", "tra", "tre", "triplo", "ultimo", "un", "una", "uno", "va", "vai", "voi", "volte", "vostro"]

    def __init__(self, engl=True, span=True, ital=True):
        self.stop_list = set()
        if engl:
            self.stop_list = self.stop_list.union(set(self.eng_stop_list))
        if span:
            self.stop_list = self.stop_list.union(set(self.span_stop_list))
        if ital:
            self.stop_list = self.stop_list.union(set(self.ital_stop_list))

    def add_session_stop_list(self, slist):
        # suplement list for this session only
        self.stop_list = self.stop_list.union(set(slist))

    def remove_session_stop_list(self, slist):
        # remove items from list for this session only
        self.stop_list -= set(slist)

    def __len__(self):
        return len(self.stop_list)

    def __iter__(self):
        for x in self.stop_list:
            yield x

    def __getitem__(self, x):
        return x.lower() in self.stop_list


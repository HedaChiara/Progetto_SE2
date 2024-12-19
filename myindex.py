# versione più lunga di index.py, se da linea di comando -S vengono usati i synset. L'indice tende ad ingrandirsi ma non è un problema
# ho modificato alcune cose per Robust, riscarica da moodle se vuoi versione originale

#--- importazione di moduli interi
import string
import sys
import getopt
import os.path
import json

#--- importazione di parti di modulo ---#
from elasticsearch import Elasticsearch


# DEVO CONNETTERMI AL SERVER DI ELASTICSEARCH!

try:
    opts, args = getopt.getopt(sys.argv[1:], "i:VSI",
                               ["index","VERBOSE","EN_STEMMER"])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    sys.exit(2)

#--- variabili globali ---#
INDEXNAME = "sf_books_index"
FILES     = None
VERBOSE   = True
EN_STEMMER = True
STOP = True

nargs = 0
for o, a in opts:
    if o in ("-i", "--index"):
        INDEXNAME = a
        nargs += 2
    elif o in ("-V", "--VERBOSE"):
        VERBOSE = True
        nargs += 1
    elif o in ("-E", "--EN_STEMMER"):
        EN_STEMMER = True
        nargs += 1
    else:
        assert False, "unhandled option"
#--- connettiti al server
server = Elasticsearch('http://localhost:9200')

    
if STOP:
    config = {
  "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_" 
        },
        "english_stemmer": {
          "type":       "stemmer",
          "language":   "english"
        },
        "english_possessive_stemmer": {
          "type":       "stemmer",
          "language":   "possessive_english"
        }
      },
      "analyzer": {
        "rebuilt_english": {
          "tokenizer":  "standard",
          "filter": [
            "english_possessive_stemmer",
            "lowercase",
            "english_stop",
            "english_stemmer"
          ]
        }
      }
    }
  }
}
    response  = server.indices.create(index = "rindexstop",        # si crea l'indice, o con un documento o usando una configurazione. Così si crea indice vuoto, senza posting list
                                      body  = config )


# io userò bulk per indicizzare

''' 
#--- scansione dei file dei documenti ---#
FILES = sys.argv[nargs+1:]
for f in FILES:
    #--- apertura del file del documento ---#
    if VERBOSE:
        print("processing",f,"...")
    infile = open(f,'r')
    ndoc = 0
    #--- lettura del documento ---#
    for doc in infile:
        if len(doc) > 0:
            ndoc += 1
            record = json.loads(doc)
            if VERBOSE:
                print(f,record["id"],'...',end='')                 
            res = server.index(index=INDEXNAME,
                               id=record["id"],
                               document=record)
            if VERBOSE:
                print("added")                 
    if VERBOSE:
        print(f,"done")
if VERBOSE:
    print("all done")

'''    

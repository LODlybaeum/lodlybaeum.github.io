import xml.etree.ElementTree as ET
import rdflib
import hashlib
from rdflib.namespace import RDF, RDFS, XSD, FOAF
from rdflib import Graph, URIRef, Literal, Namespace

TEI = Namespace("http://www.tei-c.org/ns/1.0")
DC = Namespace("http://purl.org/dc/elements/1.1/")
SCHEMA = Namespace("http://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")


tree = ET.parse('article.xml')
g = rdflib.Graph()

g.bind("SCHEMA", SCHEMA)

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

article =  tree.find('.//tei:title', namespaces=ns).text
article_uri = "https://purl.archive.org/domain/lodlybaeum/article/" 

#file description
title = tree.find('.//tei:title', namespaces=ns).text
title_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/title/" 

respElement = tree.find('.//tei:respStmt/tei:name', namespaces=ns).text 
resp_uri= "https://purl.archive.org/domain/lodlybaeum/article/fd/author/"

publicationEl = tree.find('.//tei:publicationStmt', namespaces=ns)
publisher = publicationEl[0].text 
publisher_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/publisher/" 

place = publicationEl[1].text 
place_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/place/" 

date = publicationEl[2].attrib['when']
date_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/pubdate/" 

seriesEl = tree.find('.//tei:seriesStmt', namespaces=ns)
pages = seriesEl[2]
seriesTitle = seriesEl[0].text 
st_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/journal/"
seriesVolume=seriesEl[1].text 
sv_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/volume/"

seriesPages= seriesEl[2].attrib['from']+ '-' + seriesEl[2].attrib['to']
sp_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/pages/"

issn = seriesEl[3].text 
issn_uri = "https://purl.archive.org/domain/lodlybaeum/article/fd/issn/"

g.add((URIRef(article_uri), RDF.type, SCHEMA.ScholarlyArticle))
g.add((URIRef(article_uri), SCHEMA.name, Literal(title))) 
g.add((URIRef(title_uri), RDFS.label, Literal(title))) #title, RDFS.label, To be Taken with...
g.add((URIRef(resp_uri), RDF.type, FOAF.Person)) #author, RDF.type, person
g.add((URIRef(resp_uri), RDFS.label, Literal(respElement))) 
g.add((URIRef(article_uri), DC.creator, URIRef(resp_uri))) 

g.add((URIRef(article_uri), DC.publisher, Literal(publisher))) 
g.add((URIRef(publisher_uri), DC.location, Literal(place))) #publisher, DC.location, Chicago
g.add((URIRef(article_uri), SCHEMA.datePublished, Literal(date, datatype=XSD.date))) 

g.add((URIRef(st_uri), RDF.type, SCHEMA.Periodical)) #journal, rdf.type, periodical
g.add((URIRef(st_uri), RDFS.label, Literal(seriesTitle)))     #rdf.label, Classical Philology
g.add((URIRef(sv_uri), SCHEMA.PublicationVolume, Literal(seriesVolume))) #volume, Schema.publicationVolume, 81
g.add((URIRef(article_uri), DC.extent, Literal(seriesPages))) 
g.add((URIRef(article_uri), SCHEMA.issn, Literal(issn)))
g.add((URIRef(issn_uri), RDF.type, SCHEMA.issn))

g.add((URIRef(article_uri), DC.publisher, Literal(publisher)))
g.add((URIRef(publisher_uri), DC.location, Literal(place)))
g.add((URIRef(article_uri), SCHEMA.datePublished, Literal(date, datatype=XSD.date)))

g.add((URIRef(article_uri), SCHEMA.provider, URIRef(st_uri)))

g.add((URIRef(st_uri), RDF.type, SCHEMA.volumeNumber))
g.add((URIRef(article_uri), SCHEMA.volumeNumber, Literal(seriesVolume)))
g.add((URIRef(article_uri), DC.extent, Literal(seriesPages)))
g.add((URIRef(article_uri), SCHEMA.issn, Literal(issn)))
g.add((URIRef(issn_uri), RDF.type, SCHEMA.issn))

# Triples - article:
#article, RDF.type, scholarly article
         #RDFS.label, Ronald Ridley
         #DC.creator, author
         #DC.publisher, University of Chicago
         #DC.extent, pages
         #Schema.datePublished, date
         #Schema.name, title
         #Schema.issn, issn
         #Schema.provider, Classical Philology

#Citations
quotes_list = []

for element in tree.findall('tei:text/tei:body/tei:p/tei:cit/tei:quote', namespaces=ns):
    quote = element.text
    quotes_list.append(quote)
    
quotes_uris = {}
for i, quote in enumerate(quotes_list):
    quote_uri = "https://purl.archive.org/domain/lodlybaeum/article/quote/" + str(i + 1)  
    quotes_uris[quote] = quote_uri 

for quote, quote_uri in quotes_uris.items():
    g.add((URIRef(quote_uri), RDF.type, DC.bibliographicCitation))
    g.add((URIRef(quote_uri), RDFS.label, Literal(quote)))

#Citations: bibliography
biblio_list = []

for biblio in tree.findall('tei:text/tei:body/tei:p/tei:cit/tei:bibl', namespaces=ns):
    bib = biblio.text
    biblio_list.append(bib)

biblio_uris = {}

for i, bib in enumerate(biblio_list):
    biblio_uri = "https://purl.archive.org/domain/lodlybaeum/article/bibliography/quote/" + str(i + 1)
    biblio_uris[bib] = biblio_uri
    
    g.add((URIRef(biblio_uri), RDF.type, DC.BibliographicResource))
    g.add((URIRef(biblio_uri), RDFS.label, Literal(bib)))
    #citations = Bibliographic resource + text

for j, quote in enumerate(quotes_list):
    quote_uri = "https://purl.archive.org/domain/lodlybaeum/article/quote/" + str(j + 1)
    
    g.add((URIRef(quote_uri), RDFS.label, Literal(quote)))
    
    biblio_uri = biblio_uris.get(biblio_list[j])
    
    if biblio_uri:
        g.add((URIRef(quote_uri), DC.references, URIRef(biblio_uri)))
        g.add((URIRef(article_uri), DC.references, URIRef(biblio_uri)))


#BIbliographic resources not explicitly quoted
all_biblio = [] 
for biblioEntry in tree.findall('tei:text/tei:body/tei:p/tei:bibl', namespaces=ns):
    be = biblioEntry.text
    all_biblio.append(be)
    
for item in biblio_list:
    if item in all_biblio:
        all_biblio.remove(item)

all_biblio_uris = {}
for i, biblioEntry in enumerate(all_biblio):
    all_biblio_uri = "https://purl.archive.org/domain/lodlybaeum/article/bibliography/" + str(i + 1)
    all_biblio_uris[biblioEntry] = all_biblio_uri
    g.add((URIRef(article_uri), DC.references, URIRef(all_biblio_uri)))

g.serialize(destination='toRDF.rdf')

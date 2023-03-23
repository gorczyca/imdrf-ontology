import json
import re

import itertools

from  config import ANNEXES_JSON, ALL_IMDRF


PREFIX = 'imdrf'
BASE_SUPER_CLASS = 'owl:Thing'


OUTPUT_FILE = './imdrf/ontologies/imdrf_ontology_manchester.owl'





def to_upper_cammel_case(s):
    # Remove anything inside parentheses or brackets
    s = re.sub(r'\(.*?\)', '', s)
    s = re.sub(r'\[.*?\]', '', s)

    # Remove non-letter characters and split the string
    words = re.findall('[a-zA-Z]+', s)
    return ''.join([w.capitalize() for w in words])


def find_by_code(annex_json_terms, code):
    return list(filter(lambda x: x['code'] == code, annex_json_terms))[0]


def escape_string(s):
    return s.replace('"', '\\"')


def get_parent(entity_group):
    parents = {find_by_code(ALL_IMDRF, code)[
                                    'term'] for entity in entity_group for code in entity['CodeHierarchy'].split('|')[:-1]}
    top_parents = {ANNEXES_JSON[entity['annex']]['label'] for entity in entity_group }
    return [f'{PREFIX}:{to_upper_cammel_case(par_name)}' for par_name in parents.union(top_parents)]


def get_annexes_manchester(annex_name, annex_label):
    disjoint_annexes = ',\n\t\t'.join([
        f'{PREFIX}:{to_upper_cammel_case(a["label"])}' for a_name, a in ANNEXES_JSON.items() if a_name != annex_name
    ])

    return f'''Class: {PREFIX}:{to_upper_cammel_case(annex_label)}

    Annotations:
        rdfs:label "{annex_label}"@en,
        {PREFIX}:annex "{annex_name}"^^xsd:string
    
    SubClassOf:
        {BASE_SUPER_CLASS}
        
    DisjointWith:
        {disjoint_annexes}
        \n\n'''


def get_term_manchester(term_name, term_group):
    parents = ',\n\t\t'.join(get_parent(term_group))

    my_lambda = lambda x: x['CodeHierarchy']

    groups = {k: list(group) for k, group in itertools.groupby(
        sorted(term_group, key=my_lambda), key=my_lambda)}

    if len(groups) > 1:
        comment = 'Warning! This concept appeared multiple times in the IMDRF with many code hierarchies!'
        for hierarchy, group in groups.items():
            group_definition = escape_string(group[0]['definition'])
            comment += f'\n\nHierarchy: {hierarchy}\n{group_definition}'
    else:
        comment = term_group[0]['definition']

    return f'''Class: {PREFIX}:{to_upper_cammel_case(term_name)}

    Annotations:
        rdfs:label "{term_name}"@en,
        rdfs:comment "{escape_string(comment)}"@en
    
    SubClassOf:
        {parents}\n\n'''



def get_ontology_beginning():
    return f'''Prefix: : <http://www.co-ode.org/ontologies/imdrf.owl#>
Prefix: dc: <http://purl.org/dc/elements/1.1/>
Prefix: owl: <http://www.w3.org/2002/07/owl#>
Prefix: imdrf: <http://www.co-ode.org/ontologies/imdrf.owl#>
Prefix: rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
Prefix: rdfs: <http://www.w3.org/2000/01/rdf-schema#>
Prefix: skos: <http://www.w3.org/2004/02/skos/core#>
Prefix: terms: <http://purl.org/dc/terms/>
Prefix: xml: <http://www.w3.org/XML/1998/namespace>
Prefix: xsd: <http://www.w3.org/2001/XMLSchema#>



Ontology: <http://www.co-ode.org/ontologies/imdrf>
<http://www.co-ode.org/ontologies/imdrf/2.0.0>

Annotations: 
    dc:description "An IMDRF (International Medical Device Regulators Forum) terminologies for Categorized Adverse Event Reporting (AER): terms, terminology and codes."@en,
    dc:title "imdrf"@en,
    terms:contributor "Piotr Gorczyca",
    terms:license "Creative Commons Attribution 3.0 (CC BY 3.0)"^^xsd:string

    
AnnotationProperty: dc:description

    
AnnotationProperty: dc:title

    
AnnotationProperty: owl:versionInfo

    
AnnotationProperty: rdfs:comment

    
AnnotationProperty: rdfs:label

    
AnnotationProperty: rdfs:seeAlso

    
AnnotationProperty: skos:altLabel

    
AnnotationProperty: skos:definition

    
AnnotationProperty: skos:prefLabel

    
AnnotationProperty: terms:contributor

    
AnnotationProperty: terms:license

    
AnnotationProperty: terms:provenance


AnnotationProperty: imdrf:annex

    
Datatype: rdf:PlainLiteral

    
Datatype: xsd:string


'''


if __name__ == '__main__':

    return_term = lambda x: x['term']

    groups = {k: list(group) for k, group in itertools.groupby(
        sorted(ALL_IMDRF, key=return_term), key=return_term)}

    groups_sorted = list(
        reversed(sorted(groups.items(), key=lambda i: len(groups[i[0]]))))


    ontology_string = get_ontology_beginning()

    for annex_name, annex in ANNEXES_JSON.items():
        ontology_string += get_annexes_manchester(
            annex_name, annex['label'])

    ontology_string += '\n\n\n'

    for term_name, term_group in groups_sorted:
        ontology_string += get_term_manchester(term_name, term_group)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(ontology_string)

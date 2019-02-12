import json
from collections import defaultdict

def dict_check_dups(pairs):
    """Check for and reject duplicate keys in a json dictionary"""
    #adapted from https://stackoverflow.com/questions/14902299/json-loads-allows-duplicate-keys-in-a-dictionary-overwriting-the-first-value
    d = {}
    for k,v in pairs:
        if k in d:
            raise ValueError("Duplicate Key {}".format(k))
        d[k] = v
    return d

def check_do_attributes_have_ids(model):
    """does each element of the attribute array have an id key?"""
    passed = True
    for entity in model.values():
        for att in entity['attributes']:
            if 'id' not in att:
                print("Attribute missing id in entity {}".format(entity['id']))
                passed = False
    return passed

def check_unique_attribute_ids(model):
    """Are the attribute identifiers unique across entity"""
    att_count = defaultdict(int)
    for entity in model.values():
        for att in entity['attributes']:
            att_count[ att['id'] ] += 1
    passed = True
    for att_id, c in att_count.items():
        if c > 1:
            print("Overloaded attribute ID: {}".format(att_id))
            passed = False
    return passed

def check_entity_ids_match_keys(model):
    """Does each entity have an id, and does the id match the key?"""
    passed = True
    for key,entity in model.items():
        if 'id' not in entity:
            print('Entity without an id property {}'.format(key))
            passed = False
        else:
            if key != entity['id']:
                print('Entity key {} does not match entity id {}'.format(key,entity['id']))
                passed = False
    return passed

def check_entity_iris(model):
    """Does each entity have an iri?  Is it valid?"""
    passed = True
    for key,entity in model.items():
        if 'iri' not in entity:
            print('Entity lacks an iri key: {}'.format(key))
            passed = False
    return passed

def check_entity_iris(model):
    """Does each entity have an iri?  Is it valid?"""
    passed = True
    for key,entity in model.items():
        if 'iri' not in entity:
            print('Entity lacks an iri key: {}'.format(key))
            passed = False
    return passed

def check_empty_entity_values(model):
    """Does every property of every entity have a non-empty value?"""
    passed = True
    for key,entity in model.items():
        for prop,value in entity.items():
            if prop != 'attributes':
                if len(value.strip()) == 0:
                    print( "Empty value for entity property {}.{}".format(key,prop) )
                    passed = False
    return passed

def check_empty_attribute_values(model):
    """Does every property of every attribute have a non-empty value?"""
    passed = True
    for key,entity in model.items():
        atts = entity['attributes']
        if len(atts) == 0:
            print('Empty attributes for entity {}'.format(key))
            passed = False
        else:
            for att in atts:
                for prop,value in att.items():
                    if not isinstance(value,str):
                        continue
                    if len(value.strip()) == 0:
                        print( "Empty value for attribute property {}.{}.{}".format(key,att['id'],prop) )
                        passed = False
    return passed

def go(model_filename):
    """Read in the model json and run it through some checks to generate
    a punchlist of work to be done"""
    #It's possible that this would be best implemented as a pytest module,
    # but most tests are going to fail on first failed assert, and the output
    # can be wonky looking.  Maybe there are ways around those things? 

    #Or, some (many?) of these tests could be put into a schema for the model spec and tested there.

    #A simple test: is the model even valid json
    #With the object_pairs_hook, we're also making sure that every entity has a unique id, and
    # that every attribute has a unique id within the entity
    with open(model_filename,'r') as model_file:
        model = json.load(model_file, object_pairs_hook = dict_check_dups)

    passed = True
    passed = passed & check_do_attributes_have_ids(model)
    passed = passed & check_unique_attribute_ids(model)
    passed = passed & check_entity_ids_match_keys(model)
    passed = passed & check_entity_iris(model)
    passed = passed & check_empty_entity_values(model)
    passed = passed & check_empty_attribute_values(model)
    #passed = passed & check_attribute_entityId(model)
    #passed = passed & check_valueSets(model)
    #passed = passed & check_iri_labels(model)

    if passed:
        print("No errors found. Good for you!")


if __name__ == '__main__':
    go('model.json')

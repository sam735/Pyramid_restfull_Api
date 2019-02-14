from apis.immunization.type_lookup import(type_lookup)


def insert_to_source_specific_model(iterable,fhirIdn,source,session):
    for key, val in iterable.items():
        if type(val).__name__ == 'list':
            for value in val:
                fn = type_lookup.get(type(value).__name__ )
                if fn is not None:
                    fn( value,fhirIdn,source,key,session)

def lookup_from_type_lookup_and_insert_to_corresponding_table(lookupObj,fhirIdn,source,key,session):
    fn = type_lookup.get(type(lookupObj).__name__ )
    if fn is not None:
        fn( lookupObj,fhirIdn,source,key,session)

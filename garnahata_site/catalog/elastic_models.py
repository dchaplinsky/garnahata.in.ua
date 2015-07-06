from elasticsearch_dsl import DocType, Completion


class Address(DocType):
    """Person document."""
    full_name_suggest = Completion(preserve_separators=False)

    class Meta:
        index = 'garnahata'

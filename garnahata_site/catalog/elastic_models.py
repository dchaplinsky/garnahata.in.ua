from elasticsearch_dsl import DocType, Completion


class Address(DocType):
    """Address document."""

    class Meta:
        index = 'garnahata'


class Ownership(DocType):
    """Ownership document."""
    full_name_suggest = Completion(preserve_separators=False)

    class Meta:
        index = 'garnahata'

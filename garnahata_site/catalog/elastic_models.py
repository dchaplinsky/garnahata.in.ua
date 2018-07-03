from elasticsearch_dsl import (
    DocType,
    Keyword,
    Text,
    Index,
    analyzer,
    tokenizer,
    token_filter,
    Date
)

namesAutocompleteAnalyzer = analyzer(
    "namesAutocompleteAnalyzer",
    tokenizer=tokenizer(
        "autocompleteTokenizer",
        type="edge_ngram",
        min_gram=1,
        max_gram=25,
        token_chars=["letter", "digit"],
    ),
    filter=["lowercase"],
)

namesAutocompleteSearchAnalyzer = analyzer(
    "namesAutocompleteSearchAnalyzer", tokenizer=tokenizer("lowercase")
)

ukrainianAddressesStopwordsAnalyzer = analyzer(
    "ukrainianAddressesStopwordsAnalyzer",
    type="ukrainian",
    filter=[
        token_filter(
            "addresses_stopwords",
            type="stop",
            stopwords=[
                "будинок",
                "обл",
                "район",
                "вулиця",
                "місто",
                "м",
                "квартира",
                "вул",
                "село",
                "буд",
                "кв",
                "проспект",
                "область",
                "селище",
                "міського",
                "типу",
                "офіс",
                "н",
                "р",
                "б",
                "с",
                "провулок",
                "корпус",
                "бульвар",
                "кімната",
                "шосе",
                "в",
                "смт",
                "просп",
                "№",
            ],
        ),
        "lowercase",
    ],
)

BASIC_INDEX_SETTINGS = {
    "number_of_shards": 5,
    "number_of_replicas": 0,
}


class Address(DocType):
    """Address document."""

    class Meta:
        index = 'garnahata_addresses'



OWNERSHIP_INDEX = "garnahata_ownerships"
ownership_idx = Index(OWNERSHIP_INDEX)
ownership_idx.settings(**BASIC_INDEX_SETTINGS)

ownership_idx.analyzer(namesAutocompleteAnalyzer)
ownership_idx.analyzer(namesAutocompleteSearchAnalyzer)
ownership_idx.analyzer(ukrainianAddressesStopwordsAnalyzer)


@ownership_idx.doc_type
class Ownership(DocType):
    """Ownership document."""
    addresses = Text(analyzer="ukrainianAddressesStopwordsAnalyzer", copy_to="all")
    persons = Text(analyzer="ukrainian", copy_to="all")
    companies = Text(analyzer="ukrainian", copy_to="all")
    registered = Date()
    mortgage_registered = Date()
    names_autocomplete = Text(
        analyzer="namesAutocompleteAnalyzer",
        search_analyzer="namesAutocompleteSearchAnalyzer",
        fields={"raw": Text(index=True)},
    )

    all = Text(analyzer="ukrainian")

    class Meta:
        index = OWNERSHIP_INDEX
        doc_type = "garnahata_ownerships_doctype"


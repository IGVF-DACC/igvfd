import logging

from igvfd.ontology import load_ontology
from igvfd.ontology import write_data_to_reference_database
from igvfd.ontology import REFERENCE_ONTOLOGY_TABLE_NAME


logging.basicConfig()
logging.getLogger('igvfd').setLevel(logging.INFO)


def main():
    ontology_data = load_ontology()
    write_data_to_reference_database(
        ontology_data,
        REFERENCE_ONTOLOGY_TABLE_NAME
    )


if __name__ == '__main__':
    main()

import sys

from tabulate import tabulate


def print_title(s):
    """
    Print a string as a title with a strong underline

    Args:
        s: string to print as a title
    """
    print(s)
    print(len(s) * "=")
    print("")


def print_subtitle(s):
    """
    Print a string as a subtitle with an underline

    Args:
        s: string to print as a title
    """
    print(s)
    print(len(s) * "-")
    print("")


def print_entity(entity, title=None, headers=True):
    """
    Print an entity as a title along with the tabular representation
    of the entity.

    Args:
        title: The title to print
        entity: The entity to print
    """

    if title is not None and len(title) > 0:
        print_title(title)

    headers = ["Name", "Value"]
    headers=[]
    tablefmt = "rst"
    body = []

    for field in entity.fields():
        name = field.displayName
        value = field.value
        if field.typeClass.startswith("array"):
            value = "[{}]".format(len(field.value))
        elif field.typeClass.startswith("object"):
            value = "<{}>".format(field.typeName)
        body.append([name, value])

    getattr(sys.stdout, 'buffer', sys.stdout).write(
        tabulate
        (
            body,
            headers,
            tablefmt=tablefmt
        ).encode('utf-8')
    )
    print("")


def print_collection(title, entities, columns):
    """
    Print a collection of entities with specified headers and formatters

    Args:
        title: The title to pring
        entites: The collection to print, one per row in the table
        columns: Tuple of column header name and column row formatter to be
                 applied to each entity in the collection
    """

    if len(entities) == 0:
        return

    if title is not None and len(title) > 0:
        print_title(title)

    headers = [c[0] for c in columns]
    tablefmt = "rst"
    body = []

    for e in entities:
        body.append([c[1](e) for c in columns])

    getattr(sys.stdout, 'buffer', sys.stdout).write(
        tabulate
        (
            body,
            headers,
            tablefmt=tablefmt,
        ).encode('utf-8')
    )
    print("")



def print_response_entity(
    response,
    expected_status,
    title,
    transaction_name
):
    """
    Print a Transaction from a response object if the Transaction exists and
    the response has the expected HTTP status code. 

    If the Transaction doesn't exist in the response, this function silently
    fails and nothing is printed.

    Args:
        response: The response object to extract the Transaction from
        expected_status: The status that the response is expected to have
        title: The title to use for the rendered Transction
        transaction_name: The name of the Transaction expected
    """

    try:
        transaction = response.get(transaction_name, expected_status)
        print_entity(transaction, title=title)
        print("")
    except:
        pass

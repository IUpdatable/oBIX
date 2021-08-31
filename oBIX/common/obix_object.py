
class OBIXObject(object):
    # name: defines the object’s purpose in its parent object
    name: str
    # href: provides a URI reference for identifying the object
    href: str
    # null: support for null objects
    null_able: bool
    # facets: a set of attributes used to provide meta-data about the object
    facets: str
    # val: an attribute used only with value objects (bool, int, real, str, enum, abstime, reltime, date, time and uri)
    # to store the actual value. The literal representation of values map to [XML Schema Part 2: Datatypes] -
    # indicated in the following sections via the “xs:” prefix.
    val: object

    status: str


class ParseError(RuntimeError):
    pass


def _key_remap(kw):
    """ Maps - to _ to make resource attribute name more pleasant. """
    for k, v in kw.items():
        k = k.replace("-", "_")
        yield str(k),v


class Instanceable(type):

    """
    A metaclass for objects that can be instanced from Yay

    This is a base type, you are expected to subclass it for each group of
    objects you wish to instance from Yay. For example::

        class TaskType(Instanceable):
            pass

        class Task(object):
            __metaclass__ = TaskType

    Now any subclasses of Task will be registered with TaskType and can be
    created through the factory methods of TaskType::

        class Foo(Task):
            pass

        instance = TaskType.create_one("Foo", name="freddy", baz=1)

    When combined with Yay you can::

        config = yay.load_uri(StringIO(\"\"\"
            tasks:
              - Foo:
                  name: freddy
                  baz: 1
              - OtherTask:
                  name: domino
                  baz: 22
            \"\"\")

        tasks = TaskType.create_all(config["tasks"])
    """

    objects = {}

    def __new__(meta, class_name, bases, new_attrs):
        cls = super(Instanceable, meta).__new__(meta, class_name, bases, new_attrs)

        registry = meta.objects.setdefault(meta, {})

        name = getattr(cls, "__name__", class_name)
        if name in registry:
            raise KeyError("'%s' is already defined" % name)
        registry[name] = cls

        return cls

    @classmethod
    def create_one(cls, typename, **data):
        if not isinstance(data, dict):
            raise ParseError("Expected mapping for %s, got %s" % (typename, instance))

        registry = cls.objects[cls]

        if not typename in registry:
            raise ParseError("There is no type '%s'" % typename)

        return registry[typename](**dict(_key_remap(data)))

    @classmethod
    def create_all(cls, specification):
        """
        Given a list of types to instance, create an return them
        """
        created = []

        for stanza in specification:
            if len(stanza.keys()) > 1:
                raise ParseError("Too many keys in list item")

            typename, instances = stanza.items()[0]
            if not isinstance(instances, list):
                instances = [instances]

            for instance in instances:
                c = cls.create_one(typename, **instance)
                created.append(c)

        return created


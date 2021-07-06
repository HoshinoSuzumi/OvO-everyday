import uuid


class Utils:
    @staticmethod
    def uuid_mapped(name):
        return uuid.uuid5(uuid.NAMESPACE_X500, name)

    @staticmethod
    def uuid_unmapped():
        return uuid.uuid1()

    @staticmethod
    def is_fetch_done(total: int, offset: int, limit: int):
        return (offset + limit) >= total

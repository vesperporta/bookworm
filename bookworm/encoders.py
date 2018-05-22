from django.core.serializers.json import DjangoJSONEncoder

from hashid_field.hashid import Hashid


class HashidJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Hashid):
            return str(o)
        return super().default(o)

from django.conf import settings

AUTCOMPLETE_DOCUMENT_FIELD = getattr(settings, 'AUTCOMPLETE_DOCUMENT_FIELD', 'content')

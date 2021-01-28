
import os
import sys
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"images/{instance.dir}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"
import os
from operator import itemgetter

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

from translitua.translit import translitua

from fs.totxt import convert_many


@staff_member_required
def index(request):
    links = []
    for root, dirs, files in os.walk(settings.PDF_STORAGE, topdown=True):
        if not dirs and files:
            links.append([root, len(files)])

    return render(
        request,
        "fs/index.html",
        {
            'content': sorted(links, key=itemgetter(0)),
        }

    )


@staff_member_required
def get_xls(request, path):
    pdf_dir = os.path.abspath(os.path.join(settings.PDF_STORAGE, path))

    if os.path.exists(pdf_dir) and pdf_dir.startswith(settings.PDF_STORAGE):
        res = convert_many(pdf_dir + "/*.pdf")
        if res:
            response = HttpResponse(content=res.read(),
                                    content_type='application/ms-excel')

            response['Content-Disposition'] = 'attachment; filename=%s.xlsx' \
                % translitua(pdf_dir.rsplit('/')[-1]).replace(" ", "_")
            return response
        else:
            return HttpResponse('Error: File was not returned.')
    else:
        return HttpResponse('Error: File does not exist.')

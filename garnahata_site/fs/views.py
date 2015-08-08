import os
from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

from .totxt import convert_many


@staff_member_required
def index(request):
    links = []
    for root, dirs, files in os.walk(settings.PDFS_STORAGE,topdown=True):
        for filename in files:
            if filename.endswith('pdf'):
                links.append(os.path.join(root,filename).split('/files/')[1]) 

    return render(
        request,
        "fs/index.html",
        {
            'content': sorted(links),
        }
    )

@staff_member_required
def get_xls(request,path):
    path_to_pdf = os.path.abspath(os.path.join(settings.PDFS_STORAGE, path))
    if path_to_pdf.startswith(settings.PDFS_STORAGE) and os.path.exists(path_to_pdf):
        res = convert_many(path_to_pdf)
        if res:
            response = HttpResponse(content=res.read(),content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xlsx' \
                                           % path_to_pdf.rsplit('/')[-1].split('.')[0]
            return response
        else:
        	return HttpResponse('Error: File was not returned.')
    else:
    	return HttpResponse('Error: File does not exist.')

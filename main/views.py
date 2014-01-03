import json

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.utils.html import escape

import deltalife


def index(request):
    obcine = deltalife.get_obcine()
    return render(request, 'main/index.html', {"obcine": obcine})


def obcina(request):
    if 'x' in request.GET and 'y' in request.GET:
        x = float(request.GET['x'])
        y = float(request.GET['y'])
        id, ime = deltalife.katera_obcina(x, y)
        print id, ime
        return HttpResponse(json.dumps({'id': int(id), 'ime': ime}), content_type="application/json")
    else:
        raise Http404

def prim(request):
    if 'o1' in request.GET and 'o2' in request.GET:
        o1 = int(request.GET['o1'])
        o2 = int(request.GET['o2'])
        povzetek, opis, kazalniki = deltalife.opis(o1, o2)
        return HttpResponse(json.dumps({
            'povzetek' : povzetek,
            'opis' : opis,
            'kazalniki': kazalniki,
        }), content_type="application/json")
    else:
        raise Http404

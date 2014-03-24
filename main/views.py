import json

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.utils.html import escape

import deltalife


def index(request):
    obcine = deltalife.get_obcine()
    sklopi = []
    for key, val in deltalife.SKLOPI.items():
        sklopi.append({'id': key, 'ime': val['ime']})
    return render(request, 'main/index.html', {"obcine": obcine, 'sklopi': sklopi})


def obcina(request):
    if 'x' in request.GET and 'y' in request.GET:
        x = float(request.GET['x'])
        y = float(request.GET['y'])
        id, ime = deltalife.katera_obcina(x, y)
        return HttpResponse(json.dumps({'id': int(id), 'ime': ime}), content_type="application/json")
    else:
        raise Http404

def prim(request):
    if 'o1' in request.GET and 'o2' in request.GET:
        o1 = int(request.GET['o1'])
        o2 = int(request.GET['o2'])
        povzetek, opis, kazalniki = deltalife.opis(o1, o2, meje=False)
        return HttpResponse(json.dumps({
            'povzetek' : povzetek,
            'opis' : opis,
            'kazalniki': kazalniki,
        }), content_type="application/json")
    else:
        raise Http404


def sklopi(request):
    return HttpResponse(json.dumps(deltalife.SKLOPI), content_type="application/json")

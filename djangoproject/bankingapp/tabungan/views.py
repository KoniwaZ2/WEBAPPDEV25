from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Buku
from .forms import BukuTabungan


def list_buku(request):
    #query db
    list_buku = Buku.objects.all() #ambil semua data buku tabungan
    data = {'list_buku': list_buku}
    return render(request, 'buku/list.html', data)

def create_buku(request):
    form = BukuTabungan(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('tabungan:list-buku'))

    data = {}
    data['form'] = form
    return render(request, 'buku/create.html', data)

def update_buku(request, buku_id):
    obj = get_object_or_404(Buku, id=buku_id)
    form = BukuTabungan(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('tabungan:list-buku'))
    context = {}
    context['form'] = form
    return render(request, 'buku/update.html', context)

def delete_buku(request, buku_id):
    obj = get_object_or_404(Buku, id=buku_id)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect(reverse('tabungan:list-buku'))
    context = {'obj': obj}
    return render(request, 'buku/delete.html', context)
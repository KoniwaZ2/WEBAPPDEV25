from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum, Q
from .models import Buku, Transaksi
from .forms import BukuTabungan, TransaksiForm


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

def transaksi(request, buku_id):
    obj = get_object_or_404(Buku, id=buku_id)
    form = TransaksiForm(request.POST or None)
    if form.is_valid():
        transaksi_obj = form.save(commit=False)
        transaksi_obj.buku = obj
        transaksi_obj.save()
        return HttpResponseRedirect(reverse('tabungan:transaksi', args=[buku_id]))
    totals = obj.transaksi.aggregate(
        total_debit=Sum('jumlah', filter=Q(jenis_transaksi='debit')),
        total_credit=Sum('jumlah', filter=Q(jenis_transaksi='credit')),
    )
    total_debit = totals.get('total_debit') or 0
    total_credit = totals.get('total_credit') or 0

    context = {
        'form': form,
        'obj': obj,
        'total_debit': total_debit,
        'total_credit': total_credit,
    }
    return render(request, 'buku/transaksi.html', context)
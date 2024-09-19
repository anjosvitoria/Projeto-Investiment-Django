from django.shortcuts import render, redirect
from empresarios.models import Empresas, Documento
from .models import PropostaInvestimento
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, Http404
# Create your views here.
def sugestao(request):
    if not request.user.is_autenticated:
        return redirect('/usuarios/logar')
    areas = Empresas.area_choices
    if request.method == 'GET':
        return render(request, 'sugestao.html', {'areas: areas'})
    elif request.method == 'POST':
        tipo = request.POST.get('tipo')
        area = request.POST.getlist ('area')
        valor = request.POST.get('valor')
    
    if tipo == 'C':
        empresas = Empresas.objects.filter(tempo_existencia='+5').filter(estagio='E')
    elif tipo = 'D'
        empresas = Empresas.objects.filter(tempo_existencia__in=['-6', '+6', '+1']).exclude(estagio='E')
        #todo: tipo genérico ex: tipo mediano
        
    empresas = empresas. filter(area__in=area)
    
    empresas_selecionadas = []
    for empresa in empresas:
        percentual = float(valor) * 100 / float(empresa.valuation)
        if percentual >= 1:
            empresas_selecionadas.append(empresa)
    return render(request, 'sugestao.html', {'empresas': empresas_selecionadas, 'areas': areas})

def ver_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    documentos = Documento.objects.filter(empresa=empresa)
    #todo: listar as metricas dinamicamente  
    return  render(request, 'ver_empresa.html',{'emrpesa': empresa, 'documentos': documentos})

def realizar_proposta(request, id):
    valor = request.POST.get('valor')
    percentual = request.POST.get('percentual')
    empresa = Empresa.objects.get(id=id)
    
     propostas_aceitas = PropostaInvestimento.objects.filter(empresa=empresa).filter(status=PA)
     
     total=0
     for pa in propostas_aceitas:
        total = total + pa.percentual
        
    if total + float(percentual) > empresa.percentual_equity
        messagens.add_messages(request, constants.WARNING, 'o percentual solicitado ultrapassa o percentual maximo')
        return redirect(f'/investidores/ver_empresas/{id}')
    
    valuation = (100 * int(valor))/ int(percentual)
    
    if valuation < (int(empresa.valuation / 2)):
        messagens.add_messages(request, constants.WARNING, f'seu valuation proposto foi R${valuation} e deve ser no minimo {empresa.valuation}')
        return redirect(f'/investidores/ver_empresas/{id}')
    
    pi = PropostaInvestimento(
        valor = valor,
        percetual = percentual,
        empresa = empresa,
        investidor = request.user
    )
    
    pi.save()
    return redirect(f'/investidores/assinar_contrato/{pi.id}') #vai da erro por enquanto
    
def assinar_contrato(request, id):
    pi = PropostaInvestimento.objects.get(id=id)
    if pi.status != 'AS'
        raise Http404()
    
    if request.method == "GET":
        return render(request, 'assinar_contrato.html', {'id': id})
from django.shortcuts import render, HttpResponse
from .models import *
from .database_operations import *
from pyecharts import Line, Overlap
from .forms import *
import json
from django.db import *


# Create your views here.
def test(request):
    batch = 'AAFRHBCTP'


# 动态加载5个相似的批次号
def search_batch(request):
    batchs = request.GET.get('batch')
    batch_data = BatchComparison.objects.filter(batch__istartswith=batchs).values('batch').all()[0:5]
    batch_list = [i['batch'] for i in batch_data]
    msg = json.dumps(batch_list)
    return HttpResponse(msg)


# 动态查询该批次号对应该款式店铺
def search_shops(request):
    err = ''
    batchs = request.GET.get('batch')
    style_codings = request.GET.get('style')
    shops_data = SpuidComparison.objects.filter(batch=batchs, style_coding=style_codings).all()
    shops_list = [i.brand for i in shops_data]
    if len(shops_list) < 1:
        err = '该批次的该款式没有上架'
    else:
        shops_list.append('全部')
    msg = {}
    msg['errs'] = err
    msg['shop_list'] = shops_list
    msg = json.dumps(msg)
    return HttpResponse(msg)


def index(request):
    over_list = []
    style_coding_list = []
    err = ''
    batchs = ''
    style = ''
    shops_list = ''
    shops = ''
    if request.method == 'POST':
        batchs = request.POST.get('batch')
    # 判断款式号是否有误
    if len(batchs) > 0:
        # 查询款式
        style_coding_data = SpuidComparison.objects.filter(batch=batchs).values('style_coding').all()
        # 判断是否存在对应款式
        if len(style_coding_data) > 0:
            # 该款式的所有查询spuid的
            if request.method == 'POST':
                style = request.POST.get('style_coding')
                spuid_data = SpuidComparison.objects.filter(style_coding=style).all()
            else:
                spuid_data = SpuidComparison.objects.filter(style_coding=style_coding_data.first()).all()
            spuid_list = []
            for spuids in spuid_data:
                spuid_dic = {}
                spuid_dic['spuid'] = spuids.spuid
                spuid_dic['brand'] = spuids.brand
                spuid_list.append(spuid_dic)
            # 款式列表
            style_coding_data_2 = SpuidComparison.objects.filter(batch=batchs).values('style_coding').distinct().all()
            style_coding_list = [i['style_coding'] for i in style_coding_data_2]
            # 店铺列表
            shops_data = SpuidComparison.objects.filter(batch=batchs, style_coding=style).all()
            # shops_list = [i.brand for i in shops_data]
            shops_list = []
            for i in shops_data:
                tmp = {}
                tmp['brand'] = i.brand
                tmp['spuid'] = i.spuid
                shops_list.append(tmp)

            shops = request.POST.get('shopname')
            # 判断该款式是否存在spuid号
            if len(spuid_list) > 0:
                # 查询data并生成图表
                over_list = []
                if shops == '全部':
                    for shop in shops_list:
                        data = StoreDailyData.objects.filter(spuid=shop['spuid'], brand=shop['brand']).values('uv',
                                                                                                              'conversion_rate_of_order_payment',
                                                                                                              'conversion_rate_of_payment',
                                                                                                              'number_of_additional_purchases',
                                                                                                              'collection_number',
                                                                                                              'number_of_order_items', 'date').all()
                        x_list = [i['date'] for i in data]
                        y_list_1 = ['%.2f' % (i['conversion_rate_of_payment'] * 100) for i in data]
                        y_list_1_2 = []
                        for i in data:
                            if i['uv'] == 0:
                                tmp = '0.00'
                            else:
                                tmp = '%.2f' % (i['collection_number'] / i['uv'] * 100)
                            y_list_1_2.append(tmp)
                        y_list_1_3 = []
                        for i in data:
                            if i['uv'] == 0:
                                tmp = '0.00'
                            else:
                                tmp = '%.2f' % (i['number_of_additional_purchases'] / i['uv'] * 100)
                            y_list_1_3.append(tmp)
                        overlap = Overlap()
                        line = Line()
                        line.add('转化率', x_list, y_list_1, yaxis_formatter='%', is_smooth=True)
                        line.add('收藏率', x_list, y_list_1_2, yaxis_formatter='%', is_smooth=True)
                        line.add('加购率', x_list, y_list_1_3, yaxis_formatter='%', is_smooth=True)
                        line_2 = Line(shop['brand'] + '-' + shop['spuid'])
                        y_list_2 = [i['uv'] for i in data]
                        y_list_2_2 = [i['number_of_order_items'] for i in data]
                        line_2.add('UV', x_list, y_list_2, is_smooth=True)
                        line_2.add('成交量', x_list, y_list_2_2, is_smooth=True)
                        overlap.add(line_2)
                        overlap.add(line, is_add_yaxis=True, yaxis_index=1)
                        ds = overlap.render_embed()
                        over_list.append(ds)
                else:
                    spuid_all = SpuidComparison.objects.filter(batch=batchs, style_coding=style, brand=shops).all()
                    spuid_list = [i.spuid for i in spuid_all]
                    for spuid_ in spuid_list:
                        data = StoreDailyData.objects.filter(spuid=spuid_, ).values('uv', 'conversion_rate_of_order_payment',
                                                                                    'conversion_rate_of_payment',
                                                                                    'number_of_additional_purchases',
                                                                                    'collection_number',
                                                                                    'number_of_order_items', 'date').all()
                        x_list = [i['date'] for i in data]
                        y_list_1 = ['%.2f' % (i['conversion_rate_of_payment'] * 100) for i in data]
                        y_list_1_2 = []
                        for i in data:
                            if i['uv'] == 0:
                                tmp = '0.00'
                            else:
                                tmp = '%.2f' % (i['collection_number'] / i['uv'] * 100)
                            y_list_1_2.append(tmp)
                        y_list_1_3 = []
                        for i in data:
                            if i['uv'] == 0:
                                tmp = '0.00'
                            else:
                                tmp = '%.2f' % (i['number_of_additional_purchases'] / i['uv'] * 100)
                            y_list_1_3.append(tmp)
                        overlap = Overlap()
                        line = Line()
                        line.add('转化率', x_list, y_list_1, yaxis_formatter='%', is_smooth=True)
                        line.add('收藏率', x_list, y_list_1_2, yaxis_formatter='%', is_smooth=True)
                        line.add('加购率', x_list, y_list_1_3, yaxis_formatter='%', is_smooth=True)
                        line_2 = Line(shops + '-' + spuid_)
                        y_list_2 = [i['uv'] for i in data]
                        y_list_2_2 = [i['number_of_order_items'] for i in data]
                        line_2.add('UV', x_list, y_list_2, is_smooth=True)
                        line_2.add('成交量', x_list, y_list_2_2, is_smooth=True)
                        overlap.add(line_2)
                        overlap.add(line, is_add_yaxis=True, yaxis_index=1)
                        ds = overlap.render_embed()
                        over_list.append(ds)
                shops_list.append({'brand': '全部'})
            else:
                err = '该款式没有对应的spuid'
        else:
            err = '该批次没有对应的款式'
    # else:
    #     err = '批次号有误'
    batch_form = Batch()

    return render(request, 'index.html',
                  {'style_coding': style_coding_list, "line_list": over_list, 'err': err, 'batch_form': batch_form, 'batch': batchs, 'style': style,
                   'style_coding_list': style_coding_list, 'shops_list': shops_list, 'shops': shops})


# 动态验证批次号并加载对应的款式号
def search_style(request):
    batchs = request.GET.get('batch')
    style_coding_list = []
    errs = ''
    batch_exit = BatchComparison.objects.filter(batch=batchs).all()
    if len(batch_exit) > 0:
        style_coding_data = SpuidComparison.objects.filter(batch=batchs).values('style_coding').distinct().all()
        style_coding_list = [i['style_coding'] for i in style_coding_data]
        if len(style_coding_list) < 1:
            errs = '该批次号没有款式'
    else:
        errs = '批次号有误，请仔细核对'
    batch_data = BatchComparison.objects.filter(batch=batchs).all()
    for i in batch_data:
        shooting_dates = i.shooting_date
        types = i.type
        models = i.model
        locations = i.location
        stylists = i.stylist
        remarks = i.remark
    msg = {}
    msg['style_coding_list'] = style_coding_list
    msg['errs'] = errs
    msg['shooting_dates'] = str(shooting_dates)
    msg['types'] = types
    msg['models'] = models
    msg['locations'] = locations
    msg['stylists'] = stylists
    msg['remarks'] = remarks
    msg = json.dumps(msg)
    return HttpResponse(msg)

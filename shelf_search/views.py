from django.shortcuts import render, HttpResponse
from .database_operations import *
from pyecharts import Line, Overlap
from .forms import *
import json
from django.db import *


# Create your views here.
def test(request):
    batch = 'AAFRHBCTP'


def test2(request):
    db = Database_operat()
    over_list = []
    style_coding_list = []
    err = ''
    batch = ''
    if request.method == 'POST':
        batch = request.POST.get('batch')
    # 判断款式号是否有误
    if len(batch) > 0:
        # 查询款式
        style_coding_sql = "SELECT DISTINCT style_coding FROM spuid_comparison WHERE batch='%s'; " % batch
        style_coding_list = db.search_all(style_coding_sql)
        # 判断是否存在对应款式
        if len(style_coding_list) > 0:
            # 该款式的所有查询spuid的
            if request.method == 'POST':
                style = request.POST.get('style_coding')
                spuid_sql = "SELECT spuid,brand FROM spuid_comparison WHERE style_coding='%s';" % style
            else:
                spuid_sql = "SELECT spuid,brand FROM spuid_comparison WHERE style_coding='%s';" % style_coding_list[0]
            spuid_list = db.search_all(spuid_sql)
            # 判断该款式是否存在spuid号
            if len(spuid_list) > 0:
                # 查询data并生成图表
                over_list = []
                for spuid in spuid_list:
                    data_sql = "SELECT date,UV,conversion_rate_of_payment,number_of_additional_purchases,collection_number,number_of_order_items FROM store_daily_data WHERE spuid='%s';" % \
                               spuid[0]
                    data = db.search_all(data_sql)
                    x_list = [i[0] for i in data]
                    y_list_1 = ['%.2f' % (i[2] * 100) for i in data]
                    y_list_1_2 = ['%.2f' % (i[4] / i[1] * 100) for i in data]
                    y_list_1_3 = ['%.2f' % (i[3] / i[1] * 100) for i in data]
                    overlap = Overlap()
                    line = Line(spuid[1])
                    line.add('转化率', x_list, y_list_1, yaxis_formatter='%',is_smooth=True)
                    line.add('收藏率', x_list, y_list_1_2, yaxis_formatter='%',is_smooth=True )
                    line.add('加购率', x_list, y_list_1_3, yaxis_formatter='%',is_smooth=True)
                    line_2 = Line(spuid[1])
                    y_list_2 = [i[1] for i in data]
                    y_list_2_2 = [i[5] for i in data]
                    line_2.add('UV', x_list, y_list_2,is_smooth=True )
                    line_2.add('成交量', x_list, y_list_2_2,is_smooth=True)
                    overlap.add(line_2)
                    overlap.add(line, is_add_yaxis=True, yaxis_index=1)
                    ds = overlap.render_embed()
                    over_list.append(ds)
            else:
                err = '该款式没有对应的spuid'
        else:
            err = '该批次没有对应的款式'
    # else:
    #     err = '批次号有误'
    db.db.close()
    batch_form = Batch()
    return render(request, 'test.html', {'style_coding': style_coding_list, "line_list": over_list, 'err': err, 'batch_form': batch_form,'batch':batch})


def search_style(request):
    db = Database_operat()
    batch = request.GET.get('batch')
    style_coding_list = []
    errs = ''
    batch_sql = "SELECT batch FROM batch_comparison WHERE batch='%s';" % batch
    batch = db.search_all(batch_sql)
    if len(batch) > 0:
        style_coding_sql = "SELECT DISTINCT style_coding FROM spuid_comparison WHERE batch='%s'; " % batch[0]
        style_coding_list = db.search_all(style_coding_sql)
        if len(style_coding_list) > 0:
            pass
        else:
            errs = '该批次号没有款式'
    else:
        errs = '批次号有误，请仔细核对'
    msg = {}
    msg['style_coding_list'] = style_coding_list
    msg['errs'] = errs
    db.db.close()
    msg = json.dumps(msg)
    return HttpResponse(msg)

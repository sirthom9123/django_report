from django.shortcuts import render
from django.views.generic import ListView, DetailView
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Sale
from .forms import SalesSearchForm
from .utils import get_customer_from_id, get_salesman_from_id, get_chart

from reports.forms import ReportForm

@login_required
def home_view(request):
    sale_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        print(date_from, date_to, chart_type)
    
        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs) > 0:
            sale_df = pd.DataFrame(sale_qs.values())
            sale_df['customer_id'] = sale_df['customer_id'].apply(get_customer_from_id)
            sale_df['salesman_id'] = sale_df['salesman_id'].apply(get_salesman_from_id)
            sale_df['created'] = sale_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sale_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            
            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id()
                    }                
                    
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sale_df, positions_df, on='sales_id')
            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')
            
            chart = get_chart(chart_type, sale_df, results_by)


            sale_df = sale_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
        else:
            no_data = 'No data available in the date range'
        
    context = {
                'search_form': search_form, 
                'report_form': report_form,
                'no_data': no_data,
                'sale_df': sale_df, 
                'positions_df': positions_df, 
                'merged_df': merged_df, 
                'df': df, 
                'chart': chart
               }
    return render(request, 'sales/home.html', context)

class SaleListView(ListView, LoginRequiredMixin):
    model = Sale
    template_name = 'sales/main.html'
    
class SaleDetailView(DetailView, LoginRequiredMixin):
    model = Sale
    template_name = 'sales/detail.html'
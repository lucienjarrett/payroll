from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from ..forms import * 
from .. import views 
from django.test import RequestFactory
# class TimeSheetView(TemplateView):
#     pass

# class TestTimeSheetView1(FormView):
#     # form_class = TimeSheetForm
#     template_name = 'payroll/timesheet.html'

class TestTimeSheetView(FormView):
        form_class = TimeSheetForm
        template_name = 'payroll/timesheet.html'
        req = RequestFactory().get('/')
        resp = views.TimeSheetView.as_view()(req)
        assert resp.status_code == 200



from django.forms import ModelForm
from .models import * 

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','price','size']

class InboundCreateForm(ModelForm):
    class Meta:
        model = Inbound
        exclude = ['price','date']
        
class OutboundCreateForm(ModelForm):
    class Meta:
        model = Outbound
        exclude = ['price','date']
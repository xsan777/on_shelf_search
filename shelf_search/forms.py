from django import forms


class Batch(forms.Form):
    batch = forms.CharField(label='批次号',
                            widget=forms.TextInput(attrs={'placeholder': '批次号', 'class': 'form-control', 'id': 'batch','list':'batch_list',
                                                          ' autocomplete':'off','onchange':'change_style()'}))

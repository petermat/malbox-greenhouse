import django_tables2 as tables
from .models import VagrantBox


class VagrantBoxTable(tables.Table):
    class Meta:
        model = VagrantBox


class SearchApiResultsTable(tables.Table):
    #name = tables.Column()
    #name = tables.columns.TemplateColumn(template_code=u""{{ record.name }}"", orderable=True, verbose_name='Name')
    #surname = tables.columns.TemplateColumn(template_code=u""{{ record.surname }}"", orderable=True, verbose_name='Surname')
    #address = tables.columns.TemplateColumn(template_code=u""{{ record.address }}"", orderable=True, verbose_name='Address')

    tag = tables.Column()
    username = tables.Column()
    name = tables.Column()
    private = tables.BooleanColumn()
    downloads = tables.Column()
    created_at = tables.Column()
    updated_at = tables.Column()
    short_description = tables.Column()
    description_markdown = tables.Column()
    description_html = tables.Column()
    current_version = tables.JSONColumn()

    class Meta:
        attrs = {'class': 'table table-condensed table-vertical-center', 'id': 'dashboard_table'}
        #fields = ('name', 'surname', 'address')
        #sequence = fields
        #order_by = ('-name', )
        
        
        

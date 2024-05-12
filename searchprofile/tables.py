import django_tables2 as tables
from .models import Brand


class BrandTable(tables.Table):

    brand_link = tables.TemplateColumn(template_name='searchprofile/researchlink.html', orderable=False, extra_context={"target": "#newcontent"})
    name = tables.Column()

    class Meta:
        model = Brand
        fields = ("name", )
        template_name = "django_tables2/bootstrap4.html"

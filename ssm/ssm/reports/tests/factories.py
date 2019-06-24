from factory import DjangoModelFactory

from ssm.reports.models import Report, History


class ReportFactory(DjangoModelFactory):

    class Meta:
        model = Report


class HistoryFactory(DjangoModelFactory):

    class Meta:
        model = History

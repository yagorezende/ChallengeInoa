from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    """
    Modelo abstrato para controle de datas
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data do registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data da última atualização')

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


CHANNEL_CHOICES = {
    ('phone', 'Telefone'),
    ('email', 'Email'),
}

STATUS_CHOICES = {
    ('active', 'Ativo'),
    ('archived', 'Arquivado'),
}


class Contact(models.Model):
    """
    Modelo para armazenar os contatos dos usuários
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=16, choices=CHANNEL_CHOICES, null=False, blank=False)
    contact = models.CharField(max_length=256, null=False, blank=False)  # 256 chars é o limite do email vide: RFC 5321


class Stock(models.Model):
    """
    Modelo para armazenar as informações sobre as ações das empresas.
    Utilize este modelo para identificar as empresas que serão monitoradas.
    """
    company_name = models.CharField(max_length=128, null=False, blank=False)
    symbol = models.CharField(max_length=12, null=False, blank=False)


class StockPrice(models.Model):
    """
    Modelo para armazenar o preço das ações das empresas.
    NI: Será atualizado conforme o intervalo definido pelo usuário.
    """
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)
    timestamp = models.DateTimeField(null=False, blank=False)


class UserMonitorStock(TimeStampedModel):
    """
    Modelo para armazenar as informações sobre como e qual ação o usuário deseja monitorar
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='monitors')
    interval = models.PositiveIntegerField(null=False, blank=False)  # editável
    price_limit_top = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)  # editável
    price_limit_bottom = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)  # editável
    notify = models.BooleanField(default=True)  # editável
    status = models.CharField(max_length=16, null=False, blank=False, choices=STATUS_CHOICES, default='active')


class UserStockNotificationHistory(TimeStampedModel):  # 'print' do UserMonitorStock para manter histórico
    """
    Modelo para armazenar o histórico de notificações enviadas ao usuário.
    NI: Para manter o histórico, mesmo após atualização do UserMonitorStock, este modelo
    mantém uma cópia dos dados do UserMonitorStock no momento da notificação.
    """
    user_monitor_stock = models.ForeignKey(UserMonitorStock, on_delete=models.CASCADE)
    interval = models.PositiveIntegerField(null=False, blank=False)
    price_limit_top = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    price_limit_bottom = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    last_notified = models.DateTimeField(null=True, blank=True)  # Data da última notificação enviada

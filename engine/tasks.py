from datetime import datetime
from threading import Thread

from celery import shared_task
from dill import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from engine.stocks.interface import StockInterface
from standard.models import UserMonitorStock, StockPrice, UserStockNotificationHistory


@shared_task
def task_monitor(interval: int):
    """
    Task to monitor the stock prices -> run every interval minutes for each active UserMonitorStock
    IN: the task also checks if the stock price is within the limits defined by the user in a separated thread
    :param interval: interval in minutes
    :return: None
    """
    print(f"Running monitor for {interval} minutes")

    # ignore if now is weekend or after 17:00 or before 09:00
    if datetime.now().weekday() in [5, 6] or datetime.now().hour >= 17 or datetime.now().hour < 9:
        print("Ignoring monitor task")
        return None

    # load monitors
    monitors = UserMonitorStock.objects.filter(interval=interval, status='active')
    stock_api = StockInterface()
    for monitor in monitors:
        try:
            stock_data = stock_api.get_stock_price(monitor.stock, interval)
            print(f"Checking stock {monitor.stock.symbol} - {monitor.stock.company_name}")
            if stock_data:
                price = dict(stock_data.get('results')[0]) if stock_data.get('results') else None
                if price:
                    # print price now
                    stock_price = stock_api.data_to_stock_price(monitor.stock, price)
                    print(f"Price for {monitor.stock.symbol} - {monitor.stock.company_name}: {stock_price.price}")
                    # check limits in a separated thread
                    stock_thread = Thread(target=check_stock_tunnel_limits, args=(monitor, stock_price))
                    stock_thread.start()
        except Exception as e:
            print(f"Error on monitor {monitor.stock.symbol} - {monitor.stock.company_name}: {str(e)}")


def check_stock_tunnel_limits(monitor: UserMonitorStock, stock_price: StockPrice):
    """
    Check if the stock price is within the limits defined by the user
    :param monitor:
    :param stock_price:
    :return:
    """

    # check if the user has already been notified
    today_midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59)

    last_notification = UserStockNotificationHistory.objects.filter(
        user_monitor_stock=monitor,
        last_notified__range=[today_midnight, today_end]
    )
    if last_notification.exists():
        print(f"User {monitor.user.email} already notified for {monitor.stock.symbol} - {monitor.stock.company_name}")
        return

    tip = None
    if monitor.price_limit_top <= stock_price.price:
        print(f"Stock {monitor.stock.symbol} - {monitor.stock.company_name} reached the top limit")
        # send notification to sell
        tip = 'VENDA'

    elif monitor.price_limit_bottom >= stock_price.price:
        print(f"Stock {monitor.stock.symbol} - {monitor.stock.company_name} reached the bottom limit")
        # send notification to buy
        tip = 'COMPRA'

    if tip:
        html_content = render_to_string('email.html', {
            'monitor': monitor,
            'stock_price': stock_price,
            'tip': tip
        })
        text_content = strip_tags(html_content)
        send_email_task(
            subject=f'[{tip}] INOA Stocks',
            message=text_content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[monitor.user.email]
        )
    return None


@shared_task(queue='email_queue')
def send_email_task(subject, message, from_email, recipient_list, monitor):
    """
    Task to send email
    :param subject: message subject
    :param message: email message or body
    :param from_email: sender email
    :param recipient_list: list of recipients
    :param monitor: UserMonitorStock instance
    :return: None
    """
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(message, "text/html")
    status = email.send()
    # Save notification history
    if status: # status == number of emails sent -> if all successful, status == len(recipient_list)
        print(f"Email sent to {recipient_list}")
        UserStockNotificationHistory.objects.create(
            user_monitor_stock=monitor,
            interval=monitor.interval,
            price_limit_top=monitor.price_limit_top,
            price_limit_bottom=monitor.price_limit_bottom,
            last_notified=datetime.now()
        )

import logging

from aiogram import Dispatcher

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    log.info("Configure handlers...")
    from .bot.start import register_start
    from .bot.help import register_help

    from .main_menu import register_main_menu
    from .bot.about import register_about
    from .contacts import register_contacts, register_support

    from .verify_user import register_verification
    from .debt import register_debt, register_remind_payment
    from .news import register_news
    from .meters import register_meters, register_submit_meters
    from .bids import register_add_bid, register_new_bid, \
        register_order_certificate, register_contact_specialist, \
        register_choose_service
    from .bot.echo import register_echo

    register_help(dp)
    register_start(dp)
    register_main_menu(dp)
    register_verification(dp)
    register_debt(dp)
    register_remind_payment(dp)
    register_contacts(dp)
    register_news(dp)
    register_about(dp)
    register_meters(dp)
    register_submit_meters(dp)
    register_add_bid(dp)
    register_order_certificate(dp)
    register_contact_specialist(dp)
    register_choose_service(dp)
    register_support(dp)
    register_new_bid(dp)
    register_echo(dp)

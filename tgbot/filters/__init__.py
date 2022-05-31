import logging

from aiogram import Dispatcher

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    log.info("Configure filters...")
    from .verified import VerifiedUsersOnly
    from .not_verified import NotVerifiedUsersOnly

    dp.filters_factory.bind(VerifiedUsersOnly)
    dp.filters_factory.bind(NotVerifiedUsersOnly)

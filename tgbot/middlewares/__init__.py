import logging

from aiogram import Dispatcher

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    log.info("Configure middlewares...")
    # from .acl import ACLMiddleware
    from .album import AlbumMiddleware

    # dp.middleware.setup(ACLMiddleware())
    dp.middleware.setup(AlbumMiddleware())

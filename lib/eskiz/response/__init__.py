"""
the responses of eskiz
"""
from .login import LoginResponse # noqa
from .refresh import RefreshTokenResponse # noqa
from .user import UserResponse # noqa
from .send import SendSMSResponse # noqa
from .limit import GetLimitResponse # noqa
from .batch import SendBatchSMSResponse, SendGlobalSMSResponse # noqa
from .messages import (
    GetUserMessagesResponse, GetDispatchStatusResponse, MessageStatusResponse
) # noqa
from .reports import TotalsResponse, UserTotalsResponse # noqa
from .templates import TemplatesResponse # noqa
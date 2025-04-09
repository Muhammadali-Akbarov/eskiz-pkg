"""
init requests of eskiz
"""
from .login import LoginRequest # noqa
from .send import SendSMSRequest # noqa
from .batch import SendBatchSMSRequest, SendGlobalSMSRequest # noqa
from .messages import (
    GetUserMessagesRequest, GetUserMessagesByDispatchRequest,
    GetDispatchStatusRequest, ExportMessagesRequest
) # noqa
from .reports import (
    TotalsByRangeRequest, TotalsByDispatchRequest, UserTotalsRequest
) # noqa

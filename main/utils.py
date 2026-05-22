from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def push_balance_update(user, profile):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_balance",
            "balance": float(profile.balance),
            "interest": float(profile.interest_balance)
        }
    )


def push_support_message(user, message, sender):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "support_message",
            "message": message,
            "sender": sender
        }
    )
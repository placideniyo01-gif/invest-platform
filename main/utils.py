from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_admin(data):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "admin_live",
        {
            "type": "send_update",
            "data": data
        }
    )


def send_live_update(data):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "admin_live",
        {
            "type": "send_update",
            "data": data
        }
    )
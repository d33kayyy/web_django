# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def live_notify_count(context, badge_id='live_notify_badge', classes=""):
    user = user_context(context)
    if not user:
        return ''

    html = "<i id='{badge_id}' data-count='{unread}' class='{classes}'></i>".format(badge_id=badge_id,
                                                                                    classes=classes,
                                                                                    unread=user.notifications.unread().count()
                                                                                    )
    return format_html(html)


def user_context(context):
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user
    if user.is_anonymous():
        return None
    return user

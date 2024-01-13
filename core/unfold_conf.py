import random

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "HEAT Warehouse Admin",
    "SITE_HEADER": "HEAT Warehouse Admin",
    "SITE_URL": "https://heat-management-system.vercel.app",
    "SITE_ICON": lambda request: static("assets/img/store-icon.png"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("assets/img/admin-logo.svg"),  # dark mode
    # },
    # # "SITE_LOGO": lambda request: static("assets/img/store-icon.png"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("assets/img/welcome-logo.svg"),  # light mode
    #     "dark": lambda request: static("assets/img/admin-logo.svg"),  # dark mode
    # },
    "SITE_SYMBOL": "store",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "ENVIRONMENT": "core.unfold_conf.environment_callback",
    "DASHBOARD_CALLBACK": "core.unfold_conf.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("assets/img/warehouse-vector.jpg"),
    },
    "STYLES": [
        lambda request: static("assets/css/main.css"),
    ],
    "SCRIPTS": [
        lambda request: static("assets/js/admin.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uz": "🇺🇿",
                "ru": "🇷🇺",
                "en": "🇬🇧",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "badge": "core.unfold_conf.badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Warehouse"),
                "separator": True,
                "items": [
                    {
                        "title": _("Orders"),
                        "icon": "shopping_cart",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:warehouse_order_changelist"),
                    },
                    {
                        "title": _("Products"),
                        "icon": "receipt",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:warehouse_product_changelist"),
                    },
                ],
            },
            # Common
            {
                # "title": _("Common"),
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": _("Common"),
                        "icon": "tune",
                        "link": reverse_lazy("admin:common_versionhistory_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "common.versionhistory",
                "common.frontendtranslation",
            ],
            "items": [
                {
                    "title": _("Version History"),
                    "link": reverse_lazy("admin:common_versionhistory_changelist"),
                },
                {
                    "title": _("Frontend Translation"),
                    "link": reverse_lazy("admin:common_frontendtranslation_changelist"),
                },
            ],
        },
        {
            "models": [
                "warehouse.order",
                "warehouse.orderitem",
            ],
            "items": [
                {
                    "title": _("Orders"),
                    "link": reverse_lazy("admin:warehouse_order_changelist"),
                },
                {
                    "title": _("Order Items"),
                    "link": reverse_lazy("admin:warehouse_orderitem_changelist"),
                },
            ],
        },
        {
            "models": [
                "warehouse.product",
                "warehouse.productunit",
            ],
            "items": [
                {
                    "title": _("Products"),
                    "link": reverse_lazy("admin:warehouse_product_changelist"),
                },
                {
                    "title": _("Product Units"),
                    "link": reverse_lazy("admin:warehouse_productunit_changelist"),
                },
            ],
        },
    ],
}


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "sample": "example",  # this will be injected into templates/admin/index.html
            "adminTheme": "light",  # light or dark
        }
    )
    return context


def badge_callback(request):
    return f"+{random.randint(1, 100)}"


def permission_callback(request):
    return request.user.has_perm("sample_app.change_model")


def environment_callback(request):
    """
    Callback has to return a list of two values representing text value and the color
    type of the label displayed in top right corner.
    """

    if settings.DEBUG:
        return ["Development", "warning"]

    return ["Production", "success"]  # info, danger, warning, success

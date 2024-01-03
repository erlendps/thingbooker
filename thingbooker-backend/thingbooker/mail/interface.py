from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

if TYPE_CHECKING:
    from typing import Any

    from django.template import Template


class EmailInterface:
    """Interface for creating email and sending them."""

    TEMPLATE_PREFIX = "mail/"

    @classmethod
    def _get_templates(cls, template_name: str):
        """Fetches the txt version of the template and if it exists the HTML version"""

        templates: dict[str, Template] = {}

        txt_template: Template = get_template(cls.TEMPLATE_PREFIX + template_name + ".txt")
        templates["txt"] = txt_template

        # try fetching html version as well
        try:
            html_template: Template = get_template(cls.TEMPLATE_PREFIX + template_name + ".html")
            templates["html"] = html_template
        except TemplateDoesNotExist:
            pass

        return templates

    @classmethod
    def _render_templates(cls, templates: dict[str, Template], context: dict[str, Any]):
        """Renders a list of templates with the given context."""

        rendered_templates: dict[str, str] = {}

        for key, template in templates.items():
            rendered: str = template.render(context)
            rendered_templates[key] = rendered

        return rendered_templates

    @classmethod
    def send_mail(
        cls,
        *,
        template_name: str,
        context: dict[str, Any],
        to_address: str,
        subject: str,
        from_address: str = "tb@thingbooker.no",
    ):
        """Fetches and renders the templates, then sends them to the receiver"""

        templates = cls._get_templates(template_name)
        messages = cls._render_templates(templates, context)

        msg = EmailMultiAlternatives(
            subject=subject, body=messages["txt"], from_email=from_address, to=to_address
        )
        if "html" in messages:
            msg.attach_alternative(messages["html"], "text/html")

        return msg.send()

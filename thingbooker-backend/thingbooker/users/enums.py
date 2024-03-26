from django.db.models import TextChoices


class MembershipStatusEnum(TextChoices):
    """Enum for status of a (potential) member in a group or a thing"""

    NOT_MEMBER = ("not_member", "User is not a member and hasn't any active invites")
    SENT_INVITE = ("sent_invite", "An invite has been sent to the user")
    ALREADY_INVITED = ("already_invited", "User is not a member, but has an active invitation")
    MEMBER = ("member", "User is a member of the group")


class InviteStatusEnum(TextChoices):
    """Enum for status of an invitation"""

    TOKEN_EXPIRED = ("token_expired", "Token has expired, request a new one.")
    TOKEN_USED = ("token_used", "Token is already used.")
    TOKEN_CONSUMED = ("token_consumed", "Token has been consumed.")

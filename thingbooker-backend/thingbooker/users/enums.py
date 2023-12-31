from enum import EnumMeta

from choicesenum import ChoicesEnum


class GroupMemberStatusEnum(ChoicesEnum, metaclass=EnumMeta):
    """Enum for status of a (potential) member in a group"""

    NOT_MEMBER = (0, "User is not a member and hasn't any active invites")
    SENT_INVITE = (1, "An invite has been sent to the user")
    ALREADY_INVITED = (2, "User is not a member, but has an active invitation")
    MEMBER = (3, "User is a member of the group")


class InviteStatusEnum(ChoicesEnum, metaclass=EnumMeta):
    """Enum for status of an invitation"""

    TOKEN_EXPIRED = ("token_expired", "Token has expired, request a new one.")
    TOKEN_USED = ("token_used", "Token is already used.")
    TOKEN_CONSUMED = ("token_consumed", "Token has been consumed.")

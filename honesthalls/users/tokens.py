from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, profile, timestamp):
        return (
            six.text_type(profile.user.pk) + six.text_type(timestamp) +
            six.text_type(profile.verified)
        )

verification_token = TokenGenerator()

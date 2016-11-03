from django.contrib.sessions.backends.db import SessionStore as DBStore
import sf_user

class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        return sf_user.models.CustomSession

    def create_model_instance(self, data):
        obj = super(SessionStore, self).create_model_instance(data)
        try:
            account_id = int(data.get('_auth_user_id'))
        except (ValueError, TypeError):
            account_id = None
        obj.account_id = account_id
        return obj
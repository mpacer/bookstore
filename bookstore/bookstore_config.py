from traitlets import (
    Any,
    Bool,
    Dict,
    Instance,
    List,
    TraitError,
    Type,
    Unicode,
    validate,
    default,
)

from traitlets.config import LoggingConfigurable

class BookstoreS3Settings(LoggingConfigurable):
    # Allowed to not set these as we can pick up IAM roles instead
    access_key_id = Unicode(
        help="S3/AWS access key ID", allow_none=True, default_value=None).tag(
            config=True, env="JPYNB_S3_ACCESS_KEY_ID")
    secret_access_key = Unicode(
        help="S3/AWS secret access key", allow_none=True, default_value=None).tag(
            config=True, env="JPYNB_S3_SECRET_ACCESS_KEY")

    endpoint_url = Unicode(
        "https://s3.amazonaws.com", help="S3 endpoint URL").tag(
            config=True, env="JPYNB_S3_ENDPOINT_URL")
    region_name = Unicode(
        "us-east-1", help="Region name").tag(
            config=True, env="JPYNB_S3_REGION_NAME")
    bucket = Unicode(
        "notebooks", help="Bucket name to store notebooks").tag(
            config=True, env="JPYNB_S3_BUCKET")


class Bookstore(LoggingConfigurable):
    workspace_prefix = Unicode("workspace", help="Prefix for the live workspace notebooks").tag(config=True)
    published_prefix = Unicode("published", help="Prefix for published notebooks").tag(config=True)

    storage_class = Type(BookstoreS3Settings, help="Class for settings").tag(config=True)
    storage_settings = Instance(klass=LoggingConfigurable,
                                help="Instance of settings object used in Bookstore",
                                allow_none=True)

    @default('storage_settings')
    def _storage_settings_default(self):
        return self.storage_class(parent=self)

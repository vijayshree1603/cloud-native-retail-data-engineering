"""Raw-file storage abstraction with local and S3-compatible implementations."""

from abc import ABC, abstractmethod
from pathlib import Path

from src.config import LOCAL_STORAGE_PATH, RAW_DATA_KEY, S3_BUCKET, S3_PREFIX, STORAGE_BACKEND


class ObjectStorage(ABC):
    @abstractmethod
    def get_local_path(self, key: str) -> Path:
        """Return a local path for the requested object, downloading if required."""


class LocalObjectStorage(ObjectStorage):
    def __init__(self, root: Path = LOCAL_STORAGE_PATH):
        self.root = Path(root)

    def get_local_path(self, key: str) -> Path:
        return self.root / key


class S3ObjectStorage(ObjectStorage):
    def __init__(self, bucket: str = S3_BUCKET, prefix: str = S3_PREFIX):
        if not bucket:
            raise ValueError("S3_BUCKET is required when STORAGE_BACKEND=s3.")
        self.bucket, self.prefix = bucket, prefix.strip("/")

    def get_local_path(self, key: str) -> Path:
        try:
            import boto3
        except ImportError as error:
            raise RuntimeError("Install boto3 to use S3 object storage.") from error
        destination = Path("/tmp") / Path(key).name
        object_key = f"{self.prefix}/{key}" if self.prefix else key
        boto3.client("s3").download_file(self.bucket, object_key, str(destination))
        return destination


def get_object_storage() -> ObjectStorage:
    if STORAGE_BACKEND == "local":
        return LocalObjectStorage()
    if STORAGE_BACKEND == "s3":
        return S3ObjectStorage()
    raise ValueError("STORAGE_BACKEND must be 'local' or 's3'.")


def get_raw_data_path() -> Path:
    return get_object_storage().get_local_path(RAW_DATA_KEY)

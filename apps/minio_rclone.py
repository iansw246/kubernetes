from transpire.resources import Secret
from secrets import token_urlsafe

name = "minio-rclone"


def objects():
    yield {
        "apiVersion": "batch/v1",
        "kind": "CronJob",
        "metadata": {"name": "rclone-job"},
        "spec": {
            "schedule": "00 00 * * *",
            "jobTemplate": {
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "rclone",
                                    # TODO: Insert custom image
                                    "image": "rclone/rclone",
                                    "imagePullPolicy": "IfNotPresent",
                                    "env": [
                                        {
                                            "name": "O3_ACCESS_KEY",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "o3-backup-credentials",
                                                    "key": "o3-access-key",
                                                }
                                            },
                                        },
                                        {
                                            "name": "O3_SECRET_KEY",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "o3-backup-credentials",
                                                    "key": "o3-secret-key",
                                                }
                                            },
                                        },
                                        {
                                            "name": "MINIO_ROOT_USER",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "o3-backup-credentials",
                                                    "key": "minio-root-user",
                                                }
                                            },
                                        },
                                        {
                                            "name": "MINIO_ROOT_PASSWORD",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": "o3-backup-credentials",
                                                    "key": "minio-root-password",
                                                }
                                            },
                                        },
                                    ],
                                },
                            ],
                            "restartPolicy": "OnFailure",
                        }
                    }
                }
            },
        },
    }

    yield Secret(
        name="o3-backup-credentials",
        string_data={
            "o3-access-key": token_urlsafe(24),
            "o3-secret-key": token_urlsafe(24),
            "minio-root-user": token_urlsafe(24),
            "minio-root-password": token_urlsafe(24),
        },
    ).build()

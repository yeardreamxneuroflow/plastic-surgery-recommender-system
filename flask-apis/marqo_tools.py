"""Handling Marqo from Flask server.
"""


from typing import List

import marqo
import boto3
from PIL import Image

from macro import MarqoMacro, AWSMacro, MediaPipeMacro


def insert_landmarks_to_marqo(wannabe_list: List[str]) -> None:
    """Get extracted landmarks from S3 and insert it to Marqo.
    """

    mq_macro = MarqoMacro()
    aws_macro = AWSMacro()
    mp_macro = MediaPipeMacro()

    mq = marqo.Client(
        f"http://{mq_macro.VECTOR_DB_IP}:{mq_macro.VECTOR_DB_PORT}")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_macro.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_macro.AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )

    for wannabe in wannabe_list:
        for landmark in mp_macro.Landmark.DEFINED_LANDMARKS:
            img_url = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": aws_macro.AWS_MANUAL_WANNABE_BUCKET_NAME,
                    "Key": f"{wannabe}/{landmark}.jpg",
                },
                ExpiresIn=aws_macro.S3_URL_EXPIRATION,
            )
            r = mq.index(landmark).add_documents(
                [
                    {
                        "img": img_url,
                        "wannabe_is": wannabe,
                    },
                ],
                tensor_fields=["img"],
            )
            r  # Breakpoint


def infer_landmarks(user_timestamp: str) -> List[str]:
    """Get most similar wannabe landmark per each landmark.
    """

    mq_macro = MarqoMacro()
    aws_macro = AWSMacro()
    mp_macro = MediaPipeMacro()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_macro.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_macro.AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )

    mq = marqo.Client(
        f"http://{mq_macro.VECTOR_DB_IP}:{mq_macro.VECTOR_DB_PORT}")

    for landmark in mp_macro.Landmark.DEFINED_LANDMARKS:
        # TODO: DELETE REDEFINITION AFTER TEST
        user_timestamp = "1703491543.5945203"
        landmark_img_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": aws_macro.AWS_USER_LANDMARK_BUCKET_NAME,
                "Key": f"{user_timestamp}/{landmark}.jpg",
            },
            ExpiresIn=aws_macro.S3_URL_EXPIRATION,
        )

        # TODO: Fix `MarqoWebError`
        r = mq.index(landmark).search(q=landmark_img_url)
        pass

        # TODO: Process `r` and return result that processed from `r`


if __name__ == "__main__":
    """Manual image data insertion.
    """

    wannabe_list = [
        "박보검",
        "뷔",
        "서강준",
        "송강",
        "송중기",
        "신세경",
        "아이린",
        "아이유",
        "오연서",
        "윈터",
        "육성재",
        "윤아",
        "이주빈",
        "장원영",
        "정국",
        "정우성",
        "제니",
        "차은우",
        "카리나",
    ]

    insert_landmarks_to_marqo(wannabe_list=wannabe_list)

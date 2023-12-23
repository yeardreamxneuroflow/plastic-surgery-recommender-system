from typing import List

import marqo
import boto3

from face_landmark_macro import DEFINED_LANDMARKS
from marqo_macro import VECTOR_DB_IP, VECTOR_DB_PORT
from aws_macro import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from aws_macro import AWS_MANUAL_WANNABE_BUCKET_NAME, S3_URL_EXPIRATION


def insert_landmarks_to_marqo(wannabe_list: List[str]) -> None:
    """Insert Extracted Landmarks from S3 Bucket to Marqo
    """

    mq = marqo.Client(f"http://{VECTOR_DB_IP}:{VECTOR_DB_PORT}")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )

    for wannabe in wannabe_list:
        for landmark in DEFINED_LANDMARKS:
            # landmark_path = f"s3://{AWS_MANUAL_WANNABE_BUCKET_NAME}/{wannabe}/{landmark}.jpg"
            img_url = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": AWS_MANUAL_WANNABE_BUCKET_NAME,
                    "Key": f"{wannabe}/{landmark}.jpg",
                },
                ExpiresIn=S3_URL_EXPIRATION,
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
            r  # BP


def infer_landmarks(face_landmark_imgs: list) -> list[str]:
    # ret = [
    #     [
    #         wannabe,
    #         score,
    #     ],
    #     ...
    # ]

    mq = marqo.Client(f"http://{VECTOR_DB_IP}:{VECTOR_DB_PORT}")

    for idx, img in enumerate(face_landmark_imgs):
        if idx == 0:
            landmark = "left-eye"
        elif idx == 1:
            landmark = "right-eye"
        elif idx == 2:
            landmark = "nose"
        elif idx == 3:
            landmark = "lips"

        r = mq.index(landmark).search(q=img)
        r  # Currently blocked by for manual landmark insertion


# Manual Image Data Insertion
if __name__ == "__main__":
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
    insert_landmarks_to_marqo(wannabe_list)

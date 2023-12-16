from PIL import Image

import marqo

from marqo_macro import VECTOR_DB_IP, VECTOR_DB_PORT


def insert_landmarks_manually():
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
    wannabe_landmark_imgs = []

    # Read landmark images from local
    for wannabe in wannabe_list:
        four_landmarks = []
        for landmark in ["left-eye", "right-eye", "nose", "lips"]:
            with Image.open(f"manual_images/{wannabe}/{landmark}.jpg") as im:
                four_landmarks.append(im)
        wannabe_landmark_imgs.append(four_landmarks)

    insert_landmarks_to_marqo(
        wannabe_list,
        wannabe_landmark_imgs,
    )


def insert_landmarks_to_marqo(
    wannabe_list: list[str],
    wannabe_landmark_imgs: list[list[Image]],
):
    mq = marqo.Client(f"http://{VECTOR_DB_IP}:{VECTOR_DB_PORT}")

    for wannabe_idx, wannabe in enumerate(wannabe_list):
        for img_idx, img in enumerate(wannabe_landmark_imgs[wannabe_idx]):
            if img_idx == 0:
                landmark = "left-eye"
            elif img_idx == 1:
                landmark = "right-eye"
            elif img_idx == 2:
                landmark = "nose"
            elif img_idx == 3:
                landmark = "lips"

            # TODO: Fix `TypeError: Object of type JpegImageFile is not JSON serializable`
            mq.index(landmark).add_documents(
                [
                    {
                        "img": img,
                        "wannabe_is": wannabe,
                    },
                ],
                tensor_fields=["img"],
            )


def infer_landmarks(face_landmark_imgs: list[Image]) -> list[str]:
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


# Manual Image Data Insertion Only
if __name__ == "__main__":
    insert_landmarks_manually()

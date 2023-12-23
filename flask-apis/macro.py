"""Intergrated Module to Handle Multiple Macros
"""


import os
from abc import ABC
from typing import List


class MacroUsingEnvVar(ABC):
    """Boilerplate for Macro using OS Environment Variable
    """

    def __init__(self, env_var_list: List[str]):
        self.env_var_list = []

        for env_var in env_var_list:
            self.env_var_list.append(env_var)

        self.get_value()

    def get_value(self):
        """Get Each Values from Environment Variable Using getenv()
        """

        for env_var in self.env_var_list:
            setattr(self, env_var, os.getenv(env_var))
            assert getattr(self, env_var) is not None, \
                f"{env_var} environment variable is not set."


class AWSMacro(MacroUsingEnvVar):
    """Define Macros to Operate AWS Reosurce-related Operations
    """

    def __init__(self):
        self.S3_URL_EXPIRATION = 10  # Seconds
        aws_env_var_list = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_WANNABE_BUCKET_NAME",
            "AWS_MANUAL_WANNABE_BUCKET_NAME",
        ]
        super().__init__(aws_env_var_list)


class MarqoMacro(MacroUsingEnvVar):
    """Define Macros to Operate VectorDB-related Operations
    """

    def __init__(self):
        marqo_env_var_list = [
            "VECTOR_DB_IP",
            "VECTOR_DB_PORT",
        ]
        super().__init__(marqo_env_var_list)


class ScrapyMacro(MacroUsingEnvVar):
    """Define Macros to Operate Scrapy-related Operations
    """

    def __init__(self):
        scrapy_env_var_list = [
            "SCRAPER_NODE_IP",
            "SCRAPER_NODE_PORT",
        ]
        super().__init__(scrapy_env_var_list)


class MediaPipeMacro:
    """Defined Macros to Operate MediaPipe-related Operations
    """

    class __Index:
        def __init__(self):
            self.LEFT_EYE_LEFT_EDGE = 359
            self.LEFT_EYE_TOP_EDGE = 257
            self.LEFT_EYE_RIGHT_EDGE = 362
            self.LEFT_EYE_BOTTOM_EDGE = 449

            self.RIGHT_EYE_LEFT_EDGE = 133
            self.RIGHT_EYE_TOP_EDGE = 27
            self.RIGHT_EYE_RIGHT_EDGE = 226
            self.RIGHT_EYE_BOTTOM_EDGE = 229

            self.NOSE_LEFT_EDGE = 64
            self.NOSE_TOP_EDGE = 27
            self.NOSE_RIGHT_EDGE = 294
            self.NOSE_BOTTOM_EDGE = 2

            self.LIPS_LEFT_EDGE = 61
            self.LIPS_TOP_EDGE = 267
            self.LIPS_RIGHT_EDGE = 291
            self.LIPS_BOTTOM_EDGE = 17

    class __Landmark:
        def __init__(self):
            self.DEFINED_LANDMARKS = [
                "left-eye",
                "right-eye",
                "nose",
                "lips",
            ]

    def __init__(self):
        self.Index = MediaPipeMacro.__Index()
        self.Landmark = MediaPipeMacro.__Landmark()

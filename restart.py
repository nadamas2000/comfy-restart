"""
ComfyUI Restart Node.

This module implements a ComfyUI custom node that requests
a ComfyUI process restart after workflow completion.

The node is designed as an OUTPUT_NODE, following the same
execution model used by ComfyUI nodes such as PreviewImage
and SaveImage.

The node does not restart the container. It terminates the
ComfyUI Python process. A supervisor script (for example
start-comfy.py) is responsible for launching ComfyUI again.

The input socket accepts any ComfyUI data type and is only used
as an execution trigger.
"""

import os
import threading
import time


class RestartComfyUI:
    """
    ComfyUI output node that terminates the current process
    after a configurable delay.

    The node intentionally does not return workflow data because
    it represents the final stage of execution.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Define node inputs.

        Returns:
            dict:
                ComfyUI input definition.
        """

        return {
            "required": {
                "input": (
                    "*",
                    {}
                ),

                "delay_seconds": (
                    "INT",
                    {
                        "default": 5,
                        "min": 1,
                        "max": 60
                    }
                )
            }
        }


    RETURN_TYPES = ()

    FUNCTION = "restart"

    OUTPUT_NODE = True

    CATEGORY = "utils"


    def restart(self, input, delay_seconds):
        """
        Schedule the ComfyUI process termination.

        Args:
            input:
                Any object received from the previous node.
                It is only used as an execution trigger.

            delay_seconds:
                Number of seconds before terminating ComfyUI.

        Returns:
            dict:
                UI information displayed by ComfyUI.
        """

        def delayed_exit():
            """
            Wait and terminate the current Python process.
            """

            time.sleep(delay_seconds)

            os._exit(0)


        thread = threading.Thread(
            target=delayed_exit,
            daemon=True
        )

        thread.start()


        return {
            "ui": {
                "text": [
                    f"Restarting ComfyUI in {delay_seconds}s"
                ]
            }
        }


NODE_CLASS_MAPPINGS = {
    "RestartComfyUI": RestartComfyUI
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "RestartComfyUI": "Restart ComfyUI"
}
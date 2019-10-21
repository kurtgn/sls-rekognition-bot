from typing import List

from .rekognition import Emotion


def emotions_summary(emotions: List[Emotion]):
    """
    Create a text with emotions and rounded confidence, like so:

    HAPPY: 99.87
    SURPRISED: 0.07
    ANGRY: 0.03
    FEAR: 0.01
    CONFUSED: 0.01
    CALM: 0.01
    DISGUSTED: 0.01
    SAD: 0.0

    """
    return '\n'.join(
        f'{e.type}: {round(e.confidence, 2)}' for e in emotions
    )

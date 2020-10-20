"""not sure what I'm doing here..."""

import json
from pathlib import Path
import re

class AwsTranscript(object):
    def __init__(obj:dict):
        self._data = obj



    ######################################
    ### just tentative draft stuff below
    # @property
    # def is_completed(self) -> bool:
    #     return self.status == 'COMPLETED'

    # @property
    # def items(self) -> list:
    #     return self.results['items']


    # @property
    # def job_name(self) -> str:
    #     return self._data['jobName']

    # @property
    # def results(self) -> dict:
    #     return self._data['results']

    # @property
    # def speaker_count(self) -> int:
    #     return self.speaker_labels['speakers'] if self.speaker_labels else None

    # @property
    # def speaker_labels(self) -> dict:
    #     return self.results.get('speaker_labels')


    # @property
    # def status(self) -> str:
    #     return self._data['status']


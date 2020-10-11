
from seshkit.clients.aws import AWSClient
from pathlib import Path as StdPath


class TranscribeClient(AWSClient):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html
    """
    aws_service = 'transcribe'
    MEDIA_FORMATS = ('mp3', 'mp4', 'wav', 'flac', 'ogg', 'amr', 'webm',)


    def start_job(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService.Client.start_transcription_job

        response = client.start_transcription_job(
            TranscriptionJobName='string',
            LanguageCode='af-ZA'|'ar-AE'|'ar-SA'|'cy-GB'|'da-DK'|'de-CH'|'de-DE'|'en-AB'|'en-AU'|'en-GB'|'en-IE'|'en-IN'|'en-US'|'en-WL'|'es-ES'|'es-US'|'fa-IR'|'fr-CA'|'fr-FR'|'ga-IE'|'gd-GB'|'he-IL'|'hi-IN'|'id-ID'|'it-IT'|'ja-JP'|'ko-KR'|'ms-MY'|'nl-NL'|'pt-BR'|'pt-PT'|'ru-RU'|'ta-IN'|'te-IN'|'tr-TR'|'zh-CN',
            MediaSampleRateHertz=123,
            MediaFormat='mp3'|'mp4'|'wav'|'flac'|'ogg'|'amr'|'webm',
            Media={
                'MediaFileUri': 'string'
            },
            OutputBucketName='string',
            OutputKey='string',
            OutputEncryptionKMSKeyId='string',
            Settings={
                'VocabularyName': 'string',
                'ShowSpeakerLabels': True|False,
                'MaxSpeakerLabels': 123,
                'ChannelIdentification': True|False,
                'ShowAlternatives': True|False,
                'MaxAlternatives': 123,
                'VocabularyFilterName': 'string',
                'VocabularyFilterMethod': 'remove'|'mask'
            },
            ModelSettings={
                'LanguageModelName': 'string'
            },
            JobExecutionSettings={
                'AllowDeferredExecution': True|False,
                'DataAccessRoleArn': 'string'
            },
            ContentRedaction={
                'RedactionType': 'PII',
                'RedactionOutput': 'redacted'|'redacted_and_unredacted'
            },
            IdentifyLanguage=True|False,
            LanguageOptions=[
                'af-ZA'|'ar-AE'|'ar-SA'|'cy-GB'|'da-DK'|'de-CH'|'de-DE'|'en-AB'|'en-AU'|'en-GB'|'en-IE'|'en-IN'|'en-US'|'en-WL'|'es-ES'|'es-US'|'fa-IR'|'fr-CA'|'fr-FR'|'ga-IE'|'gd-GB'|'he-IL'|'hi-IN'|'id-ID'|'it-IT'|'ja-JP'|'ko-KR'|'ms-MY'|'nl-NL'|'pt-BR'|'pt-PT'|'ru-RU'|'ta-IN'|'te-IN'|'tr-TR'|'zh-CN',
            ]
        )
        """
        pass

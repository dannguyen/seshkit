**********************************************************
Example of AWS transcribe using awscli - multiple speakers
**********************************************************

.. contents:: :local:


S3 upload
=========

.. code-block:: sh

    aws s3 cp --profile seshkit --acl public-read \
        examples/audio/obama-romney-town-hall.mp3 \
        s3://test-seshkit-input-bucket/seshkit-input/obama-romney-town-hall.mp3


Transcribe
==========


Start job call
--------------

.. code-block:: sh

    aws transcribe start-transcription-job \
        --profile seshkit \
        --language-code 'en-US' \
        --media-format 'mp3' \
        --transcription-job-name 'obama-romney-town-hall' \
        --media '{"MediaFileUri": "s3://test-seshkit-input-bucket/seshkit-input/obama-romney-town-hall.mp3"}' \
        --output-key 'seshkit-output/obama-romney-town-hall.json' \
        --output-bucket-name 'test-seshkit-output-bucket' \
        --settings '{"ShowSpeakerLabels": true, "MaxSpeakerLabels": 4, "ShowAlternatives": true, "MaxAlternatives": 3}'



Start job response
------------------

.. code-block:: json

    {
        "TranscriptionJob": {
            "TranscriptionJobName": "obama-romney-town-hall",
            "TranscriptionJobStatus": "IN_PROGRESS",
            "LanguageCode": "en-US",
            "MediaFormat": "mp3",
            "Media": {
                "MediaFileUri": "s3://test-seshkit-input-bucket/seshkit-input/obama-romney-town-hall.mp3"
            },
            "StartTime": 1603202924.06,
            "CreationTime": 1603202924.002,
            "Settings": {
                "ShowSpeakerLabels": true,
                "MaxSpeakerLabels": 4,
                "ShowAlternatives": true,
                "MaxAlternatives": 3
            }
        }
    }



Job status update
-----------------


.. code-block:: sh

    aws transcribe get-transcription-job \
        --profile seshkit \
        --transcription-job-name 'obama-romney-town-hall'


Response
^^^^^^^^

.. code-block:: json

    {
        "TranscriptionJob": {
            "TranscriptionJobName": "obama-romney-town-hall",
            "TranscriptionJobStatus": "IN_PROGRESS",
            "LanguageCode": "en-US",
            "MediaSampleRateHertz": 44100,
            "MediaFormat": "mp3",
            "Media": {
                "MediaFileUri": "s3://test-seshkit-input-bucket/seshkit-input/obama-romney-town-hall.mp3"
            },
            "Transcript": {},
            "StartTime": 1603202924.06,
            "CreationTime": 1603202924.002,
            "Settings": {
                "ShowSpeakerLabels": true,
                "MaxSpeakerLabels": 4,
                "ChannelIdentification": false,
                "ShowAlternatives": true,
                "MaxAlternatives": 3
            }
        }
    }


Completed job status
^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

    {
        "TranscriptionJob": {
            "TranscriptionJobName": "obama-romney-town-hall",
            "TranscriptionJobStatus": "COMPLETED",
            "LanguageCode": "en-US",
            "MediaSampleRateHertz": 44100,
            "MediaFormat": "mp3",
            "Media": {
                "MediaFileUri": "s3://test-seshkit-input-bucket/seshkit-input/obama-romney-town-hall.mp3"
            },
            "Transcript": {
                "TranscriptFileUri": "https://s3.us-east-1.amazonaws.com/test-seshkit-output-bucket/seshkit-output/obama-romney-town-hall.json"
            },
            "StartTime": 1603202924.06,
            "CreationTime": 1603202924.002,
            "CompletionTime": 1603203074.838,
            "Settings": {
                "ShowSpeakerLabels": true,
                "MaxSpeakerLabels": 4,
                "ChannelIdentification": false,
                "ShowAlternatives": true,
                "MaxAlternatives": 3
            }
        }
    }


Fetching JSON transcript with S3
--------------------------------


.. code-block:: shell

    $ aws s3 cp s3://test-seshkit-output-bucket/seshkit-output/obama-romney-town-hall.json examples/transcripts/obama-romney-town-hall.json

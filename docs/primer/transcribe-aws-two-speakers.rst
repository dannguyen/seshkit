*****************************************************
Example of AWS transcribe using awscli - two speakers
*****************************************************


.. contents:: :local:


Using awscli
============


transcribe: Request to start job
--------------------------------

.. code-block:: sh

    aws transcribe start-transcription-job \
        --profile seshkit \
        --language-code 'en-US' \
        --media-format 'mp3' \
        --transcription-job-name 'trump-clinton-debate-snippet' \
        --media '{"MediaFileUri": "s3://test-seshkit-input-bucket/seshkit-input/trump-clinton-debate-snippet.mp3"}' \
        --output-key 'seshkit-output/trump-clinton-debate-snippet.json' \
        --output-bucket-name 'test-seshkit-output-bucket' \
        --settings '{"ShowSpeakerLabels": true, "MaxSpeakerLabels": 2, "ShowAlternatives": true, "MaxAlternatives": 3}'


transcribe: Getting job status
------------------------------

.. code-block:: sh

    aws transcribe get-transcription-job \
        --profile seshkit \
        --transcription-job-name 'trump-clinton-debate-snippet'


Data responses
==============

Start job response
------------------

.. literalinclude:: /../examples/aws/transcribe/2-speakers/start-transcription-job-response.json


Job in progress
---------------

.. literalinclude:: /../examples/aws/transcribe/2-speakers/get-transcription-job-in-progress-response.json

Job is completed
----------------

.. literalinclude:: /../examples/aws/transcribe/2-speakers/get-transcription-job-completed-response.json


Transcript
----------

.. literalinclude:: /../examples/aws/transcribe/2-speakers/transcript.json

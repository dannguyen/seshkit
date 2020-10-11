# TODOS

Left off at:

- documentation in: docs/examples/transcribe-aws-cli-simple.rst
- Changed SeshProfile format to have `default_bucket` instead of `output_bucket`
- `sesh whoami` basic implementation


## 0.1.0

### overall stuff
- [x] alias seshkit to sesh
- use awscli to generate samples:
    - [x] sample job status response
    - [x] sample transcript with no speakers
    - [?] add audio files
    - sample transcript with speakers


### Commands

`sesh config`
- maybe `--config-profile` should be `-c` and not `-p`?

`sesh whoami`
- needs tests
- should throw errors:
    - when profile fails validation (e.g. missing attributes)
    - when creds file doesn't exist
    - when authentication fails

### Objects

SeshProfile
- [x] basic implementation
- [x] basic tests with isolated filesystem
- instantiated from .seshkitrc profile
    - [x] has `profile` key to specify profile in seshconfig
    - [x] if `profile` is empty, use first profile in seshconfig
    - [ ] if `profile` is empty, should use `default` profile first
- reads service_creds_file and parses it
    - [x] parses credfile based on service, e.g. knows that 'aws' refers to INI format with keys: `aws_access_key_id` and `aws_secret_access_key`


S3Client
- [x] basic implementationish
- [x] accepts SeshProfile
- list bucket contents
- list seshkit-project/*
- 
- upload_file
    - should set proper encoding/data type based on extension or --filetype argument
- head
- download


seshkit.types.path
- [x] basic implementation; not used in library yet...


### types.paths

- [ ] every path type should have a 'slug' property that attempts to be a kind of unique file reference based on filename. Can basically be "basename"

### sesh config

- no params/options
    - if ~/.seshkitrc does NOT exist
        - [x] create [default] profile
        - [x] write to ~/.seshkitrc
    - [x] always print filename and contents to stderr
- option `--profile`
    - [x] assume user wants to interactively edit it
    - [x] write to existing ~/.seshkitrc

- option `--set-default [existing_profile]`
    - [ ] create or overwrite default profile with `existing_profile`

### sesh bucket

Just a class for getting info about a bucket

- uses AWSClient    
- argument `name`: refers to name of bucket
- default behavior
    - return read/write access
    - return name of latest key(?)
- option `--init output`: make sure bucket is a valid output bucket (e.g. writable, has `seshkit-projects` subdir)
- option `--init input`: is this even needed? 

### sesh scribe

options:
- `-i/--input`
    - local path to an audio file
- `-F/--format`
    - format of audio; by default, discerned from file extension
- `-S/--id-speakers [maxnum]`
    - tells Amazon to identify a `maxnum` number of speakers
- `-p/--project-name`
    - name of project folder to create and write to; default is YYYY-MM-DD-[slug]

- `-b/--bucket`
    - output bucket; default is read from seshkitrc[profile].output_bucket
- `--profile`
    - seshkitrc profile to use; default is 'default'

## Future

### seshkit bucket

- Return information about default bucket
- `--init` Create a new bucket and configure it
    - Prompt: set as default?
    - Prompt: Make public?
- `--default` Set existing bucket as default
    - require full URL

### seshkit scribe

Prompts:
- media-format [mp3]
- uri? [filename or s3:URI or URL]
- language? [en-US]
- identify speakers? [Y]
- max speakers? [2]
- jobname? []
- output bucket? 
- await it? [yes]

### seshkit status

- --jobname get job status json
- no flags: get all current jobs

## seshkit compile/process/finish

- provide s3:URI or URL or filepath
- if project path, concatenate files

### seshkit split
- given a large audio file, split into n pieces and create a folder
- --split-on-quiet: attempt to split audio on quiet sections
- split-by-time: split on max length, give or take some seconds




### Structure of a transcribe project

- Given an audio file like: /tmp/path/to/hello-world.mp3
    - and default bucket: mybucket
- Create
    - project folder: s3://mybucket/seshkit-projects/2020_10_10_hello-world 
        - (or should date slug be appended instead of prepended, for s3 list search wildcard convenience?)
    - meta.json
        - name of original file(s)
        - project folder slug
        - s3 URI for project folder
        - configuration parameters
        - created_at
        - updated_at
        - status: in progress/completed/error
    - source:
        - ./_source/hello-world.mp3 [original]
    - audio file: ./job/audio/000.mp3 [may be processed/split/etc]
    - transcripts: ./job/transcripts/000.json
    - statuses: ./job/statuses/000.json [check for completed status]

- In progress:
    - if job/statuses/000.json is `in progress`, check after n-seconds/minutes
    - if `completed`, get job/transcripts/000.json
    - job is "done" when every job/audio/file has a corresponding transcript 

- Production/simplify:
    - check S3 folder for completion status
    - Download project folder to local drive
    - Process and compile ./job/transcripts/000.json to produced/transcript.json

Workflow:
- Create local project folder first, with `_source/` and `seshkit.json`; meta.json points to the remote work bucket
- s3 sync to remote bucket
- In remote bucket, create ./job 
- Polling consists of calling get-transcription-job and doing s3 sync on ./job
- Create ./produced/transcript.json/csv 




```sh
    aws transcribe start-transcription-job --language-code 'en-US' --media-format mp3 \
        --settings '{"ShowSpeakerLabels": true, "MaxSpeakerLabels": 4}' \
        --transcription-job-name $FNAME  \
        --media "{\"MediaFileUri\": \"s3://data.danwin.com/tmp/${FNAME}.mp3\"}" \
        --output-bucket-name 'data.danwin.com' 
```


## References

- https://gist.github.com/dannguyen/9b8c51f5bb853209f19f1a0f18f0f74c
- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html



## awscli examples


```sh
aws s3 cp --profile seshkit --output json --acl public-read \
    examples/audio/trump-fav-people.mp3 \
    s3://test-seshkit-input-bucket/audio/trump-fav-people.mp3


```

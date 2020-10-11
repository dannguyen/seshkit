# TODOS

Left off at:

- basic `sesh config` implementation
- basic `seshkit.types.path` implementation

## 0.1.0

### overall stuff

- [x] alias seshkit to sesh
- [ ] ServiceClient
    - `.seshkitrc` MUST be initialized and have existing profiles, and, presumably, valid authorizations for the services    
        - given a service (e.g. 'aws') and profile name (e.g. 'default'), read `creds_path[service_profile]`
        - use service-specific library to return interface object
- [ ] SeshProfile
    - instantiated from .seshkitrc profile


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

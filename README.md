# Epic Kitchens United

Scripts to parse the official [EPIC-KITCHENS 100](https://github.com/epic-kitchens/epic-kitchens-100-annotations) (EK) and [EPIC-SOUNDS](https://github.com/epic-kitchens/epic-sounds-annotations) (ES) annotations to a single csv file. 

To achieve this, the resulting rows in the csv describe the actions and sounds that occur in a fixed-size temporal window.

Example parsed annotations also included. 

## To install and prepare 
```
git clone https://github.com/iranroman/epic-kitchens-united.git

cd epic-kitchens-united

pip install -e .
```

Also, if you haven't please also clone the EK and ES annotations:

```
git clone https://github.com/epic-kitchens/epic-kitchens-100-annotations

git clone https://github.com/epic-kitchens/epic-sounds-annotations
```

## How to use:
We provide a script that parses user inputs via the command line. To use it run

``
python main.py DT VID_ID OUT_FILE ORIG_EK_ANN ORIG_ES_ANN EK_COLUMN_NAME_LIST ES_COLUMN_NAME_LIST
``

where:
* `DT`: the temporal window size (or timestep), in miliseconds
* `VID_ID`: the ID of the video you want to generate annotations for
* `NEW_FILEPATH`: the path and filename where the output will be generated 
* `EK_ANN_PATH`: the path to the original EK annotation csv
* `ES_ANN_PATH`: the path to the original ES annotation csv
* `EK_COLUMN_NAME_LIST`: a list with names of EK columns that we want in the output csv
    * possible column names are: `narration_id, participant_id, video_id, narration_timestamp, start_timestamp, stop_timestamp, start_frame, stop_frame, narration, verb, verb_class, noun, noun_class, all_nouns, all_noun_classes`
    * see the official [EPIC-KITCHENS 100](https://github.com/epic-kitchens/epic-kitchens-100-annotations) repo for more details about each column's meaning
* `ES_COLUMN_NAME_LIST`: a list with names of ES columns that we want in the output csv
    * possible column names are: `annotation_id, participant_id, video_id, start_timestamp, stop_timestamp, start_sample, stop_sample, description, class, class_id`
    * see the official [EPIC-SOUNDS 100](https://github.com/epic-kitchens/epic-sounds-annotations) repo for more details about each column's meaning

Specific example use:
```
python main.py 500 P01_103 out_example.csv epic-kitchens-100-annotations/EPIC_100.csv epic-sounds-annotations/EPIC_Sounds_train.csv  "['narration_id','verb','all_nouns','verb_class','all_noun_classes']" "['annotation_id','class','class_id']"
```

You can also generate output files by writing a python script:
```
import epic_kitchens_united as eku

dt = 500 
vid_id = P01_103 
new_filepath = 'out_example.csv' 
ek_old_filepath = 'epic-kitchens-100-annotations/EPIC_100.csv' 
es_old_filepath = 'epic-sounds-annotations/EPIC_Sounds_train.csv'
ek_column_name_list = "['narration_id','verb','all_nouns','verb_class','all_noun_classes']" 
es_column_name_list = "['annotation_id','class','class_id']"

eku.merge_csv(dt, vid_id, new_filepath, ek_old_filepath, es_old_filepath, ek_column_name_list, es_column_name_list)
```

## Pre-computed files
We also provide pre-computed output files for convenience. You can find them under `EKU_generated_annotations`:

* `EK_ES_train_allcols_1sec.csv`
* `EK_ES_val_allcols_1sec.csv`
* `EK_ES_train_minimalcols_1sec.csv`
* `EK_ES_val_minimalcols_1sec.csv`

* `allcols` includes all columns originally found in EK and ES
* `minimalcols` only includes EK: `narration_id, participant_id, video_id, verb, verb_class, noun, noun_class` and ES: `annotation_id, description, class, class_id`

## License
Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

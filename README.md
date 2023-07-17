# Epic Kitchens United
Scripts to parse the official [EPIC-KITCHENS 100](https://github.com/epic-kitchens/epic-kitchens-100-annotations) and [EPIC-SOUNDS](https://github.com/epic-kitchens/epic-sounds-annotations) annotations to a single csv file. Example parsed annotations also included. 

## to install 
```
pip install -e .
```

# Example use:

```
python main.py --video_id P01_103 --time_delta 0.5 --video_columns "['narration_id','verb','all_nouns','verb_class','all_noun_classes']" --sounds_columns "['annotation_id','class','class_id']"
```
import epic_kitchens_united as eku


def run(dt, vid_id, new_filepath, ek_old_filepath, es_old_filepath, ek_column_name_list, es_column_name_list):
    '''
    main function to trigger the data generation
    '''
    eku.merge_csv(dt, vid_id, new_filepath, ek_old_filepath, es_old_filepath, ek_column_name_list, es_column_name_list)


if __name__ == "__main__":
    import fire 
    fire.Fire(run)

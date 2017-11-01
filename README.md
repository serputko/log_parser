# log_parser
To parse log execute next command:
  python {project_dir}/bin/parser.py --path {path_to_logfile} --not {number_of_transactions_to_display}

Sample log is located in data/ directory
Use python {project_dir}/bin/parser.py -h to get help
    
Output example:
    max_tpm_all_transactions = 510

    GET /media/catalog/product/XXXXXX
    total_hits = 28878, percentage = 63.89%, max_tpm = 348

    GET /media/klevu_images/XXXXXX
    total_hits = 287, percentage = 0.63%, max_tpm = 26

    GET /skin/m/XXXXXX
    total_hits = 2354, percentage = 5.21%, max_tpm = 25

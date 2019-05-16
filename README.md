# Auto-Annotator-Validator
Automated annotator and validator for various models

Automated annotator, validator and trainer for various models
Currently supports EAST
Usage:
python3 main.py --option A--dataset /home/insanesac/workspace/images/myntra_test --mode 0
Parameters:
--option  - A for Annotation, V for Validation and T for Training
--dataset - Path to the dataset that requires annotation/validation/training
--mode    - 0 for East
Will generate reports which will give a list of file names which has annotation errors
To Do:

Implement same for other models
Data visualization for validation module
10%random sample validation option instead of validating entire data

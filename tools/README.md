Tools
====

run-sa-learn.py is a tool that I run from incron whenever a new file is created in SPAM or HAM directories. 

It runs sa-learn --ham and --spam on these dirs, depending on which is which. 

For archiving reasons the run-sa-learn.py tool does not delete spam/ham after processing. 

Sa-learn will not re-learn already learned mails, unless run with --forget. I do this with a separate crontab in order to archive the mails for a certain number of months. 

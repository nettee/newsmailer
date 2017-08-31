.PHONY: sendmail

sendmail:
	@echo `date` >> sendmail.log
	./sendmail.py >> sendmail.log 2>&1
	@echo '====================================' >> sendmail.log

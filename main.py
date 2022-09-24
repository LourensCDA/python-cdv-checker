import pprint
import logging
import shared
import verboselogs
import coloredlogs  # doesn't want to install on system but works in virtual env
from db_setup import setup_CDV

# initialise logging
# using package verboselogs https://pypi.org/project/verboselogs/
logger = verboselogs.VerboseLogger("verbose")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# package that provides colors on loggin
# https://pypi.org/project/coloredlogs/
coloredlogs.install(level=logging.DEBUG, logger=logger)

sql_db = setup_CDV()

banking_details = {
    "account_number": "123456789",
    "branch_code": "632005",
    "account_type": "Savings",
}

logger.debug(f"\nOriginal details provided: {banking_details}")

# initialise class for cdv check
cdv = shared.cdv_class(sql_db, **banking_details)

# check if branch exists
branch = cdv.return_branch()
if branch:
    logger.success("Branch exists")
    logger.info(
        f"\nBranch details\nBank: {branch['member_name']} \nBranch: {branch['branch_name']}\nClosed: {branch['Closed']}",
    )
else:
    logger.error("Branch does not exist")

# check if account type is valid
if cdv.banking_details["account_type_no"] == 4:
    logger.error("Account type: Invalid")
else:
    logger.success("Account type: Valid")

# check if account number is valid
response = cdv.cdv_check()
pprint.pprint(response)

import pprint
import logging
import shared
import coloredlogs
from db_setup import setup_CDV

logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG, logger=logger)

sql_db = setup_CDV()

banking_details = {
    "account_number": "123456789",
    "branch_code": "250655",
    "account_type": "Savings2",
}

cdv = shared.cdv_class(sql_db, **banking_details)

# check if branch exists
branch = cdv.return_branch()
if branch:
    logger.info("Branch exists")
    logger.debug(
        f"\nBranch details\nBank: {branch['member_name']} \nBranch: {branch['branch_name']}\nClosed: {branch['Closed']}",
    )
else:
    logger.error("Branch does not exist")

# check if account type is valid
if cdv.banking_details["account_type_no"] == 4:
    logger.error("Account type: Invalid")
else:
    logger.info("Account type: Valid")

pprint.pprint(cdv.banking_details)

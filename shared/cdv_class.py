from .sqlite_helper import *

# class that handles bank account validation using algorythm check
class cdv_class:
    ## initialise class
    # params:
    #   sql_db: sqlite database connection
    #   banking_details: dictinoary with banking details
    #     banking_details = {
    #       "account_number": "123456789",
    #       "branch_code": "250655",
    #       "account_type": "Savings",
    #      }
    def __init__(self, db_file, **banking_details):
        self.db_file = db_file
        self.banking_details = banking_details
        self.set_account_type_number()

    ## validate account type number
    def set_account_type_number(self):
        ## account default to 4 if invalid account type is provided
        ## current account
        acc_type_no = (
            1
            if self.banking_details["account_type"].lower() in ("cheque", "current")
            else 4
        )
        ## savings account
        acc_type_no = (
            2
            if self.banking_details["account_type"].lower() in ("savings")
            else acc_type_no
        )
        ## transmission account
        acc_type_no = (
            3
            if self.banking_details["account_type"].lower() in ("transmission")
            else acc_type_no
        )
        self.banking_details["account_type_no"] = acc_type_no

    ## return branch details for branch
    def return_branch(self):
        sql = f"""SELECT * FROM view_branch_details WHERE branch_no = '{self.banking_details["branch_code"]}'"""
        if sqlite_select_data(self.db_file, sql):
            return sqlite_select_data(self.db_file, sql)[0]
        else:
            return None

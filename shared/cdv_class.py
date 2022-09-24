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
        self.banking_details["branch_code"] = (
            "000000" + self.banking_details["branch_code"]
        )[-6:]
        self.banking_details["account_number"] = (
            self.banking_details["account_number"]
            .replace(" ", "")
            .replace("-", "")
            .strip()
        )

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

    ## return cdv pass or fail
    def cdv_check(self):
        output = {"success": None, "message": "Could not validate account"}
        # exclude branch codes not catered for
        if self.banking_details["branch_code"] in ("678910", "679000"):
            return {"success": True, "message": "Unable to validate this branch"}
        # Invalid account type
        if self.banking_details["account_type_no"] == 4:
            return {"success": False, "message": "Invalid account type"}
        # return branch details
        branch = self.return_branch()
        # if branch does not exist then fail
        if not branch:
            return {"success": False, "message": "Branch does not exist"}
        # if branch closed then fail
        if branch["Closed"] == "Y":
            return {"success": False, "message": "Branch closed"}
        # if account number is empty then fail
        if not self.banking_details["account_number"]:
            return {"success": False, "message": "Account number not provided"}
        # if account number contains non numeric characters then fail
        if not self.banking_details["account_number"].isnumeric():
            return {"success": False, "message": "Account number not numeric"}
        return output

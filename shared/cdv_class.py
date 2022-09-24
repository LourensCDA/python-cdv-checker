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
        self.banking_details["account_number_length"] = len(
            self.banking_details["account_number"]
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

    ## standard bank SA checks
    def standard_bank_checks(self, branch_code):
        outcome = None
        if (
            branch_code != "000000"
            and self.banking_details["account_number_length"] == 11
            and self.banking_details["account_number"][:1] != "0"
            and self.banking_details["branch_code"] != branch_code
        ):
            return {"success": False, "message": "Account number must start with 0"}
        if (
            branch_code == "051001"
            and self.banking_details["account_number_length"] == 11
            and self.banking_details["account_number"][:1] != "1"
            and self.banking_details["branch_code"] == branch_code
        ):
            return {"success": False, "message": "Account number must start with 1"}
        if (
            branch_code == "000000"
            and self.banking_details["account_number_length"] == 13
            and self.banking_details["account_number"][3] not in (2, 4)
        ):
            return {"success": False, "message": "Account number invalid"}
        return outcome

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
        # standard bank checks
        if (
            branch["member_name"].lower() == "standard bank"
            or self.banking_details["branch_code"] == "051001"
        ):
            if (
                branch["country"].lower() == "south africa"
                or self.banking_details["branch_code"] == "051001"
            ):
                output = self.standard_bank_checks("051001")
            elif branch["country"].lower() == "namibia":
                output = self.standard_bank_checks("087373")
            elif branch["member_name"].upper() in (
                "STANDARD BANK SWAZILAND",
                "STANDARD LESOTHO BANK",
                "STANDARD LESOTHO BANK LTD",
            ):
                output = self.standard_bank_checks("000000")
            if output:
                return output
        # check for branch code 087373
        if (
            self.banking_details["branch_code"] == "087373"
            and self.banking_details["account_number_length"] == 11
            and self.banking_details["account_number"][:1] != "6"
        ):
            return {"success": False, "message": "Account number must start with 6"}
        # check for habib bank
        if (
            branch["member_name"].upper() == "HABIB OVERSEAS BANK LIMITED"
            and self.banking_details["account_number_length"] == 11
            and self.banking_details["account_number"][:1] != "0"
        ):
            return {"success": False, "message": "Account number must start with 0"}
        # get weighting factor
        self.banking_details["account_number_fmt"] = (
            ("00000000000" + self.banking_details["account_number"])[-11:]
            if self.banking_details["account_number_length"] < 11
            else self.banking_details["account_number"]
        )
        # get weighting factor
        wf = sqlite_select_data(
            self.db_file,
            f"""SELECT * FROM view_weighting_factor WHERE branch_no = '{self.banking_details["branch_code"]}' and CDVAccType = '{self.banking_details["account_type_no"]}'""",
        )[0]
        # if no weighting factor return default
        if not wf or wf["EFT_CDV_AccInd"] == 0:
            return output
        return output

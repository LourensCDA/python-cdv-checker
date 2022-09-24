import shared
import zipfile
import os


def setup_CDV():
    # create intial CIM900 data table
    sql_db = shared.create_connection("cim900.db")
    shared.create_table(
        sql_db,
        "CREATE TABLE IF NOT EXISTS cim900_data (_data text);",
    )

    # create view for branches
    shared.create_table(
        sql_db,
        "CREATE VIEW IF NOT EXISTS view_branch_details AS select distinct trim(substr(_data,3,6)) AS branch_no,trim(substr(_data,9,30)) AS branch_name,(case when (trim(substr(_data,9,30)) like '%closed%') then 'Y' else 'N' end) AS Closed,trim(substr(_data,39,30)) AS member_name,trim(substr(_data,77,6)) AS member_no,trim(substr(_data,273,35)) AS country from cim900_data;",
    )

    # create view for weighting factor
    shared.create_table(
        sql_db,
        "CREATE VIEW IF NOT EXISTS view_weighting_factor AS SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 0)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 0)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 0)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 0)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 0)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 0)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 0)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 0)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 0)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 0)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 0)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 1)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 1)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 1)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 1)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 1)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 1)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 1)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 1)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 1)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 1)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 1)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 2)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 2)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 2)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 2)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 2)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 2)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 2)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 2)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 2)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 2)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 2)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 3)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 3)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 3)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 3)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 3)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 3)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 3)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 3)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 3)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 3)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 3)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 4)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 4)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 4)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 4)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 4)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 4)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 4)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 4)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 4)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 4)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 4)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 5)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 5)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 5)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 5)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 5)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 5)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 5)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 5)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 5)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 5)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 5)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 6)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 6)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 6)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 6)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 6)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 6)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 6)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 6)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 6)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 6)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 6)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 7)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 7)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 7)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 7)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 7)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 7)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 7)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 7)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 7)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 7)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 7)), 1)) AS EFT_CDV_StatusInd FROM cim900_data  UNION SELECT DISTINCT TRIM(SUBSTR(_data, 3, 6)) AS branch_no, TRIM(SUBSTR(_data, (725 + (37 * 8)), 1)) AS CDVAccType, TRIM(SUBSTR(_data, (726 + (37 * 8)), 22)) AS EFT_CDV_Weight, TRIM(SUBSTR(_data, (748 + (37 * 8)), 2)) AS EFT_CDV_Fudge, TRIM(SUBSTR(_data, (750 + (37 * 8)), 2)) AS EFT_CDV_Mod, TRIM(SUBSTR(_data, (752 + (37 * 8)), 2)) AS EFT_CDV_Remain, TRIM(SUBSTR(_data, (754 + (37 * 8)), 2)) AS EFT_CDV_Pos, TRIM(SUBSTR(_data, (756 + (37 * 8)), 1)) AS EFT_CDV_Dig1, TRIM(SUBSTR(_data, (757 + (37 * 8)), 1)) AS EFT_CDV_Dig2, TRIM(SUBSTR(_data, (758 + (37 * 8)), 1)) AS EFT_CDV_AccInd, TRIM(SUBSTR(_data, (759 + (37 * 8)), 2)) AS EFT_CDV_ExcepType, TRIM(SUBSTR(_data, (761 + (37 * 8)), 1)) AS EFT_CDV_StatusInd FROM cim900_data;",
    )

    # extract CIM900.zip
    with zipfile.ZipFile("CIM900.zip", "r") as zip_ref:
        zip_ref.extractall(".")

    # read CIM900 file
    with open("CIM900", "r") as f:
        data = f.readlines()

    # remove file
    os.remove("CIM900")

    # insert data into table
    shared.insert_data_many(
        sql_db,
        "INSERT OR IGNORE INTO cim900_data VALUES (?);",
        [(x,) for x in data],
    )

    return sql_db


if __name__ == "__main__":
    import pprint

    sql_db = setup_CDV()

    print("Branch details:")
    pprint.pprint(
        shared.select_data(sql_db, "SELECT * FROM view_branch_details limit 2;")
    )

    print("Weighting factors:")
    pprint.pprint(
        shared.select_data(sql_db, "SELECT * FROM view_weighting_factor limit 2;")
    )

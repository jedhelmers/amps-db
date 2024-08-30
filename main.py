import csv
import db
import json
import os
import sqlite3

import queries
import utilities


if __name__ == "__main__":
    db.import_data()
    # brands = queries.get_all_brands()

    # for brand in brands:
    #     print(brand)
    #     print(queries.get_all_parts_by_brand(brand))

    # print(brands)
    # print(
    #     json.dumps(
    #         queries.get_all_parts_by_amp('Vibro-Champ'),
    #         indent=2,
    #         ensure_ascii=False
    #     )
    # )
    # 

    resistors = queries.get_all_resistors_by_amp_grouped('Vibro-Champ')
    print(
        json.dumps(
            utilities.to_csv(resistors),
            indent=2,
            ensure_ascii=False
        )
    )

    caps = queries.get_all_capacitors_by_amp_grouped('Vibro-Champ')
    print(
        json.dumps(
            utilities.to_csv(caps),
            indent=2,
            ensure_ascii=False
        )
    )

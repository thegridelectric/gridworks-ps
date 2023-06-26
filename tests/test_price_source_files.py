from gwprice.dev_utils.price_source_files import *


def test_eprt_sync_uid_by_source_file():
    uid_by_file = get_eprt_sync_uid_by_source_file()
    file_by_uid = get_eprt_sync_source_file_by_uid()
    assert set(file_by_uid.values()) == set(uid_by_file.keys())
    assert set(file_by_uid.keys()) == set(uid_by_file.values())
    assert uid_by_file == {
        "input_data/electricity_prices/caiso/eprt__w.caiso.n15__2020__gw.up50.csv": "0c3c167d-fa6d-4ebc-969e-1ffe808c9eb6",
        "input_data/electricity_prices/caiso/eprt__w.caiso.n15__2018__caisoenergyonline.from5min.dubious.csv": "4c96665c-21c4-4e28-8ef2-d87a0192d3d5",
        "input_data/electricity_prices/caiso/eprt__w.caiso.n15__2019__caisoenergyonline.from5min.dubious.csv": "e37ada67-de50-45a0-996d-de29e91428f9",
        "input_data/electricity_prices/caiso/eprt__w.caiso.n15__2019__gw.stdev.up200.csv": "60785ab7-f3e0-449b-a352-67a66db6ee19",
        "input_data/electricity_prices/isone/eprt__w.isone.4001__2019.csv": "9f8e9dd1-ac19-41eb-b95d-0e482df7919e",
        "input_data/electricity_prices/isone/eprt__w.isone.4001__2020.csv": "dd84a579-9737-47d9-bf02-7a089e9c656f",
        "input_data/electricity_prices/isone/eprt__w.isone.4001__2021.csv": "df3f8137-7787-4ac5-abd9-ae1b705379e1",
        "input_data/electricity_prices/isone/eprt__w.isone.4001__2022.csv": "d1a301bf-0a62-41b3-ade2-57dc4fe16235",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__2020.csv": "4cfba22e-fa07-43ea-a7e4-a8babb4f7bcc",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__2021.csv": "d9d102a6-0392-4a23-9bdc-aad9a3bccd33",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__2022.csv": "66b3435d-7784-4b1b-94db-0115a19f1df3",
        "input_data/electricity_prices/isone/eprt__w.isone.4008__2019__gw.da.predicted.rolling4wks.alpha.csv": "e080f0c7-cebc-4cb1-b032-e77004fec11b",
        "input_data/electricity_prices/ng/eprt__w.ng__20210825.csv": "3907f438-aa82-4d51-a243-8739e0d382fe",
        "input_data/electricity_prices/isone/eprt__w.isone.4001_DAnotRT__2020.csv": "3907f438-aa82-4d51-a243-8739e0d382f1",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__gwpathwaysalpha__2020.csv": "ed40f2c4-524c-4329-9d9f-fcac2c18d663",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__gwpathwaysalpha__2022.csv": "298f3170-90c6-42dd-8cb1-a7c820ad7409",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__gwpathwaysbeta__2020.csv": "cd82637b-5535-4228-b087-c76637547277",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__gwpathwaysbeta__2021.csv": "1b77cd4f-bd76-4c2c-8ed7-2e6870982bd2",
        "input_data/electricity_prices/isone/eprt__w.isone.stetson__gwpathwaysbeta__2022.csv": "2c1ee59c-de41-4855-8476-7a2ef0e9f9f5",
        "input_data/electricity_prices/isone/eprt__w.isone.suroweic__2019.csv": "4cfba22e-fa07-43fa-a7e4-a8babb4f7bcc",
    }


def test_distp_sync_uid_by_source_file():
    uid_by_file = get_distp_sync_uid_by_source_file()
    file_by_uid = get_distp_sync_source_file_by_uid()
    assert set(file_by_uid.values()) == set(uid_by_file.keys())
    assert set(file_by_uid.keys()) == set(uid_by_file.values())
    assert uid_by_file == {
        "input_data/electricity_prices/isone/distp__w.isone.stetson__2020__gw.me.versant.a1.res.ets.csv": "78ca8f20-7024-4178-8cf9-bfafc3813cad",
        "input_data/electricity_prices/isone/distp__w.isone.stetson__2021__gw.me.versant.a1.res.ets.csv": "b7d96b56-9e9d-4f3a-92bb-bd90c0907f6e",
        "input_data/electricity_prices/isone/distp__w.isone.stetson__2022__gw.me.versant.a1.res.ets.csv": "43949171-3561-475b-86bc-42280c3b63f7",
        "input_data/electricity_prices/caiso/distp__w.caiso.n15.rcea__2018__gw.ca.rcea.offpeak1.csv": "243bcd06-c8b6-4c81-83a9-47e3b82da267",
        "input_data/electricity_prices/caiso/distp__w.caiso.n15.rcea__2019__gw.ca.rcea.offpeak1.csv": "16391f17-84b2-4a19-b676-a48bdeef4682",
    }

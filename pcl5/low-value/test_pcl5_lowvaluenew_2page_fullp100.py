import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 2Page_fullp100.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-fullp100.obj=438e71f9989037ea7ecd4e8b8e31d99463d470df605e450aa6f8bdafa83551fc
    +test_classification:System
    +name: test_pcl5_lowvaluenew_2page_fullp100
    +test:
        +title: test_pcl5_lowvaluenew_2page_fullp100
        +guid:285c1e5f-3de9-4bad-a274-6c223d750e67
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_2page_fullp100(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in','stationery')
    printjob.print_verify('438e71f9989037ea7ecd4e8b8e31d99463d470df605e450aa6f8bdafa83551fc', timeout=600)
    outputsaver.save_output()

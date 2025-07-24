import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 54Page_rasarro2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:54Page-rasarro2.obj=1922ee0b38c91dbfa2fbce7d19e2ccba5c7c8f258a7964125fd9042b8996ae9e
    +test_classification:System
    +name: test_pcl5_highvalue_54page_rasarro2
    +test:
        +title: test_pcl5_highvalue_54page_rasarro2
        +guid:8bf1f002-5aaa-46d2-9d8f-0068010d2850
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_54page_rasarro2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1922ee0b38c91dbfa2fbce7d19e2ccba5c7c8f258a7964125fd9042b8996ae9e', timeout=600,expected_jobs=2)
    outputsaver.save_output()

import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_isosub.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-isosub.obj=0f8d17d33852a6066c4d500314c30fafca94eda2fb1bdc20177d1fd309c69715
    +test_classification:System
    +name: test_pcl5_highvalue_6page_isosub
    +test:
        +title: test_pcl5_highvalue_6page_isosub
        +guid:4eba00d6-a2e8-4e60-b666-cd66a848a031
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

def test_pcl5_highvalue_6page_isosub(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0f8d17d33852a6066c4d500314c30fafca94eda2fb1bdc20177d1fd309c69715')
    outputsaver.save_output()

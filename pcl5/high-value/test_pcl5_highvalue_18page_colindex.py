import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 18Page_colindex.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:18Page-colindex.obj=0f362987b25f6b3f37e22ee648d2d496d652b741aa76ccd6cc383754ec515357
    +test_classification:System
    +name: test_pcl5_highvalue_18page_colindex
    +test:
        +title: test_pcl5_highvalue_18page_colindex
        +guid:41b327e8-2b19-4228-a140-43774837b108
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

def test_pcl5_highvalue_18page_colindex(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0f362987b25f6b3f37e22ee648d2d496d652b741aa76ccd6cc383754ec515357')
    outputsaver.save_output()

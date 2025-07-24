import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_vector_clip.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-vector_clip.obj=5b201bf01bc7def91688729da98de56fd369a3b6156120a547bbb2b2bf07d163
    +test_classification:System
    +name: test_pcl5_highvalue_5page_vector_clip
    +test:
        +title: test_pcl5_highvalue_5page_vector_clip
        +guid:aab2c320-9858-405f-8ca6-a329b201506a
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

def test_pcl5_highvalue_5page_vector_clip(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5b201bf01bc7def91688729da98de56fd369a3b6156120a547bbb2b2bf07d163', timeout=300)
    outputsaver.save_output()

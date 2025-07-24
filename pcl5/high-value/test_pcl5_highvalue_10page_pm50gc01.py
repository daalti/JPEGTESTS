import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 10Page_pm50gc01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:10Page-pm50gc01.obj=1d7370a0431231673204ea11d4147331d0fbf06dad6507bed407f62ad6c1c963
    +test_classification:System
    +name: test_pcl5_highvalue_10page_pm50gc01
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_10page_pm50gc01
        +guid:400cb021-ad7b-43c1-a40f-be8ca3cfa1f7
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

def test_pcl5_highvalue_10page_pm50gc01(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1d7370a0431231673204ea11d4147331d0fbf06dad6507bed407f62ad6c1c963',timeout=600,expected_jobs=3)
    outputsaver.save_output()

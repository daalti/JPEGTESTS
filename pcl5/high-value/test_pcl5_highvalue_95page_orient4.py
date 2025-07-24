import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669605 pcl5 highvalue using 95Page_orient4.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:95Page-orient4.obj=edbb9a9ea16456cfa09a51ef5a5f10a280d3f5260f2ac94c03d23c9afa03495e
    +test_classification:System
    +name: test_pcl5_highvalue_95page_orient4
    +test:
        +title: test_pcl5_highvalue_95page_orient4
        +guid:0e8326a8-48e8-4c23-b3e4-5600bd5deff4
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

    +overrides:
        +Home:
            +is_manual:False
            +timeout:1500
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_95page_orient4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('edbb9a9ea16456cfa09a51ef5a5f10a280d3f5260f2ac94c03d23c9afa03495e', timeout=1500)
    outputsaver.save_output()

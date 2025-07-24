import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 23Page_inter.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:23Page-inter.obj=58717738b2086e0c6c0f902e714a09e5f77dd5ba277c940a03395d5b14884cc8
    +test_classification:System
    +name: test_pcl5_basicfunctionality_23page_inter
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_23page_inter
        +guid:9d447eaa-8051-4650-a306-14272c78dae3
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
def test_pcl5_basicfunctionality_23page_inter(setup_teardown, printjob, outputsaver):
    printjob.print_verify('58717738b2086e0c6c0f902e714a09e5f77dd5ba277c940a03395d5b14884cc8', timeout=300)
    outputsaver.save_output()

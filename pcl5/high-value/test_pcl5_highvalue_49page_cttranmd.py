import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 49Page_cttranmd.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:49Page-cttranmd.obj=90767eb6259158c8099ad9e1b28fa17923c32003d0428163b02b99af1d39013f
    +test_classification:System
    +name: test_pcl5_highvalue_49page_cttranmd
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_49page_cttranmd
        +guid:20601706-af77-4a52-baff-43de5870ac38
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
def test_pcl5_highvalue_49page_cttranmd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('90767eb6259158c8099ad9e1b28fa17923c32003d0428163b02b99af1d39013f', timeout=600)
    outputsaver.save_output()

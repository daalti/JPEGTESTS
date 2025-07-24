import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 37Page_syntax.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:37Page-syntax.obj=a9806b0ed0c972e665ea4f060c43410bfbeb1ceb8763e154bbfae1a8f7f9bcbe
    +test_classification:System
    +name: test_pcl5_highvalue_37page_syntax
    +test:
        +title: test_pcl5_highvalue_37page_syntax
        +guid:204331a6-6012-4a31-93ff-70e777cf6e98
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

def test_pcl5_highvalue_37page_syntax(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a9806b0ed0c972e665ea4f060c43410bfbeb1ceb8763e154bbfae1a8f7f9bcbe', timeout=600)
    outputsaver.save_output()

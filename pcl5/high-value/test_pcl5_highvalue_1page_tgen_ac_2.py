import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_tgen_ac_2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-tgen_ac_2.obj=da798212dac9bf916cd71b6a053d0908fb99da1f1eb33a6f66d0a4cf6e17dfe8
    +test_classification:System
    +name: test_pcl5_highvalue_1page_tgen_ac_2
    +test:
        +title: test_pcl5_highvalue_1page_tgen_ac_2
        +guid:bba7d940-117a-44c7-99ec-c830be59ad14
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

def test_pcl5_highvalue_1page_tgen_ac_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('da798212dac9bf916cd71b6a053d0908fb99da1f1eb33a6f66d0a4cf6e17dfe8', timeout=600)
    outputsaver.save_output()

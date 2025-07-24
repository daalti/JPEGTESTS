import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 119Page_pclunits.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:119Page-pclunits.obj=f357059e8610f2db86b6c7477cff887820970a864373700f3dc44188402e7239
    +test_classification:System
    +name: test_pcl5_highvalue_119page_pclunits
    +test:
        +title: test_pcl5_highvalue_119page_pclunits
        +guid:2468eed1-6130-4bd3-8632-d2614f51578d
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

def test_pcl5_highvalue_119page_pclunits(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f357059e8610f2db86b6c7477cff887820970a864373700f3dc44188402e7239', timeout=3600)
    outputsaver.save_output()

import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ttfdes.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttfdes.obj=3fb2e8b2fecba5a7b4f1164bf2965b1dd7a66e11e300f90bf4dacb02e7c7999e
    +test_classification:System
    +name: test_pcl5_pcl_fontf_tt_ttfdes
    +test:
        +title: test_pcl5_pcl_fontf_tt_ttfdes
        +guid:2903db80-1d19-4411-b7bd-a163ac315e90
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_tt_ttfdes(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3fb2e8b2fecba5a7b4f1164bf2965b1dd7a66e11e300f90bf4dacb02e7c7999e', timeout=900)
    outputsaver.save_output()

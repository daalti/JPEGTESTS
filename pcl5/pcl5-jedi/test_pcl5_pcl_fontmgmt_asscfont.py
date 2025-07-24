import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using asscfont.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:asscfont.obj=f36340dbfdb0b84053ac2336c691fcf971d375c8ee0cf36dcd0fd4462b5f035d
    +test_classification:System
    +name: test_pcl5_pcl_fontmgmt_asscfont
    +test:
        +title: test_pcl5_pcl_fontmgmt_asscfont
        +guid:557dd6d6-6455-4087-9836-0f5f327ae25d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontmgmt_asscfont(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f36340dbfdb0b84053ac2336c691fcf971d375c8ee0cf36dcd0fd4462b5f035d', timeout=600)
    outputsaver.save_output()

import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sc.obj=65ac845e33bcc793482b5e99b673aef0850a7e245d7727917321bfd67f99908f
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_sc
    +test:
        +title: test_pcl5_hpgl_cfgstat_sc
        +guid:b656599f-9b1d-462c-b900-f1c267b874a6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_sc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('65ac845e33bcc793482b5e99b673aef0850a7e245d7727917321bfd67f99908f', timeout=600)
    outputsaver.save_output()

import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pw_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pw_tt.obj=c1bc483810f7894e6b8fcbea64be2c41176f22c672e5ba5165df8bb1671f8272
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_tt_pw_tt
    +test:
        +title: test_pcl5_hpgl_lfatt_tt_pw_tt
        +guid:451a2deb-7bbc-45fe-b2bc-91f950e622af
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_tt_pw_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c1bc483810f7894e6b8fcbea64be2c41176f22c672e5ba5165df8bb1671f8272', timeout=600)
    outputsaver.save_output()
